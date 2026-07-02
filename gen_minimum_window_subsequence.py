"""
gen_minimum_window_subsequence.py
Regenerates the Notion page for LeetCode #727 Minimum Window Subsequence IN-PLACE.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8155-a92e-d3d60d77146a"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=727,
    pattern="Sliding Window",
    subpatterns=["Sliding Window Variable"],
    tc="O(|s1|·|s2|)",
    sc="O(1)",
    key_insight="Forward scan finds right boundary; backward scan tightens left boundary. start = i+1 after backward loop.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
PROBLEM_STATEMENT = (
    "Given strings s1 and s2, return the minimum window in s1 which will contain "
    "all the characters in s2 in order (as a subsequence). "
    "If there is no such window in s1 that covers all characters in s2, return the empty string "
    '"". If there are multiple such minimum-length windows, return the one with the smallest starting index.'
)

FWD_BWD_CODE = '''\
def minWindow(s1: str, s2: str) -> str:
    m, n = len(s1), len(s2)
    i, best = 0, ""
    while i < m:
        # Phase 1: forward scan — match s2 left-to-right
        j = 0
        while i < m and j < n:
            if s1[i] == s2[j]:
                j += 1
            i += 1
        if j < n:
            break  # s2 not fully matched — no more windows possible
        # Phase 2: backward scan — tighten left boundary
        end = i
        j = n - 1
        i -= 1
        while j >= 0:
            if s1[i] == s2[j]:
                j -= 1
            i -= 1
        start = i + 1  # i overshot by 1 in the backward loop
        if not best or end - start < len(best):
            best = s1[start:end]
        i = start + 1  # next anchor: just after this window's start
    return best
'''

BRUTE_CODE = '''\
def minWindow_brute(s1: str, s2: str) -> str:
    def is_subseq(window, t):
        j = 0
        for ch in window:
            if j < len(t) and ch == t[j]:
                j += 1
        return j == len(t)

    best = ""
    for start in range(len(s1)):
        for end in range(start + len(s2), len(s1) + 1):
            window = s1[start:end]
            if is_subseq(window, s2):
                if not best or len(window) < len(best):
                    best = window
                break  # first valid end for this start is always shortest
    return best
    # O(|s1|^2 * |s2|) — correct but too slow
'''

DP_CODE = '''\
def minWindow_dp(s1: str, s2: str) -> str:
    m, n = len(s1), len(s2)
    # dp[i][j] = start index in s1 such that s1[dp[i][j]:i]
    #            contains s2[0:j] as subsequence, or -1 if none
    dp = [[-1] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i  # empty s2: start = current position
    best = ""
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # chars match: inherit diagonal start
            else:
                dp[i][j] = dp[i - 1][j]       # no match: propagate from above
        if dp[i][n] != -1:
            window = s1[dp[i][n]:i]
            if not best or len(window) < len(best):
                best = window
    return best
    # O(m*n) time, O(m*n) space
'''

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.para(N.rich([
        ("Example: s1 = ", {}),
        ('"abcdebdde"', {"code": True}),
        (", s2 = ", {}),
        ('"bde"', {"code": True}),
        (" → ", {}),
        ('"bcde"', {"code": True}),
        (' (length 4, indices 1–4). Also "bdde" (length 4) at indices 5–8, but "bcde" comes first.', {}),
    ])),
    N.divider(),
]

# ── Solution 1: Two-Pointer Forward-Backward ─────────────────────────────
blocks += [
    N.h2("Solution 1 — Two-Pointer Forward-Backward (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the shortest contiguous window in s1 that contains all characters of s2 "
            "in-order (subsequence). We can choose any contiguous slice of s1 as a window, "
            "as long as s2 appears somewhere inside it with characters in the correct left-to-right order."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A standard sliding window (frequency map, expand/shrink) works when we only need "
            "characters present in any order. Here, order matters — s2 must appear as a subsequence. "
            "Brute force (try all O(|s1|²) substrings, check each in O(|s2|)) is too slow: O(|s1|²·|s2|)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "For each right endpoint we find (via a greedy forward scan), we can efficiently find "
            "the TIGHTEST left boundary by scanning backward — matching s2 from right-to-left. "
            "The backward scan greedily assigns each s2 character to the latest possible s1 position, "
            "shrinking the window as much as possible."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Start anchor i at 0. 2. Forward scan: advance i through s1, match s2 left-to-right. "
            "When j == len(s2), all matched — record end = i. 3. Backward scan: start from end, "
            "walk i leftward matching s2 right-to-left. When j < 0, start = i+1. "
            "4. Update best if window is shorter. 5. Next anchor = start+1. Repeat."
        ),
        N.callout(
            "Analogy: Reading a book forward to find the last word you need (right boundary), "
            "then reading backward to find the earliest first word (tightest left boundary).",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(FWD_BWD_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(s1), len(s2)", {"code": True}), " — cache string lengths for convenience."])),
    N.para(N.rich([("i, best = 0, \"\"", {"code": True}), " — i is our current scan anchor; best holds the shortest window found so far."])),
    N.para(N.rich([("j = 0", {"code": True}), " — j tracks how many chars of s2 we've matched so far in Phase 1."])),
    N.para(N.rich([("while i < m and j < n:", {"code": True}), " — advance until s1 exhausted or all of s2 matched."])),
    N.para(N.rich([("if s1[i] == s2[j]: j += 1", {"code": True}), " — on match, advance s2 pointer. Always advance i."])),
    N.para(N.rich([("if j < n: break", {"code": True}), " — s2 was not fully matched; no more valid windows possible from any further anchor."])),
    N.para(N.rich([("end = i", {"code": True}), " — i is one past the rightmost character of this window. Save it."])),
    N.para(N.rich([("j = n - 1; i -= 1", {"code": True}), " — reset j to last s2 index; step back to last matched s1 position for backward scan."])),
    N.para(N.rich([("if s1[i] == s2[j]: j -= 1", {"code": True}), " — backward match. Always decrement i (even on match)."])),
    N.para(N.rich([("start = i + 1", {"code": True}),
                   " — i was decremented one extra time on the final match. True start = i+1, NOT i."])),
    N.para(N.rich([("best = s1[start:end]", {"code": True}), " — update best if this window is shorter."])),
    N.para(N.rich([("i = start + 1", {"code": True}), " — next anchor begins one position after where this window started."])),
    N.divider(),
]

# ── Solution 2: Brute Force ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (All Substrings)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible contiguous window in s1, check if s2 is a subsequence of it, keep track of the shortest."),
        N.h4("What Doesn't Work"),
        N.para("This approach is correct but O(|s1|²·|s2|) — for large inputs it times out."),
        N.h4("The Key Observation"),
        N.para("Useful as a reference implementation to verify the optimized solution on small test cases."),
        N.h4("Building the Solution"),
        N.para("For each start, try increasing end positions. Once we find one valid window, shorter ones at the same start don't exist — break inner loop."),
        N.callout("Use this to verify edge cases only. In an interview, propose it first then immediately optimize.", "💡", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.divider(),
]

# ── Solution 3: DP ────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — DP Table"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Define dp[i][j] = the start index in s1 such that s1[dp[i][j]:i] contains s2[0:j] "
            "as a subsequence. If no valid start, dp[i][j] = -1."
        ),
        N.h4("What Doesn't Work"),
        N.para("Same time complexity as two-pointer (O(mn)) but uses O(mn) space — not ideal when space is constrained."),
        N.h4("The Key Observation"),
        N.para(
            "Recurrence: if s1[i-1] == s2[j-1], the start carrying over from dp[i-1][j-1] (diagonal). "
            "Otherwise, we inherit dp[i-1][j] (skip s1[i-1]). When dp[i][n] != -1, s1[dp[i][n]:i] is a valid window."
        ),
        N.h4("Building the Solution"),
        N.para("Initialize dp[i][0] = i for all i (empty s2 matches at the current position). Fill row by row."),
        N.callout("This approach is more naturally extensible to variants like 'how many windows contain s2?' or 'find all window start positions'.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(DP_CODE),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all substrings)", "O(|s1|²·|s2|)", "O(|s1|)"],
        ["Two-Pointer Fwd-Bwd (Optimal) ✓", "O(|s1|·|s2|)", "O(1)"],
        ["DP Table", "O(|s1|·|s2|)", "O(|s1|·|s2|)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Sliding Window Variable (subsequence-matching variant)"])),
    N.callout(
        "When to recognize this pattern: "
        "'Find minimum/shortest window containing X as a subsequence' — order matters, standard sliding window fails. "
        "Right boundary found with greedy forward scan; left boundary tightened with backward scan. "
        "Next anchor = found start + 1.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or adjacent technique:"),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), " (Hard) — #76: all chars of t any order; frequency map + classic sliding window"])),
    N.bullet(N.rich([("Is Subsequence", {"bold": True}), " (Easy) — #392: is t a subsequence of s? The core building block for brute force above"])),
    N.bullet(N.rich([("Number of Matching Subsequences", {"bold": True}), " (Medium) — #792: count how many words are subsequences of s; bucket by first char"])),
    N.bullet(N.rich([("Longest Common Subsequence", {"bold": True}), " (Medium) — #1143: max-length subsequence common to both; classic 2D DP"])),
    N.bullet(N.rich([("Distinct Subsequences", {"bold": True}), " (Hard) — #115: count ways to embed t as subsequence of s; counting DP"])),
    N.bullet(N.rich([("Shortest Common Supersequence", {"bold": True}), " (Hard) — #1092: shortest string containing both as subsequences; DP + reconstruction"])),
    N.para("These problems share the sequential in-order character matching technique (subsequence check)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.4/1.5 (Sliding Window Variable)", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_window_subsequence")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
