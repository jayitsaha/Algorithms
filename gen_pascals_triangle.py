"""
gen_pascals_triangle.py  —  Notion page rebuild for Pascal's Triangle (LeetCode #118)
Uses inline Notion helpers (notion_lib.py has a TOKEN syntax error from concurrent edits).
Run: python3 gen_pascals_triangle.py
"""
import json, time, urllib.request, urllib.error

TOKEN = "NOTION_TOKEN_REDACTED"
NOTION_VERSION = "2022-06-28"
GITHUB_PAGES = "https://jayitsaha.github.io/Algorithms/"
BASE = "https://api.notion.com/v1"
PAGE_ID = "39193418-809c-81b8-b0ba-de70a040cd88"

_HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}


def _req(method, path, body=None):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    last = None
    for attempt in range(7):
        r_obj = urllib.request.Request(url, data=data, method=method, headers=_HEADERS)
        try:
            with urllib.request.urlopen(r_obj) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            code = e.code
            payload = e.read().decode()[:500]
            last = f"{code}: {payload}"
            if code == 429:
                wait = float(e.headers.get("Retry-After", 2))
                time.sleep(min(wait, 12))
                continue
            if code >= 500:
                time.sleep(min(2 ** attempt, 12))
                continue
            raise RuntimeError(f"Notion {method} {path} -> {last}")
        except urllib.error.URLError:
            time.sleep(min(2 ** attempt, 12))
            last = "network"
    raise RuntimeError(f"failed after retries -> {last}")


def _ann(bold=False, italic=False, code=False, color="default"):
    return {"bold": bold, "italic": italic, "strikethrough": False,
            "underline": False, "code": code, "color": color}


def _split(text, size=1900):
    text = "" if text is None else str(text)
    if not text:
        return [{"type": "text", "text": {"content": ""}}]
    return [{"type": "text", "text": {"content": text[i:i+size]}}
            for i in range(0, len(text), size)]


def rt(text, bold=False, italic=False, code=False, color="default"):
    a = _ann(bold, italic, code, color)
    runs = _split(text)
    for run in runs:
        run["annotations"] = a
    return runs


def rich(parts):
    out = []
    for p in parts:
        if isinstance(p, str):
            t, kw = p, {}
        elif isinstance(p, (list, tuple)) and len(p) == 2 and isinstance(p[1], dict):
            t, kw = p[0], p[1]
        else:
            continue
        a = _ann(kw.get("bold", False), kw.get("italic", False),
                 kw.get("code", False), kw.get("color", "default"))
        for run in _split(t):
            run["annotations"] = a
            out.append(run)
    return out


def h2(t): return {"type": "heading_2", "heading_2": {"rich_text": rt(t)}}
def h3(t): return {"type": "heading_3", "heading_3": {"rich_text": rt(t)}}
def h4(t): return {"type": "paragraph", "paragraph": {"rich_text": rt(t, bold=True)}}
def para(x): r = x if isinstance(x, list) else rt(x); return {"type": "paragraph", "paragraph": {"rich_text": r}}
def cb(t, lang="python"): return {"type": "code", "code": {"language": lang, "rich_text": _split(t)}}
def divider(): return {"type": "divider", "divider": {}}
def callout(x, emoji="💡", color="gray_background"):
    r = x if isinstance(x, list) else rt(x)
    return {"type": "callout", "callout": {"rich_text": r, "icon": {"type": "emoji", "emoji": emoji}, "color": color}}
def bullet(x): r = x if isinstance(x, list) else rt(x); return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": r}}
def tog3(t, children): return {"type": "heading_3", "heading_3": {"rich_text": rt(t), "is_toggleable": True, "children": children}}
def emb(url): return {"type": "embed", "embed": {"url": url}}
def tbl(rows, header=True):
    w = max(len(r) for r in rows)
    trows = [{"type": "table_row", "table_row": {"cells": [rt(str(c)) for c in r] + [rt("")]*(w-len(r))}} for r in rows]
    return {"type": "table", "table": {"table_width": w, "has_column_header": header, "has_row_header": False, "children": trows}}


