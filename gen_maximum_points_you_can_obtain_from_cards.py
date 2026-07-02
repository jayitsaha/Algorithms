"""
gen_maximum_points_you_can_obtain_from_cards.py
Notion IN-PLACE update for LeetCode #1423.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81d8-a83d-ea15c952d62e"
SLUG = "maximum_points_you_can_obtain_from_cards"

# ── Step 1: Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1423,
    pattern="Sliding Window",
    subpatterns=["Minimum Middle Window"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Taking k cards from both ends leaves n-k contiguous cards in the middle; minimize that middle window to maximize the take.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe old body ────────────────────────────────────────────────────
print("Wiping old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── Step 3: Build new body blocks ────────────────────────────────────────────
blocks = []

# ─── Problem ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There is a row of ", {}),
        ("cardPoints", {"code": True}),
        (" cards, each with a point value. In one step you may take one card from the left end or the right end. You must take exactly ", {}),
        ("k", {"code": True}),
        (" cards. Return the maximum score you can obtain.", {})
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ cardPoints.length ≤ 10⁵, 1 ≤ cardPoints[i] ≤ 10⁴, 1 ≤ k ≤ cardPoints.length", {})
    ])),
    N.divider(),
]

# ─── Solution 1: Complement Sliding Window ───
SOLUTION_1_CODE = """\
def maxScore(cardPoints: list[int], k: int) -> int:
    n = len(cardPoints)
    total = sum(cardPoints)       # baseline: take every card
    w = n - k                     # size of the middle "skip" window
    if w == 0:
        return total              # k == n: take all cards
    win_sum = sum(cardPoints[:w]) # initial window at leftmost position
    min_win = win_sum
    for i in range(1, k + 1):    # slide k more positions
        win_sum += cardPoints[i + w - 1]  # new right element enters
        win_sum -= cardPoints[i - 1]      # old left element exits
        min_win = min(min_win, win_sum)
    return total - min_win        # maximize taken = minimize skipped\
"""

blocks += [
    N.h2("Solution 1 — Complement Sliding Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Taking k cards from both ends always leaves exactly n−k consecutive cards untouched in the middle. So instead of asking 'which k cards to take?', we ask 'which n−k contiguous cards to skip?' To maximize the taken sum, we minimize the skipped sum."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (always take the larger end) fails because a locally smaller card at one end might block a much larger card just behind it. For example, [1,100,100,100,2], k=4: greedy takes 1+2+100+100=203, but taking all 4 from the right gives 100+100+100+2=302."),
        N.h4("The Key Observation"),
        N.para("Every valid k-card selection from both ends corresponds to exactly one window of size n−k in the middle. Sliding that window through all k+1 positions enumerates every possible selection in O(n) time."),
        N.h4("Building the Solution"),
        N.para("1. Compute total = sum of all cards. 2. Compute window size w = n−k. 3. Initialize win_sum = sum(cardPoints[:w]). 4. Slide the window right k times, each time: add cardPoints[i+w−1], subtract cardPoints[i−1], track min_win. 5. Return total − min_win."),
        N.callout("Analogy: Imagine flipping the problem upside down. Instead of filling a bag from the ends, you're choosing a hole in the middle to drain through — pick the smallest hole.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(cardPoints)", {"code": True}), (" — total number of cards.", {})])),
    N.para(N.rich([("total = sum(cardPoints)", {"code": True}), (" — the sum of all cards. This is the maximum possible score. We will subtract the minimum-sum skip window from it.", {})])),
    N.para(N.rich([("w = n - k", {"code": True}), (" — the size of the window we must skip. Every valid selection leaves exactly w consecutive cards unselected.", {})])),
    N.para(N.rich([("if w == 0: return total", {"code": True}), (" — edge case: k equals n, we take every card, no skip window exists.", {})])),
    N.para(N.rich([("win_sum = sum(cardPoints[:w])", {"code": True}), (" — initial window sum: the leftmost w cards (skip all w from the left side, take k from the right). This is window position i=0.", {})])),
    N.para(N.rich([("min_win = win_sum", {"code": True}), (" — initialize the minimum tracker with the first window.", {})])),
    N.para(N.rich([("for i in range(1, k + 1)", {"code": True}), (" — slide the window k more times. Loop index i = number of cards taken from the left end.", {})])),
    N.para(N.rich([("win_sum += cardPoints[i + w - 1]", {"code": True}), (" — the element entering the window from the right side. When we take i cards from the left, the window's right boundary is at index i+w−1.", {})])),
    N.para(N.rich([("win_sum -= cardPoints[i - 1]", {"code": True}), (" — the element exiting the window from the left side. It was index i−1 (0-based), the rightmost of the left-taken cards.", {})])),
    N.para(N.rich([("min_win = min(min_win, win_sum)", {"code": True}), (" — update the minimum skip sum. After all slides, this holds the smallest middle chunk sum across all k+1 configurations.", {})])),
    N.para(N.rich([("return total - min_win", {"code": True}), (" — the answer: take the total sum and subtract the minimum waste.", {})])),
    N.divider(),
]

# ─── Solution 2: Direct Two-Pointer ───
SOLUTION_2_CODE = """\
def maxScore(cardPoints: list[int], k: int) -> int:
    # Start by taking all k cards from the left
    left_sum = sum(cardPoints[:k])
    best = left_sum
    right_sum = 0
    # Trade one left card for one right card, k times
    for i in range(1, k + 1):
        left_sum -= cardPoints[k - i]   # return the rightmost left card
        right_sum += cardPoints[-i]     # pick up the i-th card from the right
        best = max(best, left_sum + right_sum)
    return best\
