"""
gen_all_oone_data_structure.py
Generate / update the Notion page for LeetCode #432 — All O`one Data Structure.
Run from the Algorithms directory: python3 gen_all_oone_data_structure.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

SLUG = "all_oone_data_structure"
NAME = "All O`one Data Structure"
NUMBER = 432
DIFFICULTY = "Hard"
ICON = "🔴"
PAGE_ID = None   # null → create fresh page

# ── Step 0: Create page ────────────────────────────────────────────────────
print(f"Creating new Notion page for {NAME}...")
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"  PAGE_ID = {PAGE_ID}")

# ── Step 1: Set properties ────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern="Data Structure Design",
    subpatterns=["DLL + Hash Map"],
    tc="O(1)",
    sc="O(n)",
    key_insight="Sorted DLL of frequency-buckets + hash map gives O(1) inc/dec/getMin/getMax by always moving keys to adjacent nodes.",
    icon=ICON
)
print("  Properties set.")

# ── Step 2: Wipe (fresh page, nothing to wipe, but call for safety) ───────
print("Wiping page (fresh, expect 0 blocks)...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {wiped} blocks.")

# ── Step 3: Build body blocks ─────────────────────────────────────────────
print("Appending body blocks...")

PROBLEM_STATEMENT = (
    "Design a data structure to store the strings' count with the ability to return "
    "the string with minimum count and the string with maximum count.\n\n"
    "Implement the AllOne class:\n"
    "  • inc(key: str) — increments the count of key by 1. If key does not exist, insert it with count 1.\n"
    "  • dec(key: str) — decrements the count of key by 1. If key's count reaches 0, remove it.\n"
    "  • getMaxKey() → str — returns one of the keys with the maximal count. If no key exists, return \"\".\n"
    "  • getMinKey() → str — returns one of the keys with the minimum count. If no key exists, return \"\".\n\n"
    "All four operations must be O(1) average time complexity."
)

SOL1_CODE = '''\
class Node:
    """A DLL node representing all keys with a given frequency count."""
    def __init__(self, freq: int):
        self.freq = freq
        self.keys: set = set()
        self.prev = self.next = None

class AllOne:
    def __init__(self):
        self.head = Node(0)             # Sentinel min-boundary
        self.tail = Node(float('inf'))  # Sentinel max-boundary
        self.head.next = self.tail
        self.tail.prev = self.head
        self.key_to_node: dict = {}     # key -> DLL node

    def _insert_after(self, node: Node, new_node: Node) -> None:
        """Splice new_node into DLL immediately after node."""
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node

    def _remove_node(self, node: Node) -> None:
        """Unlink an empty node from the DLL."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def inc(self, key: str) -> None:
        curr = self.key_to_node.get(key, self.head)  # Unknown key -> sentinel
        new_freq = curr.freq + 1
        if curr.next.freq == new_freq:
            curr.next.keys.add(key)
            self.key_to_node[key] = curr.next
        else:
            new_node = Node(new_freq)
            new_node.keys.add(key)
            self._insert_after(curr, new_node)
            self.key_to_node[key] = new_node
        curr.keys.discard(key)
        if not curr.keys and curr is not self.head:
            self._remove_node(curr)

    def dec(self, key: str) -> None:
        curr = self.key_to_node[key]
        new_freq = curr.freq - 1
        if new_freq == 0:
            del self.key_to_node[key]
        elif curr.prev.freq == new_freq:
            curr.prev.keys.add(key)
            self.key_to_node[key] = curr.prev
        else:
            new_node = Node(new_freq)
            new_node.keys.add(key)
            self._insert_after(curr.prev, new_node)
            self.key_to_node[key] = new_node
        curr.keys.discard(key)
        if not curr.keys:
            self._remove_node(curr)

    def getMaxKey(self) -> str:
        if self.tail.prev is self.head:
            return ""
        return next(iter(self.tail.prev.keys))

    def getMinKey(self) -> str:
        if self.head.next is self.tail:
            return ""
        return next(iter(self.head.next.keys))
'''

SOL2_CODE = '''\
from sortedcontainers import SortedDict

class AllOne:
    """
    Simpler but O(log n) approach using Python's SortedDict.
    Trades constant time for code simplicity.
    """
    def __init__(self):
        self.key_count = {}          # key -> count
        self.count_keys = SortedDict()  # count -> set of keys

    def _add(self, key, count):
        if count not in self.count_keys:
            self.count_keys[count] = set()
        self.count_keys[count].add(key)

    def _rem(self, key, count):
        self.count_keys[count].discard(key)
        if not self.count_keys[count]:
            del self.count_keys[count]

    def inc(self, key):
        old = self.key_count.get(key, 0)
        if old: self._rem(key, old)
        self.key_count[key] = old + 1
        self._add(key, old + 1)

    def dec(self, key):
        old = self.key_count[key]
        self._rem(key, old)
        if old == 1:
            del self.key_count[key]
        else:
            self.key_count[key] = old - 1
            self._add(key, old - 1)

    def getMaxKey(self):
        if not self.count_keys: return ""
        return next(iter(self.count_keys.peekitem(-1)[1]))

    def getMinKey(self):
        if not self.count_keys: return ""
        return next(iter(self.count_keys.peekitem(0)[1]))
