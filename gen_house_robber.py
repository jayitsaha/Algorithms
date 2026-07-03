"""
gen_house_robber.py — Notion page builder for House Robber (LeetCode #198)
notion_page_id = None → CREATE a new page
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Step 0: Create page (notion_page_id is null) ──
PAGE_ID = N.create_page("House Robber", 198, "Medium", "🟡")
print("Created page:", PAGE_ID)

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=198,
    pattern="Dynamic Programming",
    subpatterns=["Max Skip or Take"],
    tc="O(n)",
    sc="O(1)",
    key_insight="dp[i] = max(dp[i-1], nums[i] + dp[i-2]): at each house, rob it or skip it, take the max.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Build page body ──
PROBLEM_STATEMENT = (
    "You are a professional robber planning to rob houses along a street. "
    "Adjacent houses have security systems connected, and it will automatically "
    "contact the police if two adjacent houses are broken into on the same night. "
    "Given an integer array nums representing the amount of money in each house, "
    "return the maximum amount of money you can rob tonight without alerting the police.\n\n"
    "Example 1: nums = [1,2,3,1] → Output: 4 (Rob house 0 and house 2: 1 + 3 = 4)\n"
    "Example 2: nums = [2,7,9,3,1] → Output: 12 (Rob houses 0, 2, 4: 2 + 9 + 1 = 12)\n\n"
    "Constraints: 1 ≤ nums.length ≤ 100, 0 ≤ nums[i] ≤ 400"
)

SOL1_CODE = """\
def rob(nums: list[int]) -> int:
    prev2, prev1 = 0, 0       # dp[i-2] and dp[i-1], initialized to 0
    for num in nums:           # process each house left to right
        curr = max(prev1,      # SKIP: best loot up to previous house
                   num + prev2) # ROB: this house + best from 2 steps back
        prev2 = prev1          # slide window: old prev1 becomes new prev2
        prev1 = curr           # curr becomes new prev1
    return prev1               # dp[n-1]: max loot over all n houses
"""

SOL2_CODE = """\
def rob(nums: list[int]) -> int:
    n = len(nums)
    if n == 1:
        return nums[0]          # edge: single house
    dp = [0] * n
    dp[0] = nums[0]             # base case: only first house
    dp[1] = max(nums[0], nums[1]) # base case: better of first two
    for i in range(2, n):
        dp[i] = max(dp[i-1],    # skip house i
                    nums[i] + dp[i-2])  # rob house i
    return dp[n - 1]
"""

SOL3_CODE = """\
from functools import lru_cache

def rob(nums: list[int]) -> int:
    @lru_cache(maxsize=None)
    def dp(i):
        if i < 0:   return 0         # base: no houses
        if i == 0:  return nums[0]   # base: one house
        return max(dp(i - 1),        # skip house i
                   nums[i] + dp(i - 2)) # rob house i
    return dp(len(nums) - 1)
