"""
gen_longest_substring_with_at_most_k_distinct_characters.py
Regenerates the Notion page for LC #340 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-812a-8a53-f3fd73bdb5be"
SLUG    = "longest_substring_with_at_most_k_distinct_characters"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 340,
    pattern     = "Sliding Window",
    subpatterns = ["Hash Map <= K Keys"],
    tc          = "O(n)",
    sc          = "O(k)",
    key_insight = "Expand right greedily; shrink left when distinct chars exceed k; delete key when count hits 0.",
    icon        = "🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given a string ", ("s", {"code": True}),
        " and an integer ", ("k", {"code": True}),
        ", return the length of the longest substring that contains at most ",
        ("k", {"code": True}), " distinct characters. "
        "For example, s=\"eceba\", k=2 → 3 (substring \"ece\" uses only {'e','c'})."
    ])),
    N.divider(),
]

# ── Solution 1: Optimal Sliding Window ──
sol1_code = '''\
def lengthOfLongestSubstringKDistinct(s: str, k: int) -> int:
    if k == 0: return 0
    char_count = {}
    left = result = 0
    for right in range(len(s)):
        c = s[right]
        char_count[c] = char_count.get(c, 0) + 1
        while len(char_count) > k:
            lc = s[left]
            char_count[lc] -= 1
            if char_count[lc] == 0:
                del char_count[lc]
            left += 1
        result = max(result, right - left + 1)
    return result\
'''

blocks += [
    N.h2("Solution 1 — Variable Sliding Window + Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the longest contiguous window in s that uses ≤ k different characters. The window can contain repeated characters — only distinct character count matters."),
        N.h4("What Doesn't Work"),
        N.para("Trying every possible substring is O(n²): for each starting index, extend rightward until we hit k+1 distinct chars. This is too slow for large inputs."),
        N.h4("The Key Observation"),
        N.para("A valid window shrinks only when a new distinct character enters. We can keep a running hash map of character counts; len(map) = distinct chars. Expand right freely, shrink left when len(map) > k. Each character enters and exits at most once → O(n) total."),
        N.h4("Building the Solution"),
        N.para("1) Two pointers: left and right defining the window. 2) Hash map: char → count inside window. 3) Expand right: add s[right] to map. 4) If len(map) > k: shrink left (decrement count, delete key if zero, left++). 5) Update result = max(result, right-left+1). Critical: delete key when count hits 0, otherwise len(map) stays wrong."),
        N.callout(
            "Analogy: Think of a hotel with k rooms. Every new guest (character) needs a room. If a new distinct guest arrives when all rooms are full, evict from the front (left pointer) until a room frees up. Track the longest stay.",
            "🏨", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if k == 0: return 0", {"code": True}), " — Edge case: zero distinct characters allowed means only empty substrings are valid; immediately return 0."])),
    N.para(N.rich([("char_count = {}", {"code": True}), " — Hash map from character to its count inside the current window. The number of keys equals distinct chars."])),
    N.para(N.rich([("left = result = 0", {"code": True}), " — left is the left window boundary; result stores the longest valid window length seen so far."])),
    N.para(N.rich([("for right in range(len(s)):", {"code": True}), " — right always advances forward one step; we try every possible right endpoint."])),
    N.para(N.rich([("char_count[c] = char_count.get(c, 0) + 1", {"code": True}), " — Add s[right] to window. get(c, 0) defaults to 0 for first occurrence."])),
    N.para(N.rich([("while len(char_count) > k:", {"code": True}), " — Window is invalid (too many distinct). Must be a while loop — may need multiple left advances to evict one character."])),
    N.para(N.rich([("char_count[lc] -= 1", {"code": True}), " — Reduce count of the leftmost character; one fewer occurrence in window."])),
    N.para(N.rich([("if char_count[lc] == 0: del char_count[lc]", {"code": True}), " — If fully evicted, remove the key so len(char_count) accurately reflects distinct count."])),
    N.para(N.rich([("left += 1", {"code": True}), " — Shrink window left boundary by one. Loop continues if still > k distinct."])),
    N.para(N.rich([("result = max(result, right - left + 1)", {"code": True}), " — Window [left, right] is now valid. Record its length if it beats our best."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
sol2_code = '''\
def lengthOfLongestSubstringKDistinct(s: str, k: int) -> int:
    result = 0
    for i in range(len(s)):
        seen = {}
        for j in range(i, len(s)):
            seen[s[j]] = seen.get(s[j], 0) + 1
            if len(seen) > k:
                break
            result = max(result, j - i + 1)
    return result\
'''

blocks += [
    N.h2("Solution 2 — Brute Force: All Substrings (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Enumerate all possible starting positions. For each start, extend rightward as long as distinct chars ≤ k. Stop when k+1 distinct encountered."),
        N.h4("What Doesn't Work (long term)"),
        N.para("O(n²) is too slow for large strings (n=50,000 → 2.5 billion operations). But this is a correct brute force that's easy to derive first in an interview."),
        N.h4("The Key Observation"),
        N.para("Once we can break early (when distinct > k), the inner loop is bounded on average. But worst case (k ≥ alphabet size) is still O(n²)."),
        N.h4("Building the Solution"),
        N.para("Two nested loops: outer picks start i, inner extends j. Track distinct chars in a local dict. Break inner loop early when over budget. The sliding window solution eliminates the re-scanning of the left portion by reusing state."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(s)):", {"code": True}), " — Try every starting index as the left boundary of a potential answer window."])),
    N.para(N.rich([("seen = {}", {"code": True}), " — Fresh distinct-char tracker for this starting position."])),
    N.para(N.rich([("if len(seen) > k: break", {"code": True}), " — Window starting at i can't be extended further; any longer substring would violate the constraint."])),
    N.para(N.rich([("result = max(result, j - i + 1)", {"code": True}), " — Record length of this valid window."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                          "Time",  "Space"],
        ["Brute Force (all substrings)",      "O(n²)", "O(k)"],
        ["Sliding Window + HashMap (Optimal)","O(n)",  "O(k)"],
        ["Sliding Window + Fixed Array",      "O(n)",  "O(1)=O(256)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Hash Map ≤ K Keys (Variable Sliding Window)"])),
    N.callout(
        "When to recognize this pattern: Problem says 'longest / shortest contiguous substring' + an upper-bound constraint like 'at most k distinct'. Need a variable-size window that shrinks when over budget. Track window contents with a hash map whose key count = distinct elements.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Hash Map ≤ K Keys / Variable Sliding Window):"),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), " (Medium) — k=all-distinct special case; every char must appear ≤ 1 time (#3)"])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), " (Medium) — Identical problem reframed; k=2 baskets/distinct fruits (#904)"])),
    N.bullet(N.rich([("Longest Repeating Character Replacement", {"bold": True}), " (Medium) — Window with at most k replacements; check via max-freq char (#424)"])),
    N.bullet(N.rich([("Subarrays with K Different Integers", {"bold": True}), " (Hard) — Exactly k distinct: atMost(k) - atMost(k-1) trick; same window base (#992)"])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), " (Hard) — Shortest window covering all chars of t; same expand/shrink structure (#76)"])),
    N.bullet(N.rich([("Longest Subarray of 1's After Deleting One Element", {"bold": True}), " (Medium) — At most 1 zero in window; variant of at-most-k pattern (#1493)"])),
    N.para("These problems share the core technique: variable sliding window where a hash map (or counter) tracks window contents and the shrink-loop restores a constraint."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.5 (Sliding Window: Dynamic/Variable) · Sub-Pattern: Hash Map ≤ K Keys", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
