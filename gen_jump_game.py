"""gen_jump_game.py — Notion update for Jump Game (LeetCode #55)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ab-9b14-ff60c8012ffd"

# ── 1) Set properties ─────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=55,
    pattern="Greedy",
    subpatterns=["Track Max Reachable"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Track max_reach = max(max_reach, i+nums[i]); if i > max_reach, stranded — return False.",
    icon="🟡"
)
print("Properties set OK")

# ── 2) Wipe old body ──────────────────────────────────────────────────
print("Wiping old blocks...")
n_wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {n_wiped} blocks")

# ── 3) Build new body ─────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer array ", {}),
        ("nums", {"code": True}),
        (". You are initially positioned at the first index of the array. Each element in the array represents your maximum jump length at that position. Return ", {}),
        ("True", {"code": True}),
        (" if you can reach the last index, or ", {}),
        ("False", {"code": True}),
        (" otherwise.", {}),
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ("nums = [2,3,1,1,4]", {"code": True}),
        (" → True  (jump 1 to index 1, then 3 to reach index 4)", {}),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ("nums = [3,2,1,0,4]", {"code": True}),
        (" → False  (always stuck at index 3, where nums[3]=0)", {}),
    ])),
    N.callout(
        N.rich([
            ("Constraints: ", {"bold": True}),
            ("1 ≤ nums.length ≤ 10⁴, 0 ≤ nums[i] ≤ 10⁵", {}),
        ]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1 — Greedy (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Greedy: Track Max Reachable (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We don't need the specific jump path — we just need to know if ANY path exists. This is a reachability question, not a shortest-path question. That distinction is key for choosing the right algorithm."),
        N.h4("What Doesn't Work"),
        N.para("Trying all jump sequences (DFS) is O(2^n) — exponential. Adding memoization (DP) brings it to O(n²). Both are correct but inefficient. We need to eliminate redundant exploration."),
        N.h4("The Key Observation"),
        N.para("At any reachable position i, the farthest we can extend our reach is i + nums[i]. We don't need to track individual paths — just the running maximum of this value. If we can reach up to index k, we have implicitly checked every position from 0 to k via the max."),
        N.h4("Building the Solution"),
        N.para("Initialize max_reach = 0. At each index i: (1) if i > max_reach, we're stranded — return False. (2) Update max_reach = max(max_reach, i + nums[i]). (3) If max_reach >= n-1, return True. This greedy works because a larger reach from any reachable position dominates all smaller options — no backtracking possible or needed."),
        N.callout("Analogy: Imagine a hose that extends from index 0. Each tap you can reach gives the hose more length. You want to know if the hose can reach the far end. You don't simulate walking to the end — you just track the maximum hose length achievable from any connected tap.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def canJump(nums: list[int]) -> bool:
    max_reach = 0              # Farthest index reachable from any visited position
    n = len(nums)              # Cache length; used in loop and exit check
    for i in range(n):         # Visit every index left to right
        if i > max_reach:      # Are we beyond what's reachable? Stranded!
            return False
        max_reach = max(max_reach, i + nums[i])  # Extend reach by jumping nums[i] from here
        if max_reach >= n - 1: # Already proven last index is reachable
            return True        # Early exit — no need to continue
    return True                # Loop completed without getting stranded → reachable"""),
    N.h3("Line by Line"),
    N.para(N.rich([("max_reach = 0", {"code": True}), (" — Initialize: the farthest index we can currently guarantee reaching. Starts at 0 because we're standing at index 0.", {})])),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — Iterate left to right. We visit every index to check if it's reachable and to update our reach frontier.", {})])),
    N.para(N.rich([("if i > max_reach:", {"code": True}), (" — Critical check: if the current index is beyond our best reach, no prior jump could have gotten us here. We're stranded permanently — no choice of earlier jumps changes this since max_reach already captured the best possible outcome.", {})])),
    N.para(N.rich([("max_reach = max(max_reach, i + nums[i])", {"code": True}), (" — From index i, jumping nums[i] steps reaches i + nums[i]. Take the max to maintain the global best reach across all reachable positions.", {})])),
    N.para(N.rich([("if max_reach >= n - 1:", {"code": True}), (" — Early exit: if we already know the last index is reachable, stop. No need to process the remaining indices.", {})])),
    N.para(N.rich([("return True", {"code": True}), (" (final) — If the loop completes without returning False, we never got stranded, so the last index was reachable.", {})])),
    N.callout("You can simplify by removing the early exit and just writing return max_reach >= n - 1 after the loop. Both are correct. The early exit is an optimization for cases where the answer is found quickly.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2 — DP ──
blocks += [
    N.h2("Solution 2 — Dynamic Programming: Tabulation (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define dp[i] = True if index i is reachable from index 0. We want dp[n-1]."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization visits the same subproblems exponentially. We need to compute each index's reachability exactly once."),
        N.h4("The Key Observation"),
        N.para("dp[i] = True if there exists any j < i such that dp[j] = True AND j + nums[j] >= i. In other words: can any reachable predecessor reach index i?"),
        N.h4("Building the Solution"),
        N.para("Initialize dp[0] = True (we start there). For each index i from 1 to n-1, scan all j < i: if dp[j] and j + nums[j] >= i, set dp[i] = True and break. Return dp[n-1]."),
    ]),
    N.h3("Code"),
    N.code("""def canJump(nums: list[int]) -> bool:
    n = len(nums)
    dp = [False] * n           # dp[i] = True if index i is reachable from 0
    dp[0] = True               # We start at index 0 by definition
    for i in range(1, n):      # For each index, check if any prior index can reach it
        for j in range(i):     # Check all indices before i
            if dp[j] and j + nums[j] >= i:  # j is reachable AND can jump far enough
                dp[i] = True
                break          # Found one valid predecessor — no need to check more
    return dp[n - 1]           # Is the last index reachable?"""),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [False] * n", {"code": True}), (" — Create a boolean array. dp[i] will be True once we verify index i is reachable.", {})])),
    N.para(N.rich([("dp[0] = True", {"code": True}), (" — Base case: index 0 is always reachable (we start there).", {})])),
    N.para(N.rich([("for j in range(i):", {"code": True}), (" — Inner loop: check every index j before i as a potential predecessor.", {})])),
    N.para(N.rich([("if dp[j] and j + nums[j] >= i:", {"code": True}), (" — j must itself be reachable (dp[j]=True) AND must be able to jump far enough to reach i.", {})])),
    N.para(N.rich([("return dp[n-1]", {"code": True}), (" — Answer: is the last index reachable?", {})])),
    N.divider(),
]

