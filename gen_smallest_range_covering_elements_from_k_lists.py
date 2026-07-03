"""
gen_smallest_range_covering_elements_from_k_lists.py
Rebuilds the Notion page for LC #632 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8165-85b5-f465e73b9718"
SLUG    = "smallest_range_covering_elements_from_k_lists"

# ── 1) Set properties ─────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=632,
    pattern="Heaps",
    subpatterns=["Min Heap + Track Max"],
    tc="O(n·k·log k)",
    sc="O(k)",
    key_insight="Maintain one frontier element per list in a min-heap; always advance the minimum pointer to shrink the range.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build body ────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a list of k sorted integer lists. Find the smallest range ", {}),
        ("[a, b]", {"code": True}),
        (" such that there is at least one integer from each list within the range. If two ranges have the same size, return the one with the smaller left bound.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]", {"code": True}),
        (" → Output: ", {}),
        ("[20,24]", {"code": True}),
        (" (covers 24 from L0, 20 from L1, 22 from L2; size=4).", {}),
    ])),
    N.divider(),
]

# Solution 1 — Min Heap + Track Max
sol1_code = """\
import heapq

def smallestRange(nums):
    heap = []
    cur_max = float('-inf')
    for i, lst in enumerate(nums):
        heapq.heappush(heap, (lst[0], i, 0))
        cur_max = max(cur_max, lst[0])
    best = [heap[0][0], cur_max]
    while True:
        val, i, j = heapq.heappop(heap)
        if j + 1 >= len(nums[i]):
            break
        nxt = nums[i][j + 1]
        heapq.heappush(heap, (nxt, i, j + 1))
        cur_max = max(cur_max, nxt)
        new_min = heap[0][0]
        if cur_max - new_min < best[1] - best[0]:
            best = [new_min, cur_max]
    return best
"""

blocks += [
    N.h2("Solution 1 — Min Heap + Track Max (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to pick exactly one element from each of k sorted lists such that (max_chosen − min_chosen) is minimized. The range [a, b] is just the spread of those k chosen elements."),
        N.h4("What Doesn't Work"),
        N.para("A brute force that tries every possible combination of one element per list is O((n·k)^k) — completely infeasible. Even trying all pairs of (leftmost, rightmost) across the flattened sorted list is O((n·k)^2 · k)."),
        N.h4("The Key Observation"),
        N.para("The lists are sorted. At any moment if we hold one element per list as a 'frontier', the range is [min_frontier, max_frontier]. To shrink the range, we should raise the minimum (not lower the maximum — we can't). The only way to raise the minimum is to advance that list's pointer to its next element."),
        N.h4("Building the Solution"),
        N.para("Use a min-heap of size k — one element per list. The heap root always gives the current minimum for free in O(log k). Track cur_max separately (a simple variable). Each step: pop minimum, push next from same list, update cur_max, check range. Stop when any list is exhausted."),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}),
                    ("Imagine k runners on separate tracks, each moving in sorted order. You want the moment when all k runners are bunched as close together as possible. You force the slowest runner to advance — that's your greedy move.", {})]),
            "🏃", "blue_background"
        ),
    ]),
]

blocks += [
    N.h3("🔬 Algorithm Deep-Dive: Min-Heap for K Sorted Streams"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Generalization of 'Merge K Sorted Lists' (LC #23). A min-heap of size k maintains a sorted frontier across k sorted sequences, giving O(log k) per element advance instead of O(k) linear scan.", {}),
    ])),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("Exactly one live element per list in the heap at all times — always the smallest unprocessed element from that list. The heap root is the global minimum across all live elements.", {}),
    ])),
    N.para(N.rich([
        ("Recognize when: ", {"bold": True}),
        ('"k sorted lists, process in global sorted order" or "choose one element from each of k groups to minimize/maximize something." Also: LC #378 (Kth Smallest Matrix), #373 (K Pairs Smallest Sums), #632 (this problem).', {}),
    ])),
]

blocks += [
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = []", {"code": True}), (" — min-heap storing tuples ", {}),
                   ("(value, list_index, element_index)", {"code": True}), (".", {})])),
    N.para(N.rich([("cur_max = float('-inf')", {"code": True}),
                   (" — tracks the maximum among all current frontier elements; updated when a new element is pushed.", {})])),
    N.para(N.rich([("for i, lst in enumerate(nums): heappush(heap, (lst[0], i, 0))", {"code": True}),
                   (" — seed the heap with the first element from each list. The 3-tuple allows us to look up the next element later.", {})])),
    N.para(N.rich([("cur_max = max(cur_max, lst[0])", {"code": True}),
                   (" — update the running maximum as we insert each first element.", {})])),
    N.para(N.rich([("best = [heap[0][0], cur_max]", {"code": True}),
                   (" — record the initial range; heap[0][0] is the heap root (minimum) without popping.", {})])),
    N.para(N.rich([("val, i, j = heapq.heappop(heap)", {"code": True}),
                   (" — extract the smallest frontier element: its value, which list it came from (i), and its position in that list (j).", {})])),
    N.para(N.rich([("if j + 1 >= len(nums[i]): break", {"code": True}),
                   (" — list i is exhausted; we cannot maintain coverage of all k lists. Any further iteration is pointless.", {})])),
    N.para(N.rich([("nxt = nums[i][j + 1]; heappush(heap, (nxt, i, j+1))", {"code": True}),
                   (" — advance list i's pointer by one and push the next element back into the heap.", {})])),
    N.para(N.rich([("cur_max = max(cur_max, nxt)", {"code": True}),
                   (" — cur_max can only grow (sorted list: nxt ≥ val). Update if the new element is the largest yet.", {})])),
    N.para(N.rich([("new_min = heap[0][0]", {"code": True}),
                   (" — the heap root after the push is the new global minimum.", {})])),
    N.para(N.rich([("if cur_max - new_min < best[1] - best[0]: best = [new_min, cur_max]", {"code": True}),
                   (" — if the current range is strictly tighter than the best seen, update. Ties are broken naturally by iteration order (earlier smaller ranges win on ties because we only update on strict improvement).", {})])),
    N.divider(),
]

# Solution 2 — Flatten + Sliding Window
sol2_code = """\
def smallestRange_sw(nums):
    # Flatten all values with their list index
    all_v = sorted((v, i)
                   for i, lst in enumerate(nums)
                   for v in lst)
    count = {}
    have, need = 0, len(nums)
    best = [all_v[0][0], all_v[-1][0]]
    lo = 0
    for hi, (v, lst) in enumerate(all_v):
        count[lst] = count.get(lst, 0) + 1
        if count[lst] == 1:
            have += 1          # First element from this list -> coverage gained
        while have == need:    # All lists covered -> try shrinking left
            if v - all_v[lo][0] < best[1] - best[0]:
                best = [all_v[lo][0], v]
            lv, ll = all_v[lo]
            count[ll] -= 1
            if count[ll] == 0:
                have -= 1      # Lost coverage of a list -> stop shrinking
            lo += 1
    return best
