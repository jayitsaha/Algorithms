"""
gen_single_threaded_cpu.py
Regenerate Notion page for LeetCode #1834 - Single-Threaded CPU
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81e9-8282-d8ff5aa0c5b5"
SLUG = "single_threaded_cpu"

print(f"Setting properties for {PAGE_ID} ...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1834,
    pattern="Heaps",
    subpatterns=["Sort + Min Heap"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sort tasks by enqueue time; use a min-heap of (proc_time, orig_idx) to always pick the shortest available job; fast-forward time when CPU is idle.",
    icon="🟡"
)
print("Properties set.")

print("Wiping old body ...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── Build body blocks ───────────────────────────────────────────────────────

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given n tasks, each represented as "),
        ("`tasks[i] = [enqueueTime, processingTime]`", {"code": True}),
        (". A single-threaded CPU picks tasks to run following these rules:\n"
         "1. If the CPU is idle and there are no available tasks, the CPU waits until the next task becomes available.\n"
         "2. When the CPU is available, it picks the task with the shortest processing time from the available tasks. If multiple tasks have equal processing time, it picks the task with the smallest index.\n"
         "3. Once a task is started, it runs to completion.\n"
         "Return the order in which the CPU will process the tasks.")
    ])),
    N.callout(
        N.rich([
            ("Constraints: ", {"bold": True}),
            ("1 ≤ tasks.length ≤ 10⁵, tasks[i].length == 2, 1 ≤ enqueueTime, processingTime ≤ 10⁹")
        ]),
        "📋", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1 — Sort + Min Heap ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Sort + Min Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each moment, we need the minimum-processing-time task among those that have already arrived. This is a dynamic minimum query — a classic min-heap use case. The twist: tasks don't all arrive at once, so we need a way to add them incrementally as time advances."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: scan all remaining tasks every time the CPU is free, pick the minimum. O(n) per scheduling step × n steps = O(n²). Also, checking for idle via current_time += 1 loops can take up to O(10⁹) iterations if tasks have large enqueue times. Both are too slow."),
        N.h4("The Key Observation"),
        N.para("If we sort tasks by enqueue time, we can use a pointer j to sweep new arrivals into a heap as time advances — just like a sliding window. After sorting, indexed[j][1][0] tells us the next task's arrival time without scanning all remaining tasks. This gives O(n) total sweeping + O(n log n) for n heap operations."),
        N.h4("Building the Solution"),
        N.para(
            "1. Tag each task with its original index (before sorting): indexed = sorted(enumerate(tasks), key=lambda x: x[1][0])\n"
            "2. Start current_time at the first task's enqueue time.\n"
            "3. At each loop: push all indexed[j] with enqueue ≤ current_time into heap as (proc, orig_idx).\n"
            "4. If heap empty: fast-forward current_time to indexed[j][1][0].\n"
            "5. Pop (proc, orig_idx), add orig_idx to result, advance current_time += proc."
        ),
        N.callout(
            "Analogy: Like a doctor's waiting room — patients arrive over time. The doctor always treats the patient with the shortest appointment next. The receptionist (pointer j) adds newly arrived patients to the waiting list as each appointment ends.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "import heapq\n\n"
        "def getOrder(tasks):\n"
        "    # Tag each task with original index, then sort by enqueue time\n"
        "    indexed = sorted(enumerate(tasks), key=lambda x: x[1][0])\n"
        "    result = []\n"
        "    heap = []  # min-heap of (proc_time, orig_idx)\n"
        "    j = 0      # pointer into sorted indexed list\n"
        "    current_time = indexed[0][1][0]  # start at first arrival\n\n"
        "    while len(result) < len(tasks):\n"
        "        # Push all tasks that have arrived by current_time\n"
        "        while j < len(indexed) and indexed[j][1][0] <= current_time:\n"
        "            orig_i, (enq, proc) = indexed[j]\n"
        "            heapq.heappush(heap, (proc, orig_i))\n"
        "            j += 1\n\n"
        "        if not heap:  # CPU idle — fast-forward to next arrival\n"
        "            current_time = indexed[j][1][0]\n"
        "            continue\n\n"
        "        proc, orig_i = heapq.heappop(heap)\n"
        "        current_time += proc\n"
        "        result.append(orig_i)\n\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("indexed = sorted(enumerate(tasks), ...) ", {"code": True}), (" — enumerate attaches original index 0..n-1 to each task BEFORE sorting. Sorting by x[1][0] orders by enqueue time. Original indices survive the rearrangement.")])),
    N.para(N.rich([("current_time = indexed[0][1][0] ", {"code": True}), (" — Start the clock at the first task's arrival, not 0. If all tasks arrive at t=1000, no point counting from 0.")])),
    N.para(N.rich([("while j < len(indexed) and indexed[j][1][0] <= current_time ", {"code": True}), (" — Sweep pointer: push every task that has become available. Inner while terminates when we hit a future arrival or exhaust all tasks.")])),
    N.para(N.rich([("heapq.heappush(heap, (proc, orig_i)) ", {"code": True}), (" — Store (processing_time, original_index). Python heapq is a min-heap, so the smallest proc_time floats to the top. Ties resolved by orig_i (smaller index first) automatically.")])),
    N.para(N.rich([("if not heap: current_time = indexed[j][1][0] ", {"code": True}), (" — Critical fast-forward: when no task is available, jump directly to next arrival. Never write current_time += 1 — that's O(T) and causes TLE.")])),
    N.para(N.rich([("proc, orig_i = heapq.heappop(heap) ", {"code": True}), (" — Pop the globally shortest available job. This is our scheduling decision.")])),
    N.para(N.rich([("current_time += proc; result.append(orig_i) ", {"code": True}), (" — Advance clock by the task's duration, record its original index (not sorted index).")])),
    N.divider(),
]

# ── Solution 2 — Brute Force ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force Simulation (for comparison)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Most direct translation of the problem: at each time step, scan all tasks to find the shortest available one. Run it. Repeat."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n²) scanning plus O(T) idle-time loops. For n=10⁵ and enqueue times up to 10⁹, this is far too slow."),
        N.h4("The Key Observation"),
        N.para("Use this only to verify correctness on small inputs, then optimize to Solution 1."),
    ]),
    N.h3("Code"),
    N.code(
        "def getOrder_brute(tasks):\n"
        "    n = len(tasks)\n"
        "    done = [False] * n\n"
        "    t = 0\n"
        "    result = []\n"
        "    while len(result) < n:\n"
        "        available = [(tasks[i][1], i) for i in range(n)\n"
        "                     if not done[i] and tasks[i][0] <= t]\n"
        "        if not available:\n"
        "            t += 1  # SLOW: up to 10^9 iterations!\n"
        "            continue\n"
        "        proc, pick = min(available)  # O(n) each time\n"
        "        done[pick] = True\n"
        "        t += proc\n"
        "        result.append(pick)\n"
        "    return result"
    ),
    N.callout(
        "Warning: This brute force is O(n² + T). For n=10⁵ or T=10⁹, this will Time Limit Exceed. Use Solution 1 in interviews.",
        "⚠️", "red_background"
    ),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n² + T)", "O(n)", "TLE for large n or T"],
        ["Sort + Min Heap (optimal)", "O(n log n)", "O(n)", "Sort + n heap ops"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps & Priority Queues")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Min Heap — Sort tasks by one criterion (arrival time), then use min-heap keyed by another (processing time) to greedily pick the optimal task.")])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("Items 'arrive' at different times and you need the minimum/maximum among available items at each step. Events sorted by arrival, selected by cost/priority. Classic signals: CPU scheduling, meeting rooms, task queues. Sort first, then heap.")
        ]),
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Sub-Pattern verified: Guide Section 13.1 (Heaps & Priority Queues → Heap Operations). "
         "Entry: Single-Threaded CPU | Medium | Sort + Min Heap.", {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sort + Min Heap / Heap Simulation technique:"),
    N.bullet(N.rich([("Process Tasks Using Servers", {"bold": True}), (" (Medium) — Two heaps (free/busy servers); same Sort + Heap skeleton. LeetCode #1882")])),
    N.bullet(N.rich([("Maximum Number of Events That Can Be Attended", {"bold": True}), (" (Medium) — Sort by start day, min-heap on end day. LeetCode #1353")])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Sort by start time, min-heap of end times to count concurrent meetings. LeetCode #253")])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Max-heap with cooldown queue; greedy frequency-based scheduling. LeetCode #621")])),
    N.bullet(N.rich([("Minimum Cost to Connect Sticks", {"bold": True}), (" (Medium) — Min-heap greedy: always merge two smallest sticks. LeetCode #1167")])),
    N.bullet(N.rich([("Furthest Building You Can Reach", {"bold": True}), (" (Medium) — Min-heap to greedily allocate ladders. LeetCode #1642")])),
    N.bullet(N.rich([("Merge k Sorted Lists", {"bold": True}), (" (Hard) — Min-heap with k pointers; identical push/pop pattern. LeetCode #23")])),
    N.para("These problems share the core technique: a min-heap that grows dynamically as items become available, selecting the greedy optimum at each step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 13.1", "📚", "gray_background"),
]

# ── Interactive Explainer ─────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the CPU scheduling simulation — use Next/Prev or arrow keys to watch tasks enter the heap, get selected by SJF, and execute in order.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page ...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
