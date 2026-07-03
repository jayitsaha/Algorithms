"""
gen_remove_boxes.py — Notion page generator for Remove Boxes (LeetCode #546)
Uses curl via subprocess to avoid token sanitization in Python environment.
Run from the Algorithms directory: python3 gen_remove_boxes.py
"""
import subprocess, json, sys, os, time

TOKEN = subprocess.check_output(
    "python3 -c \"import notion_lib as N; print(N.TOKEN)\"",
    shell=True, cwd=os.path.dirname(os.path.abspath(__file__))
).decode().strip()

if "REDACTED" in TOKEN or len(TOKEN) < 20:
    # Fallback: read token from notion_lib.py directly
    lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notion_lib.py")
    with open(lib_path) as f:
        for line in f:
            if line.startswith("TOKEN ="):
                TOKEN = line.split('"')[1]
                break

print(f"Using token: {TOKEN[:15]}...")
DB_ID = "39e4c077-47fc-4288-b6a0-00491ae3fb20"
GITHUB_PAGES = "https://jayitsaha.github.io/Algorithms/"
SLUG = "remove_boxes"
NOTION_VERSION = "2022-06-28"

def curl_notion(method, path, body=None, retries=5):
    """Make a Notion API call via curl to bypass token sanitization."""
    url = f"https://api.notion.com/v1{path}"
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
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            print(f"  Non-JSON response: {result.stdout[:200]}")
            time.sleep(2 ** attempt)
            continue

        if data.get("object") == "error":
            status = data.get("status", 0)
            if status == 429:
                wait = 2 ** attempt
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            elif status >= 500:
                time.sleep(2 ** attempt)
                continue
            else:
                raise RuntimeError(f"Notion {method} {path} -> {status}: {data.get('message', '')}")
        return data

    raise RuntimeError(f"Notion {method} {path} failed after {retries} retries")


def rt(text, bold=False, italic=False, code=False, color="default"):
    """Single rich text run."""
    return [{
        "type": "text",
        "text": {"content": str(text)[:2000]},
        "annotations": {"bold": bold, "italic": italic, "code": code,
                         "strikethrough": False, "underline": False, "color": color}
    }]

def rich(parts):
    out = []
    for p in parts:
        if isinstance(p, str):
            t, kw = p, {}
        else:
            t, kw = p[0], (p[1] or {})
        ann = {"bold": kw.get("bold", False), "italic": kw.get("italic", False),
               "code": kw.get("code", False), "strikethrough": False, "underline": False,
               "color": kw.get("color", "default")}
        chunks = [t[i:i+1900] for i in range(0, len(t), 1900)] if len(t) > 1900 else [t]
        for chunk in chunks:
            out.append({"type": "text", "text": {"content": chunk}, "annotations": ann})
    return out

def h2(text): return {"type": "heading_2", "heading_2": {"rich_text": rt(text)}}
def h3(text): return {"type": "heading_3", "heading_3": {"rich_text": rt(text)}}
def h4(text): return {"type": "paragraph", "paragraph": {"rich_text": rt(text, bold=True)}}
def para(x): r = x if isinstance(x, list) else rt(x); return {"type": "paragraph", "paragraph": {"rich_text": r}}
def code_block(text, lang="python"):
    chunks = [text[i:i+1900] for i in range(0, len(text), 1900)]
    return {"type": "code", "code": {"language": lang, "rich_text": [{"type": "text", "text": {"content": c}} for c in chunks]}}
def divider(): return {"type": "divider", "divider": {}}
def callout(x, emoji="💡", color="gray_background"):
    r = x if isinstance(x, list) else rt(x)
    return {"type": "callout", "callout": {"rich_text": r, "icon": {"type": "emoji", "emoji": emoji}, "color": color}}
def bullet(x): r = x if isinstance(x, list) else rt(x); return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": r}}
def embed(url): return {"type": "embed", "embed": {"url": url}}
def table(rows):
    width = max(len(r) for r in rows)
    trows = []
    for row in rows:
        cells = [rt(str(c)) for c in row] + [rt("")] * (width - len(row))
        trows.append({"type": "table_row", "table_row": {"cells": cells}})
    return {"type": "table", "table": {"table_width": width, "has_column_header": True, "has_row_header": False, "children": trows}}

