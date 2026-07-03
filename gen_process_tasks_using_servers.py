"""
gen_process_tasks_using_servers.py — Notion update for LeetCode #1882
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8184-a750-fbf4ddc26846"
SLUG    = "process_tasks_using_servers"

# ── 1. Set properties ─────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1882,
    pattern="Heaps",
    subpatterns=["Two Heaps (Free/Busy)", "Greedy + Heap"],
    tc="O((n+m) log n)",
    sc="O(n)",
    key_insight="Use two min-heaps: free servers by (weight, index), busy servers by finish_time; advance time when no server is free.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old content ──────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ── 3. Build body blocks ─────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array ", {}),
        ("servers", {"code": True}),
        (" of length n where ", {}),
        ("servers[i]", {"code": True}),
        (" is the weight of the i-th server, and an array ", {}),
        ("tasks", {"code": True}),
        (" of length m where ", {}),
        ("tasks[j]", {"code": True}),
        (" is the processing time of task j. Task j becomes available at time j. Assign each task to the free server with the smallest weight (break ties by smallest index). If no server is free, wait until the earliest busy server finishes. Return ", {}),
        ("ans", {"code": True}),
        (" where ", {}),
        ("ans[j]", {"code": True}),
        (" is the index of the server that processed task j.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Two-Heap Greedy ──
SOLUTION_1_CODE = """\
import heapq

def assignTasks(servers: list[int], tasks: list[int]) -> list[int]:
    # free heap: (weight, index) — min by weight then index
    free = [(w, i) for i, w in enumerate(servers)]
    heapq.heapify(free)

    # busy heap: (finish_time, weight, index)
    busy = []
    ans = [0] * len(tasks)

    for j, duration in enumerate(tasks):
        time = j  # task j arrives at time j

        # Release all servers that finished by now
        while busy and busy[0][0] <= time:
            ft, w, idx = heapq.heappop(busy)
            heapq.heappush(free, (w, idx))

        # If still no free server, jump time to earliest finish
        if not free:
            time = busy[0][0]
            while busy and busy[0][0] <= time:
                ft, w, idx = heapq.heappop(busy)
                heapq.heappush(free, (w, idx))

        # Assign to best free server
        w, idx = heapq.heappop(free)
        ans[j] = idx
        heapq.heappush(busy, (time + duration, w, idx))

    return ans
"""

blocks += [
    N.h2("Solution 1 — Two-Heap Greedy Simulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're running a job shop simulation. Tasks arrive on a conveyor belt every second, and we must route each to a worker (server) following strict priority rules: cheapest worker first, break ties by seniority (index). Workers may be busy — we have to wait for the next available one."),
        N.h4("What Doesn't Work"),
        N.para("A naive approach scans all n servers for each of m tasks to find the best free one: O(n·m). For n=m=100,000 this is 10^10 operations — hard time limit exceeded. We need O(log n) access to the 'best free' server."),
        N.h4("The Key Observation"),
        N.para("At any moment, we need to answer two different 'minimum' queries: (A) among free servers, which has the smallest weight (then index)? and (B) among busy servers, which one finishes soonest? These require two different orderings — which means two separate min-heaps."),
        N.h4("Building the Solution"),
        N.para("Initialize the free heap with all (weight, index) pairs. Python tuples compare lexicographically, so heapq naturally gives us the right priority. The busy heap stores (finish_time, weight, index). For each task: release finished servers (while busy[0][0] <= time), jump time if free is empty, then pop best free and push to busy."),
        N.callout("Analogy: Think of two priority lines at a DMV — one for available agents (sorted by window number/seniority), one for busy agents (sorted by their estimated free time). You always route to the first available window; if all windows are occupied, you check the clock on the earliest-returning agent.", "🏦", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("free = [(w,i) for i,w in enumerate(servers)]", {"code": True}), (" — Build list of (weight, index) tuples. We enumerate to get index i, then swap order because we want weight as primary sort key.", {})])),
    N.para(N.rich([("heapq.heapify(free)", {"code": True}), (" — Convert list to min-heap in O(n). All servers start free.", {})])),
    N.para(N.rich([("busy = []", {"code": True}), (" — Empty busy heap: will hold (finish_time, weight, index) triples.", {})])),
    N.para(N.rich([("for j, duration in enumerate(tasks):", {"code": True}), (" — Iterate tasks in order. j is both the task index and its arrival time.", {})])),
    N.para(N.rich([("time = j", {"code": True}), (" — Nominal start time. May be advanced if no server is free.", {})])),
    N.para(N.rich([("while busy and busy[0][0] <= time:", {"code": True}), (" — Release all busy servers whose finish_time has arrived or passed. Use while, not if — multiple servers can finish at the exact same time.", {})])),
    N.para(N.rich([("heapq.heappop(busy)", {"code": True}), (" → ", {}), ("heapq.heappush(free, (w, idx))", {"code": True}), (" — Destructure the triple, push (weight, index) back to free heap.", {})])),
    N.para(N.rich([("if not free:", {"code": True}), (" — If still no free server after normal release, must wait. This happens when all tasks arrive faster than servers process them.", {})])),
    N.para(N.rich([("time = busy[0][0]", {"code": True}), (" — Jump clock to the minimum finish_time. The heap's top element has the smallest finish_time.", {})])),
    N.para(N.rich([("while busy and busy[0][0] <= time:", {"code": True}), (" — Release all servers finishing at that exact moment (ties possible).", {})])),
    N.para(N.rich([("w, idx = heapq.heappop(free)", {"code": True}), (" — Pop the best available server. Min-heap gives smallest weight first; tie-broken by smallest index.", {})])),
    N.para(N.rich([("ans[j] = idx", {"code": True}), (" — Record which server handles task j.", {})])),
    N.para(N.rich([("heapq.heappush(busy, (time+duration, w, idx))", {"code": True}), (" — Schedule server as busy until time+duration. Store weight/index so we can reconstruct the server identity when releasing.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
SOLUTION_2_CODE = """\
def assignTasks_brute(servers: list[int], tasks: list[int]) -> list[int]:
    finish = [0] * len(servers)  # finish[i] = when server i is next free
    ans = []
    for j, dur in enumerate(tasks):
        t = j
        best = -1
        # Scan all servers for best free one at time t
        for i in range(len(servers)):
            if finish[i] <= t:
                if best == -1 or (servers[i], i) < (servers[best], best):
                    best = i
        # If no free server, find earliest finishing one
        if best == -1:
            min_finish = min(finish)
            t = min_finish
            for i in range(len(servers)):
                if finish[i] == t:
                    if best == -1 or (servers[i], i) < (servers[best], best):
                        best = i
        finish[best] = t + dur
        ans.append(best)
    return ans
    # Time: O(n*m) — TLE for large inputs