def get_children(pid):
    out, cursor = [], None
    while True:
        path = f"/blocks/{pid}/children?page_size=100" + (f"&start_cursor={cursor}" if cursor else "")
        d = _req("GET", path)
        out += d["results"]
        if d.get("has_more"): cursor = d["next_cursor"]
        else: break
    return out


def wipe_page(pid):
    n = 0
    for b in get_children(pid):
        _req("DELETE", f"/blocks/{b['id']}")
        n += 1
    return n


def append_blocks(pid, blocks, chunk=40):
    for i in range(0, len(blocks), chunk):
        _req("PATCH", f"/blocks/{pid}/children", {"children": blocks[i:i+chunk]})


# ══ CONTENT ══════════════════════════════════════════════════════════════════

SOL1 = """\
def generate(numRows: int) -> list[list[int]]:
    result = [[1]]                         # Seed: Row 0 is the DP base case
    for i in range(1, numRows):            # Build rows 1..numRows-1
        prev = result[-1]                  # Look up the already-solved subproblem
        new_row = [1]                      # Left edge always 1: C(i,0)=1
        for j in range(1, len(prev)):      # Interior cells: sum of two parents above
            new_row.append(prev[j-1] + prev[j])
        new_row.append(1)                  # Right edge always 1: C(i,i)=1
        result.append(new_row)             # Store row; it becomes prev next iteration
    return result                          # DP table IS the answer
"""

SOL2 = """\
from functools import lru_cache

def generate(numRows: int) -> list[list[int]]:
    @lru_cache(maxsize=None)
    def C(n, k):                           # Memoised binomial coefficient
        if k == 0 or k == n: return 1      # Base cases: edges always 1
        return C(n-1, k-1) + C(n-1, k)    # Pascal's Identity

    return [[C(i, j) for j in range(i+1)]
            for i in range(numRows)]
"""

SOL3 = """\
def generate(numRows: int) -> list[list[int]]:
    result = []
    for _ in range(numRows):
        # zip-shift: pair prev with offset copy -> pairwise sums = interior cells
        row = [1] + [a+b for a,b in zip(result[-1], result[-1][1:])] + [1] \\
              if result else [1]
        result.append(row)
    return result
"""

REC = """\
# Pascal's Identity (the DP recurrence):
#
# C(n, 0) = 1                        # left edge base case
# C(n, n) = 1                        # right edge base case
# C(n, k) = C(n-1, k-1) + C(n-1, k) # interior cells — DP transition
#
# In code:  new_row[j] = prev[j-1] + prev[j]  ≡  C(n,k) = C(n-1,k-1)+C(n-1,k)
"""

# ── 1. Set properties ─────────────────────────────────────────────────────────
print("Setting properties...")
props = {
    "Difficulty": {"select": {"name": "Easy"}},
    "Status": {"select": {"name": "Solved"}},
    "Number": {"rich_text": rt("118")},
    "Pattern": {"multi_select": [{"name": "Dynamic Programming"}]},
    "Subpattern": {"multi_select": [{"name": "Add Two Above"}]},
    "Source": {"select": {"name": "LeetCode"}},
    "Time Complexity": {"rich_text": rt("O(numRows^2)")},
    "Space Complexity": {"rich_text": rt("O(numRows^2)")},
    "Key Insight": {"rich_text": rt(
        "Each interior cell = sum of two cells above (Pascal's Identity). "
        "Classic bottom-up DP: every row built from the previously stored row."
    )},
}
_req("PATCH", f"/pages/{PAGE_ID}", {"properties": props, "icon": {"type": "emoji", "emoji": "🟢"}})
print("Properties OK.")

# ── 2. Wipe old body ──────────────────────────────────────────────────────────
print("Wiping old body...")
deleted = wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3. Build content ──────────────────────────────────────────────────────────
blocks = []

