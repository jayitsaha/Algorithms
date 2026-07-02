"""
gen_minimum_deletions_to_make_character_frequencies_unique.py
Updates Notion page 39193418-809c-816a-9be9-e8a9660dc299 in-place for
LeetCode #1647 — Minimum Deletions to Make Character Frequencies Unique
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-816a-9be9-e8a9660dc299"
SLUG = "minimum_deletions_to_make_character_frequencies_unique"

# ── 1) Set properties ─────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1647,
    pattern="Hash Tables",
    subpatterns=["Greedy Decrement Duplicates"],
    tc="O(n)",
    sc="O(k)",
    key_insight="Count frequencies; greedily decrement each conflicting frequency by 1 until a free slot is found, accumulating deletions.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ───────────────────────────────────────────────
print("Wiping old page content...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

# ── 3) Build body ─────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" of lowercase characters, a string is called ", {}),
        ("good", {"bold": True}),
        (" if there are no two different characters with the same frequency. Return the ", {}),
        ("minimum", {"bold": True}),
        (" number of characters you need to delete to make ", {}),
        ("s", {"code": True}),
        (" good.", {}),
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ('s = "aab" → Output: 0', {"code": True}),
        ('. Already good (a→2, b→1, all unique).', {}),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ('s = "aaabbbcc" → Output: 2', {"code": True}),
        ('. Delete one b and one c → a→3, b→2, c→1. All unique frequencies.', {}),
    ])),
    N.para(N.rich([
        ("Example 3: ", {"bold": True}),
        ('s = "ceabaacb" → Output: 2', {"code": True}),
        ('. After deleting 2 characters the string can be made good.', {}),
    ])),
    N.callout(
        "Key constraint: you can only DELETE characters, not insert or rearrange. Each deletion reduces one character's frequency by exactly 1.",
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1 — Greedy + Set ──
SOLUTION_1_CODE = '''\
from collections import Counter

def minDeletions(s: str) -> int:
    freq = list(Counter(s).values())  # Frequency of each character
    used = set()                       # Already-claimed frequency slots
    deletions = 0

    for f in freq:
        # While this frequency is already taken (and we haven't deleted all)
        while f > 0 and f in used:
            f -= 1          # Delete one occurrence; try next lower slot
            deletions += 1  # Count this deletion

        if f > 0:
            used.add(f)  # Claim this slot (skip 0: "fully deleted" needs no slot)

    return deletions
'''

blocks += [
    N.h2("Solution 1 — Greedy Decrement with Used-Set (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The character identities don't matter — only the frequency values matter. "
            "We have a multiset of positive integers (the counts). We need to make them "
            "all distinct, where the only operation is decrement (deletion). "
            "Restate: given integers, minimize total decrements to make them all unique."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force — trying all subsets of characters to delete — is exponential O(2^n). "
            "We can't greedily delete the most-frequent character each time without knowing "
            "the global state. We need a smarter invariant."
        ),
        N.h4("The Key Observation"),
        N.para(
            "For each conflicting frequency f (already claimed), the minimum cost to resolve "
            "it is decrement-until-free: try f-1, f-2, ... until we land on an unclaimed slot. "
            "This is optimal because each step costs exactly 1 deletion and we stop the instant "
            "we succeed. We can't do it in fewer steps."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Count all character frequencies with Counter. "
            "2. Maintain a set of 'used' frequency values. "
            "3. For each frequency f: while f is in used and f > 0, decrement f and count one deletion. "
            "4. If f > 0, add to used-set. If f == 0, skip (multiple chars can be fully deleted). "
            "5. Return total deletions."
        ),
        N.callout(
            "Analogy: Imagine frequency slots as hotel rooms numbered 1, 2, 3, ... "
            "Each character wants the highest-numbered available room ≤ its original count. "
            "If taken, it tries the room below. Each failed try = one deletion.",
            "🏨", "gray_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("freq = list(Counter(s).values())", {"code": True}),
                   (" — Count each character's frequency using Counter; extract only the values. We discard which char has which count — only the numbers matter.", {})])),
    N.para(N.rich([("used = set()", {"code": True}),
                   (" — Empty set to track which frequency values are already 'claimed' by processed characters.", {})])),
    N.para(N.rich([("for f in freq:", {"code": True}),
                   (" — Process each character's frequency one at a time.", {})])),
    N.para(N.rich([("while f > 0 and f in used:", {"code": True}),
                   (" — If the current frequency slot is taken (conflict!), and we haven't deleted all occurrences (f > 0), we must keep decrementing.", {})])),
    N.para(N.rich([("f -= 1", {"code": True}),
                   (" — One deletion: conceptually remove one occurrence of this character, moving to the next lower frequency slot.", {})])),
    N.para(N.rich([("deletions += 1", {"code": True}),
                   (" — Count this deletion toward the total.", {})])),
    N.para(N.rich([("if f > 0: used.add(f)", {"code": True}),
                   (" — Only claim a slot if the character still exists (f > 0). Frequency 0 means 'completely deleted' — no need to reserve it as multiple chars can share this state.", {})])),
    N.para(N.rich([("return deletions", {"code": True}),
                   (" — The accumulated count is the minimum number of deletions needed.", {})])),
    N.divider(),
]

# ── Solution 2 — Sort + Sweep ──
SOLUTION_2_CODE = '''\
from collections import Counter

def minDeletions(s: str) -> int:
    # Sort frequencies descending: largest gets highest slot
    freq = sorted(Counter(s).values(), reverse=True)
    deletions = 0

    for i in range(1, len(freq)):
        # freq[i] must be strictly less than freq[i-1]
        if freq[i] >= freq[i - 1]:
            # Reduce to just below previous; minimum is 0
            new_f = max(0, freq[i - 1] - 1)
            deletions += freq[i] - new_f
            freq[i] = new_f  # Update for the next comparison

    return deletions
'''

blocks += [
    N.h2("Solution 2 — Sort + Sweep (No Set Required)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "After sorting frequencies descending, a 'good' configuration means the array "
            "must be strictly decreasing (each element < the one before it). "
            "If freq[i] >= freq[i-1], we have a conflict and must reduce freq[i] to "
            "max(0, freq[i-1] - 1). The reduction amount is the number of deletions."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Without sorting, we can't use this left-to-right sweep. "
            "Sorting ensures we process in a consistent order where 'previous' always "
            "represents the highest already-assigned frequency."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Once sorted descending, each element needs to be at most (previous - 1). "
            "If it's already smaller, no action needed. If not, reduce it to (previous - 1) "
            "and count the difference as deletions. Then update freq[i] because the next "
            "element will compare against this new value."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Sort descending. Iterate i from 1 to n-1. "
            "If freq[i] >= freq[i-1]: compute new_f = max(0, freq[i-1] - 1). "
            "Add freq[i] - new_f to deletions. Set freq[i] = new_f. "
            "Continue. Return deletions."
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("freq = sorted(Counter(s).values(), reverse=True)", {"code": True}),
                   (" — Sort character frequencies in descending order. Largest frequencies get first pick of high slots.", {})])),
    N.para(N.rich([("for i in range(1, len(freq)):", {"code": True}),
                   (" — Compare each frequency to the one before it in the sorted list.", {})])),
    N.para(N.rich([("if freq[i] >= freq[i - 1]:", {"code": True}),
                   (" — In a properly good sorted-descending array, freq[i] must be strictly less than freq[i-1]. Any equality or reversal means conflict.", {})])),
    N.para(N.rich([("new_f = max(0, freq[i - 1] - 1)", {"code": True}),
                   (" — The best we can assign to freq[i] is one below the previous. Clamp to 0 (can't go negative).", {})])),
    N.para(N.rich([("deletions += freq[i] - new_f", {"code": True}),
                   (" — Deletions = how much we had to reduce freq[i] to resolve the conflict.", {})])),
    N.para(N.rich([("freq[i] = new_f", {"code": True}),
                   (" — Update freq[i] so the next iteration compares against this corrected value, not the original.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy + Set (S1)", "O(n)", "O(k)"],
        ["Sort + Sweep (S2)", "O(n + k log k)", "O(k)"],
        ["Brute Force", "O(2^n)", "O(n)"],
    ]),
    N.para(
        "k = number of distinct characters (≤ 26 for lowercase English → effectively O(1) space). "
        "The greedy while-loop total iterations across all characters is bounded by n "
        "(total decrements can't exceed total character count), giving O(n) overall."
    ),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Hash Tables", {}),
                   (" — We use a frequency count (Counter) to identify the core values to manipulate, then a set for O(1) collision detection.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Greedy Decrement Duplicates", {}),
                   (" — Greedily resolve duplicate values in a frequency map by decrementing until a free slot is found.", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem involves character frequencies or counts. "
        "(2) Need to make values UNIQUE. "
        "(3) Only DELETION (decrement) is allowed. "
        "(4) Objective is MINIMUM operations. "
        "→ Greedy decrement with a used-set is the canonical solution.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Minimum Steps to Make Two Strings Anagram", {"bold": True}),
                     (" (#1347, Medium) — Frequency delta between two strings; greedy matching to reduce one to match the other.", {})])),
    N.bullet(N.rich([("Determine if Two Strings Are Close", {"bold": True}),
                     (" (#1657, Medium) — Frequency multisets must match in distribution. Same Counter-based thinking.", {})])),
    N.bullet(N.rich([("Reorganize String", {"bold": True}),
                     (" (#767, Medium) — Place characters so no two adjacent are same; max-heap + frequency manipulation.", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}),
                     (" (#621, Medium) — Greedy CPU scheduling: max frequency character determines idle slots.", {})])),
    N.bullet(N.rich([("Sort Characters By Frequency", {"bold": True}),
                     (" (#451, Medium) — Rebuild string in descending frequency order using Counter + sort.", {})])),
    N.bullet(N.rich([("Maximum Frequency Stack", {"bold": True}),
                     (" (#895, Hard) — Frequency-ordered push/pop; frequency maps as keys in a hash map of stacks.", {})])),
    N.para("These problems share the core technique: count character frequencies, then manipulate the frequency values themselves (not the characters) to satisfy a uniqueness or ordering constraint."),
    N.callout("📚 Reference: Hash Tables section — Sub-Pattern: Greedy Decrement Duplicates", "📚", "gray_background"),
]

# ── Visual Explainer Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append all blocks ──────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
