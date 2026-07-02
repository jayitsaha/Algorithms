"""
gen_longest_substring_with_at_most_two_distinct_characters.py
Notion IN-PLACE update for LeetCode #159.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81a0-a6b2-f5ce704b5094"
SLUG = "longest_substring_with_at_most_two_distinct_characters"

# ─── 1) Set page properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=159,
    pattern="Sliding Window",
    subpatterns=["Hash Map <= 2 Keys"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Store last-seen index per char; evict the char with the leftmost last-index when a 3rd distinct char enters the window.",
    icon="🟡"
)
print("Properties set.")

# ─── 2) Wipe old body ───
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── 3) Build new body ───
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given a string ",
        ("s", {"code": True}),
        ", return the length of the longest substring that contains at most two distinct characters."
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ('s = "eceba"', {"code": True}),
        ' -> 3   (longest valid window: "ece", uses only {e, c})'
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ('s = "ccaab"', {"code": True}),
        ' -> 4   (longest valid window: "ccaa", uses only {c, a})'
    ])),
    N.para("Edge cases: empty string returns 0; string with 1 distinct character returns len(s); string with exactly 2 distinct characters returns len(s); string where every character is unique returns 2 (or 1 if single character)."),
    N.divider()
]

# ── Solution 1 — Optimal ──
SOL1_CODE = """\
def lengthOfLongestSubstringTwoDistinct(s: str) -> int:
    char_map = {}        # char -> last index seen in current window
    left = 0             # left boundary (inclusive)
    result = 0           # best valid window length

    for right in range(len(s)):
        char_map[s[right]] = right   # add/update char's last-seen position

        if len(char_map) > 2:        # 3rd distinct char appeared — invalid
            leftmost = min(char_map.values())   # char with earliest last-index
            del char_map[s[leftmost]]            # evict it from the map
            left = leftmost + 1                  # shrink window past it

        result = max(result, right - left + 1)  # window is valid; record if best

    return result
"""

blocks += [
    N.h2("Solution 1 — Sliding Window with Last-Index Map (Interview Pick)"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We are looking for the longest contiguous slice of the string that stays within a budget of 2 distinct characters. This is a 'largest valid window' problem — the window grows from the right and shrinks from the left when it exceeds the budget."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: enumerate all O(n^2) substrings and check each one's distinct-character count. This is too slow for strings up to 50,000 characters. We need a smarter approach that avoids re-examining characters we have already processed."),
        N.h4("The Key Observation"),
        N.para("When a 3rd distinct character enters from the right, we do not need to restart. We advance the left pointer until one character fully exits the window. The right pointer never moves backward — this amortized movement makes the whole algorithm O(n)."),
        N.h4("Building the Solution"),
        N.para("Maintain char_map: character to last index seen. Expand right freely. When map size exceeds 2, find the character with the minimum last-index (its last occurrence is leftmost). Delete it from the map. Set left = that index + 1. Then record window size."),
        N.callout(
            "Analogy: A petri dish that can only culture 2 bacterial types at once. As you slide it along a sample strip, when a 3rd type enters from the right, slide the left wall forward until the oldest type exits entirely. Record the longest dish width where the 2-type rule held.",
            "🧪", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("char_map = {}", {"code": True}), " — Hash map from character to its most recent index in the current window. Bounded to at most 3 keys at any moment."])),
    N.para(N.rich([("left = 0", {"code": True}), " — Left boundary of the sliding window. Only ever moves forward (never shrinks back)."])),
    N.para(N.rich([("result = 0", {"code": True}), " — Running maximum of valid window lengths seen so far."])),
    N.para(N.rich([("for right in range(len(s)):", {"code": True}), " — Right boundary expands exactly one step per iteration. Each character is visited once."])),
    N.para(N.rich([("char_map[s[right]] = right", {"code": True}), " — Record or update where we last saw this character. If it is new, map size may grow to 3."])),
    N.para(N.rich([("if len(char_map) > 2:", {"code": True}), " — Window is invalid: 3 distinct characters present. Use 'if' not 'while' — we add exactly one char per step so the count can overshoot by at most 1."])),
    N.para(N.rich([("leftmost = min(char_map.values())", {"code": True}), " — Find the character whose last occurrence is furthest left. O(k) = O(1) since k <= 3."])),
    N.para(N.rich([("del char_map[s[leftmost]]", {"code": True}), " — Remove that character from the map. Map size returns to 2."])),
    N.para(N.rich([("left = leftmost + 1", {"code": True}), " — Advance left to the position just past the evicted character's last occurrence."])),
    N.para(N.rich([("result = max(result, right - left + 1)", {"code": True}), " — Window is now valid. Record length if it is the best seen."])),
    N.para(N.rich([("return result", {"code": True}), " — The length of the longest substring with at most 2 distinct characters."])),
    N.divider()
]

# ── Solution 2 — Brute Force ──
SOL2_CODE = """\
def lengthOfLongestSubstringTwoDistinct_brute(s: str) -> int:
    n = len(s)
    result = 0
    for i in range(n):             # try every start index
        distinct = set()
        for j in range(i, n):      # extend right from i
            distinct.add(s[j])
            if len(distinct) > 2:  # 3rd distinct char — invalid
                break
            result = max(result, j - i + 1)
    return result
