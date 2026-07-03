import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81fe-91b7-c55ecea387e0"

# 1) Properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1011,
    pattern="Binary Search",
    subpatterns=["BS on Answer"],
    tc="O(n log S)",
    sc="O(1)",
    key_insight="Binary-search the capacity value; greedy O(n) feasibility check is monotone.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe old body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Rebuild body
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("A conveyor belt has packages that must be shipped within ", {}),
        ("days", {"code": True}),
        (" days. Each day we ship a contiguous chunk of packages (in order), limited by the ship's weight ", {}),
        ("capacity", {"code": True}),
        (". Find the ", {}),
        ("minimum weight capacity", {"bold": True}),
        (" of the ship that will result in all packages being shipped within ", {}),
        ("days", {"code": True}),
        (" days.", {})
    ])),
    N.para(N.rich([
        ("Constraints: packages must be loaded in order, no reordering allowed. ", {}),
        ("weights[i]", {"code": True}),
        (" is the weight of the i-th package.", {})
    ])),
    N.callout(
        N.rich([("Example: weights=[1,2,3,4,5,6,7,8,9,10], days=5 → Answer: 15", {})]),
        "📦", "gray_background"
    ),
    N.divider()
]

# Solution 1
blocks += [
    N.h2("Solution 1 — Binary Search on Capacity (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the smallest capacity C such that all packages can be delivered in at most D days. This is a 'find minimum X satisfying a constraint' problem — the classic signal for binary search on the answer."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try every capacity from max(weights) to sum(weights). The range can be enormous (up to 500×500=250,000), and for each capacity we need O(n) to simulate. Total: O(n × S) — too slow for large inputs."),
        N.h4("The Key Observation"),
        N.para("Feasibility is monotone: if capacity C works (ships in ≤ D days), then any capacity C+1 also works. If C fails (needs > D days), any C-1 also fails. This [False...False...True...True] monotone structure is exactly what binary search requires."),
        N.h4("Building the Solution"),
        N.para("Binary-search the capacity value itself. For each candidate mid = (lo+hi)//2, run a greedy O(n) simulation: pack packages left-to-right, start new day when load would overflow. If days_needed ≤ D, try smaller (hi=mid); else go larger (lo=mid+1). Return lo when lo==hi."),
        N.callout(
            "Analogy: You're the shipping manager. You test different ship sizes by loading a trial cargo. If it fits in time, try a smaller ship. If it doesn't, rent a bigger one. Binary-search the ship size.",
            "🧠", "blue_background"
        )
    ])
]

# Code
blocks += [
    N.h3("Code"),
    N.code("""def shipWithinDays(weights: list, days: int) -> int:
    lo, hi = max(weights), sum(weights)  # search space: [must carry heaviest, carry all at once]
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(weights, days, mid):
            hi = mid       # mid works; try smaller
        else:
            lo = mid + 1   # mid too small; go larger
    return lo

def feasible(weights, days, capacity) -> bool:
    days_needed = 1
    current_load = 0
    for w in weights:
        if current_load + w > capacity:
            days_needed += 1
            current_load = 0
        current_load += w
    return days_needed <= days""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = max(weights), sum(weights)", {"code": True}), (" — lo is the minimum viable capacity (ship must carry the heaviest package); hi is the maximum needed (carry all in one day). Answer is in [lo, hi].", {})])),
    N.para(N.rich([("while lo < hi", {"code": True}), (" — continue until the search space collapses to one value, which is our answer.", {})])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — candidate capacity. Round down is essential for the 'find leftmost true' template to avoid infinite loops.", {})])),
    N.para(N.rich([("if feasible(...): hi = mid", {"code": True}), (" — mid works as a capacity; keep it as a candidate but try to find something smaller.", {})])),
    N.para(N.rich([("else: lo = mid + 1", {"code": True}), (" — mid definitely fails; the smallest possible valid capacity is at least mid+1.", {})])),
    N.para(N.rich([("return lo", {"code": True}), (" — when lo==hi, this is the minimum feasible capacity.", {})])),
    N.para(N.rich([("days_needed = 1; current_load = 0", {"code": True}), (" — initialize for greedy simulation. Always at least one day.", {})])),
    N.para(N.rich([("if current_load + w > capacity", {"code": True}), (" — this package would exceed today's ship capacity.", {})])),
    N.para(N.rich([("days_needed += 1; current_load = 0", {"code": True}), (" — start a new day and reset the load. Then fall through to load this package.", {})])),
    N.para(N.rich([("current_load += w", {"code": True}), (" — load the package (either on the reset new day or continuing the current day).", {})])),
    N.para(N.rich([("return days_needed <= days", {"code": True}), (" — True if we finished loading all packages within the allowed number of days.", {})])),
    N.divider()
]

# Solution 2 (brute force)
blocks += [
    N.h2("Solution 2 — Brute Force Linear Scan"),
    N.toggle_h3("💡 Intuition", [
        N.h4("Approach"),
        N.para("Try every integer capacity from max(weights) to sum(weights) in order. The first one that passes the feasibility check is the minimum. Correct but O(n × S) — too slow for the given constraints."),
    ]),
    N.h3("Code"),
    N.code("""def shipWithinDays_brute(weights, days):
    for capacity in range(max(weights), sum(weights) + 1):
        if feasible(weights, days, capacity):
            return capacity  # first feasible = minimum""", "python"),
    N.divider()
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (linear scan)", "O(n · S)", "O(1)"],
        ["Binary Search on Capacity ✓", "O(n log S)", "O(1)"]
    ]),
    N.para("S = sum(weights) − max(weights). For n=500 packages each of weight 500, Binary Search does ≈9,000 ops vs Brute Force's ≈125,000,000 ops."),
    N.divider()
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BS on Answer (Binary Search on Capacity / Parametric Search)", {})])),
    N.callout(
        "When to recognize this pattern: The problem asks for 'minimum X such that constraint Y is satisfied' or 'maximum X such that constraint holds.' The feasibility of X is monotone (if X works, X+1 also works in the same direction). Feasibility can be checked in O(n) time.",
        "🔎", "green_background"
    ),
    N.divider()
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 'BS on Answer' technique:"),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium) — Binary search eating speed; greedy: hours = sum(ceil(pile/speed)). Identical structure. (#875)", {})])),
    N.bullet(N.rich([("Split Array Largest Sum", {"bold": True}), (" (Hard) — Minimize max subarray sum over m parts; same BS + greedy feasibility. (#410)", {})])),
    N.bullet(N.rich([("Minimum Number of Days to Make m Bouquets", {"bold": True}), (" (Medium) — BS on day number; feasibility counts adjacent bloomed flowers. (#1482)", {})])),
    N.bullet(N.rich([("Find the Smallest Divisor Given a Threshold", {"bold": True}), (" (Medium) — BS on divisor; feasibility = sum of ceil(w/d) ≤ threshold. (#1283)", {})])),
    N.bullet(N.rich([("Magnetic Force Between Two Balls", {"bold": True}), (" (Medium) — Maximize minimum distance; BS on the distance value. (#1552)", {})])),
    N.bullet(N.rich([("Minimized Maximum of Products Distributed to Any Store", {"bold": True}), (" (Medium) — BS on max-per-store. (#2064)", {})])),
    N.para("These problems share the same core technique: binary search a numeric answer, verify feasibility with a greedy O(n) check."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9 (Binary Search), Sub-Pattern: BS on Answer", "📚", "gray_background"),
    N.divider()
]

# Embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("capacity_to_ship_packages_within_d_days")),
    N.para(N.rich([("Step through the binary search and greedy simulation visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
