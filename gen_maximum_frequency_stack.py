"""
Notion update script for Maximum Frequency Stack (#895).
Run from the Algorithms directory alongside notion_lib.py.
"""
import notion_lib as N

PAGE_ID = "39193418-809c-814d-a36e-d8622821c62c"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=895,
    pattern="Data Structure Design",
    subpatterns=["Frequency Buckets"],
    tc="O(1) per operation",
    sc="O(n)",
    key_insight="Bucket elements by frequency; group[f] is a stack of all values at freq f. maxfreq tracks the peak and adjusts by ±1 — frequency is monotone.",
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body blocks ───────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a stack-like data structure that supports two operations:\n\n",{}),
        ("push(val)", {"code":True}),
        (" — push an integer onto the stack.\n",{}),
        ("pop()", {"code":True}),
        (" — remove and return the element with the ", {}),
        ("highest push frequency", {"bold":True}),
        (". If multiple elements are tied for highest frequency, return the one that was pushed most recently.",{})
    ])),
    N.para("Both operations must run in O(1) time."),
    N.divider(),
]

# ── Solution 1 — Frequency Bucket Stacks (Interview Pick) ──────────────────
blocks += [
    N.h2("Solution 1 — Frequency Bucket Stacks (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a data structure that always knows the most-frequently-pushed element AND can break ties by recency. The challenge: keeping both pieces of info up-to-date in O(1) per operation."),
        N.h4("What Doesn't Work"),
        N.para("A heap keyed by (−frequency, −push_time) works correctly but costs O(log n) per operation — the problem clearly hints at O(1). A sorted list has the same problem. We can't afford any sorting or searching."),
        N.h4("The Key Observation"),
        N.para("Frequency is monotone: each push increments a value's frequency by exactly 1, and each pop decrements it by exactly 1. So the maximum frequency can only change by ±1. We don't need to sort frequencies — we just track the current maximum as a single integer and adjust it by 1 when needed."),
        N.h4("Building the Solution"),
        N.para("Since we want elements grouped by frequency, create group[f] as a list (stack) of all elements currently at frequency f. This list preserves push order, so group[f][-1] is always the most recently pushed element at that frequency — which is exactly what we need for tie-breaking. Maintain maxfreq = the largest f with a non-empty group[f]."),
        N.callout("Analogy: Imagine a hotel with floors numbered by visit count. Each guest is on the floor matching how many times they've visited. The concierge (maxfreq) always knows the highest occupied floor. When the top guest checks out, they drop to the floor below — and if that floor empties, the concierge notes the new top floor.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""class FreqStack:
    def __init__(self):
        self.freq_count = {}   # val -> current push count
        self.group = {}        # freq_level -> stack (list) of vals at that freq
        self.maxfreq = 0       # highest frequency with >= 1 element

    def push(self, val: int) -> None:
        f = self.freq_count.get(val, 0) + 1   # new frequency for val
        self.freq_count[val] = f
        if f not in self.group:
            self.group[f] = []
        self.group[f].append(val)              # add to freq bucket (preserves order)
        self.maxfreq = max(self.maxfreq, f)    # update max if new high

    def pop(self) -> int:
        val = self.group[self.maxfreq].pop()   # top of max-freq bucket -> O(1)
        self.freq_count[val] -= 1              # val's freq drops by 1
        if not self.group[self.maxfreq]:       # if bucket now empty...
            self.maxfreq -= 1                  # ...lower max by exactly 1 (always correct)
        return val"""),
    N.h3("Line by Line"),
    N.para(N.rich([("freq_count = {}", {"code":True}), " — maps each value to its current push count. Used to know which frequency bucket to put a newly pushed value into."])),
    N.para(N.rich([("group = {}", {"code":True}), " — maps a frequency level ", ("f", {"code":True}), " to a list of all values currently at that frequency. The list acts as a stack: append on push, pop on pop. This preserves push order, enabling correct tie-breaking."])),
    N.para(N.rich([("maxfreq = 0", {"code":True}), " — tracks the highest active frequency. Updated on push; decremented by 1 on pop if the bucket empties."])),
    N.para(N.rich([("f = freq_count.get(val, 0) + 1", {"code":True}), " — computes val's new frequency. Using ", ("get(val, 0)", {"code":True}), " gracefully handles the first push of a value (defaults to 0)."])),
    N.para(N.rich([("group[f].append(val)", {"code":True}), " — adds val to its frequency bucket. The append preserves temporal order; the most recently pushed element at freq f is always at the end of the list."])),
    N.para(N.rich([("self.maxfreq = max(self.maxfreq, f)", {"code":True}), " — only needs a simple max comparison. If val's new frequency equals maxfreq+1, we update; otherwise maxfreq stays."])),
    N.para(N.rich([("val = self.group[self.maxfreq].pop()", {"code":True}), " — removes and returns the most recently pushed element at the highest frequency. Both conditions of the problem spec are satisfied in this one line."])),
    N.para(N.rich([("self.freq_count[val] -= 1", {"code":True}), " — val's frequency just dropped by 1. Its group[maxfreq] entry was removed; its group[maxfreq-1] entry (if any, from a prior push) becomes the live entry."])),
    N.para(N.rich([("if not self.group[self.maxfreq]: self.maxfreq -= 1", {"code":True}), " — if the max-frequency bucket is now empty, decrement maxfreq. This is always correct because frequencies are contiguous and monotone — the next non-empty group must be at maxfreq−1."])),
    N.divider(),
]

# ── Solution 2 — Heap (suboptimal) ─────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Max Heap (O(log n), easier to derive first)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to always pop the element that maximizes (frequency, push_time). A max-heap ordered by (−frequency, −push_time) gives exactly this priority ordering."),
        N.h4("What Doesn't Work"),
        N.para("This approach works correctly — it's just not O(1). Each heappush and heappop costs O(log n). Worth proposing as a first solution before optimizing."),
        N.h4("The Key Observation"),
        N.para("By negating both frequency and push_time in the heap tuple, Python's min-heap acts as a max-heap: highest frequency wins; ties broken by highest push_time (most recent)."),
        N.h4("Building the Solution"),
        N.para("Track a global push timer (increment on every push). Heap key: (−freq, −push_time, val). Push: increment freq, push to heap. Pop: heappop returns the winner automatically."),
    ]),
    N.h3("Code"),
    N.code("""import heapq

class FreqStack:
    def __init__(self):
        self.freq = {}
        self.heap = []    # max-heap via negation: (-freq, -push_time, val)
        self.time = 0

    def push(self, val):
        self.freq[val] = self.freq.get(val, 0) + 1
        self.time += 1
        heapq.heappush(self.heap, (-self.freq[val], -self.time, val))

    def pop(self):
        _, _, val = heapq.heappop(self.heap)
        self.freq[val] -= 1
        return val"""),
    N.h3("Line by Line"),
    N.para(N.rich([("(-freq, -push_time, val)", {"code":True}), " — the heap key. Negating freq and time turns Python's min-heap into a max-heap: the element with the largest freq (most negative −freq) is at the top; ties broken by largest push_time."])),
    N.para(N.rich([("heappush", {"code":True}), " and ", ("heappop", {"code":True}), " — each costs O(log n) due to the heap sift operations. Space is O(n) — each push adds one heap entry."])),
    N.callout("Trade-off: The heap approach is simpler to reason about and verify correct. In an interview, propose this first to demonstrate you understand the problem, then offer to optimize to O(1) with frequency buckets.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",               "push()",    "pop()",    "Space"],
        ["Heap (−freq, −time)",    "O(log n)",  "O(log n)", "O(n)"],
        ["Frequency Buckets ✓",    "O(1)",      "O(1)",     "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold":True}), "Data Structure Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold":True}), "Frequency Buckets"])),
    N.callout(
        "When to recognize this pattern: 'Design a data structure with O(1) access to most/least frequent element' + 'tie-break by recency' + frequencies change one step at a time → Frequency Buckets with monotone maxfreq tracking.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("LFU Cache", {"bold":True}), " (Hard) — Same frequency-bucket structure but with capacity-based eviction; also tracks minfreq for O(1) eviction (#460)"])),
    N.bullet(N.rich([("LRU Cache", {"bold":True}), " (Medium) — O(1) access by recency using hash map + doubly linked list (#146)"])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold":True}), " (Medium) — Bucket sort by frequency, the same freq→list grouping idea applied to batch queries (#347)"])),
    N.bullet(N.rich([("Sort Characters By Frequency", {"bold":True}), " (Medium) — Frequency bucket sort applied to string characters (#451)"])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold":True}), " (Hard) — Two-heap design for O(log n) insert, O(1) median access (#295)"])),
    N.bullet(N.rich([("Max Stack", {"bold":True}), " (Hard) — Design a stack with O(1) max retrieval — uses auxiliary stack or sorted structure (#716)"])),
    N.bullet(N.rich([("Insert Delete GetRandom O(1)", {"bold":True}), " (Medium) — Array + hash map swap design for O(1) uniform random access (#380)"])),
    N.para("These problems share the core challenge: maintaining O(1) access to a priority-ordered element while supporting O(1) insertion and deletion."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 15 — Data Structure Design. Sub-Pattern: Frequency Buckets. Source: Guide Section 15.", "📚", "gray_background"),
]

# ── Interactive Embed ──────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_frequency_stack")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic":True,"color":"gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
