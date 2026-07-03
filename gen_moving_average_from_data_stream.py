"""
gen_moving_average_from_data_stream.py
Regenerates Notion page for LeetCode #346 — Moving Average from Data Stream
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-817a-aca5-d4ad4c5cf116"
SLUG    = "moving_average_from_data_stream"

# ── 1) Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=346,
    pattern="Queues",
    subpatterns=["Queue with Size Limit"],
    tc="O(1)",
    sc="O(size)",
    key_insight="Maintain a bounded deque and a running sum; add new value, subtract evicted oldest — O(1) per call.",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe existing body ──
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3) Rebuild body ──
PROBLEM_STATEMENT = (
    "Design a class MovingAverage that computes the moving average of a sliding window "
    "of size size from a data stream. Implement: "
    "__init__(size) — initialises the object with window capacity size; "
    "next(val) — returns the moving average of the last min(count, size) integers, "
    "where count is the total number of values inserted so far."
)

SOL1_CODE = """\
from collections import deque

class MovingAverage:
    def __init__(self, size: int):
        self.size = size
        self.queue = deque()        # holds current window values (oldest at front)
        self.window_sum = 0         # invariant: always == sum(queue)

    def next(self, val: int) -> float:
        self.queue.append(val)      # new value enters at the back
        self.window_sum += val      # keep sum in sync
        if len(self.queue) > self.size:
            self.window_sum -= self.queue.popleft()  # evict oldest, subtract
        return self.window_sum / len(self.queue)     # len <= size handles warm-up
"""

SOL2_CODE = """\
class MovingAverage:
    def __init__(self, size: int):
        self.size = size
        self.buf = [0] * size       # pre-allocated ring buffer; no dynamic allocation
        self.head = 0               # next write position (wraps with modulo)
        self.count = 0              # actual elements in window (caps at size)
        self.window_sum = 0

    def next(self, val: int) -> float:
        self.window_sum -= self.buf[self.head]       # subtract old value in this slot
        self.buf[self.head] = val                    # overwrite with new value
        self.window_sum += val                       # add new value to sum
        self.head = (self.head + 1) % self.size      # advance head, wrap around
        self.count = min(self.count + 1, self.size)  # cap count at size
        return self.window_sum / self.count
