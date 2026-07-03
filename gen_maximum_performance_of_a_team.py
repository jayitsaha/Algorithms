"""gen_maximum_performance_of_a_team.py — Notion in-place update for LeetCode #1383."""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-819d-8545-e2e2c370e608"
SLUG = "maximum_performance_of_a_team"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1383,
    pattern="Heaps",
    subpatterns=["Sort + Min Heap for K Max"],
    tc="O(n log n)",
    sc="O(k)",
    key_insight="Sort by efficiency desc; current engineer is always min_eff. Min-heap of size k holds top-k speeds. candidate = sum_speed × eff.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build new body ─────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given two integers arrays ", {}),
        ("speed", {"code": True}),
        (" and ", {}),
        ("efficiency", {"code": True}),
        (", both of length ", {}),
        ("n", {"code": True}),
        (", and an integer ", {}),
        ("k", {"code": True}),
        (". Choose at most ", {}),
        ("k", {"code": True}),
        (" engineers to form a team. The team's performance is defined as:\n\nperformance = (sum of engineers' speeds) × (minimum of engineers' efficiencies)\n\nReturn the maximum performance of this team (modulo 10⁹ + 7).", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Sort + Min-Heap (Optimal) ─────────────────────────────────────
sol1_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("We want to maximize (sum of speeds) × (min efficiency). The min creates a tension: adding more engineers raises sum_speed but risks dropping min_eff. The key question: can we fix which engineer provides the minimum efficiency?"),

    N.h4("What Doesn't Work"),
    N.para("A naive brute force tries every combination of up to k engineers from n: that's C(n,k) combinations, which is astronomically large for n=10⁵, k=50000. Even the smarter brute force (try each engineer as the min-eff bottleneck, then pick k fastest from eligible) is O(n² log n) — still too slow."),

    N.h4("The Key Observation"),
    N.para("In any valid team, exactly one engineer has the minimum efficiency. If we enumerate who that bottleneck engineer is, the optimal strategy for the rest of the team is simple: pick the k−1 fastest engineers whose efficiency is ≥ the bottleneck's. This turns the problem into: for each possible min_eff value, what is the best sum_speed we can achieve?"),

    N.h4("Building the Solution"),
    N.para("Sort engineers by efficiency descending. Now as we scan left to right, the current engineer's efficiency is ≤ all previously processed engineers' efficiencies — making them the natural minimum. We just need to track the k fastest speeds seen so far: a min-heap of size k does this in O(log k) per step. Push each new speed, evict the minimum if we exceed k. At each step, compute candidate = sum_speed × current_eff and update the global max."),

    N.callout(
        "Analogy: Hiring a team with a group efficiency rating. The group rating is dragged down by the least-efficient person. Sort candidates from most efficient to least. For each 'weakest link' candidate, greedily pick the k−1 fastest colleagues with better credentials.",
        "🧠", "blue_background"
    ),
]

sol1_code = """import heapq
MOD = 10**9 + 7

def maxPerformance(n, speed, efficiency, k):
    # Pair (efficiency, speed) and sort by efficiency descending
    # So current engineer is always the min efficiency
    eng = sorted(zip(efficiency, speed), reverse=True)

    heap = []       # min-heap tracking up to k fastest speeds
    sum_speed = 0   # running total of speeds in heap
    ans = 0         # global maximum performance

    for eff, spd in eng:
        heapq.heappush(heap, spd)   # add this speed
        sum_speed += spd

        if len(heap) > k:
            # Evict slowest: pop minimum from heap
            sum_speed -= heapq.heappop(heap)

        # eff is guaranteed to be min_efficiency (sorted desc)
        ans = max(ans, sum_speed * eff)

    return ans % MOD"""

