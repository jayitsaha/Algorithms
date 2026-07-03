"""gen_first_bad_version.py — Notion update for First Bad Version (LC #278)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81cd-a6a5-f8ef8f73f91d"
SLUG = "first_bad_version"

def lbl(code_text, explanation):
    """Helper: code snippet + plain explanation text as rich text list."""
    return [("", {})] if False else N.rich([
        (code_text, {"code": True}),
        (" — " + explanation, {}),
    ])

# ── 1) Set page properties ───────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=278,
    pattern="Binary Search",
    subpatterns=["BS: First/Last Occurrence"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Versions form a monotone F...FT...T sequence; binary search (lower bound) finds the first T in O(log n) API calls.",
    icon="🟢",
)
print("Properties set OK")

# ── 2) Wipe existing body ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3) Build body blocks ─────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para("You are a product manager and the latest product has n versions [1, 2, ..., n]. One version is bad and all versions after it are also bad. You are given an API isBadVersion(version) that returns True if the version is bad. Implement a function to find the first bad version. Minimize the number of calls to the API."),
    N.para("Example: n=5, bad=4. isBadVersion answers: F F F T T. Answer: 4."),
    N.divider(),
]

# ── Solution 1: Binary Search Lower Bound (Interview Pick) ──
sol1_code = """\
def firstBadVersion(n: int) -> int:
    lo, hi = 1, n                # search the full range [1, n]
    while lo < hi:               # while more than one candidate remains
        mid = lo + (hi - lo) // 2  # midpoint, overflow-safe
        if isBadVersion(mid):    # bad: first bad is at mid or earlier
            hi = mid             # keep mid in range - it might be the answer
        else:                    # good: first bad is strictly after mid
            lo = mid + 1         # safely exclude mid
    return lo                    # lo == hi, single candidate is the answer"""

blocks += [
    N.h2("Solution 1 — Binary Search, Lower Bound (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a boolean array isBad[1..n] shaped like: F,F,...,F,T,T,...,T — a monotone sequence. We need the index of the first True. This is the classic Lower Bound binary search problem."),
        N.h4("What Doesn't Work"),
        N.para("A linear scan checks every version one by one — up to n API calls. When n is 2^31 - 1, that is over 2 billion calls. The isBadVersion API is expensive (a full build pipeline per call). O(n) is completely infeasible."),
        N.h4("The Key Observation"),
        N.para("The version sequence is MONOTONE: once a version is bad, all subsequent ones are bad. If we check any midpoint: if bad, the answer is at mid-or-left; if good, the answer is strictly to the right. We always halve the search space in one API call."),
        N.h4("Building the Solution"),
        N.para("1. Maintain [lo, hi] as the candidate range. Invariant: first bad is always in [lo, hi].\n2. Compute mid = lo + (hi-lo)//2 (overflow-safe for large n).\n3. If isBad(mid) is True: set hi=mid (keep mid, it could be the answer).\n4. If isBad(mid) is False: set lo=mid+1 (mid is good, safely exclude it).\n5. When lo==hi, return lo — that is the first bad version."),
        N.callout(
            "Analogy: A book where pages 1..k are 'good' and k+1..n are 'bad'. Open to the middle — if bad, the first bad page is in the left half (including where you opened). If good, it is in the right half. You never need to read every page.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Binary Search — Lower Bound Deep Dive"),
    N.para(N.rich([
        ("Pattern: ", {"bold": True}),
        ("Lower Bound (First True). Given a monotone boolean predicate P over [lo, hi], find the smallest x such that P(x) = True.", {}),
    ])),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("At all times, the answer is within [lo, hi]. Each iteration shrinks the interval by at least half. Terminates in O(log n) steps.", {}),
    ])),
    N.para(N.rich([
        ("Critical rule: ", {"bold": True}),
        ("When P(mid)=True, use hi=mid (NOT hi=mid-1). Mid itself may be the answer. When P(mid)=False, use lo=mid+1 to safely exclude mid.", {}),
    ])),
    N.para(N.rich([
        ("Overflow safety: ", {"bold": True}),
        ("Use lo + (hi-lo)//2, not (lo+hi)//2. When both are near 2^31, their sum overflows a 32-bit signed integer in Java/C++.", {}),
    ])),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(lbl("lo, hi = 1, n", "Initialize search to full range. Loop invariant: first bad version is in [lo, hi] throughout.")),
    N.para(lbl("while lo < hi:", "Continue while more than one candidate remains. When lo==hi, we have our answer.")),
    N.para(lbl("mid = lo + (hi-lo)//2", "Overflow-safe midpoint. For lo=1, hi=8: mid=1+3=4.")),
    N.para(lbl("if isBadVersion(mid):", "One API call per iteration. This is the only expensive operation.")),
    N.para(lbl("hi = mid", "Mid is bad. First bad is at mid or to the left. Keep mid in range — it could be the answer. Do NOT use mid-1.")),
    N.para(lbl("lo = mid + 1", "Mid is good. First bad is strictly to the right. Safe to exclude mid entirely.")),
    N.para(lbl("return lo", "lo==hi, one candidate remains. By the loop invariant, it must be the first bad version.")),
    N.divider(),
]

