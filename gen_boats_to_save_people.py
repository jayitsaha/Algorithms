"""
gen_boats_to_save_people.py — Notion update for LeetCode #881 Boats to Save People
Run: python3 gen_boats_to_save_people.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-818a-aaf0-fc64bd45f7b9"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=881,
    pattern="Array Manipulation",
    subpatterns=["Two Pointer: Opposite Direction"],
    tc="O(n log n)",
    sc="O(1)",
    key_insight="Sort then greedily pair heaviest with lightest; heaviest always boards unconditionally.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array ", {}),
        ("people", {"code": True}),
        (" where ", {}),
        ("people[i]", {"code": True}),
        (" is the weight of the i-th person, and an infinite number of boats where each boat can carry a maximum weight of ", {}),
        ("limit", {"code": True}),
        (". Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most ", {}),
        ("limit", {"code": True}),
        (". Return the minimum number of boats to carry every given person.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Two-Pointer Greedy (Interview Pick) ───────────────────────
blocks += [
    N.h2("Solution 1 — Two-Pointer Greedy (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have n people and unlimited boats, each holding at most 2. Every boat is either a solo (1 person) or a pair (2 people). Minimizing boats = maximizing pairs. So the question becomes: how do we greedily form the maximum number of valid pairs?"),

        N.h4("What Doesn't Work"),
        N.para("Naively trying every combination of pairs is O(n!) — obviously too slow. Even an O(n²) nested scan (try each person with each other) is inefficient. We need a smarter structure."),

        N.h4("The Key Observation"),
        N.para("The heaviest person is the hardest to pair. If you can't pair them with the lightest available person, you can't pair them with anyone (since everyone else is at least as heavy as the lightest). So: sort, then always process the heaviest by trying to pair them with the lightest. If it works, both board. If not, the heaviest goes solo."),

        N.h4("Building the Solution"),
        N.para("Sort the people array. Place lo=0 (lightest) and hi=n-1 (heaviest). At each step: (1) Check if people[lo]+people[hi]<=limit. (2) If yes, move lo right — lightest joins the boat. (3) Always move hi left — heaviest always boards. (4) boats++. Repeat while lo<=hi."),

        N.callout("Analogy: Loading a Ferry. Sort passengers by weight. Load from both ends — heaviest from one side, lightest from the other. If they fit on the same trip, great. Otherwise, the heaviest takes a solo trip and the lightest waits for the next one.", "🛥️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def numRescueBoats(people: list[int], limit: int) -> int:\n"
        "    people.sort()                    # Sort ascending\n"
        "    lo, hi = 0, len(people) - 1     # lo = lightest, hi = heaviest\n"
        "    boats = 0\n"
        "    while lo <= hi:\n"
        "        if people[lo] + people[hi] <= limit:\n"
        "            lo += 1                  # Lightest boards too\n"
        "        hi -= 1                      # Heaviest ALWAYS boards (unconditional)\n"
        "        boats += 1\n"
        "    return boats\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("people.sort()", {"code": True}), (" — Sort ascending so we can access lightest (index 0) and heaviest (index n-1) in O(1). Timsort is in-place, O(n log n).", {})])),
    N.para(N.rich([("lo, hi = 0, len(people) - 1", {"code": True}), (" — Initialize opposite-direction two pointers. lo=lightest unrescued, hi=heaviest unrescued.", {})])),
    N.para(N.rich([("while lo <= hi", {"code": True}), (" — Continue while at least one person is unrescued. When lo==hi, one person is left and the loop body handles them correctly.", {})])),
    N.para(N.rich([("if people[lo] + people[hi] <= limit", {"code": True}), (" — The key greedy check: can the lightest and heaviest share a boat? If yes, lo advances.", {})])),
    N.para(N.rich([("lo += 1", {"code": True}), (" — Only executed when pairing succeeds. Lightest person boards with the heaviest.", {})])),
    N.para(N.rich([("hi -= 1", {"code": True}), (" — UNCONDITIONAL — outside the if block. Heaviest person always boards a boat, whether paired or solo. This is the most common bug location.", {})])),
    N.para(N.rich([("boats += 1", {"code": True}), (" — One boat used per iteration regardless of whether it carried one or two people.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Sort + Nested Scan (Brute Force)"),
    N.toggle_h3("💡 Intuition: Why Brute Force Fails", [
        N.h4("Reframe the Problem"),
        N.para("Process people from heaviest to lightest. For each unrescued heavy person, scan for the lightest available partner. Mark both as rescued when paired."),

        N.h4("What Doesn't Work"),
        N.para("The inner scan is O(n) per person, making this O(n²) overall. For n=50,000 people (LeetCode constraint), this is 2.5 billion operations — far too slow."),

        N.h4("The Key Observation"),
        N.para("The brute force is conceptually correct but inefficient. The two-pointer approach replaces the O(n) inner scan with an O(1) step — we always know the lightest available person is at lo, so no scan needed."),

        N.callout("The two-pointer greedy is essentially the brute force with the inner scan eliminated by maintaining the invariant that lo is always the lightest unrescued person.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def numRescueBoats_brute(people, limit):\n"
        "    people.sort()\n"
        "    used = [False] * len(people)\n"
        "    boats = 0\n"
        "    for i in range(len(people)-1, -1, -1):  # heaviest first\n"
        "        if used[i]: continue\n"
        "        for j in range(i):  # scan for lightest partner — O(n)\n"
        "            if not used[j] and people[j] + people[i] <= limit:\n"
        "                used[j] = True\n"
        "                break\n"
        "        used[i] = True\n"
        "        boats += 1\n"
        "    return boats\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(people)-1, -1, -1)", {"code": True}), (" — Process from heaviest to lightest.", {})])),
    N.para(N.rich([("for j in range(i)", {"code": True}), (" — Inner O(n) scan for the lightest unused partner. This is what the two-pointer eliminates.", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two-Pointer Greedy (optimal)", "O(n log n)", "O(1)"],
        ["Brute Force Nested Scan", "O(n²)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Array Manipulation", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Two Pointer: Opposite Direction (with Greedy Pairing)", {})])),
    N.callout(
        "When to recognize this pattern: Problem asks to minimize the number of groups/pairs subject to a combined sum ≤ limit. At most 2 elements per group. After sorting, the most constrained element (heaviest) is at one end; the best possible partner (lightest) is at the other end.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (opposite-direction two pointers + greedy):"),
    N.bullet(N.rich([("Two Sum II – Input Array Is Sorted", {"bold": True}), (" (Medium) — Classic lo/hi converging to find target sum. Direct template for this problem.", {})])),
    N.bullet(N.rich([("Container With Most Water", {"bold": True}), (" (Medium) — Maximize area by always moving the shorter pointer. Greedy reasoning similar.", {})])),
    N.bullet(N.rich([("3Sum", {"bold": True}), (" (Medium) — Fix one element, use lo/hi two pointers to find the complementary pair.", {})])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), (" (Hard) — lo/hi track left/right max boundaries as pointers converge.", {})])),
    N.bullet(N.rich([("Valid Palindrome", {"bold": True}), (" (Easy) — lo/hi converge toward center checking character equality.", {})])),
    N.bullet(N.rich([("Assign Cookies", {"bold": True}), (" (Easy) — Greedily assign smallest sufficient cookie to least greedy child. Same pairing logic.", {})])),
    N.para("These problems share the core insight: sort first, then use opposite-direction pointers to greedily match the most constrained element with its best available partner."),
    N.divider(),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("boats_to_save_people")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
