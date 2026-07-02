"""
Notion updater for Group Shifted Strings (LeetCode #249).
Updates the existing page in-place (wipe + rewrite).
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81bd-a018-fb2febdef4f4"

# ── 1. Properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=249,
    pattern="Hash Tables",
    subpatterns=["Shift Pattern as Key"],
    tc="O(n·k)",
    sc="O(n·k)",
    key_insight="Consecutive character gaps mod 26 form a shift-invariant canonical key for hash-map grouping.",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe old content ────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks")

# ── 3. Build new body ─────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a list of strings, group all strings that belong to the same shifting sequence. "
         "A string ", {}),
        ("s", {"code": True}),
        (" can be shifted by incrementing all its characters by 1 (wrapping ", {}),
        ("z → a", {"code": True}),
        ("). Two strings are in the same group if one can be obtained from the other by "
         "some number of shifts. Return a list of all groups.", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('Input: ["abc","bcd","az","ba","a","b","z"] → Output: [["abc","bcd"],["az","ba"],["a","b","z"]]', {"code": True})
    ])),
    N.divider(),
]

# ── Solution 1: Gap Tuple Key (Interview Pick) ──────────────────
blocks += [
    N.h2("Solution 1 — Gap Tuple Key (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Grouping items that are 'equivalent under some transformation' is a classic hash map problem. The key question is: what property is preserved when you shift a string? We need a canonical fingerprint that all strings in the same shift-group share."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each pair, try all 26 possible shifts to see if one becomes the other — O(n²·k·26). Way too slow. Also error-prone with wraparound. We need to normalize each string independently, not compare strings pairwise."),
        N.h4("The Key Observation"),
        N.para("Shifting all characters by the same constant d leaves the consecutive differences UNCHANGED. If gap[i] = (s[i+1] - s[i]) % 26, then ((s[i+1]+d) - (s[i]+d)) % 26 = gap[i]. So the gap tuple is shift-invariant — it's the perfect canonical key."),
        N.h4("Building the Solution"),
        N.para("For each string, compute key = tuple((ord(s[i]) - ord(s[i-1])) % 26 for i in range(1, len(s))). Use this as the hash map key. Append the string to groups[key]. Length-1 strings get key = empty tuple (), correctly grouping all single-char strings together. Return list(groups.values())."),
        N.callout(
            "Analogy: Think of the gap tuple as a string's 'DNA' — it captures the rhythm and intervals between characters, independent of what note the music starts on. Two melodies with the same intervals are the same tune played in different keys.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import defaultdict\n\n"
        "def groupStrings(strings):\n"
        "    groups = defaultdict(list)\n"
        "    for s in strings:\n"
        "        key = tuple(\n"
        "            (ord(s[i]) - ord(s[i-1])) % 26\n"
        "            for i in range(1, len(s))\n"
        "        )\n"
        "        groups[key].append(s)\n"
        "    return list(groups.values())"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("groups = defaultdict(list)", {"code": True}), (" — Create a hash map that auto-initializes missing keys to empty lists. Keys will be gap tuples; values will be lists of strings.", {})])),
    N.para(N.rich([("for s in strings:", {"code": True}), (" — Process each input string exactly once.", {})])),
    N.para(N.rich([("key = tuple((ord(s[i]) - ord(s[i-1])) % 26 for i in range(1, len(s)))", {"code": True}), (" — Compute k-1 consecutive character differences, each mod 26 to handle wraparound. The % 26 is critical: (ord('a') - ord('z')) % 26 = 1, not -25.", {})])),
    N.para(N.rich([("groups[key].append(s)", {"code": True}), (" — Bucket the string under its fingerprint. defaultdict handles the first-time case automatically.", {})])),
    N.para(N.rich([("return list(groups.values())", {"code": True}), (" — Each value is a list of strings in the same shifting sequence.", {})])),
    N.divider(),
]

# ── Solution 2: Normalize to 'a' ───────────────────────────────
blocks += [
    N.h2("Solution 2 — Normalize to Start at 'a'"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of computing relative gaps, we can shift every string so it 'starts with a'. Two strings in the same shift-group, when normalized to start with 'a', will produce identical character sequences — giving us the same canonical key."),
        N.h4("What Doesn't Work"),
        N.para("Using the raw string as a key won't work — 'abc' and 'bcd' would have different keys even though they're in the same group. We must normalize away the absolute position."),
        N.h4("The Key Observation"),
        N.para("If we subtract the code of the first character from every character (mod 26), the normalized string always starts at 'a'. Any two strings in the same shift-group produce the same normalized tuple."),
        N.h4("Building the Solution"),
        N.para("offset = ord(s[0]) - ord('a'). Then key = tuple((ord(c) - ord('a') - offset) % 26 for c in s). Example: 'bcd' → offset=1 → (0,1,2) — same as 'abc' (offset=0 → (0,1,2)). Use this key in the same hash map approach."),
    ]),
    N.h3("Code"),
    N.code(
        "def groupStrings(strings):\n"
        "    groups = defaultdict(list)\n"
        "    for s in strings:\n"
        "        offset = ord(s[0]) - ord('a')\n"
        "        key = tuple(\n"
        "            (ord(c) - ord('a') - offset) % 26\n"
        "            for c in s\n"
        "        )\n"
        "        groups[key].append(s)\n"
        "    return list(groups.values())"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("offset = ord(s[0]) - ord('a')", {"code": True}), (" — Distance from the first character to 'a'. For 'bcd', offset=1; for 'abc', offset=0.", {})])),
    N.para(N.rich([("(ord(c) - ord('a') - offset) % 26", {"code": True}), (" — Normalize each character: subtract offset so the string conceptually 'starts at a'. % 26 handles wraparound for all shifts.", {})])),
    N.para("Both solutions are O(n·k) time and space, and are equivalent — they produce the same groupings. Use whichever you can explain more clearly in the interview."),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (pairwise)", "O(n²·k·26)", "O(n)"],
        ["Gap Tuple Key (Interview Pick)", "O(n·k)", "O(n·k)"],
        ["Normalize to 'a'", "O(n·k)", "O(n·k)"],
    ]),
    N.para(N.rich([
        ("n", {"code": True}), (" = number of strings, ", {}),
        ("k", {"code": True}), (" = max string length. Computing a length-k gap tuple is O(k); hashing it is O(k). "
        "The space accounts for storing all strings in the hash map and all gap-tuple keys.", {})
    ])),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Hash Tables", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Shift Pattern as Key", {})])),
    N.callout(
        "When to recognize this pattern: Problem asks to GROUP strings that are 'equivalent' under a uniform character transformation. "
        "The transformation preserves relative inter-character differences. "
        "Key signals: 'shifting sequence', 'same pattern', 'cyclic equivalence', 'group by structure not value'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Group Anagrams", {"bold": True}), (" (Medium) — Same hash-map grouping template; canonical key = sorted characters (#49)", {})])),
    N.bullet(N.rich([("Valid Anagram", {"bold": True}), (" (Easy) — Frequency count; atomic building block for character-based grouping (#242)", {})])),
    N.bullet(N.rich([("Isomorphic Strings", {"bold": True}), (" (Easy) — Check if two strings share the same character-mapping pattern (#205)", {})])),
    N.bullet(N.rich([("Word Pattern", {"bold": True}), (" (Easy) — Pattern matching between abstract pattern and word sequence (#290)", {})])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), (" (Medium) — Sliding window with canonical frequency key (#438)", {})])),
    N.bullet(N.rich([("Encode and Decode Strings", {"bold": True}), (" (Medium) — Canonical encoding; preserving relational structure (#271)", {})])),
    N.para("These problems all share the core technique: compute a canonical representation invariant to some equivalence class, then use a hash map to bucket by that representation."),
    N.divider(),
]

# ── Interactive Visual Explainer ─────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("group_shifted_strings")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch each string get mapped to its shift-pattern key and see the groups form in real time.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
