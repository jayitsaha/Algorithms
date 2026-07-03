"""Notion updater for LFU Cache (LC #460)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81a9-a236-f84af2757288"

# ── 1. Properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=460,
    pattern="Design",
    subpatterns=["Multiple Data Structures"],
    tc="O(1)",
    sc="O(capacity)",
    key_insight="Group items by frequency in OrderedDicts; track min_freq as a scalar for O(1) eviction.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ──
print("Wiping old body...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

# ── 3. Build body ──
PROBLEM_STATEMENT = (
    "Design a data structure that follows the Least Frequently Used (LFU) cache policy. "
    "Implement the LFUCache class:\n"
    "  LFUCache(int capacity) — initialize with capacity.\n"
    "  int get(int key) — return the value if key exists, else -1. Counts as one use.\n"
    "  void put(int key, int value) — insert or update. If cache is full and a new key "
    "arrives, evict the least-frequently-used key. Break frequency ties by LRU (least "
    "recently used among those tied). All operations must run in O(1) average time."
)

SOL1_CODE = '''\
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity                      # max entries
        self.min_freq = 0                        # current minimum frequency
        self.key_map  = {}                       # key -> [value, freq]
        self.freq_map = defaultdict(OrderedDict) # freq -> {key: val}, insertion-ordered

    def get(self, key: int) -> int:
        if key not in self.key_map:
            return -1                            # cache miss
        self._increment(key)                     # access counts; bump freq
        return self.key_map[key][0]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0: return                 # edge: zero-capacity no-op
        if key in self.key_map:                  # UPDATE existing key
            self.key_map[key][0] = value
            self._increment(key)
            return
        if len(self.key_map) == self.cap:        # EVICT: new key, cache full
            evict_key, _ = self.freq_map[self.min_freq].popitem(last=False)
            del self.key_map[evict_key]          # remove evicted key
        # INSERT new key at freq = 1
        self.key_map[key] = [value, 1]
        self.freq_map[1][key] = value
        self.min_freq = 1                        # new key always has freq=1

    def _increment(self, key: int):
        val, freq = self.key_map[key]
        del self.freq_map[freq][key]             # remove from old bucket
        if not self.freq_map[freq]:              # bucket now empty...
            if freq == self.min_freq:            # ...and was the minimum
                self.min_freq += 1               # raise min by exactly 1
        self.freq_map[freq + 1][key] = val       # append to tail of next bucket
        self.key_map[key] = [val, freq + 1]      # update freq in key_map
'''

SOL2_CODE = '''\
# Brute-force O(n) approach — illustrates what we avoid
class LFUCacheNaive:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}   # key -> value
        self.freq  = {}   # key -> frequency

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.freq[key] = self.freq.get(key, 0) + 1
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if not self.cap: return
        if key in self.cache:
            self.cache[key] = value
            self.freq[key]  = self.freq.get(key, 0) + 1
            return
        if len(self.cache) == self.cap:
            # O(n) scan for minimum frequency key
            min_key = min(self.freq, key=self.freq.get)
            del self.cache[min_key], self.freq[min_key]
        self.cache[key] = value
        self.freq[key]  = 1
        # Doesn't correctly break LRU ties — just for contrast
'''

blocks = []

# Problem
blocks += [N.h2("Problem"), N.para(PROBLEM_STATEMENT), N.divider()]

# Solution 1 — Optimal
blocks += [
    N.h2("Solution 1 — HashMap + OrderedDict Buckets (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need O(1) get and O(1) put that can instantly find the least-frequently-used "
            "item (with LRU tie-breaking) without scanning anything. The challenge: 'least "
            "frequently used' is a global property that changes with every access."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Sorting by frequency is O(n log n). A min-heap gives O(log n) eviction but "
            "requires lazy deletion for stale entries. A single LRU list (like LRU Cache) "
            "doesn't track frequency at all. None of these hit O(1)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "What if we group items by their frequency? Each frequency f has a set of keys "
            "that have been accessed exactly f times. Within a group, LRU ordering resolves "
            "ties. If we also track the current minimum frequency as a single integer, "
            "eviction is: 'find the LRU item in the min-frequency group' — all O(1) with "
            "the right structures."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: key_map[key] = [value, freq] for O(1) value and frequency lookup by key.\n"
            "Step 2: freq_map[freq] = OrderedDict{key: val} — groups keys by frequency, "
            "insertion-ordered (oldest=LRU is at front, newest=MRU is at back).\n"
            "Step 3: min_freq integer — tracks the current minimum frequency so we jump "
            "directly to the eviction bucket without scanning.\n"
            "Step 4: _increment(key) atomically moves a key from bucket f to bucket f+1, "
            "and raises min_freq if the old bucket empties at the minimum."
        ),
        N.callout(
            "Analogy: Think of a library. Books are grouped by 'how many times borrowed this "
            "year'. Within each group, the oldest-returned book is the LRU. When we need to "
            "discard a book, we go to the shelf with the fewest-borrowed and take the one "
            "returned longest ago. We always know which shelf has fewest — that's min_freq.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.cap = capacity", {"code": True}), " — Store capacity for the full-check in put()."])),
    N.para(N.rich([("self.min_freq = 0", {"code": True}), " — Will be set to 1 on first insertion; 0 is a sentinel for 'empty cache'."])),
    N.para(N.rich([("self.key_map = {}", {"code": True}), " — Maps each live key to [value, freq]. The single source of truth."])),
    N.para(N.rich([("self.freq_map = defaultdict(OrderedDict)", {"code": True}), " — Maps each frequency to an insertion-ordered dict of keys at that frequency. defaultdict auto-creates new empty OrderedDicts."])),
    N.para(N.rich([("if key not in self.key_map: return -1", {"code": True}), " — Cache miss. Any key not in key_map is either never inserted or was evicted."])),
    N.para(N.rich([("self._increment(key)", {"code": True}), " — Even a get counts as one use, so we bump the key's frequency."])),
    N.para(N.rich([("if key in self.key_map:", {"code": True}), " — Update path: existing key, no eviction needed."])),
    N.para(N.rich([("self.key_map[key][0] = value", {"code": True}), " — Update value in place (index 0 of mutable list)."])),
    N.para(N.rich([("evict_key, _ = self.freq_map[self.min_freq].popitem(last=False)", {"code": True}), " — Pop the first (oldest=LRU) item from the minimum-frequency bucket. O(1)."])),
    N.para(N.rich([("del self.key_map[evict_key]", {"code": True}), " — Remove evicted key from key_map to keep both structures in sync."])),
    N.para(N.rich([("self.freq_map[1][key] = value", {"code": True}), " — Add new key to tail of freq=1 bucket (MRU position; will be LRU last after others are added)."])),
    N.para(N.rich([("self.min_freq = 1", {"code": True}), " — Reset min_freq. New key always enters at freq=1, which is the global minimum."])),
    N.para(N.rich([("del self.freq_map[freq][key]", {"code": True}), " — Remove key from its current frequency bucket."])),
    N.para(N.rich([("if not self.freq_map[freq] and freq == self.min_freq: self.min_freq += 1", {"code": True}), " — Critical: only raise min_freq if the emptied bucket WAS the minimum."])),
    N.para(N.rich([("self.freq_map[freq + 1][key] = val", {"code": True}), " — Append key at the tail (MRU position) of the next frequency bucket."])),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute-Force Linear Scan (Not for Interviews)"),
    N.toggle_h3("💡 Intuition: Why This Fails", [
        N.h4("Reframe the Problem"),
        N.para("For contrast: the naive approach stores key→value and key→freq in two separate dicts, then scans all frequencies to find the minimum during eviction."),
        N.h4("What Doesn't Work"),
        N.para(
            "min(self.freq, key=self.freq.get) scans ALL keys to find the one with the lowest "
            "frequency — O(n) per eviction. For a cache with 10,000 entries, each put that "
            "triggers eviction does 10,000 comparisons. This also doesn't correctly break ties "
            "by LRU order — min() returns an arbitrary key among ties."
        ),
        N.h4("The Key Observation"),
        N.para("This brute-force approach is a useful stepping stone: it makes the correctness logic clear, then we optimize it to O(1) by replacing the scan with the freq_map structure."),
        N.callout("Use this approach to explain the problem to an interviewer, then say 'we can do better in O(1) by grouping items by frequency.'", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("min(self.freq, key=self.freq.get)", {"code": True}), " — O(n) scan: iterates all keys in self.freq to find the one with the minimum value. Correct but slow."])),
    N.para("Also fails LRU tie-breaking: Python's min() returns an arbitrary element among ties, not the least-recently-used one."),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time (get/put)", "Space", "Notes"],
        ["Brute-Force Linear Scan", "O(n) per eviction", "O(n)", "No LRU tie-breaking"],
        ["Min-Heap with lazy deletion", "O(log n)", "O(n)", "Stale entry handling complex"],
        ["HashMap + OrderedDict Buckets ✓", "O(1)", "O(capacity)", "Optimal; interview answer"],
    ]),
    N.divider(),
]

# Pattern
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Multiple Data Structures"])),
    N.callout(
        "When to recognize this pattern: Any problem asking for O(1) operations "
        "on a bounded store with a non-trivial eviction/ordering policy. The signal is "
        "'design a cache' or 'all operations in O(1)' alongside a constraint that "
        "requires knowing a minimum/maximum/ordering without scanning. Use one dict per "
        "lookup dimension needed.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Multiple Data Structures):"),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium) — Simpler predecessor: one dict + one OrderedDict for recency-only eviction. (#146)"])),
    N.bullet(N.rich([("All O(1) Data Structure", {"bold": True}), " (Hard) — O(1) inc/dec/getMaxKey/getMinKey: two dicts + doubly-linked list of value-sets. (#432)"])),
    N.bullet(N.rich([("Maximum Frequency Stack", {"bold": True}), " (Hard) — Pop the most-frequent, LRU tie-break: freq map + group map. (#895)"])),
    N.bullet(N.rich([("Design Twitter", {"bold": True}), " (Medium) — Combine heap + dict + linked list for real-time feed. (#355)"])),
    N.bullet(N.rich([("Design Search Autocomplete System", {"bold": True}), " (Hard) — Trie + frequency map + heap for top-3 suggestions. (#642)"])),
    N.bullet(N.rich([("Snapshot Array", {"bold": True}), " (Medium) — Dict per index + binary search for O(1) snap, O(log n) get. (#1146)"])),
    N.para("These problems all require coordinating two or more data structures where each structure serves a distinct O(1) lookup need."),
    N.callout("📚 Reference: Multiple Data Structures sub-pattern — LFU Cache is the canonical example of this pattern.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("lfu_cache")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# Append in chunks
print("Appending blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
