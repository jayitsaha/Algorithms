"""
gen_max_chunks_to_make_sorted.py
Regenerates the Notion page for Max Chunks To Make Sorted (LC #769) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81d7-a26b-d1666f6ab5d5"
SLUG    = "max_chunks_to_make_sorted"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(PAGE_ID,
    difficulty="Medium",
    number=769,
    pattern="Monotonic Stack",
    subpatterns=["Track Max So Far"],
    tc="O(n)",
    sc="O(1)",
    key_insight="A chunk boundary exists at index i iff max(arr[0..i]) == i (prefix is a self-contained permutation subset).",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("arr", {"code": True}),
        (" that is a permutation of ", {}),
        ("[0, 1, ..., n - 1]", {"code": True}),
        (", we split the array into some number of chunks (i.e., partitions), and individually sort each chunk. "
         "After concatenating the sorted chunks, the result should equal the sorted array "
         "[0, 1, 2, ..., n-1]", {}),
        (". Return the largest number of chunks we can make.", {}),
    ])),
    N.para("Constraints: 1 ≤ n ≤ 10, arr is a permutation of [0..n-1]."),
    N.divider(),
]

# ── Solution 1: Track Max So Far (Interview Pick) ──────────────────────────
blocks += [
    N.h2("Solution 1 — Track Max So Far (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We're looking for the maximum number of contiguous cuts in a permutation such that each cut "
            "segment contains exactly the values that belong in those positions of the sorted output. "
            "A chunk ending at index i is valid iff the elements in arr[0..i] form the set {0,1,...,i}."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Trying every possible set of cuts is 2^n possibilities. Sorting each candidate prefix to check "
            "equality is O(n² log n). We need a constant-time boundary check."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Because arr is a permutation of {0,...,n-1}, element values equal their sorted positions. "
            "A prefix arr[0..i] is a valid chunk iff it contains exactly {0,1,...,i}. "
            "For a set of i+1 distinct non-negative integers, this is equivalent to: max(arr[0..i]) == i. "
            "The max tells us the 'furthest right destination' of any element in the prefix. "
            "If max == i, no element needs to go past position i."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Track a running max as we scan. Each time max_so_far == i, increment the chunk counter. "
            "This is greedy and optimal: taking every valid cut maximizes the count because skipping "
            "a valid boundary only merges chunks, never creates new ones."
        ),
        N.callout(
            "Analogy: Imagine sorting a shuffled deck of cards numbered 0-4. You can cut the deck anywhere "
            "as long as every card in the left pile belongs there. 'max == i' means the highest card "
            "in the pile fits exactly — so the pile is complete and self-contained.",
            "🃏", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""\
def maxChunksToSorted(arr: list[int]) -> int:
    max_so_far = 0   # running maximum of arr[0..i]
    chunks = 0       # count of valid chunk boundaries
    for i, val in enumerate(arr):
        max_so_far = max(max_so_far, val)  # update "furthest right destination"
        if max_so_far == i:                # prefix arr[0..i] = {0,1,...,i}
            chunks += 1                    # cut here — self-contained chunk
    return chunks
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("max_so_far = 0", {"code": True}), " — running maximum of elements seen so far; represents the rightmost sorted position needed by any element in the current chunk."])),
    N.para(N.rich([("chunks = 0", {"code": True}), " — accumulator for valid chunk boundaries found."])),
    N.para(N.rich([("for i, val in enumerate(arr):", {"code": True}), " — iterate with both index and value; we need ", ("i", {"code": True}), " for the boundary equality check."])),
    N.para(N.rich([("max_so_far = max(max_so_far, val)", {"code": True}), " — update running max: does ", ("val", {"code": True}), " push the 'need to reach' further right? Only if it's larger than the current max."])),
    N.para(N.rich([("if max_so_far == i:", {"code": True}), " — the key boundary condition: max == index means the prefix contains exactly {0,...,i}. This follows from the permutation property: i+1 distinct non-negatives with max == i must be exactly {0,...,i}."])),
    N.para(N.rich([("chunks += 1", {"code": True}), " — valid cut found! This chunk can be sorted independently. The elements in arr[i+1..] are completely unaffected by what happens in arr[0..i]."])),
    N.para(N.rich([("return chunks", {"code": True}), " — maximum number of sortable chunks. Always ≥ 1 since the whole array is trivially a valid single chunk."])),
    N.divider(),
]

# ── Solution 2: Brute Force ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force Sort"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Directly test every possible chunk ending point by sorting the prefix and comparing."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n² log n) — for each of n positions, we sort a prefix of up to length n. Correct but impractical for large n."),
        N.h4("The Key Observation"),
        N.para("sorted(arr[:i+1]) == list(range(i+1)) is the direct definition of a valid chunk. Use this as a stepping stone before optimizing to max tracking."),
        N.h4("Building the Solution"),
        N.para("For each index i from 0 to n-1, sort arr[0..i] and compare to [0,1,...,i]. If equal, increment chunks."),
    ]),
    N.h3("Code"),
    N.code("""\