"""

blocks += [
    N.h2("Solution 2 — Flatten + Sliding Window"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we sort all n·k elements and annotate each with its source list, we can use a sliding window: expand right until all k lists are covered, then shrink left as much as possible, recording the window bounds as a candidate range."),
        N.h4("What Doesn't Work"),
        N.para("We cannot shrink the window to zero because we need coverage from all k lists. We must maintain that invariant."),
        N.h4("The Key Observation"),
        N.para("The minimum element in a valid window is always its leftmost element (since we sorted). The maximum is the rightmost. We want the window with minimum (right - left) among all valid windows."),
        N.h4("Building the Solution"),
        N.para("Flatten and sort. Use two pointers (lo, hi). Expand hi until all lists are covered. Then advance lo until coverage is lost, recording the best window each time. O(nk log nk) time, O(nk) space — less efficient than the heap but conceptually simpler."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("all_v = sorted(...)", {"code": True}),
                   (" — flatten all values into one sorted list of (value, list_index) tuples. O(nk log nk) sort.", {})])),
    N.para(N.rich([("count[lst] == 1: have += 1", {"code": True}),
                   (" — the first time we see an element from list lst in the current window, coverage count increases.", {})])),
    N.para(N.rich([("while have == need:", {"code": True}),
                   (" — all k lists covered; the window is valid. Try to shrink from the left.", {})])),
    N.para(N.rich([("count[ll] == 0: have -= 1", {"code": True}),
                   (" — we just removed the last element from list ll; coverage lost. Stop shrinking.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O((nk)^k)", "O(k)"],
        ["Flatten + Sliding Window", "O(nk · log nk)", "O(nk)"],
        ["Min Heap + Track Max (optimal)", "O(nk · log k)", "O(k)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min Heap + Track Max (Merge K Sorted variant)", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("k sorted lists/sequences where you need the global minimum repeatedly, and you want to process one element at a time while maintaining coverage of all k groups. Key signals: 'k sorted lists', 'at least one from each', 'minimize range/difference'.", {})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Min-Heap / Merge K Sorted technique:"),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), (" (Hard) — Same heap structure; output the full merged stream, LC #23.", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a Sorted Matrix", {"bold": True}), (" (Medium) — Min-heap advancing through a 2D sorted structure; the k-th pop gives the answer. LC #378.", {})])),
    N.bullet(N.rich([("Find K Pairs with Smallest Sums", {"bold": True}), (" (Medium) — Heap over pair combinations; advance the frontier of promising pairs. LC #373.", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Two heaps (min + max) to maintain median with O(log n) inserts. LC #295.", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Min-heap of end times; greedy room assignment using the 'advance minimum' idea. LC #253.", {})])),
    N.bullet(N.rich([("IPO", {"bold": True}), (" (Hard) — Greedy + heap; pick max-profit task reachable within capital budget. LC #502.", {})])),
    N.para("These problems share the core technique: min-heap maintaining exactly one frontier element per sorted sequence, advancing the minimum at each step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heaps section. Sub-Pattern: Min Heap + Track Max (Merge K Sorted variant). Source: Guide + Analysis.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── 4) Append all blocks ─────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