"""

blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Bounded Deque + Running Sum (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to return the average of the last size elements on every call. "
            "The window shifts by one element per call — oldest element leaves, newest enters."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: store the last size values in a list, sum them every call — O(size) per call. "
            "Correct, but for size = 10 000 called 10 000 times, that is 10^8 operations. "
            "We're recomputing a sum where only one element changed."
        ),
        N.h4("The Key Observation"),
        N.para(
            "new_sum = old_sum + new_value - evicted_value. "
            "If we maintain the sum alongside the window, we can update it in O(1) per call. "
            "The queue tells us which value to evict — it's always the oldest, sitting at the front (FIFO)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Keep a deque (FIFO queue) of at most size elements.\n"
            "2. On each next(val) call: append val to back, add val to window_sum.\n"
            "3. If len(queue) > size: pop from front (oldest), subtract from window_sum.\n"
            "4. Return window_sum / len(queue). Use len(queue), not size — queue may not be full yet."
        ),
        N.callout(
            "Analogy: Think of a conveyor belt that holds exactly size boxes. "
            "A new box slides onto one end; if the belt is full, the oldest box falls off the other. "
            "You track the total weight of boxes on the belt. Adding a box: add its weight. "
            "Box falls off: subtract its weight. You never re-weigh all boxes from scratch.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), " — Import deque for O(1) popleft(). A plain list's pop(0) is O(n) because Python shifts all elements left."])),
    N.para(N.rich([("self.size = size", {"code": True}), " — Store the maximum window capacity. Used in the eviction check."])),
    N.para(N.rich([("self.queue = deque()", {"code": True}), " — The sliding window. Oldest element at front (left), newest at back (right)."])),
    N.para(N.rich([("self.window_sum = 0", {"code": True}), " — The running total. Invariant: always equals sum(self.queue) after every operation."])),
    N.para(N.rich([("self.queue.append(val)", {"code": True}), " — New value enters the window at the back. O(1) for deque."])),
    N.para(N.rich([("self.window_sum += val", {"code": True}), " — Keep sum in sync: sum(queue) increased by val, so window_sum increases by val."])),
    N.para(N.rich([("if len(self.queue) > self.size:", {"code": True}), " — After appending, check if we exceeded capacity. Evict only when we're over."])),
    N.para(N.rich([("self.window_sum -= self.queue.popleft()", {"code": True}), " — Remove oldest element (front) and subtract its value from the sum simultaneously. One line keeps both in sync."])),
    N.para(N.rich([("return self.window_sum / len(self.queue)", {"code": True}), " — Divide by the actual queue length (≤ size), not by size. Critical during the warm-up phase before the window fills."])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Circular Buffer (Production-Grade Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same goal: O(1) per call. But instead of a dynamic data structure (deque), "
            "we pre-allocate a fixed array of exactly size slots and reuse them cyclically."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A circular (ring) buffer is an array where a head pointer wraps around: "
            "head = (head + 1) % size. The slot at head always holds the oldest value. "
            "When we write a new value to head, it overwrites the oldest — effectively evicting it. "
            "No dynamic memory allocation ever occurs."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialise buf = [0]*size, head = 0, count = 0, window_sum = 0.\n"
            "2. On next(val): subtract buf[head] from sum (old value in that slot), "
            "write val to buf[head], add val to sum, advance head = (head+1)%size, "
            "increment count (capped at size).\n"
            "3. Return window_sum / count."
        ),
        N.callout(
            "Why this is impressive in interviews: shows knowledge of data structure internals, "
            "no GC pressure (fixed allocation), constant memory footprint. "
            "Mention it after the deque solution as a follow-up optimisation.",
            "🔬", "purple_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.buf = [0] * size", {"code": True}), " — Fixed-size ring. Initialised to 0 so the first subtract in next() is always safe (0 - 0 = 0)."])),
    N.para(N.rich([("self.head = 0", {"code": True}), " — Points to the next slot to write — which also holds the value to evict (the oldest)."])),
    N.para(N.rich([("self.count = min(self.count + 1, self.size)", {"code": True}), " — Tracks how many elements are actually in the window (cannot exceed size). Used as divisor."])),
    N.para(N.rich([("self.window_sum -= self.buf[self.head]", {"code": True}), " — Subtract the old occupant of slot head before overwriting it. During warm-up, slots are 0 so this subtracts nothing."])),
    N.para(N.rich([("self.head = (self.head + 1) % self.size", {"code": True}), " — Advance head. When head reaches size, it wraps to 0, creating the circular effect."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time / call", "Space", "Notes"],
        ["Recompute from scratch", "O(size)", "O(size)", "Correct but wasteful for large windows"],
        ["Deque + Running Sum (✓ Interview)", "O(1)", "O(size)", "Clean, idiomatic Python; interview pick"],
        ["Circular Buffer", "O(1)", "O(size) fixed", "No dynamic allocation; production-grade"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Queues"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Queue with Size Limit — bounded FIFO queue with O(1) sliding window aggregate"])),
    N.callout(
        "When to recognise this pattern:\n"
        "• 'Last k elements', 'moving/rolling/sliding average or sum'\n"
        "• 'Design a class' + stream input + window size constraint\n"
        "• If aggregate is sum/count → O(1) with running total.\n"
        "  If aggregate is max/min → monotonic deque.\n"
        "  If aggregate is median → two heaps.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (bounded queue / sliding window aggregate):"),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Monotonic deque tracks the max instead of sum; O(1) amortised per step (#239)"])),
    N.bullet(N.rich([("Number of Recent Calls", {"bold": True}), " (Easy) — Count API calls in last 3000ms; evict old timestamps from a bounded queue (#933)"])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), " (Hard) — Two heaps maintain the rolling median; O(log n) per insert (#295)"])),
    N.bullet(N.rich([("Design Circular Queue", {"bold": True}), " (Medium) — Implement bounded FIFO with fixed array and head/tail pointer arithmetic (#622)"])),
    N.bullet(N.rich([("Maximum Average Subarray I", {"bold": True}), " (Easy) — Find the fixed-size window with highest average; identical running-sum trick (#643)"])),
    N.bullet(N.rich([("First Unique Character in a Stream", {"bold": True}), " (Medium) — Bounded queue + frequency map; evict non-unique entries (#1429)"])),
    N.para("These problems share the core technique: maintain a bounded window with O(1) state updates."),
    N.callout("📚 Pattern: Queues → Sub-Pattern: Queue with Size Limit (Analysis-based classification — stream input + bounded window + O(1) aggregate update)", "📚", "gray_background"),
]

# Embed block
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK  {PAGE_ID}  ({len(blocks)} blocks appended)")
