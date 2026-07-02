"""
gen_find_all_anagrams_in_a_string.py
Notion in-place update for LC #438 — Find All Anagrams in a String
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81ad-9c24-c4456bbabb94"
SLUG = "find_all_anagrams_in_a_string"

print("Step 1: Set properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=438,
    pattern="Sliding Window",
    subpatterns=["Frequency Count Window"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Slide a fixed-size window maintaining a 'need' counter; when need==0 all char frequencies match p.",
    icon="🟡"
)
print("Properties set.")

print("Step 2: Wipe old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

print("Step 3: Build new body...")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings ", {}),
        ("s", {"code": True}),
        (" and ", {}),
        ("p", {"code": True}),
        (", return an array of all the start indices of ", {}),
        ("p", {"code": True}),
        ("'s anagrams in ", {}),
        ("s", {"code": True}),
        (". You may return the answer in any order.", {}),
        ("\n\nExample: s = \"cbaebabacd\", p = \"abc\" → [0, 6]\n", {}),
        ("Explanation: Window at index 0 is \"cba\" (anagram of \"abc\"); window at index 6 is \"bac\" (anagram of \"abc\").", {"italic": True}),
    ])),
    N.divider(),
]

# ── Solution 1 — Optimal ──
blocks += [
    N.h2("Solution 1 — Sliding Window + Need Counter (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find every starting position i in s such that the substring s[i..i+m-1] (m = len(p)) contains the same characters with the same frequencies as p. Position within the window doesn't matter — only the multiset of characters."),
        N.h4("What Doesn't Work"),
        N.para("Checking every window from scratch costs O(m) per window — O(n·m) total. For n,m ~ 10⁴ this is 10⁸ operations: too slow. We're repeating identical work: when sliding one step, m−1 characters don't change."),
        N.h4("The Key Observation"),
        N.para("When we slide the window one step right, exactly one character enters (s[right]) and one leaves (s[left]). Instead of recomputing the full frequency count, we update it incrementally in O(1). To detect a match in O(1) — not O(26) — we track how many distinct characters are 'satisfied' (their window count equals their p count) using a 'need' counter."),
        N.h4("Building the Solution"),
        N.para("1. Build p_count once (O(m)). Set need = len(p_count). 2. Slide right: add s[right] to s_count; if that char just hit its p target, need--. 3. When window hits size m: if need==0, record left. Remove s[left]: if that char was exactly at its p target, need++. Advance left."),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}), ("Think of 'need' as a satisfaction score. Ordering pizza: you need 1 pepperoni, 1 mushroom, 1 olive. Each ingredient you get ticks off the list. Each one removed unchecks it. When all boxes are checked (need=0), the order is complete.", {})]),
            "🍕", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""def findAnagrams(s: str, p: str) -> list[int]:
    if len(p) > len(s): return []
    p_count, s_count = {}, {}
    for c in p:
        p_count[c] = p_count.get(c, 0) + 1
    need = len(p_count)          # # distinct chars not yet satisfied
    result, left = [], 0
    for right in range(len(s)):
        c = s[right]
        s_count[c] = s_count.get(c, 0) + 1
        if c in p_count and s_count[c] == p_count[c]:
            need -= 1            # just exactly satisfied this char
        if right - left + 1 == len(p):   # window is full
            if need == 0:
                result.append(left)
            lc = s[left]
            if lc in p_count and s_count[lc] == p_count[lc]:
                need += 1        # removing will break this exact match
            s_count[lc] -= 1
            left += 1
    return result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("if len(p) > len(s): return []", {"code": True}), (" — Quick fail: p can't fit in a shorter s. Zero windows possible.", {})])),
    N.para(N.rich([("p_count, s_count = {}, {}", {"code": True}), (" — Two frequency maps: p_count is the fixed target; s_count tracks the live window.", {})])),
    N.para(N.rich([("for c in p: p_count[c] = ...", {"code": True}), (" — Build p's frequency map once, O(m). We compare window frequencies against this.", {})])),
    N.para(N.rich([("need = len(p_count)", {"code": True}), (" — Number of distinct characters whose window count doesn't yet match p_count. Starts at max.", {})])),
    N.para(N.rich([("for right in range(len(s)):", {"code": True}), (" — Expand right edge across all of s, one step at a time.", {})])),
    N.para(N.rich([("s_count[c] = s_count.get(c,0) + 1", {"code": True}), (" — Increment count of the new character entering the window.", {})])),
    N.para(N.rich([("if c in p_count and s_count[c] == p_count[c]: need -= 1", {"code": True}), (" — Only decrement need when we exactly hit the target. Going below (0) or above doesn't change need at this line.", {})])),
    N.para(N.rich([("if right - left + 1 == len(p):", {"code": True}), (" — Window has reached exactly size m. Time to check and then slide.", {})])),
    N.para(N.rich([("if need == 0: result.append(left)", {"code": True}), (" — All characters are exactly satisfied → anagram! Record the starting index.", {})])),
    N.para(N.rich([("if lc in p_count and s_count[lc] == p_count[lc]: need += 1", {"code": True}), (" — Check BEFORE decrementing. If current count equals target, decrementing will break the match.", {})])),
    N.para(N.rich([("s_count[lc] -= 1; left += 1", {"code": True}), (" — Remove left character from window, slide left forward. Window is now size m−1 until next right expansion.", {})])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Counter Comparison (Cleaner, O(n·26))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same sliding window idea, but instead of tracking a 'need' counter, we maintain two full Counter objects and compare them directly at each window position."),
        N.h4("What Doesn't Work (about this approach)"),
        N.para("Comparing two Counter objects takes O(26) per window since there are at most 26 lowercase characters. This is technically O(26n) which is O(n), but the constant factor is 26× larger than Solution 1."),
        N.h4("The Key Observation"),
        N.para("Python's Counter equality (==) works correctly and handles cleanup of zero-count entries. The code is simpler to write and reason about. In interviews, mention this first, then optimize to the need-counter approach."),
        N.h4("Building the Solution"),
        N.para("Build the initial window's counter for s[:len(p)]. Compare to p's counter. Slide: add new right char, remove old left char, clean up zero entries (necessary for == to work), compare."),
    ]),
    N.h3("Code"),
    N.code("""from collections import Counter

