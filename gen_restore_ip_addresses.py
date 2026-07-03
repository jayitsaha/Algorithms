"""
gen_restore_ip_addresses.py
LeetCode #93 — Restore IP Addresses
Pattern: Backtracking | Sub-Pattern: 4 Parts, Valid Range
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Page already created in prior run ──────────────────────────────────────
PAGE_ID = "39193418-809c-8112-9549-fc71f0e740c7"
print(f"Using existing page: {PAGE_ID}")

# ── Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=93,
    pattern="Backtracking",
    subpatterns=["4 Parts Valid Range"],
    tc="O(1)",
    sc="O(1)",
    key_insight="Place 3 dots into a digit string to form 4 valid IP octets (0–255, no leading zeros); backtrack with pruning over at most 3^4=81 paths.",
    icon="🟡",
)
print("Properties set.")

# ── Wipe any existing body (fresh page, but safe to call) ───────────────────
N.wipe_page(PAGE_ID)
print("Page wiped (was fresh).")

# ── Build body blocks ───────────────────────────────────────────────────────
blocks = []

# ── Problem ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string "), ("s", {"code": True}),
        (" containing only digits, return all valid IPv4 addresses that can be obtained by inserting exactly three dots into "),
        ("s", {"code": True}),
        (". A valid IP address has exactly four parts separated by dots, where each part is a non-empty string, has a value between 0 and 255 (inclusive), and has no leading zeros (except '0' itself). Return the valid IPs in any order."),
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ("s = \"25525511135\" → [\"255.255.11.135\", \"255.255.111.35\"]"),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ("s = \"0000\" → [\"0.0.0.0\"]"),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ s.length ≤ 20, s consists of digits only."),
    ])),
    N.divider(),
]

# ── Solution 1 — Backtracking ────────────────────────────────────────────────
sol1_code = """\
def restoreIpAddresses(s: str) -> list[str]:
    result = []

    def backtrack(start: int, parts: list):
        # Base case: all 4 parts placed
        if len(parts) == 4:
            if start == len(s):              # consumed entire string?
                result.append(".".join(parts))
            return

        parts_left = 4 - len(parts)
        remaining  = len(s) - start

        # Pruning: impossible digit distribution
        if remaining < parts_left or remaining > 3 * parts_left:
            return

        for length in range(1, 4):           # try segment lengths 1, 2, 3
            if start + length > len(s):
                break
            seg = s[start : start + length]
            if length > 1 and seg[0] == '0': # leading zero → break (longer also fails)
                break
            if int(seg) > 255:               # value too large → break
                break
            parts.append(seg)                # choose
            backtrack(start + length, parts) # explore
            parts.pop()                      # unchoose (backtrack)

    backtrack(0, [])
    return result\
