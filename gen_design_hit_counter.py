"""
gen_design_hit_counter.py — Notion update for Design Hit Counter (LeetCode #362)
Run from the Algorithms/ directory: python3 gen_design_hit_counter.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8192-838d-eb5301c89bce"

print(f"Setting properties on page {PAGE_ID}...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=362,
    pattern="Design",
    subpatterns=["Circular Buffer"],
    tc="O(1)",
    sc="O(300) = O(1)",
    key_insight="Map timestamp t to slot t%300; overwrite stale data since it falls outside any future 300-second window.",
    icon="🟡"
)
print("Properties set.")

print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

# ─── Build the page body ───
blocks = []

# Problem Statement
blocks += [
    N.h2("Problem"),
    N.para(
        "Design a hit counter which counts the number of hits received in the past 5 minutes (300 seconds).\n\n"
        "hit(timestamp) — Records a hit at the given timestamp (seconds granularity). "
        "Timestamps are non-decreasing.\n\n"
        "getHits(timestamp) — Returns the number of hits in the past 300 seconds, i.e., "
        "all hits where timestamp - 299 <= hit_timestamp <= timestamp."
    ),
    N.divider(),
]

# ─── Solution 1: Circular Buffer ───
sol1_code = '''\
class HitCounter:
    def __init__(self):
        self.times = [0] * 300   # which second each slot records
        self.hits  = [0] * 300   # hit count for that second

    def hit(self, timestamp: int) -> None:
        i = timestamp % 300
        if self.times[i] != timestamp:   # stale or empty slot
            self.times[i] = timestamp    # claim slot for this second
            self.hits[i]  = 1            # reset count
        else:
            self.hits[i] += 1            # same second: increment

    def getHits(self, timestamp: int) -> int:
        total = 0
        for i in range(300):             # scan all slots (O(1))
            if self.times[i] > timestamp - 300:
                total += self.hits[i]
        return total'''

blocks += [
    N.h2("Solution 1 — Circular Buffer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a counter that answers 'how many events happened in the past 300 seconds?' at any moment. The key constraint: the window is always exactly 300 seconds wide, and timestamps are monotonically non-decreasing."),
        N.h4("What Doesn't Work"),
        N.para("A naive queue stores every individual hit timestamp. On getHits we pop stale entries from the front. This is O(n) space — for a high-traffic API server recording millions of hits per day, the queue grows without bound."),
        N.h4("The Key Observation"),
        N.para("Since the window is exactly 300 seconds, we only ever need one counter per second — and only the last 300 seconds. That's at most 300 counters, always. We can reuse a fixed array of size 300, mapping timestamp t to slot t % 300. Two timestamps that land on the same slot differ by a multiple of 300 seconds — exactly when the older one falls outside any future query window."),
        N.h4("Building the Solution"),
        N.para("Two arrays of size 300: times[] stores which second each slot belongs to, hits[] stores the count. On hit(t): if times[i] == t, increment; else overwrite. On getHits(t): scan all 300 slots, sum those where times[i] > t - 300."),
        N.callout("Analogy: A clock face with 300 tick marks. Each tick represents one second in the current 5-minute cycle. When the clock hand advances 300 seconds past a tick, the old count is erased and a fresh count begins.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("self.times = [0] * 300", {"code": True}),
        " — Fixed 300-slot array. Each slot records which second it currently belongs to. 0 = unused (valid timestamps >= 1).",
    ])),
    N.para(N.rich([
        ("self.hits = [0] * 300", {"code": True}),
        " — Parallel array storing the hit count for the second recorded in times[].",
    ])),
    N.para(N.rich([
        ("i = timestamp % 300", {"code": True}),
        " — Map any timestamp to slot [0..299]. The modulo is a natural circular index that wraps around every 300 seconds.",
    ])),
    N.para(N.rich([
        ("if self.times[i] != timestamp:", {"code": True}),
        " — If the slot records a different second, it has stale data from at least 300 seconds ago. Safe to overwrite.",
    ])),
    N.para(N.rich([
        ("self.times[i] = timestamp; self.hits[i] = 1", {"code": True}),
        " — Claim the slot for this second, reset count to 1 (first hit this second).",
    ])),
    N.para(N.rich([
        ("self.hits[i] += 1", {"code": True}),
        " — Same second, multiple hits: just increment the existing counter.",
    ])),
    N.para(N.rich([
        ("if self.times[i] > timestamp - 300:", {"code": True}),
        " — Strict inequality. A hit exactly 300 seconds old is excluded from the window. This is intentional.",
    ])),
    N.para(N.rich([
        ("total += self.hits[i]", {"code": True}),
        " — Add this slot's aggregated count. Each slot holds all hits for exactly one second.",
    ])),
    N.divider(),
]

# ─── Solution 2: Deque ───
sol2_code = '''\
from collections import deque

class HitCounter:
    def __init__(self):
        self.q = deque()   # stores each hit's timestamp

    def hit(self, timestamp: int) -> None:
        self.q.append(timestamp)   # O(1)

    def getHits(self, timestamp: int) -> int:
        # Pop stale hits from front (monotone: front = oldest)
        while self.q and self.q[0] <= timestamp - 300:
            self.q.popleft()
        return len(self.q)'''

blocks += [
    N.h2("Solution 2 — Deque / Queue (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Store every hit, then discard old ones on query. Since timestamps are monotonically increasing, stale hits are always at the front of a queue."),
        N.h4("What Doesn't Work"),
        N.para("For high-traffic systems with millions of hits, the queue grows unboundedly. Memory usage scales with hit volume, not window size. This is the brute force to mention first in an interview, then optimize."),
        N.h4("The Key Observation"),
        N.para("Timestamps are monotonically non-decreasing, so the oldest hits are always at the front (left) of the deque. We can evict them with O(1) popleft. The deque length after eviction is exactly the answer."),
        N.h4("Building the Solution"),
        N.para("On hit: append to right. On getHits: pop from left while front <= timestamp - 300. Return deque length."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("self.q.append(timestamp)", {"code": True}),
        " — O(1): push this hit's timestamp to the right. Each hit gets its own entry — no aggregation.",
    ])),
    N.para(N.rich([
        ("while self.q and self.q[0] <= timestamp - 300:", {"code": True}),
        " — Since timestamps are monotone, the front is always the oldest. Pop while stale.",
    ])),
    N.para(N.rich([
        ("return len(self.q)", {"code": True}),
        " — Every remaining entry is in-window. No summing needed — just the count.",
    ])),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "hit()", "getHits()", "Space"],
        ["Deque (brute force)", "O(1)", "O(n) amortized", "O(n) unbounded"],
        ["Circular Buffer", "O(1)", "O(300) = O(1)", "O(300) = O(1)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Circular Buffer (Ring Buffer)"])),
    N.callout(
        "When to recognize this pattern: Fixed-size sliding window over time → fixed-size array with modulo indexing. "
        "Signals: (1) window size is a fixed constant, (2) timestamps are monotonically non-decreasing, "
        "(3) O(1) space required regardless of event volume, (4) per-unit-time aggregation is sufficient.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Logger Rate Limiter", {"bold": True}), " (Easy) — Per-message cooldown with last-seen timestamp; same fixed-window eviction. LeetCode #359."])),
    N.bullet(N.rich([("Moving Average from Data Stream", {"bold": True}), " (Easy) — Fixed-size circular buffer for sliding window average. LeetCode #346."])),
    N.bullet(N.rich([("Number of Recent Calls", {"bold": True}), " (Easy) — Count API calls in last 3000ms using a deque. LeetCode #933."])),
    N.bullet(N.rich([("Time Based Key-Value Store", {"bold": True}), " (Medium) — Timestamp-indexed key-value design with binary search. LeetCode #981."])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Fixed window with O(1) per-element via monotonic deque. LeetCode #239."])),
    N.bullet(N.rich([("Design Circular Buffer", {"bold": True}), " (Medium) — Implement the ring buffer data structure from scratch. LeetCode #622."])),
    N.para("These problems share the core pattern: a fixed-size window over ordered data, where older entries are evicted or overwritten because they fall outside the window."),
    N.callout("📚 Sub-pattern: Circular Buffer — Analysis classification (Design pattern; ring buffer specific to fixed time windows).", "📚", "gray_background"),
]

# ─── Embed ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("design_hit_counter")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
