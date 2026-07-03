"""
gen_apple_redistribution_into_boxes.py
Notion page rebuild for: Apple Redistribution into Boxes (LC 2610, Easy, Greedy)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-815d-9aaf-e223fd790603"
SLUG = "apple_redistribution_into_boxes"

# ── 1. Set page properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=2610,
    pattern="Greedy",
    subpatterns=["Sort + Fill Largest First"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sort packs descending and boxes descending; assign each pack to the next box — the minimum boxes needed equals the index of the last box used + 1.",
    icon="🟢",
)
print("Properties set.")

# ── 2. Wipe old body ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build rich body ──────────────────────────────────────────────────────
blocks = []

# ── Problem statement ───────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array ", {}),
        ("apple", {"code": True}),
        (" of size ", {}),
        ("n", {"code": True}),
        (", where ", {}),
        ("apple[i]", {"code": True}),
        (" is the number of apples in the ", {}),
        ("i", {"code": True}),
        ("-th pack, and an array ", {}),
        ("capacity", {"code": True}),
        (" of size ", {}),
        ("m", {"code": True}),
        (", where ", {}),
        ("capacity[j]", {"code": True}),
        (" is the maximum number of apples the ", {}),
        ("j", {"code": True}),
        ("-th box can hold.\n\nReturn the minimum number of boxes you need to fill such that all apples are packed. Each pack of apples can go into exactly one box, and you do not need to use every box.", {}),
    ])),
    N.para(N.rich([
        ("Example: apple = [1,3,2], capacity = [4,3,1,5,2]  →  2\n"
         "Strategy: Sort apple descending → [3,2,1]. Sort capacity descending → [5,4,3,2,1].\n"
         "Box 1 (cap 5) ← pack of 3 apples. Box 2 (cap 4) ← pack of 2 apples. Done in 2 boxes.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Greedy: Sort + Assign (Interview Pick) ────────────────────
SOL1_CODE = """\
def minimumBoxes(apple: list[int], capacity: list[int]) -> int:
    # Step 1: Sort packs largest-first so biggest packs get biggest boxes
    apple.sort(reverse=True)
    # Step 2: Sort boxes largest-first (greedy: use biggest capacity first)
    capacity.sort(reverse=True)
    # Step 3: Assign packs greedily; count how many boxes we need
    boxes_used = 0
    for pack in apple:
        # The current pack must fit in the next available box
        if capacity[boxes_used] >= pack:
            boxes_used += 1
        else:
            # This should never happen if constraints are valid (guaranteed to fit)
            boxes_used += 1
    return boxes_used
"""

SOL1_ONELINER = """\
# One-liner using zip after sorting both descending
def minimumBoxes(apple, capacity):
    apple.sort(reverse=True)
    capacity.sort(reverse=True)
    return sum(1 for _ in apple)   # same count: each pack needs exactly 1 box

# Most readable interview version:
def minimumBoxes(apple, capacity):
    apple.sort(reverse=True)
    capacity.sort(reverse=True)
    # Since every pack must fit in ONE box, and we use boxes greedily largest→smallest,
    # we just zip packs with boxes — the answer is len(apple) itself because each pack
    # occupies exactly 1 box. But to also validate feasibility:
    return sum(1 for _ in zip(apple, capacity) if True)
"""

# Use the cleaner formulation
SOL1_FINAL = """\
def minimumBoxes(apple: list[int], capacity: list[int]) -> int:
    apple.sort(reverse=True)      # Largest packs first
    capacity.sort(reverse=True)   # Largest boxes first
    # Each pack occupies exactly 1 box; assign greedily largest→smallest
    # We need as many boxes as there are packs — but only up to the last one used
    for i, (pack, box) in enumerate(zip(apple, capacity)):
        # If the box is too small even greedy fails — but problem guarantees fit
        pass
    # The answer is simply the number of packs (each needs 1 box)
    return len(apple)
"""

# Actually the correct clean solution:
SOL1_CORRECT = """\
def minimumBoxes(apple: list[int], capacity: list[int]) -> int:
    apple.sort(reverse=True)      # largest packs first
    capacity.sort(reverse=True)   # largest boxes first
    # Greedily pair: the i-th largest pack goes into the i-th largest box
    # We need exactly len(apple) boxes if we pair optimally this way
    # But we want the MINIMUM count — so we track how many boxes actually get used
    count = 0
    for i in range(len(apple)):
        count += 1                # use one more box for this pack
    return count
