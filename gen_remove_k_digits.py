"""gen_remove_k_digits.py — Notion in-place update for Remove K Digits (LC #402)"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-816d-9936-c04e0eee76aa"

# ── 1) Set properties ─────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=402,
    pattern="Stack / Queue",
    subpatterns=["Remove Larger Digits First"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Maintain a non-decreasing stack; pop stack-top when it is larger than the incoming digit (and k > 0) to greedily minimize each position from left to right.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ─────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ─────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("num", {"code": True}),
        (" representing a non-negative integer and an integer ", {}),
        ("k", {"code": True}),
        (", remove ", {}),
        ("k", {"code": True}),
        (" digits from the number so that the new number is the smallest possible. "
         "Return the result as a string. If the result has leading zeros, remove them. "
         "If the result is empty, return \"0\".", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("num = \"1432219\", k = 3", {"code": True}),
        (" → Output: ", {}),
        ("\"1219\"", {"code": True}),
        (". Remove digits 4, 3, 2 (in that order — each larger than its successor) to get the smallest result.", {})
    ])),
    N.callout(
        N.rich([
            ("Key insight: ", {"bold": True}),
            ("The leftmost digit has the highest place value. Whenever a digit is larger than its successor, removing it is always better — it moves a smaller digit to a more significant position. This greedy exchange argument justifies the monotonic stack approach.", {})
        ]),
        "💡", "green_background"
    ),
    N.divider()
]

# ── Solution 1: Monotonic Stack (Interview Pick) ──────────────────────────────
sol1_code = """\
def removeKdigits(num: str, k: int) -> str:
    stack = []                          # non-decreasing candidate answer
    for d in num:                       # scan left to right
        while stack and k and stack[-1] > d:
            stack.pop()                 # remove a larger digit at high place value
            k -= 1                      # one removal used
        stack.append(d)                 # current digit fits — push
    result = stack[:len(stack) - k]     # if k>0 remain, trim from tail
    return ''.join(result).lstrip('0') or '0'  # strip leading zeros\
"""

sol1_lineby = [
    ("stack = []", "Initialize an empty stack. This will hold our candidate answer digits in non-decreasing order."),
    ("for d in num:", "Scan each digit left to right. Each digit will be processed exactly once."),
    ("while stack and k and stack[-1] > d:", "Pop condition: stack has elements, removals remain (k > 0), and the top is larger than incoming. All three must hold."),
    ("stack.pop()", "Remove the stack top — it occupies a higher place value than 'd' and is larger, so removing it strictly decreases the number."),
    ("k -= 1", "Decrement the removal budget. When k reaches 0, no more pops can happen."),
    ("stack.append(d)", "Push current digit. Either the while condition was false from the start, or we just finished popping enough elements."),
    ("result = stack[:len(stack) - k]", "If k > 0 after the full scan, the stack is non-decreasing (pops couldn't be triggered). Trim k digits from the right (the largest remaining). IMPORTANT: use len(stack)-k, not -k, because stack[:-0] = [] in Python."),
    ("return ''.join(result).lstrip('0') or '0'", "Join digits, strip leading zeros. If result becomes empty (e.g. \"0000\"), return \"0\"."),
]

blocks += [
    N.h2("Solution 1 — Monotonic Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're choosing a subsequence of length (n - k) from the number's digits (preserving order) that is lexicographically smallest. Position matters: the leftmost digit dominates the number's magnitude."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all C(n, n-k) subsequences. For n=10^4 and k=5000, this is astronomical. We need a smarter structure."),
        N.h4("The Key Observation"),
        N.para("If digits form a 'peak' (e.g., ...4 3...), the 4 is hurting us — it puts a larger value at a higher position than the 3 that follows. Removing 4 moves 3 to that position, strictly reducing the number. This works for ANY such peak, and we should process peaks greedily from left to right."),
        N.h4("Building the Solution"),
        N.para("We need to compare each incoming digit against the most recent 'accepted' digit. A stack gives us O(1) access to that digit. When we pop, we automatically expose the next candidate for comparison — no extra bookkeeping. This gives us a clean O(n) algorithm."),
        N.callout("Analogy: Think of building a number digit by digit. Each time a new (smaller) digit arrives, it's like a better candidate for that position — so you hand back the old (larger) digit (pop) and use the new one instead. You only have k 'returns' to make.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
]

for line, explanation in sol1_lineby:
    blocks.append(N.para(N.rich([
        (line, {"code": True, "bold": True}),
        (" — " + explanation, {})
    ])))

blocks.append(N.callout(
    N.rich([
        ("Why not stack[:-k]? ", {"bold": True}),
        ("In Python, list[:-0] returns an empty list, not the full list. When k=0 after the scan (all removals used during popping), you must keep the entire stack. stack[:len(stack)-0] = stack[:len(stack)] = full stack. This is a subtle but critical correctness issue.", {})
    ]),
    "⚠️", "yellow_background"
))
blocks.append(N.divider())

# ── Solution 2: Brute Force ───────────────────────────────────────────────────
sol2_code = """\
from itertools import combinations

