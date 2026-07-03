"""
gen_queue_reconstruction_by_height.py
Notion in-place update for LeetCode #406 Queue Reconstruction by Height.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8167-abeb-d515309c84f1"

# ── 1) Set properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=406,
    pattern="Greedy",
    subpatterns=["Sort + Insert by K"],
    tc="O(n²)",
    sc="O(n)",
    key_insight="Sort tallest-first, insert each person at index k — all existing elements are ≥ h so k elements satisfy constraint instantly.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build the new body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a list of people, each represented as ", {}),
        ("[h, k]", {"code": True}),
        (" where ", {}),
        ("h", {"code": True}),
        (" is the person's height and ", {}),
        ("k", {"code": True}),
        (" is the number of people in front of them who have a height greater than or equal to ", {}),
        ("h", {"code": True}),
        (". The list is shuffled. Reconstruct and return the queue that satisfies every person's ", {}),
        ("k", {"code": True}),
        ("-constraint.", {}),
    ])),
    N.para("Example: Input [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]] → Output [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]."),
    N.divider(),
]

# ── Solution 1: Greedy Sort + Insert (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Greedy Sort + Insert (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to place n people in a line so that each person [h,k] has exactly k people of height ≥ h in front of them. Think of it as: each person knows their rank among taller peers, and we need to reconstruct the ordering from those ranks."),
        N.h4("What Doesn't Work"),
        N.para("Brute force (try all permutations): O(n! × n) — completely impractical. Shortest-first greedy: when we place a short person at index k, we don't know yet how many tall people will be inserted before them. Future tall-person insertions change their actual k-count, breaking the already-placed constraint."),
        N.h4("The Key Observation"),
        N.para("Tall people don't care about short people. A person of height 7 only counts people of height ≥ 7 in their k-count. People of height 4, 5, or 6 are completely invisible to them. This asymmetry means: if we place tall people first, their constraints only involve each other. Shorter people inserted afterward are invisible to the tall ones and cannot break their constraints."),
        N.h4("Building the Solution"),
        N.para("Sort tallest-first (key: (-h, k)). Ties broken by k ascending — so for equal heights, the person with smaller k is placed first, making them 'visible' to the person with larger k. Then for each person [h,k] in sorted order: result.insert(k, [h,k]). At this moment, all existing elements have height ≥ h, so indices 0..k-1 give exactly k elements satisfying the constraint. Done."),
        N.callout("Analogy: Imagine seating people by height in a theatre. Tallest rows fill first. Each new person says 'I want exactly k people in front of me who are at least as tall.' Since all seats already taken are taller-or-equal, they just count k seats in and sit down.", "🎭", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def reconstructQueue(people: list[list[int]]) -> list[list[int]]:\n"
        "    # Sort: tallest first; equal heights by k ascending\n"
        "    people.sort(key=lambda x: (-x[0], x[1]))\n"
        "    result = []\n"
        "    for h, k in people:\n"
        "        # At this point, all elements in result have height >= h\n"
        "        # Inserting at index k places exactly k elements of height >= h in front\n"
        "        result.insert(k, [h, k])\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("people.sort(key=lambda x: (-x[0], x[1]))", {"code": True}), (" — Sort descending by height (", {}), ("-x[0]", {"code": True}), ("), ascending by k (", {}), ("x[1]", {"code": True}), (") for ties. This ensures tallest people are processed first, and among equal heights, smaller k comes first.", {})])),
    N.para(N.rich([("result = []", {"code": True}), (" — Empty list. We build the final queue incrementally. Every insertion maintains the greedy invariant: all placed people have their k-constraint satisfied.", {})])),
    N.para(N.rich([("for h, k in people:", {"code": True}), (" — Iterate over sorted input. At each iteration, people not yet processed are all shorter-or-equal to current person (since we sorted tallest-first).", {})])),
    N.para(N.rich([("result.insert(k, [h, k])", {"code": True}), (" — Insert at index k. Key guarantee: all elements currently in result have height ≥ h. So indices 0..k-1 are all ≥ h. Exactly k people of height ≥ h are in front. The constraint is satisfied at the moment of insertion.", {})])),
    N.para(N.rich([("return result", {"code": True}), (" — All constraints satisfied by construction. No verification pass needed.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force (for context) ──
blocks += [
    N.h2("Solution 2 — Brute Force (Permutation Check)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible ordering of the n people. For each permutation, verify whether all k-constraints are satisfied. Return the first valid ordering found."),
        N.h4("What Doesn't Work"),
        N.para("There are n! permutations. For n=6 that's 720; for n=20 it's over 2 quadrillion. Each check takes O(n²). This is completely infeasible."),
        N.h4("The Key Observation"),
        N.para("This establishes a baseline: any correct algorithm must be far better than O(n! × n). The greedy approach achieves O(n²) by exploiting the structure of the problem."),
        N.h4("Building the Solution"),
        N.para("Enumerate all permutations using itertools.permutations. For each, check each person's k-count against their position. Return the first valid one."),
    ]),
    N.h3("Code"),
    N.code(
        "from itertools import permutations\n\n"
        "def reconstructQueue_brute(people: list[list[int]]) -> list[list[int]]:\n"
        "    for perm in permutations(people):\n"
        "        valid = True\n"
        "        for i, (h, k) in enumerate(perm):\n"
        "            count = sum(1 for ph, _ in perm[:i] if ph >= h)\n"
        "            if count != k:\n"
        "                valid = False\n"
        "                break\n"
        "        if valid:\n"
        "            return list(perm)\n"
        "    return []  # Problem guarantees a solution exists"
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (permutation check)", "O(n! × n)", "O(n)"],
        ["Greedy Sort + Insert (optimal)", "O(n²)", "O(n)"],
        ["Greedy + Binary Indexed Tree", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Greedy", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Insert by K", {})])),
    N.callout(
        "When to recognize this pattern: Each element has a positional constraint based on counting neighbors with a specific property (height ≥ h). One dimension defines visibility/priority (height), and the second gives the exact target position (k). The 'tallest first' order ensures constraints can be satisfied greedily without revision.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Greedy / Sort-based reconstruction):"),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Greedy arrangement of tasks with cooldown; count frequencies to determine idle gaps. #621", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), (" (Medium) — Sort by end time, greedy keep to minimize removals. #435", {})])),
    N.bullet(N.rich([("Minimum Arrows to Burst Balloons", {"bold": True}), (" (Medium) — Sort by balloon end, greedy coverage with minimum arrows. #452", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Sort by start time, assign greedily using min-heap of end times. #253", {})])),
    N.bullet(N.rich([("Car Pooling", {"bold": True}), (" (Medium) — Events sorted by position, greedy capacity constraint checking. #1094", {})])),
    N.bullet(N.rich([("Russian Doll Envelopes", {"bold": True}), (" (Hard) — Sort by width ascending, apply LIS on height. Same 'sort one dimension, process other' paradigm. #354", {})])),
    N.para("These problems share the core technique: sort by one attribute to establish a processing order that enables greedy local decisions."),
    N.callout("📚 Pattern: Greedy · Sub-Pattern: Sort + Insert by K · Source: Analysis (not explicitly in DSA Patterns Guide, but related to 'Sort + Greedy Insertion' family)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("queue_reconstruction_by_height")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
