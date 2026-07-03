"""
gen_find_the_duplicate_number.py
LeetCode #287 — Find the Duplicate Number
Pattern: Math / Floyd's Cycle Detection
Notion page update (in-place).
"""
import notion_lib as N

PAGE_ID = "39193418-809c-816b-8d82-dfd1ce8fb04d"

# ──────────────────────────────────────────────────────────
# Step 1 — Properties
# ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=287,
    pattern="Math",
    subpatterns=["Floyd Cycle Detection"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Treat the array as a linked list; value at index is the 'next' pointer. The duplicate creates a cycle, and Floyd's algorithm finds the cycle entry = the duplicate.",
    icon="🟡",
)
print("Properties OK")

# ──────────────────────────────────────────────────────────
# Step 2 — Wipe old body
# ──────────────────────────────────────────────────────────
print("Wiping old page body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {n_deleted} blocks")

# ──────────────────────────────────────────────────────────
# Step 3 — Rebuild body
# ──────────────────────────────────────────────────────────

# ── PROBLEM ────────────────────────────────────────────────
blocks = []
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array ", {}),
        ("nums", {"code": True}),
        (" of ", {}),
        ("n + 1", {"code": True}),
        (" integers where each integer is in the range ", {}),
        ("[1, n]", {"code": True}),
        (" inclusive, there is exactly one repeated number. Return that duplicate without modifying the array and using only O(1) extra space.", {}),
    ])),
    N.callout(
        N.rich([
            ("Constraints: ", {"bold": True}),
            ("You cannot modify ", {}),
            ("nums", {"code": True}),
            (". Must use O(1) extra space. Must be O(n) time. 1 ≤ n ≤ 10⁵.", {}),
        ]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── SOLUTION 1 — Floyd's Cycle Detection (INTERVIEW PICK) ──
blocks += [
    N.h2("Solution 1 — Floyd's Cycle Detection (Interview Pick)"),

    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Imagine each array value as a 'next pointer'. Index i points to nums[i]. "
            "So starting at index 0, we follow: 0 → nums[0] → nums[nums[0]] → … "
            "This forms a sequence through indices. Since nums has n+1 elements all in [1,n], "
            "every value is a valid index — the sequence never falls off the array. "
            "The duplicate value means two different indices both point to the same 'next' node — "
            "that's the definition of a cycle entry in a linked list."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Sorting takes O(n log n) and needs to modify the array. "
            "A hash set finds duplicates in O(n) time but uses O(n) space — violates constraints. "
            "Marking visited by negating values modifies the array — also forbidden. "
            "Binary search on the answer runs in O(n log n) (covered in Solution 2) but Floyd's is cleaner."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The array [1, 3, 4, 2, 2] defines this chain of jumps: "
            "0→1→3→2→4→2→4→2→… (the 2 keeps repeating). "
            "Notice we've entered a loop at index 2. The duplicate (the value 2) is EXACTLY "
            "the index where the cycle begins. Floyd's tortoise-and-hare algorithm was invented "
            "precisely to detect cycle entry points in O(n) time and O(1) space."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Phase 1 — Find the intersection: start slow and fast both at index 0. "
            "Move slow one step (slow = nums[slow]), fast two steps (fast = nums[nums[fast]]). "
            "When they meet, they're inside the cycle.\n\n"
            "Phase 2 — Find the cycle entry: reset one pointer to 0, keep the other at the meeting point. "
            "Move both one step at a time. Where they meet again is the cycle entry = the duplicate."
        ),
        N.callout(
            "Analogy: Two runners on a circular track. The fast runner laps the slow one inside the loop. "
            "Once they meet, send a third runner from the start at the same speed as the slow runner — "
            "they meet exactly at the loop's entrance.",
            "🏃", "blue_background"
        ),
    ]),

    N.h3("🔬 Algorithm Deep-Dive: Floyd's Cycle Detection"),
    N.para(
        "Floyd's Tortoise and Hare algorithm, invented by Robert W. Floyd in 1967, detects cycles "
        "in sequences of the form xᵢ₊₁ = f(xᵢ) using only two pointers and O(1) space.\n\n"
        "Core invariant: If a cycle of length λ exists starting at position μ steps from the origin, "
        "the two pointers will meet at position μ + k·λ for some integer k ≥ 1 — always inside the cycle.\n\n"
        "Why Phase 2 finds the entry: Let μ = distance from start to cycle entry, λ = cycle length, "
        "and C = meeting point inside cycle. At meeting point, slow has taken μ + λ - r steps "
        "(where r is remainder). Setting one pointer to 0 and advancing both at speed 1: "
        "the pointer from 0 takes μ steps to reach entry; the pointer inside the cycle also travels "
        "exactly μ more steps to wrap to the entry. They meet at position μ — the cycle entry.\n\n"
        "When to recognize: 'Find duplicate in array of size n+1 with values in [1,n]', "
        "'Linked list cycle detection', 'Find start of loop in sequence'."
    ),
    N.code(
        "# Floyd's Cycle Detection Template\n"
        "def find_cycle_entry(head):\n"
        "    slow = fast = head\n"
        "    # Phase 1: find intersection\n"
        "    while True:\n"
        "        slow = slow.next\n"
        "        fast = fast.next.next\n"
        "        if slow == fast:\n"
        "            break\n"
        "    # Phase 2: find entry\n"
        "    start = head\n"
        "    while start != slow:\n"
        "        start = start.next\n"
        "        slow = slow.next\n"
        "    return start  # cycle entry = duplicate value"
    ),

    N.h3("Code"),
    N.code(
        "def findDuplicate(nums: list[int]) -> int:\n"
        "    # Phase 1: Detect intersection inside the cycle\n"
        "    slow = nums[0]\n"
        "    fast = nums[nums[0]]\n"
        "    while slow != fast:\n"
        "        slow = nums[slow]          # one step\n"
        "        fast = nums[nums[fast]]    # two steps\n"
        "\n"
        "    # Phase 2: Find cycle entry = duplicate\n"
        "    slow = 0\n"
        "    while slow != fast:\n"
        "        slow = nums[slow]\n"
        "        fast = nums[fast]\n"
        "    return slow"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("slow = nums[0]", {"code": True}), " — Tortoise starts at nums[0] (first jump from index 0)."])  ),
    N.para(N.rich([("fast = nums[nums[0]]", {"code": True}), " — Hare starts two jumps ahead."])  ),
    N.para(N.rich([("while slow != fast:", {"code": True}), " — Keep moving until the two pointers collide inside the cycle."])  ),
    N.para(N.rich([("slow = nums[slow]", {"code": True}), " — Tortoise: one step (follow the 'next pointer')."])  ),
    N.para(N.rich([("fast = nums[nums[fast]]", {"code": True}), " — Hare: two steps in one line."])  ),
    N.para(N.rich([("slow = 0", {"code": True}), " — Phase 2: reset tortoise to the START of the sequence (index 0)."])  ),
    N.para(N.rich([("while slow != fast:", {"code": True}), " — Now both move one step at a time from their respective positions."])  ),
    N.para(N.rich([("slow = nums[slow]; fast = nums[fast]", {"code": True}), " — They advance in sync; due to cycle math, they meet at the duplicate."])  ),
    N.para(N.rich([("return slow", {"code": True}), " — The meeting point in Phase 2 is the cycle entry = the duplicate number."])  ),
    N.divider(),
]

