"""
gen_next_greater_element_i.py — Notion IN-PLACE update for #496 Next Greater Element I
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8177-97ce-f5570dd4e1e3"

# ── 1) Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=496,
    pattern="Stack and Queue",
    subpatterns=["Monotonic Stack: Next Greater"],
    tc="O(m+n)",
    sc="O(n)",
    key_insight="Precompute next-greater for all of nums2 via monotonic decreasing stack; answer nums1 queries in O(1) each.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────
print("Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ─────────────────────────────────────────────────────
BRUTE_CODE = """\
def nextGreaterElement(nums1, nums2):
    idx_map = {v: i for i, v in enumerate(nums2)}
    result = []
    for x in nums1:
        pos = idx_map[x]
        ans = -1
        for j in range(pos + 1, len(nums2)):
            if nums2[j] > x:
                ans = nums2[j]
                break
        result.append(ans)
    return result
# Time: O(m*n)  Space: O(n) for idx_map"""

OPTIMAL_CODE = """\
def nextGreaterElement(nums1, nums2):
    nge_map = {}      # value -> next greater element (or -1)
    stack = []        # monotonic decreasing stack: pending values

    for x in nums2:
        # Pop everything smaller than x — x is their next greater
        while stack and stack[-1] < x:
            nge_map[stack.pop()] = x
        stack.append(x)   # x is still awaiting its answer

    # Remaining stack elements have no greater element to their right
    for v in stack:
        nge_map[v] = -1

    return [nge_map[x] for x in nums1]
# Time: O(m+n)  Space: O(n)"""

blocks = []

# ─── Problem ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two distinct integer arrays ", {}),
        ("nums1", {"code": True}),
        (" and ", {}),
        ("nums2", {"code": True}),
        (", where ", {}),
        ("nums1", {"code": True}),
        (" is a subset of ", {}),
        ("nums2", {"code": True}),
        (". For each element in ", {}),
        ("nums1", {"code": True}),
        (", find its ", {}),
        ("next greater element", {"bold": True}),
        (" in ", {}),
        ("nums2", {"code": True}),
        (": the first element to the right of that position in ", {}),
        ("nums2", {"code": True}),
        (" that is strictly greater. Return ", {}),
        ("-1", {"code": True}),
        (" if no such element exists. All values are distinct.", {}),
    ])),
    N.para(N.rich([
        ("Example: nums1=[4,1,2], nums2=[1,3,4,2] → ", {}),
        ("[-1, 3, -1]", {"code": True}),
        (" (4 has no greater in nums2; 1's next greater is 3; 2 has none)", {}),
    ])),
    N.divider(),
]

# ─── Solution 1: Brute Force ───
blocks += [
    N.h2("Solution 1 — Brute Force (O(m·n)) — Mention First"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each x in nums1: (1) find where x lives in nums2, (2) scan everything to x's right until we see something larger."),
        N.h4("What Doesn't Work (at scale)"),
        N.para("This works correctly, but is O(m·n) — for each of m queries we scan up to n elements. With m=n=1000, that's 10^6 operations. The optimal solution can do this in O(m+n)."),
        N.h4("The Key Observation"),
        N.para("The problem separates into two tasks: (1) locate x in nums2, and (2) scan right. We propose this naive approach first to set up the optimization."),
        N.h4("Building the Solution"),
        N.para("Precompute an index map {value: index} for nums2 in O(n). Then for each x in nums1, jump to its index and scan right linearly."),
        N.callout("Analogy: Like looking up a word in a dictionary by scanning every page from the start.", "📖", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("idx_map = ...", {"code": True}), (" — Precompute position of each value in nums2 so we can jump to x's location in O(1).", {})])),
    N.para(N.rich([("for x in nums1:", {"code": True}), (" — Process each query element.", {})])),
    N.para(N.rich([("pos = idx_map[x]", {"code": True}), (" — Get the index where x lives in nums2.", {})])),
    N.para(N.rich([("for j in range(pos+1, len(nums2)):", {"code": True}), (" — Scan everything to the right of x.", {})])),
    N.para(N.rich([("if nums2[j] > x:", {"code": True}), (" — First element larger than x is the next greater. Record and break.", {})])),
    N.divider(),
]

