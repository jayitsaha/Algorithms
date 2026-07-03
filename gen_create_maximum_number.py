"""
gen_create_maximum_number.py
Regenerates the Notion page for LeetCode #321 Create Maximum Number in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8185-bcc6-cbccf0a7faa7"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=321,
    pattern="Stack / Queue",
    subpatterns=["Monotonic Stack + Merge"],
    tc="O(k*(m+n+k))",
    sc="O(k)",
    key_insight="Enumerate all valid splits i; for each use monotonic stack for best sub-seqs then greedy suffix-comparison merge.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body ──────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two integer arrays ", {}),
        ("nums1", {"code": True}),
        (" and ", {}),
        ("nums2", {"code": True}),
        (" of lengths ", {}),
        ("m", {"code": True}),
        (" and ", {}),
        ("n", {"code": True}),
        (" respectively, and an integer ", {}),
        ("k", {"code": True}),
        (", create the maximum number of length ", {}),
        ("k", {"code": True}),
        (" from digits of the two numbers. The relative order of the digits from the same array must be preserved. Return an array of the ", {}),
        ("k", {"code": True}),
        (" digits representing the answer.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Monotonic Stack + Greedy Merge ─────────────────────────────
SOL1_CODE = """\
def maxNumber(nums1, nums2, k):
    def max_subseq(nums, p):
        \"\"\"Extract lexicographically largest subsequence of length p.\"\"\"
        drop = len(nums) - p          # discard budget
        stack = []
        for d in nums:
            while drop and stack and stack[-1] < d:
                stack.pop()
                drop -= 1             # spend one discard
            stack.append(d)
        return stack[:p]              # trim if budget unused

    def merge(A, B):
        \"\"\"Merge two sequences into lexicographically largest result.\"\"\"
        res, i, j = [], 0, 0
        while i < len(A) or j < len(B):
            if A[i:] >= B[j:]:        # suffix comparison — handles ties
                res.append(A[i]); i += 1
            else:
                res.append(B[j]); j += 1
        return res

    m, n, best = len(nums1), len(nums2), []
    for i in range(max(0, k - n), min(k, m) + 1):   # valid split range
        s1 = max_subseq(nums1, i)
        s2 = max_subseq(nums2, k - i)
        candidate = merge(s1, s2)
        if candidate > best:           # Python list comparison is lexicographic
            best = candidate
    return best
"""

blocks += [
    N.h2("Solution 1 — Monotonic Stack + Greedy Merge (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the largest k-digit number, drawing from two arrays with order preserved. Think of it as: how many digits do I take from each array? If I fix that split, the rest is deterministic — find best subseq per array, then merge them optimally."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: enumerate all ways to choose i from nums1 and k-i from nums2, try all interleavings — exponential. Greedy 'always pick the largest available digit' fails because it ignores relative order; you can't skip a digit that's earlier in the array just because a later one is bigger."),
        N.h4("The Key Observation"),
        N.para("Decompose into three independent sub-problems: (1) best i-length subsequence of nums1, (2) best (k-i)-length subsequence of nums2, (3) largest merge of those two. Each is solvable in O(n) or O(k). Iterate over all valid i and keep the global best."),
        N.h4("Building the Solution"),
        N.para("max_subseq uses a monotonic decreasing stack with a 'discard budget' of drop = len(nums) - p. Pop the stack top when a larger digit arrives and budget > 0 — greedily replace smaller earlier digits. merge uses suffix comparison A[i:] >= B[j:] to break ties correctly."),
        N.callout(
            "Analogy: Imagine two queues of coins. To build the largest stack of k coins, you first pull the best i coins from queue 1 and best k-i from queue 2. Then combine them, always placing the coin whose remaining pile looks bigger — judging not just the next coin but all future ones.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Monotonic Stack"),
    N.para(N.rich([
        ("Monotonic Stack", {"bold": True}),
        (" is a stack that maintains a strict ordering (increasing or decreasing) among its elements at all times. Here we use a ", {}),
        ("decreasing", {"bold": True}),
        (" variant: every element in the stack from bottom to top is non-increasing. ", {}),
    ])),
    N.para("Origin: Used in O(n) solutions to 'Next Greater Element', 'Largest Rectangle in Histogram', and 'Remove K Digits'. The core idea: when we see a larger value, any smaller values already in the stack that are 'before' it in the result are strictly suboptimal — replace them if we have remaining budget."),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("At every step, the stack contains the best subsequence achievable from digits seen so far, given the remaining discard budget. We never pop when drop = 0 (would leave us unable to reach length p).", {}),
    ])),
    N.para(N.rich([
        ("When to recognize it: ", {"bold": True}),
        ("'Find best k-length subsequence preserving order', 'Remove k digits to maximize/minimize number', 'Next greater/smaller element in sequence'.", {}),
    ])),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("drop = len(nums) - p", {"code": True}), (" — discard budget: we can delete at most this many digits to get from the full array down to our target length p.", {})])),
    N.para(N.rich([("while drop and stack and stack[-1] < d", {"code": True}), (" — three-part pop condition: (1) have discards left, (2) stack is non-empty, (3) current digit strictly beats the stack top. All three must hold.", {})])),
    N.para(N.rich([("stack.pop(); drop -= 1", {"code": True}), (" — remove the smaller earlier digit (improving our subsequence) and spend one discard unit.", {})])),
    N.para(N.rich([("stack.append(d)", {"code": True}), (" — always push the current digit. It may get popped later by an even larger one.", {})])),
    N.para(N.rich([("return stack[:p]", {"code": True}), (" — slice to p because if we never exhausted drop (all digits were non-increasing), the stack has len(nums) elements, not p.", {})])),
    N.para(N.rich([("if A[i:] >= B[j:]", {"code": True}), (" — compare full remaining suffixes (list slices). In Python, this is O(k) lexicographic comparison. Handles ties: when first elements are equal, we look deeper into both sequences.", {})])),
    N.para(N.rich([("for i in range(max(0, k-n), min(k, m)+1)", {"code": True}), (" — valid split range: i must be ≤ m (nums1 length) and k-i must be ≤ n (nums2 length), and both must be non-negative.", {})])),
    N.para(N.rich([("if candidate > best", {"code": True}), (" — Python list comparison is naturally lexicographic, exactly what we want for comparing digit sequences.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force (educational) ─────────────────────────────────
SOL2_CODE = """\
from itertools import combinations