# ── SOLUTION 2 — Binary Search on Answer ───────────────────
blocks += [
    N.h2("Solution 2 — Binary Search on Value Range"),

    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of searching in the array by index, search for the duplicate VALUE. "
            "The duplicate is some integer in [1, n]. Can we binary search on this range?"
        ),
        N.h4("The Key Observation"),
        N.para(
            "Pigeonhole principle: if we count how many elements in nums are ≤ mid, "
            "and that count > mid, then the duplicate must be in [1, mid] (more values "
            "than slots). Otherwise it's in [mid+1, n]. This is O(n) per binary search "
            "step, and we do O(log n) steps → O(n log n) overall. Still O(1) space."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Binary search lo=1, hi=n. At each mid, count elements ≤ mid. "
            "If count > mid → duplicate is ≤ mid → hi = mid. "
            "Else → duplicate is > mid → lo = mid + 1."
        ),
    ]),

    N.h3("Code"),
    N.code(
        "def findDuplicate(nums: list[int]) -> int:\n"
        "    lo, hi = 1, len(nums) - 1\n"
        "    while lo < hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        count = sum(1 for x in nums if x <= mid)\n"
        "        if count > mid:   # too many values ≤ mid → duplicate is low\n"
        "            hi = mid\n"
        "        else:\n"
        "            lo = mid + 1\n"
        "    return lo"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 1, len(nums) - 1", {"code": True}), " — Search range is the value domain [1, n]."])  ),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), " — Midpoint value (not index)."])  ),
    N.para(N.rich([("count = sum(1 for x in nums if x <= mid)", {"code": True}), " — Count values ≤ mid in O(n)."])  ),
    N.para(N.rich([("if count > mid: hi = mid", {"code": True}), " — Pigeonhole: too many values in lower half → duplicate is there."])  ),
    N.para(N.rich([("else: lo = mid + 1", {"code": True}), " — Duplicate must be in upper half."])  ),
    N.para(N.rich([("return lo", {"code": True}), " — When lo == hi, that value is the duplicate."])  ),
    N.divider(),
]