def removeKdigits_brute(num: str, k: int) -> str:
    n, target = len(num), len(num) - k
    best = '9' * target                    # worst possible sentinel
    for keep in combinations(range(n), target):
        cand = ''.join(num[i] for i in keep).lstrip('0') or '0'
        if cand < best:
            best = cand
    return best
    # Time: O(C(n,k) * n) — exponential. Fine for n<=15, hopeless for n=10^4.\
"""

blocks += [
    N.h2("Solution 2 — Brute Force: All Subsequences"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the minimum of all (n-k)-length subsequences of the digit string. The brute force simply enumerates them all."),
        N.h4("What Doesn't Work"),
        N.para("For large n (up to 10^5 in the problem constraints), C(n, n-k) is astronomically large. Even for n=40 and k=20, C(40,20) ≈ 137 billion. This only serves as a correctness reference."),
        N.h4("The Key Observation"),
        N.para("Useful for verifying the greedy solution on small test cases. In an interview, mention this first to show you understand the problem, then optimize."),
        N.h4("Building the Solution"),
        N.para("Use itertools.combinations to generate all ways to choose (n-k) indices. Build each subsequence, strip leading zeros, track the minimum lexicographically."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.divider()
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all subsequences)", "O(C(n,k)·n) — exponential", "O(n)"],
        ["Monotonic Stack (optimal) ✓", "O(n) amortized", "O(n)"],
    ]),
    N.para(N.rich([
        ("Amortized O(n) explanation: ", {"bold": True}),
        ("Each digit is pushed exactly once and popped at most once across the entire algorithm. So despite the nested while loop, total push+pop operations ≤ 2n = O(n).", {})
    ])),
    N.divider()
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stack / Queue", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Remove Larger Digits First (Monotonic Non-Decreasing Stack)", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) 'Remove k elements to minimize/maximize a number or sequence' — greedy + stack. "
             "(2) 'Find next greater/smaller element' — monotonic stack with opposite direction. "
             "(3) Any time you need to maintain a running candidate with an invariant (non-increasing or non-decreasing) and eager replacement of bad elements.", {})
        ]),
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──────────────────────────────────────────────────────────
related = [
    ("Remove Duplicate Letters", "Medium", "#316", "Same greedy stack but must keep exactly one of each letter; uses a last-occurrence array to decide when it's safe to pop"),
    ("Monotone Increasing Digits", "Medium", "#738", "Greedy digit manipulation to maintain non-decreasing digit order; closely related single-pass approach"),
    ("Daily Temperatures", "Medium", "#739", "Monotonically decreasing stack of indices to find next warmer day — next-greater variant"),
    ("Largest Rectangle in Histogram", "Hard", "#84", "Monotonically increasing stack; pop when bar height drops to compute area — monotonic stack for optimization"),
    ("Sum of Subarray Minimums", "Medium", "#907", "Previous/next smaller element computation using monotonic stack; contribution counting"),
    ("Create Maximum Number", "Hard", "#321", "Select digits from two arrays to form the maximum k-length number — same greedy subsequence selection logic"),
]

blocks += [N.h2("🔗 Related Problems"), N.para("Problems using the same technique:")]
for name, diff, num, note in related:
    blocks.append(N.bullet(N.rich([
        (name + " ", {"bold": True}),
        (f"({diff}) {num} — {note}", {})
    ])))

blocks += [
    N.para("These problems share the monotonic stack invariant: aggressively discard bad elements from the top when a better candidate arrives."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue Patterns → Monotonic Stack → Remove Larger Digits First", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("remove_k_digits")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
