"""
Notion regeneration for LeetCode #857 — Minimum Cost to Hire K Workers
Pattern: Greedy | Sub-pattern: Sort by Ratio + Heap
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8113-8e98-caa48eeaef01"

# 1) Set page properties
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=857,
    pattern="Greedy",
    subpatterns=["Sort by Ratio + Heap"],
    tc="O(n log n)",
    sc="O(n + k)",
    key_insight="Sort workers by wage/quality ratio; the worker with max ratio sets the rate. Sweep with a max-heap of size k to keep the k smallest qualities — minimizing cost at each captain.",
    icon="🔴"
)
print("Properties set.")

# 2) Wipe existing body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Build body
SOLUTION_1 = """\
import heapq

def mincostToHireWorkers(quality, wage, k):
    workers = sorted(
        (wage[i] / quality[i], quality[i])
        for i in range(len(quality))
    )
    heap = []
    quality_sum = 0
    ans = float('inf')
    for ratio, q in workers:
        heapq.heappush(heap, -q)
        quality_sum += q
        if len(heap) > k:
            quality_sum += heapq.heappop(heap)
        if len(heap) == k:
            ans = min(ans, ratio * quality_sum)
    return ans"""

SOLUTION_2 = """\
from itertools import combinations

def mincostToHireWorkers_brute(quality, wage, k):
    ans = float('inf')
    for group in combinations(range(len(quality)), k):
        rate = max(wage[i]/quality[i] for i in group)
        cost = rate * sum(quality[i] for i in group)
        ans = min(ans, cost)
    return ans"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There are ", {}),
        ("n", {"code": True}),
        (" workers. Each worker ", {}),
        ("i", {"code": True}),
        (" has a quality ", {}),
        ("quality[i]", {"code": True}),
        (" and a minimum wage expectation ", {}),
        ("wage[i]", {"code": True}),
        (". We want to hire exactly ", {}),
        ("k", {"code": True}),
        (" workers subject to two rules: (1) Pay is proportional to quality — all workers share the same rate ", {}),
        ("r", {"code": True}),
        (" so ", {}),
        ("pay[i] = r × quality[i]", {"code": True}),
        (". (2) No worker is paid below their minimum wage: ", {}),
        ("pay[i] ≥ wage[i]", {"code": True}),
        (". Find the minimum total cost.", {}),
    ])),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — Sort by Ratio + Max-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("All workers share a rate r. Rule 2 says r ≥ wage[i]/quality[i] for every hired worker. So r must equal the maximum ratio in the group. The worker with the max ratio is the 'captain' — they set the rate. Total cost = r × Σquality. To minimize cost, for each possible captain, pick the k workers with smallest total quality from those with ratio ≤ captain's ratio."),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries all C(n,k) groups — exponential for large n. Sorting by quality alone doesn't help: a low-quality worker can demand a high ratio and force an expensive rate on everyone."),
        N.h4("The Key Observation"),
        N.para("If workers are sorted by ratio, then when we process worker i as captain, every worker to their left has a lower ratio and will accept the captain's rate. We just need the k workers with minimum total quality from the prefix [0..i]. A max-heap of size k maintains this dynamically."),
        N.h4("Building the Solution"),
        N.para("Sort by ratio. Sweep left to right. Add each worker's quality to a max-heap. If heap size exceeds k, evict the largest quality (most expensive). When heap size == k, compute cost = ratio × quality_sum. Track minimum. One pass, O(n log k) with O(n log n) sorting."),
        N.callout(
            "Analogy: You're hiring freelancers. The most expensive (highest rate) freelancer sets the billing rate for the whole team. To cut costs: sort by billing rate, and for each possible 'lead', keep only the k team members with the smallest workload (quality). Smaller workload × same rate = lower bill.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1),
    N.h3("Line by Line"),
    N.para(N.rich([("workers = sorted((w/q, q) for ...)", {"code": True}), (" — Build (ratio, quality) pairs and sort ascending by ratio. Sorting is the key greedy enabler.", {})])),
    N.para(N.rich([("heap = []; quality_sum = 0; ans = float('inf')", {"code": True}), (" — Max-heap (via negation), running quality sum, and best-answer tracker.", {})])),
    N.para(N.rich([("for ratio, q in workers:", {"code": True}), (" — Each iteration treats the current worker as the captain. All previous workers have lower ratios and accept the captain's rate.", {})])),
    N.para(N.rich([("heapq.heappush(heap, -q)", {"code": True}), (" — Push negated quality. The min-heap root becomes the most-negative = largest quality = next to evict.", {})])),
    N.para(N.rich([("quality_sum += q", {"code": True}), (" — Update running sum of qualities in the heap.", {})])),
    N.para(N.rich([("if len(heap) > k: quality_sum += heapq.heappop(heap)", {"code": True}), (" — Evict the largest quality. heappop returns -max_q; adding it to quality_sum subtracts max_q. One line, two operations.", {})])),
    N.para(N.rich([("if len(heap) == k: ans = min(ans, ratio * quality_sum)", {"code": True}), (" — Full group: cost = captain's ratio × total quality. Update minimum.", {})])),
    N.para(N.rich([("return ans", {"code": True}), (" — The minimum cost across all valid k-worker groups.", {})])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — Brute Force (Exponential, for understanding)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible group of k workers. For each group, the captain is the worker with the highest wage/quality ratio. The total cost = that ratio × sum of qualities in the group."),
        N.h4("What Doesn't Work"),
        N.para("This runs in O(C(n,k) × k) time — exponential for n=10,000. Correct but useless in practice."),
        N.h4("The Key Observation"),
        N.para("Useful for understanding the formula and verifying the greedy solution on small test cases. In interviews, mention this first to show you understood the problem, then propose the optimal approach."),
        N.h4("Building the Solution"),
        N.para("Use itertools.combinations to enumerate all groups. For each group compute max ratio (captain) and sum of qualities, then compute and track minimum total cost."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2),
    N.h3("Line by Line"),
    N.para(N.rich([("for group in combinations(range(n), k):", {"code": True}), (" — Enumerate every subset of k workers from n total.", {})])),
    N.para(N.rich([("rate = max(wage[i]/quality[i] for i in group)", {"code": True}), (" — Captain's ratio = max ratio in the group = minimum valid rate.", {})])),
    N.para(N.rich([("cost = rate * sum(quality[i] for i in group)", {"code": True}), (" — Total cost = rate × total quality of the group.", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all C(n,k) groups)", "O(C(n,k) × k)", "O(k)"],
        ["Sort + Max-Heap (optimal)", "O(n log n)", "O(n + k)"],
    ]),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Greedy", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort by Ratio + Heap", {})])),
    N.callout(
        "When to recognize this pattern: 'pick k out of n' where total cost = (worst element's rate) × (sum of elements). One element sets a ceiling that determines everyone else's payment. Sorting by the ceiling metric + max-heap of size k = classic greedy. Keywords: proportional, ratio, hire group, minimum rate, k workers.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sort by Ratio + Heap technique:"),
    N.bullet(N.rich([("IPO (Maximize Capital)", {"bold": True}), (" (Hard) — Greedy with two heaps; pick highest-profit affordable project each round. Same idea: sort by threshold, pick best from eligible set. (#502)", {})])),
    N.bullet(N.rich([("K Closest Points to Origin", {"bold": True}), (" (Medium) — Max-heap of size k to maintain k-smallest distances dynamically. (#973)", {})])),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium) — Min-heap of size k or quickselect to find kth largest. (#215)", {})])),
    N.bullet(N.rich([("Find K Pairs with Smallest Sums", {"bold": True}), (" (Medium) — Heap-based enumeration of k-best pairs from two sorted arrays. (#373)", {})])),
    N.bullet(N.rich([("Minimum Number of Refueling Stops", {"bold": True}), (" (Hard) — Greedy + max-heap; always pick the best fuel stop seen so far when running out of gas. (#871)", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Greedy scheduling with priority queue to minimize idle time. (#621)", {})])),
    N.para("These problems share the core technique: sort or filter by a threshold/ratio, then use a heap to dynamically maintain the optimal k-element subset."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Greedy section. Sub-Pattern: Sort by Ratio + Heap. Source: Analysis (not explicitly listed in guide under this exact name).", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_cost_to_hire_k_workers")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# Append in chunks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
