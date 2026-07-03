"""
gen_max_stack.py — Notion regeneration for Max Stack (LC #716)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8172-98c6-e06634f10489"

# ── 1) Properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=716,
    pattern="Design",
    subpatterns=["Two Stacks or DLL + TreeMap"],
    tc="O(log n)",
    sc="O(n)",
    key_insight="Parallel max-tracking stack stores running max per level; lazy deletion enables O(log n) popMax via SortedList.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build new body ─────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para("Design a max stack data structure that supports the following operations:\n\npush(x) - push element x onto the stack.\npop() - remove the element on top of the stack and return it.\ntop() - get the element on the top.\npeekMax() - retrieve the maximum element in the stack.\npopMax() - retrieve the maximum element in the stack, and remove it. If you find more than one maximum elements, only remove the top-most one."),
    N.divider(),
]

# Solution 1 — Two Stacks (Interview Pick)
SOL1_CODE = """\
class MaxStack:
    def __init__(self):
        self.stack = []     # main stack, actual values
        self.max_stk = []   # max_stk[i] = max of stack[0..i]

    def push(self, x: int) -> None:          # O(1)
        self.stack.append(x)
        cur = max(x, self.max_stk[-1] if self.max_stk else x)
        self.max_stk.append(cur)

    def pop(self) -> int:                    # O(1)
        self.max_stk.pop()
        return self.stack.pop()

    def top(self) -> int:                    # O(1)
        return self.stack[-1]

    def peekMax(self) -> int:                # O(1)
        return self.max_stk[-1]

    def popMax(self) -> int:                 # O(n) worst, O(1) amortized
        max_val = self.peekMax()
        buffer = []
        while self.stack[-1] != max_val:
            buffer.append(self.pop())        # self.pop() keeps both stacks in sync
        self.pop()                           # remove the max
        for val in reversed(buffer):         # push back in original order
            self.push(val)
        return max_val
"""

blocks += [
    N.h2("Solution 1 — Two Stacks (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You need O(1) access to two different elements simultaneously: the most-recently-inserted (top) and the largest-valued (max). A single stack gives O(1) for the first but O(n) for the second. The reframe: can you maintain a shadow structure that always knows the current max?"),
        N.h4("What Doesn't Work"),
        N.para("A single stack gives no efficient max. A max-heap gives O(log n) max but O(log n) pop-by-position for normal stack ops — you can't pop by insertion order efficiently. A naive scan for max on every peekMax/popMax is O(n) per call."),
        N.h4("The Key Observation"),
        N.para("At every stack level i, the maximum of stack[0..i] can be computed as max(stack[i], max_of_stack[0..i-1]). This recurrence lets us build a parallel max-stack where max_stk[i] = running max. We only need to compute it once per push — O(1)."),
        N.h4("Building the Solution"),
        N.para("Maintain two stacks in lockstep. On push(x): append x to main stack, append max(x, current_max) to max_stk. On pop: remove from both. On peekMax: return max_stk[-1]. For popMax: find max_val, buffer elements above it, remove it, push buffer back using self.push() (which rebuilds the max_stk invariant at each level)."),
        N.callout("Analogy: Think of the max_stk as a 'high-water mark' record. At each level, you record the highest water seen so far. Popping is like erasing the latest record. The current high-water mark is always at the top of max_stk.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.stack = []", {"code": True}), " — main stack, stores actual values in insertion order"])),
    N.para(N.rich([("self.max_stk = []", {"code": True}), " — parallel stack; max_stk[i] = max of stack[0..i] at all times"])),
    N.para(N.rich([("push", {"code": True}), " — appends x to stack, then computes running max: ", ("max(x, max_stk[-1])", {"code": True}), " if non-empty, else x itself. Appends to max_stk. O(1)."])),
    N.para(N.rich([("pop", {"code": True}), " — pops both stacks together. ", ("max_stk.pop()", {"code": True}), " removes this level's max entry, keeping the parallel stacks in sync. O(1)."])),
    N.para(N.rich([("top", {"code": True}), " — returns ", ("stack[-1]", {"code": True}), " without removing. O(1)."])),
    N.para(N.rich([("peekMax", {"code": True}), " — returns ", ("max_stk[-1]", {"code": True}), ". The running-max invariant guarantees this is always the global maximum. O(1)."])),
    N.para(N.rich([("popMax", {"code": True}), " — gets max_val from peekMax, buffers elements above it using self.pop() (keeps both stacks in sync!), removes the max, then pushes buffer back with self.push() in reversed order to restore stack order. Returns max_val."])),
    N.callout("⚠️  Always use self.pop() and self.push() inside popMax — never the raw lists. These methods keep both stacks synchronized. Raw list manipulation breaks the max_stk invariant.", "⚠️", "yellow_background"),
    N.callout("⚠️  reversed(buffer) is critical: we popped top-to-bottom into buffer, so we must push bottom-to-top (reversed) to restore original stack order.", "⚠️", "yellow_background"),
    N.divider(),
]

# Solution 2 — DLL + SortedList
SOL2_CODE = """\
from sortedcontainers import SortedList

