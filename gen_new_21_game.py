"""
gen_new_21_game.py — Notion regeneration for LeetCode #837 New 21 Game
Pattern: Dynamic Programming / Sliding Window Probability
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81a7-a791-f028b006abdb"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=837,
    pattern="Dynamic Programming",
    subpatterns=["Sliding Window Probability"],
    tc="O(n + maxPts)",
    sc="O(n)",
    key_insight="dp[i] = window_sum / maxPts; slide the window instead of recomputing the sum each time.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build new body ─────────────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks.append(N.h2("Problem"))
blocks.append(N.para(N.rich([
    ("Alice plays the following game, risking her job.\n\n"
     "Alice starts with 0 points and draws numbers while she has fewer than ", {}),
    ("k", {"code": True}),
    (" points. During each draw she gains an integer in the range ", {}),
    ("[1, maxPts]", {"code": True}),
    (" with equal probability. She stops drawing when she gets ", {}),
    ("k", {"code": True}),
    (" or more points.\n\n"
     "Return the probability that Alice ends up with ", {}),
    ("n", {"code": True}),
    (" or fewer points. Answers within ", {}),
    ("10^-5", {"code": True}),
    (" of the actual answer are considered accepted.\n\n"
     "Constraints: 0 <= k <= n <= 10^4, 1 <= maxPts <= 10^4", {})
])))
blocks.append(N.divider())

# ── Solution 1 — DP with Sliding Window (Optimal / Interview Pick) ─────────────
blocks.append(N.h2("Solution 1 — DP with Sliding Window (Interview Pick)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "Alice keeps drawing cards in [1, maxPts] uniformly at random and stops the moment "
        "she reaches or exceeds k points. We want P(final score ≤ n). "
        "Think of it as: what is the probability of landing on each possible score in [k, n], "
        "and those are the scores she accepts."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "A brute-force simulation works but is O(n * maxPts) per state and too slow. "
        "A naive DP that recomputes the sum dp[i-1] + dp[i-2] + ... + dp[i-maxPts] for every i "
        "is also O(n * maxPts) — still too slow for n = 10^4, maxPts = 10^4."
    ),
    N.h4("The Key Observation"),
    N.para(
        "dp[i] = probability that Alice's score is exactly i when she stops (or during play). "
        "Specifically, for i < k, dp[i] is the probability she is currently at score i "
        "(and has not stopped yet). For i >= k, dp[i] is the probability she lands exactly at i.\n\n"
        "The recurrence is: dp[i] = (sum of dp[i-1] + dp[i-2] + ... + dp[max(0, i-maxPts)]) / maxPts\n\n"
        "The window of contributions always has exactly maxPts elements (clamped at boundaries). "
        "We can maintain a running window_sum to compute this in O(1) per step instead of O(maxPts)."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1. Initialize dp[0] = 1.0 (Alice starts at 0 with certainty).\n"
        "2. Maintain window_sum = dp[0] = 1.0.\n"
        "3. For each score i from 1 to n:\n"
        "   - dp[i] = window_sum / maxPts\n"
        "   - If i < k, add dp[i] to window_sum (Alice can still draw from score i)\n"
        "   - If i >= maxPts, subtract dp[i - maxPts] from window_sum (window slides out)\n"
        "4. Answer = sum(dp[k..n])."
    ),
    N.callout(
        N.rich([
            ("Analogy: ", {"bold": True}),
            ("Think of dp[i] as water flowing through a pipe of width maxPts. "
             "At each score i, exactly maxPts previous scores feed into it equally. "
             "Instead of summing all pipes every time, we slide a window — add the newest pipe, "
             "drop the oldest — keeping the total current in O(1) time.", {})
        ]),
        "🧠", "blue_background"
    )
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    """def new21Game(n: int, k: int, maxPts: int) -> float:
    # Edge case: already done or n is large enough to include all outcomes
    if k == 0 or n >= k + maxPts - 1:
        return 1.0

    dp = [0.0] * (n + 1)
    dp[0] = 1.0          # Start at 0 with certainty
    window_sum = 1.0     # Sliding window sum of dp[max(0,i-maxPts)..i-1]

    for i in range(1, n + 1):
        dp[i] = window_sum / maxPts       # Uniform probability from window

        if i < k:                          # Still drawing: add dp[i] to window
            window_sum += dp[i]

        if i >= maxPts:                    # Slide window: remove oldest entry
            window_sum -= dp[i - maxPts]

    return sum(dp[k:n + 1])               # Sum probabilities of accepting scores""",
    "python"
))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("if k == 0 or n >= k + maxPts - 1:", {"code": True}),
    (" — Edge cases: if k=0, Alice never draws (probability 1.0). "
     "If n >= k + maxPts - 1, even the worst case (drawing maxPts after reaching k-1) stays ≤ n, so probability is 1.0.", {})
])))
blocks.append(N.para(N.rich([
    ("dp = [0.0] * (n + 1)", {"code": True}),
    (" — DP array where dp[i] = probability of score exactly i occurring during play.", {})
])))
blocks.append(N.para(N.rich([
    ("dp[0] = 1.0", {"code": True}),
    (" — Base case: Alice starts at 0 with probability 1.", {})
])))
blocks.append(N.para(N.rich([
    ("window_sum = 1.0", {"code": True}),
    (" — Running sum of dp values that can contribute to next scores. "
     "Initially just dp[0] = 1.0.", {})
])))
blocks.append(N.para(N.rich([
    ("dp[i] = window_sum / maxPts", {"code": True}),
    (" — Each score in [i-maxPts, i-1] contributes equally (uniform distribution). "
     "Dividing the window sum by maxPts gives the probability of reaching exactly i.", {})
])))
blocks.append(N.para(N.rich([
    ("if i < k: window_sum += dp[i]", {"code": True}),
    (" — Score i is still a drawing state (not a stopping state), so future draws can originate here.", {})
])))
blocks.append(N.para(N.rich([
    ("if i >= maxPts: window_sum -= dp[i - maxPts]", {"code": True}),
    (" — The window can only go back maxPts steps. Slide the window by dropping the oldest entry.", {})
])))
blocks.append(N.para(N.rich([
    ("return sum(dp[k:n + 1])", {"code": True}),
    (" — Sum all accepting probabilities. Scores [k, n] are where Alice stops and we accept.", {})
])))

