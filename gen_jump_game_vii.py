"""
gen_jump_game_vii.py — Notion updater for Jump Game VII (LeetCode #1871)
Updates page 39193418-809c-81ae-8676-c6ce8cbdf35a IN-PLACE.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ae-8676-c6ce8cbdf35a"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1871,
    pattern="Greedy",
    subpatterns=["BFS with Range"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Maintain a sliding window count 'pre' of reachable predecessors; if pre>0 and s[j]='0', mark j reachable in O(1).",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────
blocks = []

# ── Problem Statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a 0-indexed binary string ", {}),
        ("s", {"code": True}),
        (" and two integers ", {}),
        ("minJump", {"code": True}),
        (" and ", {}),
        ("maxJump", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if you can reach the last index of the string, starting from index 0. "
         "You can move from index ", {}),
        ("i", {"code": True}),
        (" to index ", {}),
        ("j", {"code": True}),
        (" only if: (1) ", {}),
        ("minJump <= j - i <= maxJump", {"code": True}),
        (", and (2) ", {}),
        ("s[j] == '0'", {"code": True}),
        (". Note: s[0] is always '0'.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Optimal ──
blocks += [
    N.h2("Solution 1 — Sliding Window Count (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to know, for each index j, whether there exists any reachable index i "
               "that can jump to j. The condition is: j - maxJump <= i <= j - minJump AND reach[i]=True."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach checks every index in [j-maxJump, j-minJump] for each j — "
               "O(n × maxJump) time, which is quadratic when maxJump is large (e.g., maxJump ≈ n)."),
        N.h4("The Key Observation"),
        N.para("The window [j-maxJump, j-minJump] slides by exactly 1 as j advances: one index enters "
               "at the right (j-minJump), one exits at the left (j-maxJump). Instead of re-scanning the "
               "window, maintain 'pre' = count of reachable positions in it. Add/subtract incrementally."),
        N.h4("Building the Solution"),
        N.para("For each j: (1) Add reach[j-minJump] to pre (enters window). "
               "(2) If pre > 0 and s[j]='0', mark reach[j]=True. "
               "(3) Subtract reach[j-maxJump] from pre (exits window). "
               "Since reach[] is boolean (0/1), arithmetic on it gives the count for free."),
        N.callout(
            "Analogy: Think of a hotel booking system. 'pre' is a counter of guests (reachable positions) "
            "currently checked in (in the window). As days advance (j increases), one guest checks in "
            "(enters window) and one checks out (exits window). You never need to list all guests — "
            "just track the count.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""def canReach(s: str, minJump: int, maxJump: int) -> bool:
    n = len(s)
    reach = [False] * n
    reach[0] = True
    pre = 0
    for j in range(1, n):
        if j - minJump >= 0:
            pre += reach[j - minJump]   # index enters window
        if pre > 0 and s[j] == '0':
            reach[j] = True
        if j - maxJump >= 0:
            pre -= reach[j - maxJump]   # index exits window
    return reach[-1]"""),
    N.h3("Line by Line"),
    N.para(N.rich([("reach = [False] * n; reach[0] = True", {"code": True}),
                   (" — reach[i] is True if index i can be landed on. We start at 0.", {})])),
    N.para(N.rich([("pre = 0", {"code": True}),
                   (" — running count of reachable positions in the current sliding window [j-max, j-min].", {})])),
    N.para(N.rich([("for j in range(1, n):", {"code": True}),
                   (" — sweep every index except 0 (already handled).", {})])),
    N.para(N.rich([("if j - minJump >= 0: pre += reach[j - minJump]", {"code": True}),
                   (" — index j-minJump just entered the window. Adds 1 if reachable, 0 if not.", {})])),
    N.para(N.rich([("if pre > 0 and s[j] == '0': reach[j] = True", {"code": True}),
                   (" — someone in window can jump here AND j is a '0' cell → reachable.", {})])),
    N.para(N.rich([("if j - maxJump >= 0: pre -= reach[j - maxJump]", {"code": True}),
                   (" — index j-maxJump just exited the window. Subtracts 1 if reachable, 0 if not.", {})])),
    N.para(N.rich([("return reach[-1]", {"code": True}),
                   (" — final answer: did we ever reach the last index?", {})])),
    N.divider(),
]

