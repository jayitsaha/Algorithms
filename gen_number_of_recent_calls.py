"""
gen_number_of_recent_calls.py
Regenerates the Notion page for LeetCode #933 Number of Recent Calls.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e2-b073-f860b41f017f"

print("Step 1: Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=933,
    pattern="Queues",
    subpatterns=["Sliding Window Queue"],
    tc="O(1) amortized",
    sc="O(W)",
    key_insight="Use a deque sliding window: append new timestamp, evict stale fronts where q[0] < t-3000, return len(q).",
    icon="🟢"
)
print("  Properties set OK.")

print("Step 2: Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks.")

print("Step 3: Building page body...")

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You have a ", {}),
        ("RecentCounter", {"code": True}),
        (" class that counts the number of requests in the past 3000 milliseconds. Implement:\n", {}),
        ("RecentCounter()", {"code": True}),
        (" — initializes the counter with zero recent requests.\n", {}),
        ("ping(t)", {"code": True}),
        (" — adds a new request at time ", {}),
        ("t", {"code": True}),
        (" (in milliseconds) and returns the number of requests that have happened in the past 3000 milliseconds (inclusive of ", {}),
        ("t - 3000", {"code": True}),
        (" and ", {}),
        ("t", {"code": True}),
        ("). It is guaranteed that every call to ", {}),
        ("ping", {"code": True}),
        (" uses a strictly larger value of ", {}),
        ("t", {"code": True}),
        (" than the previous call.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Sliding Window Queue (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Sliding Window Queue with deque (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para('We need to answer "how many calls fell in [t-3000, t]?" for every new call t. This is a moving time window — the left edge advances as t grows.'),
        N.h4("What Doesn't Work"),
        N.para('Brute force: store every timestamp ever, then scan all of them each query. This is O(n) per ping and grows unboundedly in space. For a long-running system (millions of calls), this is a disaster.'),
        N.h4("The Key Observation"),
        N.para('Timestamps arrive in strictly increasing order (guaranteed). So the oldest call is always at the FRONT of any ordered collection. Once a timestamp falls behind the left window edge (t - 3000), it will NEVER be counted again — we can safely discard it. This is the sliding window pattern applied to time.'),
        N.h4("Building the Solution"),
        N.para('Use a deque (double-ended queue) to store in-window timestamps. On each ping(t): (1) append t to the back — it always belongs in its own window. (2) while the front < t - 3000, popleft() — evict stale timestamps. (3) return len(q). The queue always contains exactly the in-window timestamps.'),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}), ("Think of the queue as a train. New passengers board at the back. Old passengers who have ridden past their stop get kicked off the front. At any moment, only the passengers currently on the train are counted.")]),
            "🚂", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
"""from collections import deque

class RecentCounter:
    def __init__(self):
        self.q = deque()        # holds in-window timestamps

    def ping(self, t: int) -> int:
        self.q.append(t)        # new request always in its own window
        while self.q[0] < t - 3000:  # evict stale front elements
            self.q.popleft()    # O(1) — must use deque, not list
        return len(self.q)      # every remaining element is in [t-3000, t]""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), (" — import deque for O(1) front-pop. Using list.pop(0) would be O(n) and defeat the optimization.", {})])),
    N.para(N.rich([("self.q = deque()", {"code": True}), (" — initialize empty queue in constructor. Queue holds timestamps of all requests still inside the current window.", {})])),
    N.para(N.rich([("self.q.append(t)", {"code": True}), (" — enqueue the new timestamp at the back FIRST. This ensures the queue is never empty when we check the front below, because t always satisfies the window condition.", {})])),
    N.para(N.rich([("while self.q[0] < t - 3000:", {"code": True}), (" — the front holds the oldest request. If it's strictly before the left edge of the current window, it's expired and must be removed. Loop continues until front is in-window.", {})])),
    N.para(N.rich([("self.q.popleft()", {"code": True}), (" — O(1) removal from the front. This is the key operation that makes the deque essential.", {})])),
    N.para(N.rich([("return len(self.q)", {"code": True}), (" — the queue now contains exactly the timestamps in [t-3000, t]. Its length is the answer.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force: Store All, Filter Each Time"),
    N.toggle_h3("💡 Intuition: Why This Is the Starting Point", [
        N.h4("Reframe the Problem"),
        N.para('The direct reading: keep track of every call ever made, and each time count how many are in the window.'),
        N.h4("What Doesn't Work"),
        N.para('For long-running systems, storing every timestamp is O(n) space and filtering is O(n) per call. At 1 million calls, every query scans 1 million timestamps.'),
        N.h4("The Key Observation"),
        N.para('This is useful as a starting point to present to the interviewer before optimizing to the queue solution.'),
    ]),
    N.h3("Code"),
    N.code(
"""class RecentCounter:
    def __init__(self):
        self.calls = []

    def ping(self, t: int) -> int:
        self.calls.append(t)
        return sum(1 for c in self.calls if c >= t - 3000)""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.calls = []", {"code": True}), (" — plain list stores every timestamp ever — grows unboundedly.", {})])),
    N.para(N.rich([("self.calls.append(t)", {"code": True}), (" — add new call.", {})])),
    N.para(N.rich([("sum(1 for c in self.calls if c >= t - 3000)", {"code": True}), (" — scan ALL past calls and count those in window. O(n) per query.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time (per ping)", "Space", "Notes"],
        ["Brute Force", "O(n)", "O(n)", "n = total calls. Scans all timestamps."],
        ["Sliding Window Queue ✓", "O(1) amortized", "O(W) = O(1)", "W ≤ 3000. Each ts enqueued/dequeued once."],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Queues", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sliding Window Queue — FIFO queue with front eviction as window advances over monotone-timestamped events.", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ('"How many events in the last X ms/sec?" · Monotone timestamps · Need to discard stale data · Queue front = oldest · Evict when outside left window boundary.', {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sliding Window Queue sub-pattern:"),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard) — Monotonic deque tracks max in fixed window; evict from both ends (#239)", {})])),
    N.bullet(N.rich([("Moving Average from Data Stream", {"bold": True}), (" (Easy) — Fixed-size window with running sum; evict oldest when size exceeds k (#346)", {})])),
    N.bullet(N.rich([("Design Hit Counter", {"bold": True}), (" (Medium) — Nearly identical problem: count hits in past 300 seconds. Same queue approach (#362)", {})])),
    N.bullet(N.rich([("Max Consecutive Ones III", {"bold": True}), (" (Medium) — Variable-size sliding window with constraint on zeros allowed (#1004)", {})])),
    N.bullet(N.rich([("Minimum Size Subarray Sum", {"bold": True}), (" (Medium) — Variable window; shrink when sum exceeds target, grow to find min length (#209)", {})])),
    N.bullet(N.rich([("Longest Subarray of 1s After Deleting One Element", {"bold": True}), (" (Medium) — Variable sliding window with deletion constraint (#1493)", {})])),
    N.para("These problems share the core technique: maintain a sliding window, evict expired/invalid elements from one end, and derive the answer from the window state."),
    N.callout("📚 Reference: Queues section — Sliding Window Queue sub-pattern. Analysis-based classification.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("number_of_recent_calls")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. All 4 ping() calls shown with queue state, window range, eviction events, and code highlighting.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"  Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("  Blocks appended OK.")

print("NOTION OK", PAGE_ID)