blocks.append(N.callout(
    N.rich([
        ("Why NOT sum(dp[0:k])?  ", {"bold": True}),
        ("Scores in [0, k-1] are intermediate states — Alice has NOT stopped yet when at those scores. "
         "Only scores >= k are stopping states. The answer is P(stops in [k, n]).", {})
    ]),
    "⚠️", "yellow_background"
))

blocks.append(N.divider())

# ── Solution 2 — Naive DP (Brute Force) ──────────────────────────────────────
blocks.append(N.h2("Solution 2 — Naive DP (O(n × maxPts), for understanding)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "Before optimizing, the naive DP makes the recurrence crystal clear. "
        "For each score i, every score j in [i-maxPts, i-1] could have transitioned to i "
        "with probability 1/maxPts, but only if j was still a drawing state (j < k)."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "The inner loop over maxPts values makes this O(n * maxPts) which is 10^8 operations "
        "in the worst case — too slow for the given constraints (TLE on large inputs)."
    ),
    N.h4("The Key Observation"),
    N.para(
        "This approach is valuable for correctness verification and understanding the structure "
        "of the DP before applying the sliding window optimization."
    ),
    N.callout("Use this approach to understand the recurrence, then optimize to Solution 1.", "📖", "gray_background")
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    """def new21Game_naive(n: int, k: int, maxPts: int) -> float:
    if k == 0 or n >= k + maxPts - 1:
        return 1.0

    dp = [0.0] * (n + 1)
    dp[0] = 1.0

    for i in range(1, n + 1):
        # Sum contributions from all valid previous states
        for j in range(max(0, i - maxPts), min(k, i)):
            dp[i] += dp[j] / maxPts

    return sum(dp[k:n + 1])""",
    "python"
))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("for j in range(max(0, i - maxPts), min(k, i)):", {"code": True}),
    (" — Iterate over all previous scores that could draw to reach i. "
     "j must be >= 0 (floor), < k (only drawing states contribute), and j+draw=i means draw=i-j in [1,maxPts] so j >= i-maxPts.", {})
])))
blocks.append(N.para(N.rich([
    ("dp[i] += dp[j] / maxPts", {"code": True}),
    (" — Each transition from j to i has uniform probability 1/maxPts.", {})
])))

blocks.append(N.divider())

# ── Why is this DP? ────────────────────────────────────────────────────────────
blocks.append(N.h2("Why is This Dynamic Programming?"))

blocks.append(N.h3("Optimal Substructure"))
blocks.append(N.para(
    "The probability of reaching score i depends directly on the probabilities of reaching "
    "scores i-1, i-2, ..., i-maxPts (those that can draw a card to reach i). "
    "We cannot compute dp[i] without knowing dp[j] for all j in the window — "
    "so subproblem solutions directly compose into the larger answer."
))

