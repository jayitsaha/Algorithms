"""gen_sort_characters_by_frequency.py — Notion update for LC #451."""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-813a-96c0-f9c2c71fb8f3"
SLUG = "sort_characters_by_frequency"

# ── 1) Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=451,
    pattern="Sorting",
    subpatterns=["Frequency Buckets"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Count frequencies, place chars in bucket[freq], scan buckets n→1 writing char*i — O(n) bucket sort beats O(n log n) comparison sort because frequencies are bounded by n.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (", sort it in decreasing order based on the frequency of the characters "
         "and return the sorted string. If there are multiple answers, return any of them.", {}),
    ])),
    N.para("Example 1: s = \"tree\" → \"eert\" (e appears 2 times, t and r appear 1 time each)."),
    N.para("Example 2: s = \"cccaaa\" → \"cccaaa\" or \"aaaccc\" (both valid — tie between c and a)."),
    N.para("Example 3: s = \"Aabb\" → \"bbAa\" or \"bbaA\" ('A' and 'a' are distinct characters)."),
    N.divider(),
]

# ── Solution 1: Bucket Sort (Optimal) ──
sol1_code = """\
def frequencySort(s: str) -> str:
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    buckets = [[] for _ in range(len(s) + 1)]
    for char, count in freq.items():
        buckets[count].append(char)
    result = []
    for i in range(len(s), 0, -1):
        for char in buckets[i]:
            result.append(char * i)
    return ''.join(result)"""