"""

sol1_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("We need to insert exactly 3 dots into a digit string to create 4 non-empty parts. The question is: which 3 positions in the string can receive dots such that all 4 resulting substrings are valid IP octets?"),
    N.h4("What Doesn't Work"),
    N.para("Brute force: try all ways to split the string into 4 parts without any early filtering. This processes many clearly invalid states (e.g., parts with 6 digits) before rejecting them. We want to reject invalid branches as early as possible — before we finish building them."),
    N.h4("The Key Observation"),
    N.para("Each IP octet is 1–3 digits long, has value 0–255, and has no leading zeros. This severely constrains our search: at each position we have at most 3 choices for how many characters to include in the current part. With 4 parts and 3 choices each, the entire search space is at most 3^4 = 81 paths — a constant!"),
    N.h4("Building the Solution"),
    N.para("Use recursive backtracking: backtrack(start, parts) tries each segment length, validates it, appends to parts, recurses, then pops (undo). Two pruning conditions cut branches early: (1) too few remaining chars to fill remaining parts, (2) too many remaining chars to absorb in valid segments. The break-not-continue insight: once a segment of length L is invalid (leading zero or >255), all longer segments from the same position are also invalid."),
    N.callout("Analogy: Think of placing 3 bookmarks into a row of 4–12 numbered tiles. You can only put a bookmark after 1, 2, or 3 tiles — and only if the tiles between bookmarks form a valid number. Backtracking is just trying each bookmark position and taking it back if it leads nowhere.", "🧠", "blue_background"),
]

blocks += [
    N.h2("Solution 1 — Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol1_intuition_children),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), " — Accumulate all valid IP strings found."])),
    N.para(N.rich([("def backtrack(start, parts):", {"code": True}), " — Recursive helper. ", ("start", {"code": True}), " is the current index in ", ("s", {"code": True}), "; ", ("parts", {"code": True}), " holds segments chosen so far."])),
    N.para(N.rich([("if len(parts) == 4:", {"code": True}), " — Base case: exactly 4 parts have been placed. Check if we consumed the full string."])),
    N.para(N.rich([("if start == len(s):", {"code": True}), " — Only add to results if all characters are used. If parts were formed but characters remain, this is not a valid IP."])),
    N.para(N.rich([("result.append(\".\" .join(parts))", {"code": True}), " — Join the 4 parts with dots to form the final IP string."])),
    N.para(N.rich([("parts_left = 4 - len(parts)", {"code": True}), " — How many more parts still need to be assigned."])),
    N.para(N.rich([("remaining = len(s) - start", {"code": True}), " — How many characters are left to distribute."])),
    N.para(N.rich([("if remaining < parts_left or remaining > 3 * parts_left:", {"code": True}), " — Key pruning. If too few chars exist to fill each remaining part with at least 1 digit, or too many chars exist to absorb with at most 3 digits each, this branch is impossible."])),
    N.para(N.rich([("for length in range(1, 4):", {"code": True}), " — Try segment lengths 1, 2, and 3 — the only valid octet lengths."])),
    N.para(N.rich([("seg = s[start : start + length]", {"code": True}), " — Extract the candidate segment string."])),
    N.para(N.rich([("if length > 1 and seg[0] == '0': break", {"code": True}), " — Leading zero check: '0' alone is valid, '01' or '001' are not. Break (not continue) because a longer segment at the same position also starts with '0'."])),
    N.para(N.rich([("if int(seg) > 255: break", {"code": True}), " — Value range check. Break because a longer segment is numerically larger and also fails."])),
    N.para(N.rich([("parts.append(seg)", {"code": True}), " / ", ("backtrack(...)", {"code": True}), " / ", ("parts.pop()", {"code": True}), " — The classic choose → explore → unchoose backtracking triple. The pop() undoes the choice so the next iteration starts with a clean ", ("parts", {"code": True}), " list."])),
    N.divider(),
]

# ── Solution 2 — Iterative ───────────────────────────────────────────────────
sol2_code = """\
def restoreIpAddresses(s: str) -> list[str]:
    n, result = len(s), []

    def ok(part: str) -> bool:
        return (len(part) <= 3
                and int(part) <= 255
                and (part[0] != '0' or len(part) == 1))

    # Place 3 dots at positions i, j, k (exclusive right boundaries)
    for i in range(1, min(4, n)):
        for j in range(i + 1, min(i + 4, n)):
            for k in range(j + 1, min(j + 4, n)):
                p1, p2, p3, p4 = s[:i], s[i:j], s[j:k], s[k:]
                if all(ok(p) for p in [p1, p2, p3, p4]):
                    result.append(f"{p1}.{p2}.{p3}.{p4}")
    return result\
