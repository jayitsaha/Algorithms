"""
gen_range_addition.py — Notion rebuild for Range Addition (LeetCode #370)
Difference Array sub-pattern, Medium difficulty.
"""
import notion_lib as N

PAGE_ID = "39193418-809c-818e-9fd8-de103e4b575c"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=370,
    pattern="Prefix Sum",
    subpatterns=["Difference Array"],
    tc="O(n + k)",
    sc="O(n)",
    key_insight="Encode each range update as two O(1) diff-array writes; one prefix-sum pass reconstructs all values.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────
BRUTE_CODE = """\
def getModifiedArray_brute(n: int, updates: list) -> list:
    result = [0] * n
    for start, end, inc in updates:      # for each operation...
        for i in range(start, end + 1):  # ...update every element in range -- O(n) per op
            result[i] += inc             # correct but slow; TLE when n=k=10^5
    return result"""

OPTIMAL_CODE = """\
def getModifiedArray(n: int, updates: list) -> list:
    diff = [0] * (n + 1)            # size n+1: guard slot absorbs diff[end+1] when end=n-1
    for start, end, inc in updates: # O(1) per operation
        diff[start] += inc          # mark: value rises by inc from this index
        diff[end + 1] -= inc        # cancel that rise one position past the end
    result, running = [], 0         # output list + prefix-sum accumulator
    for i in range(n):              # scan indices 0..n-1 only (skip guard)
        running += diff[i]          # absorb net change at position i
        result.append(running)      # running IS the final value at index i
    return result                   # Time O(n+k), Space O(n)"""

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "You are given an integer ", ("n", {"code": True}),
        " and a list of ", ("k", {"code": True}),
        " update operations. The array starts as all zeros. Each operation is a triple ",
        ("[startIndex, endIndex, inc]", {"code": True}),
        ": add ", ("inc", {"code": True}),
        " to every element from index ", ("startIndex", {"code": True}),
        " through ", ("endIndex", {"code": True}),
        " inclusive. Return the final array after all operations.\n\n"
        "Example: n=5, updates=[[1,3,2],[0,2,1],[2,4,3]] -> [1, 3, 6, 5, 3]\n\n"
        "Constraints: 1 <= n <= 10^5, 0 <= k <= 10^5, each operation has valid indices, "
        "inc can be any integer (positive or negative)."
    ])),
    N.divider(),
]

