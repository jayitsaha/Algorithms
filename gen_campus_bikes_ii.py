"""
gen_campus_bikes_ii.py — Notion regeneration for Campus Bikes II (LC #1066)
Bitmask DP: assign bikes to workers minimizing total Manhattan distance.
HTML is already good (919 lines, all markers) — Notion only.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8159-b508-c5047f6936d7"
SLUG = "campus_bikes_ii"

# ── 1. Properties ────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1066,
    pattern="Dynamic Programming",
    subpatterns=["Bitmask DP Min Distance"],
    tc="O(W × 2^B × B)",
    sc="O(2^B)",
    key_insight="Encode which bikes are taken as a bitmask; popcount(mask) reveals which worker is next — enabling 1D DP over 2^B states.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ─────────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3. Build new body ────────────────────────────────────────────────────────
blocks = []

# ── PROBLEM ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("On a campus represented as a 2D grid, there are ", {}),
        ("n", {"code": True}),
        (" workers and ", {}),
        ("m", {"code": True}),
        (" bikes, where ", {}),
        ("n ≤ m ≤ 10", {"code": True}),
        (". You are given two arrays ", {}),
        ("workers", {"code": True}),
        (" and ", {}),
        ("bikes", {"code": True}),
        (", each element a 2-element list ", {}),
        ("[x, y]", {"code": True}),
        (". Assign each worker exactly one bike such that no two workers share a bike, "
         "minimizing the sum of Manhattan distances between each worker and their assigned bike. "
         "Return this minimum total distance.", {}),
    ])),
    N.callout(
        N.rich([
            ("Constraints: ", {"bold": True}),
            ("n ≤ m ≤ 10, grid coordinates in [0, 1000]. Manhattan distance = |x1 - x2| + |y1 - y2|.", {}),
        ]),
        "📌", "gray_background"
    ),
    N.divider(),
]

# ── SOLUTION 1 — BOTTOM-UP BITMASK DP (Interview Pick) ───────────────────────
blocks += [
    N.h2("Solution 1 — Bitmask DP Bottom-Up (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need a one-to-one assignment: worker 0 gets one bike, worker 1 gets a different bike, and so on. "
            "The key question at each assignment step is: which bikes have already been claimed? "
            "That 'set of claimed bikes' is the core state we must track."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy fails: giving each worker their closest available bike can leave later workers stranded far away, "
            "producing a sub-optimal global sum. Brute-force permutations (m! orderings) are instructive but redundant — "
            "many orderings reach the same 'bikes taken' state without sharing computation."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Since m ≤ 10, the set of taken bikes fits in a bitmask of at most 10 bits (2^10 = 1024 states). "
            "We process workers in fixed order 0, 1, ..., n-1. At any point, the number of 1-bits in the mask "
            "equals the worker index: popcount(mask) == worker_index. "
            "So the state is fully captured by just the mask — the worker index is implicit."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Define dp[mask] = minimum total Manhattan distance to assign workers[0..popcount(mask)-1] "
            "using exactly the bikes indicated by mask.\n\n"
            "1. Base case: dp[0] = 0 (no workers assigned, zero cost).\n"
            "2. For each mask in order 0 to 2^m - 1:\n"
            "   - worker k = popcount(mask) is the next to assign.\n"
            "   - For each bike b NOT in mask: relax dp[mask | (1<<b)] with dp[mask] + dist(workers[k], bikes[b]).\n"
            "3. Answer: min(dp[mask]) over all masks with exactly n bits set.\n\n"
            "Iterating masks in ascending order guarantees all smaller sub-states are finalized before larger ones."
        ),
        N.callout(
            "Analogy: Think of the bitmask as a hotel key-card panel — each bit is a room (bike). "
            "As you check in workers one by one, you flip a bit for the room they get. "
            "The panel state (bitmask) tells you exactly what is available for the next worker.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Bitmask DP"),
    N.para(
        "Bitmask DP is the standard technique for exact assignment / TSP-style problems over small sets (n ≤ 20). "
        "It was popularized by the Held-Karp algorithm (1962) for the Travelling Salesman Problem.\n\n"
        "Core invariant: dp[mask] holds the minimum cost to optimally assign the first popcount(mask) workers "
        "to exactly the bikes encoded by mask.\n\n"
        "Why it works: Processing workers in a fixed order ensures we never revisit a worker. "
        "The bitmask encodes the full 'which bikes are taken' state, so every sub-problem is uniquely identified. "
        "The recurrence exhausts all possible bike choices for the current worker, picking the cheapest.\n\n"
        "Generalization: Replace 'bike assignment' with any 1-to-1 matching over a small universe. "
        "The pattern is dp[mask] → dp[mask | (1<<item)] for each unclaimed item.\n\n"
        "Recognize when: 'Assign n items to n resources, minimize total cost, n ≤ 20' → Bitmask DP."
    ),
    N.h3("Code"),
    N.code("""\
from typing import List