# ─── Solution 2: Monotonic Stack (optimal) ───
blocks += [
    N.h2("Solution 2 — Monotonic Decreasing Stack + Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("nums1 is just a set of queries against nums2. The real subproblem: for every element in nums2, what is its next greater element? If we precompute this for all elements in O(n), each query in nums1 is answered in O(1)."),
        N.h4("What Doesn't Work"),
        N.para("A naive second pass for each element is O(n²). We need a way to resolve multiple elements simultaneously when we encounter a larger one."),
        N.h4("The Key Observation"),
        N.para("When we encounter element x while scanning nums2, x is the next greater element for ALL elements in the stack that are smaller than x. We can pop them all and record their answers in one sweep — this is why the total work is O(n)."),
        N.h4("Building the Solution"),
        N.para("Maintain a stack of 'pending' elements in decreasing order. For each x: while stack top < x, pop and record. Then push x. After the scan, remaining stack → -1. The decreasing invariant ensures correctness: each pop finds exactly the first (next) greater element."),
        N.callout("Analogy: A line of people ordered shortest-to-tallest (front to back). When a taller person walks in, they immediately resolve the 'who's taller' question for everyone shorter in the line — in one sweep.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("nge_map = {}", {"code": True}), (" — Hash map to store each value's next greater element. O(1) lookup for nums1 queries.", {})])),
    N.para(N.rich([("stack = []", {"code": True}), (" — Monotonic decreasing stack. Holds values from nums2 in decreasing order, each waiting for its answer.", {})])),
    N.para(N.rich([("for x in nums2:", {"code": True}), (" — Single left-to-right pass over nums2.", {})])),
    N.para(N.rich([("while stack and stack[-1] < x:", {"code": True}), (" — While the top of the stack is smaller than x, x is the answer for that top. Use while (not if!) because x might resolve multiple pending values.", {})])),
    N.para(N.rich([("nge_map[stack.pop()] = x", {"code": True}), (" — Pop the top, record its answer as x. The popped element is done.", {})])),
    N.para(N.rich([("stack.append(x)", {"code": True}), (" — x's next greater is still unknown; push it onto the pending stack.", {})])),
    N.para(N.rich([("for v in stack: nge_map[v] = -1", {"code": True}), (" — Elements still on the stack never found a greater element → -1.", {})])),
    N.para(N.rich([("return [nge_map[x] for x in nums1]", {"code": True}), (" — Answer each query with O(1) hash lookup.", {})])),
    N.callout("Key Insight: Use while not if — a single incoming element can resolve multiple pending elements simultaneously, keeping total work O(n).", "⚠️", "yellow_background"),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(m·n)", "O(n)"],
        ["Monotonic Stack (optimal)", "O(m+n)", "O(n)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stack and Queue", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Monotonic Stack: Next Greater", {})])),
    N.callout(
        "When to recognize this pattern: problem asks 'for each element, find the first element to its right/left that is greater/smaller.' Naive is O(n²); the monotonic stack achieves O(n). Key signals: 'next greater', 'next smaller', 'previous greater', or 'span' questions.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sub-pattern (Monotonic Stack: Next Greater / Next Smaller):"),
    N.bullet(N.rich([("Next Greater Element II", {"bold": True}), (" (Medium) — Circular array; iterate nums 2× with index mod. #503", {})])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), (" (Medium) — Return days until warmer temp; store indices on decreasing stack. #739", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Monotonic increasing stack finds previous/next smaller boundaries. #84", {})])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), (" (Hard) — Can be solved with monotonic stack or two-pointer. #42", {})])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), (" (Medium) — Two monotonic stacks (prev/next smaller) count contributions. #907", {})])),
    N.bullet(N.rich([("Stock Span Problem", {"bold": True}), (" (Medium) — Span = distance to previous greater; classic monotonic decreasing stack.", {})])),
    N.para("These problems share the core technique: maintain a stack with a monotonic invariant (decreasing for next-greater, increasing for next-smaller) so each element is processed in amortized O(1)."),
    N.callout("📚 Sub-pattern verified from DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue section: Monotonic Stack: Next Greater", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("next_greater_element_i")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
