"""
gen_snapshot_array.py — Notion page for Snapshot Array (LeetCode #1146)
Run from the Algorithms/ directory:  python3 gen_snapshot_array.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Step 0: Create the page (notion_page_id is null) ──────────────────────────
PAGE_ID = N.create_page("Snapshot Array", 1146, "Medium", "🟡")
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ─────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1146,
    pattern="Design",
    subpatterns=["Snapshot Version List"],
    tc="O(log s) per get",
    sc="O(total set calls)",
    key_insight="Store per-index (snap_id, val) changelogs; binary search for historical queries.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Build body blocks ──────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Implement a SnapshotArray that supports: "),
        ("SnapshotArray(length)", {"code": True}),
        (" initializes an array of the given length, all zeros. "),
        ("set(index, val)", {"code": True}),
        (" sets the element at "),
        ("index", {"code": True}),
        (" to "),
        ("val", {"code": True}),
        (". "),
        ("snap()", {"code": True}),
        (" takes a snapshot and returns the snap_id (starts at 0). "),
        ("get(index, snap_id)", {"code": True}),
        (" returns the value at "),
        ("index", {"code": True}),
        (" at the time snapshot "),
        ("snap_id", {"code": True}),
        (" was taken."),
    ])),
    N.divider(),
]

# ── Solution 1 ─────────────────────────────────────────────────────────────────
sol1_code = """\
from bisect import bisect_right

class SnapshotArray:
    def __init__(self, length: int):
        self.snap_id = 0
        # Each index has a changelog: list of (snap_id, value) tuples
        # Seeded with (0, 0) so every index always has a baseline value
        self.data = [[(0, 0)] for _ in range(length)]

    def set(self, index: int, val: int) -> None:
        # If last entry is already this snap_id, overwrite (last write wins)
        if self.data[index][-1][0] == self.snap_id:
            self.data[index][-1] = (self.snap_id, val)
        else:
            # New snap_id epoch: append a fresh (snap_id, val) entry
            self.data[index].append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1          # Advance epoch; O(1), no copying
        return self.snap_id - 1    # Return id of the snapshot just taken

    def get(self, index: int, snap_id: int) -> int:
        timeline = self.data[index]
        # Find insertion point after all entries with snap_id <= target
        # (snap_id, inf) is greater than any real (snap_id, val) tuple
        pos = bisect_right(timeline, (snap_id, float('inf')))
        return timeline[pos - 1][1]  # Step back: most recent write at/before target
"""

blocks += [
    N.h2("Solution 1 — Version List + Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need versioned random access: read any index at any past snapshot. The challenge is doing this without storing full array copies."),
        N.h4("What Doesn't Work"),
        N.para("Copying the full array on every snap() is O(n) per snap. With n=50,000 and 50,000 snapshots, that's 2.5 billion stored values — memory limit exceeded."),
        N.h4("The Key Observation"),
        N.para("Most indices don't change between snapshots. Only record what changes, and tag each change with a snapshot timestamp. This is the 'sparse versioning' observation."),
        N.h4("Building the Solution"),
        N.para("Give each index its own sorted list of (snap_id, value) pairs. set() appends in O(1). snap() just increments a counter in O(1). get() binary-searches the per-index list to find the most recent write at or before the queried snap_id — O(log s)."),
        N.callout(
            "Analogy: Think of it like a spreadsheet's version history. The file doesn't store a full copy on every save — it stores a delta (what changed). When you restore version 5, it finds the last relevant delta.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.snap_id = 0", {"code": True}), " — Global epoch counter. Starts at 0. Increments on every snap() call."])),
    N.para(N.rich([("self.data = [[(0, 0)] for _ in range(length)]", {"code": True}), " — One sorted changelog per index, seeded with (0, 0) as a baseline so get() always has something to return."])),
    N.para(N.rich([("if self.data[index][-1][0] == self.snap_id", {"code": True}), " — Check if the last entry for this index already belongs to the current epoch. If so, no need to append — just overwrite to avoid duplicate snap_ids."])),
    N.para(N.rich([("self.data[index].append((self.snap_id, val))", {"code": True}), " — New epoch: append a fresh entry. Since snap_id only increases, the list stays sorted automatically."])),
    N.para(N.rich([("self.snap_id += 1; return self.snap_id - 1", {"code": True}), " — Increment then return the old value. O(1) — no data copying."])),
    N.para(N.rich([("bisect_right(timeline, (snap_id, float('inf')))", {"code": True}), " — The sentinel float('inf') ensures we land after all real (snap_id, val) tuples with the target snap_id, since inf > any stored value."])),
    N.para(N.rich([("return timeline[pos - 1][1]", {"code": True}), " — Step back one position: this is the last write at or before the queried snapshot. Return its value (index [1] of the tuple)."])),
    N.divider(),
]

# ── Solution 2 ─────────────────────────────────────────────────────────────────
sol2_code = """\
class SnapshotArrayBrute:
    def __init__(self, length: int):
        self.arr = [0] * length   # Working array
        self.history = []         # List of full array copies per snapshot

    def set(self, index: int, val: int) -> None:
        self.arr[index] = val     # Simple in-place update

    def snap(self) -> int:
        self.history.append(self.arr[:])  # O(n) copy -- bottleneck!
        return len(self.history) - 1

    def get(self, index: int, snap_id: int) -> int:
        return self.history[snap_id][index]  # O(1) lookup