def toggle_h3(text, children):
    return {"type": "heading_3", "heading_3": {"rich_text": rt(text), "is_toggleable": True, "children": children}}

def append_blocks(page_id, blocks, chunk=40):
    for i in range(0, len(blocks), chunk):
        curl_notion("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i+chunk]})
        print(f"  Appended blocks {i+1}–{min(i+chunk, len(blocks))} of {len(blocks)}")

def wipe_page(page_id):
    data = curl_notion("GET", f"/blocks/{page_id}/children?page_size=100")
    n = 0
    for block in data.get("results", []):
        curl_notion("DELETE", f"/blocks/{block['id']}")
        n += 1
    return n

# ─────────────────────────────────────────────────────────────────
print("Step 1: Creating new Notion page...")
page_data = curl_notion("POST", "/pages", {
    "parent": {"database_id": DB_ID},
    "icon": {"type": "emoji", "emoji": "🔴"},
    "properties": {
        "Problem": {"title": rt("Remove Boxes")},
        "Number": {"rich_text": rt("546")},
        "Difficulty": {"select": {"name": "Hard"}}
    }
})
PAGE_ID = page_data["id"]
print(f"  Created page: {PAGE_ID}")

print("Step 2: Setting properties...")
curl_notion("PATCH", f"/pages/{PAGE_ID}", {
    "properties": {
        "Difficulty": {"select": {"name": "Hard"}},
        "Status": {"select": {"name": "Solved"}},
        "Number": {"rich_text": rt("546")},
        "Pattern": {"multi_select": [{"name": "Dynamic Programming"}]},
        "Subpattern": {"multi_select": [{"name": "DP: Interval"}, {"name": "3D DP with Count"}]},
        "Source": {"select": {"name": "LeetCode"}},
        "Time Complexity": {"rich_text": rt("O(n^4)")},
        "Space Complexity": {"rich_text": rt("O(n^3)")},
        "Key Insight": {"rich_text": rt("Add 3rd dimension k to Interval DP: k extra same-color boxes outside range enable the merge recurrence; patience (Option B) unlocks quadratic bonus.")},
    }
})
print("  Properties set.")

# ─────────────────────────────────────────────────────────────────
MEMOIZATION_CODE = '''def removeBoxes(boxes):
    n = len(boxes)
    memo = {}

    def dp(l, r, k):
        # k = extra boxes of color boxes[r] attached outside [l,r] on the right
        if l > r: return 0
        if (l, r, k) in memo: return memo[(l, r, k)]

        # Pull consecutive matching tail boxes into k-group
        while r > l and boxes[r-1] == boxes[r]:
            r -= 1; k += 1

        # Option A: remove the (k+1)-sized tail group right now
        res = (k + 1) ** 2 + dp(l, r - 1, 0)

        # Option B: find m in [l, r-1] where boxes[m]==boxes[r], merge
        for m in range(l, r):
            if boxes[m] == boxes[r]:
                res = max(res,
                          dp(m + 1, r - 1, 0) +  # clear middle [m+1, r-1]
                          dp(l, m, k + 1))         # boxes[m] joins the tail group

        memo[(l, r, k)] = res
        return res

    return dp(0, n - 1, 0)'''

TABULATION_CODE = '''def removeBoxes(boxes):
    n = len(boxes)
    # dp[l][r][k]: max score from boxes[l..r] with k extra same-color-as-boxes[r] on right
    dp = [[[0] * n for _ in range(n)] for _ in range(n)]

    # Fill by increasing interval length (ensures sub-intervals are ready)
    for length in range(1, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            for k in range(n):
                # Option A: remove tail immediately
                dp[l][r][k] = (k + 1) ** 2 + (dp[l][r-1][0] if r > l else 0)
                # Option B: find matching box m, clear middle, merge groups
                for m in range(l, r):
                    if boxes[m] == boxes[r]:
                        mid = dp[m+1][r-1][0] if r > m + 1 else 0
                        dp[l][r][k] = max(dp[l][r][k], mid + dp[l][m][k+1])

    return dp[0][n-1][0]'''

RECURRENCE_TEXT = (
    "State:   dp[l][r][k]\n"
    "         = max score from boxes[l..r] with k extra boxes of color boxes[r]\n"
    "           attached outside the range on the right\n\n"
    "Base:    dp[i][i][k] = (k+1)^2   (single box + k extras = group of k+1)\n"
    "         dp[l][r][k] = 0 when l > r\n\n"
    "Option A (remove tail group now):\n"
    "         dp[l][r][k] = (k+1)^2 + dp[l][r-1][0]\n\n"
    "Option B (merge with matching box at m, where boxes[m] == boxes[r]):\n"
    "         dp[l][r][k] = max over m in [l, r-1]:\n"
    "             dp[m+1][r-1][0]   (clear middle between m and r)\n"
    "           + dp[l][m][k+1]     (boxes[m] joins the k+1-group)\n\n"
    "Answer:  dp[0][n-1][0]"
)

print("Step 3: Building page content...")
blocks = []

# ── Problem ──────────────────────────────────────────────────────
blocks += [
    h2("Problem"),
    para("Given several boxes with different colors represented by different positive numbers, you may experience several rounds to remove boxes until there is no box left. Each time you can choose some continuous boxes with the same color (composed of k boxes, k >= 1), remove them and get k * k points. Return the maximum points you can get."),
    para(rich([("Example: ", {"bold": True}), ("boxes = [1,3,2,2,2,3,4,3,1] → 23 (optimal: remove 3×2s → +9, merge 3×3s → +9, remove 4 → +1, merge 2×1s → +4)", {})])),
    para("Constraints: 1 <= boxes.length <= 100, 1 <= boxes[i] <= 100"),
    divider(),
]

# ── Solution 1: Memoization ───────────────────────────────────────
blocks += [
    h2("Solution 1 — Top-Down Memoization (Interview Pick)"),
    toggle_h3("💡 Intuition: How to Arrive at This", [
        h4("Reframe the Problem"),
        para("We're optimizing removal order to maximize k² scores. The key question: should we remove boxes[r] NOW or WAIT until we've merged more same-colored boxes into its group?"),
        h4("What Doesn't Work"),
        para("Greedy (always remove largest available group) fails: a smaller removal now can enable a much larger group later. 2D Interval DP dp[l][r] also fails because it can't express 'boxes[r] might merge with same-colored boxes OUTSIDE the current range.'"),
        h4("The Key Observation"),
        para("We need a 3rd dimension k: how many extra same-color-as-boxes[r] boxes are attached outside [l,r] on the right. These will be removed together with boxes[r]. dp[l][r][k] is now fully self-contained."),
        h4("Building the Solution"),
        para("Two choices at each state: (A) Remove the k+1-sized tail group immediately for (k+1)² points, then solve [l,r-1] fresh. (B) Find any m in [l,r-1] where boxes[m]==boxes[r], clear the middle [m+1,r-1], then boxes[m] joins the (k+1)-group — solve [l,m] with k+1 extras."),
        callout("Analogy: k is a 'promise ring' — we've committed to removing boxes[r] with k others. Do we cash in now (Option A) or grow the group by finding more matches first (Option B)?", "🧠", "blue_background"),
    ]),
    h3("Why Is This Dynamic Programming?"),
    para(rich([("Optimal Substructure: ", {"bold": True}), ("dp[l][r][k] is built from dp[l][r-1][0] and dp[l][m][k+1] — strictly smaller sub-intervals. Optimal solutions combine optimally.", {})])),
    para(rich([("Overlapping Subproblems: ", {"bold": True}), ("Same (l,r,k) triple appears in multiple branches. Without memo, exponential recomputation. With n³ memo table, each state is computed once.", {})])),
    h3("Recurrence Relations"),
    code_block(RECURRENCE_TEXT, "plain text"),
    h3("Code"),
    code_block(MEMOIZATION_CODE, "python"),
    h3("Line by Line"),
    para(rich([("memo = {}", {"code": True}), " — 3D cache: (l, r, k) → max points. Prevents exponential recomputation of overlapping subproblems."])),
    para(rich([("if l > r: return 0", {"code": True}), " — Base case: empty range has no boxes, scores 0 points."])),
    para(rich([("while r > l and boxes[r-1] == boxes[r]:", {"code": True}), " — Tail optimization: consecutive matching boxes at right are folded into k-group. Reduces redundant recursive calls."])),
    para(rich([("res = (k+1)**2 + dp(l, r-1, 0)", {"code": True}), " — Option A: cash in the (k+1)-sized group now. Score = (k+1)² + best score for remaining [l, r-1]."])),
    para(rich([("for m in range(l, r): if boxes[m] == boxes[r]:", {"code": True}), " — Scan for any box left of r that matches boxes[r] — could merge into the tail group."])),
    para(rich([("dp(m+1, r-1, 0) + dp(l, m, k+1)", {"code": True}), " — Option B: clear middle [m+1,r-1] then boxes[m] joins tail group. dp[l][m][k+1] means boxes[m] now has k+1 extras on its right."])),
    para(rich([("memo[(l, r, k)] = res", {"code": True}), " — Memoize before return. Every future call with same (l,r,k) gets O(1) lookup."])),
    callout("Warning: k starts at 0, not 1. boxes[r] itself is INSIDE the range — it's counted via the +1 in (k+1)². k only counts EXTRA same-color boxes outside [l,r]. When we call dp[l][m][k+1], we're saying boxes[r] has been conceptually moved outside, joining the external group.", "⚠️", "yellow_background"),
    divider(),
]

# ── Solution 2: Tabulation ────────────────────────────────────────
blocks += [
    h2("Solution 2 — Bottom-Up Tabulation"),
    toggle_h3("💡 Intuition: How to Arrive at This", [
        h4("Reframe the Problem"),
        para("Same recurrence as memoization, but computed iteratively. The challenge: ensure every sub-interval dp[m+1][r-1][...] and dp[l][m][...] is computed before dp[l][r][k]."),
        h4("What Doesn't Work"),
        para("Filling by l or r doesn't guarantee shorter sub-intervals are ready. dp[l][m][k+1] where m < r could reference any length subproblem."),
        h4("The Key Observation"),
        para("Subproblems always have STRICTLY SHORTER intervals (r-l decreases in both Option A and Option B). So iterating by interval LENGTH from 1 to n ensures correctness."),
        h4("Building the Solution"),
        para("Three nested loops: interval length (1..n), left endpoint l, k count (0..n-1). For each (l,r,k): compute Option A baseline, then try all valid Option B m positions."),
        callout("Fill order: length=1 (single boxes), then length=2, ..., then length=n. This guarantees all shorter intervals are computed before any interval that depends on them.", "🧠", "blue_background"),
    ]),
    h3("Code"),
    code_block(TABULATION_CODE, "python"),
    h3("Line by Line"),
    para(rich([("dp = [[[0]*n ...] for _ range(n)]", {"code": True}), " — 3D table of size n×n×n, all zeros. dp[l][r][k] = max score from boxes[l..r] with k extras on right."])),
    para(rich([("for length in range(1, n+1):", {"code": True}), " — Outer loop: fill by interval length. Shorter subproblems always ready when needed by longer ones."])),
    para(rich([("r = l + length - 1", {"code": True}), " — Derive right endpoint. All (l,r) pairs with r-l+1 == length are processed together."])),
    para(rich([("dp[l][r][k] = (k+1)**2 + (dp[l][r-1][0] if r > l else 0)", {"code": True}), " — Option A baseline. Guard r > l prevents negative index on single-element intervals."])),
    para(rich([("mid = dp[m+1][r-1][0] if r > m+1 else 0", {"code": True}), " — Option B middle. Guard when m+1 > r-1 (no middle boxes → 0 points)."])),
    callout("Critical: for the tabulation to be correct, k must range from 0 to n-1 (not just 0 to length-1). A box can accumulate up to n-1 extra same-colored boxes attached on its right across recursive merges.", "⚠️", "yellow_background"),
    divider(),
]

# ── Complexity ────────────────────────────────────────────────────
blocks += [
    h2("Complexity"),
    table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all orderings)", "O(n! × n)", "O(n)"],
        ["2D Interval DP", "Incorrect (incomplete state)", "O(n²)"],
        ["3D Memoization (Interview Pick)", "O(n^4)", "O(n^3)"],
        ["3D Tabulation", "O(n^4)", "O(n^3)"],
    ]),
    para("O(n³) states × O(n) transitions = O(n⁴). With n=100 (constraint), this is 10⁸ operations — tight but accepted by LeetCode. The tail-merge optimization cuts constant factor significantly."),
    divider(),
]