def maxChunksToSorted_brute(arr: list[int]) -> int:
    chunks = 0
    for i in range(len(arr)):
        # Sort the prefix and check if it equals [0, 1, ..., i]
        if sorted(arr[:i + 1]) == list(range(i + 1)):
            chunks += 1
    return chunks
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("sorted(arr[:i+1])", {"code": True}), " — sort the prefix of length i+1. This is O((i+1) log(i+1)) per step."])),
    N.para(N.rich([("list(range(i+1))", {"code": True}), " — generates [0, 1, ..., i], the expected sorted prefix. Comparison is O(i+1)."])),
    N.para("Total: O(n) steps × O(n log n) per step = O(n² log n) overall. Correct but use only for small inputs or verification."),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (sort each prefix)", "O(n² log n)", "O(n)"],
        ["Track Max So Far (optimal)", "O(n)", "O(1)"],
        ["Prefix max / Suffix min (LC #768)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Monotonic Stack (Greedy prefix boundary detection)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Track Max So Far — scan with a running maximum and fire an event when max == index"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Input is a permutation of [0..n-1] (values = sorted positions). "
        "(2) Need to cut/partition into maximum pieces where each piece is sortable in-place. "
        "(3) O(1) space desired with a single scan. "
        "(4) The 'furthest reach' of a prefix determines whether it closes.",
        "🔎", "green_background"
    ),
    N.para("Note: This specific sub-pattern (prefix max == index as chunk boundary test) is classification from analysis. The DSA Patterns Guide lists related stack/monotonic patterns but does not enumerate this exact permutation-chunk sub-pattern by name."),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Max Chunks To Make Sorted II", {"bold": True}), " (Hard) — Same problem with duplicates; use prefix_max[i] ≤ suffix_min[i+1] instead of max == i (#768)"])),
    N.bullet(N.rich([("Partition Labels", {"bold": True}), " (Medium) — Greedy: track last occurrence of each char, cut when i == last occurrence of the character — same 'running reach' pattern (#763)"])),
    N.bullet(N.rich([("Jump Game", {"bold": True}), " (Medium) — Track max reachable index; cut when current index > max_reach; same running-max-vs-index logic (#55)"])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — Monotonic stack finds left/right boundaries for each bar; boundary condition analogous to chunk cuts (#84)"])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), " (Medium) — Monotonic stack tracks valid boundaries where each element is the minimum of its chunk (#907)"])),
    N.bullet(N.rich([("Remove Duplicate Letters", {"bold": True}), " (Medium) — Greedy character selection with monotonic stack; prefix conditions gate when to pop (#316)"])),
    N.para("These problems share the core technique: a running aggregate (max, last-occurrence, reach) compared to the current index determines a valid boundary condition."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Monotonic Stack section. Sub-Pattern: Track Max So Far (analysis-based classification).", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