"""

blocks += [
    N.h2("Solution 2 — Brute Force: Full Array Copy"),
    N.toggle_h3("💡 Intuition: Why This Is the Starting Point", [
        N.h4("Reframe the Problem"),
        N.para("The simplest version control: keep a list of full snapshots. Like copying a file on every save."),
        N.h4("What Doesn't Work"),
        N.para("snap() costs O(n) time and O(n) extra memory per call. With large n and many snapshots, this quickly hits time and memory limits."),
        N.h4("The Key Observation"),
        N.para("get() is fast (O(1) direct lookup), but snap() is the bottleneck. The optimal solution moves the work to get() using binary search."),
        N.h4("Building the Solution"),
        N.para("This approach is useful for understanding the problem. Propose it first in an interview, then pivot to the Version List approach."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.history.append(self.arr[:])", {"code": True}), " — arr[:] creates a full shallow copy in O(n). This is the expensive operation."])),
    N.para(N.rich([("return self.history[snap_id][index]", {"code": True}), " — Direct 2D indexing: O(1). Fast get, but memory cost is O(n × number_of_snaps)."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "set()", "snap()", "get()", "Space"],
        ["Brute Force (Full Copy)", "O(1)", "O(n)", "O(1)", "O(n × s)"],
        ["Version List + Binary Search", "O(1)", "O(1)", "O(log s)", "O(set calls)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design — building a custom data structure with multi-operation contracts"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Snapshot Version List — per-key sorted version history with binary search for predecessor queries"])),
    N.callout(
        "When to recognize this pattern: 'What was the value at time T?' queries on mutable data. Writes are sparse (few changes per snapshot). Need O(1) writes, O(log n) historical reads. The phrase 'snap_id', 'timestamp', or 'version' in the problem statement.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same versioned binary search technique:"),
    N.bullet(N.rich([("Time Based Key-Value Store", {"bold": True}), " (Medium, LC 981) — Exact same pattern: per-key sorted list of (timestamp, value) pairs; bisect_right on get()."])),
    N.bullet(N.rich([("Design Hit Counter", {"bold": True}), " (Medium, LC 362) — Time-windowed counting; sorted timestamp list + binary search for window bounds."])),
    N.bullet(N.rich([("My Calendar I", {"bold": True}), " (Medium, LC 729) — Sorted intervals; bisect for insertion point to check overlap."])),
    N.bullet(N.rich([("Find K Closest Elements", {"bold": True}), " (Medium, LC 658) — Binary search for insertion point, then expand window; predecessor lookup logic."])),
    N.bullet(N.rich([("Range Sum Query — Immutable", {"bold": True}), " (Easy, LC 303) — Prefix sums per index; similar 'precompute versioned data, query efficiently' design."])),
    N.bullet(N.rich([("Count of Smaller Numbers After Self", {"bold": True}), " (Hard, LC 315) — Sorted structure + binary search for predecessor count; same O(log n) query pattern."])),
    N.para("These problems share the core technique: maintain a sorted structure of (timestamp/snap_id, value) and use binary search to answer 'what was the value at or before time T?' queries."),
    N.callout("📚 Pattern: Design → Snapshot Version List. Key tool: bisect_right with a sentinel tuple (snap_id, float('inf')) for correct predecessor lookup.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("snapshot_array")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Page URL: https://www.notion.so/{PAGE_ID.replace('-', '')}")