# ── Solution 3 — Brute Force ──
blocks += [
    N.h2("Solution 3 — Brute Force DFS (O(2^n)) — for completeness"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Recursively answer: starting at index i, can I reach the last index by trying every possible jump?"),
        N.h4("What Doesn't Work"),
        N.para("No pruning — each position branches into up to nums[i] subproblems. With large values, this is exponential."),
        N.h4("The Key Observation"),
        N.para("This is the foundation — it directly models the problem. Mention this first in interviews before optimizing."),
    ]),
    N.h3("Code"),
    N.code("""def canJump(nums: list[int]) -> bool:
    def dfs(i: int) -> bool:   # Can we reach the end starting from index i?
        if i >= len(nums) - 1: # Base: at or past last index
            return True
        for jump in range(1, nums[i] + 1):  # Try every possible jump length
            if dfs(i + jump):  # Recurse on the jump destination
                return True
        return False           # No jump from here leads to success
    return dfs(0)"""),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["DFS Brute Force", "O(2^n)", "O(n)", "Exponential — tries all jump sequences"],
        ["DP Tabulation", "O(n²)", "O(n)", "Quadratic — each index checked against all predecessors"],
        ["Greedy ✓", "O(n)", "O(1)", "Optimal — single variable, single pass"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Greedy", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Track Max Reachable", {})])),
    N.callout(
        "When to recognize this pattern: Problem asks 'can you reach X?' with variable-size forward moves. Each element defines a maximum range (not a fixed step). You need reachability, not shortest path. Zero values in the array may create blockades.",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Source: ", {"bold": True}), ("Guide Section 16 — Greedy → Track Max Reachable · Verified", {})])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same greedy/reachability technique:"),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), (" (Medium) — Minimum jumps; greedy with two boundary pointers (current reach, next reach) — #45", {})])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), (" (Medium) — Maximum score jumping; DP + Monotonic Deque for window max — #1696", {})])),
    N.bullet(N.rich([("Jump Game VII", {"bold": True}), (" (Medium) — String-based jumping with range restrictions; BFS approach — #1871", {})])),
    N.bullet(N.rich([("Gas Station", {"bold": True}), (" (Medium) — Greedy: start where cumulative deficit recovers; similar 'stranded' detection — #134", {})])),
    N.bullet(N.rich([("Max Chunks To Make Sorted", {"bold": True}), (" (Medium) — Track max-so-far; chunk boundary when max equals current index — #769", {})])),
    N.bullet(N.rich([("Video Stitching", {"bold": True}), (" (Medium) — Interval coverage: always pick clip extending reach farthest — #1024", {})])),
    N.bullet(N.rich([("Minimum Number of Taps to Open to Water a Garden", {"bold": True}), (" (Hard) — Same 'extend frontier' greedy with interval taps — #1326", {})])),
    N.para("These problems share the core technique: maintain a running maximum reach and extend it greedily from every reachable position."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 16 (Greedy) — Track Max Reachable", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("jump_game")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