def maxNumber_brute(nums1, nums2, k):
    \"\"\"
    Brute force: try all subsets of size i from nums1 and k-i from nums2.
    For each pair, generate the lexicographically largest merge via recursion.
    O(C(m,i) * C(n,k-i) * ...) — completely impractical for large inputs.
    Shown for intuition only.
    \"\"\"
    def subseqs(nums, length):
        # All increasing-index subsequences of 'nums' of given 'length'
        return [list(c) for c in combinations(range(len(nums)), length)
                if True]  # placeholder — yields O(C(n,length)) candidates

    # In practice: exponential candidates * exponential interleavings
    # This is why the monotonic stack + greedy merge is necessary.
    pass  # not implemented — see Solution 1 instead
"""

blocks += [
    N.h2("Solution 2 — Brute Force (Educational Reference Only)"),
    N.toggle_h3("💡 Intuition: Why This Doesn't Work", [
        N.h4("Reframe the Problem"),
        N.para("Enumerate every way to choose i elements from nums1 (preserving order) and k-i from nums2, then try all valid interleavings and return the largest."),
        N.h4("What Doesn't Work"),
        N.para("There are C(m, i) ways to choose from nums1 and C(n, k-i) from nums2. For each pair, the number of interleavings is C(k, i). Even for m=n=20, k=10 this is astronomically large. Completely impractical."),
        N.h4("The Key Observation"),
        N.para("The structure of the problem — 'preserve relative order, pick best' — is exactly what the monotonic stack solves in O(n), making the brute force unnecessary."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.para("This approach is shown only to motivate why the O(k*(m+n+k)) solution is necessary. Do not implement this in an interview."),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "Exponential", "Exponential"],
        ["Monotonic Stack + Greedy Merge (optimal)", "O(k*(m+n+k))", "O(k)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stack / Queue (Monotonic Stack sub-family)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Monotonic Stack + Merge — compound pattern combining monotonic decreasing stack (for optimal subsequence extraction) with greedy suffix-comparison merge (for optimal interleaving).", {})])),
    N.callout(
        "When to recognize this pattern: 'Build the largest number from k digits across two arrays' / 'Remove K digits to maximize' / 'Merge two ordered sequences into lexicographically largest result'. Key signals: preserve relative order + maximize lexicographic value + two sources.",
        "🔎", "green_background"
    ),
    N.para("Note: This sub-pattern classification is based on analysis — 'Monotonic Stack + Merge' as a compound is not listed as a single sub-pattern in the guide, but combines the 'Monotonic Stack: Next Greater' technique with a greedy merge."),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique:"),
    N.bullet(N.rich([("Remove K Digits", {"bold": True}), (" (Medium) — Monotonic stack with discard budget; single array version of max_subseq (#402)", {})])),
    N.bullet(N.rich([("Largest Number", {"bold": True}), (" (Medium) — Arrange numbers to form largest integer; same lexicographic comparison principle (#179)", {})])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), (" (Easy) — Core monotonic stack pattern: 'wait for a larger digit' (#496)", {})])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), (" (Medium) — Monotonic stack for next warmer day; same 'hold smaller values' invariant (#739)", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Monotonic stack tracking 'previous smaller'; area maximization (#84)", {})])),
    N.bullet(N.rich([("Merge k Sorted Lists", {"bold": True}), (" (Hard) — Greedy merge generalized to k sequences; same 'always pick best head' principle (#23)", {})])),
    N.para("These problems share the core technique: use a monotonic stack to maintain an extremal invariant while scanning a sequence, possibly combined with greedy multi-sequence merging."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue section, Monotonic Stack sub-patterns. Compound pattern (Stack + Merge) classified from analysis.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("create_maximum_number")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