"""

WHY_DP_CODE = """\
# Recurrence Relations (1D Max Skip or Take DP):
#
#   dp[0] = nums[0]
#   dp[1] = max(nums[0], nums[1])
#   dp[i] = max(dp[i-1], nums[i] + dp[i-2])   for i >= 2
#
# SKIP house i  → dp[i-1]         (best up to previous house)
# ROB  house i  → nums[i]+dp[i-2] (this house + best 2 back)
#
# Space Optimization: dp[i] depends only on dp[i-1] and dp[i-2]
# → Replace full array with two rolling variables prev2, prev1
# → O(n) time, O(1) space
"""

# Full block list
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider()
]

# ── Solution 1: Space-Optimized DP ──
blocks += [
    N.h2("Solution 1 — Space-Optimized DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "At each house, you have exactly two choices: rob it or skip it. "
            "Robbing house i prevents you from robbing house i-1, and adds nums[i] to whatever you had through house i-2. "
            "Skipping house i leaves you with the best you had through house i-1. "
            "You want the maximum loot from the entire row."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy (always pick the largest available house) fails. "
            "Consider [2, 7, 9, 3, 1]: greedy picks 9 (index 2), then must skip 7 and 3, leaving only 2+1=3 from adjacent houses. "
            "But rob 7 → skip 9 → rob 3 → only 10. Rob 2+9+1=12 is the actual optimum. "
            "Greedy can't look ahead to see that skipping a large value now enables a better combination later."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The optimal answer for houses 0..i depends only on two things: "
            "the optimal answer for 0..i-1 (skip case) and 0..i-2 (rob case). "
            "No other history matters. This 'one decision, two lookbacks' structure is the hallmark of 1D 'max skip or take' DP."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Define dp[i] = max loot from houses 0 through i.\n"
            "2. Recurrence: dp[i] = max(dp[i-1], nums[i] + dp[i-2]).\n"
            "3. Base cases: dp[0] = nums[0]; dp[1] = max(nums[0], nums[1]).\n"
            "4. Since dp[i] only needs dp[i-1] and dp[i-2], replace the array with two rolling variables (prev2, prev1) for O(1) space."
        ),
        N.callout(
            "Analogy: Imagine you're at a buffet where every other dish is poisoned. "
            "You can skip any dish freely, but eating one means you must skip the one right next to it. "
            "You want the maximum total calories. At each dish: skip (keep your current max) or eat (add its calories to the max 2 dishes back).",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("prev2, prev1 = 0, 0", {"code": True}), " — Initialize both rolling variables to 0. prev2 represents dp[i-2] and prev1 represents dp[i-1]. Starting at 0 means 'no loot before any houses.'" ])),
    N.para(N.rich([("for num in nums:", {"code": True}), " — Iterate through each house value. We process every house exactly once, left to right." ])),
    N.para(N.rich([("curr = max(prev1, num + prev2)", {"code": True}), " — Core decision: skip this house (prev1) vs rob it (num + prev2). We record the better option as curr = dp[i]." ])),
    N.para(N.rich([("prev2 = prev1", {"code": True}), " — Slide the window: old prev1 becomes the new prev2. Critical: do this BEFORE updating prev1." ])),
    N.para(N.rich([("prev1 = curr", {"code": True}), " — curr becomes the new prev1 for the next iteration. The window is now fully advanced." ])),
    N.para(N.rich([("return prev1", {"code": True}), " — After the loop, prev1 holds dp[n-1], the maximum loot considering all n houses." ])),
    N.divider()
]

# ── Why is This DP? ──
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(
        "This problem has both pillars of dynamic programming:\n\n"
        "1. OPTIMAL SUBSTRUCTURE: The best answer for houses 0..i is fully determined by the best answers for 0..i-1 and 0..i-2. "
        "Knowing only the maximum dollar amounts (not which exact houses were robbed) is sufficient to compute the next step correctly.\n\n"
        "2. OVERLAPPING SUBPROBLEMS: A naive recursion computing dp(4) would call dp(3) and dp(2). dp(3) calls dp(2) again. "
        "dp(2) is computed multiple times — exponential redundancy that memoization/tabulation eliminates.\n\n"
        "This is why the naive O(2^n) recursion without memoization times out, while DP gives O(n)."
    ),
    N.code(WHY_DP_CODE, "python"),
    N.divider()
]

# ── Solution 2: Tabulation ──
blocks += [
    N.h2("Solution 2 — Tabulation with Full DP Array"),
    N.toggle_h3("💡 Intuition: Explicit DP Table", [
        N.h4("What Doesn't Work"),
        N.para(
            "The full array approach uses O(n) space, which is avoidable (as Solution 1 shows). "
            "However, it has a key advantage: the dp table makes each subproblem's result explicit and inspectable, "
            "which is valuable for debugging, teaching, and understanding the recurrence visually."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Allocating dp[0..n-1] and filling it left-to-right is conceptually cleaner: "
            "dp[i] = max(dp[i-1], nums[i] + dp[i-2]). "
            "For whiteboard interviews or when explaining your thought process, writing out the table row makes the logic immediately verifiable."
        ),
        N.callout(
            "Trace: nums=[2,7,9,3,1] → dp=[2,7,11,11,12]\n"
            "dp[0]=2, dp[1]=max(2,7)=7, dp[2]=max(7,9+2)=11, dp[3]=max(11,3+7)=11, dp[4]=max(11,1+11)=12",
            "📊", "gray_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.callout(
        "⚠️ Edge case trap: when n == 1, accessing nums[1] would raise IndexError. "
        "Always guard single-element inputs before setting dp[1].",
        "⚠️", "yellow_background"
    ),
    N.divider()
]

# ── Solution 3: Memoization ──
blocks += [
    N.h2("Solution 3 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: Recursive with Cache", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of building up from the base case, ask: 'What is the max loot from house i downward?' "
            "dp(i) = max(dp(i-1), nums[i] + dp(i-2)). This recursion naturally expresses the 'skip or rob' choice and is easy to write directly from the recurrence."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Without caching, this recursion recomputes dp(i-2) many times. "
            "@lru_cache ensures each dp(i) is computed exactly once, giving O(n) time. "
            "Top-down memoization is the most natural way to arrive at a DP solution in an interview: "
            "write the recursion first, add @lru_cache, then (optionally) convert to iterative."
        )
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE, "python"),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Naive Recursion (no memo)", "O(2ⁿ)", "O(n) stack", "TLE on large inputs"],
        ["Memoization (top-down)", "O(n)", "O(n)", "Cache + call stack"],
        ["Tabulation (bottom-up)", "O(n)", "O(n)", "Full dp array"],
        ["Space-Optimized (Interview Pick)", "O(n)", "O(1)", "Two rolling variables"],
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming (Section 18 of DSA Guide)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Max Skip or Take (1-D DP) · Guide Section 18.1"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Cannot pick adjacent / neighboring elements'\n"
        "• Maximizing or minimizing a sum with a local exclusion constraint\n"
        "• Greedy (always pick largest) produces the wrong answer\n"
        "• Only two previous states needed → O(1) space optimization possible\n"
        "• Recurrence of the form: dp[i] = max/min(dp[i-1], f(nums[i]) + dp[i-2])",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (1D Max Skip or Take DP):"),
    N.bullet(N.rich([("House Robber II", {"bold": True}), " (Medium) — Circular street: run House Robber twice excluding first or last house; take the max. (#213)"])),
    N.bullet(N.rich([("House Robber III", {"bold": True}), " (Medium) — Tree structure: DFS returning (rob_root, skip_root) pair from leaves up. (#337)"])),
    N.bullet(N.rich([("Delete and Earn", {"bold": True}), " (Medium) — Choosing value v removes v±1 neighbors. Transform to House Robber on value array. (#740)"])),
    N.bullet(N.rich([("Climbing Stairs", {"bold": True}), " (Easy) — Same Fibonacci-style recurrence dp[i]=dp[i-1]+dp[i-2]. (#70)"])),
    N.bullet(N.rich([("Min Cost Climbing Stairs", {"bold": True}), " (Easy) — Inverse objective: dp[i]=cost[i]+min(dp[i-1],dp[i-2]). (#746)"])),
    N.bullet(N.rich([("Paint House", {"bold": True}), " (Medium) — Adjacent houses must differ in color; extends state to (house, last_color). (#256)"])),
    N.bullet(N.rich([("Maximum Alternating Subsequence Sum", {"bold": True}), " (Medium) — State machine DP with two alternating states. (#1911)"])),
    N.para("These problems all share the core technique: at each position, make a binary choice with a local exclusion constraint, and use two lookback values to resolve it optimally."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18.1 (1-D Dynamic Programming)\nSub-Pattern verified in Guide table: House Robber → dp[i] = max(dp[i-1], dp[i-2] + nums[i])", "📚", "gray_background")
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("house_robber")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("Blocks appended.")
print("NOTION OK", PAGE_ID)

# ── Write status file ──
import json, pathlib
status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)

html_path = pathlib.Path(__file__).parent / "house_robber_explainer.html"
html_lines = len(html_path.read_text().splitlines())

status = {
    "slug": "house_robber",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Fresh page created. 3 solutions (space-opt DP, tabulation, memoization). 17-step walkthrough. 1019 HTML lines."
}
(status_dir / "house_robber.json").write_text(json.dumps(status, indent=2))
print(f"RESULT house_robber | html=OK | notion=OK | lines={html_lines}")
