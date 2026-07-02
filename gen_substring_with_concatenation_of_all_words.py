"""
gen_substring_with_concatenation_of_all_words.py
Rebuilds the Notion page for LeetCode #30 in-place.
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8168-9e03-d3f15705f719"

# ── Step 1: Set page properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=30,
    pattern="Sliding Window",
    subpatterns=["Multiple Starting Points + Hash"],
    tc="O(n × w)",
    sc="O(k)",
    key_insight="All words have equal length w; interleave w independent sliding windows—one per residue class mod w—each scanning word-sized chunks.",
    icon="🔴",
)
print("Properties set.")

# ── Step 2: Wipe the old body ─────────────────────────────────────────────────
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} old blocks.")

# ── Step 3: Build the new body ───────────────────────────────────────────────
blocks = []

# ─── Problem ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" and an array of strings ", {}),
        ("words", {"code": True}),
        (", where every word in ", {}),
        ("words", {"code": True}),
        (" has the same length ", {}),
        ("w", {"code": True}),
        (", return all starting indices of substrings of ", {}),
        ("s", {"code": True}),
        (" that are a concatenation of each word in ", {}),
        ("words", {"code": True}),
        (" exactly once, in any order, with no intervening characters. "
         "The result may be returned in any order.", {}),
    ])),
    N.divider(),
]

# ─── Solution 1 — Brute Force ───
BRUTE_CODE = '''\
from collections import Counter

def findSubstring(s: str, words: list[str]) -> list[int]:
    if not s or not words:
        return []
    w = len(words[0])          # each word's length
    k = len(words)             # number of words
    window = k * w             # total window length
    word_count = Counter(words) # required freq of each word
    result = []

    for i in range(len(s) - window + 1):
        # Slice k chunks of size w starting at i
        seen = Counter(
            s[i + j * w : i + (j + 1) * w]
            for j in range(k)
        )
        if seen == word_count:
            result.append(i)

    return result
'''

blocks += [
    N.h2("Solution 1 — Brute Force: Check Every Starting Index"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Any valid window has exact length k × w. So try every starting index i "
            "from 0 to len(s) − k×w. Split the window into k non-overlapping chunks "
            "of length w and count them. If the chunk multiset equals the words multiset, i is a hit."
        ),
        N.h4("What Doesn't Work Immediately"),
        N.para(
            "A character-level scan is wrong — words can contain repeated patterns. "
            "We can't check one character at a time; we must compare fixed-length slices."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Since all words have the SAME length w, every valid window can be cut into "
            "exactly k equal-sized pieces. Counter comparison of those pieces vs Counter(words) "
            "directly answers the membership question."
        ),
        N.h4("Building the Solution"),
        N.para(
            "For each i in 0…len(s)−window: extract k chunks of size w, build a Counter, "
            "compare with word_count. O(n × k) time — correct but slow."
        ),
        N.callout(
            "Analogy: Think of words as puzzle pieces. You're sliding a picture frame of "
            "fixed size across a mosaic and checking whether all pieces inside the frame "
            "exactly match your target set. Brute force resets the count from scratch each frame.",
            "🧩", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("w = len(words[0])", {"code": True}), (" — all words share one length; record it once.", {})])),
    N.para(N.rich([("k = len(words)", {"code": True}), (" — how many words must be consumed per window.", {})])),
    N.para(N.rich([("window = k * w", {"code": True}), (" — the fixed size of every candidate substring.", {})])),
    N.para(N.rich([("word_count = Counter(words)", {"code": True}), (" — required frequency of each word (handles duplicates).", {})])),
    N.para(N.rich([("for i in range(len(s) - window + 1)", {"code": True}), (" — iterate every valid starting position (can't start too close to end).", {})])),
    N.para(N.rich([("seen = Counter(s[i+j*w : i+(j+1)*w] for j in range(k))", {"code": True}), (" — extract k word-sized chunks, count them.", {})])),
    N.para(N.rich([("if seen == word_count", {"code": True}), (" — Counter equality checks both keys and values; exact multiset match.", {})])),
    N.divider(),
]

# ─── Solution 2 — Optimal (Interview Pick) ───
OPTIMAL_CODE = '''\
from collections import Counter

def findSubstring(s: str, words: list[str]) -> list[int]:
    if not s or not words:
        return []
    n, w, k = len(s), len(words[0]), len(words)
    window_len = k * w
    word_count = Counter(words)   # required word frequencies
    distinct = len(word_count)    # distinct word types to satisfy
    result = []

    for offset in range(w):       # w independent sliding windows
        left = offset
        window = {}               # current window word frequencies
        matched = 0               # how many distinct types are fully satisfied

        j = offset
        while j + w <= n:
            word = s[j : j + w]  # read next word-sized chunk
            j += w

            if word in word_count:
                window[word] = window.get(word, 0) + 1
                if window[word] == word_count[word]:
                    matched += 1
                # Over-counted: shrink from left until balanced
                while window[word] > word_count[word]:
                    left_word = s[left : left + w]
                    window[left_word] -= 1
                    if window[left_word] == word_count[left_word] - 1:
                        matched -= 1
                    left += w
            else:
                # Invalid chunk: reset window entirely
                window.clear()
                matched = 0
                left = j          # restart left past the bad chunk

            if matched == distinct:
                result.append(left)
                # Slide one word-position to allow the next match
                left_word = s[left : left + w]
                window[left_word] -= 1
                if window[left_word] < word_count[left_word]:
                    matched -= 1
                left += w

    return result
'''

blocks += [
    N.h2("Solution 2 — Optimal: w Interleaved Sliding Windows (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Brute force is O(n × k). Can we reuse computation between nearby windows? "
            "Yes — but only between windows that share word-boundary alignment. "
            "Windows starting at index i and i+w both slice at the same word boundaries. "
            "This means windows sharing offset mod w can share a sliding window structure."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A single left-to-right sliding window fails because different starting offsets "
            "(0, 1, 2, …, w−1) produce completely non-overlapping word grids. You can't "
            "share a Counter across them. You need w separate passes."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Every valid starting index i must satisfy i % w == some fixed offset. "
            "Within one offset class, as the window slides by one word (w characters), "
            "you add one word on the right and remove one word on the left — classic "
            "sliding window on a word-tokenized sequence. This drops each pass to O(n/w) "
            "word-steps, and w passes total = O(n) word-level work = O(n × w) character work."
        ),
        N.h4("Building the Solution"),
        N.para(
            "For each offset in [0, w): start left = offset, scan right j in word-steps. "
            "Maintain a window Counter and a 'matched' count of fully-satisfied distinct words. "
            "When matched == distinct, record left. Handle invalid words by resetting. "
            "When over-counted, shrink from left."
        ),
        N.callout(
            "Analogy: Imagine w parallel conveyor belts, each carrying word-sized blocks. "
            "You run one inspector per belt who slides a frame of exactly k blocks and checks "
            "the multiset. When a frame passes, slide one block forward — don't restart. "
            "This is the 'reuse' that makes it O(n) per belt.",
            "🏭", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for offset in range(w)", {"code": True}), (" — run w independent passes, one per residue class mod w.", {})])),
    N.para(N.rich([("left = offset", {"code": True}), (" — left boundary of current window; starts at the offset.", {})])),
    N.para(N.rich([("window = {}", {"code": True}), (" — tracks word frequencies in the current sliding window.", {})])),
    N.para(N.rich([("matched = 0", {"code": True}), (" — counts distinct word types whose required frequency is exactly met.", {})])),
    N.para(N.rich([("word = s[j : j + w]", {"code": True}), (" — extract next word-sized chunk from position j.", {})])),
    N.para(N.rich([("j += w", {"code": True}), (" — advance right pointer by one word-length (not one character).", {})])),
    N.para(N.rich([("if word in word_count", {"code": True}), (" — only process words that appear in the required set.", {})])),
    N.para(N.rich([("if window[word] == word_count[word]: matched += 1", {"code": True}), (" — word type exactly satisfied → increment match counter.", {})])),
    N.para(N.rich([("while window[word] > word_count[word]", {"code": True}), (" — over-counted: shrink window from left until count is back to required.", {})])),
    N.para(N.rich([("window.clear(); matched = 0; left = j", {"code": True}), (" — invalid chunk breaks word-grid alignment; reset entirely, left jumps past it.", {})])),
    N.para(N.rich([("if matched == distinct: result.append(left)", {"code": True}), (" — full match! Record left index; then evict leftmost word to search for next match.", {})])),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n × k)", "O(k)"],
        ["Optimal — w Sliding Windows (Interview Pick)", "O(n × w)", "O(k)"],
    ]),
    N.para(
        "Where n = len(s), k = len(words), w = word length. "
        "In practice w is small (typically 1–10), so O(n × w) ≈ O(n). "
        "Space O(k) is for the word_count Counter and per-offset window dict."
    ),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sliding Window", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Multiple Starting Points + Hash (w interleaved fixed-size windows with frequency map)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) The problem asks for substrings of a FIXED TOTAL LENGTH. "
        "(2) The substring must be a permutation/concatenation of a given set. "
        "(3) All 'tokens' (words) have equal size w → word-grid alignment. "
        "Signal phrase: 'concatenation of all words exactly once, in any order'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (sliding window + frequency map):"),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), (" (Medium) — fixed-size sliding window, char frequency map (#438)", {})])),
    N.bullet(N.rich([("Permutation in String", {"bold": True}), (" (Medium) — check if any permutation of p appears as substring in s (#567)", {})])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), (" (Hard) — variable-size window; must contain all chars of t (#76)", {})])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard) — fixed-size window; track max with deque (#239)", {})])),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), (" (Medium) — dynamic window with character set (#3)", {})])),
    N.bullet(N.rich([("Max Consecutive Ones III", {"bold": True}), (" (Medium) — sliding window with budget (at most k zeros flipped) (#1004)", {})])),
    N.para("These problems all share the core pattern: maintain a window of bounded content and use a hash structure to verify membership or frequency constraints in O(1) per step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Sliding Window section. Sub-Pattern: Multiple Starting Points + Hash (analysis-based classification for word-grid alignment variant).", "📚", "gray_background"),
]

# ─── Interactive Visual Explainer ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("substring_with_concatenation_of_all_words")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Step 4: Append all blocks ──────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page {PAGE_ID}.")
print("NOTION OK", PAGE_ID)