class Solution:
    def assignBikes(self, workers: List[List[int]], bikes: List[List[int]]) -> int:
        n, m = len(workers), len(bikes)
        INF = float('inf')

        # dp[mask] = min total Manhattan distance to assign workers[0..popcount(mask)-1]
        #            using exactly the bikes encoded by `mask`
        dp = [INF] * (1 << m)
        dp[0] = 0  # base case: 0 workers assigned, 0 cost

        ans = INF
        for mask in range(1 << m):
            if dp[mask] == INF:
                continue               # unreachable state — skip
            worker = bin(mask).count('1')   # popcount = next worker index
            if worker == n:
                ans = min(ans, dp[mask])    # all workers assigned — record
                continue
            wx, wy = workers[worker]
            for b in range(m):
                if mask & (1 << b):        # bike b already taken
                    continue
                dist = abs(wx - bikes[b][0]) + abs(wy - bikes[b][1])
                new_mask = mask | (1 << b)
                if dp[mask] + dist < dp[new_mask]:
                    dp[new_mask] = dp[mask] + dist

        return ans
""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("n, m = len(workers), len(bikes)", {"code": True}), " — W workers, B bikes (n ≤ m ≤ 10)."])),
    N.para(N.rich([("dp = [INF] * (1 << m)", {"code": True}), " — One cell per possible subset of bikes (2^m cells). All start at infinity (unvisited)."])),
    N.para(N.rich([("dp[0] = 0", {"code": True}), " — Base case: empty set of bikes taken → 0 workers assigned → 0 cost."])),
    N.para(N.rich([("for mask in range(1 << m):", {"code": True}), " — Iterate all bike subsets ascending. Smaller masks are computed before larger ones, so sub-states are always ready."])),
    N.para(N.rich([("if dp[mask] == INF: continue", {"code": True}), " — Skip unreachable states (subsets that can't arise from valid partial assignments)."])),
    N.para(N.rich([("worker = bin(mask).count('1')", {"code": True}), " — Number of bits set = number of bikes already assigned = index of the next worker."])),
    N.para(N.rich([("if worker == n: ans = min(ans, dp[mask])", {"code": True}), " — All n workers assigned; this is a complete valid assignment. Update global answer."])),
    N.para(N.rich([("if mask & (1 << b): continue", {"code": True}), " — Skip bike b if already taken (bit b set in mask)."])),
    N.para(N.rich([("dist = abs(wx - bikes[b][0]) + abs(wy - bikes[b][1])", {"code": True}), " — Manhattan distance from current worker to bike b."])),
    N.para(N.rich([("new_mask = mask | (1 << b)", {"code": True}), " — Set bit b to mark bike b as now taken."])),
    N.para(N.rich([("dp[new_mask] = min(dp[new_mask], dp[mask] + dist)", {"code": True}), " — Classic DP relaxation: carry forward the cheapest path."])),
    N.divider(),
]

# ── SOLUTION 2 — TOP-DOWN MEMOIZATION ───────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down Memoization (Easier to Derive in Interview)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same state-space as Solution 1 but derived recursively. "
            "We ask: what is the minimum cost to assign workers starting from worker w, "
            "given that `mask` encodes the already-taken bikes?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion without memoization re-solves the same (w, mask) sub-problem many times. "
            "With n=4, m=10, there are 4 × 2^10 = 4096 unique sub-problems. Without caching, we'd re-explore them exponentially."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Two recursive calls with the same (w, mask) pair yield identical results. "
            "Cache with @lru_cache. Since worker = popcount(mask), the state can also be keyed by mask alone — "
            "but using (w, mask) is more readable and explicit."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. dfs(w, mask): min cost to assign workers w..n-1 given bikes in mask are taken.\n"
            "2. Base: dfs(n, mask) = 0.\n"
            "3. Recurse: for each free bike b, cost = dist(workers[w], bikes[b]) + dfs(w+1, mask | (1<<b)).\n"
            "4. Return min over all b."
        ),
        N.callout(
            "Memoization tip: @lru_cache(maxsize=None) on a nested function works cleanly here. "
            "Python's tuple hashing handles (w, mask) keys efficiently.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""\
from typing import List
from functools import lru_cache

class Solution:
    def assignBikes(self, workers: List[List[int]], bikes: List[List[int]]) -> int:
        n, m = len(workers), len(bikes)

        @lru_cache(maxsize=None)
        def dfs(w: int, mask: int) -> int:
            # w = index of next worker to assign
            # mask = bitmask of already-taken bikes
            if w == n:
                return 0  # all workers assigned
            wx, wy = workers[w]
            best = float('inf')
            for b in range(m):
                if mask & (1 << b):
                    continue  # bike b already taken
                dist = abs(wx - bikes[b][0]) + abs(wy - bikes[b][1])
                best = min(best, dist + dfs(w + 1, mask | (1 << b)))
            return best

        return dfs(0, 0)
""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " — Memoizes every (w, mask) result. Without this, identical sub-problems are recomputed exponentially."])),
    N.para(N.rich([("if w == n: return 0", {"code": True}), " — Base case: all workers assigned, zero remaining cost."])),
    N.para(N.rich([("if mask & (1 << b): continue", {"code": True}), " — Skip bikes already claimed (bit b set in mask)."])),
    N.para(N.rich([("best = min(best, dist + dfs(w+1, mask|(1<<b)))", {"code": True}), " — Try giving bike b to worker w, recurse for remaining workers. Keep minimum."])),
    N.para(N.rich([("return dfs(0, 0)", {"code": True}), " — Start with worker 0 and no bikes taken."])),
    N.divider(),
]

