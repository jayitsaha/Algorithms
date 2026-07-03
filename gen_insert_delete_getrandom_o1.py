"""
gen_insert_delete_getrandom_o1.py
Regenerates the Notion page for LeetCode #380 Insert Delete GetRandom O(1) in-place.
"""
import notion_lib as N

PAGE_ID = "39193418-809c-81e2-93d0-eadcc7de4d74"

# ── 1) Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=380,
    pattern="Design",
    subpatterns=["Array + Hash Map Swap"],
    tc="O(1) average",
    sc="O(n)",
    key_insight="Keep a dense array for O(1) random access + a hash map for O(1) lookup; delete via swap-with-last to avoid array shifting.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ──
SOLUTION_1 = """\
import random

class RandomizedSet:
    def __init__(self):
        self.lst = []           # Dense array of values
        self.val_to_idx = {}    # val -> current index in lst

    def insert(self, val: int) -> bool:
        if val in self.val_to_idx:
            return False        # Duplicate: reject
        self.lst.append(val)
        self.val_to_idx[val] = len(self.lst) - 1
        return True

    def remove(self, val: int) -> bool:
        if val not in self.val_to_idx:
            return False        # Not found
        del_idx = self.val_to_idx[val]
        last = self.lst[-1]
        self.lst[del_idx] = last        # Overwrite gap with tail
        self.val_to_idx[last] = del_idx # Update map for moved element
        self.lst.pop()                  # Remove duplicate tail O(1)
        del self.val_to_idx[val]        # Erase val from map
        return True

    def getRandom(self) -> int:
        return random.choice(self.lst)  # Dense array -> uniform O(1)
"""

