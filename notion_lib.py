"""
notion_lib.py — Shared, robust Notion helper for the DSA pipeline regeneration.

Every regeneration agent imports this module so that ALL 538 problem pages get
uniform, correctly-formatted content. Do NOT hand-roll curl JSON in agents.

Key facts about the DSA Mastery Vault database:
  DB properties (exact names): Problem(title), Number(rich_text), Difficulty(select),
    Status(select), Pattern(multi_select), Subpattern(multi_select),
    Sub-Pattern(multi_select, legacy — DO NOT USE), Source(select),
    Time Complexity(rich_text), Space Complexity(rich_text), Key Insight(rich_text),
    Added(created_time). There is NO "Algorithm" property — do not set it.
  Notion supports heading_1/2/3 only (no heading_4 -> use bold paragraph).
  rich_text content max ~2000 chars per run -> long text/code is auto-split.
  Multi-select options auto-create on write.

Usage in an agent's gen_<slug>.py:
    import notion_lib as N
    N.set_properties(PAGE_ID, difficulty="Easy", number=242, pattern="Hashing",
                     subpatterns=["Frequency Count"], tc="O(n)", sc="O(1)",
                     key_insight="Compare character counts.", icon="🟢")
    N.wipe_page(PAGE_ID)
    blocks = [ N.h2("Problem"), N.para("..."), N.divider(), ... ]
    N.append_blocks(PAGE_ID, blocks)
"""
import json, time, urllib.request, urllib.error

def _load_token():
    import os, base64
    v = os.environ.get("NOTION_TOKEN")
    if v and v.startswith("ntn_"):
        return v
    try:
        s = open(os.path.expanduser("~/.config/ndsa_tok")).read().strip()
        d = base64.b64decode(s).decode()
        if d.startswith("ntn_"):
            return d
    except Exception:
        pass
    return base64.b64decode("bnRuXzM5NTI4NzI2Njg0N2FHTXVKNnhuQjRkdTMyTFN0U2FUT2NVdFFucDBhcTQ0elY=").decode()
TOKEN = _load_token()
NOTION_VERSION = "2022-06-28"
DB_ID = "39e4c077-47fc-4288-b6a0-00491ae3fb20"
BASE = "https://api.notion.com/v1"
GITHUB_PAGES = "https://jayitsaha.github.io/Algorithms/"

_HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}


def _req(method, path, body=None):
    """HTTP with retry/backoff on 429 and 5xx."""
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    last = None
    for attempt in range(7):
        req = urllib.request.Request(url, data=data, method=method, headers=_HEADERS)
        try:
            with urllib.request.urlopen(req) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            code = e.code
            payload = e.read().decode()[:500]
            last = f"{code}: {payload}"
            if code == 429:
                wait = float(e.headers.get("Retry-After", 2))
                time.sleep(min(wait, 12));  continue
            if code >= 500:
                time.sleep(min(2 ** attempt, 12));  continue
            raise RuntimeError(f"Notion {method} {path} -> {last}")
        except urllib.error.URLError:
            time.sleep(min(2 ** attempt, 12));  last = "network"
    raise RuntimeError(f"Notion {method} {path} failed after retries -> {last}")


# ─────────────────────────── rich text ───────────────────────────
def _ann(bold=False, italic=False, code=False, color="default"):
    return {"bold": bold, "italic": italic, "strikethrough": False,
            "underline": False, "code": code, "color": color}


def _split(text, size=1900):
    text = "" if text is None else str(text)
    if text == "":
        return [{"type": "text", "text": {"content": ""}}]
    return [{"type": "text", "text": {"content": text[i:i + size]}}
            for i in range(0, len(text), size)]


def rt(text, bold=False, italic=False, code=False, color="default"):
    """Rich text array from a single string (auto-split if long)."""
    a = _ann(bold, italic, code, color)
    runs = _split(text)
    for run in runs:
        run["annotations"] = a
    return runs


def rich(parts):
    """Rich text from mixed runs. parts = list of str or (str, kwargs-dict).
    Example: rich([("i", {'code':True}), " is the index"]) """
    out = []
    for p in parts:
        if isinstance(p, str):
            t, kw = p, {}
        else:
            t, kw = p[0], (p[1] or {})
        a = _ann(kw.get("bold", False), kw.get("italic", False),
                 kw.get("code", False), kw.get("color", "default"))
        for run in _split(t):
            run["annotations"] = a
            out.append(run)
    return out


# ─────────────────────────── block builders ───────────────────────────
def h2(text):
    return {"type": "heading_2", "heading_2": {"rich_text": rt(text)}}


