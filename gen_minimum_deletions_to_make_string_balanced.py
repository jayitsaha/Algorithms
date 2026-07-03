"""
gen_minimum_deletions_to_make_string_balanced.py
Regenerate Notion page for LeetCode #1653 — Minimum Deletions to Make String Balanced
DP pattern: Track b-count and a-deletions (single-pass O(n) space-optimal)
"""
import notion_lib as N

# ── Step 0: Create page (notion_page_id was null) ──────────────────────────
PAGE_ID = N.create_page("Minimum Deletions to Make String Balanced", 1653, "Medium", "🟡")
print("Created page:", PAGE_ID)

# ── Step 1: Set properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1653,
    pattern="Dynamic Programming",
    subpatterns=["Track b-count and a-deletions"],
    tc="O(n)",
    sc="O(1)",
    key_insight="At each position decide: delete this 'a' (cost 1) or keep all b's seen so far (cost b_count). dp = min(dp+1, b_count).",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe (new page is empty, but wipe is safe no-op) ────────────────
N.wipe_page(PAGE_ID)

# ── Step 3: Build body blocks ────────────────────────────────────────────────
blocks = []

# ── PROBLEM ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a string ", {}),
        ("s", {"code": True}),
        (" consisting only of characters ", {}),
        ("'a'", {"code": True}),
        (" and ", {}),
        ("'b'", {"code": True}),
        (". You can delete any number of characters in ", {}),
        ("s", {"code": True}),
        (" to make ", {}),
        ("s", {"code": True}),
        (" balanced. A string is balanced if there is no pair of indices ", {}),
        ("(i, j)", {"code": True}),
        (" such that ", {}),
        ("i < j", {"code": True}),
        (" and ", {}),
        ("s[i] = 'b'", {"code": True}),
        (" and ", {}),
        ("s[j] = 'a'", {"code": True}),
        (". Return the minimum number of deletions needed to make ", {}),
        ("s", {"code": True}),
        (" balanced.", {}),
    ])),
    N.divider(),
]

# ── SOLUTION 1 — OPTIMAL DP (O(n) time, O(1) space) ─────────────────────────
blocks += [
    N.h2("Solution 1 — DP: Track b-count and a-deletions (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "A balanced string has ALL 'a's before ALL 'b's — no 'b' can appear before an 'a'. "
            "We scan left-to-right and at every position we are deciding: what is the minimum cost "
            "to make the prefix balanced, ending here? We want a balanced string: any split point k "
            "means everything left of k is 'a' and everything right is 'b'."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: try every possible split point k (0 to n). For each k, count the 'b's "
            "in s[0..k-1] (must delete them) and the 'a's in s[k..n-1] (must delete them). "
            "This is O(n²) time. We can do much better."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Process characters left to right. Track two things: "
            "(1) b_count = how many 'b's we've seen so far (they appear before any future 'a'), "
            "(2) dp = minimum deletions to balance the string up to the current character. "
            "When we see a 'b': b_count += 1. "
            "When we see an 'a': this 'a' violates balance (a 'b' came before it). "
            "We have exactly TWO choices: "
            "  Option A — DELETE this 'a' (dp + 1). "
            "  Option B — DELETE all previous 'b's instead (b_count). "
            "We take the minimum: dp = min(dp + 1, b_count)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialize dp = 0 (no deletions yet), b_count = 0 (no b's seen). "
            "2. Scan each character c in s: "
            "   • If c == 'b': increment b_count (this b is now a problem for future a's). "
            "   • If c == 'a': dp = min(dp + 1, b_count) — cheapest way to handle this conflict. "
            "3. Return dp. "
            "The final dp value is the minimum deletions. This is a true DP because each state "
            "builds on the previous: dp[i] depends on dp[i-1] and b_count[i-1]."
        ),
        N.callout(
            "Analogy: Imagine scanning a to-do list left to right. Each time you find a task "
            "out of order ('a' after 'b'), you can either scratch out THIS task (cost 1) or "
            "go back and scratch out all the earlier out-of-order items (cost = how many b's you saw). "
            "Always pick whichever is cheaper.",
            "🧠", "blue_background"
        ),
    ]),

    N.h3("Code"),
    N.code(
        "def minDeletions(s: str) -> int:\n"
        "    dp = 0        # min deletions for balanced prefix so far\n"
        "    b_count = 0   # number of 'b' chars seen to the left\n"
        "\n"
        "    for c in s:\n"
        "        if c == 'b':\n"
        "            b_count += 1\n"
        "        else:  # c == 'a'\n"
        "            # Option A: delete this 'a' (dp + 1)\n"
        "            # Option B: delete all b's seen so far (b_count)\n"
        "            dp = min(dp + 1, b_count)\n"
        "\n"
        "    return dp\n"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("dp = 0", {"code": True}),
                   " — Start with zero deletions; the empty prefix is trivially balanced."])),
    N.para(N.rich([("b_count = 0", {"code": True}),
                   " — No 'b's seen yet; tracks how many 'b's have appeared to our left (each is a potential conflict with future 'a's)."])),
    N.para(N.rich([("for c in s:", {"code": True}),
                   " — Scan every character left to right."])),
    N.para(N.rich([("if c == 'b': b_count += 1", {"code": True}),
                   " — A 'b' doesn't create a problem now, but it becomes a liability for every 'a' that follows. Count it."])),
    N.para(N.rich([("else: dp = min(dp + 1, b_count)", {"code": True}),
                   " — An 'a' after some 'b's is a violation. We compare: (A) deleting this one 'a' costs dp+1 total; (B) deleting every 'b' seen so far costs b_count. Take the cheaper option."])),
    N.para(N.rich([("return dp", {"code": True}),
                   " — After the full scan, dp holds the minimum total deletions."])),
    N.divider(),
]

