"""
Notion in-place regeneration for Jump Game II (LeetCode #45).
Run from the Algorithms directory: python3 gen_jump_game_ii.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81c2-bce4-f97e5b811a73"

# ── 1) Set page properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=45,
    pattern="Greedy",
    subpatterns=["Track Current/Next Boundary"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Treat jumps as BFS levels; track cur_end (current level boundary) and farthest (next level boundary) — jump when you exhaust the current level.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Removed {wiped} old blocks.")

# ── 3) Build new body ────────────────────────────────────────────────────────
PROBLEM_STATEMENT = (
    "Given a 0-indexed array of integers nums of length n, you are initially positioned at nums[0]. "
    "Each element nums[i] represents the maximum length of a forward jump from index i. "
    "Return the minimum number of jumps to reach nums[n-1]. "
    "The test cases are generated such that you can always reach nums[n-1]."
)

SOL1_CODE = '''\
def jump(nums: list[int]) -> int:
    jumps = 0       # answer: total jumps taken
    cur_end = 0     # right boundary of current BFS level
    farthest = 0    # farthest index reachable from current level
    for i in range(len(nums) - 1):   # stop at n-2
        farthest = max(farthest, i + nums[i])  # best reach from i
        if i == cur_end:   # exhausted current level
            jumps += 1     # take the jump
            cur_end = farthest  # advance to next level
    return jumps
'''

SOL2_CODE = '''\
def jump(nums: list[int]) -> int:
    n = len(nums)
    dp = [float('inf')] * n
    dp[0] = 0                     # 0 jumps to reach index 0
    for i in range(n):            # from each position...
        for j in range(i + 1, min(i + nums[i] + 1, n)):
            dp[j] = min(dp[j], dp[i] + 1)  # relax
    return dp[n - 1]
'''

blocks = []

# ─── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider()
]

# ─── Solution 1 ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Greedy Boundary Tracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the minimum number of jumps to traverse an array. "
            "Each nums[i] gives a maximum jump distance — we can jump any amount from 1 to nums[i]. "
            "The key reframe: think of indices reachable in exactly k jumps as 'level k' in a BFS. "
            "Minimum jumps = the BFS level where the last index first becomes reachable."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naive approach: always jump the full nums[i] steps. This is wrong — it greedily extends "
            "each individual jump but ignores which jump-off point gives the best reach for the next level. "
            "Example: nums=[2,3,1,1,4]. Jumping max from 0 lands at index 2 (nums[2]=1, reach=3). "
            "But jumping just 1 step from 0 to index 1 (nums[1]=3, reach=4) reaches the end in one more jump. "
            "DP (O(n^2)) works but is too slow for n up to 10^4."
        ),
        N.h4("The Key Observation"),
        N.para(
            "In BFS for minimum jumps, we only care about HOW FAR each level extends, not which "
            "specific position within the level we jump from. The farthest reachable index from "
            "any position in the current level becomes the boundary of the next level. "
            "We can track this with just two numbers: cur_end (where current level ends) and "
            "farthest (best reach found while scanning the level)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Scan i from 0 to n-2. At each i, update farthest = max(farthest, i + nums[i]). "
            "When i reaches cur_end, we have explored the entire current level — take a jump, "
            "increment jumps, and set cur_end = farthest to open the next level. "
            "The loop stops at n-2 because we never need to jump from the last index — "
            "reaching it is the goal, and the jump that puts cur_end >= n-1 was already counted."
        ),
        N.callout(
            "Analogy: Think of it like a frog on lily pads in groups. Group 0 has only pad 0. "
            "From group 0, the frog can reach some set of pads — that's group 1. "
            "The frog jumps once to enter group 1 (it doesn't matter which pad in group 1 it lands on). "
            "The answer is: how many group transitions to include the last pad?",
            "🐸", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("jumps = 0", {"code": True}), " — initialize the answer counter to zero"])),
    N.para(N.rich([("cur_end = 0", {"code": True}), " — boundary of the current BFS level; initially just index 0"])),
    N.para(N.rich([("farthest = 0", {"code": True}), " — farthest index reachable from any position in the current level"])),
    N.para(N.rich([("for i in range(len(nums) - 1)", {"code": True}), " — scan i from 0 to n-2; no jump needed from last index"])),
    N.para(N.rich([("farthest = max(farthest, i + nums[i])", {"code": True}), " — i+nums[i] = farthest we can jump from position i; take the max over the whole level"])),
    N.para(N.rich([("if i == cur_end", {"code": True}), " — we have exhausted the current BFS level; must take a jump"])),
    N.para(N.rich([("jumps += 1", {"code": True}), " — count this jump; greedy commits to reaching farthest"])),
    N.para(N.rich([("cur_end = farthest", {"code": True}), " — advance to the next BFS level; it extends to farthest"])),
    N.para(N.rich([("return jumps", {"code": True}), " — minimum jumps to reach the last index"])),
    N.divider()
]

# ─── Solution 2 ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Dynamic Programming (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Define dp[i] = minimum number of jumps to reach index i. "
            "Base case: dp[0] = 0. For every other index, try all positions that can reach it."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion without memoization repeats subproblems exponentially. "
            "DP is the structured way to avoid recomputation."
        ),
        N.h4("The Key Observation"),
        N.para(
            "From position i, we can reach all j in [i+1, i+nums[i]]. "
            "For each such j, dp[j] = min(dp[j], dp[i]+1). "
            "This is a standard edge-relaxation approach — like Dijkstra but uniform-weight edges."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Initialize dp[0] = 0, all others infinity. "
            "For each i, for each reachable j, relax dp[j]. "
            "Answer is dp[n-1]. O(n^2) time, O(n) space — correct but too slow for large inputs."
        )
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [float('inf')] * n", {"code": True}), " — infinity means unreachable initially"])),
    N.para(N.rich([("dp[0] = 0", {"code": True}), " — we're already at index 0, zero jumps needed"])),
    N.para(N.rich([("for i in range(n)", {"code": True}), " — process each position as a potential jump source"])),
    N.para(N.rich([("for j in range(i+1, min(i+nums[i]+1, n))", {"code": True}), " — all positions reachable from i"])),
    N.para(N.rich([("dp[j] = min(dp[j], dp[i]+1)", {"code": True}), " — relax: reaching j via i costs one more jump than reaching i"])),
    N.para(N.rich([("return dp[n-1]", {"code": True}), " — minimum jumps to reach the last index"])),
    N.divider()
]

# ─── Complexity table ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy Boundary Tracking (Interview Pick)", "O(n)", "O(1)"],
        ["Dynamic Programming", "O(n²)", "O(n)"],
        ["Explicit BFS (level sets)", "O(n)", "O(1)"],
    ]),
    N.divider()
]

# ─── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Greedy"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Track Current/Next Boundary"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'minimum number of jumps/steps/moves to reach a goal' "
        "(2) each position gives a forward range you can move "
        "(3) O(1) space BFS desired — don't need an explicit queue "
        "(4) reachability guaranteed (no stuck-detection needed) "
        "(5) covering interval problems with minimum segments/clips",
        "🔎", "green_background"
    ),
    N.divider()
]

# ─── Related Problems ────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Jump Game", {"bold": True}), " (Medium) — Can you reach the last index? Same greedy scan, return bool (#55)"])),
    N.bullet(N.rich([("Jump Game III", {"bold": True}), " (Medium) — Jump ±nums[i] steps, reach a zero; BFS with visited set (#1306)"])),
    N.bullet(N.rich([("Jump Game VII", {"bold": True}), " (Medium) — Jump in [minJump, maxJump], identical boundary-tracking greedy (#1871)"])),
    N.bullet(N.rich([("Video Stitching", {"bold": True}), " (Medium) — Cover interval [0,T] with minimum clips; same greedy pattern (#1024)"])),
    N.bullet(N.rich([("Minimum Number of Taps to Open to Water Garden", {"bold": True}), " (Hard) — Cover [0,n] with min taps; identical algorithm (#1326)"])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), " (Medium) — Greedy interval scheduling; related greedy reasoning (#435)"])),
    N.para("These problems share the same core technique: scan forward, track the farthest boundary reachable, and commit to a new level when you exhaust the current one."),
    N.divider()
]

# ─── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("jump_game_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ─── Append all blocks ───────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
