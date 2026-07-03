"""
gen_top_k_frequent_elements.py — Notion update for #347 Top K Frequent Elements
Run from the Algorithms directory alongside notion_lib.py.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-817f-9048-ed004818f005"

# ── 1. Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=347,
    pattern="Heaps",
    subpatterns=["Top K", "Bucket Sort"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Frequency is bounded 1–n; place elements in freq-indexed buckets and scan right-to-left for top k in O(n).",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ───────────────────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body ──────────────────────────────────────────────────────────────
blocks = []

# ─── Problem ───────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return the ", {}),
        ("k", {"code": True}),
        (" most frequent elements. You may return the answer in any order.\n\n"
         "Example 1: nums = [1,1,1,2,2,3], k = 2  →  [1, 2]\n"
         "Example 2: nums = [1], k = 1  →  [1]\n\n"
         "Constraints: 1 ≤ nums.length ≤ 10^5, k is valid, answer is unique.", {})
    ])),
    N.divider(),
]

# ─── Solution 1 — Bucket Sort (Optimal, O(n)) ─────────────────────────────────
sol1_code = """\
def topKFrequent(nums, k):
    count = {}
    for n in nums:
        count[n] = count.get(n, 0) + 1
    freq = [[] for _ in range(len(nums) + 1)]
    for n, c in count.items():
        freq[c].append(n)
    res = []
    for i in range(len(freq) - 1, 0, -1):
        for n in freq[i]:
            res.append(n)
            if len(res) == k:
                return res"""

blocks += [
    N.h2("Solution 1 — Bucket Sort (Interview Pick, O(n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to rank elements by how often they appear, then return the top k. This is a sorting-by-frequency problem — but we don't necessarily need comparison-based sorting."),
        N.h4("What Doesn't Work"),
        N.para("Naive: sort all elements by frequency descending, return first k. That costs O(n log n). A min-heap of size k cuts it to O(n log k). But we can do better if we notice a special property of frequencies."),
        N.h4("The Key Observation"),
        N.para("Frequencies are bounded integers in the range [1, n]. Whenever keys are bounded integers, bucket sort runs in O(n) — no comparisons needed. We can use the frequency value itself as the array index."),
        N.h4("Building the Solution"),
        N.para("1. Count frequencies with a hash map in O(n).\n"
               "2. Create n+1 empty lists (buckets). bucket[f] will hold all elements with exactly frequency f.\n"
               "3. Place each element into its frequency's bucket in O(n).\n"
               "4. Scan buckets from index n down to 1 (high frequency first), collecting elements until we have k. Return early."),
        N.callout("Analogy: Imagine sorting exam scores where all scores are whole numbers 0–100. "
                  "Instead of comparison sort, you create 101 bins, drop each paper in its bin, "
                  "and read from bin 100 downward. That is bucket sort — and it is O(n) when scores are bounded. "
                  "Here, 'scores' are frequencies, bounded by n.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("count = {}", {"code": True}), " — Initialize an empty hash map to store element frequencies."])),
    N.para(N.rich([("for n in nums: count[n] = count.get(n, 0) + 1", {"code": True}), " — Pass 1: for each element, increment its count. get(n, 0) defaults to 0 if unseen."])),
    N.para(N.rich([("freq = [[] for _ in range(len(nums) + 1)]", {"code": True}), " — Create n+1 empty lists. Index i will hold elements with frequency i. n+1 because max frequency is n."])),
    N.para(N.rich([("for n, c in count.items(): freq[c].append(n)", {"code": True}), " — Pass 2: for each (element, count) pair, place the element in the bucket at index count."])),
    N.para(N.rich([("for i in range(len(freq) - 1, 0, -1):", {"code": True}), " — Scan buckets from highest index (highest frequency) down to index 1 (skip 0, always empty)."])),
    N.para(N.rich([("res.append(n)", {"code": True}), " — Add this element to the result list."])),
    N.para(N.rich([("if len(res) == k: return res", {"code": True}), " — Early exit as soon as we have collected k elements. No need to continue scanning lower buckets."])),
    N.divider(),
]

# ─── Solution 2 — Min-Heap (O(n log k)) ───────────────────────────────────────
sol2_code = """\
import heapq