# ── WHY IS THIS DP ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(
        "Two pillars of DP are met:\n\n"
        "1. Optimal Substructure — Once we fix which bike worker 0 gets, the remaining sub-problem "
        "(assign workers 1..n-1 to the remaining bikes) is independent and must also be solved optimally. "
        "The global optimum decomposes cleanly into sub-optimal solutions.\n\n"
        "2. Overlapping Sub-problems — Many different paths through the recursion tree reach the same "
        "(worker_index, bike_mask) state. Without memoization, each sub-problem would be recomputed "
        "exponentially many times."
    ),
    N.code("""\
# Recurrence relation:
# dp(w, mask) = min over all free bikes b of:
#               dist(workers[w], bikes[b]) + dp(w+1, mask | (1<<b))
#
# Base case:
# dp(n, any_mask) = 0
#
# Bottom-up equivalent:
# dp[mask | (1<<b)] = min(dp[mask | (1<<b)], dp[mask] + dist(workers[popcount(mask)], bikes[b]))
# for each bike b NOT in mask, iterating mask from 0 to 2^m - 1
""", "python"),
    N.callout(
        "The bitmask trick: encoding 'which bikes are taken' as an integer allows dp array indexing in O(1). "
        "2^10 = 1024 states — tiny and perfectly cacheable.",
        "🔐", "gray_background"
    ),
    N.divider(),
]

# ── COMPLEXITY ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bitmask DP Bottom-Up (optimal)", "O(W × 2^B × B)", "O(2^B)"],
        ["Top-Down Memoization", "O(W × 2^B × B)", "O(W × 2^B) + call stack"],
        ["Brute Force Permutations", "O(B! / (B-W)! × W)", "O(W)"],
    ]),
    N.para(
        "W = workers (≤ 10), B = bikes (≤ 10). "
        "For bottom-up DP: 2^10 = 1024 masks × 10 workers × 10 bikes = 102,400 operations — instant. "
        "Bottom-up uses only O(2^B) space; worker index is implicit in popcount(mask)."
    ),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Bitmask DP Min Distance (assignment / matching over small set)"])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("'Assign n items to n resources, minimize total cost, n ≤ 20.' "
             "Key signals: small n (≤ 20), set-membership state needed (which items taken), one-to-one assignment. "
             "Encode taken set as bitmask. Process items in fixed order; popcount derives position.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── RELATED PROBLEMS ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Bitmask DP technique:"),
    N.bullet(N.rich([("Campus Bikes I (LC 1057)", {"bold": True}), " (Medium) — Greedy version; useful contrast. No DP needed there."])),
    N.bullet(N.rich([("Shortest Path Visiting All Nodes (LC 847)", {"bold": True}), " (Hard) — BFS + bitmask over graph nodes visited."])),
    N.bullet(N.rich([("Fair Distribution of Cookies (LC 2305)", {"bold": True}), " (Medium) — Bitmask DP to minimise max cookie load across children."])),
    N.bullet(N.rich([("Minimum Number of Work Sessions to Finish the Tasks (LC 1986)", {"bold": True}), " (Medium) — Bitmask DP over task subsets."])),
    N.bullet(N.rich([("Stickers to Spell Word (LC 691)", {"bold": True}), " (Hard) — Bitmask over character coverage of target word."])),
    N.bullet(N.rich([("Partition to K Equal Sum Subsets (LC 698)", {"bold": True}), " (Medium) — Backtracking + bitmask over element subsets."])),
    N.bullet(N.rich([("Find Shortest Superstring (LC 943)", {"bold": True}), " (Hard) — Classic O(n^2 * 2^n) bitmask DP on string adjacency."])),
    N.bullet(N.rich([("Smallest Sufficient Team (LC 1125)", {"bold": True}), " (Hard) — Bitmask DP over skill sets; assign team to cover all required skills."])),
    N.para("These problems share the core technique: represent a subset of used items as an integer bitmask, and use DP over all 2^n subsets."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18, Sub-Pattern: DP: Bitmask", "📚", "gray_background"),
]

# ── EMBED ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Push to Notion ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")

# ── 5. Status marker ──────────────────────────────────────────────────────────
import json as _json, pathlib as _pl
html_path = _pl.Path(__file__).parent / "campus_bikes_ii_explainer.html"
html_lines = len(html_path.read_text().splitlines())
status = {
    "slug": SLUG,
    "html": "OK",
    "notion": "OK",
    "lines": html_lines,
    "notes": "HTML kept (919 lines, all markers). Notion wiped and rebuilt with full DP bitmask content."
}
status_dir = _pl.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
(status_dir / "campus_bikes_ii.json").write_text(_json.dumps(status, indent=2))
print(f"RESULT {SLUG} | html=OK | notion=OK | lines={html_lines}")
