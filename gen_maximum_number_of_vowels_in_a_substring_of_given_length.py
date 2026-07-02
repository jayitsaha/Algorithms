"""
Notion gen script for:
  Maximum Number of Vowels in a Substring of Given Length
  LC #1456 | Medium | Sliding Window (Fixed Size)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e5-9e4f-f5f25b2e9c52"
SLUG    = "maximum_number_of_vowels_in_a_substring_of_given_length"

# ── Step 1: Set properties ──────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1456,
    pattern="Sliding Window",
    subpatterns=["Sliding Window (Fixed Size)", "Maintain Vowel Count"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Slide a fixed k-size window: add entering char (+1 if vowel), subtract leaving char (-1 if vowel), track running max.",
    icon="🟡"
)
print("Properties set OK")

# ── Step 2: Wipe old body ───────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── Step 3: Rebuild body ────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return the maximum number of vowel letters in any substring of ", {}),
        ("s", {"code": True}),
        (" with length ", {}),
        ("k", {"code": True}),
        (". Vowel letters are ", {}),
        ("a, e, i, o, u", {"code": True}),
        (".", {}),
    ])),
    N.para("Example: s = \"abciiidef\", k = 3 → 3 (the substring \"iii\" has 3 vowels)."),
    N.divider(),
]

# ── Solution 1: Sliding Window (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Sliding Window / Fixed Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the maximum number of vowels across all contiguous substrings of length exactly k. There are n-k+1 such windows. Naively we'd scan each one — O(k) per window — but that's O(n·k) total which is too slow."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each starting index i, count vowels in s[i..i+k-1]. This is O(n·k). For n = 10^5 and k = 10^4, that is 10^9 operations — TLE. We need to avoid re-scanning shared characters."),
        N.h4("The Key Observation"),
        N.para("When we slide the window one step right, the new window overlaps with the old window in k-1 positions. Those k-1 characters we already counted. Only ONE character leaves (s[i-k]) and ONE enters (s[i]). So the vowel count changes by at most 1 in either direction — we never need to re-scan."),
        N.h4("Building the Solution"),
        N.para("1. Count vowels in the first window s[0..k-1] — this is O(k) once. 2. For each subsequent window, update: if the entering char is a vowel, increment count; if the leaving char was a vowel, decrement count. 3. Track the running maximum. 4. Early exit if count reaches k (all-vowel window — provably optimal)."),
        N.callout("Analogy: Think of a train car of k seats. At each station, one passenger exits and one boards. You don't re-count everyone — you just adjust by ±1.", "🚂", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def maxVowels(s: str, k: int) -> int:\n"
        "    VOWELS = set('aeiou')                 # O(1) membership test\n"
        "    count = sum(c in VOWELS               # Count vowels in first window\n"
        "                for c in s[:k])\n"
        "    max_count = count                     # Best so far\n"
        "    for i in range(k, len(s)):            # i = entering index\n"
        "        count += (s[i] in VOWELS)         # Entering char: +1 if vowel\n"
        "        count -= (s[i-k] in VOWELS)       # Leaving char: -1 if was vowel\n"
        "        max_count = max(max_count, count) # Update running max\n"
        "        if max_count == k: return k        # Early exit: can't do better\n"
        "    return max_count"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("VOWELS = set('aeiou')", {"code": True}), (" — Creates a set for O(1) membership. Faster than 'c in \"aeiou\"' which is O(5) string scan every call.", {})])),
    N.para(N.rich([("count = sum(c in VOWELS for c in s[:k])", {"code": True}), (" — Counts vowels in the initial window s[0..k-1] using a generator expression. True counts as 1, False as 0.", {})])),
    N.para(N.rich([("max_count = count", {"code": True}), (" — Seeds the running best with the first window's count.", {})])),
    N.para(N.rich([("for i in range(k, len(s)):", {"code": True}), (" — i is the index of the character entering the right edge. Runs n-k times.", {})])),
    N.para(N.rich([("count += (s[i] in VOWELS)", {"code": True}), (" — Add 1 if entering char is a vowel, 0 otherwise. Python bool-as-int.", {})])),
    N.para(N.rich([("count -= (s[i-k] in VOWELS)", {"code": True}), (" — Subtract 1 if the leaving char (at index i-k, just exited the window) was a vowel.", {})])),
    N.para(N.rich([("max_count = max(max_count, count)", {"code": True}), (" — Keep track of the highest vowel count seen.", {})])),
    N.para(N.rich([("if max_count == k: return k", {"code": True}), (" — If the entire window is vowels, that's the theoretical max for a k-size window. Return immediately.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force (O(n·k), for contrast)"),
    N.toggle_h3("💡 Intuition: Simplest Correct Approach", [
        N.h4("Reframe the Problem"),
        N.para("Directly examine every possible k-length window starting at each index."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n·k) — correct but too slow for large inputs. For n = 10^5 and k = 10^4, it's 10^9 operations."),
        N.h4("The Key Observation"),
        N.para("Use this as a baseline in interviews — propose it first, then optimize to the sliding window."),
        N.h4("Building the Solution"),
        N.para("Iterate all starting positions, count vowels in each window via a nested loop or generator, track maximum."),
    ]),
    N.h3("Code"),
    N.code(
        "def maxVowels_brute(s: str, k: int) -> int:\n"
        "    VOWELS = set('aeiou')\n"
        "    best = 0\n"
        "    for i in range(len(s) - k + 1):              # O(n) windows\n"
        "        cnt = sum(c in VOWELS for c in s[i:i+k]) # O(k) each\n"
        "        best = max(best, cnt)\n"
        "    return best  # Total: O(n*k)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(s) - k + 1)", {"code": True}), (" — Iterates n-k+1 starting positions (all valid k-length windows).", {})])),
    N.para(N.rich([("cnt = sum(c in VOWELS for c in s[i:i+k])", {"code": True}), (" — Counts vowels in window s[i..i+k-1]. This is O(k) work per window — the expensive re-scan.", {})])),
    N.para(N.rich([("best = max(best, cnt)", {"code": True}), (" — Track highest count seen across all windows.", {})])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n·k)", "O(k)"],
        ["Sliding Window (Optimal)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sliding Window", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sliding Window (Fixed Size), Maintain Vowel Count", {})])),
    N.callout(
        "When to recognize this pattern: The problem asks for a property (max/min/count/sum) of a contiguous subarray or substring of FIXED length k. The aggregate can be updated incrementally (add one element, remove one) — making re-computation unnecessary.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Fixed-Size Sliding Window technique:"),
    N.bullet(N.rich([("Maximum Average Subarray I", {"bold": True}), (" (Easy) — Max average of k-length window; identical structure with sum (#643)", {})])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), (" (Medium) — Fixed window + frequency map, slide and compare (#438)", {})])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard) — Fixed window max using a monotonic deque (#239)", {})])),
    N.bullet(N.rich([("Grumpy Bookstore Owner", {"bold": True}), (" (Medium) — Fixed window to find the best 'bonus' contiguous interval (#1052)", {})])),
    N.bullet(N.rich([("Number of Sub-arrays of Size K and Average >= Threshold", {"bold": True}), (" (Medium) — Count fixed windows satisfying a condition (#1343)", {})])),
    N.bullet(N.rich([("Substrings of Size Three with Distinct Characters", {"bold": True}), (" (Easy) — Fixed k=3 window, check all-distinct condition (#1876)", {})])),
    N.para("These problems share the same core technique: build first window in O(k), then slide in O(1) per step, maintaining an invariant about the window's content."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.4 — Sliding Window (Fixed Size)", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