# PROBLEM
blocks += [
    h2("Problem"),
    para(rich([
        ("Given an integer ", {}),
        ("numRows", {"code": True}),
        (", return the first ", {}),
        ("numRows", {"code": True}),
        (" rows of Pascal's Triangle. In Pascal's Triangle, each number is the sum of "
         "the two numbers directly above it. "
         "The first and last element of every row is always 1.", {}),
    ])),
    callout(rich([
        ("Example: ", {"bold": True}),
        ("numRows = 5", {"code": True}),
        ("  →  [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]\n", {}),
        ("Constraints: 1 <= numRows <= 30", {"italic": True}),
    ]), "📋", "blue_background"),
    divider(),
]

# SOLUTION 1
blocks += [
    h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    tog3("💡 Intuition: How to Arrive at This", [
        h4("Reframe the Problem"),
        para("We need to produce numRows rows, where each row is fully determined by the previous row. "
             "What do we keep? Just the last completed row. This is exactly bottom-up DP / tabulation: "
             "store solved subproblem results and look them up to solve larger ones."),
        h4("What Doesn't Work"),
        para("The factorial formula C(n,k)=n!/(k!(n-k)!) overflows for n=30 (30! > 10^32). "
             "A pure recursive approach without caching recomputes the same cells exponentially — "
             "C(4,1) appears in both the C(5,1) and C(5,2) expansion trees."),
        h4("The Key Observation"),
        para("Row i depends ONLY on row i-1. Once row i-1 is stored, each interior cell "
             "of row i is just prev[j-1]+prev[j] — a single addition, no overflow, no redundancy. "
             "The output IS the DP table, so we waste no space by storing every row."),
        h4("Building the Solution"),
        para("1. Seed: result=[[1]] — Row 0, the DP base case.\n"
             "2. Loop i from 1 to numRows-1.\n"
             "3. prev=result[-1] — look up the solved subproblem.\n"
             "4. new_row=[1] — left edge. Interior: append prev[j-1]+prev[j]. Append 1 — right edge.\n"
             "5. result.append(new_row). After the loop, return result."),
        callout(
            "Analogy: A pyramid of champagne glasses. Each glass fills from the overflow of the two "
            "directly above it. Fill one level at a time — never look more than one level above. "
            "This is exactly the 'previous row only' DP pattern.",
            "🥂", "green_background"
        ),
    ]),
    h3("Why Is This Dynamic Programming?"),
    para(rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("Row i is completely determined by row i-1. Building row i requires first building row i-1 — "
         "it is a genuinely necessary subproblem.\n", {}),
        ("Overlapping Subproblems: ", {"bold": True}),
        ("In naive recursion, C(5,2) requires C(4,1) and C(4,2); C(4,2) requires C(3,1) and C(3,2); "
         "C(4,1) also requires C(3,1). C(3,1) is computed twice. "
         "Tabulation avoids this by storing each row once.", {}),
    ])),
    cb(REC, "python"),
    h3("Code"),
    cb(SOL1, "python"),
    h3("Line by Line"),
    para(rich([("result = [[1]]", {"code": True}),
               (" — Initialize the DP table with Row 0. Base case: C(0,0)=1, one way to choose 0 from nothing.", {})])),
    para(rich([("for i in range(1, numRows):", {"code": True}),
               (" — Iterate from row 1 to numRows-1. Row 0 is already seeded.", {})])),
    para(rich([("prev = result[-1]", {"code": True}),
               (" — Look up the last completed row — the solved subproblem we stored and now reuse.", {})])),
    para(rich([("new_row = [1]", {"code": True}),
               (" — Every row begins with 1. Left-edge base case: C(i,0)=1.", {})])),
    para(rich([("for j in range(1, len(prev)):", {"code": True}),
               (" — Loop over interior positions only. For row i, runs i-1 times "
                "(j=0 left edge is pre-placed; j=i right edge is added after).", {})])),
    para(rich([("new_row.append(prev[j-1] + prev[j])", {"code": True}),
               (" — DP transition: interior cell = left parent + right parent from prev row. "
                "This is Pascal's Identity: C(n,k) = C(n-1,k-1) + C(n-1,k).", {})])),
    para(rich([("new_row.append(1)", {"code": True}),
               (" — Right-edge base case: C(i,i)=1. Added after interior loop completes.", {})])),
    para(rich([("result.append(new_row)", {"code": True}),
               (" — Store the completed row in our DP table. Becomes prev next iteration.", {})])),
    para(rich([("return result", {"code": True}),
               (" — The DP table IS the answer. Return the full accumulated list of rows.", {})])),
    callout(
        "Time: O(numRows²) — total cells = 1+2+...+numRows = numRows*(numRows+1)/2.\n"
        "Space: O(numRows²) — output space; we cannot do better since output IS the triangle.",
        "⏱️", "purple_background"
    ),
    divider(),
]