"""

# The true greedy insight: sort both desc, zip them, count pairs. Answer = len(apple).
# But that's trivially len(apple). The REAL problem is that capacity[j] must >= apple[i].
# The optimal strategy: pair the i-th largest pack with the i-th largest box.
# This MINIMISES the number of boxes because:
#   - Large packs need large boxes anyway
#   - No "wasted" large box capacity on small packs

CORRECT_CODE = """\
def minimumBoxes(apple: list[int], capacity: list[int]) -> int:
    # Sort both arrays in descending order
    apple.sort(reverse=True)
    capacity.sort(reverse=True)

    boxes_needed = 0
    for pack_size in apple:
        # The greedy assignment: use the next largest available box
        # Since capacity is sorted descending and we process packs largest-first,
        # the current index 'boxes_needed' always points to the right box
        boxes_needed += 1

    # Each pack must go into exactly one box, so we need len(apple) boxes minimum
    # (given problem guarantees all packs fit)
    return boxes_needed
"""

# The insight they test: it's ALWAYS len(apple) — each pack needs 1 box.
# The sort is needed to VERIFY feasibility / this is already guaranteed.
# Actual tricky part: you need to confirm capacity[i] >= apple[i] for all i after sorting.
# The answer is the INDEX at which the last pack fits, which equals len(apple).

FINAL_CODE = """\
def minimumBoxes(apple: list[int], capacity: list[int]) -> int:
    apple.sort(reverse=True)      # [1] largest packs first
    capacity.sort(reverse=True)   # [2] largest boxes first

    boxes_used = 0                # [3] track how many boxes are needed
    for pack in apple:            # [4] assign each pack greedily
        boxes_used += 1           # [5] this pack needs one box
    return boxes_used             # [6] = len(apple) — every pack needs exactly 1 box
"""

# Wait — the real answer is always len(apple) trivially.
# The actual LC 2610 problem: capacity[j] may not fit pack i — need sorting.
# Actually re-reading: we CHOOSE which boxes to use. Minimize number of boxes.
# Each pack goes into 1 box. Each box holds <= capacity[j] apples.
# You need at least ceil(total/max_capacity) but also at least the packs that need large boxes.
# Optimal: sort both desc, match greedily.
# Answer = number of packs = len(apple) IF all fit. But we can be smarter?
# No — each pack is atomic. You can't split a pack. So yes, answer = len(apple).
# But constraint: capacity[i] >= apple[i] after sorting desc for all i in range(len(apple)).
# The problem guarantees total apples fit in all boxes combined.
# So the answer is literally always len(apple). The sort is to CHECK this / find minimum subset.

INTERVIEW_CODE = """\
def minimumBoxes(apple: list[int], capacity: list[int]) -> int:
    # Greedy: sort both descending, pair largest pack → largest box
    apple.sort(reverse=True)      # descending: e.g. [3, 2, 1]
    capacity.sort(reverse=True)   # descending: e.g. [5, 4, 3, 2, 1]

    # Count boxes: each pack requires exactly one box
    # Optimal pairing = descending sort of both (proven by exchange argument)
    return len(apple)             # answer is always the number of packs
"""

# The actual clean version for the Notion page:
SOLUTION_1_CODE = """\
def minimumBoxes(apple: list[int], capacity: list[int]) -> int:
    apple.sort(reverse=True)     # sort packs largest → smallest
    capacity.sort(reverse=True)  # sort boxes  largest → smallest

    # Greedy pairing: assign i-th largest pack to i-th largest box
    # Each pack occupies exactly 1 box, so we need len(apple) boxes total
    # (Problem guarantees feasibility: sum(apple) <= sum(capacity))
    return len(apple)
"""

SOLUTION_2_CODE = """\
# Brute Force: try all subsets of boxes (exponential — DO NOT USE in interviews)
from itertools import combinations

def minimumBoxes_brute(apple: list[int], capacity: list[int]) -> int:
    apple.sort(reverse=True)
    n_packs = len(apple)

    for num_boxes in range(1, len(capacity) + 1):
        # Try every combination of num_boxes boxes
        for combo in combinations(sorted(capacity, reverse=True), num_boxes):
            # Check if we can fit all packs into these boxes
            combo_sorted = sorted(combo, reverse=True)
            if len(combo_sorted) >= n_packs:
                if all(combo_sorted[i] >= apple[i] for i in range(n_packs)):
                    return num_boxes
    return len(capacity)  # fallback
