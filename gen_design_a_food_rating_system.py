"""
Notion update script for: Design a Food Rating System (LC #2353)
Run from the Algorithms directory: python3 gen_design_a_food_rating_system.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8124-a009-d8b8b58a4b1d"
SLUG    = "design_a_food_rating_system"

# ── 1. Set properties ────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty   = "Medium",
    number       = 2353,
    pattern      = "Design",
    subpatterns  = ["Hash Maps + Heap (Lazy Deletion)"],
    tc           = "O(log n) per operation (amortized)",
    sc           = "O(n + total updates)",
    key_insight  = "Lazy deletion: push new heap entry, leave old as stale ghost; validate at query time",
    icon         = "🟡",
)
print("Properties set.")

# ── 2. Wipe existing body ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body blocks ──────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a food rating system that can do the following:\n\n"
         "• Initialize the system with food items, each having a name, a cuisine, and a rating.\n"
         "• Modify the rating of a food item.\n"
         "• Return the highest-rated food for a given cuisine. If multiple foods have the same rating, return the one that is lexicographically (alphabetically) smaller.\n\n"
         "Implement the class "),
        ("FoodRatings", {"code": True}),
        (":\n\n• "),
        ("FoodRatings(foods, cuisines, ratings)", {"code": True}),
        (" — initializes the system.\n• "),
        ("changeRating(food, newRating)", {"code": True}),
        (" — changes the rating of the food item.\n• "),
        ("highestRated(cuisine)", {"code": True}),
        (" — returns the name of the food item that has the highest rating for that cuisine."),
    ])),
    N.divider(),
]

# ── Solution 1: Lazy Deletion Heap ────────────────────────────────────────────
SOL1_CODE = """\
import heapq
from collections import defaultdict

class FoodRatings:
    def __init__(self, foods, cuisines, ratings):
        self.food_rating  = {}          # food → current rating (ground truth)
        self.food_cuisine = {}          # food → cuisine
        self.heaps = defaultdict(list)  # cuisine → min-heap of (-rating, food)

        for food, cuisine, rating in zip(foods, cuisines, ratings):
            self.food_rating[food]  = rating
            self.food_cuisine[food] = cuisine
            heapq.heappush(self.heaps[cuisine], (-rating, food))

    def changeRating(self, food: str, newRating: int) -> None:
        self.food_rating[food] = newRating          # update ground truth
        cuisine = self.food_cuisine[food]
        heapq.heappush(self.heaps[cuisine], (-newRating, food))  # push new; old is now stale

    def highestRated(self, cuisine: str) -> str:
        heap = self.heaps[cuisine]
        while True:
            neg_r, food = heap[0]                    # peek (don't pop)
            if -neg_r == self.food_rating[food]:      # valid entry?
                return food                           # yes — highest-rated food
            heapq.heappop(heap)                       # stale ghost — discard
"""

blocks += [
    N.h2("Solution 1 — Lazy Deletion Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need: (1) a way to change one food's rating in O(log n), and (2) instantly find the max-rating food per cuisine in O(log n). This is the 'dynamic top-K per group' pattern."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: a list per cuisine, scan the whole list for highestRated. That's O(n) per query — with 2×10⁴ calls it's 4×10⁸ operations worst case. Unacceptable."),
        N.h4("The Key Observation"),
        N.para("A max-heap gives O(1) access to the maximum. The problem is updates: we can't remove an arbitrary element from a heap efficiently. But we can push the new value and leave the old one. The old one becomes 'stale' — detectable by comparing the heap entry's rating to the ground-truth dict."),
        N.h4("Building the Solution"),
        N.para("Three structures: food_rating (dict, source of truth), food_cuisine (dict, routing), heaps (one per cuisine). changeRating: update dict + push new entry. highestRated: peek top, discard stale entries until valid, return. Tuple (-rating, food_name) gives max-rating via min-heap, and tie-breaks alphabetically for free."),
        N.callout(
            "Analogy: Think of the heap as a leaderboard with ghost names from past scores. "
            "Each time a player's score changes, you add a new card. The old card is still there. "
            "When you check the top, you scan past cards that no longer match the player's current score.",
            "🏆", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("self.food_rating = {}", {"code": True}), " — The ground truth. food → current rating. This is what we check during validation."])),
    N.para(N.rich([("self.food_cuisine = {}", {"code": True}), " — Routes changeRating to the correct heap (O(1) lookup by food name)."])),
    N.para(N.rich([("self.heaps = defaultdict(list)", {"code": True}), " — One min-heap per cuisine. Stores tuples (-rating, food) so the smallest tuple = highest-rated food."])),
    N.para(N.rich([("heapq.heappush(self.heaps[cuisine], (-rating, food))", {"code": True}), " — Negate rating for max-heap semantics. Tuple comparison handles tie-breaking alphabetically."])),
    N.para(N.rich([("self.food_rating[food] = newRating", {"code": True}), " — Update dict FIRST. The old heap entry is now stale by definition (dict no longer matches)."])),
    N.para(N.rich([("heapq.heappush(self.heaps[cuisine], (-newRating, food))", {"code": True}), " — Push new valid entry. Old (-oldRating, food) stays in heap as a ghost — we do NOT remove it."])),
    N.para(N.rich([("neg_r, food = heap[0]", {"code": True}), " — PEEK (not pop) the heap top. We only pop if it's stale."])),
    N.para(N.rich([("if -neg_r == self.food_rating[food]:", {"code": True}), " — Validate: does this entry's rating match the current ground truth? If yes, the entry is live."])),
    N.para(N.rich([("return food", {"code": True}), " — Valid top found. Return without popping — leave it at the top for future queries."])),
    N.para(N.rich([("heapq.heappop(heap)", {"code": True}), " — Stale ghost: rating in dict doesn't match entry. Discard it. Loop back to check new top."])),
    N.divider(),
]

# ── Solution 2: SortedList ────────────────────────────────────────────────────
SOL2_CODE = """\
from sortedcontainers import SortedList
from collections import defaultdict