blocks += [
    N.h2("Solution 1 — Bucket Sort (Interview Pick, O(n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to reorder characters so that more-frequent characters appear first. "
               "This is a sorting problem where the sort key is frequency — not the character itself."),
        N.h4("What Doesn't Work"),
        N.para("Sorting characters directly (sorted(s)) orders alphabetically, not by frequency. "
               "Even sorting by a frequency key (Counter + sort) is O(n log n) — "
               "it doesn't leverage the fact that frequencies are bounded integers."),
        N.h4("The Key Observation"),
        N.para("Character frequencies are integers in the range [0, n] where n = len(s). "
               "A character can appear at most n times. This bounded integer range is the "
               "classic signal for BUCKET SORT — we can skip comparisons entirely by "
               "placing each character directly in bucket[freq[char]]."),
        N.h4("Building the Solution"),
        N.para("Step 1: Count frequencies in one pass → O(n). "
               "Step 2: Create buckets[0..n]. Put each char c in buckets[freq[c]] → O(n). "
               "Step 3: Scan buckets from index n down to 1. For each char at buckets[i], "
               "append char * i to result → O(n) total characters written. "
               "Step 4: Join and return → O(n)."),
        N.callout(
            "Analogy: Imagine sorting students by grade. Instead of comparing each student's "
            "grade to another (O(n log n)), just create 10 buckets (one per possible grade A–F+) "
            "and drop each student into their grade bucket. Then read the buckets from A down to F. "
            "That's bucket sort — the bounded range eliminates comparisons.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("freq = {}", {"code": True}), " — Initialize empty frequency map."])),
    N.para(N.rich([("for c in s:", {"code": True}), " — Single pass over the input string."])),
    N.para(N.rich([("freq[c] = freq.get(c, 0) + 1", {"code": True}),
                   " — Increment count; freq.get(c,0) safely defaults to 0 for first-time chars."])),
    N.para(N.rich([("buckets = [[] for _ in range(len(s) + 1)]", {"code": True}),
                   " — Create n+1 empty lists. Index i will hold all chars with frequency i."])),
    N.para(N.rich([("for char, count in freq.items():", {"code": True}),
                   " — Iterate over (character, frequency) pairs."])),
    N.para(N.rich([("buckets[count].append(char)", {"code": True}),
                   " — Place char into its frequency bucket. e.g., freq('e')=2 → buckets[2].append('e')."])),
    N.para(N.rich([("for i in range(len(s), 0, -1):", {"code": True}),
                   " — Scan from n down to 1. Start at len(s) because a char could appear n times. Stop before 0 (no char has frequency 0)."])),
    N.para(N.rich([("for char in buckets[i]:", {"code": True}),
                   " — Inner loop: for each character stored at this frequency index."])),
    N.para(N.rich([("result.append(char * i)", {"code": True}),
                   " — The key line: write char exactly i times (e.g., i=2 → 'ee'). NOT just char."])),
    N.para(N.rich([("return ''.join(result)", {"code": True}),
                   " — Concatenate all parts into the final string."])),
    N.divider(),
]

# ── Solution 2: Counter + most_common() ──
sol2_code = """\
from collections import Counter

def frequencySort(s: str) -> str:
    count = Counter(s)
    return ''.join(
        char * freq
        for char, freq in count.most_common()
    )"""

blocks += [
    N.h2("Solution 2 — Counter + most_common() (Simpler, O(n log n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Count frequencies, then sort characters by those frequencies descending, "
               "then write each character its count number of times."),
        N.h4("What Doesn't Work"),
        N.para("Sorting raw characters gives alphabetical order, not frequency order. "
               "We need to sort by the count, not the character itself."),
        N.h4("The Key Observation"),
        N.para("Python's Counter has a built-in most_common() method that returns "
               "(char, count) pairs sorted by count descending. This is exactly what we need. "
               "We just need to reconstruct: join(char * count for each pair)."),
        N.h4("Building the Solution"),
        N.para("Counter(s) builds the frequency map. most_common() sorts it. "
               "Generator expression multiplies each char by its count. join() combines. "
               "Four operations, two lines of code. The simplicity makes it interview-friendly."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("count = Counter(s)", {"code": True}),
                   " — Build frequency map using Python's built-in Counter class."])),
    N.para(N.rich([("count.most_common()", {"code": True}),
                   " — Returns list of (char, freq) tuples sorted by frequency descending. This is O(n log n) internally."])),
    N.para(N.rich([("char * freq", {"code": True}),
                   " — Python string multiplication: 'e' * 2 = 'ee'. Each char repeated freq times."])),
    N.para(N.rich([("''.join(...)", {"code": True}),
                   " — Concatenate all the repeated-char strings into one result string."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Bucket Sort (Sol 1)", "O(n)", "O(n)", "Optimal; no comparison sort needed"],
        ["Counter + most_common() (Sol 2)", "O(n log n)", "O(n)", "Simpler; relies on Python sort"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sorting"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Frequency Buckets"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks to sort/order elements by how often they appear. "
        "(2) The sorting key is a bounded integer (frequencies bounded by n). "
        "(3) Output requires grouping all copies of the same element together. "
        "These signals together = Frequency Buckets (bucket sort on counts).",
        "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Frequency Buckets / Sorting technique:"),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}),
                     " (Medium) — Bucket sort on integer frequencies to find k most common in O(n). #347")])),
    N.bullet(N.rich([("Top K Frequent Words", {"bold": True}),
                     " (Medium) — Frequency + lexicographic tie-breaking; same bucket intuition. #692")])),
    N.bullet(N.rich([("Reorganize String", {"bold": True}),
                     " (Medium) — Frequency-based greedy character placement using bucket counts. #767")])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}),
                     " (Medium) — Frequency-driven scheduling; max-frequency char determines minimum time. #621")])),
    N.bullet(N.rich([("Minimum Deletions to Make Character Frequencies Unique", {"bold": True}),
                     " (Medium) — Track and deconflict frequency values greedily. #1647")])),
    N.bullet(N.rich([("Sort Array By Parity", {"bold": True}),
                     " (Easy) — Partition array elements into two buckets by a binary property. #905")])),
    N.para("These problems share the core technique: count occurrence frequencies, "
           "leverage the bounded integer range to sort/bucket in O(n) rather than O(n log n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Sorting section, Frequency Buckets sub-pattern.",
              "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