def topKFrequent(nums, k):
    count = {}
    for n in nums:
        count[n] = count.get(n, 0) + 1
    # nlargest keeps a min-heap of size k internally
    return heapq.nlargest(k, count.keys(), key=count.get)"""

blocks += [
    N.h2("Solution 2 — Min-Heap / heapq.nlargest (O(n log k))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("After counting frequencies, we need to find the k elements with the highest counts. This is exactly what a 'find top k' operation does — and heaps are optimized for exactly this."),
        N.h4("What Doesn't Work"),
        N.para("Sorting all elements by count is O(n log n). If k is much smaller than n (e.g., k=3 out of n=100,000), that's wasteful — we don't need a full sort."),
        N.h4("The Key Observation"),
        N.para("We only need the top k, not all n elements ranked. A min-heap of size k can process all n elements in O(n log k): push each element, and if the heap exceeds k, pop the minimum. The k survivors are the top k."),
        N.h4("Building the Solution"),
        N.para("Python's heapq.nlargest(k, iterable, key) does exactly this — it internally uses a min-heap of size k. We pass the elements (the dictionary keys) and a key function that returns each element's frequency."),
        N.callout("heapq.nlargest(k, count.keys(), key=count.get) is idiomatic Python and handles all edge cases. "
                  "count.get is passed as the key function — it returns count[n] for each n in count.keys().", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("count = {}; for n in nums: count[n] = count.get(n, 0) + 1", {"code": True}), " — Same frequency counting as Solution 1."])),
    N.para(N.rich([("heapq.nlargest(k, count.keys(), key=count.get)", {"code": True}), " — Find k keys with the largest values under key function count.get. Internally uses a min-heap of size k. Returns a list."])),
    N.divider(),
]

# ─── Solution 3 — Sort (O(n log n)) ───────────────────────────────────────────
sol3_code = """\
from collections import Counter

def topKFrequent(nums, k):
    # Counter builds the freq map; most_common(k) returns top-k (element, count) pairs
    return [x for x, _ in Counter(nums).most_common(k)]"""

blocks += [
    N.h2("Solution 3 — Sort via Counter.most_common (O(n log n), simplest)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Python's Counter class already handles frequency counting and has a most_common() method that returns elements sorted by frequency."),
        N.h4("Building the Solution"),
        N.para("Counter(nums) builds the frequency map. .most_common(k) returns the k (element, count) pairs in descending count order. We extract just the elements with a list comprehension."),
        N.callout("This is the interview starting point — propose it first to show you know the language, "
                  "then optimize to heap or bucket sort for the follow-up.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(sol3_code),
    N.divider(),
]

# ─── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bucket Sort (optimal)", "O(n)", "O(n)"],
        ["Min-Heap (nlargest)", "O(n log k)", "O(n)"],
        ["Sort via Counter", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Heaps"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Top K · Bucket Sort (for the O(n) variant)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Find the k most/least frequent elements'\n"
        "• 'Rank items by an integer count/score'\n"
        "• 'Top k by some metric' with streaming or bounded data\n"
        "• Frequencies are bounded integers → prefer bucket sort over heap for O(n)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Top K / Heap / Bucket Sort):"),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), " (Medium) — Quickselect or min-heap of size k to find kth order statistic (#215)"])),
    N.bullet(N.rich([("Sort Characters By Frequency", {"bold": True}), " (Medium) — Same freq map + bucket sort, rebuild sorted string (#451)"])),
    N.bullet(N.rich([("Top K Frequent Words", {"bold": True}), " (Medium) — Same pattern but break ties alphabetically; heap with (−count, word) tuples (#692)"])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), " (Easy) — Maintain min-heap of size k; root is always the kth largest (#703)"])),
    N.bullet(N.rich([("K Closest Points to Origin", {"bold": True}), " (Medium) — Min-heap by Euclidean distance, nlargest pattern (#973)"])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), " (Hard) — Two heaps: max-heap for lower half, min-heap for upper half (#295)"])),
    N.para("These problems share the core technique: count/measure each element, then efficiently select the top k without fully sorting."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heaps section, Top K sub-pattern. "
              "Bucket Sort variant: Guide + Analysis (frequency-as-index technique).", "📚", "gray_background"),
]

# ─── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("top_k_frequent_elements")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Append all blocks ───────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
