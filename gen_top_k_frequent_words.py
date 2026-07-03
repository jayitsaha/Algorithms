"""
gen_top_k_frequent_words.py — Notion in-place update for Top K Frequent Words (#692)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-817e-b82f-ed9f0623749a"

# ── 1. Set page properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=692,
    pattern="Sorting",
    subpatterns=["Bucket by Frequency"],
    tc="O(n + m log m)",
    sc="O(n)",
    key_insight="Group words into frequency buckets; sweep high-to-low; sort each bucket alphabetically for tie-breaking.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3. Rebuild body ─────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of strings ", {}),
        ("words", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return the ", {}),
        ("k", {"code": True}),
        (" most frequent words. The answer should be sorted by frequency from highest to lowest. "
         "Words with the same frequency should be sorted alphabetically.", {})
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ('words = ["i","love","leetcode","i","love","coding"], k = 2 → ["i","love"]', {"code": True})
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ('words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4 → ["the","is","sunny","day"]', {"code": True})
    ])),
    N.divider()
]

# ── Solution 1: Bucket Sort ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bucket Sort by Frequency (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the top k words by how often they appear — with alphabetical tie-breaking. "
               "This is really two sub-problems: (1) count each word's frequency, and (2) select/order "
               "the top k. The insight is that these two concerns can be separated cleanly."),
        N.h4("What Doesn't Work"),
        N.para("Sorting all input words directly is O(n log n) — but we're sorting n words including "
               "duplicates. We should only sort among m distinct words. Even better: we shouldn't "
               "compare words across different frequencies at all — a word appearing 3 times "
               "unconditionally beats one appearing 2 times. Comparing them wastes work."),
        N.h4("The Key Observation"),
        N.para("Bucket sort separates words by frequency structurally. Words in bucket[f] appear "
               "exactly f times. Sweeping from the highest bucket to the lowest gives frequency order "
               "for free — no comparison needed. Within a bucket, a simple alphabetical sort handles "
               "ties. Two orthogonal ordering criteria, handled independently."),
        N.h4("Building the Solution"),
        N.para("Step 1: count frequencies with a hash map — O(n). "
               "Step 2: create n+1 buckets (index = frequency, max is n). Place each distinct word in its bucket — O(m). "
               "Step 3: sweep from bucket[n] down to bucket[1]. For each non-empty bucket, sort alphabetically and harvest words. "
               "Stop when len(result) == k. Early exit makes this very fast when k is small."),
        N.callout(
            "Analogy: Imagine sorting students by grade (A/B/C/D) then alphabetically within each grade. "
            "Instead of one giant sort, you group by grade first (buckets), then sort names within each group. "
            "Much faster when grade buckets are small.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(
        "def topKFrequent(words, k):\n"
        "    freq = {}\n"
        "    for w in words:\n"
        "        freq[w] = freq.get(w, 0) + 1\n"
        "    n = len(words)\n"
        "    buckets = [[] for _ in range(n + 1)]  # index = frequency\n"
        "    for word, count in freq.items():\n"
        "        buckets[count].append(word)\n"
        "    result = []\n"
        "    for i in range(n, 0, -1):              # highest freq first\n"
        "        for word in sorted(buckets[i]):    # alphabetical within bucket\n"
        "            result.append(word)\n"
        "            if len(result) == k:\n"
        "                return result\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("freq = {}", {"code": True}), (" — Initialize empty hash map to count word occurrences.", {})])),
    N.para(N.rich([("for w in words:", {"code": True}), (" — Iterate over every word in the input (including duplicates).", {})])),
    N.para(N.rich([("freq[w] = freq.get(w, 0) + 1", {"code": True}), (" — Increment count; ", {}), ("get(w, 0)", {"code": True}), (" returns 0 for unseen words so we don't KeyError.", {})])),
    N.para(N.rich([("n = len(words)", {"code": True}), (" — We need n to size the bucket array. Max frequency = n.", {})])),
    N.para(N.rich([("buckets = [[] for _ in range(n + 1)]", {"code": True}), (" — Create n+1 empty lists. Index i will hold all words appearing exactly i times. Index 0 is always empty.", {})])),
    N.para(N.rich([("for word, count in freq.items():", {"code": True}), (" — Iterate over each distinct word and its frequency.", {})])),
    N.para(N.rich([("buckets[count].append(word)", {"code": True}), (" — Place the word in its frequency slot.", {})])),
    N.para(N.rich([("for i in range(n, 0, -1):", {"code": True}), (" — Sweep from highest frequency down to 1. This ensures we collect more-frequent words before less-frequent ones.", {})])),
    N.para(N.rich([("for word in sorted(buckets[i]):", {"code": True}), (" — Sort the bucket alphabetically. All words here share frequency i, so alphabetical ordering resolves ties correctly.", {})])),
    N.para(N.rich([("result.append(word)", {"code": True}), (" — Add the current word to the result.", {})])),
    N.para(N.rich([("if len(result) == k: return result", {"code": True}), (" — Early exit: as soon as we have k words, stop. No need to look at remaining buckets.", {})])),
    N.divider()
]

# ── Solution 2: Custom Sort Key ──────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Custom Sort Key (Simplest, O(n + m log m))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of building buckets, we can express the desired ordering as a sort key. "
               "Python's sort is stable and compares tuples lexicographically — we can encode "
               "both criteria in one key function."),
        N.h4("The Key Observation"),
        N.para("The tuple (-freq[w], w) encodes everything: negative frequency means higher frequency "
               "sorts first (since -3 < -2); the word string itself breaks ties alphabetically. "
               "Python compares tuples left-to-right, so this single key handles both criteria."),
        N.h4("Building the Solution"),
        N.para("Count with Counter. Call sorted() on distinct words with the compound key. "
               "Slice the first k results. Three lines of code, completely correct."),
        N.callout("This is the cleanest interview answer to write first. Then offer to optimize "
                  "to bucket sort if asked about reducing unnecessary comparisons.", "💡", "green_background")
    ]),
    N.h3("Code"),
    N.code(
        "from collections import Counter\n"
        "\n"
        "def topKFrequent(words, k):\n"
        "    freq = Counter(words)\n"
        "    return sorted(\n"
        "        freq.keys(),\n"
        "        key=lambda w: (-freq[w], w)\n"
        "    )[:k]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("freq = Counter(words)", {"code": True}), (" — Pythonic O(n) counting. Counter is a dict subclass that handles unseen-key defaulting automatically.", {})])),
    N.para(N.rich([("sorted(freq.keys(), key=lambda w: (-freq[w], w))", {"code": True}), (" — Sort only the m distinct words (not all n input words). The key tuple ", {}), ("(-freq[w], w)", {"code": True}), (" puts higher frequency first (negated), then alphabetical within the same frequency.", {})])),
    N.para(N.rich([("[:k]", {"code": True}), (" — Slice the first k words from the sorted list. These are guaranteed to be the k most frequent, ties broken alphabetically.", {})])),
    N.divider()
]

# ── Solution 3: Min-Heap ──────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Min-Heap of Size k (O(n + m log k), best for streaming)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If k is very small (say k=3 out of 50,000 distinct words), sorting all distinct "
               "words is wasteful. A heap lets us maintain only the top k candidates at all times."),
        N.h4("The Key Observation"),
        N.para("Use a max-heap indexed by (-frequency, word). Python's heapq is a min-heap, "
               "but negating frequency turns it into an effective max-heap. The natural string "
               "comparison on word provides alphabetical ordering for ties — no custom comparator needed."),
        N.h4("When to Use"),
        N.para("When k ≪ m (k much smaller than distinct words), heapify is O(m) and popping k times "
               "is O(k log m). Total: O(n + m + k log m). For streaming scenarios where words arrive "
               "incrementally, a heap can be maintained dynamically.")
    ]),
    N.h3("Code"),
    N.code(
        "import heapq\n"
        "from collections import Counter\n"
        "\n"
        "def topKFrequent(words, k):\n"
        "    freq = Counter(words)\n"
        "    heap = [(-cnt, word) for word, cnt in freq.items()]\n"
        "    heapq.heapify(heap)\n"
        "    return [heapq.heappop(heap)[1] for _ in range(k)]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = [(-cnt, word) ...]", {"code": True}), (" — Build list of tuples: negate count so min-heap ordering gives max-frequency first. String comparison gives alphabetical tie-break.", {})])),
    N.para(N.rich([("heapq.heapify(heap)", {"code": True}), (" — Convert list to a valid heap in O(m) — much faster than O(m log m) sort.", {})])),
    N.para(N.rich([("heapq.heappop(heap)[1] for _ in range(k)", {"code": True}), (" — Pop k times. Each pop takes O(log m) and returns the minimum tuple (= maximum frequency). Take index [1] (the word).", {})])),
    N.divider()
]

# ── Complexity table ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Sort all words directly", "O(n log n)", "O(n)"],
        ["Custom sort key (Solution 2)", "O(n + m log m)", "O(m)"],
        ["Bucket Sort (Solution 1) ✓", "O(n + m log m)", "O(n)"],
        ["Min-Heap size k (Solution 3)", "O(n + m + k log m)", "O(m)"],
    ]),
    N.para(N.rich([
        ("n = total words, m = distinct words (m ≤ n). Bucket sort and custom sort key share the same asymptotic complexity; bucket sort wins in practice by avoiding cross-frequency comparisons.", {"italic": True, "color": "gray"})
    ])),
    N.divider()
]

# ── Pattern classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sorting", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Bucket by Frequency", {})])),
    N.callout(
        "When to recognize this pattern: The problem asks for 'top K by frequency' with a secondary "
        "ordering for ties. Frequency values bounded by n → use n+1 buckets. If you need K items "
        "from N and K ≪ N, consider a heap instead of sorting everything.",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Bucket by Frequency):"),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), (" (Medium) — same pattern with numbers; no alphabetical tie-break needed (#347)", {})])),
    N.bullet(N.rich([("Sort Characters By Frequency", {"bold": True}), (" (Medium) — sort all characters in a string by descending frequency using buckets (#451)", {})])),
    N.bullet(N.rich([("Maximum Frequency Stack", {"bold": True}), (" (Hard) — dynamic frequency buckets with push/pop by max frequency; same bucket structure (#895)", {})])),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium) — top-K selection on raw values; quickselect gives O(n) average (#215)", {})])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), (" (Easy) — streaming top-K; maintain a min-heap of fixed size k (#703)", {})])),
    N.bullet(N.rich([("Find K Closest Elements", {"bold": True}), (" (Medium) — top-K selection with custom distance metric; binary search + sliding window (#658)", {})])),
    N.para("These problems share the same core technique: count a frequency-like metric, then select top k using either a sorted structure, a heap, or bucket sort."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Sorting section → Bucket by Frequency", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("top_k_frequent_words")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