"""

blocks += [
    N.h2("Solution 2 — Brute Force Linear Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Maintain a finish_time array. For each task, scan all servers to find the free one with smallest weight/index. If none free, find the minimum of finish times and wait."),
        N.h4("What Doesn't Work"),
        N.para("The O(n) scan per task yields O(n*m) overall. TLE for n=m=10^5."),
        N.h4("The Key Observation"),
        N.para("This brute force is correct — useful for small inputs, testing, and generating expected output. It establishes the baseline to optimize from."),
        N.h4("Building the Solution"),
        N.para("Simple two-loop structure: outer loop over tasks, inner loop over servers. The jump-time logic is straightforward with min(finish)."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE, "python"),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force — linear scan", "O(n·m)", "O(n)"],
        ["Two Heaps — greedy (Interview Pick)", "O((n+m) log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Two Heaps (Free/Busy), Greedy + Heap", {})])),
    N.callout(
        "When to recognize this pattern: Resources have two states (free/busy) with different ordering priorities. You need both 'best available' (free heap) and 'earliest releasing' (busy heap) simultaneously. Keywords: 'assign to server/worker/machine', 'earliest finish', 'priority scheduling', event-driven simulation.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
related = [
    ("Meeting Rooms II", "Medium", "Min-heap of room end-times; pop and reuse when a room frees before the next meeting. Same free/busy pattern.", "#253"),
    ("Find Median from Data Stream", "Hard", "Classic two-heap split: max-heap for lower half, min-heap for upper half. O(log n) insert, O(1) median.", "#295"),
    ("Task Scheduler", "Medium", "Greedy with max-heap of task frequencies; enforce cooldown between same-task runs.", "#621"),
    ("IPO", "Hard", "Two heaps: min-heap by capital requirement, max-heap by profit. Pick k most profitable projects within budget.", "#502"),
    ("Single-Threaded CPU", "Medium", "Sort tasks by enqueue time; use min-heap by processing time for greedy CPU assignment.", "#1834"),
    ("Furthest Building You Can Reach", "Medium", "Greedy: use ladders for the k largest height jumps, tracked with a min-heap.", "#1642"),
    ("Minimum Number of Refueling Stops", "Hard", "Max-heap of reachable fuel amounts; greedily refuel from richest station seen.", "#871"),
]

blocks += [N.h2("🔗 Related Problems"), N.para("Problems using the same Two Heaps or Greedy + Heap technique:")]
for name, diff, note, num in related:
    blocks += [N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) {num} — {note}", {}),
    ]))]
blocks += [N.divider()]

# ── Interactive Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the two-heap simulation visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Append all blocks ────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} ({len(blocks)} blocks appended)")