"""

blocks += [
    N.h2("Solution 2 — Brute Force (All Substrings)"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Most direct approach: try every possible substring, check whether it has at most 2 distinct characters, and track the longest valid one."),
        N.h4("Why This Is Slow"),
        N.para("There are O(n^2) substrings. For each starting index i, we extend j rightward until we hit a 3rd distinct character. Total work is O(n^2) — correct but too slow for large inputs."),
        N.h4("The Key Observation"),
        N.para("The inner loop short-circuits as soon as a 3rd character appears. But in the worst case (e.g., all same character), we still do O(n^2) work. Use this approach only to verify your optimal solution on small examples."),
        N.h4("Building the Solution"),
        N.para("For each start index i: reset a set, extend j right, add s[j] to the set, break if set size exceeds 2, otherwise update result with the current length j-i+1."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), " — Try every possible start index for the substring."])),
    N.para(N.rich([("distinct = set()", {"code": True}), " — Reset distinct-character tracker for each new start position."])),
    N.para(N.rich([("distinct.add(s[j])", {"code": True}), " — Add the current character to the distinct-char set."])),
    N.para(N.rich([("if len(distinct) > 2: break", {"code": True}), " — A 3rd distinct character appeared. Any further extension is also invalid. Stop extending from this start."])),
    N.para(N.rich([("result = max(result, j - i + 1)", {"code": True}), " — Valid substring of length j-i+1; update running best."])),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all substrings)", "O(n^2)", "O(1)"],
        ["Sliding Window — last-index map (Optimal)", "O(n)", "O(1)"],
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Hash Map <= 2 Keys  (variable-size window with bounded character frequency map)"])),
    N.callout(
        "When to recognize this pattern: 'Longest substring / subarray with AT MOST K distinct / different elements.' "
        "Key signals: (1) you want the LONGEST contiguous window, "
        "(2) validity depends on a character/element frequency constraint, "
        "(3) the constraint is monotone — if [l, r] is invalid, so is [l, r+1] for any extension.",
        "🔎", "green_background"
    ),
    N.para("This problem appears verbatim as LeetCode #904 (Fruit Into Baskets) — two fruit types equals two distinct characters. Recognizing this disguise in an interview shows strong pattern fluency."),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same sliding-window-with-constraint technique:"),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), " (Medium) — sliding window where all characters must be unique; k=0 repeats allowed"])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), " (Medium) — identical problem in disguise: 2 baskets = 2 distinct fruit types"])),
    N.bullet(N.rich([("Longest Substring with At Most K Distinct Characters", {"bold": True}), " (Hard, LC #340) — direct generalization; change threshold from 2 to k"])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), " (Hard) — sliding window with 'must contain all target characters' frequency requirement"])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), " (Medium) — fixed-size sliding window with full character frequency map"])),
    N.bullet(N.rich([("Subarrays with K Different Integers", {"bold": True}), " (Hard, LC #992) — exactly K distinct = atMost(k) minus atMost(k-1)"])),
    N.para("These problems all share the core technique: a two-pointer window where a hash map enforces a character/element frequency constraint, and shrinking is triggered when the constraint is violated."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Sliding Window (Dynamic / Variable). Sub-pattern: Hash Map <= 2 Keys.", "📚", "gray_background")
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ]))
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"Total blocks appended: {len(blocks)}")
