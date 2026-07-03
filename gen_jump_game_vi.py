"""gen_jump_game_vi.py — Notion update for Jump Game VI (LC #1696)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81cc-af44-dd94ca6aea99"

# ── 1) Set properties ────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1696,
    pattern="Stack / Queue",
    subpatterns=["Monotonic Queue", "DP + Monotonic Deque"],
    tc="O(n)",
    sc="O(n)",
    key_insight="DP recurrence dp[i]=nums[i]+max(dp[j]) for j in [i-k,i-1]; use a monotonic deque for O(1) sliding window max.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body ────────────────────────────────────────────────────
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a 0-indexed integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (". You are standing at index 0. In one move, you can jump at most ", {}),
        ("k", {"code": True}),
        (" steps forward — from index ", {}),
        ("i", {"code": True}),
        (" to any index ", {}),
        ("j", {"code": True}),
        (" where ", {}),
        ("i < j <= i + k", {"code": True}),
        (". You want to reach the last index of the array. Your score is the sum of all ", {}),
        ("nums[i]", {"code": True}),
        (" where ", {}),
        ("i", {"code": True}),
        (" is a visited index. Return the maximum score you can get.", {}),
    ])),
    N.divider(),
]

# Solution 1 — DP + Monotonic Deque
blocks += [
    N.h2("Solution 1 — DP + Monotonic Deque (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the maximum-score path from index 0 to index n−1 where each jump covers 1–k steps. This is an optimization over a DAG — a classic sign of DP. Define dp[i] as the maximum score to reach index i."),
        N.h4("What Doesn't Work"),
        N.para("The naïve recurrence dp[i] = nums[i] + max(dp[j]) for j in [i−k, i−1] is correct but costs O(k) per index → O(nk) total. With n and k up to 10^5, that is 10^10 operations — too slow."),
        N.h4("The Key Observation"),
        N.para("The inner max is always over the last k dp values as i advances — a sliding window maximum. The classic O(n) solution to sliding window maximum uses a monotonic decreasing deque: it stores indices with decreasing dp values, front holds the maximum, and stale (out-of-window) indices are evicted from the front."),
        N.h4("Building the Solution"),
        N.para("Combine DP with the deque. For each i: (1) evict from front while out of range, (2) compute dp[i] = nums[i] + dp[dq[0]], (3) evict from back any index dominated by i (dp ≤ dp[i]), (4) push i. Each index enters and exits the deque at most once → amortized O(1) per step → O(n) total."),
        N.callout("Analogy: Think of the deque as a 'hall of fame' leaderboard for dp values. When a new champion arrives (higher dp), all weaker previous entries are knocked out immediately — they can never beat the champion for any future position.", "🏆", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n\ndef maxResult(nums: list[int], k: int) -> int:\n    n = len(nums)\n    dp = [0] * n\n    dp[0] = nums[0]              # base case: always start here\n    dq = deque([0])              # deque of indices; front = best predecessor\n    \n    for i in range(1, n):\n        # Step 1: evict out-of-range front\n        while dq[0] < i - k:\n            dq.popleft()\n        # Step 2: compute dp[i] using best predecessor\n        dp[i] = nums[i] + dp[dq[0]]\n        # Step 3: evict dominated back entries\n        while dq and dp[dq[-1]] <= dp[i]:\n            dq.pop()\n        # Step 4: push current index\n        dq.append(i)\n    \n    return dp[-1]",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp[0] = nums[0]", {"code": True}), (" — Base case: we always land on index 0 and collect its value. No predecessor to consider.", {})])),
    N.para(N.rich([("dq = deque([0])", {"code": True}), (" — Seed the deque with index 0. It is the sole candidate predecessor for index 1.", {})])),
    N.para(N.rich([("while dq[0] < i - k: dq.popleft()", {"code": True}), (" — Front eviction: remove indices that are more than k steps behind i (cannot be jumped from). O(1) per removal; amortized O(n) total.", {})])),
    N.para(N.rich([("dp[i] = nums[i] + dp[dq[0]]", {"code": True}), (" — The deque front is now the highest-dp index in the valid window [i−k, i−1]. We add the current cell value to get dp[i].", {})])),
    N.para(N.rich([("while dq and dp[dq[-1]] <= dp[i]: dq.pop()", {"code": True}), (" — Back eviction: any back index with dp ≤ dp[i] is dominated by i (same or better dp, more recent index, larger future window). Discard immediately.", {})])),
    N.para(N.rich([("dq.append(i)", {"code": True}), (" — Push current index as a future predecessor candidate. Deque remains monotone decreasing by dp value.", {})])),
    N.para(N.rich([("return dp[-1]", {"code": True}), (" — The answer is the maximum score to reach the last index.", {})])),
    N.divider(),
]

# Solution 2 — Naïve DP
blocks += [
    N.h2("Solution 2 — Naïve DP, O(nk) (Brute Force, do NOT use in interviews for large n)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same DP definition: dp[i] = max score to reach index i."),
        N.h4("What Doesn't Work"),
        N.para("This IS the working solution — it is just slow. For n=k=10^5 it performs 10^10 operations and times out."),
        N.h4("The Key Observation"),
        N.para("For small inputs (n, k ≤ 1000), the O(nk) nested loop is perfectly fine and easy to reason about."),
        N.h4("Building the Solution"),
        N.para("For each index i, iterate over all valid predecessors j in [max(0, i−k), i−1] and take the max dp[j]. Then dp[i] = nums[i] + that max."),
    ]),
    N.h3("Code"),
    N.code(
        "def maxResult_naive(nums: list[int], k: int) -> int:\n    n = len(nums)\n    dp = [float('-inf')] * n\n    dp[0] = nums[0]\n    for i in range(1, n):\n        for j in range(max(0, i - k), i):  # O(k) per step\n            dp[i] = max(dp[i], dp[j] + nums[i])\n    return dp[-1]",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [float('-inf')] * n", {"code": True}), (" — Initialise all as unreachable (−∞). Only reachable indices get updated.", {})])),
    N.para(N.rich([("for j in range(max(0, i-k), i):", {"code": True}), (" — Iterate all valid predecessors. max(0, i−k) ensures we don't go below index 0. This inner loop is O(k).", {})])),
    N.para(N.rich([("dp[i] = max(dp[i], dp[j] + nums[i])", {"code": True}), (" — Take the best predecessor. The total work is O(nk).", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naïve DP", "O(nk)", "O(n)"],
        ["DP + Monotonic Deque", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stack / Queue (Monotonic Queue sub-category)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Monotonic Queue, DP + Monotonic Deque", {})])),
    N.callout(
        "When to recognize this pattern: DP recurrence that requires max or min over a sliding window of previous DP states. The window has a fixed size k. Naïve O(k) inner loop gives O(nk) total — the monotonic deque cuts this to O(n). Signal phrases: 'jump at most k steps', 'within distance k', 'last k elements'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DP + Monotonic Deque / Sliding Window Maximum technique:"),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (#239, Hard) — the canonical sliding window max problem; identical deque technique on raw array", {})])),
    N.bullet(N.rich([("Constrained Subsequence Sum", {"bold": True}), (" (#1425, Hard) — closest sibling: max subsequence sum where gap between chosen indices ≤ k", {})])),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), (" (#45, Medium) — min jumps to reach end; greedy BFS, no DP needed", {})])),
    N.bullet(N.rich([("Jump Game VII", {"bold": True}), (" (#1871, Medium) — reachability with DP + sliding window over boolean array", {})])),
    N.bullet(N.rich([("Frog Jump", {"bold": True}), (" (#403, Hard) — DP with variable jump size stored per node; more complex state than VI", {})])),
    N.bullet(N.rich([("Shortest Subarray with Sum at Least K", {"bold": True}), (" (#862, Hard) — monotonic deque over prefix sums for minimum-length variant", {})])),
    N.bullet(N.rich([("Maximum Points You Can Obtain from Cards", {"bold": True}), (" (#1423, Medium) — sliding window on score arrays", {})])),
    N.para("These problems share the core technique: O(1) sliding window max/min using a deque whose front is always the optimum."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section on Stack/Queue, Monotonic Queue sub-pattern.", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("jump_game_vi")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4) Append all blocks ────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