# ── SOLUTION 3 — Brute Force (educational baseline) ────────
blocks += [
    N.h2("Solution 3 — Brute Force (Hash Set)"),

    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Simple approach: keep a set of seen numbers; the first repeat is the answer."),
        N.h4("Why It Fails Here"),
        N.para("Uses O(n) extra space — violates the problem constraints. Valid for interviews where space is not constrained."),
    ]),

    N.h3("Code"),
    N.code(
        "def findDuplicate(nums: list[int]) -> int:\n"
        "    seen = set()\n"
        "    for num in nums:\n"
        "        if num in seen:\n"
        "            return num\n"
        "        seen.add(num)\n"
        "    return -1  # unreachable given valid input"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("seen = set()", {"code": True}), " — Track all numbers encountered so far."])  ),
    N.para(N.rich([("if num in seen:", {"code": True}), " — O(1) lookup. First number seen twice is the duplicate."])  ),
    N.para(N.rich([("seen.add(num)", {"code": True}), " — Record this number for future lookups."])  ),
    N.divider(),
]

# ── COMPLEXITY TABLE ───────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Floyd's Cycle Detection", "O(n)", "O(1)"],
        ["Binary Search on Value", "O(n log n)", "O(1)"],
        ["Hash Set (Brute Force)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ─────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Math", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Floyd Cycle Detection", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("Array of size n+1 with values in [1,n] and exactly one duplicate. "
             "Must be O(1) space and O(n) time. Treating array indices as linked list 'next pointers' "
             "reveals a cycle whose entry is the duplicate. Also look for: 'find start of loop', "
             "'detect cycle in sequence', 'linked list cycle II'.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── RELATED PROBLEMS ──────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Linked List Cycle II", {"bold": True}), " (Medium) — Direct Floyd's application on actual linked list; find the node where cycle begins."])),
    N.bullet(N.rich([("Linked List Cycle", {"bold": True}), " (Easy) — Floyd's Phase 1 only; just detect if a cycle exists."])),
    N.bullet(N.rich([("Find the Missing Number", {"bold": True}), " (Easy) — Complement problem: cyclic sort or XOR to find the gap in [0,n]."])),
    N.bullet(N.rich([("Set Mismatch", {"bold": True}), " (Easy) — Find both the duplicate and the missing number using Floyd's or XOR."])),
    N.bullet(N.rich([("First Missing Positive", {"bold": True}), " (Hard) — Cyclic sort variant to place values at correct indices then scan for gap."])),
    N.bullet(N.rich([("Happy Number", {"bold": True}), " (Easy) — Floyd's detects whether a sequence of digit-square-sums cycles (non-happy) or reaches 1."])),
    N.bullet(N.rich([("Find All Duplicates in an Array", {"bold": True}), " (Medium) — Negation trick (modifies array) to detect duplicates — same constraints family."])),
    N.bullet(N.rich([("Number of Connected Components in an Undirected Graph", {"bold": True}), " (Medium) — Union-Find cycle detection, different mechanism but same 'cycle = duplicate' intuition."])),
    N.para("These problems share the core insight: model the array as a function f(i) = nums[i] and detect structure (cycles, missing entries) in that function."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math / Floyd Cycle Detection", "📚", "gray_background"),
    N.divider(),
]

# ── VISUAL EXPLAINER EMBED ─────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_the_duplicate_number")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── APPEND ALL BLOCKS ─────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