def h3(text):
    return {"type": "heading_3", "heading_3": {"rich_text": rt(text)}}


def h4(text):
    # Notion has no heading_4; render as bold paragraph.
    return {"type": "paragraph", "paragraph": {"rich_text": rt(text, bold=True)}}


def para(text_or_rich):
    r = text_or_rich if isinstance(text_or_rich, list) else rt(text_or_rich)
    return {"type": "paragraph", "paragraph": {"rich_text": r}}


def code(text, lang="python"):
    return {"type": "code", "code": {"language": lang, "rich_text": _split(text)}}


def divider():
    return {"type": "divider", "divider": {}}


def callout(text_or_rich, emoji="💡", color="gray_background"):
    r = text_or_rich if isinstance(text_or_rich, list) else rt(text_or_rich)
    return {"type": "callout", "callout": {
        "rich_text": r, "icon": {"type": "emoji", "emoji": emoji}, "color": color}}


def bullet(text_or_rich):
    r = text_or_rich if isinstance(text_or_rich, list) else rt(text_or_rich)
    return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": r}}


def numbered(text_or_rich):
    r = text_or_rich if isinstance(text_or_rich, list) else rt(text_or_rich)
    return {"type": "numbered_list_item", "numbered_list_item": {"rich_text": r}}


def toggle_h3(text, children):
    """Collapsible heading_3 with nested children (used for Intuition section)."""
    return {"type": "heading_3", "heading_3": {
        "rich_text": rt(text), "is_toggleable": True, "children": children}}


def quote(text_or_rich):
    r = text_or_rich if isinstance(text_or_rich, list) else rt(text_or_rich)
    return {"type": "quote", "quote": {"rich_text": r}}


def embed(url):
    return {"type": "embed", "embed": {"url": url}}


def table(rows, has_col_header=True):
    """rows = list of lists of cell strings. First row is header if has_col_header."""
    width = max(len(r) for r in rows)
    trows = []
    for r in rows:
        cells = [rt(str(c)) for c in r] + [rt("")] * (width - len(r))
        trows.append({"type": "table_row", "table_row": {"cells": cells}})
    return {"type": "table", "table": {
        "table_width": width, "has_column_header": has_col_header,
        "has_row_header": False, "children": trows}}


# ─────────────────────────── page operations ───────────────────────────
def get_children(page_id):
    out, cursor = [], None
    while True:
        path = f"/blocks/{page_id}/children?page_size=100"
        if cursor:
            path += f"&start_cursor={cursor}"
        d = _req("GET", path)
        out += d["results"]
        if d.get("has_more"):
            cursor = d["next_cursor"]
        else:
            break
    return out


def wipe_page(page_id):
    """Delete every existing top-level child block (the 'redo' step)."""
    n = 0
    for b in get_children(page_id):
        _req("DELETE", f"/blocks/{b['id']}")
        n += 1
    return n


def append_blocks(page_id, blocks, chunk=40):
    """Append blocks in chunks (Notion limit 100/req; 40 is safe with nesting)."""
    for i in range(0, len(blocks), chunk):
        _req("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i + chunk]})


def set_properties(page_id, difficulty, number, pattern, subpatterns,
                   tc, sc, key_insight, icon=None, status="Solved", source="LeetCode"):
    subs = subpatterns if isinstance(subpatterns, (list, tuple)) else [subpatterns]
    pats = pattern if isinstance(pattern, (list, tuple)) else [pattern]
    props = {
        "Difficulty": {"select": {"name": difficulty}},
        "Status": {"select": {"name": status}},
        "Number": {"rich_text": rt(str(number))},
        "Pattern": {"multi_select": [{"name": p} for p in pats if p]},
        "Subpattern": {"multi_select": [{"name": s} for s in subs if s]},
        "Source": {"select": {"name": source}},
        "Time Complexity": {"rich_text": rt(tc)},
        "Space Complexity": {"rich_text": rt(sc)},
        "Key Insight": {"rich_text": rt(key_insight)},
    }
    body = {"properties": props}
    if icon:
        body["icon"] = {"type": "emoji", "emoji": icon}
    _req("PATCH", f"/pages/{page_id}", body)


def create_page(name, number, difficulty, icon):
    body = {"parent": {"database_id": DB_ID},
            "icon": {"type": "emoji", "emoji": icon},
            "properties": {
                "Problem": {"title": rt(name)},
                "Number": {"rich_text": rt(str(number))},
                "Difficulty": {"select": {"name": difficulty}}}}
    d = _req("POST", "/pages", body)
    return d["id"]


def embed_url_for(slug):
    return f"{GITHUB_PAGES}{slug}_explainer.html"
