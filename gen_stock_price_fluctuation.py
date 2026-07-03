"""
gen_stock_price_fluctuation.py
Notion update for LeetCode #2034 Stock Price Fluctuation
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81d4-afe2-c856e2b79f41"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2034,
    pattern="Trees",
    subpatterns=["Hash Map + TreeMap"],
    tc="O(log n)",
    sc="O(n)",
    key_insight="Use a sorted map (price→count) alongside a hash map (ts→price); decrement old count on update to keep min/max correct.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────
blocks = []

# ── Problem statement ──────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a stream of stock price records as "),
        ("(timestamp, price)", {"code": True}),
        (" pairs. Records can arrive out of order, and a previously recorded timestamp can be "),
        ("corrected", {"bold": True}),
        (" by submitting a new price for that timestamp. Design a class "),
        ("StockPrice", {"code": True}),
        (" that supports:\n"
         "• update(timestamp, price): Records or corrects the price at the given timestamp.\n"
         "• current(): Returns the price at the latest timestamp.\n"
         "• minimum(): Returns the minimum price over all recorded timestamps.\n"
         "• maximum(): Returns the maximum price over all recorded timestamps."),
    ])),
    N.divider(),
]

# ── Solution 1: Hash Map + SortedDict ─────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Hash Map + SortedDict (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a live, mutable dataset where: (a) we can correct any entry at O(log n), and (b) we can always answer min/max in O(log n). A plain hash map handles (a) but not (b); a sorted array handles (b) but not (a) efficiently."),
        N.h4("What Doesn't Work"),
        N.para("Keeping a single max_price variable fails: when timestamp 1 changes from 10 to 3, max_price=10 becomes stale. We'd have to rescan all prices to find the true max — O(n) per query. Unacceptable."),
        N.h4("The Key Observation"),
        N.para("We need a structure that (1) keeps prices in sorted order so min/max are instant, and (2) supports removal of individual prices when they're overwritten. A sorted map (balanced BST) with price→count gives exactly this. When count drops to 0, we remove the price entirely."),
        N.h4("Building the Solution"),
        N.para("Use TWO structures together:\n"
               "• prices (hash map): timestamp → current price. O(1) lookup of old price before overwriting.\n"
               "• sorted_map (SortedDict / balanced BST): price → count. Keeps prices in sorted order; first key = min, last key = max.\n"
               "On update: look up old price, decrement its count (delete if 0), then set new price and increment its count.\n"
               "On current(): track max_ts separately for O(1).\n"
               "On minimum()/maximum(): first/last BST key."),
        N.callout("Analogy: Think of the sorted_map as a sorted histogram of live prices. Each bar represents how many timestamps currently have that price. When a price is fully replaced, its bar disappears. Min/max are always the leftmost and rightmost bars.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from sortedcontainers import SortedDict\n\n"
        "class StockPrice:\n"
        "    def __init__(self):\n"
        "        self.prices = {}               # timestamp -> current price\n"
        "        self.sorted_map = SortedDict() # price -> count of timestamps with this price\n"
        "        self.max_ts = 0                # track latest timestamp\n\n"
        "    def update(self, timestamp: int, price: int) -> None:\n"
        "        if timestamp in self.prices:\n"
        "            old = self.prices[timestamp]\n"
        "            self.sorted_map[old] -= 1\n"
        "            if self.sorted_map[old] == 0:\n"
        "                del self.sorted_map[old]\n"
        "        self.prices[timestamp] = price\n"
        "        self.sorted_map[price] = self.sorted_map.get(price, 0) + 1\n"
        "        self.max_ts = max(self.max_ts, timestamp)\n\n"
        "    def current(self) -> int:\n"
        "        return self.prices[self.max_ts]\n\n"
        "    def maximum(self) -> int:\n"
        "        return self.sorted_map.peekitem(-1)[0]\n\n"
        "    def minimum(self) -> int:\n"
        "        return self.sorted_map.peekitem(0)[0]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.prices = {}", {"code": True}), " — Hash map for O(1) lookup of any timestamp's current price."])),
    N.para(N.rich([("self.sorted_map = SortedDict()", {"code": True}), " — Balanced BST (sorted by key). First key = minimum price, last key = maximum price, always."])),
    N.para(N.rich([("self.max_ts = 0", {"code": True}), " — Tracks the latest timestamp seen so far; used for O(1) current() queries."])),
    N.para(N.rich([("if timestamp in self.prices:", {"code": True}), " — Is this an update to an existing timestamp? If so, we must remove its old price from sorted_map."])),
    N.para(N.rich([("old = self.prices[timestamp]", {"code": True}), " — Look up the old price before overwriting it. This is why we need the hash map."])),
    N.para(N.rich([("self.sorted_map[old] -= 1", {"code": True}), " — Decrement the count of the old price. One fewer timestamp now has it."])),
    N.para(N.rich([("if self.sorted_map[old] == 0: del ...", {"code": True}), " — If no timestamps remain with this price, remove it from the BST entirely. This keeps min/max correct."])),
    N.para(N.rich([("self.prices[timestamp] = price", {"code": True}), " — Record the new price for this timestamp (overwrites old value)."])),
    N.para(N.rich([("self.sorted_map[price] = ... + 1", {"code": True}), " — Add or increment the new price's count in the BST."])),
    N.para(N.rich([("self.max_ts = max(self.max_ts, timestamp)", {"code": True}), " — Update latest timestamp if this one is newer."])),
    N.para(N.rich([("return self.prices[self.max_ts]", {"code": True}), " — current() is O(1): max_ts is always tracked, hash map lookup is O(1)."])),
    N.para(N.rich([("self.sorted_map.peekitem(-1)[0]", {"code": True}), " — maximum() returns the last key of the BST = the largest price. O(log n)."])),
    N.para(N.rich([("self.sorted_map.peekitem(0)[0]", {"code": True}), " — minimum() returns the first key of the BST = the smallest price. O(log n)."])),
    N.divider(),
]

# ── Solution 2: Two Heaps with Lazy Deletion ───────────────────────────────
blocks += [
    N.h2("Solution 2 — Two Heaps with Lazy Deletion"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If sortedcontainers is unavailable, we need another way to get O(log n) min and max. Python's heapq (binary heap) gives O(1) peek at the minimum — but arbitrary removal is O(n). The trick: don't remove stale entries eagerly; instead, check validity at query time."),
        N.h4("What Doesn't Work"),
        N.para("A single min-heap for minimum() is fine, but we need maximum() too. Python's heapq is a min-heap only. Solution: use two heaps — one for min (stores (price, ts)), one for max (stores (-price, ts) — negate to simulate max-heap)."),
        N.h4("The Key Observation"),
        N.para("When a price is updated, the old entry in the heap is now stale (the timestamp's price has changed). We can't remove it efficiently, but we can detect staleness at query time: if the heap's top entry's price doesn't match prices[timestamp], it's outdated — pop and continue."),
        N.h4("Building the Solution"),
        N.para("On update: just push the new (price, ts) pair to both heaps. On minimum()/maximum(): loop popping the heap top until we find one whose price matches the current price_map entry. This 'lazy deletion' is amortized O(log n) per operation."),
    ]),
    N.h3("Code"),
    N.code(
        "import heapq\n\n"
        "class StockPrice:\n"
        "    def __init__(self):\n"
        "        self.prices = {}       # source of truth: timestamp -> current price\n"
        "        self.min_heap = []     # (price, timestamp) pairs\n"
        "        self.max_heap = []     # (-price, timestamp) — negated for max-heap\n"
        "        self.max_ts = 0\n\n"
        "    def update(self, timestamp: int, price: int) -> None:\n"
        "        self.prices[timestamp] = price  # overwrite; old heap entries become stale\n"
        "        heapq.heappush(self.min_heap, (price, timestamp))\n"
        "        heapq.heappush(self.max_heap, (-price, timestamp))\n"
        "        self.max_ts = max(self.max_ts, timestamp)\n\n"
        "    def current(self) -> int:\n"
        "        return self.prices[self.max_ts]\n\n"
        "    def minimum(self) -> int:\n"
        "        # Pop stale entries until the top matches current price\n"
        "        while self.min_heap[0][0] != self.prices[self.min_heap[0][1]]:\n"
        "            heapq.heappop(self.min_heap)\n"
        "        return self.min_heap[0][0]\n\n"
        "    def maximum(self) -> int:\n"
        "        while -self.max_heap[0][0] != self.prices[self.max_heap[0][1]]:\n"
        "            heapq.heappop(self.max_heap)\n"
        "        return -self.max_heap[0][0]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.prices[timestamp] = price", {"code": True}), " — Overwrites old price. Old heap entries for this timestamp are now stale (they store an outdated price)."])),
    N.para(N.rich([("heapq.heappush(self.min_heap, (price, timestamp))", {"code": True}), " — Push new price (lazy: don't remove old entry, just add new one)."])),
    N.para(N.rich([("heapq.heappush(self.max_heap, (-price, timestamp))", {"code": True}), " — Negate price to simulate max-heap with Python's min-heap."])),
    N.para(N.rich([("while min_heap[0][0] != self.prices[min_heap[0][1]]:", {"code": True}), " — The heap top is (price, ts). Is price still the current price for ts? If not, it's stale."])),
    N.para(N.rich([("heapq.heappop(self.min_heap)", {"code": True}), " — Discard the stale entry. Repeat until we find a valid one."])),
    N.para(N.rich([("return self.min_heap[0][0]", {"code": True}), " — The first valid entry at the top is the true minimum."])),
    N.callout("Amortized analysis: each (price, ts) pair is pushed at most once and popped at most once. Total work across all operations: O(n log n). Per operation: O(log n) amortized.", "⏱️", "gray_background"),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "update()", "current()", "minimum() / maximum()", "Space"],
        ["Brute Force (rescan)", "O(1)", "O(1)", "O(n)", "O(n)"],
        ["Two Heaps (lazy delete)", "O(log n)", "O(1)", "O(log n) amort.", "O(n)"],
        ["Hash Map + SortedDict ✓", "O(log n)", "O(1)", "O(log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (Balanced BST / Sorted Map)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Hash Map + TreeMap — two structures in tandem for O(1) lookup + O(log n) sorted queries"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Design a class with update and min/max queries'\n"
        "• Values can be corrected/overwritten — not just appended\n"
        "• Multiple keys may share the same value (use count, not set)\n"
        "• Need O(1) lookup by key AND sorted-order queries on values simultaneously",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Hash Map + Sorted Structure technique:"),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), " (Hard) — Two heaps to maintain running median; O(log n) insert, O(1) median. #295"])),
    N.bullet(N.rich([("My Calendar II", {"bold": True}), " (Medium) — SortedList to detect triple-booking among overlapping intervals. #731"])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Monotonic deque or sorted structure to track max across a sliding window. #239"])),
    N.bullet(N.rich([("Design Twitter", {"bold": True}), " (Medium) — Hash map + heap for top-k tweet feeds; classic data-structure design. #355"])),
    N.bullet(N.rich([("Count of Smaller Numbers After Self", {"bold": True}), " (Hard) — BST or Fenwick tree to count elements in sorted order as we scan. #315"])),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium) — Hash map + doubly linked list for O(1) mixed get/put; data-structure design. #146"])),
    N.para("These problems share the core technique: combine a hash map for O(1) direct lookup with a sorted structure for O(log n) order-statistic queries."),
    N.callout("📚 Pattern: Trees → Sub-Pattern: Hash Map + TreeMap. Source: Analysis (sorted-container design pattern for mutable price records).", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("stock_price_fluctuation")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
