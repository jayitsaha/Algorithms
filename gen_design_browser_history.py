"""Notion update script for Design Browser History (LeetCode #1472)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ba-9904-c4e89039ee74"

# ── Step 1: Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1472,
    pattern="Design",
    subpatterns=["List + Two Pointers"],
    tc="O(1) back/forward, O(n) visit amortized",
    sc="O(n)",
    key_insight="Store URLs in a flat list; curr index is the read-head. back/forward are O(1) arithmetic; visit truncates at curr+1 to wipe forward history.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe existing body ──────────────────────────────────────────────
print("Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build body blocks ───────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You have a ", {}),
        ("BrowserHistory", {"code": True}),
        (" class. Implement three methods: ", {}),
        ("visit(url)", {"code": True}),
        (" navigates to a new URL and wipes all forward history. ", {}),
        ("back(steps)", {"code": True}),
        (" moves ", {}),
        ("steps", {"code": True}),
        (" backward in history (clamp to start if not enough). ", {}),
        ("forward(steps)", {"code": True}),
        (" moves ", {}),
        ("steps", {"code": True}),
        (" forward (clamp to end). Return the current URL after each navigation.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Array + Index Pointer ──────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Array + Index Pointer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a sequence of URLs where we can jump to any position instantly. Back and forward are just \"move my position left or right.\" A flat array with a current-index pointer is the simplest model that supports this in O(1)."),
        N.h4("What Doesn't Work"),
        N.para("Two stacks (back-stack + forward-stack) is the natural first thought. It handles visit() correctly in O(1). But back(k) requires k individual pop+push operations — O(steps), not O(1). For large histories navigated frequently, this is unacceptable."),
        N.h4("The Key Observation"),
        N.para("Navigation doesn't require moving data — it requires moving your position in the data. If all URLs live in a single list, back/forward become arithmetic: curr -= steps and curr += steps (with clamping). The list never changes during navigation — only curr changes."),
        N.h4("Building the Solution"),
        N.para("Store history as a Python list. Maintain curr as the current index. For visit(): wipe forward entries via list slicing (history[:curr+1]) then append the new URL. For back/forward: arithmetic + max/min clamping. This gives O(1) for all navigation operations."),
        N.callout("Analogy: Browser history is a cassette tape with a read-head. You slide the head left (back) or right (forward). When you record something new (visit), you cut the tape at the current head position before recording — everything after the cut is gone.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "class BrowserHistory:\n"
        "    def __init__(self, homepage: str):\n"
        "        self.history = [homepage]  # tape starts with homepage\n"
        "        self.curr = 0              # read-head at index 0\n"
        "\n"
        "    def visit(self, url: str) -> None:\n"
        "        # Wipe everything after curr, then append new URL\n"
        "        self.history = self.history[:self.curr + 1]\n"
        "        self.history.append(url)\n"
        "        self.curr = len(self.history) - 1\n"
        "\n"
        "    def back(self, steps: int) -> str:\n"
        "        self.curr = max(0, self.curr - steps)  # clamp at 0\n"
        "        return self.history[self.curr]\n"
        "\n"
        "    def forward(self, steps: int) -> str:\n"
        "        self.curr = min(len(self.history) - 1, self.curr + steps)  # clamp at end\n"
        "        return self.history[self.curr]\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.history = [homepage]", {"code": True}), (" — tape initialised with just the homepage; the list grows as URLs are visited.", {})])),
    N.para(N.rich([("self.curr = 0", {"code": True}), (" — read-head starts at index 0, pointing to the only entry.", {})])),
    N.para(N.rich([("self.history = self.history[:self.curr + 1]", {"code": True}), (" — truncate the list at curr+1; everything from curr+1 onward (forward history) is discarded.", {})])),
    N.para(N.rich([("self.history.append(url)", {"code": True}), (" — append the new URL at the end of the now-truncated tape.", {})])),
    N.para(N.rich([("self.curr = len(self.history) - 1", {"code": True}), (" — advance read-head to the new last position. Post-visit, curr always equals len-1, so no forward history exists.", {})])),
    N.para(N.rich([("self.curr = max(0, self.curr - steps)", {"code": True}), (" — slide head left by steps; clamp with max(0,...) so we never underflow to a negative index.", {})])),
    N.para(N.rich([("return self.history[self.curr]", {"code": True}), (" — O(1) random access; returns the URL at the new position.", {})])),
    N.para(N.rich([("self.curr = min(len(self.history) - 1, self.curr + steps)", {"code": True}), (" — slide right; clamp with min(len-1,...) so we never overflow past the last valid index.", {})])),
    N.divider(),
]

# ── Solution 2: Two Stacks ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Two Stacks (Brute Force, O(steps) navigation)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of back/forward as two opposing directions. A stack naturally supports 'undo' — push when you go forward, pop when you go back. Two stacks mirror the browser's forward and back directions."),
        N.h4("What Doesn't Work"),
        N.para("The two-stack approach is O(steps) per back()/forward() call — each step individually pops from one stack and pushes to the other. For back(100) on a 1000-page history, that's 100 operations vs. the array approach's single arithmetic expression."),
        N.h4("The Key Observation"),
        N.para("This approach is intuitive and correct, but suboptimal. Propose it first in interviews to show you can reason naturally about the problem, then improve to the array approach."),
        N.h4("Building the Solution"),
        N.para("back_stack holds all history up to and including the current page (top = current). fwd_stack holds forward history (top = most recent forward page). visit() clears fwd_stack and pushes to back_stack. back() transfers pages one by one from back to forward; forward() does the reverse."),
    ]),
    N.h3("Code"),
    N.code(
        "class BrowserHistory:\n"
        "    def __init__(self, homepage: str):\n"
        "        self.back_st = [homepage]  # current + past; top = current\n"
        "        self.fwd_st = []           # forward history; top = nearest forward\n"
        "\n"
        "    def visit(self, url: str) -> None:\n"
        "        self.back_st.append(url)\n"
        "        self.fwd_st.clear()        # erase all forward history\n"
        "\n"
        "    def back(self, steps: int) -> str:\n"
        "        while steps > 0 and len(self.back_st) > 1:\n"
        "            self.fwd_st.append(self.back_st.pop())\n"
        "            steps -= 1\n"
        "        return self.back_st[-1]\n"
        "\n"
        "    def forward(self, steps: int) -> str:\n"
        "        while steps > 0 and self.fwd_st:\n"
        "            self.back_st.append(self.fwd_st.pop())\n"
        "            steps -= 1\n"
        "        return self.back_st[-1]\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.back_st = [homepage]", {"code": True}), (" — back-stack holds all pages up to current; top of stack is the page you're viewing.", {})])),
    N.para(N.rich([("self.fwd_st.clear()", {"code": True}), (" — visiting a new URL erases forward history. clear() is O(1) since it drops references.", {})])),
    N.para(N.rich([("while steps > 0 and len(self.back_st) > 1", {"code": True}), (" — loop k times where k = min(steps, available_back). Guard on >1 keeps the homepage pinned (can't go before the very first page).", {})])),
    N.para(N.rich([("self.fwd_st.append(self.back_st.pop())", {"code": True}), (" — move current page to forward stack; the page below it becomes the new current. This is the O(steps) cost.", {})])),
    N.divider(),
]

# ── Complexity table ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "visit()", "back() / forward()", "Space"],
        ["Two Stacks", "O(1)", "O(steps)", "O(n)"],
        ["Array + Index (optimal)", "O(curr) amortized", "O(1)", "O(n)"],
        ["Doubly Linked List (follow-up)", "O(1)", "O(steps)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Design — Data Structure Implementation", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("List + Two Pointers (curr index as read-head into dynamic array tape)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks you to 'design' a class with multiple operations. "
        "(2) Need 'current position' in a sequence with backward/forward navigation. "
        "(3) Visiting a new state erases future states (history-like semantics). "
        "(4) O(1) navigation required — hints that data movement is a no-go.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Design + indexed navigation):"),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), (" (Medium) — O(1) get/put via doubly linked list + hashmap; classic design problem (#146)", {})])),
    N.bullet(N.rich([("Design Linked List", {"bold": True}), (" (Medium) — Build full linked list from scratch with O(1) head/tail ops (#707)", {})])),
    N.bullet(N.rich([("Min Stack", {"bold": True}), (" (Medium) — Parallel auxiliary stack tracking minimum — same 'index as state' idea (#155)", {})])),
    N.bullet(N.rich([("Snapshot Array", {"bold": True}), (" (Medium) — Array with snapshot/restore — curr pointer represents snapshot version (#1146)", {})])),
    N.bullet(N.rich([("Design Circular Deque", {"bold": True}), (" (Medium) — Array with head/tail pointers and modulo wraparound (#641)", {})])),
    N.bullet(N.rich([("Text Editor", {"bold": True}), (" (Hard) — Cursor left/right in a string — same bounded pointer arithmetic in a linear structure (#2296)", {})])),
    N.para("These problems share the core insight: maintain a position index into a linear data structure and use arithmetic to navigate rather than physically moving data."),
    N.callout("📚 Reference: Design problems section — Sub-Pattern: List + Two Pointers (curr read-head). This sub-pattern classification is based on analysis; may not appear by this exact name in the DSA guide.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("design_browser_history")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