"""

blocks += [
    N.h2("Solution 2 — Direct Two-Pointer"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start with the most extreme valid configuration: take all k cards from the left. Then iteratively trade one left card for one right card, checking each resulting score. This directly models all k+1 valid left+right splits."),
        N.h4("What Doesn't Work"),
        N.para("This approach still enumerates all configurations but without the complement inversion. It's slightly harder to derive from scratch but simpler to verify mentally."),
        N.h4("The Key Observation"),
        N.para("Taking i cards from the left and k−i from the right: left_sum = prefix sum of length i, right_sum = suffix sum of length k−i. We iteratively transfer one card from the left pile to the right pile."),
        N.h4("Building the Solution"),
        N.para("Initialize left_sum = sum of first k cards. For i from 1 to k: drop the rightmost left card, pick up the i-th right card, check if left_sum + right_sum beats the best."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("left_sum = sum(cardPoints[:k])", {"code": True}), (" — take all k cards from the left as the starting point.", {})])),
    N.para(N.rich([("best = left_sum", {"code": True}), (" — first candidate: take k from left, 0 from right.", {})])),
    N.para(N.rich([("right_sum = 0", {"code": True}), (" — no right cards picked yet.", {})])),
    N.para(N.rich([("left_sum -= cardPoints[k - i]", {"code": True}), (" — return the rightmost of the current left-side picks. On first iteration (i=1), this is cardPoints[k−1].", {})])),
    N.para(N.rich([("right_sum += cardPoints[-i]", {"code": True}), (" — pick up the i-th card from the right end. Negative indexing: cardPoints[−1] is the last card.", {})])),
    N.para(N.rich([("best = max(best, left_sum + right_sum)", {"code": True}), (" — is this split better than our current best?", {})])),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (enumerate splits)", "O(k²)", "O(1)", "Recompute prefix/suffix each time"],
        ["Prefix + Suffix arrays", "O(n)", "O(n)", "Build full arrays, then scan splits"],
        ["Complement Window (Sol 1) ✓", "O(n)", "O(1)", "Optimal — canonical interview pick"],
        ["Direct Two-Pointer (Sol 2)", "O(k)", "O(1)", "O(n) worst case; simpler mental model"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sliding Window (Array Manipulation)", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Minimum Middle Window", {})])),
    N.para(N.rich([("Section: ", {"bold": True}), ("Guide Section 1.5 — Sliding Window - Dynamic Size", {})])),
    N.callout(
        "When to recognize: 'Take exactly k elements from either end' → the untouched elements are always contiguous → reframe as minimize(middle window of size n−k). Also: whenever 'what you DON'T pick is always contiguous' and you want to optimize the complement.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sliding window technique:"),
    N.bullet(N.rich([("Maximum Average Subarray I", {"bold": True}), (" (Easy) — Classic fixed-size window; find max average over k-length window (#643)", {})])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), (" (Medium) — Fixed-size window with frequency count constraint (#438)", {})])),
    N.bullet(N.rich([("Permutation in String", {"bold": True}), (" (Medium) — Fixed-size frequency count window; find if s1's permutation is in s2 (#567)", {})])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), (" (Medium) — Dynamic window; at most 2 distinct types (#904)", {})])),
    N.bullet(N.rich([("Max Consecutive Ones III", {"bold": True}), (" (Medium) — Dynamic window; count zeros allowed up to k (#1004)", {})])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), (" (Hard) — Dynamic window; expand until valid, shrink to optimize (#76)", {})])),
    N.bullet(N.rich([("Subarray Product Less Than K", {"bold": True}), (" (Medium) — Dynamic window; track running product, count valid subarrays (#713)", {})])),
    N.para("These problems share the fixed-size or dynamic window template: maintain a running aggregate and slide efficiently in O(n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.5 — Sliding Window Dynamic Size", "📚", "gray_background"),
]

# ─── Interactive Explainer Embed ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. ",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
