"""Regenerate Notion page for Frog Jump (LC #403) in-place."""
import notion_lib as N

PAGE_ID = "39193418-809c-8160-913a-f6048285867c"

# ─── 1. Set properties ───────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=403,
    pattern="Dynamic Programming",
    subpatterns=["DP with Jump Size State"],
    tc="O(n²)",
    sc="O(n²)",
    key_insight="State=(stone pos, last jump k); dp[pos]=set of arrival jump sizes; propagate k±1 forward.",
    icon="🔴"
)
print("Properties set.")

# ─── 2. Wipe old body ────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ─── 3. Build new body ───────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("A frog is on the first stone and wants to get to the last stone. "
         "An array ", {}),
        ("stones", {"code": True}),
        (" of sorted stone positions is given. If the frog's last jump was ", {}),
        ("k", {"code": True}),
        (" units, its next jump must be ", {}),
        ("k-1", {"code": True}),
        (", ", {}),
        ("k", {"code": True}),
        (", or ", {}),
        ("k+1", {"code": True}),
        (" units (must be positive). The first jump must be exactly 1. "
         "Return True if the frog can reach the last stone, False otherwise.", {})
    ])),
    N.divider()
]

# ─── Solution 1: Bottom-Up DP (Interview Pick) ───────────────────────
SOLN1_CODE = """\
def canCross(stones: list[int]) -> bool:
    if stones[1] != 1:
        return False
    stone_set = set(stones)
    dp = {s: set() for s in stones}  # dp[pos] = set of arrival jump sizes
    dp[0].add(0)                     # sentinel: "0 jump" to start
    for pos in stones:
        for k in dp[pos]:
            for next_k in (k-1, k, k+1):
                if next_k > 0 and (pos + next_k) in stone_set:
                    dp[pos + next_k].add(next_k)
    return bool(dp[stones[-1]])
"""

blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to know: from position 0, is there any valid sequence of jumps that lands "
            "the frog exactly on the last stone? The key constraint is that each jump size is "
            "bounded by ±1 from the previous jump size. This creates 'momentum' — you can't "
            "instantly jump from speed 1 to speed 100."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy fails because there's no local rule that guarantees global success — "
            "always jumping as far as possible may skip all remaining stones. "
            "Brute-force DFS is O(3^n) — exponential — because each step branches 3 ways "
            "and many paths revisit the same (stone, jump) combinations."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The frog's next valid jumps depend on both WHERE it is AND its last jump size k. "
            "Two frogs at the same stone with different k values have completely different futures. "
            "So the DP state must be (position, last_jump_size) — a 2D state space. "
            "Since jump size is bounded by O(n), total states = O(n²), which is tractable."
        ),
        N.h4("Building the Solution"),
        N.para(
            "For each stone, store the SET of all jump sizes that can reach it. "
            "Iterate stones left to right (they're sorted). For each (pos, k), try k-1, k, k+1 "
            "and push valid jump sizes forward to the next landing stones. "
            "Answer: the last stone's set is non-empty."
        ),
        N.callout(
            "Analogy: Think of the frog like a car that can only change speed by 1 unit per second. "
            "At each stone, we record every valid speed the car could have when it arrives. "
            "The set of speeds at the finish line tells us if the car can get there at all.",
            "🚗", "blue_background"
        )
    ]),
    N.h3("🔬 Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("Whether the frog can finish from (pos, k) depends only on the stones ahead "
         "and the current momentum k — not on how the frog reached pos. "
         "The subproblem is self-contained and composable.", {})
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Multiple paths can converge on the same (stone, k) state. Without memoization, "
         "we'd re-explore the same futures from that state repeatedly. "
         "DP merges all arrivals first, then expands forward exactly once per state.", {})
    ])),
    N.h3("📐 The Recurrence"),
    N.code(
        "dp[pos] = set of jump sizes k that can land the frog on stone at pos\n\n"
        "For each (pos, k) where k ∈ dp[pos]:\n"
        "    For next_k ∈ {k-1, k, k+1} where next_k > 0:\n"
        "        If (pos + next_k) ∈ stone_set:\n"
        "            dp[pos + next_k].add(next_k)\n\n"
        "Base case: dp[0] = {0}  # sentinel jump\n"
        "Answer: bool(dp[stones[-1]])",
        lang="python"
    ),
    N.h3("Code"),
    N.code(SOLN1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if stones[1] != 1:", {"code": True}),
                   (" — Fast fail: the first jump must be exactly 1 unit. If the second stone isn't at position 1, return False immediately.", {})])),
    N.para(N.rich([("stone_set = set(stones)", {"code": True}),
                   (" — Build a set for O(1) membership checks: 'is this position a valid stone?'", {})])),
    N.para(N.rich([("dp = {s: set() for s in stones}", {"code": True}),
                   (" — Each stone gets an empty set. dp[pos] will hold all jump sizes that can land on pos.", {})])),
    N.para(N.rich([("dp[0].add(0)", {"code": True}),
                   (" — Seed with sentinel 0. Processing k=0 at pos=0 tries next_k ∈ {-1,0,1}; only 1 is valid, bootstrapping the first jump.", {})])),
    N.para(N.rich([("for pos in stones:", {"code": True}),
                   (" — Iterate all stone positions in sorted order (left to right).", {})])),
    N.para(N.rich([("for k in dp[pos]:", {"code": True}),
                   (" — For each valid arrival jump size at this stone, try extending from here.", {})])),
    N.para(N.rich([("for next_k in (k-1, k, k+1):", {"code": True}),
                   (" — Try all three momentum options: slow down, maintain, or speed up.", {})])),
    N.para(N.rich([("if next_k > 0 and (pos + next_k) in stone_set:", {"code": True}),
                   (" — Skip jump=0 (no-op would cause infinite loop) and jumps that land off-stone.", {})])),
    N.para(N.rich([("dp[pos + next_k].add(next_k)", {"code": True}),
                   (" — Record: the next stone can be reached with jump size next_k.", {})])),
    N.para(N.rich([("return bool(dp[stones[-1]])", {"code": True}),
                   (" — If the last stone's set is non-empty, the frog made it. Return True.", {})])),
    N.callout(
        "⚠️ Why dp[0]={0} not {1}? The sentinel 0 naturally produces the first jump of 1 via "
        "k=0 → next_k=1. Seeding with 1 would assume the first jump happened without validating "
        "stones[1]==1. The sentinel approach is cleaner and self-validating.",
        "⚠️", "yellow_background"
    ),
    N.divider()
]