def findAnagrams(s: str, p: str) -> list[int]:
    if len(p) > len(s): return []
    pc = Counter(p)
    wc = Counter(s[:len(p)])
    result = [0] if wc == pc else []
    for i in range(len(p), len(s)):
        wc[s[i]] += 1
        wc[s[i - len(p)]] -= 1
        if wc[s[i - len(p)]] == 0:
            del wc[s[i - len(p)]]      # keep Counter clean for == comparison
        if wc == pc:
            result.append(i - len(p) + 1)
    return result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("pc = Counter(p)", {"code": True}), (" — Build the target frequency map.", {})])),
    N.para(N.rich([("wc = Counter(s[:len(p)])", {"code": True}), (" — Build the first window's frequency map.", {})])),
    N.para(N.rich([("result = [0] if wc == pc else []", {"code": True}), (" — Check the first window immediately.", {})])),
    N.para(N.rich([("wc[s[i]] += 1; wc[s[i-len(p)]] -= 1", {"code": True}), (" — Add new char, remove departing char. O(1) each.", {})])),
    N.para(N.rich([("if wc[...] == 0: del wc[...]", {"code": True}), (" — Counter equality requires no zero-value keys (Counter({a:0}) != Counter({})).", {})])),
    N.para(N.rich([("if wc == pc: result.append(...)", {"code": True}), (" — O(26) comparison. Correct but 26× slower than need counter.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (recount each window)", "O(n·m)", "O(m)"],
        ["Sliding Window — Counter Comparison", "O(26n) = O(n)", "O(1)"],
        ["Sliding Window — Need Counter (Optimal)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sliding Window", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Frequency Count Window (fixed-size sliding window with character frequency matching)", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) Fixed-length substrings/windows of size k. (2) Need to check if window's character multiset matches a target pattern. (3) Sliding one character in / one out incrementally. (4) Keywords: 'anagram', 'permutation', 'rearrangement' in substring context.", {})
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Frequency Count Window technique:"),
    N.bullet(N.rich([("Valid Anagram", {"bold": True}), (" (Easy) — One-window version; compare full string frequencies (#242)", {})])),
    N.bullet(N.rich([("Permutation in String", {"bold": True}), (" (Medium) — Identical algorithm; return bool instead of index list (#567)", {})])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), (" (Hard) — Same need counter; variable window shrinks when need==0 (#76)", {})])),
    N.bullet(N.rich([("Group Anagrams", {"bold": True}), (" (Medium) — Bucket words by sorted key or frequency tuple; no sliding needed (#49)", {})])),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), (" (Medium) — Variable window; each char count ≤ 1 constraint (#3)", {})])),
    N.bullet(N.rich([("Longest Repeating Character Replacement", {"bold": True}), (" (Medium) — Variable window; window_size - max_freq ≤ k (#424)", {})])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), (" (Medium) — Variable window; at most 2 distinct types (#904)", {})])),
    N.para("These problems share the core technique: incrementally maintain a frequency map as the window slides, and detect a match condition in O(1) per step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.4 (Sliding Window: Fixed Size) — Sub-Pattern: Frequency Count Window", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print("Done.")