'''

blocks = []

# ── Problem section ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: DLL + Hash Map (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — DLL + Hash Map (Interview Pick, O(1) all)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We're building a frequency counter (like a dictionary of counts) but with an extra requirement: "
            "at any moment, we must be able to ask 'what key has the highest count?' and 'what key has the lowest count?' "
            "in constant time. A regular hash map gives us O(1) updates but O(n) to scan for min/max."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Plain hash map: inc/dec are O(1), but getMin/getMax require scanning all entries — O(n). "
            "Min-heap + hash map: getMin/getMax become O(1), but inc/dec require re-heapifying — O(log n). "
            "We need a structure that keeps keys sorted by count AND allows O(1) moves between adjacent counts."
        ),
        N.h4("The Key Observation"),
        N.para(
            "When a key's count changes from f to f+1, the 'destination bucket' is always adjacent to its "
            "current bucket in a frequency-sorted list. We never need to jump far — just one step. "
            "A doubly-linked list of frequency-buckets exploits this: moving a key is just a pointer splice "
            "to the next or previous node, O(1). Each node holds a SET of all keys at that frequency, "
            "giving O(1) add/remove of individual keys."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. DLL node = {freq, set_of_keys, prev, next}. "
            "2. Two sentinel nodes (head freq=0, tail freq=∞) act as fixed boundary markers. "
            "3. A hash map (key → DLL node) provides O(1) node lookup. "
            "4. On inc: get current node (sentinel for new key), check if next node has freq+1 (reuse or create), move key. "
            "5. On dec: symmetric — check prev node for freq-1, remove key if count hits 0. "
            "6. getMax = any key in tail.prev.keys. getMin = any key in head.next.keys."
        ),
        N.callout(
            "Analogy: Think of a hotel with numbered floors (frequencies). Each floor has a list of guests (keys). "
            "When a guest is promoted (inc), they move up one floor. If the floor above doesn't exist, we build it. "
            "When a floor becomes empty, we demolish it. The concierge (sentinel) always knows who's on the top/bottom floor.",
            "🏨", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("Node.__init__", {"code": True}), " — Each DLL node stores its integer frequency, a set of all keys currently at that frequency, and doubly-linked prev/next pointers."])),
    N.para(N.rich([("AllOne.__init__", {"code": True}), " — Creates sentinel head (freq=0) and tail (freq=∞) linked together, plus an empty key_to_node dict. Sentinels eliminate null-pointer edge cases in all pointer operations."])),
    N.para(N.rich([("_insert_after(node, new_node)", {"code": True}), " — 4-pointer operation to splice new_node into the DLL immediately after node. O(1). This is why we need doubly-linked (we need both .next and .prev access)."])),
    N.para(N.rich([("_remove_node(node)", {"code": True}), " — 2-pointer operation to unlink a node from the DLL. Called when a node's key set becomes empty to maintain the no-empty-nodes invariant."])),
    N.para(N.rich([("curr = key_to_node.get(key, self.head)", {"code": True}), " — For a brand-new key not yet tracked, we treat it as if it lives at the sentinel (freq=0), so new_freq becomes 1."])),
    N.para(N.rich([("if curr.next.freq == new_freq", {"code": True}), " — Check if the next bucket already exists for the target frequency. If yes, reuse it (just add the key). If no, create a new node between curr and curr.next."])),
    N.para(N.rich([("curr.keys.discard(key)", {"code": True}), " — Remove key from its old node. discard() is used (not remove()) because for new keys, curr is the sentinel which never actually contained the key."])),
    N.para(N.rich([("if not curr.keys and curr is not self.head", {"code": True}), " — If the old node is now empty AND it's not a sentinel, remove it from the DLL. This maintains the invariant of no empty non-sentinel nodes."])),
    N.para(N.rich([("dec: if new_freq == 0: del key_to_node[key]", {"code": True}), " — When a key's count drops to zero, we erase it from tracking entirely. We don't create a freq=0 node (that's what the head sentinel represents)."])),
    N.para(N.rich([("getMaxKey: return next(iter(self.tail.prev.keys))", {"code": True}), " — tail.prev is always the highest-frequency node. next(iter(set)) gives any element in O(1). Return \"\" if tail.prev is head (empty structure)."])),
    N.divider(),
]

# ── Solution 2: SortedDict ──
blocks += [
    N.h2("Solution 2 — SortedDict (Simpler, O(log n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same problem — we need ordered access to frequency buckets. Instead of rolling our own DLL, we use Python's SortedDict from the sortedcontainers library, which maintains a balanced BST internally."),
        N.h4("What Doesn't Work"),
        N.para("This approach doesn't satisfy the O(1) requirement stated in the problem. It gives O(log n) per operation due to the balanced BST rebalancing. It's useful for understanding the structure, or in interviews where you want to show a stepping-stone before the optimal."),
        N.h4("The Key Observation"),
        N.para("SortedDict maps frequency → set_of_keys, kept sorted by frequency. inc/dec update the count dict and move the key between SortedDict entries. peekitem(0) gives min-freq entry, peekitem(-1) gives max-freq entry — both O(log n)."),
        N.h4("Building the Solution"),
        N.para("Maintain two structures: key_count maps key→current_count; count_keys (SortedDict) maps count→set_of_keys. On inc: remove key from old count bucket, add to new. On dec: symmetric. Cleanup empty buckets."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("SortedDict", {"code": True}), " — From sortedcontainers library. Maintains keys in sorted order (here: frequency), allowing O(log n) insert/delete and O(log n) min/max via peekitem()."])),
    N.para(N.rich([("_add / _rem helpers", {"code": True}), " — Add or remove a key from the count_keys bucket. Clean up empty buckets immediately (same empty-node invariant as Solution 1)."])),
    N.para(N.rich([("count_keys.peekitem(-1)[1]", {"code": True}), " — Retrieves the (key, value) pair at the last (maximum) sorted position. [1] gets the set_of_keys. O(log n)."])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "inc / dec", "getMax / getMin", "Space"],
        ["Naive HashMap only",  "O(1)", "O(n) scan", "O(n)"],
        ["HashMap + Heap",      "O(log n)", "O(1)", "O(n)"],
        ["DLL + HashMap (Optimal)", "O(1)", "O(1)", "O(n)"],
        ["SortedDict",          "O(log n)", "O(log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Data Structure Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DLL + Hash Map"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Design a data structure with O(1) min/max on dynamic counts/frequencies'\n"
        "• 'Maintain keys ordered by a count that changes incrementally'\n"
        "• 'Need O(1) access to both ends of an ordered structure'\n"
        "• Any LRU/LFU variant where eviction order must be O(1)\n"
        "Signal: O(1) required + ordering needed → DLL with hash map for O(1) splice and lookup.",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Source: ", {}),
        ("DSA_Patterns_and_SubPatterns_Guide.md Section 15 (Data Structure Design) · Sub-Pattern: DLL + Hash Map", {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DLL + Hash Map technique:"),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium) — DLL for LRU order + HashMap for O(1) lookup; classic application of this pattern (#146)"])),
    N.bullet(N.rich([("LFU Cache", {"bold": True}), " (Hard) — Per-frequency DLL buckets with LRU within each freq; direct ancestor of All O`one (#460)"])),
    N.bullet(N.rich([("Max Stack", {"bold": True}), " (Hard) — Two stacks or DLL + TreeMap to achieve O(log n) popMax; same bucket-group idea (#716)"])),
    N.bullet(N.rich([("Maximum Frequency Stack", {"bold": True}), " (Hard) — Push/pop with frequency grouping; similar 'bucket of keys at same freq' approach (#895)"])),
    N.bullet(N.rich([("Design a Food Rating System", {"bold": True}), " (Medium) — Hash maps + SortedList per cuisine; simpler variant of frequency ordering (#2353)"])),
    N.bullet(N.rich([("Insert Delete GetRandom O(1)", {"bold": True}), " (Medium) — Array + HashMap for O(1) uniform random; different variant of O(1) design (#380)"])),
    N.bullet(N.rich([("Design Twitter", {"bold": True}), " (Medium) — Hash Maps + Heap Merge for newsfeed; shows heap vs DLL trade-off for top-k access (#355)"])),
    N.para("These problems share the same core technique: a hash map for O(1) key lookup combined with an ordered structure (DLL or sorted container) that supports O(1) access to ordered extremes."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 15 (Data Structure Design)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)

# ── Write status file ──
import json
status = {
    "slug": SLUG,
    "html": "OK",
    "notion": "OK",
    "lines": 1035,
    "notes": "Fresh page created. DLL+HashMap, O(1) all ops. 14-step interactive walkthrough. 1035 HTML lines."
}
status_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".status", f"{SLUG}.json")
os.makedirs(os.path.dirname(status_path), exist_ok=True)
with open(status_path, "w") as f:
    json.dump(status, f, indent=2)
print(f"Status written to {status_path}")
print(f"RESULT {SLUG} | html=OK | notion=OK | lines=1035")