blocks += [
    N.h2("Solution 1 — Sort + Min-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol1_intuition_children),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("eng = sorted(zip(efficiency, speed), reverse=True)", {"code": True}), (" — Zip efficiency and speed into pairs, sort by efficiency descending. The current engineer at each step will be the minimum efficiency in any team drawn from processed engineers.", {})])),
    N.para(N.rich([("heap = []", {"code": True}), (" — Min-heap. Python's heapq is a min-heap by default — the smallest speed is always at the top.", {})])),
    N.para(N.rich([("sum_speed = 0", {"code": True}), (" — Running sum of speeds currently in the heap.", {})])),
    N.para(N.rich([("ans = 0", {"code": True}), (" — Global maximum performance. Initialize to 0 (performance is always non-negative).", {})])),
    N.para(N.rich([("for eff, spd in eng:", {"code": True}), (" — Enumerate each engineer in efficiency-descending order. eff is the current minimum efficiency by invariant.", {})])),
    N.para(N.rich([("heapq.heappush(heap, spd)", {"code": True}), (" — Add this engineer's speed to the heap. O(log k) operation.", {})])),
    N.para(N.rich([("sum_speed += spd", {"code": True}), (" — Include their speed in the running total before possible eviction.", {})])),
    N.para(N.rich([("if len(heap) > k:", {"code": True}), (" — Check if we've exceeded the team size limit.", {})])),
    N.para(N.rich([("sum_speed -= heapq.heappop(heap)", {"code": True}), (" — Evict the slowest engineer (heap minimum). This keeps only the k fastest candidates in O(log k).", {})])),
    N.para(N.rich([("ans = max(ans, sum_speed * eff)", {"code": True}), (" — Current eff is the minimum by construction. Evaluate this team's performance and update the global max.", {})])),
    N.para(N.rich([("return ans % MOD", {"code": True}), (" — Apply modulo AFTER finding the true maximum. Never apply modulo inside max() comparisons — it breaks ordering.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ────────────────────────────────────────────────────
sol2_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("Try every possible minimum efficiency. For each engineer as the designated 'weakest link', collect all engineers with equal or higher efficiency and take the k fastest."),

    N.h4("What Doesn't Work at Scale"),
    N.para("This approach is O(n²) iterations × O(n log n) sorting per iteration = O(n² log n). For n=10⁵ that's ~10¹⁰ operations — time limit exceeded. Useful for testing and understanding the structure."),

    N.h4("The Key Observation"),
    N.para("The brute force correctly identifies the structure: for each candidate minimum efficiency, pick top-k speeds from eligible engineers. The optimal approach just does this more efficiently by sorting once and using a heap."),
]

sol2_code = """def maxPerformance_brute(n, speed, efficiency, k):
    ans = 0
    for i in range(n):
        min_eff = efficiency[i]  # engineer i is the bottleneck
        # Collect speeds of all engineers with eff >= min_eff
        eligible = sorted([speed[j] for j in range(n)
                           if efficiency[j] >= min_eff], reverse=True)
        # Take top k speeds
        perf = sum(eligible[:k]) * min_eff
        ans = max(ans, perf)
    return ans % (10**9 + 7)"""

blocks += [
    N.h2("Solution 2 — Brute Force (Understanding Only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol2_intuition_children),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — Try every engineer as the minimum-efficiency bottleneck.", {})])),
    N.para(N.rich([("eligible = sorted([...], reverse=True)", {"code": True}), (" — Collect all engineers with efficiency ≥ threshold, sort by speed descending.", {})])),
    N.para(N.rich([("sum(eligible[:k]) * min_eff", {"code": True}), (" — Sum the top-k speeds × the fixed minimum efficiency.", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n² log n)", "O(n)"],
        ["Sort + Min-Heap (optimal)", "O(n log n)", "O(k)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Min Heap for K Max", {})])),
    N.callout(
        "When to recognize this pattern: objective = (sum of one attribute) × (min/max of another); must choose subset ≤ k; two-attribute optimization where fixing one by sorting lets you greedily optimize the other with a heap.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("IPO", {"bold": True}), (" (Hard) — Sort by capital, max-heap on profits to pick k most profitable projects (#502)", {})])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), (" (Easy) — Min-heap of size k; heap top = kth largest (#703)", {})])),
    N.bullet(N.rich([("K Closest Points to Origin", {"bold": True}), (" (Medium) — Max-heap of size k; evict farthest to maintain k closest (#973)", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Max-heap drives greedy scheduling with cooldown (#621)", {})])),
    N.bullet(N.rich([("Furthest Building You Can Reach", {"bold": True}), (" (Medium) — Min-heap tracks where to use expensive ladders vs bricks (#1642)", {})])),
    N.bullet(N.rich([("Single-Threaded CPU", {"bold": True}), (" (Medium) — Sort by arrival time, min-heap on processing time (#1834)", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Two heaps (max-heap left + min-heap right) to maintain median (#295)", {})])),
    N.para("These problems share the core technique: a heap of bounded size k efficiently maintains the best k elements while processing a sorted or streamed input."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heap Patterns section. Sub-Pattern: Sort + Min Heap for K Max.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
