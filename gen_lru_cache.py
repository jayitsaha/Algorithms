"""gen_lru_cache.py — Notion update for LRU Cache (LC 146)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-816b-9a3a-cd41bbea0974"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=146,
    pattern="Design",
    subpatterns=["Hash Map + Doubly Linked List"],
    tc="O(1)",
    sc="O(capacity)",
    key_insight="HashMap maps key to DLL node pointer; doubly-linked list (with sentinels) keeps MRU-to-LRU order for O(1) eviction.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a data structure that follows the constraints of a "),
        ("Least Recently Used (LRU) cache", {"bold": True}),
        (". Implement the "),
        ("LRUCache", {"code": True}),
        (" class:\n• "),
        ("LRUCache(int capacity)", {"code": True}),
        (" — Initialize with positive size capacity.\n• "),
        ("int get(int key)", {"code": True}),
        (" — Return the value of the key if it exists, otherwise return -1.\n• "),
        ("void put(int key, int value)", {"code": True}),
        (" — Update the value if key exists; otherwise insert the key-value pair. If the number of keys exceeds capacity, evict the least recently used key.\n\nBoth operations must run in "),
        ("O(1) average time complexity", {"bold": True}),
        (".")
    ])),
    N.divider(),
]

# ── Solution 1: Hash Map + DLL (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Hash Map + Doubly Linked List (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a container with a fixed capacity that: (1) lets us look up any stored value by key in O(1), and (2) tracks which item was used longest ago so we can evict it instantly in O(1). These are two different O(1) requirements — no single classic data structure satisfies both."),
        N.h4("What Doesn't Work"),
        N.para("A plain hash map gives O(1) lookup but has no ordering — we can't tell which key was least recently used. A linked list maintains order but lookup is O(n) — we'd have to scan for the key. An array with timestamps gives O(n) eviction (need to scan all). None alone solves both requirements."),
        N.h4("The Key Observation"),
        N.para("If we had a pointer to a node in a linked list, we could remove and re-insert it in O(1). The missing piece is: how to get that pointer instantly? By storing it in a hash map! Hash map value = node pointer. Now lookup is O(1) AND reordering is O(1) because we always have the direct pointer to the node we need to move."),
        N.h4("Building the Solution"),
        N.para("1. Use a doubly-linked list (DLL) to maintain recency order: front (head) = MRU, back (tail) = LRU.\n2. Add dummy sentinel nodes at head and tail — eliminates all null-check edge cases.\n3. Hash map: key → DLL node. get(key): look up node → _remove → _add_head → return val. put(key): if exists, update + refresh; else insert new node + evict if over capacity.\n4. Store key inside each Node so when we evict tail.prev, we can delete it from the map."),
        N.callout("Analogy: Think of a stack of books on your desk. The book you just read goes on TOP (MRU). The book at the BOTTOM hasn't been touched longest (LRU). But you need a post-it on each book telling you its position so you can pull any book out instantly without searching the pile.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""class Node:
    def __init__(self, k=0, v=0):
        self.key = k        # store key for map removal on eviction
        self.val = v
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}               # key -> Node
        self.head = Node()          # MRU sentinel (dummy)
        self.tail = Node()          # LRU sentinel (dummy)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node  # must do before overwriting head.next
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_head(node)
            return
        node = Node(key, value)
        self.map[key] = node
        self._add_head(node)
        if len(self.map) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("Node.__init__", {"code": True}), " — Default args (k=0, v=0) let us create sentinel nodes with just Node(), keeping init clean."])),
    N.para(N.rich([("self.key = k", {"code": True}), " — Store the key inside the node. Critical: when we evict the LRU node, we need its key to remove it from the hash map (del map[lru.key])."])),
    N.para(N.rich([("self.head, self.tail = Node(), Node()", {"code": True}), " — Two dummy sentinels. head.next is always the MRU real node. tail.prev is always the LRU real node. They never hold real data."])),
    N.para(N.rich([("_remove(node)", {"code": True}), " — Two pointer updates: predecessor's next skips over node, successor's prev skips back. Same code for ALL nodes including first and last — sentinels absorb edge cases."])),
    N.para(N.rich([("_add_head(node)", {"code": True}), " — Four pointer updates to insert node between head and head.next. Order matters: set node.next/node.prev BEFORE overwriting head.next, or you lose the reference to the old first node."])),
    N.para(N.rich([("get: _remove then _add_head", {"code": True}), " — 'Move to front' = unlink from current position, re-insert at MRU position. Works whether node is first, last, or middle."])),
    N.para(N.rich([("put: if key in map", {"code": True}), " — Existing key: update value AND refresh recency. Must call _remove + _add_head or the ordering is wrong."])),
    N.para(N.rich([("lru = self.tail.prev", {"code": True}), " — LRU is always the node just before the tail sentinel. O(1) access — no scanning."])),
    N.para(N.rich([("del self.map[lru.key]", {"code": True}), " — Remove evicted node from hash map. This only works because Node stores its own key (lru.key)."])),
    N.divider(),
]

# ── Solution 2: OrderedDict (Alternative) ──
blocks += [
    N.h2("Solution 2 — Python OrderedDict (Concise Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Python's collections.OrderedDict maintains insertion order. It has a move_to_end method that moves a key to either end in O(1), and popitem can remove from either end in O(1). This is exactly what we need, wrapped neatly."),
        N.h4("What Doesn't Work"),
        N.para("This approach doesn't work in languages without an equivalent (Java's LinkedHashMap is similar but needs more setup). And in interviews, the interviewer often wants you to implement from scratch — always ask."),
        N.h4("The Key Observation"),
        N.para("OrderedDict internally uses the same hash map + doubly-linked list, just hidden. move_to_end(key, last=False) = move_to_MRU. popitem(last=True) = remove LRU. The Python approach is O(1) and clean but hides the internal data structure."),
        N.h4("Building the Solution"),
        N.para("Simply subclass OrderedDict or use it directly. get: check if key exists, move_to_end (MRU side = last=False means front), return value. put: update or insert, move_to_end, then if over capacity, popitem(last=True) to remove the LRU."),
    ]),
    N.h3("Code"),
    N.code(
"""from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = OrderedDict()  # maintains insertion/access order

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key, last=False)  # move to MRU position (front)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key, last=False)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=True)  # remove LRU (back)""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("OrderedDict()", {"code": True}), " — Dict that remembers order. move_to_end(key, last=False) = move to front (MRU). move_to_end(key, last=True) = move to back (LRU)."])),
    N.para(N.rich([("move_to_end(key, last=False)", {"code": True}), " — O(1): positions key at the 'first' end. last=False means 'beginning' (our MRU convention)."])),
    N.para(N.rich([("popitem(last=True)", {"code": True}), " — O(1): removes and returns the last (LRU) item. last=True = remove from end = LRU in our ordering."])),
    N.callout("In interviews: mention OrderedDict as the 'Pythonic' approach immediately, then offer to implement from scratch with explicit DLL. Most interviewers will ask for the scratch implementation to test your understanding of the internals.", "💡", "green_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Hash Map + DLL (from scratch)", "O(1) per op", "O(capacity)", "Best for interviews; shows DLL knowledge"],
        ["OrderedDict", "O(1) per op", "O(capacity)", "Pythonic; hides internals"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Hash Map + Doubly Linked List"])),
    N.callout(
        "When to recognize this pattern: 'Design a data structure with O(1) X and O(1) Y simultaneously' where X requires a hash map and Y requires ordered data. Any cache with eviction policy. Any structure needing both fast lookup and fast reordering.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Hash Map + DLL or O(1) design technique:"),
    N.bullet(N.rich([("LFU Cache", {"bold": True}), " (Hard) — Evict least-frequently-used; extends LRU with frequency buckets + nested DLLs per frequency level"])),
    N.bullet(N.rich([("Design Twitter", {"bold": True}), " (Medium) — Ordered feed with recency; 'keep last k' pattern using heap + hash map"])),
    N.bullet(N.rich([("All O(1) Data Structure", {"bold": True}), " (Hard) — Insert/delete/getRandom all O(1); combines hash map with array for O(1) getRandom"])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Monotonic deque maintains ordered window; similar O(1) ordered eviction idea"])),
    N.bullet(N.rich([("Min Stack", {"bold": True}), " (Medium) — Augment each stack entry with auxiliary state; same 'pair every node with metadata' design pattern"])),
    N.bullet(N.rich([("Design HashMap", {"bold": True}), " (Easy) — Build hash map from scratch with chaining; foundational for understanding LRU's hash component"])),
    N.para("These problems share the core technique: combining multiple data structures where each contributes one O(1) capability the others lack."),
    N.callout("📚 Sub-pattern 'Hash Map + Doubly Linked List' — Analysis classification (design pattern, not in standard guide sections). Related guide section: general Design category.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("lru_cache")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
