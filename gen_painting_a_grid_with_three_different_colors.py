#!/usr/bin/env python3
"""
gen_painting_a_grid_with_three_different_colors.py
Notion page creator for LeetCode #1931 — Painting a Grid With Three Different Colors
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# Token override (notion_lib.py has redacted token)
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS["Authorization"] = f"Bearer {N.TOKEN}"

SLUG = "painting_a_grid_with_three_different_colors"

# ── Step 0: Create page (notion_page_id is null) ──────────────────────────────
PAGE_ID = N.create_page("Painting a Grid With Three Different Colors", 1931, "Hard", "🔴")
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1931,
    pattern="Dynamic Programming",
    subpatterns=["DP: Bitmask", "State Compression"],
    tc="O(3^m · n)",
    sc="O(3^m)",
    key_insight="Encode each column as a base-3 integer (state); precompute valid states and compatible pairs; run column-by-column DP.",
    icon="🔴"
)
print("Properties set.")

# ── Step 2: Build page body ───────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You have an "), ("m", {"code": True}), (" × "), ("n", {"code": True}),
        (" grid and "), ("3", {"bold": True}),
        (" colors (0=Red, 1=Green, 2=Blue). Paint every cell such that no two adjacent cells (up, down, left, right) share the same color. Return the count of valid colorings modulo 10⁹+7.\n\nConstraints: 1 ≤ m ≤ 5, 1 ≤ n ≤ 1000.")
    ])),
    N.divider(),
]

# Solution 1 — Tabulation
blocks += [
    N.h2("Solution 1 — Tabulation / Bottom-Up DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count valid colorings of an m×n grid. Cells have 3 color choices, and adjacent cells must differ. A brute-force approach tries all 3^(m·n) colorings — completely infeasible for n=1000."),

        N.h4("What Doesn't Work"),
        N.para("Row-by-row DP where the state encodes the entire current row fails because n can be 1000 — the state space 3^1000 is astronomically large. Similarly, per-cell DP with (row, col, color) doesn't capture the column adjacency constraint without also storing the previous column's full coloring."),

        N.h4("The Key Observation"),
        N.para("m ≤ 5 is tiny! There are only 3^m ≤ 243 possible column colorings. We can enumerate ALL of them. The adjacency constraint between two adjacent columns only depends on their coloring — not on anything to the left. This is the Markov property: the future depends only on the current column's state."),

        N.h4("Building the Solution"),
        N.para("1. Encode each column's coloring as a base-3 integer (digit i = color of row i).\n2. Filter to valid states: no two adjacent rows share a color.\n3. Precompute compatible pairs (s, t): for every row r, color(s,r) ≠ color(t,r).\n4. DP: dp[s] = ways to reach current column in state s.\n5. Transition: new_dp[t] += dp[s] for each compatible (s,t) pair.\n6. Sum all dp values after n columns."),

        N.callout(
            "Analogy: Think of each column as a 'type'. You're counting valid sequences of column types of length n, where consecutive types must be compatible. This is like counting valid paths in a graph where nodes are column types and edges are compatibility relations.",
            "🧠", "blue_background"
        ),
    ]),

    N.h3("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The number of valid full-grid colorings through column j ending in state t depends ONLY on how many valid partial colorings of columns 0..j−1 end in states compatible with t. We don't need to track the entire left portion — just the boundary state.\n\n"),
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Many different left-column sequences produce the same column state s. Without DP we'd recount all of them for every compatible next state t. DP memoizes: 'how many ways produce state s at column j?' — computed once, reused for all compatible t.")
    ])),

    N.h3("Recurrence Relation"),
    N.code(
        "dp[j][t] = Σ dp[j-1][s]   for all s ∈ valid_states where compatible(s, t)\n"
        "\n"
        "Base case:  dp[0][s] = 1    for all s ∈ valid_states\n"
        "Answer:     Σ dp[n-1][s]   for all s ∈ valid_states\n"
        "\n"
        "Where:\n"
        "  valid_states = {s ∈ [0, 3^m) : for all i in [0,m-1], digit(s,i) ≠ digit(s,i+1)}\n"
        "  compatible(s,t) = for all i in [0,m), digit(s,i) ≠ digit(t,i)",
        "python"
    ),

    N.h3("Code"),
    N.code(
        "def colorTheGrid(m: int, n: int) -> int:\n"
        "    MOD = 10**9 + 7\n"
        "    total = 3 ** m\n"
        "\n"
        "    def get_colors(state):\n"
        "        cols = []\n"
        "        for _ in range(m):\n"
        "            cols.append(state % 3)\n"
        "            state //= 3\n"
        "        return cols\n"
        "\n"
        "    def is_valid_column(state):\n"
        "        colors = get_colors(state)\n"
        "        return all(colors[i] != colors[i+1] for i in range(m-1))\n"
        "\n"
        "    def is_compatible(s, t):\n"
        "        cs, ct = get_colors(s), get_colors(t)\n"
        "        return all(cs[i] != ct[i] for i in range(m))\n"
        "\n"
        "    valid = [s for s in range(total) if is_valid_column(s)]\n"
        "    compat = {s: [t for t in valid if is_compatible(s, t)] for s in valid}\n"
        "\n"
        "    dp = {s: 1 for s in valid}  # column 0\n"
        "\n"
        "    for _ in range(n - 1):\n"
        "        new_dp = {s: 0 for s in valid}\n"
        "        for s in valid:\n"
        "            for t in compat[s]:\n"
        "                new_dp[t] = (new_dp[t] + dp[s]) % MOD\n"
        "        dp = new_dp\n"
        "\n"
        "    return sum(dp.values()) % MOD",
        "python"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("MOD = 10**9 + 7", {"code": True}), " — standard modulus for counting problems; apply at every accumulation to prevent overflow."])),
    N.para(N.rich([("total = 3 ** m", {"code": True}), " — upper bound on state space; we'll filter this to valid states only."])),
    N.para(N.rich([("get_colors(state)", {"code": True}), " — decode a base-3 integer into a list of m color values; repeatedly take mod 3 (LSB) and integer-divide."])),
    N.para(N.rich([("is_valid_column(state)", {"code": True}), " — check vertical adjacency: for each consecutive pair of rows, colors must differ."])),
    N.para(N.rich([("is_compatible(s, t)", {"code": True}), " — check horizontal adjacency: for each row, color in column s must differ from color in column t."])),
    N.para(N.rich([("valid = [...]", {"code": True}), " — enumerate all base-3 integers; keep only vertically valid ones. For m=5 this yields at most ~96 valid states."])),
    N.para(N.rich([("compat = {...}", {"code": True}), " — precompute once: for each valid state s, which valid states t can follow it? This is O(|valid|² · m) done once."])),
    N.para(N.rich([("dp = {s: 1 for s in valid}", {"code": True}), " — base case: column 0 can be any valid state in exactly 1 way."])),
    N.para(N.rich([("for _ in range(n - 1):", {"code": True}), " — process n−1 transitions (columns 1 through n−1)."])),
    N.para(N.rich([("new_dp[t] = (new_dp[t] + dp[s]) % MOD", {"code": True}), " — core transition: ways to reach state t at next column += ways we were in compatible state s. Apply MOD each step."])),
    N.para(N.rich([("return sum(dp.values()) % MOD", {"code": True}), " — sum across all final states: total valid colorings of the entire m×n grid."])),
    N.divider(),
]

# Solution 2 — Memoization
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define dp(col, prev_state) = number of ways to color columns col through n-1, given that column col-1 has coloring prev_state."),

        N.h4("What Doesn't Work"),
        N.para("Naive recursion without memoization: from any (col, prev_state) we branch into all compatible next states, repeating the same subproblems exponentially. At column 1 there are |valid| choices; at column 2, |valid|² paths — most reuse the same (col, state) pairs."),

        N.h4("The Key Observation"),
        N.para("The state (col, prev_state) fully determines the number of valid ways to complete the grid from that point forward. Adding @lru_cache collapses the exponential tree to a table of size n × |valid| — polynomial."),

        N.h4("Building the Solution"),
        N.para("Write the natural recursion: if col == n, return 1 (complete). Otherwise sum dp(col+1, t) for each t compatible with prev_state. Add @lru_cache. For column 0, sum dp(1, s) for each valid s."),

        N.callout("Memoization is easier to derive from the recurrence and great for explaining to an interviewer. Then optimize to tabulation to eliminate recursion overhead.", "💡", "green_background"),
    ]),

    N.h3("Code"),
    N.code(
        "from functools import lru_cache\n"
        "\n"
        "def colorTheGrid(m: int, n: int) -> int:\n"
        "    MOD = 10**9 + 7\n"
        "    total = 3 ** m\n"
        "\n"
        "    def get_colors(state):\n"
        "        cols = []\n"
        "        for _ in range(m):\n"
        "            cols.append(state % 3)\n"
        "            state //= 3\n"
        "        return cols\n"
        "\n"
        "    def is_valid_column(state):\n"
        "        colors = get_colors(state)\n"
        "        return all(colors[i] != colors[i+1] for i in range(m-1))\n"
        "\n"
        "    def is_compatible(s, t):\n"
        "        cs, ct = get_colors(s), get_colors(t)\n"
        "        return all(cs[i] != ct[i] for i in range(m))\n"
        "\n"
        "    valid = [s for s in range(total) if is_valid_column(s)]\n"
        "    compat = {s: [t for t in valid if is_compatible(s, t)] for s in valid}\n"
        "\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(col, prev_state):\n"
        "        if col == n:\n"
        "            return 1  # successfully colored all columns\n"
        "        total_ways = 0\n"
        "        for next_s in compat[prev_state]:\n"
        "            total_ways = (total_ways + dp(col + 1, next_s)) % MOD\n"
        "        return total_ways\n"
        "\n"
        "    # Try all valid states for column 0\n"
        "    return sum(dp(1, s) for s in valid) % MOD",
        "python"
    ),

    N.callout(
        "Warning: Memoization uses O(n × |valid|) cache space vs O(|valid|) for tabulation. For n=1000 and m=5 (96 valid states), memoization uses ~96,000 cache entries — fine in practice, but tabulation is cleaner.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(3^(m·n))", "O(m·n)", "Try every coloring — infeasible"],
        ["Tabulation (optimal)", "O(3^m · n)", "O(3^m)", "Precompute valid+compat; linear in n"],
        ["Memoization", "O(3^m · n)", "O(3^m · n)", "Same time; larger cache"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DP: Bitmask / State Compression — encode column colorings as base-3 integers; precompute valid states and transition table; column-by-column DP accumulation."])),
    N.callout(
        "When to recognize this pattern: Grid coloring/tiling with local adjacency constraints. One dimension is small (m ≤ 5 or k ≤ 20). Counting valid configurations (not maximizing). The phrase 'no two adjacent cells share the same color' with a grid where rows << columns.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same State Compression / Bitmask DP technique:"),
    N.bullet(N.rich([("Number of Ways to Paint N×3 Grid", {"bold": True}), " (LeetCode 1411, Hard) — precursor with m=3 fixed; same column-state DP pattern, simpler state space."])),
    N.bullet(N.rich([("Tiling a Rectangle with the Fewest Squares", {"bold": True}), " (LeetCode 1240, Hard) — state encodes row-profile; column-by-column tiling DP."])),
    N.bullet(N.rich([("Shortest Path Visiting All Nodes", {"bold": True}), " (LeetCode 847, Hard) — BFS + bitmask DP where state = (node, visited_set)."])),
    N.bullet(N.rich([("Minimum Cost to Connect Two Groups", {"bold": True}), " (LeetCode 1595, Hard) — bitmask DP where state represents set of covered targets."])),
    N.bullet(N.rich([("Student Attendance Record II", {"bold": True}), " (LeetCode 552, Hard) — state machine DP encoding attendance history as compact state."])),
    N.bullet(N.rich([("Travelling Salesman Problem", {"bold": True}), " (Classic, Hard) — O(2^n · n²) bitmask DP; canonical state compression DP."])),
    N.bullet(N.rich([("House Robber III", {"bold": True}), " (LeetCode 337, Medium) — Tree DP with two-state encoding (rob/skip) per node."])),
    N.para("These problems share the core technique: compress a multi-dimensional state (set of nodes, column coloring, attendance history) into a single integer to enable polynomial-time DP."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18: Dynamic Programming → DP: Bitmask sub-pattern", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | html=OK | notion=OK | page_id={PAGE_ID}")