# ── Solution 2: Linear Scan ──
sol2_code = """\
def firstBadVersion(n: int) -> int:
    for v in range(1, n + 1):  # check every version from 1 to n
        if isBadVersion(v):    # first True we encounter is the answer
            return v           # O(n) calls -- TLE for large n"""

blocks += [
    N.h2("Solution 2 — Linear Scan (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Check versions one by one from earliest. The first version where isBadVersion returns True is the answer — simple and correct."),
        N.h4("What Doesn't Work"),
        N.para("For n up to 2^31-1, this makes up to ~2 billion API calls. In real systems, each call is a full build pipeline invocation. This gets Time Limit Exceeded on LeetCode for large inputs."),
        N.h4("The Key Observation"),
        N.para("Use this approach to establish correctness in an interview, then say: 'I notice the sequence is monotone, so we can do much better with binary search — O(log n) calls instead of O(n).'"),
        N.h4("Building the Solution"),
        N.para("Iterate v from 1 to n. Call isBadVersion(v). Return v at the first True. Since versions are monotone, the first True is guaranteed to be the first bad version."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(lbl("for v in range(1, n+1):", "Iterate every version number from 1 to n inclusive.")),
    N.para(lbl("if isBadVersion(v):", "Call the API. Since versions are monotone, the first True is the first bad version.")),
    N.para(lbl("return v", "Return immediately — all subsequent versions are also bad, but we want only the first.")),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "API Calls (n=2^31)"],
        ["Linear Scan", "O(n)", "O(1)", "~2 billion"],
        ["Binary Search (Lower Bound)", "O(log n)", "O(1)", "at most 31"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BS: First/Last Occurrence (Lower Bound — find first True in monotone predicate)", {})])),
    N.callout(
        "When to recognize this pattern: (1) Monotone property — once condition becomes True it stays True. (2) You need the FIRST position satisfying the condition. (3) Linear scan is too expensive — problem says minimize API calls or implies O(log n).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same Binary Search Lower Bound technique:"),
    N.bullet(N.rich([("Search Insert Position", {"bold": True}), (" (Easy, #35) — lower bound on a sorted array; find leftmost insertion index for target", {})])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array", {"bold": True}), (" (Medium, #153) — binary search the rotation boundary", {})])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium, #875) — binary search on answer space with a monotone feasibility check", {})])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), (" (Medium, #1011) — same binary search on answer pattern with monotone predicate", {})])),
    N.bullet(N.rich([("Find Smallest Divisor", {"bold": True}), (" (Medium, #1283) — binary search with monotone predicate on divisor value", {})])),
    N.bullet(N.rich([("Sqrt(x)", {"bold": True}), (" (Easy, #69) — find largest k where k-squared is at most x; lower bound variant", {})])),
    N.para("These problems all share: a monotone predicate over a range, binary search to find the boundary, and the same update rules (hi=mid when True, lo=mid+1 when False)."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 — Binary Search, Sub-Pattern: BS: First/Last Occurrence", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks queued: {len(blocks)}")
