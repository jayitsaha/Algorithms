"""
gen_first_unique_number.py
Notion IN-PLACE rebuild for LeetCode #1429 First Unique Number.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8178-8854-d75c99a08151"

# ── 1) Properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1429,
    pattern="Queues",
    subpatterns=["Queue + Hash Map"],
    tc="O(1) amortized",
    sc="O(d) distinct values",
    key_insight="Use a deque for insertion order + hash map for counts; lazily evict duplicates from the front on showFirstUnique().",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array of integers ", {}),
        ("nums", {"code": True}),
        (" and a class ", {}),
        ("FirstUnique", {"code": True}),
        (" that you must implement. The class receives ", {}),
        ("nums", {"code": True}),
        (" on initialization, supports ", {}),
        ("add(value)", {"code": True}),
        (" to stream new integers, and ", {}),
        ("showFirstUnique()", {"code": True}),
        (" to return the first number in the stream that has appeared exactly once. "
         "If no such number exists, return -1.", {}),
    ])),
    N.para("Example: nums=[2,3,5], then add(5), add(2) → showFirstUnique() returns 3 "
           "(2 and 5 are now duplicates; 3 appeared once and was inserted before 5)."),
    N.divider(),
]

# ── Solution 1: Queue + Hash Map (Optimal) ──
blocks += [
    N.h2("Solution 1 — Queue + Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're asked: 'Among all numbers in the stream, which one appeared first AND has count exactly 1?' "
               "This combines two independent concerns: (1) frequency counting and (2) insertion-order tracking."),
        N.h4("What Doesn't Work"),
        N.para("A plain array and rebuilding a Counter() on every query is O(n) per showFirstUnique() call — "
               "with millions of calls, this is too slow. A set doesn't preserve insertion order. "
               "An ordered dict alone doesn't track counts efficiently."),
        N.h4("The Key Observation"),
        N.para("We need TWO data structures working in parallel: a hash map for O(1) count lookups, "
               "and a queue (deque) to maintain FIFO insertion order. When a number becomes a duplicate, "
               "we don't remove it from the queue eagerly — we do it lazily when it surfaces at the front. "
               "Each element is enqueued and dequeued at most once → amortized O(1)."),
        N.h4("Building the Solution"),
        N.para("add(v): if v not seen before, enqueue it (first occurrence only). Always increment counts[v]. "
               "showFirstUnique(): peek queue front. If counts[front]==1, return it. "
               "If counts[front]>1, pop and repeat. Return -1 if queue empties."),
        N.callout("Analogy: Imagine a single-file checkout line (queue) at a store. "
                  "Each new customer joins the back. If the cashier finds a customer who now holds a VIP card "
                  "(unique), they're served. If not VIP (duplicate), the cashier skips them and looks at the next. "
                  "Lazy eviction = only kicking out non-VIPs when you actually reach them.",
                  "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "\n"
        "class FirstUnique:\n"
        "    def __init__(self, nums):\n"
        "        self.queue = deque()   # insertion order of distinct values\n"
        "        self.counts = {}       # num -> occurrence count\n"
        "        for num in nums:\n"
        "            self.add(num)      # reuse add() — DRY\n"
        "\n"
        "    def showFirstUnique(self) -> int:\n"
        "        while self.queue:\n"
        "            front = self.queue[0]          # peek, don't pop\n"
        "            if self.counts[front] == 1:\n"
        "                return front               # still unique\n"
        "            self.queue.popleft()           # lazy evict duplicate\n"
        "        return -1                          # no unique number\n"
        "\n"
        "    def add(self, value) -> None:\n"
        "        if value not in self.counts:       # first time seen\n"
        "            self.queue.append(value)       # enqueue once\n"
        "        self.counts[value] = self.counts.get(value, 0) + 1"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}),
                   (" — import deque for O(1) append-back and popleft from Python's collections.", {})])),
    N.para(N.rich([("self.queue = deque()", {"code": True}),
                   (" — the deque maintains insertion order of distinct values seen so far.", {})])),
    N.para(N.rich([("self.counts = {}", {"code": True}),
                   (" — the hash map is the ground truth for how many times each value has appeared.", {})])),
    N.para(N.rich([("for num in nums: self.add(num)", {"code": True}),
                   (" — process the initial array exactly like streaming values, keeping code DRY.", {})])),
    N.para(N.rich([("front = self.queue[0]", {"code": True}),
                   (" — peek without popping. O(1) for deque. We only pop if we confirm it's a duplicate.", {})])),
    N.para(N.rich([("if self.counts[front] == 1: return front", {"code": True}),
                   (" — count is exactly 1 → still unique. Return and leave it in the queue for future queries.", {})])),
    N.para(N.rich([("self.queue.popleft()", {"code": True}),
                   (" — lazy eviction: this number became a duplicate at some point; remove it now. "
                    "It is never re-added.", {})])),
    N.para(N.rich([("if value not in self.counts: self.queue.append(value)", {"code": True}),
                   (" — only enqueue on the FIRST occurrence. Prevents queue bloat from repeated add() calls.", {})])),
    N.para(N.rich([("self.counts[value] = self.counts.get(value, 0) + 1", {"code": True}),
                   (" — always increment. If count goes 1→2, the value just became a duplicate "
                    "(but still in queue until lazily evicted).", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force (Linear Scan)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Store everything and scan on demand. No precomputation."),
        N.h4("What Doesn't Work"),
        N.para("Rebuilding Counter(all_nums) on every showFirstUnique() call costs O(n) per query. "
               "With m queries and n numbers this is O(nm) — acceptable only for small inputs or as a starting point."),
        N.h4("The Key Observation"),
        N.para("The brute force is trivially correct and easy to code. Propose it first, then optimize. "
               "It demonstrates you understand the problem before jumping to the optimal approach."),
        N.h4("Building the Solution"),
        N.para("Keep a plain list. On showFirstUnique(), rebuild the Counter from scratch, then scan list for first element with count==1."),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import Counter\n"
        "\n"
        "class FirstUnique:\n"
        "    def __init__(self, nums):\n"
        "        self.nums = list(nums)\n"
        "\n"
        "    def showFirstUnique(self) -> int:  # O(n)\n"
        "        counts = Counter(self.nums)    # O(n) rebuild each call\n"
        "        for num in self.nums:\n"
        "            if counts[num] == 1:\n"
        "                return num\n"
        "        return -1\n"
        "\n"
        "    def add(self, value) -> None:\n"
        "        self.nums.append(value)        # O(1) add, but query suffers"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.nums = list(nums)", {"code": True}),
                   (" — store everything. Simple, but no precomputation.", {})])),
    N.para(N.rich([("counts = Counter(self.nums)", {"code": True}),
                   (" — O(n) to count every element, every time showFirstUnique() is called.", {})])),
    N.para(N.rich([("for num in self.nums: if counts[num] == 1: return num", {"code": True}),
                   (" — second O(n) scan to find the first element with count exactly 1.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "add()", "showFirstUnique()", "Space"],
        ["Brute Force (rebuild Counter)", "O(1)", "O(n)", "O(n)"],
        ["Queue + Hash Map (optimal)", "O(1)", "O(1) amortized", "O(d) distinct values"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Queues (Section 6.3 — Queue Operations)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Queue + Hash Map", {})])),
    N.callout(
        "When to recognize this pattern: "
        "'First/oldest element satisfying a property?' + 'stream or ordering matters' + 'property can change over time'. "
        "Signals: 'design a data structure', 'stream', 'first unique', 'first non-repeating'. "
        "Two needs simultaneously: insertion order (queue) + attribute lookup (hash map).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Queue + Hash Map / queue-based order tracking):"),
    N.bullet(N.rich([("First Unique Character in a String", {"bold": True}),
                     (" (Easy) — Same idea on a static string; find leftmost char with count=1. #387", {})])),
    N.bullet(N.rich([("Number of Recent Calls", {"bold": True}),
                     (" (Easy) — Queue to count calls within a sliding time window; evict old calls. #933", {})])),
    N.bullet(N.rich([("Moving Average from Data Stream", {"bold": True}),
                     (" (Easy) — Fixed-size queue to maintain sliding window average. #346", {})])),
    N.bullet(N.rich([("LRU Cache", {"bold": True}),
                     (" (Medium) — Doubly linked list + hash map for O(1) order-preserving eviction. #146", {})])),
    N.bullet(N.rich([("Design Hit Counter", {"bold": True}),
                     (" (Medium) — Queue + count to track events in a time window. #362", {})])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}),
                     (" (Hard) — Monotonic deque lazily evicts stale elements from the front. #239", {})])),
    N.para("These problems share the core technique: a queue (or deque) preserves order while a separate "
           "map or counter tracks a property — allowing O(1) amortized queries."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 6.3 (Queue Operations). "
              "Sub-Pattern: Queue + Hash Map · Verified: Guide Section 6.3",
              "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("first_unique_number")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