# ── Solution 2: Naive BFS ──
blocks += [
    N.h2("Solution 2 — Naive BFS (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Model this as a graph problem. Each '0' cell is a node. Directed edges connect "
               "i to j if minJump ≤ j-i ≤ maxJump and s[j]='0'. BFS finds reachability from node 0."),
        N.h4("What Doesn't Work"),
        N.para("Pure DFS with recursion can revisit nodes and is exponential without memoization. "
               "BFS with a visited set is correct but iterates over maxJump edges per node — O(n × maxJump)."),
        N.h4("The Key Observation"),
        N.para("BFS correctly establishes reachability, but the inner loop over [i+minJump, i+maxJump] "
               "is the bottleneck. This works correctly in practice for small maxJump values but TLEs "
               "when maxJump ≈ n."),
        N.h4("Building the Solution"),
        N.para("Use a deque. Enqueue index 0. For each dequeued index i, try every j in "
               "[i+minJump, i+maxJump] where s[j]='0' and j not visited. If j == n-1, return True. "
               "Return False if queue empties."),
    ]),
    N.h3("Code"),
    N.code("""from collections import deque

def canReach_bfs(s: str, minJump: int, maxJump: int) -> bool:
    n = len(s)
    visited = {0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in range(i + minJump, min(i + maxJump + 1, n)):
            if s[j] == '0' and j not in visited:
                if j == n - 1:
                    return True
                visited.add(j)
                queue.append(j)
    return (n - 1) in visited"""),
    N.h3("Line by Line"),
    N.para(N.rich([("visited = {0}; queue = deque([0])", {"code": True}),
                   (" — start BFS from index 0, marked visited.", {})])),
    N.para(N.rich([("for j in range(i + minJump, min(i + maxJump + 1, n)):", {"code": True}),
                   (" — try all valid jump targets from current position i.", {})])),
    N.para(N.rich([("if s[j] == '0' and j not in visited:", {"code": True}),
                   (" — only '0' cells that haven't been reached yet.", {})])),
    N.para(N.rich([("if j == n - 1: return True", {"code": True}),
                   (" — early exit: we found a path to the last index.", {})])),
    N.para(N.rich([("return (n - 1) in visited", {"code": True}),
                   (" — final check if last index was reached.", {})])),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive BFS", "O(n × maxJump)", "O(n)"],
        ["Sliding Window Count", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Greedy", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("BFS with Range (Sliding Window Reachability)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'Can you reach the end?' with a binary valid/invalid structure. "
        "(2) Jump distance falls within a range [minJump, maxJump]. "
        "(3) For each position, you need to check a contiguous range of predecessors for a property — "
        "maintain a running count instead of re-scanning. "
        "(4) Strings/arrays of '0'/'1' where movement is constrained.",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: ", {"italic": True}),
                   ("The sub-pattern 'BFS with Range' is an analysis-based classification; "
                    "it is not explicitly listed as a named sub-pattern in the DSA_Patterns_and_SubPatterns_Guide.md. "
                    "It is a specialization of the sliding window technique applied to BFS reachability.", {"italic": True})])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BFS reachability + range constraints):"),
    N.bullet(N.rich([("Jump Game", {"bold": True}), (" (Easy) — Single max jump size; greedy or DP reachability #55", {})])),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), (" (Medium) — Minimum jumps to reach end; greedy frontier expansion #45", {})])),
    N.bullet(N.rich([("Jump Game III", {"bold": True}), (" (Medium) — Jump ±arr[i] steps; BFS to find index with value 0 #1306", {})])),
    N.bullet(N.rich([("Jump Game IV", {"bold": True}), (" (Hard) — Teleport to same-value indices; BFS with adjacency lists #1345", {})])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), (" (Medium) — Max score with k-window jumps; DP + monotonic deque #1696", {})])),
    N.bullet(N.rich([("Frog Jump", {"bold": True}), (" (Hard) — Stone positions with ±1 step variation; DP with set per stone #403", {})])),
    N.bullet(N.rich([("Min Taps to Water Garden", {"bold": True}), (" (Hard) — Range coverage greedy; reduces to Jump Game II structure #1326", {})])),
    N.para("These problems share the core pattern: reachability over an array/string where "
           "predecessors that can reach each position form a contiguous range, enabling sliding window optimization."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Pattern: Greedy. "
              "Sub-pattern classification: Analysis-based (BFS with Range is not explicitly listed).",
              "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("jump_game_vii")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── 4) Append all blocks ───────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page {PAGE_ID}.")
print("NOTION OK", PAGE_ID)