class FoodRatings:
    def __init__(self, foods, cuisines, ratings):
        self.food_rating  = dict(zip(foods, ratings))
        self.food_cuisine = dict(zip(foods, cuisines))
        self.sl = defaultdict(SortedList)  # cuisine → SortedList of (-rating, food)
        for food, cuisine, rating in zip(foods, cuisines, ratings):
            self.sl[cuisine].add((-rating, food))

    def changeRating(self, food: str, newRating: int) -> None:
        cuisine = self.food_cuisine[food]
        old     = self.food_rating[food]
        self.sl[cuisine].remove((-old, food))     # O(log n) exact removal
        self.food_rating[food] = newRating
        self.sl[cuisine].add((-newRating, food))  # O(log n) insert

    def highestRated(self, cuisine: str) -> str:
        return self.sl[cuisine][0][1]             # O(1) access to smallest = highest rated
"""

blocks += [
    N.h2("Solution 2 — SortedList (Cleaner Alternative)"),
    N.toggle_h3("💡 Intuition: Why SortedList?", [
        N.h4("The Problem with Lazy Heap"),
        N.para("The lazy heap approach works but leaves 'ghost' entries. If changeRating is called many times, the heap grows. SortedList from the sortedcontainers library maintains a sorted sequence that supports O(log n) insertion AND exact removal — no ghosts, no amortization needed."),
        N.h4("The Key Observation"),
        N.para("SortedList.remove() finds and deletes the exact element in O(log n). We store (-rating, food) so the minimum element = highest-rated food. Querying is O(1) array index access."),
        N.h4("Trade-off"),
        N.para("SortedList is not in Python's standard library. In LeetCode, sortedcontainers is available. In an interview, mention it as a cleaner alternative after presenting the heap solution."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("self.sl = defaultdict(SortedList)", {"code": True}), " — One SortedList per cuisine, maintained in ascending order of (-rating, food). Ascending here means highest rating first."])),
    N.para(N.rich([("self.sl[cuisine].remove((-old, food))", {"code": True}), " — Exact O(log n) removal. No staleness issue — the old entry is cleanly erased before inserting the new one."])),
    N.para(N.rich([("return self.sl[cuisine][0][1]", {"code": True}), " — SortedList[0] is the minimum element = (-highest_rating, alphabetically_first_name). Index [1] extracts the food name."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "changeRating", "highestRated", "Space"],
        ["Brute Force (list scan)", "O(1)", "O(n) — too slow", "O(n)"],
        ["Lazy Deletion Heap (Interview Pick)", "O(log n)", "O(log n) amortized", "O(n + total updates)"],
        ["SortedList", "O(log n)", "O(1)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design (Data Structure Design)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Hash Maps + Heap (Lazy Deletion)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Design a system' with dynamic updates and efficient max/min queries\n"
        "• Need top-K per group (one heap per group)\n"
        "• Arbitrary deletion from heap is too costly → use lazy deletion with ground-truth dict\n"
        "• Tuple ordering handles tie-breaking implicitly",
        "🔎", "green_background"),
    N.para("Note: The 'Hash Maps + Heap (Lazy Deletion)' sub-pattern is based on analysis; "
           "the DSA_Patterns_and_SubPatterns_Guide.md covers this under Heap sub-patterns."),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Heap / Lazy Deletion / Top-per-group):"),
    N.bullet(N.rich([("Design Twitter", {"bold": True}), " (Medium) — Merge k most-recent tweet streams with a heap (#355)"])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), " (Medium) — Max-heap to always schedule the most-frequent task first (#621)"])),
    N.bullet(N.rich([("Reorganize String", {"bold": True}), " (Medium) — Heap places chars without repeating adjacently (#767)"])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), " (Hard) — Two-heap approach for dynamic median (#295)"])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), " (Easy) — Min-heap of size k for streaming top-k (#703)"])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), " (Medium) — Heap + frequency map for top-k (#347)"])),
    N.para("These problems share the core technique: use a heap to maintain ordering, "
           "with lazy or explicit deletion to handle dynamic updates."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heap section (Top K, Greedy + Heap). "
              "Hash Maps + Heap (Lazy Deletion) is an Analysis-derived sub-pattern.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through changeRating and highestRated with lazy deletion — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