# ── Solution 1 — Difference Array (Interview Pick) ────────────────────────
blocks += [
    N.h2("Solution 1 -- Difference Array (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to apply k range-update operations on an array of zeros and return the final state. "
            "Each operation asks: 'add inc to every element between start and end.' "
            "The naive way is to literally loop through every element in the range -- but that's O(n) per operation."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "The brute force is O(n x k). For n = k = 10^5, that is 10^10 operations -- far too slow. "
            "The core redundancy: if we add the same delta to 1000 consecutive elements, we are writing "
            "the same value 1000 times. We are not gaining new information with each repeated write."
        ),
        N.h4("The Key Observation"),
        N.para(
            "When you add a constant to a range, the differences between adjacent elements only change "
            "at the two endpoints. Inside the range, every element changes by the same amount, so adjacent "
            "differences are zero. Outside, nothing changes. This means we can encode a range update with "
            "just two boundary marks instead of touching every element in between."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Create a difference array diff of size n+1, all zeros.\n"
            "2. For each operation [start, end, inc]: write diff[start] += inc (the change begins here) "
            "and diff[end+1] -= inc (the change cancels one past the end).\n"
            "3. After all operations, compute the prefix sum of diff[0..n-1]. "
            "The running total at each index i is the net effect of all operations covering i.\n"
            "4. Return the result array. Total: O(k) to encode + O(n) to decode = O(n+k)."
        ),
        N.callout(
            "Subway Analogy: Think of a subway line. Each operation is 'a passenger boards at stop A "
            "and exits at stop B.' Instead of counting every passenger on every segment, record +1 at A "
            "and -1 at B+1. One scan gives the load at each stop in O(n) total.",
            "🚇", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("diff = [0] * (n + 1)", {"code": True}),
        " -- Allocate n+1 zeros. The extra slot at index n is a guard that safely absorbs writes to "
        "diff[end+1] when end=n-1, avoiding any bounds check."
    ])),
    N.para(N.rich([
        ("for start, end, inc in updates:", {"code": True}),
        " -- Destructure each operation. We process all k operations in this single pass. O(1) work per operation."
    ])),
    N.para(N.rich([
        ("diff[start] += inc", {"code": True}),
        " -- Mark the start boundary: from this index onward, the running total rises by inc. "
        "This does not yet touch the result array."
    ])),
    N.para(N.rich([
        ("diff[end + 1] -= inc", {"code": True}),
        " -- Mark the end boundary: one past the last included index, cancel the rise. "
        "The cancellation is at end+1, NOT at end -- index end is still inside the range."
    ])),
    N.para(N.rich([
        ("result, running = [], 0", {"code": True}),
        " -- Initialize the output list and the prefix-sum accumulator to zero."
    ])),
    N.para(N.rich([
        ("for i in range(n):", {"code": True}),
        " -- Only iterate over indices 0..n-1. We deliberately skip the guard slot at index n."
    ])),
    N.para(N.rich([
        ("running += diff[i]", {"code": True}),
        " -- Absorb the net change stored at position i. running now holds the sum of all inc values "
        "from operations that cover index i."
    ])),
    N.para(N.rich([
        ("result.append(running)", {"code": True}),
        " -- running is the final value at index i. Append it to the output."
    ])),
    N.para(N.rich([
        ("return result", {"code": True}),
        " -- Return the completed array. Time O(n+k), Space O(n)."
    ])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 -- Brute Force (Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The most literal reading of the problem: for each operation, loop through the specified "
            "range and add inc to every element. This directly implements the problem statement."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This works correctly but is O(n x k) time. For large inputs (n = k = 10^5), "
            "it performs 10^10 iterations -- roughly 10 seconds at 10^9 ops/sec. "
            "LeetCode's time limit rejects this for the largest test cases. "
            "Use this as a reference to verify your optimized solution on small examples."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The brute force is valuable for: (a) verifying your optimized solution on small inputs, "
            "(b) communicating the naive baseline to the interviewer before improving it, "
            "(c) establishing that you understand what the problem is asking."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Initialize result = [0]*n. For each [start, end, inc], "
            "loop i from start to end inclusive and do result[i] += inc. Return result."
        ),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("result = [0] * n", {"code": True}),
        " -- Initialize the output array to all zeros."
    ])),
    N.para(N.rich([
        ("for start, end, inc in updates:", {"code": True}),
        " -- Process each of the k operations in sequence."
    ])),
    N.para(N.rich([
        ("for i in range(start, end + 1):", {"code": True}),
        " -- Loop over every index in the range [start, end] -- O(n) per operation in the worst case."
    ])),
    N.para(N.rich([
        ("result[i] += inc", {"code": True}),
        " -- Directly update the element. Correct but slow; leads to TLE."
    ])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n x k)", "O(n)", "TLE for large inputs"],
        ["Difference Array (Optimal)", "O(n + k)", "O(n)", "Interview pick; k O(1) encodes + one O(n) decode"],
        ["Segment Tree (lazy prop)", "O((n+k) log n)", "O(n)", "Needed for online queries; overkill here"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Prefix Sum (Array Manipulation)"])),
    N.para(N.rich([
        ("Sub-Pattern(s): ", {"bold": True}),
        "Difference Array -- encode range updates as two boundary marks; decode with a single prefix-sum pass."
    ])),
    N.callout(
        "When to recognize this pattern:\n"
        "  - 'Add a constant to all elements in a range' and you need the final array\n"
        "  - Multiple range-increment operations queried offline (after all ops complete)\n"
        "  - 'Passengers board at A, exit at B' or any problem with start/end events\n"
        "  - Range-updates are heavy, point-reads are light\n\n"
        "Source: DSA_Patterns_and_SubPatterns_Guide.md -- Section 1.3 (Prefix Sum / Difference Array)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same Difference Array technique:"),
    N.bullet(N.rich([
        ("Corporate Flight Bookings", {"bold": True}),
        " (Medium, #1109) -- Range addition on seat counts; identical difference-array setup."
    ])),
    N.bullet(N.rich([
        ("Car Pooling", {"bold": True}),
        " (Medium, #1094) -- Passengers board and alight at discrete stops; model as range +/-."
    ])),
    N.bullet(N.rich([
        ("Shifting Letters II", {"bold": True}),
        " (Medium, #2381) -- Range character-shift operations; accumulate shifts via difference array."
    ])),
    N.bullet(N.rich([
        ("Maximum Population Year", {"bold": True}),
        " (Easy, #1854) -- Count people alive per year; each person is a [birth, death-1] range add."
    ])),
    N.bullet(N.rich([
        ("Minimum Number of K Consecutive Bit Flips", {"bold": True}),
        " (Hard, #995) -- Difference array tracks 'currently flipped' state across sliding window."
    ])),
    N.bullet(N.rich([
        ("Range Sum Query -- Immutable", {"bold": True}),
        " (Easy, #303) -- Static prefix sum for fast range-sum queries; the conceptual dual of range updates."
    ])),
    N.bullet(N.rich([
        ("Subarray Sum Equals K", {"bold": True}),
        " (Medium, #560) -- Prefix sum with hash map for O(n) range-sum lookup."
    ])),
    N.para(
        "These problems share the core technique: encode sparse boundary events in O(1) per event, "
        "then recover the full array with a single O(n) prefix-sum pass."
    ),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.3 -- Prefix Sum / Difference Array",
        "📚", "gray_background"
    ),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for("range_addition")),
    N.para(N.rich([
        ("Step through the algorithm visually -- use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