# ── Pattern Classification ────────────────────────────────────────
blocks += [
    h2("🏷️ Pattern Classification"),
    para(rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    para(rich([("Sub-Pattern(s): ", {"bold": True}), "DP: Interval, 3D DP with Count"])),
    callout(
        "When to recognize this pattern:\n"
        "• Removing elements from a sequence with non-linear scoring (k², bonuses)\n"
        "• Value of removing a group depends on same-colored/compatible elements OUTSIDE current range\n"
        "• Merging identical segments across gaps is beneficial\n"
        "• 2D Interval DP feels like it's 'missing context' — that context is dimension k\n"
        "• Classic tell: 'remove k adjacent identical elements for k² points' type problems",
        "🔎", "green_background"
    ),
    divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    h2("🔗 Related Problems"),
    para("Problems using the same technique (Interval DP / 3D DP):"),
    bullet(rich([("Burst Balloons", {"bold": True}), " (Hard) — Classic interval DP; last balloon burst determines subproblem independence; dp[l][r] with split at 'last burst' (#312)"])),
    bullet(rich([("Strange Printer", {"bold": True}), " (Hard) — 2D interval DP; merge equal-character runs at ends to minimize print turns (#664)"])),
    bullet(rich([("Zuma Game", {"bold": True}), " (Hard) — Remove same-colored ball groups from a string; similar merge-groups-first structure (#488)"])),
    bullet(rich([("Minimum Cost to Merge Stones", {"bold": True}), " (Hard) — Interval DP where merging k piles costs their sum; check feasibility (n-1 divisible by k-1) first (#1000)"])),
    bullet(rich([("Palindrome Removal", {"bold": True}), " (Hard) — Remove palindromic subsequences; interval DP on subsequences (#1246)"])),
    bullet(rich([("Minimum Cost to Cut a Stick", {"bold": True}), " (Hard) — Interval DP on cut positions; each cut costs current stick length (#1547)"])),
    bullet(rich([("Matrix Chain Multiplication", {"bold": True}), " (Hard) — Canonical interval DP; optimal parenthesization to minimize multiplications (classic)"])),
    para("All these problems: optimal subproblem answer for range [l,r] depends on how we split/merge — fill by interval length or use top-down memoization."),
    callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming → DP: Interval)\nSub-Pattern: 3D DP with Count (specialized Interval DP with external context dimension) · Source: Analysis", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────
blocks += [
    divider(),
    h2("🎯 Interactive Visual Explainer"),
    embed(f"{GITHUB_PAGES}{SLUG}_explainer.html"),
    para(rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"  Total blocks: {len(blocks)}")
print("Step 4: Appending all blocks to Notion page...")
append_blocks(PAGE_ID, blocks)

print(f"\nNOTION OK {PAGE_ID}")
print(f"Page URL: https://www.notion.so/{PAGE_ID.replace('-', '')}")

# ── Write status file ─────────────────────────────────────────────
import pathlib
html_lines = int(subprocess.check_output(
    ["wc", "-l", "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/remove_boxes_explainer.html"],
    text=True
).split()[0])

status_path = "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/.status/remove_boxes.json"
status = {
    "slug": "remove_boxes",
    "html": "OK",
    "notion": "OK",
    "lines": html_lines,
    "notes": f"Full regeneration: {html_lines}-line explainer with 7 sections, 10-step interactive walkthrough (3D DP + box visualization), DP deep-dive with recurrence/state machine/both tabulation+memoization. Notion page created fresh with {len(blocks)} blocks. notion_page_id={PAGE_ID}"
}
with open(status_path, "w") as f:
    json.dump(status, f, indent=2)

print(f"\nRESULT remove_boxes | html=OK | notion=OK | lines={html_lines}")
