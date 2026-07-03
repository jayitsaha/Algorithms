"""
gen_partition_labels.py — Notion update for Partition Labels (#763)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-810a-9e68-fcc6e2c9aacd"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=763,
    pattern="Intervals",
    subpatterns=["Last Occurrence + Extend"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Precompute last occurrence of each char; extend partition boundary greedily; cut when i == end.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ─────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Rebuild body ───────────────────────────────────────────────────────
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (", partition it into as many parts as possible so that each letter appears in at most one part. Return a list of integers representing the size of these parts. The concatenation of all parts in order must equal ", {}),
        ("s", {"code": True}),
        (".", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('s = "ababcbacadefegde"', {"code": True}),
        (" → ", {}),
        ("[9, 7]", {"code": True}),
        (". Part 1 = \"ababcbaca\" (a,b,c all contained), Part 2 = \"defegde\" (d,e,f,g all contained).", {}),
    ])),
    N.divider(),
]

# Solution 1 — Optimal
sol1_code = '''def partitionLabels(s: str) -> list[int]:
    last = {c: i for i, c in enumerate(s)}  # last[c] = rightmost index of c
    result, start, end = [], 0, 0
    for i, c in enumerate(s):
        end = max(end, last[c])   # extend boundary if c appears further right
        if i == end:              # reached boundary → partition is sealed
            result.append(end - start + 1)
            start = i + 1        # next partition begins right after cut
    return result'''

blocks += [
    N.h2("Solution 1 — Last Occurrence + Greedy Extend (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to split the string into maximum pieces such that no character appears in two different pieces. This means: for any character c, ALL its occurrences must be in the same piece. The piece containing c must therefore span at least from c's first to c's last occurrence."),
        N.h4("What Doesn't Work"),
        N.para("Naively splitting at every opportunity fails: if we cut at index 2 in \"ababcba...\", 'a' appears both before and after the cut — violating the constraint. We can't know where to cut without first knowing where each character last appears."),
        N.h4("The Key Observation"),
        N.para("The last occurrence of a character is the minimum right boundary for any partition containing it. If we track the maximum of all last-occurrences for characters seen so far, that gives us the earliest safe cut point."),
        N.h4("Building the Solution"),
        N.para("Phase 1: scan once to build last[c] = rightmost index of c. Phase 2: walk left-to-right, extend end = max(end, last[c]), cut when i == end. This greedy earliest-cut maximizes the number of partitions."),
        N.callout("Analogy: Rubber Band. As you scan, stretch the rubber band rightward to last[c] for each character. When you physically arrive at the right edge, the band is sealed — cut it off.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("last = {c: i for i, c in enumerate(s)}", {"code": True}), (" — Dict comprehension iterating left-to-right. Repeated characters overwrite earlier values, so the final entry is always the last (rightmost) occurrence. At most 26 keys for lowercase English → O(1) space.", {})])),
    N.para(N.rich([("result, start, end = [], 0, 0", {"code": True}), (" — Initialize output list, start (left edge of current partition), end (minimum right boundary we must reach before cutting).", {})])),
    N.para(N.rich([("for i, c in enumerate(s):", {"code": True}), (" — Walk the string left-to-right with both index and character.", {})])),
    N.para(N.rich([("end = max(end, last[c])", {"code": True}), (" — Extend the partition boundary if character c's last occurrence is further right than our current end. This \"rubber-bands\" the window rightward.", {})])),
    N.para(N.rich([("if i == end:", {"code": True}), (" — We've arrived at the boundary. Every character seen so far in [start..end] has last[c] ≤ end, meaning none of them appear past this point. Safe to cut!", {})])),
    N.para(N.rich([("result.append(end - start + 1)", {"code": True}), (" — Record the partition size. +1 because both endpoints are inclusive.", {})])),
    N.para(N.rich([("start = i + 1", {"code": True}), (" — Start the next partition immediately after the cut point.", {})])),
    N.para(N.rich([("return result", {"code": True}), (" — List of all partition sizes.", {})])),
    N.divider(),
]

# Solution 2 — Brute Force
sol2_code = '''def partitionLabels_brute(s: str) -> list[int]:
    result, start = [], 0
    while start < len(s):
        end = start
        while end < len(s):
            # Find the furthest right any char in current window reaches
            new_end = max(s.rfind(c) for c in s[start:end+1])
            if new_end == end:
                break  # window is stable — nothing leaks right
            end = new_end
        result.append(end - start + 1)
        start = end + 1
    return result'''

blocks += [
    N.h2("Solution 2 — Brute Force: Expand Until Stable"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start with the smallest possible window and keep expanding it until it is \"closed\" — i.e., no character inside has an occurrence outside the window. Once stable, cut and restart."),
        N.h4("What Doesn't Work Well"),
        N.para("Calling rfind for every character in every window is O(n) per character per expansion step. In the worst case this is O(n²), making it impractical for large inputs."),
        N.h4("The Key Observation"),
        N.para("The window is stable when max(last[c] for c in window) == end. We keep expanding until this self-consistency condition holds."),
        N.h4("Building the Solution"),
        N.para("Outer while loop: move start rightward through completed partitions. Inner while loop: expand end until the window is closed. Record size, advance start."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("while start < len(s):", {"code": True}), (" — Process each partition from left to right.", {})])),
    N.para(N.rich([("new_end = max(s.rfind(c) for c in s[start:end+1])", {"code": True}), (" — For each character in the current window, find its last occurrence. Take the max. O(n) per call.", {})])),
    N.para(N.rich([("if new_end == end: break", {"code": True}), (" — Window is self-consistent: no character inside it appears outside. This is the cut point.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (rfind per expansion)", "O(n²)", "O(1)"],
        ["Last Occ + Greedy (Interview Pick)", "O(n)", "O(1)"],
        ["Interval Merge (equivalent view)", "O(n)", "O(k)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Intervals — problems involving ranges, spans, and merging/splitting based on boundaries.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Last Occurrence + Extend — precompute the rightmost position of each element, then greedily extend a window to that boundary and cut when reached.", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("\"Each character/element must appear in at most one group\" → need last occurrence. \"Maximum number of parts\" → greedy earliest-cut. Window that must 'swallow' future occurrences to remain valid → extend-and-cut.", {})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Last Occurrence + Extend / Interval Greedy technique:"),
    N.bullet(N.rich([("Merge Intervals", {"bold": True}), (" (Medium) — Partition Labels is equivalent to merging [first, last] intervals per character (#56)", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), (" (Medium) — Min removals to eliminate overlaps; greedy sort-by-end (#435)", {})])),
    N.bullet(N.rich([("Minimum Number of Arrows to Burst Balloons", {"bold": True}), (" (Medium) — Count non-overlapping groups greedily (#452)", {})])),
    N.bullet(N.rich([("Insert Interval", {"bold": True}), (" (Medium) — Merge new interval into sorted list (#57)", {})])),
    N.bullet(N.rich([("Remove Covered Intervals", {"bold": True}), (" (Medium) — Sort + track max end to count uncovered (#1288)", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Greedy interval scheduling with character frequencies (#621)", {})])),
    N.para("These problems share the same core technique: precompute a range boundary, walk greedily, cut/merge at the earliest valid point."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Intervals section, Sub-Pattern: Last Occurrence + Extend", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("partition_labels")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