"""

sol2_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("Since there are exactly 3 dots to place, we can model this as choosing 3 split points i, j, k such that i < j < k, creating 4 substrings s[:i], s[i:j], s[j:k], s[k:]."),
    N.h4("What Doesn't Work"),
    N.para("Trying all possible (i, j, k) triples from 1 to n without bounds — this generates many out-of-range indices. The loop bounds min(4, n), min(i+4, n), etc. constrain each segment to at most 3 characters."),
    N.h4("The Key Observation"),
    N.para("For fixed structure (exactly 4 parts), three nested loops directly enumerate all valid dot placements. This is simpler code than backtracking, same complexity, but less generalizable if the part count changes."),
    N.h4("Building the Solution"),
    N.para("Loop i from 1 to min(4, n): first dot after 1, 2, or 3 digits. Loop j from i+1 to min(i+4, n): second dot 1–3 digits after first. Loop k from j+1 to min(j+4, n): third dot 1–3 digits after second. Then validate all 4 parts with the ok() helper."),
]

blocks += [
    N.h2("Solution 2 — Iterative Three Loops"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol2_intuition_children),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("def ok(part):", {"code": True}), " — Returns True if the string is a valid IP octet: length ≤ 3, value ≤ 255, no leading zero (unless it IS '0')."])),
    N.para(N.rich([("for i in range(1, min(4, n)):", {"code": True}), " — ", ("i", {"code": True}), " is the first dot position. Range ensures Part 1 is 1–3 chars."])),
    N.para(N.rich([("for j in range(i+1, min(i+4, n)):", {"code": True}), " — ", ("j", {"code": True}), " is the second dot. Starts 1 after i, ends so Part 2 is at most 3 chars."])),
    N.para(N.rich([("for k in range(j+1, min(j+4, n)):", {"code": True}), " — ", ("k", {"code": True}), " is the third dot. Same logic for Part 3."])),
    N.para(N.rich([("p1, p2, p3, p4 = s[:i], s[i:j], s[j:k], s[k:]", {"code": True}), " — Extract all 4 segments from the current dot positions."])),
    N.para(N.rich([("if all(ok(p) ...)", {"code": True}), " — Validate all 4 segments together. Only if all pass do we add the IP."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Backtracking (Interview Pick)", "O(1)", "O(1)"],
        ["Iterative Three Loops", "O(1)", "O(1)"],
    ]),
    N.para("Both approaches run in O(1) time and O(1) space because the input is bounded (4–12 digits for any valid IP), and the search space is bounded by 3^4 = 81 recursive paths / 3×3×3 = 27 loop iterations."),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Backtracking"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "4 Parts, Valid Range (Constrained Segmentation)"])),
    N.callout(
        "When to recognize this pattern: The problem asks to 'return all valid X' by splitting a string into exactly K parts, each satisfying specific constraints (length, value, format). A small fixed K and bounded segment lengths make backtracking viable — the search space is a constant.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same backtracking / constrained segmentation pattern:"),
    N.bullet(N.rich([("Letter Combinations of a Phone Number", {"bold": True}), " (Medium, #17) — map each digit to letters, build all strings character by character with choose/recurse/unchoose."])),
    N.bullet(N.rich([("Palindrome Partitioning", {"bold": True}), " (Medium, #131) — partition a string into valid palindromic parts; same recursive segmentation with a different validity predicate."])),
    N.bullet(N.rich([("Generate Parentheses", {"bold": True}), " (Medium, #22) — build all valid bracket strings of length 2n; choose '(' or ')' at each step with constraint checking."])),
    N.bullet(N.rich([("Word Break II", {"bold": True}), " (Hard, #140) — split string into dictionary words; backtracking with larger branching factor and memoization for overlapping subproblems."])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), " (Medium, #39) — select numbers summing to target; canonical backtracking with choose/unchoose and pruning."])),
    N.bullet(N.rich([("Subsets II", {"bold": True}), " (Medium, #90) — enumerate all subsets of an array with duplicates; backtracking with a skip-duplicate check."])),
    N.para("These problems share the same core technique: choose a valid option for the current position, recurse to fill remaining slots, then undo the choice to try the next option."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Backtracking section. Sub-pattern: Constrained Segmentation (4 Parts, Valid Range).", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ─────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("restore_ip_addresses")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Write status file ─────────────────────────────────────────────────────────
import json, pathlib
status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
html_path = pathlib.Path(__file__).parent / "restore_ip_addresses_explainer.html"
html_lines = len(html_path.read_text().splitlines())
status = {
    "slug": "restore_ip_addresses",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Fresh page created. Backtracking solution with 3-loop iterative alternative. 2 solutions in Notion."
}
status_path = status_dir / "restore_ip_addresses.json"
status_path.write_text(json.dumps(status, indent=2))
print(f"RESULT restore_ip_addresses | html=OK | notion=OK | lines={html_lines}")