# ── SOLUTION 2 — DP TABLE (O(n) space, builds intuition visually) ─────────────
blocks += [
    N.h2("Solution 2 — DP Table (Bottom-Up Tabulation)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Define dp[i] = minimum deletions to make s[0..i-1] balanced. "
            "We build this table from left to right. "
            "The answer is dp[n]."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A pure recursive approach without memoization recomputes overlapping subproblems. "
            "The recurrence dp[i] = f(dp[i-1], ...) makes it obvious that we only need the "
            "previous value — which is why Solution 1 is O(1) space."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The recurrence is: "
            "• dp[0] = 0 (empty string). "
            "• If s[i] == 'b': dp[i+1] = dp[i] (b at end doesn't hurt). "
            "• If s[i] == 'a': dp[i+1] = min(dp[i] + 1, b_count_up_to_i). "
            "Because each state only depends on dp[i] and b_count, we can compress to O(1)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialize dp array of length n+1 with 0s. "
            "2. Track b_count as we fill the table. "
            "3. For each i from 0 to n-1: apply the recurrence based on s[i]. "
            "4. Return dp[n]."
        ),
        N.callout(
            "This explicit table makes the DP structure crystal clear. "
            "In an interview, derive the recurrence here first, then optimize to O(1) space.",
            "💡", "green_background"
        ),
    ]),

    N.h3("Code"),
    N.code(
        "def minDeletions(s: str) -> int:\n"
        "    n = len(s)\n"
        "    dp = [0] * (n + 1)  # dp[i] = min deletions for s[0..i-1]\n"
        "    b_count = 0\n"
        "\n"
        "    for i, c in enumerate(s):\n"
        "        if c == 'b':\n"
        "            b_count += 1\n"
        "            dp[i + 1] = dp[i]          # b at end: no new cost\n"
        "        else:  # c == 'a'\n"
        "            dp[i + 1] = min(dp[i] + 1, b_count)  # delete 'a' vs delete all b's\n"
        "\n"
        "    return dp[n]\n"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("dp = [0] * (n + 1)", {"code": True}),
                   " — Table of n+1 entries; dp[0]=0 is the base case (empty prefix)."])),
    N.para(N.rich([("b_count = 0", {"code": True}),
                   " — Tracks 'b's seen so far, needed for the recurrence."])),
    N.para(N.rich([("if c == 'b': dp[i+1] = dp[i]", {"code": True}),
                   " — A trailing 'b' doesn't disrupt balance; cost doesn't change."])),
    N.para(N.rich([("else: dp[i+1] = min(dp[i] + 1, b_count)", {"code": True}),
                   " — An 'a' after b's: cheapest fix is either delete this 'a' or delete all prior 'b's."])),
    N.para(N.rich([("return dp[n]", {"code": True}),
                   " — After processing all n characters, dp[n] is the answer."])),
    N.divider(),
]