class MaxStack:
    def __init__(self):
        self.stk  = []           # list of (val, uid); tail = top of stack
        self.sl   = SortedList() # sorted by (val, uid); max at sl[-1]
        self.dead = set()        # lazily-deleted uids
        self.uid  = 0            # monotonically increasing

    def push(self, x: int) -> None:          # O(log n)
        self.stk.append((x, self.uid))
        self.sl.add((x, self.uid))
        self.uid += 1

    def _clean(self):
        while self.stk and self.stk[-1][1] in self.dead:
            self.dead.discard(self.stk.pop()[1])

    def pop(self) -> int:                    # O(log n) amortized
        self._clean()
        val, uid = self.stk.pop()
        self.sl.discard((val, uid))
        return val

    def top(self) -> int:
        self._clean()
        return self.stk[-1][0]

    def peekMax(self) -> int:                # O(log n)
        return self.sl[-1][0]

    def popMax(self) -> int:                 # O(log n)
        val, uid = self.sl.pop()             # remove from sorted view
        self.dead.add(uid)                   # lazy-delete from stack view
        return val
"""

blocks += [
    N.h2("Solution 2 — Lazy Deletion + SortedList (Optimal O(log n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The bottleneck of Solution 1 is popMax: O(n) to find and remove a buried element. What if we could find the max element in O(log n) and remove it from the stack in O(log n) — without scanning?"),
        N.h4("What Doesn't Work"),
        N.para("A heap gives O(log n) max but can't efficiently remove by stack-position. A sorted array gives O(log n) lookup but O(n) deletion from the middle. We need a structure that supports both O(log n) access-by-value and O(1) removal by position."),
        N.h4("The Key Observation"),
        N.para("Instead of physically removing an element from the stack when popMax is called, we can mark it as 'deleted' and skip it lazily. The SortedList handles value-order removal in O(log n). The stack defers cleanup until natural pop/top operations encounter the dead element."),
        N.h4("Building the Solution"),
        N.para("Tag each element with a unique incrementing uid (to break ties when values are equal — higher uid = more recently pushed). Store (val, uid) in both the list and the SortedList. popMax removes from SortedList in O(log n) and adds uid to dead-set. pop/top skip dead uids at the tail. Total cleanup work is bounded by total number of operations, giving O(log n) amortized."),
        N.callout("Analogy: Lazy deletion is like putting a sticky note 'TRASH' on a book in a library without actually removing it. When you later browse the shelf from the end, you skip TRASH books and throw them away only as you encounter them.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.stk", {"code": True}), " — list of (val, uid) pairs. Acts as stack; tail is top. Unique uid ensures duplicate values can be distinguished."])),
    N.para(N.rich([("self.sl", {"code": True}), " — SortedList of (val, uid). Sorted ascending; last element ", ("sl[-1]", {"code": True}), " is the global max. Higher uid wins ties between equal values (most recent = max)."])),
    N.para(N.rich([("self.dead", {"code": True}), " — set of lazily-deleted uids. An element in this set has been removed from sl but not yet cleaned from stk."])),
    N.para(N.rich([("push", {"code": True}), " — tags element with uid, appends to both stk and sl. O(log n) for SortedList insertion."])),
    N.para(N.rich([("_clean", {"code": True}), " — skips dead uids at tail of stk (amortized O(1) per dead entry encountered)."])),
    N.para(N.rich([("pop", {"code": True}), " — cleans dead entries, pops live (val, uid) from stk, discards from sl. O(log n) amortized."])),
    N.para(N.rich([("popMax", {"code": True}), " — removes last element of sl (the max) in O(log n), adds its uid to dead-set. Does NOT touch stk at all — the dead-set handles cleanup lazily. Returns val."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "push", "pop / top", "peekMax", "popMax", "Space"],
        ["Brute Force (1 stack)", "O(1)", "O(1)", "O(n)", "O(n)", "O(n)"],
        ["Two Stacks (Interview Pick)", "O(1)", "O(1)", "O(1)", "O(n)* amortized O(1)", "O(n)"],
        ["Lazy Deletion + SortedList (Optimal)", "O(log n)", "O(log n)", "O(log n)", "O(log n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design — data structure problems requiring multiple simultaneous access patterns"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Stacks or DLL + TreeMap — combine two structures for dual-ordering (insertion order + value order)"])),
    N.callout(
        "When to recognize this pattern: Problem asks to 'design a data structure' with multiple access patterns (push/pop AND max/min). "
        "One access pattern needs insertion order (stack/queue), another needs value order (heap/sorted). "
        "Lazy deletion signal: need to remove from middle of one structure but direct removal is O(n).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same design sub-pattern:"),
    N.bullet(N.rich([("Min Stack", {"bold": True}), " (Medium, #155) — identical two-stacks trick, track running minimum; use sl[0] instead of sl[-1] for optimal version"])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), " (Hard, #295) — two heaps (max-heap + min-heap) to maintain dual ordering of streaming elements, O(log n) all ops"])),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium, #146) — doubly linked list for access order + HashMap for O(1) key lookup; same dual-structure pattern"])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard, #239) — monotonic deque to maintain running max within a moving window without rescanning"])),
    N.bullet(N.rich([("Stock Price Fluctuation", {"bold": True}), " (Medium, #2034) — HashMap for timestamps + SortedList for max/min queries; lazy overwrite instead of deletion"])),
    N.bullet(N.rich([("Design a Number Container System", {"bold": True}), " (Medium, #2349) — two maps for two access patterns: index->val and val->sorted-index-set"])),
    N.para("These problems all share the core technique: maintain two data structures in sync to serve two different access patterns simultaneously."),
    N.callout("📚 Reference: Design category — Sub-Pattern 'Two Stacks or DLL + TreeMap'. Appears in patterns guide under Design Patterns section.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("max_stack")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