SOLUTION_2 = """\
# HashSet only -- FAILS O(1) getRandom requirement
import random

class RandomizedSetBrute:
    def __init__(self):
        self.s = set()

    def insert(self, val: int) -> bool:
        if val in self.s:
            return False
        self.s.add(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.s:
            return False
        self.s.discard(val)
        return True

    def getRandom(self) -> int:
        # O(n) -- must convert set to list first!
        return random.choice(list(self.s))
"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Implement the ", {}),
        ("RandomizedSet", {"code": True}),
        (" class with three methods:", {}),
    ])),
    N.bullet(N.rich([("insert(val)", {"code": True}), (" — Insert val if not present. Return ", {}), ("True", {"code": True}), (" if inserted, ", {}), ("False", {"code": True}), (" if duplicate.", {})])),
    N.bullet(N.rich([("remove(val)", {"code": True}), (" — Remove val if present. Return ", {}), ("True", {}), (" if removed, ", {}), ("False", {"code": True}), (" if not found.", {})])),
    N.bullet(N.rich([("getRandom()", {"code": True}), (" — Return a uniformly random element from the current set.", {})])),
    N.para("Each function must run in O(1) average time. You may not simply scan the full collection for getRandom."),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Array + HashMap Swap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a 'set' (unique values, fast membership) that also supports O(1) random element access. No standard data structure has all three properties — so we must build one from parts."),
        N.h4("What Doesn't Work"),
        N.para("A hash set gives O(1) insert/remove but O(n) getRandom (must convert to list). An array gives O(1) getRandom but O(n) remove (shifting). A sorted tree is O(log n) for all — still too slow."),
        N.h4("The Key Observation"),
        N.para("The array only needs to be dense (no holes), not sorted. This means we can delete from the middle in O(1) by swapping the target element with the last element, then popping the tail — no shifting required. The hash map always tells us where any element lives."),
        N.h4("Building the Solution"),
        N.para("Maintain two structures: lst (the dense array) and val_to_idx (a dict). Insert appends to the array and records the index. Remove looks up the index, swaps with the tail, updates the map for the moved element, pops the tail, and deletes from the map. getRandom does random.choice(lst)."),
        N.callout("Analogy: Think of the array as a 'pool' of swimmers. To remove one swimmer, swap them with the last swimmer in line, then shorten the line. The map is the lifeguard's chart showing each swimmer's lane number.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("self.lst = []", {"code": True}), (" — Dense array of current values. The array must always be filled without gaps (indices 0 to len-1) so that random.choice gives uniform distribution.", {})])),
    N.para(N.rich([("self.val_to_idx = {}", {"code": True}), (" — Hash map from value to its current index in lst. Provides O(1) membership check and O(1) index lookup for deletion.", {})])),
    N.para(N.rich([("if val in self.val_to_idx: return False", {"code": True}), (" — O(1) hash lookup. If already in the set, reject without modification (set semantics).", {})])),
    N.para(N.rich([("self.lst.append(val)", {"code": True}), (" — Append to the tail. O(1) amortized — Python lists double their buffer capacity when full.", {})])),
    N.para(N.rich([("self.val_to_idx[val] = len(self.lst) - 1", {"code": True}), (" — Record the index just assigned to val. This is always the last index since we just appended.", {})])),
    N.para(N.rich([("del_idx = self.val_to_idx[val]", {"code": True}), (" — Look up where val is currently sitting in the array. O(1) hash lookup.", {})])),
    N.para(N.rich([("last = self.lst[-1]", {"code": True}), (" — The tail element will fill the gap. Grab it before we overwrite anything.", {})])),
    N.para(N.rich([("self.lst[del_idx] = last", {"code": True}), (" — Move last into val's position. The array momentarily has a duplicate at the tail, but we fix that next.", {})])),
    N.para(N.rich([("self.val_to_idx[last] = del_idx", {"code": True}), (" — CRITICAL: update the map for the moved element. Without this, the invariant breaks and future operations on 'last' will read a wrong index.", {})])),
    N.para(N.rich([("self.lst.pop()", {"code": True}), (" — Remove the now-redundant tail in O(1). The array is dense again.", {})])),
    N.para(N.rich([("del self.val_to_idx[val]", {"code": True}), (" — Erase val from the map entirely. It no longer exists in the set.", {})])),
    N.para(N.rich([("return random.choice(self.lst)", {"code": True}), (" — Pick a uniformly random index in [0, len-1]. Because the array is dense, every stored value is equally reachable.", {})])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Hash Set Only (Brute Force, Fails O(1) getRandom)"),
    N.toggle_h3("💡 Intuition: Why This Fails", [
        N.h4("Reframe the Problem"),
        N.para("A standard Python set handles insert and remove naturally in O(1). The temptation is to use it directly and 'fix' getRandom by converting to a list."),
        N.h4("What Doesn't Work"),
        N.para("list(self.s) is O(n) — it must copy all n elements into a new list object before random.choice can index into it. This violates the O(1) constraint."),
        N.h4("The Key Observation"),
        N.para("Python sets are implemented as hash tables. Their internal buckets are not guaranteed to be dense or to support O(1) index-based access. There is no way to select a random element from a Python set in O(1) without converting to an indexable structure first."),
        N.h4("Building the Solution"),
        N.para("This brute-force approach is only shown to contrast with Solution 1. Never use it when O(1) getRandom is required."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2, "python"),
    N.h3("Why This Fails"),
    N.para("The single offending line is random.choice(list(self.s)). list(s) iterates over all n elements to build a new list — O(n). This violates the stated requirement. All other operations are correct O(1)."),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "insert", "remove", "getRandom", "Space"],
        ["Array + HashMap (Optimal)", "O(1) avg", "O(1) avg", "O(1)", "O(n)"],
        ["HashSet Only (Brute)", "O(1)", "O(1)", "O(n) ✗", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Design", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Array + Hash Map Swap", {})])),
    N.callout(
        "When to recognize this pattern: 'Design a data structure with O(1) insert, delete, and random element access.' Any time a problem asks for both fast membership tests AND fast random sampling from a dynamic set. The swap-with-last trick is the key unlock.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique or design pattern:"),
    N.bullet(N.rich([("Insert Delete GetRandom O(1) - Duplicates Allowed", {"bold": True}), (" (Hard) — Same design but val_to_idx maps to a set of indices per value. Remove picks any index. (#381)", {})])),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), (" (Medium) — Doubly-linked list + HashMap gives O(1) get and put with recency ordering. (#146)", {})])),
    N.bullet(N.rich([("All O(1) Data Structure", {"bold": True}), (" (Hard) — O(1) increment/decrement/getMaxKey/getMinKey — layered map and doubly-linked list design. (#432)", {})])),
    N.bullet(N.rich([("Shuffle an Array", {"bold": True}), (" (Medium) — Fisher-Yates shuffle uses the same in-place swap concept on an array. (#384)", {})])),
    N.bullet(N.rich([("Random Pick with Blacklist", {"bold": True}), (" (Hard) — Remap blacklisted indices to the valid tail zone using the same positional swap intuition. (#710)", {})])),
    N.bullet(N.rich([("Design HashMap", {"bold": True}), (" (Easy) — Implement a hash map from scratch with separate chaining. (#706)", {})])),
    N.para("These problems all require combining an array for positional access with a hash map for O(1) lookup. The 'swap to avoid shifting' insight is the shared core technique."),
    N.callout("📚 Sub-Pattern: Array + Hash Map Swap — Analysis classification (design problems of this type). Related sub-pattern in guide: Design.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("insert_delete_getrandom_o1")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
