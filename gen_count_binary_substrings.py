"""Notion update script for LeetCode #696 Count Binary Substrings."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8176-b8b7-d9a3f3661fb6"

# 1) Update properties
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=696,
    pattern="Two Pointers",
    subpatterns=["Group Count Comparison"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Decompose string into run-lengths; each adjacent-run boundary contributes min(prev_run, cur_run) valid substrings.",
    icon="🟢"
)
print("Properties set.")

# 2) Wipe old body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Rebuild body
blocks = []

# ── Problem statement ──
blocks.append(N.h2("Problem"))
blocks.append(N.para(
    N.rich([
        ("Given a binary string ", {}),
        ("s", {"code": True}),
        (", count the number of non-empty substrings that have equal numbers of consecutive 0s and 1s, "
         "where all 0s are grouped together and all 1s are grouped together. "
         "The 0s and 1s must appear in adjacent consecutive blocks — "
         '"0011" and "10" qualify; "0101" does not.', {})
    ])
))
blocks.append(N.divider())

# ── Solution 1 — Group Count Two Pointers (Optimal) ──
blocks.append(N.h2("Solution 1 — Group Count Two Pointers (Interview Pick)"))
blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "Count substrings with consecutive equal-size blocks of 0s and 1s. Instead of checking every "
        "substring, think about what makes a substring valid: it must straddle exactly one boundary "
        "between two adjacent same-character runs."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Brute force: for each pair (i, j) check if s[i:j] is valid. This is O(n²) or O(n³) because "
        "verifying 'consecutive equal groups' for each substring requires scanning it. Too slow for "
        "large inputs."
    ),
    N.h4("The Key Observation"),
    N.para(
        "Every valid substring straddles exactly one boundary between two adjacent runs. "
        "At a boundary between a run of length prev and a run of length cur, there are exactly "
        "min(prev, cur) valid substrings (lengths 2, 4, 6, ... up to 2×min(prev,cur)). "
        "Sum min(prev, cur) over all boundaries to get the answer."
    ),
    N.h4("Building the Solution"),
    N.para(
        "Track prev (length of the previous run) and cur (length of the current run). Scan character "
        "by character. When s[i] == s[i-1], extend cur. When they differ, add min(prev, cur) to the "
        "answer, then set prev=cur and reset cur=1. After the loop, add min(prev, cur) one final time "
        "for the last boundary."
    ),
    N.callout(
        "Analogy: Imagine you are laying tiles in two colors alternately (blue and red). "
        "At each color boundary, you can fit min(left_pile, right_pile) nested tile pairs side-by-side. "
        "Each pair is a valid substring.",
        "🧠",
        "blue_background"
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "def countBinarySubstrings(s: str) -> int:\n"
    "    prev, cur, count = 0, 1, 0\n"
    "    for i in range(1, len(s)):\n"
    "        if s[i] == s[i - 1]:\n"
    "            cur += 1\n"
    "        else:\n"
    "            count += min(prev, cur)\n"
    "            prev = cur\n"
    "            cur = 1\n"
    "    count += min(prev, cur)\n"
    "    return count\n"
))

blocks.append(N.h3("Line by Line"))
lines = [
    ("prev, cur, count = 0, 1, 0",
     "prev=0 (no previous run yet), cur=1 (first character starts the first run), count=0 (no valid substrings found)."),
    ("for i in range(1, len(s)):",
     "Scan from index 1 onward, comparing each character to the one before it."),
    ("if s[i] == s[i - 1]:",
     "Same character as predecessor — we are continuing the current run."),
    ("cur += 1",
     "Extend the current run length."),
    ("else:",
     "Character changed — we hit a run boundary!"),
    ("count += min(prev, cur)",
     "Valid substrings at this boundary = min(prev, cur). Add to answer."),
    ("prev = cur",
     "The run that just ended becomes the new 'previous' run."),
    ("cur = 1",
     "Start counting the new run (we have already seen 1 character of it)."),
    ("count += min(prev, cur)",
     "After the loop, handle the final boundary (last two runs never triggered the else branch)."),
    ("return count",
     "Return the total count of valid substrings."),
]
for line_code, explanation in lines:
    blocks.append(N.para(N.rich([
        (line_code, {"code": True}),
        (" — " + explanation, {})
    ])))
blocks.append(N.divider())

# ── Solution 2 — Run-Length Array ──
blocks.append(N.h2("Solution 2 — Run-Length Array (Clearer Conceptually)"))
blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "Build an explicit list of run lengths, then sum min(adjacent pairs). This makes the "
        "key insight visible in the data structure itself."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Using O(n) space is not ideal for production, but this solution is excellent for understanding "
        "the algorithm before optimizing space."
    ),
    N.h4("The Key Observation"),
    N.para(
        "groups = run-length-encoded s. For '00110011', groups = [2, 2, 2, 2]. "
        "Answer = sum(min(groups[i], groups[i+1]) for i in range(len(groups)-1))."
    ),
    N.h4("Building the Solution"),
    N.para(
        "Scan to build groups array. Then zip(groups, groups[1:]) pairs adjacent runs, and sum min of each pair."
    ),
]))
blocks.append(N.h3("Code"))
blocks.append(N.code(
    "def countBinarySubstrings(s: str) -> int:\n"
    "    groups, cur_len = [], 1\n"
    "    for i in range(1, len(s)):\n"
    "        if s[i] == s[i - 1]:\n"
    "            cur_len += 1\n"
    "        else:\n"
    "            groups.append(cur_len)\n"
    "            cur_len = 1\n"
    "    groups.append(cur_len)  # final run\n"
    "    return sum(min(a, b) for a, b in zip(groups, groups[1:]))\n"
))
blocks.append(N.divider())

# ── Complexity ──
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution", "Time", "Space"],
    ["Group Count Two Pointers (Solution 1)", "O(n)", "O(1)"],
    ["Run-Length Array (Solution 2)", "O(n)", "O(n)"],
    ["Brute Force", "O(n² – n³)", "O(1)"],
]))
blocks.append(N.divider())

# ── Pattern Classification ──
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers", {})])))
blocks.append(N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Group Count Comparison", {})])))
blocks.append(N.callout(
    "When to recognize this pattern: The problem asks you to count substrings with equal adjacent "
    "consecutive blocks. Decompose the string into run-lengths; at each boundary between adjacent "
    "runs, contribute min(prev_run, cur_run) to the answer. O(n) time, O(1) space.",
    "🔎",
    "green_background"
))
blocks.append(N.divider())

# ── Related Problems ──
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same or closely related technique:"))
related = [
    ("String Compression", "Medium", "Run-length scanning to compress consecutive character blocks (#443)"),
    ("Count and Say", "Medium", "Describe run-lengths in English; same boundary-scanning logic (#38)"),
    ("Max Consecutive Ones III", "Medium", "Extend runs by flipping at most k zeros; sliding window on runs (#1004)"),
    ("Longest Turbulent Subarray", "Medium", "Track alternating runs with prev/cur pointers (#978)"),
    ("Number of Zero-Filled Subarrays", "Medium", "Each run of k zeros contributes k*(k+1)/2 subarrays (#2348)"),
    ("Remove Duplicates from Sorted Array", "Easy", "In-place run de-duplication using a write pointer (#26)"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) — {note}", {})
    ])))
blocks.append(N.divider())

# ── Embed ──
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for("count_binary_substrings")))
blocks.append(N.para(N.rich([(
    "Step through the algorithm visually — use Next/Prev or arrow keys.",
    {"italic": True, "color": "gray"}
)])))

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
