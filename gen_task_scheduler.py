"""
gen_task_scheduler.py — Notion page update for Task Scheduler (LC #621)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8104-b539-d216b5ce23bf"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=621,
    pattern="Greedy",
    subpatterns=["Max Frequency Determines Idle"],
    tc="O(n)",
    sc="O(1)",
    key_insight="The most frequent task determines idle slots: result = max((max_f-1)*(n+1)+max_count, len(tasks))",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body blocks ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a list of CPU tasks, each labeled with an uppercase English letter, and an integer "),
        ("n", {"code": True}),
        (" representing the cooldown interval between two same tasks, return the minimum number of CPU intervals (including idle intervals) needed to finish all tasks. The same task type cannot execute again until at least "),
        ("n", {"code": True}),
        (" intervals have passed since its last execution.")
    ])),
    N.para("Example 1: tasks = [A,A,A,B,B,B], n = 2 → Output: 8  (A→B→idle→A→B→idle→A→B)"),
    N.para("Example 2: tasks = [A,A,A,B,B,B,C,C], n = 2 → Output: 8  (A→B→C→A→B→C→A→B, zero idle)"),
    N.divider(),
]

# ── Solution 1: Math Formula (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Greedy Math Formula (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("We need to schedule tasks with a cooldown constraint. Instead of simulating each slot, ask: what is the minimum possible schedule length? The answer is determined by the most frequent task — it creates unavoidable gaps."),
        N.para(N.rich([("What Doesn't Work", {"bold": True})])),
        N.para("Simulating slot-by-slot with a priority queue is correct but O(result × 26). We can do better with a direct formula that captures the schedule structure in one pass."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("Imagine the schedule as a grid: (n+1) columns wide. The most frequent task anchors the leftmost column of every row. There are (max_f - 1) complete rows, then a partial last row. Other tasks fill the remaining cells. If there are too many diverse tasks to fit in the grid, they spill over and no idle is ever needed."),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para("Grid body: (max_f - 1) complete rows × (n+1) wide = (max_f - 1) × (n+1) intervals. Last row: max_count tasks (those tied at max frequency). Total: (max_f-1)×(n+1)+max_count. But if diverse tasks overflow the grid (no idle needed), the answer is just len(tasks). Take the max of both."),
        N.callout("Analogy: Imagine filling a parking lot with (n+1) spots per row. The VIP car (most frequent task) always gets spot 1. Other cars fill spots 2 through n+1. If you run out of cars, leave spots empty (idle). If you have MORE cars than spots, they park in overflow rows — zero empty spots.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import Counter\n"
        "\n"
        "def leastInterval(tasks: list[str], n: int) -> int:\n"
        "    counts = Counter(tasks)                    # {A:3, B:3, C:2}\n"
        "    max_f = max(counts.values())               # highest frequency = 3\n"
        "    max_count = sum(1 for f in                 # tasks tied at max freq\n"
        "                    counts.values() if f == max_f)  # = 2 (A and B)\n"
        "    part1 = (max_f - 1) * (n + 1) + max_count # (2)*(3)+2 = 8\n"
        "    return max(part1, len(tasks))              # max(8, 8) = 8\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("counts = Counter(tasks)", {"code": True}), " — Build a frequency map of each task type. Counter is O(n). For 26-letter alphabet, at most 26 entries — effectively O(1) space."])),
    N.para(N.rich([("max_f = max(counts.values())", {"code": True}), " — Find the highest frequency. This is the bottleneck: the task that appears most and forces the most gaps. O(26) = O(1)."])),
    N.para(N.rich([("max_count = sum(...)", {"code": True}), " — Count how many tasks share max_f. If A and B both appear 3 times, max_count=2. Needed for the final partial row of the grid."])),
    N.para(N.rich([("part1 = (max_f - 1) * (n + 1) + max_count", {"code": True}), " — The grid formula. (max_f-1) complete frames of width (n+1), plus max_count tasks in the last partial row."])),
    N.para(N.rich([("return max(part1, len(tasks))", {"code": True}), " — If tasks are so diverse that every cooldown slot is filled, no idle is needed and the schedule is exactly len(tasks) long. The max() handles both cases."])),
    N.divider(),
]

# ── Solution 2: Heap Simulation ──
blocks += [
    N.h2("Solution 2 — Heap Simulation (Intuitive Approach)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("Simulate the actual scheduling process. At each interval, greedily pick the most frequent available task. If none are available (due to cooldown), insert idle."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("A max-heap ordered by remaining count lets us always pick the most frequent available task in O(log 26) = O(1) time. Process each interval one by one — or better, process each 'frame' of (n+1) slots at once."),
        N.callout("This approach is easier to derive in an interview without knowing the formula. Propose it first, then offer to optimize to the math formula.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "import heapq\n"
        "from collections import Counter\n"
        "\n"
        "def leastInterval(tasks: list[str], n: int) -> int:\n"
        "    freq = list(Counter(tasks).values())\n"
        "    max_heap = [-c for c in freq]  # negate for max-heap via Python min-heap\n"
        "    heapq.heapify(max_heap)\n"
        "    time_elapsed = 0\n"
        "    while max_heap:\n"
        "        # Process one frame of n+1 slots\n"
        "        cycle = []\n"
        "        for _ in range(n + 1):\n"
        "            if max_heap:\n"
        "                cycle.append(heapq.heappop(max_heap))  # most frequent\n"
        "        # Reinsert tasks with remaining count\n"
        "        for c in cycle:\n"
        "            if c + 1 < 0:  # still has occurrences left\n"
        "                heapq.heappush(max_heap, c + 1)\n"
        "        # If more work remains: full frame (n+1); else: just tasks in last cycle\n"
        "        time_elapsed += n + 1 if max_heap else len(cycle)\n"
        "    return time_elapsed\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("max_heap = [-c for c in freq]", {"code": True}), " — Negate counts because Python's heapq is a min-heap. Negating makes pop() give the largest count first."])),
    N.para(N.rich([("for _ in range(n + 1):", {"code": True}), " — Process one cooling frame of up to (n+1) slots. Pop the most frequent task each time."])),
    N.para(N.rich([("if c + 1 < 0:", {"code": True}), " — Since counts are negated, c+1 < 0 means the task still has remaining occurrences (e.g., -3+1=-2 < 0, so 2 more runs needed)."])),
    N.para(N.rich([("time_elapsed += n+1 if max_heap else len(cycle)", {"code": True}), " — If more tasks remain after this frame, we charged a full (n+1) slots. If this was the last frame, charge only the actual tasks placed (no trailing idle)."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Heap Simulation", "O(n × k) — k = cooldown", "O(1) — 26 entries max"],
        ["Math Formula (Interview Pick)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Greedy (Section 16 of DSA_Patterns_and_SubPatterns_Guide.md)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Max Frequency Determines Idle — the most frequent element determines the minimum gaps/idle in a scheduling problem"])),
    N.callout(
        "When to recognize this pattern: 'minimize total intervals' + 'cooldown between same task' → scheduling with repetition constraint. The bottleneck is the element that appears MOST — it forces the schedule structure. When the formula doesn't apply (many distinct tasks), tasks overflow → zero idle → answer = total task count.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Max Frequency / Greedy Scheduling):"),
]
related = [
    ("Reorganize String", "Medium", "#767", "Same max-frequency logic: is it possible to arrange so no two adjacent are identical?"),
    ("Rearrange String k Distance Apart", "Hard", "#358", "Direct generalization: same letter must be k apart — identical formula"),
    ("Gas Station", "Medium", "#134", "Greedy circular scheduling: start where cumulative deficit recovers"),
    ("Jump Game II", "Medium", "#45", "Greedy boundary expansion to minimize jumps — local optimal at each frame"),
    ("Maximum Frequency Stack", "Hard", "#895", "Track most-frequent and most-recent; frequency-based priority pop"),
    ("IPO / Task Scheduling with Deadlines", "Hard", "#502", "Greedy + max-heap to maximize profit with scheduling constraints"),
    ("Minimum Meeting Rooms", "Medium", "LeetCode Premium", "Max overlap at any point = rooms needed — frequency determines bound"),
]
for name, diff, num, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) {num} — {note}", {})
    ])))

blocks += [
    N.para("These problems share the same core technique: the most frequent element determines the minimum structure of an optimal schedule."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 16 — Greedy Algorithms\nSub-Pattern verified: Guide row → Task Scheduler | Medium | Max Frequency Determines Idle", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("task_scheduler")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks: {len(blocks)}")