blocks.append(N.h3("Overlapping Subproblems"))
blocks.append(N.para(
    "In a naive recursive approach, computing P(score = i) would recursively call "
    "P(score = j) for j in [i-maxPts, i-1]. Each of those recursively calls their windows. "
    "The subproblems overlap massively — without memoization, exponential recomputation occurs. "
    "DP fills the table bottom-up so each subproblem is solved exactly once."
))

blocks.append(N.h3("Recurrence Relation"))
blocks.append(N.code(
    """# Base case
dp[0] = 1.0   # Start at 0 with certainty

# Recurrence: for i in [1, n]
#   Score i receives equal probability from each drawing state in [i-maxPts, i-1]
dp[i] = (1/maxPts) * sum(dp[j] for j in range(max(0, i-maxPts), min(k, i)))

# Equivalently with sliding window:
dp[i] = window_sum / maxPts
where window_sum = sum(dp[max(0,i-maxPts) .. i-1] where index < k)

# Answer
P(score <= n) = sum(dp[k..n])""",
    "python"
))

blocks.append(N.callout(
    N.rich([
        ("State definition: ", {"bold": True}),
        ("dp[i] is the probability that Alice's trajectory visits score i. "
         "For i < k, this is a transient state (she continues drawing). "
         "For i in [k, n], this is an accepting terminal state. "
         "For i > n, these terminal states are rejecting (not counted in answer).", {})
    ]),
    "🔐", "blue_background"
))

blocks.append(N.divider())

# ── Complexity ────────────────────────────────────────────────────────────────
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution", "Time", "Space", "Notes"],
    ["Naive DP", "O(n × maxPts)", "O(n)", "Two nested loops"],
    ["DP + Sliding Window (optimal)", "O(n + maxPts)", "O(n)", "One pass with O(1) window update"],
]))
blocks.append(N.para(
    "The sliding window optimization reduces the inner loop from O(maxPts) to O(1) per index, "
    "giving O(n) total for the main loop. The maxPts term comes from the edge-case check. "
    "Space is O(n) for the dp array; no further reduction is possible since we need all values."
))
blocks.append(N.divider())

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])))
blocks.append(N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Sliding Window Probability (DP)", {})])))
blocks.append(N.callout(
    N.rich([
        ("When to recognize this pattern:\n", {"bold": True}),
        ("• The problem asks for a probability or count with uniform random choices at each step.\n"
         "• Each state's value is the average of a fixed-width window of previous states.\n"
         "• A naive DP recurrence has a sliding window structure (sum of last W values).\n"
         "• Keywords: 'equal probability', 'draw from [1, maxPts]', 'expected value', "
         "'probability that score ≤ n'.", {})
    ]),
    "🔎", "green_background"
))
blocks.append(N.divider())

# ── Related Problems ─────────────────────────────────────────────────────────
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same technique (sliding window over DP states):"))

related = [
    ("Knight Probability in Chessboard", "Medium", "DP on 2D grid, probability of staying on board after k moves"),
    ("Coin Change II", "Medium", "DP counting ways to make amount; unbounded knapsack recurrence"),
    ("Dice Roll Simulation", "Hard", "DP counting sequences avoiding consecutive repeats; sliding window over forbidden states"),
    ("Soup Servings", "Medium", "Probability DP with state transitions across two quantities"),
    ("Arithmetic Slices II — Subsequence", "Hard", "DP counting with recurrence over previous states"),
    ("Minimum Difficulty of a Job Schedule", "Hard", "DP optimizing over intervals; related sliding-window structure"),
    ("Frog Jump", "Medium", "DP with set of reachable states at each stone; probability-like reachability"),
    ("Reaching Points", "Hard", "Reverse reasoning on DP states to avoid blowup"),
    ("Probability of a Two Boxes Having the Same Number of Distinct Balls", "Hard", "Combinatorial probability DP"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (f"{name}", {"bold": True}),
        (f" ({diff}) — {note}", {})
    ])))

blocks.append(N.para(
    "These problems share the core technique: define dp[i] as a probability or count, "
    "exploit the sliding window structure of the recurrence to avoid O(n × W) brute force."
))
blocks.append(N.callout(
    "📚 Sub-pattern 'Sliding Window Probability' — Analysis classification (not explicitly listed in DSA_Patterns guide under this exact label, but falls under DP → Sliding Window DP optimization).",
    "📖", "gray_background"
))
blocks.append(N.divider())

# ── Interactive Visual Explainer ─────────────────────────────────────────────
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for("new_21_game")))
blocks.append(N.para(N.rich([
    ("Step through the algorithm visually — use Next/Prev or arrow keys.",
     {"italic": True, "color": "gray"})
])))

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