# ── SOLUTION 3 — BRUTE FORCE (try all split points) ───────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force: Try All Split Points"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "A balanced string has exactly ONE split point k: all 'a's in s[0..k-1] and all 'b's in s[k..n-1]. "
            "For each possible k (0 to n), count the 'b's before k (must delete) plus 'a's after k (must delete)."
        ),
        N.h4("What Doesn't Work"),
        N.para("O(n²) time — too slow for large inputs (n up to 10^5). This is the starter solution to derive from, not to submit."),
        N.h4("The Key Observation"),
        N.para(
            "The number of 'b's to the left of k can be precomputed with a prefix sum. "
            "The number of 'a's to the right of k can be precomputed with a suffix sum. "
            "Then the answer is min over all k of prefix_b[k] + suffix_a[k]."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. prefix_b[k] = number of 'b's in s[0..k-1]. "
            "2. suffix_a[k] = number of 'a's in s[k..n-1]. "
            "3. ans = min(prefix_b[k] + suffix_a[k]) for k in 0..n."
        ),
    ]),

    N.h3("Code"),
    N.code(
        "def minDeletions(s: str) -> int:\n"
        "    n = len(s)\n"
        "    # prefix_b[k] = count of 'b' in s[0..k-1]\n"
        "    prefix_b = [0] * (n + 1)\n"
        "    for i in range(n):\n"
        "        prefix_b[i + 1] = prefix_b[i] + (1 if s[i] == 'b' else 0)\n"
        "\n"
        "    # suffix_a[k] = count of 'a' in s[k..n-1]\n"
        "    suffix_a = [0] * (n + 1)\n"
        "    for i in range(n - 1, -1, -1):\n"
        "        suffix_a[i] = suffix_a[i + 1] + (1 if s[i] == 'a' else 0)\n"
        "\n"
        "    return min(prefix_b[k] + suffix_a[k] for k in range(n + 1))\n"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("prefix_b[k]", {"code": True}),
                   " — Count of 'b's in the left portion s[0..k-1]; these must be deleted if k is the split point."])),
    N.para(N.rich([("suffix_a[k]", {"code": True}),
                   " — Count of 'a's in the right portion s[k..n-1]; these must be deleted."])),
    N.para(N.rich([("min(prefix_b[k] + suffix_a[k])", {"code": True}),
                   " — The answer is the split point that minimizes total deletions."])),
    N.divider(),
]

# ── COMPLEXITY ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DP — Track b-count (Optimal)", "O(n)", "O(1)"],
        ["DP Table (Tabulation)", "O(n)", "O(n)"],
        ["Brute Force — All Split Points", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── WHY IS THIS DP? ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The minimum deletions to balance s[0..i] depends on the optimal answer for s[0..i-1]. "
         "Each step builds on the previous step's best answer."),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursion that tries deleting each 'a' or 'b' would recompute the same "
         "prefix states many times. The DP avoids this by storing dp[i] once."),
    ])),
    N.para(N.rich([("Recurrence Relation: ", {"bold": True}), ""])),
    N.code(
        "# dp[i] = min deletions to balance s[0..i-1]\n"
        "# b_count = number of 'b's in s[0..i-1]\n"
        "\n"
        "dp[0] = 0\n"
        "if s[i] == 'b':\n"
        "    dp[i+1] = dp[i]               # 'b' at rightmost position: no new violation\n"
        "else:  # s[i] == 'a'\n"
        "    dp[i+1] = min(\n"
        "        dp[i] + 1,                # delete this 'a'\n"
        "        b_count                   # delete all 'b's seen so far\n"
        "    )\n",
        lang="python"
    ),
    N.callout(
        "Space Optimization: Since dp[i+1] only depends on dp[i] and b_count, "
        "we collapse the array to two variables. This is a classic DP space optimization.",
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Track b-count and a-deletions (linear scan DP with O(1) state)"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Binary alphabet (only 2 character types). "
        "(2) Need all of type X before type Y (no Y then X allowed). "
        "(3) Must minimize deletions / modifications. "
        "Key signal: 'balanced string' where one character type must precede another.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── RELATED PROBLEMS ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Minimum Number of Deletions to Make Sorted", {"bold": True}),
                     (" (Hard) — Generalization to sorted array; uses LIS-based DP.")])),
    N.bullet(N.rich([("Remove Boxes", {"bold": True}),
                     (" (Hard) — Interval DP variant for deletion with grouping.")])),
    N.bullet(N.rich([("Longest Common Subsequence", {"bold": True}),
                     (" (Medium) — Complementary view: max chars to KEEP = LCS; min to delete = n+m - 2*LCS.")])),
    N.bullet(N.rich([("Delete Operation for Two Strings", {"bold": True}),
                     (" (Medium) — Minimum deletions to make two strings equal; uses LCS.")])),
    N.bullet(N.rich([("Minimum Deletions to Make Character Frequencies Unique", {"bold": True}),
                     (" (Medium) — Greedy reduction of character counts; different pattern but same 'minimize deletions' framing.")])),
    N.bullet(N.rich([("Partition Labels", {"bold": True}),
                     (" (Medium) — Greedy linear scan deciding partition boundaries.")])),
    N.bullet(N.rich([("Minimum Insertions to Balance a Parentheses String", {"bold": True}),
                     (" (Medium) — Track open-paren count for cheap O(1)-space DP; structural twin.")])),
    N.para("These problems share the core technique: linear scan DP where the state is O(1) — just track a running count that represents the cost of the alternative choice."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Dynamic Programming section", "📚", "gray_background"),
]

# ── EMBED ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_deletions_to_make_string_balanced")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