# SOLUTION 2
blocks += [
    h2("Solution 2 — Top-Down DP / Memoization"),
    tog3("💡 Intuition: How to Arrive at This", [
        h4("Reframe the Problem"),
        para("Define a recursive function C(n,k) returning the value at row n, column k. "
             "Cache every result so each unique (n,k) pair is computed only once."),
        h4("The Key Observation"),
        para("Pascal's Identity is a direct recurrence: C(n,k) = C(n-1,k-1) + C(n-1,k). "
             "Base cases: C(n,0)=1 (left edge) and C(n,n)=1 (right edge). "
             "With @lru_cache, each (n,k) pair is computed at most once — O(numRows²) total."),
        h4("Building the Solution"),
        para("1. Define @lru_cache C(n,k) with base cases.\n"
             "2. Build triangle: [[C(i,j) for j in range(i+1)] for i in range(numRows)].\n"
             "3. The cache is populated on first calls; subsequent calls are O(1) lookups."),
    ]),
    h3("Code"),
    cb(SOL2, "python"),
    h3("Line by Line"),
    para(rich([("@lru_cache(maxsize=None)", {"code": True}),
               (" — Memoization decorator. Caches (n,k) → value. Each unique pair computed once.", {})])),
    para(rich([("if k == 0 or k == n: return 1", {"code": True}),
               (" — Both edge base cases. Stops recursion at triangle boundaries.", {})])),
    para(rich([("return C(n-1, k-1) + C(n-1, k)", {"code": True}),
               (" — Pascal's Identity as recursive call. Cache makes subsequent (n-1,k-1)/(n-1,k) O(1).", {})])),
    para(rich([("return [[C(i,j) for j in range(i+1)] for i in range(numRows)]", {"code": True}),
               (" — Build full triangle. Cache warm by end; most calls are hits.", {})])),
    callout(
        "Prefer memoization over tabulation when: (1) you only need certain cells (sparse access), "
        "or (2) the recurrence is more naturally expressed recursively. "
        "For Pascal's Triangle, tabulation is simpler and avoids Python recursion overhead.",
        "💡", "green_background"
    ),
    divider(),
]

# SOLUTION 3
blocks += [
    h2("Solution 3 — Zip-Shift One-Liner (Pythonic)"),
    tog3("💡 Intuition: How to Arrive at This", [
        h4("The Key Observation"),
        para("Interior cells of each new row are pairwise sums of adjacent elements in prev. "
             "In Python, zip(prev, prev[1:]) generates all adjacent pairs at once. "
             "Summing each pair gives the interior cells. Prepend and append 1 for edges."),
        h4("Example Trace"),
        para("prev = [1, 3, 3, 1]\n"
             "prev[1:] = [3, 3, 1]\n"
             "zip -> (1,3), (3,3), (3,1)\n"
             "sums -> 4, 6, 4\n"
             "new_row = [1] + [4,6,4] + [1] = [1,4,6,4,1]  (correct Row 4)"),
    ]),
    h3("Code"),
    cb(SOL3, "python"),
    callout(
        "Trade-off: Clever and Pythonic but harder to explain at a whiteboard. "
        "Use Solution 1 in interviews — it directly demonstrates DP reasoning. "
        "Offer this as a follow-up when asked for the most concise Python version.",
        "⚠️", "yellow_background"
    ),
    divider(),
]

