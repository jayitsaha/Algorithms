"""
gen_longest_repeating_character_replacement.py
Notion IN-PLACE update for LeetCode #424: Longest Repeating Character Replacement
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81e7-868d-eabd5ae0a72f"
SLUG    = "longest_repeating_character_replacement"

# ─── 1) Set properties ───────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=424,
    pattern="Sliding Window",
    subpatterns=["Max Freq + Window Size Check"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Valid window iff (window_size − max_freq) ≤ k; max_freq only grows, window slides not collapses.",
    icon="🟡"
)
print("Properties set.")

# ─── 2) Wipe existing body ──────────────────────────────────────────
print("Wiping old body...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ─── 3) Build new body ──────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a string "), ("s", {"code": True}),
        (" and an integer "), ("k", {"code": True}),
        (". You can choose any character of the string and change it to any other uppercase English character. "
         "You can perform this operation at most "), ("k", {"code": True}), (" times.\n\n"
         "Return the length of the longest substring containing the same letter you can get after performing the above operations.")
    ])),
    N.divider(),
]

# Solution 1 — Optimal Sliding Window
sol1_code = '''\
def characterReplacement(s: str, k: int) -> int:
    count = {}       # char frequencies in current window
    max_freq = 0     # highest single-char count (only grows)
    L = 0            # left boundary
    result = 0       # best window length

    for R in range(len(s)):
        count[s[R]] = count.get(s[R], 0) + 1
        max_freq = max(max_freq, count[s[R]])

        # invalid: need more replacements than k
        if (R - L + 1) - max_freq > k:
            count[s[L]] -= 1
            L += 1                       # slide by 1, not a while-loop

        result = max(result, R - L + 1)

    return result'''

blocks += [
    N.h2("Solution 1 — Optimal Sliding Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the longest window [L, R] where we can make all characters the same using at most k replacements. The best strategy inside any window: keep the most-frequent character and replace all others."),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries all O(n²) (L, R) pairs. For each, we scan the window's character counts to find the max frequency — O(n·26) total. This is too slow for n=100,000."),
        N.h4("The Key Observation"),
        N.para("Replacements needed = (window size) − (count of the most-frequent character). A window is valid iff (window_size − max_freq) ≤ k. We track max_freq as we expand, and only shrink by 1 when invalid — because we never need a window shorter than our current best."),
        N.h4("Building the Solution"),
        N.para("Expand R right every step. Add s[R] to count, update max_freq. If invalid (need > k), remove s[L] from count and advance L by 1. Update result = max(result, R−L+1). max_freq intentionally never decreases — it tracks the globally best single-char count, and we only grow the window when we beat it."),
        N.callout("Analogy: Imagine a paint crew that can repaint at most k tiles. You keep the dominant color and repaint the minority. You want the longest stretch of wall where the minority count ≤ k.", "🎨", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("count = {}", {"code": True}), " — frequency map tracking count of each character inside the current window [L, R]."])),
    N.para(N.rich([("max_freq = 0", {"code": True}), " — the highest single-character count ever seen across all windows visited. Never decreases."])),
    N.para(N.rich([("count[s[R]] = count.get(s[R], 0) + 1", {"code": True}), " — include the new rightmost character s[R] in the window's frequency map."])),
    N.para(N.rich([("max_freq = max(max_freq, count[s[R]])", {"code": True}), " — update max_freq upward. We only ever raise it here, never lower it after a shrink."])),
    N.para(N.rich([("if (R - L + 1) - max_freq > k:", {"code": True}), " — check if the window needs more than k replacements. If yes, it is invalid."])),
    N.para(N.rich([("count[s[L]] -= 1; L += 1", {"code": True}), " — remove the leftmost character from the window (slide left pointer). This shrinks the window by 1. We use ", ("if", {"code": True}), " not ", ("while", {"code": True}), " — we never need to shrink more than once per step."])),
    N.para(N.rich([("result = max(result, R - L + 1)", {"code": True}), " — record the current window size. Since we only shrink by 1 when invalid, result tracks the maximum valid window ever seen."])),
    N.divider(),
]

# Solution 2 — Brute Force
sol2_code = '''\
def characterReplacement_brute(s: str, k: int) -> int:
    n, result = len(s), 0
    for L in range(n):
        count = {}
        for R in range(L, n):
            count[s[R]] = count.get(s[R], 0) + 1
            max_freq = max(count.values())       # O(26) each inner step
            if (R - L + 1) - max_freq <= k:
                result = max(result, R - L + 1)
    return result'''

blocks += [
    N.h2("Solution 2 — Brute Force (Understanding Only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible substring. For each, check if it can be made uniform with ≤ k replacements."),
        N.h4("What Doesn't Work"),
        N.para("For n=100,000 this is O(n²·26) ≈ 2.6×10¹¹ operations — way too slow. But it's correct and useful for understanding."),
        N.h4("The Key Observation"),
        N.para("For every (L, R) pair, compute character frequencies, find the max, and apply the validity formula. The brute force makes the optimal algorithm's optimization obvious by contrast."),
        N.h4("Building the Solution"),
        N.para("Two nested loops over L and R. Maintain a running count dict as R expands. Check validity. Record best length."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for L in range(n):", {"code": True}), " — try every left endpoint as the start of the substring."])),
    N.para(N.rich([("for R in range(L, n):", {"code": True}), " — try every right endpoint for this L."])),
    N.para(N.rich([("max_freq = max(count.values())", {"code": True}), " — scan all character counts to find the dominant one. O(26) per step."])),
    N.para(N.rich([("if (R - L + 1) - max_freq <= k:", {"code": True}), " — same validity formula as the optimal solution."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²·26)", "O(26)"],
        ["Optimal Sliding Window", "O(n)", "O(26) = O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window (Variable / Dynamic)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Max Freq + Window Size Check — window valid iff (size − max_freq) ≤ k"])),
    N.callout(
        "When to recognize this pattern: 'longest substring/subarray' + 'at most k replacements/changes'. "
        "The constraint involves a budget on non-dominant characters within the window. "
        "Key signal: you need to track the most-frequent character inside a variable window.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sliding window + frequency tracking technique:"),
    N.bullet(N.rich([("Max Consecutive Ones III", {"bold": True}), " (Medium) — binary version of this exact problem: flip at most k zeros to ones. max_freq = count of 1s. (#1004)"])),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), " (Medium) — variable window; shrink when a duplicate enters. (#3)"])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), " (Hard) — find smallest window containing all chars of t. Similar variable shrink logic. (#76)"])),
    N.bullet(N.rich([("Permutation in String", {"bold": True}), " (Medium) — fixed-size sliding window checking frequency maps match. (#567)"])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), " (Medium) — fixed window; collect start positions of valid windows. (#438)"])),
    N.bullet(N.rich([("Longest Subarray of 1's After Deleting One Element", {"bold": True}), " (Medium) — k=1 flip variant. (#1493)"])),
    N.para("These problems all share the core technique: variable window expansion with a budget constraint on 'impurities' inside the window."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.4–1.5 (Sliding Window Variable / Dynamic). Sub-Pattern: Max Freq + Window Size Check.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4) Append all blocks ─────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