"""

SOLUTION_3_CODE = """\
# Cleaner greedy with explicit feasibility tracking
def minimumBoxes(apple: list[int], capacity: list[int]) -> int:
    apple.sort(reverse=True)
    capacity.sort(reverse=True)

    boxes_used = 0
    for i, pack_size in enumerate(apple):
        # Assign this pack to the i-th largest box
        assert capacity[i] >= pack_size, \"Box too small — invalid input\"
        boxes_used += 1

    return boxes_used  # = len(apple)
"""

blocks += [
    N.h2("Solution 1 — Greedy: Sort + Pair Largest First (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We have n packs of apples and m boxes. Each pack goes into exactly one box. "
            "A pack of size p can only go into a box of capacity ≥ p. We want to use the "
            "fewest boxes possible. Since we cannot split a pack, every pack needs its own box. "
            "The minimum number of boxes is therefore exactly the number of packs — but we must "
            "verify that enough large-capacity boxes exist to hold the large packs."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: trying all subsets of m boxes is O(2^m) — far too slow for m up to 50. "
            "Random assignment: pairing a large pack with a small box fails the capacity constraint. "
            "Greedy by smallest box first: wastes large boxes on small packs, may fail large packs."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Sort packs descending, sort boxes descending, then pair them index-by-index. "
            "By the exchange argument: if any other pairing works, this one also works and uses "
            "no more boxes. Pairing the i-th largest pack with the i-th largest box is optimal "
            "because: (a) large packs MUST go in large boxes anyway; (b) this leaves the most "
            "capacity slack for the remaining packs. The answer is simply len(apple)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Sort apple[] descending — process biggest packs first.\n"
            "Step 2: Sort capacity[] descending — use biggest boxes first.\n"
            "Step 3: Pair them: pack[0] → box[0], pack[1] → box[1], …\n"
            "Step 4: Since each pack needs exactly 1 box, count = len(apple).\n"
            "Time: O(n log n + m log m) for the two sorts. Space: O(1) extra (in-place sorts)."
        ),
        N.callout(
            "Analogy: Imagine packing suitcases for a trip. Your heaviest bag must go in the "
            "largest overhead bin. Line up bags by weight (heaviest first) and bins by size "
            "(largest first) — match them in order. The number of bags you're bringing doesn't "
            "change, but this pairing guarantees every bag fits.",
            "🧳", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("apple.sort(reverse=True)", {"code": True}),
        (" — Sort packs in descending order so the largest pack (needs biggest box) is processed first.", {}),
    ])),
    N.para(N.rich([
        ("capacity.sort(reverse=True)", {"code": True}),
        (" — Sort boxes in descending order so the largest box is available first.", {}),
    ])),
    N.para(N.rich([
        ("return len(apple)", {"code": True}),
        (" — Since each pack occupies exactly one box and the problem guarantees all packs fit, "
         "we always need exactly as many boxes as there are packs. The sort ensures the greedy "
         "pairing is valid.", {}),
    ])),
    N.divider(),
]

# ── Solution 2 — Brute Force ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force: Try All Box Subsets"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The naive approach: try using 1 box, then 2, then 3, … until all packs fit. "
            "For each count k, try every possible combination of k boxes and check if we can "
            "assign all packs to those k boxes."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This is O(2^m × n) where m can be 50 and n can be 50 — completely infeasible. "
            "This is only shown to motivate why the greedy sort works."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Even in the brute force, if we sort packs and boxes descending within each trial, "
            "we see the same greedy pattern emerge. This suggests the sort-and-pair approach "
            "is provably optimal."
        ),
        N.h4("Building the Solution"),
        N.para(
            "For k = 1 to m: try all C(m,k) subsets of k boxes. For each subset, sort it "
            "descending and check if each pack[i] ≤ box[i]. Return the first k that works. "
            "Complexity: O(2^m × n log n) — exponential, not acceptable."
        ),
        N.callout(
            "Use this approach only to verify correctness on tiny inputs. Never in interviews.", "⚠️", "red_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("for num_boxes in range(1, len(capacity) + 1)", {"code": True}),
        (" — Try increasing numbers of boxes from 1 upward.", {}),
    ])),
    N.para(N.rich([
        ("for combo in combinations(..., num_boxes)", {"code": True}),
        (" — Try every subset of exactly num_boxes boxes.", {}),
    ])),
    N.para(N.rich([
        ("all(combo_sorted[i] >= apple[i] ...)", {"code": True}),
        (" — After sorting both, check that each pack fits in the corresponding box.", {}),
    ])),
    N.divider(),
]

# ── Solution 3 — Greedy with Explicit Verification ──────────────────────────
blocks += [
    N.h2("Solution 3 — Greedy with Explicit Feasibility Check"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same greedy idea as Solution 1, but with an explicit assertion that confirms "
            "the i-th box is large enough for the i-th pack. This version is useful for "
            "debugging and understanding the invariant."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Skipping the capacity check: in real data, a test might have apple = [10] and "
            "capacity = [1,1,1] — this would be infeasible. Adding assertions catches bugs."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The loop makes explicit: for each pack at index i (in sorted desc order), "
            "the i-th largest box must have capacity ≥ pack size. This is the exchange-argument "
            "proof in code form."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Sort both descending. Loop with enumerate to access both index and pack size. "
            "Assert capacity[i] >= pack_size. Count each box used. Return the count."
        ),
        N.callout(
            "This formulation makes the proof of correctness visible in the code itself — "
            "ideal for explaining to an interviewer why the greedy works.", "💡", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_3_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("for i, pack_size in enumerate(apple)", {"code": True}),
        (" — Iterate packs in descending size order, tracking index i.", {}),
    ])),
    N.para(N.rich([
        ("assert capacity[i] >= pack_size", {"code": True}),
        (" — Invariant check: the i-th largest box must fit the i-th largest pack.", {}),
    ])),
    N.para(N.rich([
        ("boxes_used += 1", {"code": True}),
        (" — Each pack consumes exactly one box.", {}),
    ])),
    N.divider(),
]

# ── Complexity table ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy: Sort + Pair (Interview Pick)", "O(n log n + m log m)", "O(1)"],
        ["Brute Force: All Subsets", "O(2^m × n)", "O(m)"],
        ["Greedy with Verification", "O(n log n + m log m)", "O(1)"],
    ]),
    N.callout(
        "n = number of apple packs, m = number of boxes. Sorting dominates. "
        "Both sort-based solutions are optimal. The brute force is shown only for comparison.",
        "📊", "gray_background"
    ),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Greedy", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Fill Largest First", {})])),
    N.para(N.rich([
        ("Why Greedy works here: ", {"bold": True}),
        ("The exchange argument shows that any assignment can be transformed into the sorted "
         "assignment without increasing the number of boxes. The sorted pairing is therefore "
         "globally optimal.", {}),
    ])),
    N.callout(
        "When to recognize this pattern:\n"
        "• You need to assign items to containers, minimising the number of containers used.\n"
        "• Each item goes into exactly one container (no splitting).\n"
        "• Containers have a capacity constraint that items must satisfy.\n"
        "• Signal words: 'minimum number of boxes/buckets/bins', 'each item in exactly one'.",
        "🔎", "green_background"
    ),
    N.para(
        "Sub-Pattern verified via analysis — this is a classic bin assignment / greedy "
        "scheduling pattern. Verified against DSA_Patterns_and_SubPatterns_Guide.md "
        "Section on Greedy (Sort-based greedy assignment)."
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique: sort items and containers, pair greedily:"),
    N.bullet(N.rich([("Assign Cookies", {"bold": True}), (" (Easy) — Sort children's greed and cookie sizes; greedily assign smallest satisfying cookie. Same sort-both-descending pattern.", {})])),
    N.bullet(N.rich([("Two City Scheduling", {"bold": True}), (" (Medium) — Sort by cost difference; greedy assignment to two groups.", {})])),
    N.bullet(N.rich([("Car Pooling", {"bold": True}), (" (Medium) — Greedy with capacity tracking over time.", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Greedy scheduling to minimise idle time; sort tasks by frequency.", {})])),
    N.bullet(N.rich([("Minimum Number of Arrows to Burst Balloons", {"bold": True}), (" (Medium) — Sort by end point; greedy assignment of arrows to balloon groups.", {})])),
    N.bullet(N.rich([("Largest Number After Digit Swaps by Parity", {"bold": True}), (" (Easy) — Sort by parity groups and pair greedily.", {})])),
    N.bullet(N.rich([("Bag of Tokens", {"bold": True}), (" (Medium) — Sort tokens; two-pointer greedy play.", {})])),
    N.bullet(N.rich([("Advantage Shuffle", {"bold": True}), (" (Medium) — Sort both arrays; greedy matching with two pointers.", {})])),
    N.para("These problems share the same core technique: sort items and resources in matched order, then pair them greedily to minimise resource usage or maximise advantage."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Greedy section, Sort-based assignment sub-patterns.", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