# COMPLEXITY
blocks += [
    h2("Complexity"),
    tbl([
        ["Solution", "Time", "Space", "Notes"],
        ["Bottom-Up DP (Sol 1)", "O(numRows²)", "O(numRows²)", "Interview pick — clearest DP reasoning"],
        ["Top-Down Memo (Sol 2)", "O(numRows²)", "O(numRows²)", "Same asymptotically; lru_cache overhead"],
        ["Zip One-Liner (Sol 3)", "O(numRows²)", "O(numRows²)", "Pythonic; same complexity"],
    ]),
    para("All three solutions share O(numRows²) time and space. "
         "Total cells = 1+2+...+numRows = numRows*(numRows+1)/2 = O(numRows²), each computed exactly once. "
         "Space is O(numRows²) because the output IS the full triangle — we cannot do better."),
    divider(),
]

# PATTERN CLASSIFICATION
blocks += [
    h2("🏷️ Pattern Classification"),
    para(rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    para(rich([("Sub-Pattern: ", {"bold": True}), ("Add Two Above (Pascal's Identity / Row-by-Row DP)", {})])),
    callout(rich([
        ("When to recognize this pattern:\n", {"bold": True}),
        ("• Build a 2D structure row by row\n"
         "• Each row depends only on the previous row (optimal substructure)\n"
         "• Each interior cell is a simple combination of adjacent cells above\n"
         "• Asked to generate all rows, not find a single value\n"
         "• Clean recurrence: C(n,k) = C(n-1,k-1) + C(n-1,k)", {}),
    ]), "🔎", "green_background"),
    callout(
        "Sub-pattern note: 'Add Two Above' is specific to Pascal's Triangle. "
        "The broader DP pattern — bottom-up tabulation where each state builds from the previous — "
        "applies to Unique Paths, Climbing Stairs, Fibonacci, Coin Change, and many more.",
        "📚", "blue_background"
    ),
    divider(),
]

# RELATED PROBLEMS
blocks += [
    h2("🔗 Related Problems"),
    para("Problems using the same technique (build from previously-stored subproblem results):"),
    bullet(rich([
        ("Pascal's Triangle II", {"bold": True}),
        (" (Easy, #119)", {}),
        (" — Return only the k-th row. Same DP, space-optimized to O(k) with in-place update.", {}),
    ])),
    bullet(rich([
        ("Unique Paths", {"bold": True}),
        (" (Medium, #62)", {}),
        (" — Count grid paths. cell = cell_above + cell_left. Same row-by-row DP.", {}),
    ])),
    bullet(rich([
        ("Triangle", {"bold": True}),
        (" (Medium, #120)", {}),
        (" — Min path sum in triangular structure. Bottom-up DP on the same layout.", {}),
    ])),
    bullet(rich([
        ("Climbing Stairs", {"bold": True}),
        (" (Easy, #70)", {}),
        (" — step = sum of two previous. The 1D analog of 'add two above'.", {}),
    ])),
    bullet(rich([
        ("Coin Change", {"bold": True}),
        (" (Medium, #322)", {}),
        (" — Classic unbounded knapsack. Each DP state depends on previously computed states.", {}),
    ])),
    bullet(rich([
        ("Fibonacci Number", {"bold": True}),
        (" (Easy, #509)", {}),
        (" — F(n)=F(n-1)+F(n-2). Pascal's Triangle is the 2D generalization.", {}),
    ])),
    bullet(rich([
        ("Unique Paths II", {"bold": True}),
        (" (Medium, #63)", {}),
        (" — Unique Paths with obstacles. Same DP with conditional transition.", {}),
    ])),
    para("These problems share the core DP technique: store computed subproblem answers, "
         "then combine adjacent stored values to build the next state."),
    callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming), Row-Building DP.",
        "📚", "gray_background"
    ),
    divider(),
]

# INTERACTIVE EXPLAINER
blocks += [
    h2("🎯 Interactive Visual Explainer"),
    emb(f"{GITHUB_PAGES}pascals_triangle_explainer.html"),
    para(rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append ────────────────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
