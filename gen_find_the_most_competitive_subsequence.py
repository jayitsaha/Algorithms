"""
Notion update for Find the Most Competitive Subsequence (LC 1673).
Updates the existing page in-place using notion_lib.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8194-962c-c17bb660b762"
SLUG = "find_the_most_competitive_subsequence"

print(f"Updating properties for page {PAGE_ID}...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1673,
    pattern="Stack & Queue",
    subpatterns=["Monotonic Stack with Size"],
    tc="O(n)",
    sc="O(k)",
    key_insight="Greedily maintain a monotonic increasing stack of size k; pop larger tops when a smaller element arrives and enough elements remain to still reach k.",
    icon="🟡",
    status="Solved",
    source="LeetCode"
)
print("Properties set.")

print("Wiping existing page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

print("Building new page body...")
blocks = []

# ─── Problem ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and a positive integer ", {}),
        ("k", {"code": True}),
        (", return the most competitive subsequence of ", {}),
        ("nums", {"code": True}),
        (" of size ", {}),
        ("k", {"code": True}),
        (". A subsequence is more competitive than another if at the first position where they differ, it has a smaller element. The subsequence must preserve the original relative order of elements.", {})
    ])),
    N.para("Example 1: nums=[3,5,2,6], k=2 → [2,6]. Example 2: nums=[2,4,3,3,5,4,9,6], k=4 → [2,3,3,4]."),
    N.divider(),
]

# ─── Solution 1 — Monotonic Stack (Optimal, Interview Pick) ───
blocks += [
    N.h2("Solution 1 — Monotonic Stack with Size Constraint (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the lexicographically smallest subsequence of size exactly k. 'Lexicographically smallest' means: at each position from left to right, minimize the value. This is a greedy problem — locally optimal choices lead to a globally optimal result."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: enumerate all C(n,k) subsequences and compare them. Time O(C(n,k)·k) — exponential for large n. For n=10000, k=5000, this is astronomically slow. We need an O(n) approach."),
        N.h4("The Key Observation"),
        N.para("If the current element is smaller than the top of our result-so-far AND we still have enough elements remaining to reach k total after popping, we should replace the top with the current element. It's strictly better at that position without breaking any earlier positions."),
        N.h4("Building the Solution"),
        N.para("Use a monotonic stack of max size k. For each element: (1) While stack[-1] > current AND n - i > k - len(stack): pop. The formula n - i > k - len(stack) checks 'room to pop' — remaining elements (including current) exceed slots still needed. (2) If len(stack) < k, push. At the end, the stack holds exactly k elements in the most competitive order."),
        N.callout(
            "Analogy: You're curating a team of k contestants for a quiz. If a newcomer scores lower than your last pick AND you'd still be able to fill the team after swapping — make the swap. Never trade when you'd be left short-handed.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def mostCompetitive(nums: list[int], k: int) -> list[int]:\n"
        "    stack = []\n"
        "    n = len(nums)\n"
        "    for i, num in enumerate(nums):\n"
        "        while (stack\n"
        "               and stack[-1] > num\n"
        "               and n - i > k - len(stack)):\n"
        "            stack.pop()\n"
        "        if len(stack) < k:\n"
        "            stack.append(num)\n"
        "    return stack",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), (" — Initialize the monotonic increasing stack. This will become our answer.", {})])),
    N.para(N.rich([("n = len(nums)", {"code": True}), (" — Cache array length; used in the pop-guard formula on every iteration.", {})])),
    N.para(N.rich([("for i, num in enumerate(nums):", {"code": True}), (" — Scan every element with its index. We need i for the size-guard formula.", {})])),
    N.para(N.rich([("while (stack and stack[-1] > num and n - i > k - len(stack)):", {"code": True}), (" — Three guards: non-empty stack, current is strictly smaller than top, and room to pop (remaining elements exceed remaining slots needed).", {})])),
    N.para(N.rich([("stack.pop()", {"code": True}), (" — Discard suboptimal top element. It's larger than current and we can afford to remove it.", {})])),
    N.para(N.rich([("if len(stack) < k: stack.append(num)", {"code": True}), (" — Only push if we still need more elements. Once stack reaches size k, new (larger) elements are simply skipped.", {})])),
    N.para(N.rich([("return stack", {"code": True}), (" — The stack holds exactly k elements forming the most competitive subsequence.", {})])),
    N.divider(),
]

# ─── Solution 2 — Brute Force ───
blocks += [
    N.h2("Solution 2 — Brute Force (Exponential, for understanding only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The naive approach: enumerate every possible size-k subsequence and pick the lexicographically smallest one."),
        N.h4("What Doesn't Work"),
        N.para("There are C(n,k) subsequences, each of length k to compare. Total time O(C(n,k)·k) — exponential for large n and mid-range k. Completely impractical for the given constraints (n up to 10^5)."),
        N.h4("The Key Observation"),
        N.para("Python's list comparison is already lexicographic, so the code is simple. This is useful for verifying correctness on small inputs before coding the optimal solution."),
        N.h4("Building the Solution"),
        N.para("Use itertools.combinations to generate all index combinations of size k, build each subsequence, and track the lexicographic minimum."),
    ]),
    N.h3("Code"),
    N.code(
        "from itertools import combinations\n\n"
        "def mostCompetitive_brute(nums: list[int], k: int) -> list[int]:\n"
        "    best = None\n"
        "    for indices in combinations(range(len(nums)), k):\n"
        "        subseq = [nums[i] for i in indices]\n"
        "        if best is None or subseq < best:  # Python list comparison is lexicographic\n"
        "            best = subseq\n"
        "    return best",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("combinations(range(len(nums)), k)", {"code": True}), (" — Generates all C(n,k) index tuples in sorted order. Each tuple represents a valid subsequence selection.", {})])),
    N.para(N.rich([("subseq < best", {"code": True}), (" — Python compares lists lexicographically: element by element until a difference is found. This is exactly 'more competitive' as defined in the problem.", {})])),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Monotonic Stack (Optimal)", "O(n)", "O(k)"],
        ["Brute Force", "O(C(n,k)·k)", "O(k)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stack & Queue (Section 6 of DSA Guide)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Monotonic Stack with Size", {})])),
    N.callout(
        "When to recognize this pattern: 'lexicographically smallest subsequence of size k', 'most competitive', 'remove elements to minimize sequence', combined with an exact output size constraint. The pop guard formula n - i > k - len(stack) is the hallmark of this sub-pattern.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Monotonic Stack with Size / lexicographic minimization):"),
    N.bullet(N.rich([("Remove K Digits", {"bold": True}), (" (Medium) — Same pop logic; removes at-most k digits to minimize a number. No exact-size constraint, so use a 'remaining = n - k' budget instead.", {})])),
    N.bullet(N.rich([("Remove Duplicate Letters", {"bold": True}), (" (Medium) — Lex-smallest subsequence with unique characters; same monotonic pop + 'seen' set to avoid re-adding removed chars.", {})])),
    N.bullet(N.rich([("Create Maximum Number", {"bold": True}), (" (Hard) — Select k elements from two arrays to form the largest number; applies this stack technique to both arrays then merges results.", {})])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), (" (Medium) — DP + monotonic deque for window-range max; same Section 6.4 of the guide.", {})])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard) — Monotonic decreasing deque to track window max; the dual data structure to this problem's increasing stack.", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Monotonic increasing stack to find left/right boundary extents; core stack concept behind many problems.", {})])),
    N.para("These problems all share the core insight: a monotonic stack greedily maintains the optimal 'frontier' of values, popping suboptimal elements when a better candidate arrives."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 6.4 (Monotonic Queue/Deque). Sub-Pattern: Monotonic Stack with Size. Verified from Guide table.", "📚", "gray_background"),
]

# ─── Embed ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
