"""
gen_string_compression.py
Regenerate Notion page for String Compression (LeetCode #443) in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-819e-a041-e4500b4d0287"

# 1) Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=443,
    pattern="Two Pointers",
    subpatterns=["Read-Write Two Pointers"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Use read and write pointers; write lags behind read since compression never expands a run.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe existing body
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# 3) Rebuild body
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a character array ", {}),
        ("chars", {"code": True}),
        (", compress it in-place using run-length encoding. Each run of consecutive identical characters is replaced by the character followed by the count (count is omitted if it equals 1, and written digit-by-digit if multi-digit). Return the new length of the array. Must use only O(1) extra space.", {})
    ])),
    N.divider()
]

# ── Solution 1: Read-Write Two Pointers (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Read-Write Two Pointers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to overwrite chars[] with a compressed version of itself. Because compression can only shrink or maintain length, we can safely write output behind the read pointer — the write head can never catch up to the read head."),
        N.h4("What Doesn't Work"),
        N.para("Building a new list and copying back uses O(n) space — that violates the constraint. We must operate directly on chars[]."),
        N.h4("The Key Observation"),
        N.para("A run of k identical characters always compresses to 1 + len(str(k)) ≤ k characters. This inequality guarantees that write ≤ read at every step, making in-place safe."),
        N.h4("Building the Solution"),
        N.para("Use three roles: (1) read pointer i scans right, (2) group_start anchor records where the current run began, (3) write pointer records where compressed output goes. Inner while loop advances i past identical chars; count = i - group_start. Write the char, then each digit of count if count > 1."),
        N.callout("Analogy: Think of a cassette editor — the read head plays forward at full speed while the write head records a shorter, compressed version behind it. They never collide because the compressed track is always shorter than the original.", "🧠", "blue_background")
    ]),
    N.h3("Code"),
    N.code("""def compress(chars):
    write = 0          # next output position
    i = 0              # read pointer
    n = len(chars)
    while i < n:
        group_start = i                          # anchor: start of this run
        while i < n and chars[i] == chars[group_start]:
            i += 1                               # advance past all identical chars
        chars[write] = chars[group_start]        # always write the character
        write += 1
        count = i - group_start
        if count > 1:
            for digit in str(count):             # each digit separately
                chars[write] = digit
                write += 1
    return write                                 # new length"""),
    N.h3("Line by Line"),
    N.para(N.rich([("write = 0", {"code": True}), (" — next slot to write compressed output; starts at front of array.", {})])),
    N.para(N.rich([("i = 0", {"code": True}), (" — read pointer that scans the entire array left to right.", {})])),
    N.para(N.rich([("n = len(chars)", {"code": True}), (" — cache original length; does not change even as we overwrite.", {})])),
    N.para(N.rich([("while i < n:", {"code": True}), (" — outer loop processes one run per iteration.", {})])),
    N.para(N.rich([("group_start = i", {"code": True}), (" — anchor: remember where this run began so count = i - group_start later.", {})])),
    N.para(N.rich([("while i < n and chars[i] == chars[group_start]: i += 1", {"code": True}), (" — inner loop advances i past all chars in the run.", {})])),
    N.para(N.rich([("chars[write] = chars[group_start]", {"code": True}), (" — write the character (always, even for single-char runs).", {})])),
    N.para(N.rich([("count = i - group_start", {"code": True}), (" — length of the run just scanned.", {})])),
    N.para(N.rich([("if count > 1:", {"code": True}), (" — only append a digit if the run length is 2 or more.", {})])),
    N.para(N.rich([("for digit in str(count): chars[write] = digit; write += 1", {"code": True}), (" — write each digit of count as a separate char element.", {})])),
    N.para(N.rich([("return write", {"code": True}), (" — write is the new length of the compressed array.", {})])),
    N.divider()
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force with Extra Space"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Build the compressed output in a separate list, then copy it back. Simpler to implement, but uses O(n) extra space."),
        N.h4("What Doesn't Work"),
        N.para("This approach violates the O(1) space constraint. It is shown here as a baseline only."),
        N.h4("The Key Observation"),
        N.para("The logic for identifying runs and formatting counts is identical to the optimal solution — only the storage mechanism differs."),
        N.h4("Building the Solution"),
        N.para("Use a result list. Scan for runs, append the character, then append each digit of the count if count > 1. Finally, copy result back into chars[]."),
    ]),
    N.h3("Code"),
    N.code("""def compress_brute(chars):
    result = []           # extra O(n) space
    i = 0
    while i < len(chars):
        ch, count = chars[i], 0
        while i < len(chars) and chars[i] == ch:
            i += 1; count += 1
        result.append(ch)
        if count > 1:
            result.extend(str(count))
    chars[:len(result)] = result
    return len(result)"""),
    N.divider()
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (extra list)", "O(n)", "O(n)"],
        ["Read-Write Two Pointers (optimal)", "O(n)", "O(1)"],
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers (Array Manipulation)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Read-Write Two Pointers (same-direction, fast/slow write variant)", {})])),
    N.callout(
        "When to recognize this pattern: 'Modify array in-place with O(1) extra space', output is shorter or equal to input (compression, deduplication, filtering). One pointer scans all elements, another writes only the transformed output. The safety invariant is that write ≤ read always holds.",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Read-Write Two Pointer technique:"),
    N.bullet(N.rich([("Remove Duplicates from Sorted Array", {"bold": True}), (" (Easy) — write advances only when chars differ; identical skeleton (#26)", {})])),
    N.bullet(N.rich([("Move Zeroes", {"bold": True}), (" (Easy) — write advances only on non-zero elements; same pointer setup (#283)", {})])),
    N.bullet(N.rich([("Remove Element", {"bold": True}), (" (Easy) — skip elements equal to val; write skips them (#27)", {})])),
    N.bullet(N.rich([("Count and Say", {"bold": True}), (" (Medium) — same run-length encoding idea applied iteratively (#38)", {})])),
    N.bullet(N.rich([("Decompress Run-Length Encoded List", {"bold": True}), (" (Easy) — reverse direction: expand each (freq, val) pair (#1313)", {})])),
    N.bullet(N.rich([("Remove Duplicates from Sorted Array II", {"bold": True}), (" (Medium) — allow at most 2 copies; write pointer has a look-back condition (#80)", {})])),
    N.para("These problems share the same core technique: a write pointer that only advances when valid/compressed output is produced, always lagging behind the read pointer."),
    N.divider()
]

# ── Interactive Visual Explainer embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("string_compression")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ]))
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
