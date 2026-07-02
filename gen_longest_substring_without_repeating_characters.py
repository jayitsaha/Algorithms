"""
gen_longest_substring_without_repeating_characters.py
Notion IN-PLACE update for LeetCode #3 — Longest Substring Without Repeating Characters
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813b-acd3-f9f7589c421f"
SLUG    = "longest_substring_without_repeating_characters"

# ── 1) Properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 3,
    pattern     = "Sliding Window",
    subpatterns = ["Hash Set + Shrink on Duplicate"],
    tc          = "O(n)",
    sc          = "O(k)",
    key_insight = "Expand right freely; shrink left when duplicate enters; set mirrors window.",
    icon        = "🟡",
)
print("Properties set.")

# ── 2) Wipe old body ──
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Rebuild body ──
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (", return the length of the longest ", {}),
        ("substring", {"bold": True}),
        (" that contains no repeated characters. A substring is a contiguous sequence of characters — you cannot skip positions.", {}),
    ])),
    N.para("Example: s = \"abcabcbb\" → 3 (\"abc\"). s = \"bbbbb\" → 1 (\"b\"). s = \"pwwkew\" → 3 (\"wke\")."),
    N.divider(),
]

# ═══════════════════════════════════════════════════════════════════
# SOLUTION 1 — Sliding Window + Hash Set (Interview Pick)
# ═══════════════════════════════════════════════════════════════════
blocks += [
    N.h2("Solution 1 — Sliding Window + Hash Set (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the longest window [left, right] over the string where every character is unique. We need to efficiently track which characters are inside the window and respond when a duplicate enters."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all O(n²) starting positions and extend until a duplicate is found. Each extension is O(1) with a set, but we restart from scratch each time — O(n²) total. For n=10⁵ that's 10¹⁰ operations. Too slow."),
        N.h4("The Key Observation"),
        N.para("When we extend right and find a duplicate, we don't need to restart from zero. We only need to advance left until the duplicate is evicted. Because the window already had all-unique characters (invariant), there is exactly one copy inside — we find it by removing from the left one step at a time."),
        N.h4("Building the Solution"),
        N.para("Two pointers (left, right) define the window. A hash set tracks window contents. Move right forward. On duplicate: enter while loop — remove s[left] from set, advance left — until s[right] is no longer in the set. Add s[right] to set. Record max window length. Each character enters and leaves the set at most once → O(n)."),
        N.callout("Analogy: Think of the window as a sliding queue at a door — you can add new people at the right. The moment a known person tries to re-enter, you eject people from the left until that person is fully out, then let the newcomer in.", "🚪", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def lengthOfLongestSubstring(s: str) -> int:\n"
        "    char_set = set()             # mirrors current window contents\n"
        "    left = 0                     # left boundary of window\n"
        "    max_len = 0                  # best answer seen\n"
        "    for right in range(len(s)):  # expand right one step\n"
        "        while s[right] in char_set:       # duplicate found\n"
        "            char_set.remove(s[left])      # evict leftmost char\n"
        "            left += 1                     # shrink window\n"
        "        char_set.add(s[right])   # safe to include\n"
        "        max_len = max(max_len, right - left + 1)\n"
        "    return max_len"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("char_set = set()", {"code": True}), (" — Hash set that always contains exactly the characters in the current window. O(1) lookup and removal.", {})])),
    N.para(N.rich([("left = 0", {"code": True}), (" — Left boundary. Only advances forward, never back.", {})])),
    N.para(N.rich([("max_len = 0", {"code": True}), (" — Running maximum window length seen so far.", {})])),
    N.para(N.rich([("for right in range(len(s))", {"code": True}), (" — Expand right edge. Every index is visited exactly once by right.", {})])),
    N.para(N.rich([("while s[right] in char_set", {"code": True}), (" — Duplicate detected. We need to shrink until s[right] is no longer in the window.", {})])),
    N.para(N.rich([("char_set.remove(s[left])", {"code": True}), (" — Evict the leftmost character from both the window and the set.", {})])),
    N.para(N.rich([("left += 1", {"code": True}), (" — Advance left boundary. The while loop keeps going until s[right] is gone from the set.", {})])),
    N.para(N.rich([("char_set.add(s[right])", {"code": True}), (" — Now safe: no duplicate in [left, right]. Add s[right] to set.", {})])),
    N.para(N.rich([("max_len = max(max_len, right - left + 1)", {"code": True}), (" — Window length: right-left+1 (inclusive on both ends). Update best if larger.", {})])),
    N.divider(),
]

# ═══════════════════════════════════════════════════════════════════
# SOLUTION 2 — Hash Map (jump shrink)
# ═══════════════════════════════════════════════════════════════════
blocks += [
    N.h2("Solution 2 — Sliding Window + Hash Map (O(1) Jump Shrink)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal. But instead of stepping left one-by-one when a duplicate is found, can we jump left directly past the old occurrence?"),
        N.h4("What Doesn't Work"),
        N.para("The set approach works perfectly but uses a while loop to step left. For strings with many long windows this is fine, but we can do even better."),
        N.h4("The Key Observation"),
        N.para("If we store char → most recent index in a map, when s[right] is a duplicate at old index j, we know left must move to j+1. One direct assignment replaces the entire while loop."),
        N.h4("Building the Solution"),
        N.para("Map stores char → last seen index. On duplicate inside window (char_map[ch] >= left), set left = char_map[ch] + 1. Always update char_map[ch] = right (even if no duplicate — to stay current). Record max_len as usual."),
        N.callout("Guard: char_map[ch] >= left is critical. Without it, if ch was seen before the current window, we'd jump left backwards, which is wrong and would over-expand the window.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def lengthOfLongestSubstring(s: str) -> int:\n"
        "    char_map = {}                # char -> most recent index\n"
        "    left = 0\n"
        "    max_len = 0\n"
        "    for right, ch in enumerate(s):\n"
        "        if ch in char_map and char_map[ch] >= left:  # inside window\n"
        "            left = char_map[ch] + 1  # jump past old occurrence\n"
        "        char_map[ch] = right     # always update to latest\n"
        "        max_len = max(max_len, right - left + 1)\n"
        "    return max_len"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("char_map = {}", {"code": True}), (" — Dictionary mapping each character to its most recently seen index in the string.", {})])),
    N.para(N.rich([("if ch in char_map and char_map[ch] >= left", {"code": True}), (" — Two conditions: (1) ch was seen before, AND (2) it was inside the current window (not before left). Both must hold.", {})])),
    N.para(N.rich([("left = char_map[ch] + 1", {"code": True}), (" — Jump left to one past the old occurrence. This is the minimum left position that excludes the duplicate. O(1) — no loop.", {})])),
    N.para(N.rich([("char_map[ch] = right", {"code": True}), (" — Always update: even when no duplicate, so future iterations see the latest position.", {})])),
    N.divider(),
]

# ═══════════════════════════════════════════════════════════════════
# SOLUTION 3 — Brute Force
# ═══════════════════════════════════════════════════════════════════
blocks += [
    N.h2("Solution 3 — Brute Force (Baseline for Discussion)"),
    N.toggle_h3("💡 Intuition", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible starting index i. Extend j rightward until a duplicate is found. Track the best window length seen."),
        N.h4("What Doesn't Work"),
        N.para("O(n²) iterations — for n=10⁵ that is 10¹⁰ operations. TLE on LeetCode. Mention this to show you understand the baseline, then pivot to the O(n) solution."),
    ]),
    N.h3("Code"),
    N.code(
        "def lengthOfLongestSubstring(s: str) -> int:\n"
        "    max_len = 0\n"
        "    for i in range(len(s)):\n"
        "        seen = set()\n"
        "        for j in range(i, len(s)):\n"
        "            if s[j] in seen: break\n"
        "            seen.add(s[j])\n"
        "            max_len = max(max_len, j - i + 1)\n"
        "    return max_len  # O(n^2)"
    ),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time",   "Space"],
        ["Brute Force",           "O(n²)",  "O(k)"],
        ["Sliding Window + Set ✓","O(n)",   "O(k)"],
        ["Sliding Window + Map",  "O(n)",   "O(k)"],
    ]),
    N.para("k = distinct characters in s (≤ 26 for lowercase, ≤ 128 for ASCII — effectively O(1) constant)."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sliding Window", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Hash Set + Shrink on Duplicate (variable-size window, shrink on constraint violation)", {})])),
    N.callout(
        "When to recognize this pattern: Problem asks for 'longest/shortest substring satisfying a condition'. "
        "The condition involves uniqueness or bounded frequency. You can check validity in O(1) and restore it "
        "by shrinking from the left. Two pointers + a set/map = O(n) instead of O(n²).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique (variable sliding window + hash structure):"),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), (" (Hard) — Shrink only when all chars of t are covered; expand otherwise. (#76)", {})])),
    N.bullet(N.rich([("Longest Substring with At Most K Distinct Characters", {"bold": True}), (" (Medium) — Shrink when distinct count in window exceeds k. (#340)", {})])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), (" (Medium) — Longest subarray with at most 2 distinct values; same pattern, k=2. (#904)", {})])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), (" (Medium) — Fixed-size window + frequency count; slide and compare. (#438)", {})])),
    N.bullet(N.rich([("Permutation in String", {"bold": True}), (" (Medium) — Check if any permutation of p is a substring of s; fixed window. (#567)", {})])),
    N.bullet(N.rich([("Longest Repeating Character Replacement", {"bold": True}), (" (Medium) — At most k replacements allowed; shrink when window - max_freq > k. (#424)", {})])),
    N.para("These problems share the core technique: a variable window with a hash structure tracking element frequency or presence, shrinking from the left when a constraint is violated."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.4/1.5 (Sliding Window → Dynamic Window). Sub-pattern verified as 'Hash Set + Shrink on Duplicate'.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