# ─── Solution 2: Top-Down Memoization ────────────────────────────────
SOLN2_CODE = """\
def canCross(stones: list[int]) -> bool:
    stone_set = set(stones)
    last = stones[-1]
    memo = {}  # (pos, k) -> bool: can frog reach last stone from here?

    def dfs(pos, k):
        if pos == last:
            return True
        if (pos, k) in memo:
            return memo[(pos, k)]
        result = False
        for next_k in (k-1, k, k+1):
            nxt = pos + next_k
            if next_k > 0 and nxt in stone_set:
                if dfs(nxt, next_k):
                    result = True
                    break
        memo[(pos, k)] = result
        return result

    return dfs(0, 0)
"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Think recursively: 'Can the frog reach the last stone from its current (pos, k) state?' "
            "This maps directly to a function dfs(pos, k) returning True or False."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Without memoization, dfs explodes exponentially — O(3^n). "
            "But (pos, k) states repeat: multiple paths lead to the same stone with the same jump. "
            "Once we know dfs(5, 2) = True, we never need to recompute it."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Cache dfs(pos, k) → bool. This transforms O(3^n) into O(n²) because "
            "there are only O(n²) distinct (pos, k) states and each is computed once."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Base case: pos == last → True. "
            "Recursive case: try dfs(pos + next_k, next_k) for next_k ∈ {k-1,k,k+1} "
            "filtered by next_k>0 and landing on a stone. Short-circuit on first True found."
        )
    ]),
    N.h3("Code"),
    N.code(SOLN2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("memo = {}", {"code": True}),
                   (" — Cache mapping (pos, k) → bool. Prevents re-exploring the same state twice.", {})])),
    N.para(N.rich([("def dfs(pos, k):", {"code": True}),
                   (" — Recursive function: 'can the frog reach the last stone from (pos, last_jump=k)?'", {})])),
    N.para(N.rich([("if pos == last: return True", {"code": True}),
                   (" — Base case: already at the destination, success!", {})])),
    N.para(N.rich([("if (pos, k) in memo: return memo[(pos, k)]", {"code": True}),
                   (" — Cache lookup: if we've solved this exact state before, reuse the answer.", {})])),
    N.para(N.rich([("if dfs(nxt, next_k): result = True; break", {"code": True}),
                   (" — Short-circuit: if any branch succeeds, no need to try others.", {})])),
    N.para(N.rich([("memo[(pos, k)] = result", {"code": True}),
                   (" — Cache the final answer for this state before returning.", {})])),
    N.divider()
]

# ─── Complexity ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute-Force DFS", "O(3^n)", "O(n)", "Exponential — TLE for n>30"],
        ["Top-Down Memoization", "O(n²)", "O(n²)", "Intuitive recursion with cache"],
        ["Bottom-Up Tabulation ✓", "O(n²)", "O(n²)", "Iterative, no recursion stack"],
    ]),
    N.divider()
]

# ─── Pattern Classification ───────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DP with Jump Size State", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'Reach position X from 0, each step constrained by previous step size.' "
        "(2) Position alone does not determine future options — you need additional state (speed/momentum/history). "
        "(3) Bounded branching factor (3 candidates per step) keeps total states polynomial. "
        "(4) Greedy or simple BFS fails due to local-global mismatch.",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: ", {"italic": True}),
        ("'DP with Jump Size State' is a new sub-pattern classification based on analysis. "
         "The closest guide entry is 'DP: State Machine' (Section 18). "
         "This variant carries jump-size as the extra carried state rather than a discrete phase label.", {"italic": True})
    ])),
    N.divider()
]

# ─── Related Problems ─────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related DP-with-extra-state technique:"),
    N.bullet(N.rich([("Jump Game", {"bold": True}), (" (Medium) — Simpler version: can you reach end? No momentum constraint, greedy or 1D DP. (#55)", {})])),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), (" (Medium) — Minimum jumps to last index; unconstrained jump sizes; greedy BFS. (#45)", {})])),
    N.bullet(N.rich([("Jump Game III", {"bold": True}), (" (Medium) — Jump ±arr[i] from each index; BFS reachability; no momentum. (#1306)", {})])),
    N.bullet(N.rich([("Jump Game IV", {"bold": True}), (" (Hard) — BFS with same-value teleportation portals; no momentum. (#1345)", {})])),
    N.bullet(N.rich([("Jump Game VII", {"bold": True}), (" (Medium) — Sliding window DP over reachable ranges. (#1871)", {})])),
    N.bullet(N.rich([("Best Time to Buy/Sell Stock with Cooldown", {"bold": True}), (" (Medium) — State machine DP: state=(hold/cash/cooldown). Same 'extra state' pattern. (#309)", {})])),
    N.bullet(N.rich([("Climbing Stairs", {"bold": True}), (" (Easy) — Foundational: reach stair n jumping 1 or 2. Fixed jump set, no momentum constraint. (#70)", {})])),
    N.para("These problems share the core pattern: position is insufficient state — extra information (jump size, momentum, transaction phase) must be carried alongside position."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming) — Sub-Pattern: DP with Jump Size State (Analysis classification)", "📚", "gray_background"),
]

# ─── Embed visual explainer ───────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("frog_jump")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ]))
]

# ─── Append all blocks ────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
