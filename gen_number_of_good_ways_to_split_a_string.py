"""
gen_number_of_good_ways_to_split_a_string.py
Regenerates the Notion page for LeetCode #1525 in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8128-9f6f-d48b453165fc"
SLUG = "number_of_good_ways_to_split_a_string"

print(f"[1/4] Setting properties for PAGE_ID={PAGE_ID}")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1525,
    pattern="Hash Tables",
    subpatterns=["Prefix-Suffix Distinct Counts"],
    tc="O(n)",
    sc="O(k)",
    key_insight="Start with all chars in right counter; walk left to right moving one char at a time; len(counter) gives distinct count only when zero keys are deleted.",
    icon="🟡"
)
print("[1/4] Properties set OK")

print("[2/4] Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"[2/4] Wiped {deleted} blocks")

print("[3/4] Building new page body...")
blocks = []

# ── Problem ──
blocks.append(N.h2("Problem"))
blocks.append(N.para(N.rich([
    ("You are given a string ", {}),
    ("s", {"code": True}),
    (". A ", {}),
    ("split at index i", {"bold": True}),
    (" divides the string into a left part ", {}),
    ("s[0..i]", {"code": True}),
    (" (inclusive) and a right part ", {}),
    ("s[i+1..n-1]", {"code": True}),
    (". A split is ", {}),
    ("good", {"bold": True}),
    (" if both parts contain the same number of distinct characters. Return the total number of good splits.", {}),
])))
blocks.append(N.para(N.rich([
    ("Example: ", {"bold": True}),
    ("s = \"aacaba\"", {"code": True}),
    (" → answer is 2 (split at i=2: \"aac\"|\"aba\" both have 2 distinct; split at i=3: \"aaca\"|\"ba\" both have 2 distinct).", {}),
])))
blocks.append(N.divider())

# ── Solution 1: Running Counter ──
blocks.append(N.h2("Solution 1 — Running Counter (Interview Pick)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para("At each possible split index i, we want to know: do both sides have the same number of distinct characters? Doing this naively means rebuilding the character set for both sides at every i — O(n²) total. Can we be smarter?"),

    N.h4("What Doesn't Work"),
    N.para("Rebuilding sets from scratch at every split point is too slow. For n=10^5, O(n²) operations would time out. We need to reuse work across split points."),

    N.h4("The Key Observation"),
    N.para("When we move from split i to split i+1, only one character changes sides: s[i] moves from the right partition to the left partition. Everything else stays the same. So we can maintain two running counters and update them incrementally."),

    N.h4("Building the Solution"),
    N.para("Initialize right_count = Counter(all of s) and left_count = empty. Walk left to right. At each i: move s[i] from right to left by incrementing left_count[s[i]] and decrementing right_count[s[i]]. If the decrement hits 0, delete that key (critical: len(Counter) counts all keys, including zeros — so zero-count keys must be removed for len() to give the correct distinct count). Then compare len(left_count) == len(right_count)."),

    N.callout(
        "Analogy: Imagine two piles of labelled blocks. You move one block at a time from the right pile to the left pile. After each move, you count how many distinct labels each pile has. The running counter is just tracking which labels are present and how many.",
        "🧠", "blue_background"
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "from collections import Counter\n\ndef numSplits(s: str) -> int:\n    right_count = Counter(s)     # all chars start on right\n    left_count = Counter()        # left starts empty\n    result = 0\n    for i in range(len(s) - 1):  # i = 0..n-2; both sides non-empty\n        c = s[i]\n        left_count[c] += 1        # move s[i] to left\n        right_count[c] -= 1\n        if right_count[c] == 0:   # zero key would corrupt len()\n            del right_count[c]\n        if len(left_count) == len(right_count):\n            result += 1\n    return result",
    "python"
))

blocks.append(N.h3("Line by Line"))
lines = [
    ("right_count = Counter(s)", "Build a frequency map of all characters in s. Initially, the entire string is on the 'right side' of the split."),
    ("left_count = Counter()", "The left side starts empty — no characters have moved yet."),
    ("for i in range(len(s) - 1):", "Iterate i from 0 to n-2. At split point i, left = s[0..i], right = s[i+1..n-1]. We stop at n-2 to keep both sides non-empty."),
    ("c = s[i]", "The character being 'moved' from right to left at this split."),
    ("left_count[c] += 1", "s[i] now belongs to the left partition."),
    ("right_count[c] -= 1", "Remove s[i] from the right partition's count."),
    ("if right_count[c] == 0: del right_count[c]", "CRITICAL: if count drops to 0, delete the key. Otherwise len(right_count) would include it as a distinct character even though it's no longer present on the right."),
    ("if len(left_count) == len(right_count):", "len(Counter) = number of keys = number of distinct characters (with nonzero frequency). Compare both sides."),
    ("result += 1", "Equal distinct counts on both sides — this is a good split!"),
]
for line, explanation in lines:
    blocks.append(N.para(N.rich([
        (line, {"code": True, "bold": True}),
        (" — " + explanation, {}),
    ])))
blocks.append(N.divider())

# ── Solution 2: Prefix + Suffix Arrays ──
blocks.append(N.h2("Solution 2 — Prefix + Suffix Arrays (Clearer for beginners)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para("Think of it as two separate tasks: (1) for each index i, what's the distinct count of s[0..i]? (2) For each index i, what's the distinct count of s[i..n-1]? Then combining them is trivial."),

    N.h4("What Doesn't Work"),
    N.para("Computing both answers from scratch at each i is O(n) per split, O(n²) total. We need to precompute."),

    N.h4("The Key Observation"),
    N.para("A left-to-right pass with a running set gives us prefix[i] in O(1) per step. Similarly, a right-to-left pass gives suffix[i]. After building both arrays, a final pass checks each split in O(1)."),

    N.callout(
        "This is the same pattern as Product of Array Except Self (#238): precompute left and right results, then combine. The only difference is we track distinct sets instead of products.",
        "🧠", "blue_background"
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "def numSplits(s: str) -> int:\n    n = len(s)\n    prefix = [0] * n          # prefix[i] = distinct chars in s[0..i]\n    suffix = [0] * n          # suffix[i] = distinct chars in s[i..n-1]\n    \n    left_set = set()\n    for i in range(n):\n        left_set.add(s[i])\n        prefix[i] = len(left_set)\n    \n    right_set = set()\n    for i in range(n - 1, -1, -1):\n        right_set.add(s[i])\n        suffix[i] = len(right_set)\n    \n    return sum(1 for i in range(n - 1)\n               if prefix[i] == suffix[i + 1])",
    "python"
))

blocks.append(N.h3("Line by Line"))
lines2 = [
    ("prefix = [0] * n", "Array to store: prefix[i] = count of distinct characters in s[0..i]."),
    ("suffix = [0] * n", "Array to store: suffix[i] = count of distinct characters in s[i..n-1]."),
    ("left_set = set(); for i in range(n): left_set.add(s[i]); prefix[i] = len(left_set)", "Left-to-right pass. Adding s[i] to the set either increases distinct count by 1 (new char) or leaves it unchanged (already present). Record len(set) at each position."),
    ("right_set = set(); for i in range(n-1, -1, -1): ...", "Right-to-left pass. Same logic, scanning backwards."),
    ("return sum(1 for i in range(n-1) if prefix[i] == suffix[i+1])", "Final comparison: split at i means left = s[0..i] (captured by prefix[i]) and right = s[i+1..n-1] (captured by suffix[i+1])."),
]
for line, explanation in lines2:
    blocks.append(N.para(N.rich([
        (line, {"code": True, "bold": True}),
        (" — " + explanation, {}),
    ])))
blocks.append(N.divider())

# ── Complexity ──
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution", "Time", "Space"],
    ["Brute Force (slice + set)", "O(n²)", "O(n)"],
    ["Prefix + Suffix Arrays", "O(n)", "O(n)"],
    ["Running Counter (pick)", "O(n)", "O(k) ≤ O(26) = O(1)"],
]))
blocks.append(N.divider())

# ── Pattern Classification ──
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Hash Tables", {})])))
blocks.append(N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Prefix-Suffix Distinct Counts", {})])))
blocks.append(N.callout(
    "When to recognize this pattern:\n"
    "• Problem asks about a property at every split point in a string or array\n"
    "• You need to compare a property on the LEFT vs RIGHT side of a partition\n"
    "• Computing from scratch at each index gives O(n²) → precompute to get O(n)\n"
    "• 'Distinct' or 'unique' character count signals: use a set or carefully managed Counter",
    "🔎", "green_background"
))
blocks.append(N.divider())

# ── Related Problems ──
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same technique:"))
related = [
    ("Product of Array Except Self", "Medium", "#238 — Prefix and suffix products; canonical two-pass precomputation pattern"),
    ("Count Unique Characters of All Substrings", "Hard", "#828 — Distinct-char contribution across all substrings with prefix boundary info"),
    ("Longest Substring Without Repeating Characters", "Medium", "#3 — Running distinct character tracking with sliding window"),
    ("Find All Anagrams in a String", "Medium", "#438 — Running counter with sliding window, comparing counts at each position"),
    ("Partition Equal Subset Sum", "Medium", "#416 — Equal-property split (sum instead of distinct count); DP approach"),
    ("Number of Substrings Containing All Three Characters", "Medium", "#1358 — Count substrings where distinct chars cross a threshold; uses prefix counting"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff})", {}),
        (" — " + note, {}),
    ])))
blocks.append(N.para("These problems share the same core technique: precomputing boundary-aware character set properties."))
blocks.append(N.divider())

# ── Interactive Visual Explainer ──
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for(SLUG)))
blocks.append(N.para(N.rich([
    ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
])))

print(f"[3/4] Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("[3/4] Notion page body rebuilt OK")
print(f"NOTION OK {PAGE_ID}")
