"""
gen_time_based_key_value_store.py
Notion IN-PLACE update for LeetCode #981 Time Based Key-Value Store
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813e-ab0b-d4063b604d3c"

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=981,
    pattern="Design",
    subpatterns=["Hash Map + Binary Search"],
    tc="O(log n) per get()",
    sc="O(N) total",
    key_insight="Timestamps are strictly increasing per key, so the stored list is always sorted — binary search gives O(log n) floor lookup.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe existing content
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Build body
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a time-based key-value data structure that can store multiple values for the same key at different timestamps and retrieve the key's value at a certain timestamp.\n\n"
         "Implement the ", {}),
        ("TimeMap", {"code": True}),
        (" class:\n\n", {}),
        ("TimeMap()", {"code": True}),
        (" Initializes the object.\n", {}),
        ("set(key, value, timestamp)", {"code": True}),
        (" Stores the key ", {}),
        ("key", {"code": True}),
        (" with value ", {}),
        ("value", {"code": True}),
        (" at the given ", {}),
        ("timestamp", {"code": True}),
        (".\n", {}),
        ("get(key, timestamp)", {"code": True}),
        (" Returns a value such that ", {}),
        ("set(key, value, timestamp_prev)", {"code": True}),
        (" was called previously with ", {}),
        ("timestamp_prev <= timestamp", {"code": True}),
        (" and the largest possible ", {}),
        ("timestamp_prev", {"code": True}),
        (". If there are no values, returns ", {}),
        ('""', {"code": True}),
        (".\n\nConstraint: All timestamps of ", {}),
        ("set()", {"code": True}),
        (" are strictly increasing.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Optimal
sol1_code = '''\
from bisect import bisect_right

class TimeMap:
    def __init__(self):
        # key -> [(timestamp, value), ...] always sorted by timestamp
        self.store = {}

    def set(self, key, value, timestamp):
        # O(1) amortized: append maintains sorted order (problem guarantee)
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        # O(log n): binary search for largest timestamp <= query
        pairs = self.store.get(key, [])
        if not pairs:
            return ""
        ts_list = [ts for ts, _ in pairs]
        # bisect_right(arr, x) - 1 = rightmost index where arr[idx] <= x (floor)
        idx = bisect_right(ts_list, timestamp) - 1
        return pairs[idx][1] if idx >= 0 else ""
'''

blocks += [
    N.h2("Solution 1 — Hash Map + Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a versioned dictionary: same key, multiple values at different timestamps. For get(), we want the 'most recent value at or before a given time' — a floor query on timestamps."),
        N.h4("What Doesn't Work"),
        N.para("A simple dict only stores one value per key — we lose history. A nested dict keyed by timestamp works for exact matches but not floor queries without scanning all keys. Linear scan works (O(n)) but wastes the sorted structure."),
        N.h4("The Key Observation"),
        N.para("The problem states timestamps in set() are strictly increasing. That single constraint means: for each key, the list of (timestamp, value) pairs is ALWAYS SORTED. A sorted list supports binary search — O(log n) floor queries."),
        N.h4("Building the Solution"),
        N.para("Store: dict[key] → list of (ts, val) tuples, always sorted by ts (append-only). set(): O(1) append. get(): binary search with bisect_right(timestamps, query) - 1 to find the floor index. If idx < 0, no valid entry exists."),
        N.callout(
            "Analogy: Think of git commits. Each key is a file; each set() is a commit. get(key, t) is 'git blame at time t' — find the last commit for that file at or before t.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.store = {}", {"code": True}), (" — Dict mapping each key to a list of ", {}), ("(timestamp, value)", {"code": True}), (" tuples. Always sorted by ts per key.", {})])),
    N.para(N.rich([("self.store[key].append((timestamp, value))", {"code": True}), (" — Append only. Since timestamps are strictly increasing, no sorting is needed. O(1) amortized.", {})])),
    N.para(N.rich([("pairs = self.store.get(key, [])", {"code": True}), (" — Safe dict lookup; returns empty list if key was never set.", {})])),
    N.para(N.rich([("ts_list = [ts for ts, _ in pairs]", {"code": True}), (" — Extract just the timestamps for bisect. Note: O(n) extraction; production code uses parallel lists to avoid this.", {})])),
    N.para(N.rich([("idx = bisect_right(ts_list, timestamp) - 1", {"code": True}), (" — ", {}), ("bisect_right(arr, x)", {"code": True}), (" returns the insertion point after any equal elements. Subtract 1 → index of rightmost ts ≤ query (the floor).", {})])),
    N.para(N.rich([("return pairs[idx][1] if idx >= 0 else \"\"", {"code": True}), (" — idx=-1 means all stored timestamps exceed the query. Guard prevents index-out-of-bounds and returns empty string.", {})])),
    N.divider(),
]

# Solution 2 — Production variant
sol2_code = '''\
class TimeMap:
    def __init__(self):
        # Parallel lists: avoids O(n) extraction on every get()
        self.ts   = {}   # key -> [t1, t2, ...] sorted timestamps
        self.vals = {}   # key -> [v1, v2, ...] parallel values

    def set(self, key, value, timestamp):
        self.ts.setdefault(key, []).append(timestamp)
        self.vals.setdefault(key, []).append(value)

    def get(self, key, timestamp):
        if key not in self.ts:
            return ""
        # Direct bisect on timestamp list — no extraction
        idx = bisect_right(self.ts[key], timestamp) - 1
        return self.vals[key][idx] if idx >= 0 else ""
'''

blocks += [
    N.h2("Solution 2 — Production Variant (Parallel Lists)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same algorithm, but the O(n) list comprehension on every get() is wasteful when n is large."),
        N.h4("What Doesn't Work"),
        N.para("Extracting timestamps on every get() is O(n) just for extraction — then O(log n) for search. The extraction cost dominates for large stores."),
        N.h4("The Key Observation"),
        N.para("If we store timestamps and values in SEPARATE parallel lists from the start, we can call bisect_right directly on the timestamp list without extraction — O(log n) with no hidden overhead."),
        N.h4("Building the Solution"),
        N.para("Two dicts: self.ts[key] for timestamps, self.vals[key] for values. set() appends to both. get() calls bisect_right(self.ts[key], timestamp) directly."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.ts = {}; self.vals = {}", {"code": True}), (" — Parallel dicts. Each key maps to two lists: sorted timestamps and corresponding values.", {})])),
    N.para(N.rich([("self.ts.setdefault(key, []).append(timestamp)", {"code": True}), (" — Initialize list on first write, then append. setdefault is cleaner than the manual key-in-dict check.", {})])),
    N.para(N.rich([("idx = bisect_right(self.ts[key], timestamp) - 1", {"code": True}), (" — Direct binary search on timestamp list. No extraction. True O(log n) per get().", {})])),
    N.para(N.rich([("return self.vals[key][idx] if idx >= 0 else \"\"", {"code": True}), (" — Same floor guard. idx=-1 → empty string. Otherwise return from parallel values list.", {})])),
    N.divider(),
]

# Solution 3 — Brute Force
sol3_code = '''\
class TimeMap:
    def __init__(self):
        self.store = {}

    def set(self, key, value, timestamp):
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key, timestamp):
        best = ""
        for ts, val in self.store.get(key, []):
            if ts <= timestamp:
                best = val  # overwrite; last valid ts wins (list is sorted)
            else:
                break       # sorted order: first ts > query means we can stop
        return best
'''

blocks += [
    N.h2("Solution 3 — Brute Force Linear Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Before thinking about binary search, the simplest approach: scan all stored entries for the key, track the latest valid one."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n) per get() where n is the number of entries for that key. For high-frequency get() calls on keys with many entries, this is too slow."),
        N.h4("The Key Observation"),
        N.para("Since the list is sorted, we can break early once we see a timestamp > query. This makes the linear scan correct and slightly faster in practice, but still O(n) worst case."),
        N.h4("Building the Solution"),
        N.para("Iterate through pairs. For each entry with ts <= timestamp, overwrite best. On first ts > timestamp, break. Return best."),
    ]),
    N.h3("Code"),
    N.code(sol3_code),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "set()", "get()", "Space"],
        ["Linear Scan", "O(1)", "O(n)", "O(N)"],
        ["Hash Map + Binary Search (Interview Pick)", "O(1)", "O(log n)", "O(N)"],
        ["Parallel Lists (Production)", "O(1)", "O(log n)", "O(N)"],
    ]),
    N.para("n = entries for one specific key; N = total set() calls across all keys"),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Design", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Hash Map + Binary Search", {})])),
    N.callout(
        "When to recognize this pattern: 'multiple values per key, retrieve by time/index' → sorted list per key + binary search. "
        "Key signal: timestamps (or any ordered attribute) are guaranteed non-decreasing on insert → never sort, just append + bisect. "
        "Two independent lookup dimensions (key AND ordered attribute) → nest a hash map with a sorted structure.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Hash Map + Binary Search / sorted list per key):"),
    N.bullet(N.rich([("Snapshot Array", {"bold": True}), (" (Medium) — Per-index list of (snap_id, val); bisect by snap_id — nearly identical design to this problem (#1146)", {})])),
    N.bullet(N.rich([("My Calendar I", {"bold": True}), (" (Medium) — Store booking intervals in sorted list; bisect to find conflicts (#729)", {})])),
    N.bullet(N.rich([("My Calendar II", {"bold": True}), (" (Medium) — Sorted events; bisect for double-booking detection (#731)", {})])),
    N.bullet(N.rich([("Stock Price Fluctuation", {"bold": True}), (" (Medium) — Timestamped prices with min/max queries using sorted containers (#2034)", {})])),
    N.bullet(N.rich([("Range Module", {"bold": True}), (" (Hard) — Sorted interval list; bisect for overlap detection and range merging (#715)", {})])),
    N.bullet(N.rich([("Design Browser History", {"bold": True}), (" (Medium) — Maintain visit list with a pointer; back/forward navigation (#1472)", {})])),
    N.para("These problems share the core technique: maintain a sorted list (by append or insort), use bisect for O(log n) floor/ceiling/range queries."),
    N.callout("📚 Pattern: Design → Hash Map + Binary Search. The bisect_right(arr, x) - 1 idiom is the canonical floor search in Python.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("time_based_key_value_store")),
    N.para(N.rich([
        ("Step through set() and get() operations visually — see binary search narrow down to the floor timestamp. Use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
