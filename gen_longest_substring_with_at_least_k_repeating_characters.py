"""
gen_longest_substring_with_at_least_k_repeating_characters.py
Notion in-place update for LeetCode #395.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-817e-afd3-f95f79c78864"

# ─── 1. Set properties ───────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=395,
    pattern=["Sliding Window"],
    subpatterns=["Divide & Conquer (Split on Invalid)", "Sliding Window Variable"],
    tc="O(n·26)",
    sc="O(n)",
    key_insight="Any char with count < k in current window is a mandatory split point — no valid substring can cross it.",
    icon="🟡"
)
print("Properties set.")

# ─── 2. Wipe old body ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── 3. Build body blocks ────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return the length of the longest substring of ", {}),
        ("s", {"code": True}),
        (" such that the frequency of each character in this substring is greater than or equal to ", {}),
        ("k", {"code": True}),
        (". A substring must consist of characters that all appear at least ", {}),
        ("k", {"code": True}),
        (" times within that substring.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Divide & Conquer ────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Divide & Conquer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the longest contiguous window where no character is 'underpowered' (appears fewer than k times). The challenge is that simple sliding window has no monotonic shrink condition — adding a character can fix a low count (window gets better), not just worse."),
        N.h4("What Doesn't Work"),
        N.para("Naive two-pointer: 'shrink left when some count < k' fails because there is no clear direction. Removing a character can drop its count below k (worse), while adding one can raise a count to exactly k (better). The window's validity is not monotone in its size."),
        N.h4("The Key Observation"),
        N.para("Any character with count < k in the CURRENT window is provably forbidden. If character c appears m < k times in the current window, any substring containing c will have count(c) ≤ m < k — violating the constraint. So c is a guaranteed split point: no valid answer can cross it."),
        N.h4("Building the Solution"),
        N.para("Count frequencies in the current window. If all chars ≥ k, return the full length (base case — it's valid!). Otherwise, find any bad character (count < k), split the string on every occurrence of that char, recursively solve each fragment, return the max. Recursion depth ≤ 26 since each split eliminates at least one distinct character from being a split point in sub-calls."),
        N.callout("Analogy: Think of bad characters as walls in a corridor. The longest corridor with no obstacles is the answer. The walls are mandatory — no valid path can pass through them.", "🧱", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import Counter\n"
        "\n"
        "def longestSubstring(s: str, k: int) -> int:\n"
        "    if len(s) == 0:\n"
        "        return 0\n"
        "    freq = Counter(s)\n"
        "    if all(v >= k for v in freq.values()):\n"
        "        return len(s)  # entire window is valid\n"
        "    # Find any character with count < k (mandatory split point)\n"
        "    bad = next(c for c in freq if freq[c] < k)\n"
        "    # Split on every occurrence of bad char\n"
        "    parts = s.split(bad)\n"
        "    return max(longestSubstring(p, k) for p in parts)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if len(s) == 0: return 0", {"code": True}), (" — Base case: empty string contributes nothing.", {})])),
    N.para(N.rich([("freq = Counter(s)", {"code": True}), (" — Count every character in the current window using Counter.", {})])),
    N.para(N.rich([("if all(v >= k ...): return len(s)", {"code": True}), (" — If every char meets the threshold, the entire window is valid — return its length. This is the 'all valid' base case.", {})])),
    N.para(N.rich([("bad = next(c for c in freq if freq[c] < k)", {"code": True}), (" — Pick the first bad character (any will do — we could pick any forbidden char and correctness holds).", {})])),
    N.para(N.rich([("parts = s.split(bad)", {"code": True}), (" — Split on every occurrence of the bad character. The bad char cannot appear in any valid answer, so splitting on it is safe.", {})])),
    N.para(N.rich([("return max(...)", {"code": True}), (" — Recursively solve each fragment and return the best. We take max (longest), not sum — the answer is a single contiguous substring.", {})])),
    N.divider(),
]

# ── Solution 2 — Sliding Window ──────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Sliding Window (Unique Count Enumeration)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The sliding window approach needs a monotonic condition to know when to shrink. Standard windows don't have one here. But what if we fix the number of unique characters the window must have? That restores monotonicity: 'shrink left when unique > target'."),
        N.h4("What Doesn't Work"),
        N.para("Without fixing unique count, there's no valid shrink rule. The window can oscillate between valid and invalid as we slide — no consistent direction for the left pointer."),
        N.h4("The Key Observation"),
        N.para("For any optimal answer, the substring has some number of distinct characters (1 to 26). If we enumerate that target count in an outer loop and run a standard sliding window for each, we are guaranteed to find the optimal answer. For each target_unique, the shrink condition 'unique > target' is perfectly monotonic."),
        N.h4("Building the Solution"),
        N.para("Outer loop: for target_unique from 1 to 26. Inner: two pointers (left, right). Track curr_unique (distinct chars in window) and curr_valid (chars with count ≥ k). Shrink when curr_unique > target_unique. Update answer when curr_unique == target_unique AND curr_valid == target_unique (all unique chars are valid)."),
        N.callout("The key: by fixing 'exactly target_unique distinct chars' as the window constraint, we get a clean monotonic shrink signal. This turns an ill-conditioned problem into a standard sliding window.", "🔑", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def longestSubstring(s: str, k: int) -> int:\n"
        "    unique_in_s = len(set(s))\n"
        "    result = 0\n"
        "    for target_unique in range(1, unique_in_s + 1):\n"
        "        freq = [0] * 26\n"
        "        left = curr_unique = curr_valid = 0\n"
        "        for right in range(len(s)):\n"
        "            ri = ord(s[right]) - ord('a')\n"
        "            if freq[ri] == 0:\n"
        "                curr_unique += 1\n"
        "            freq[ri] += 1\n"
        "            if freq[ri] == k:\n"
        "                curr_valid += 1\n"
        "            while curr_unique > target_unique:\n"
        "                li = ord(s[left]) - ord('a')\n"
        "                if freq[li] == k:\n"
        "                    curr_valid -= 1\n"
        "                freq[li] -= 1\n"
        "                if freq[li] == 0:\n"
        "                    curr_unique -= 1\n"
        "                left += 1\n"
        "            if curr_unique == target_unique == curr_valid:\n"
        "                result = max(result, right - left + 1)\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("unique_in_s = len(set(s))", {"code": True}), (" — Count distinct chars in s. We only need to iterate up to this many unique targets.", {})])),
    N.para(N.rich([("for target_unique in range(1, unique_in_s + 1):", {"code": True}), (" — Outer loop: fix the target number of distinct chars the window should have. At most 26 iterations.", {})])),
    N.para(N.rich([("if freq[ri] == 0: curr_unique += 1", {"code": True}), (" — A character just entered the window for the first time — increment unique count.", {})])),
    N.para(N.rich([("if freq[ri] == k: curr_valid += 1", {"code": True}), (" — This character just hit the k threshold — it is now a 'valid' character.", {})])),
    N.para(N.rich([("while curr_unique > target_unique:", {"code": True}), (" — Too many distinct chars — shrink from left until we're back to target. THIS is the monotonic condition.", {})])),
    N.para(N.rich([("if freq[li] == k: curr_valid -= 1", {"code": True}), (" — The left char was at exactly k — losing it drops it below threshold.", {})])),
    N.para(N.rich([("if curr_unique == target_unique == curr_valid:", {"code": True}), (" — All distinct chars in window appear ≥ k times. Valid window — update result.", {})])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all substrings)", "O(n²)", "O(n)"],
        ["Divide & Conquer (Interview Pick)", "O(n·26)", "O(n) stack"],
        ["Sliding Window (unique enum)", "O(n·26)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sliding Window / Divide & Conquer", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Divide & Conquer (Split on Invalid) + Sliding Window Variable (Unique Count Enumeration)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'Longest substring where ALL characters meet a threshold' — think D&C on bad chars. "
        "(2) Sliding window feels right but there is no monotonic shrink condition — enumerate a fixed property (unique count) in an outer loop to restore monotonicity. "
        "(3) Small fixed alphabet (≤ 26) — O(n·26) outer loop is fine.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), (" (Medium) — Standard variable sliding window with clean monotonic shrink — great precursor (#3)", {})])),
    N.bullet(N.rich([("Longest Substring with At Most K Distinct Characters", {"bold": True}), (" (Medium) — Unique-count sliding window, simpler valid condition (#340)", {})])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), (" (Medium) — 'At most 2 unique chars' — exact same unique-count window pattern (#904)", {})])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), (" (Hard) — Variable window, must cover all chars of pattern (#76)", {})])),
    N.bullet(N.rich([("Longest Repeating Character Replacement", {"bold": True}), (" (Medium) — Max window with at most k character replacements allowed (#424)", {})])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), (" (Medium) — Fixed-size window with frequency matching (#438)", {})])),
    N.para("These problems share the core sliding window technique; #395 is special because it requires either D&C or outer-loop enumeration to handle the non-monotonic validity condition."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.4 (Sliding Window Dynamic) + Divide & Conquer section", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_substring_with_at_least_k_repeating_characters")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — appended {len(blocks)} blocks to {PAGE_ID}")
