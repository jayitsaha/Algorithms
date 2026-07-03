"""
notion_curl.py — Notion API calls via curl subprocess (bypasses Python SSL issue)
"""
import subprocess, json, time

TOKEN = "NOTION_TOKEN_REDACTED"
NOTION_VERSION = "2022-06-28"
BASE = "https://api.notion.com/v1"
GITHUB_PAGES = "https://jayitsaha.github.io/Algorithms/"


def _curl(method, path, body=None, retries=5):
    url = BASE + path
    cmd = [
        "curl", "-s", "-X", method, url,
        "-H", f"Authorization: Bearer {TOKEN}",
        "-H", f"Notion-Version: {NOTION_VERSION}",
        "-H", "Content-Type: application/json",
    ]
    if body is not None:
        cmd += ["-d", json.dumps(body)]
    for attempt in range(retries):
        result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            d = json.loads(result.stdout)
        except json.JSONDecodeError:
            time.sleep(2 ** attempt)
            continue
        if isinstance(d, dict) and d.get("status") == 429:
            wait = float(d.get("retry_after", 2))
            time.sleep(min(wait, 12))
            continue
        if isinstance(d, dict) and d.get("object") == "error":
            if d.get("status", 0) >= 500:
                time.sleep(min(2 ** attempt, 12))
                continue
            raise RuntimeError(f"Notion {method} {path} -> {d.get('message')}")
        return d
    raise RuntimeError(f"Notion {method} {path} failed after {retries} retries")


def rt(text, bold=False, italic=False, code=False, color="default"):
    """Simple rich text run."""
    ann = {"bold": bold, "italic": italic, "strikethrough": False,
           "underline": False, "code": code, "color": color}
    # Split long text
    runs = []
    text = str(text) if text is not None else ""
    for i in range(0, max(1, len(text)), 1900):
        chunk = text[i:i+1900]
        runs.append({"type": "text", "text": {"content": chunk}, "annotations": ann})
    return runs


def rich(parts):
    """Rich text from list of str or (str, dict) tuples."""
    out = []
    for p in parts:
        if isinstance(p, str):
            t, kw = p, {}
        else:
            t, kw = p[0], (p[1] or {})
        ann = {"bold": kw.get("bold", False), "italic": kw.get("italic", False),
               "strikethrough": False, "underline": False, "code": kw.get("code", False),
               "color": kw.get("color", "default")}
        text = str(t) if t is not None else ""
        for i in range(0, max(1, len(text)), 1900):
            chunk = text[i:i+1900]
            out.append({"type": "text", "text": {"content": chunk}, "annotations": ann})
    return out


def h2(text): return {"type": "heading_2", "heading_2": {"rich_text": rt(text)}}
def h3(text): return {"type": "heading_3", "heading_3": {"rich_text": rt(text)}}
def h4(text): return {"type": "paragraph", "paragraph": {"rich_text": rt(text, bold=True)}}
def para(r):
    rr = r if isinstance(r, list) else rt(r)
    return {"type": "paragraph", "paragraph": {"rich_text": rr}}
def code_block(text, lang="python"):
    # split if needed
    chunks = [text[i:i+1900] for i in range(0, max(1, len(text)), 1900)]
    runs = [{"type": "text", "text": {"content": c}} for c in chunks]
    return {"type": "code", "code": {"language": lang, "rich_text": runs}}
def divider(): return {"type": "divider", "divider": {}}
def callout(r, emoji="💡", color="gray_background"):
    rr = r if isinstance(r, list) else rt(r)
    return {"type": "callout", "callout": {"rich_text": rr, "icon": {"type": "emoji", "emoji": emoji}, "color": color}}
def bullet(r):
    rr = r if isinstance(r, list) else rt(r)
    return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": rr}}
def toggle_h3(text, children):
    return {"type": "heading_3", "heading_3": {"rich_text": rt(text), "is_toggleable": True, "children": children}}
def embed(url): return {"type": "embed", "embed": {"url": url}}
def embed_url(slug): return f"{GITHUB_PAGES}{slug}_explainer.html"


def table(rows, has_col_header=True):
    width = max(len(r) for r in rows)
    trows = []
    for row in rows:
        cells = [rt(str(c)) for c in row] + [rt("")] * (width - len(row))
        trows.append({"type": "table_row", "table_row": {"cells": cells}})
    return {"type": "table", "table": {
        "table_width": width, "has_column_header": has_col_header,
        "has_row_header": False, "children": trows}}


def set_properties(page_id, difficulty, number, pattern, subpatterns, tc, sc, key_insight, icon=None):
    pats = pattern if isinstance(pattern, list) else [pattern]
    subs = subpatterns if isinstance(subpatterns, list) else [subpatterns]
    props = {
        "Difficulty": {"select": {"name": difficulty}},
        "Status": {"select": {"name": "Solved"}},
        "Number": {"rich_text": rt(str(number))},
        "Pattern": {"multi_select": [{"name": p} for p in pats if p]},
        "Subpattern": {"multi_select": [{"name": s} for s in subs if s]},
        "Source": {"select": {"name": "LeetCode"}},
        "Time Complexity": {"rich_text": rt(tc)},
        "Space Complexity": {"rich_text": rt(sc)},
        "Key Insight": {"rich_text": rt(key_insight)},
    }
    body = {"properties": props}
    if icon:
        body["icon"] = {"type": "emoji", "emoji": icon}
    _curl("PATCH", f"/pages/{page_id}", body)


def get_children(page_id):
    out, cursor = [], None
    while True:
        path = f"/blocks/{page_id}/children?page_size=100"
        if cursor:
            path += f"&start_cursor={cursor}"
        d = _curl("GET", path)
        out += d.get("results", [])
        if d.get("has_more"):
            cursor = d["next_cursor"]
        else:
            break
    return out


def wipe_page(page_id):
    n = 0
    for b in get_children(page_id):
        _curl("DELETE", f"/blocks/{b['id']}")
        n += 1
    return n


def append_blocks(page_id, blocks, chunk=40):
    for i in range(0, len(blocks), chunk):
        _curl("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i+chunk]})
