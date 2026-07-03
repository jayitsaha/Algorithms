"""
gen_final_prices_with_a_special_discount_in_a_shop.py
Regenerate the Notion page for LC #1475 in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8168-b90f-e43eef07da28"
SLUG = "final_prices_with_a_special_discount_in_a_shop"

# ── 1) Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1475,
    pattern="Stack",
    subpatterns=["Next Smaller Element"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Use a monotonic decreasing stack to find each item's first smaller-or-equal right neighbor in one pass.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build the body ──────────────────────────────────────────────────────────
BRUTE_CODE = """\
def finalPrices_brute(prices: list[int]) -> list[int]:
    n = len(prices)
    result = prices[:]
    for i in range(n):
        for j in range(i + 1, n):
            if prices[j] <= prices[i]:
                result[i] -= prices[j]
                break
    return result"""

OPTIMAL_CODE = """\
def finalPrices(prices: list[int]) -> list[int]:
    result = prices[:]      # copy: unfound discounts keep original price
    stack = []              # holds indices of items waiting for a discount
    for i, price in enumerate(prices):
        while stack and prices[stack[-1]] >= price:
            j = stack.pop()
            result[j] = prices[j] - price  # first smaller-or-equal right found
        stack.append(i)
    return result"""

blocks = []

# ── Problem ────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array ", {}),
        ("prices", {"code": True}),
        (" where ", {}),
        ("prices[i]", {"code": True}),
        (" is the price of the ", {}),
        ("i", {"code": True}),
        ("-th item in a shop. There is a special discount rule: for each item ", {}),
        ("i", {"code": True}),
        (", find the first item ", {}),
        ("j > i", {"code": True}),
        (" such that ", {}),
        ("prices[j] <= prices[i]", {"code": True}),
        (". The discount for item ", {}),
        ("i", {"code": True}),
        (" is ", {}),
        ("prices[j]", {"code": True}),
        (". If no such ", {}),
        ("j", {"code": True}),
        (" exists, no discount is applied. Return an array of final prices.", {}),
    ])),
    N.para("Example: prices = [8, 4, 6, 2, 3] → result = [4, 2, 4, 2, 3].\n"
           "  - Item 0 (price=8): first right ≤ 8 is 4 (idx 1) → 8-4=4\n"
           "  - Item 1 (price=4): first right ≤ 4 is 2 (idx 3) → 4-2=2\n"
           "  - Item 2 (price=6): first right ≤ 6 is 2 (idx 3) → 6-2=4\n"
           "  - Items 3,4: no right element ≤ their price → no discount"),
    N.divider(),
]

# ── Solution 1 — Monotonic Stack (Interview Pick) ─────────────────────────────
blocks += [
    N.h2("Solution 1 — Monotonic Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For every index i, we need the nearest j to the right where prices[j] <= prices[i]. This is the 'Next Smaller or Equal Element' problem, applied to all indices simultaneously."),
        N.h4("What Doesn't Work"),
        N.para("Brute force (nested loops): for each i, scan j=i+1 to n-1 until prices[j] <= prices[i]. This is O(n²) — 500 items → 125,000 comparisons. Too slow for n up to 500 (brute force OK) but conceptually wasteful since we're repeating work."),
        N.h4("The Key Observation"),
        N.para("As we scan left-to-right, each new item might be the discount-giver for multiple earlier items. If prices[i] is small, it can resolve the 'next smaller' query for all stack items with price >= prices[i] — in one shot. This is the monotonic stack insight."),
        N.h4("Building the Solution"),
        N.para("Maintain a stack of indices whose items are still looking for a discount. When we see prices[i], pop all stack indices j where prices[j] >= prices[i] — prices[i] is their answer. Then push i (it now waits for its own discount). Any index remaining on the stack at the end had no valid right neighbor."),
        N.callout("Analogy: A line of people waiting for a shorter person to walk by. When a shorter person arrives, all taller people who've been waiting can now be served — they found their 'first shorter right neighbor.' People of the same height or shorter serve as the answer too.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result = prices[:]", {"code": True}), (" — Copy prices into result. Unfound discounts stay as original price; no need to handle the 'no discount' case separately.", {})])),
    N.para(N.rich([("stack = []", {"code": True}), (" — Stack of indices. Stores positions (not values) so we can write result[j] when a discount is found.", {})])),
    N.para(N.rich([("for i, price in enumerate(prices):", {"code": True}), (" — Scan every item left-to-right. price = prices[i] for convenience.", {})])),
    N.para(N.rich([("while stack and prices[stack[-1]] >= price:", {"code": True}), (" — Two conditions: stack non-empty, and current price is <= stack top's price. If both hold, current item IS the discount for stack top.", {})])),
    N.para(N.rich([("j = stack.pop()", {"code": True}), (" — Pop the index that found its discount. We use the index (not value) to write to result.", {})])),
    N.para(N.rich([("result[j] = prices[j] - price", {"code": True}), (" — Apply the discount: original price minus the first smaller-or-equal right element.", {})])),
    N.para(N.rich([("stack.append(i)", {"code": True}), (" — Push current index. It hasn't found its discount yet — will wait on the stack.", {})])),
    N.para(N.rich([("return result", {"code": True}), (" — Remaining stack indices get no discount; their original price is already in result from the copy.", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (Nested Loops)"),
    N.toggle_h3("💡 Intuition: Why Start Here", [
        N.h4("Reframe the Problem"),
        N.para("The problem literally asks: for each i, find the first j > i where prices[j] <= prices[i]. The brute force directly implements this definition."),
        N.h4("What Doesn't Work at Scale"),
        N.para("For each of n elements, we potentially scan all n-1 elements to its right. Worst case (all strictly increasing, no discounts): we scan the full right portion for every element → O(n²) comparisons total."),
        N.h4("The Key Observation"),
        N.para("The brute force is correct and simple. It's the right starting point in an interview — propose it, verify it, then optimize to the monotonic stack solution."),
        N.h4("Building the Solution"),
        N.para("Two nested loops: outer iterates i, inner iterates j from i+1. On first prices[j] <= prices[i], apply discount and break. If inner loop completes without finding a j, no discount."),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result = prices[:]", {"code": True}), (" — Start with original prices; apply discounts in-place.", {})])),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — For each item, we'll search for its discount.", {})])),
    N.para(N.rich([("for j in range(i+1, n):", {"code": True}), (" — Scan every element to the right of i.", {})])),
    N.para(N.rich([("if prices[j] <= prices[i]:", {"code": True}), (" — Check discount condition (≤, not strict <).", {})])),
    N.para(N.rich([("result[i] -= prices[j]", {"code": True}), (" — Subtract the discount.", {})])),
    N.para(N.rich([("break", {"code": True}), (" — Only the FIRST valid j counts. Stop searching once found.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n²)", "O(1)", "Nested loops; correct but slow"],
        ["Monotonic Stack ✓", "O(n)", "O(n)", "Each index pushed/popped once; interview answer"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stack (Monotonic Stack)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Next Smaller Element (variant: Next Smaller or Equal)", {})])),
    N.callout(
        "When to recognize this pattern: 'For each element, find the first element to its right (or left) satisfying a comparison condition.' "
        "Key signals: 'first occurrence to the right', 'next greater/smaller', 'nearest neighbor with property X'. "
        "The monotonic stack delivers O(n) vs O(n²) brute force.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the Next Smaller / Next Greater Element technique:"),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), (" (Medium) — Next warmer day; same stack, pop when current > top", {})])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), (" (Easy) — Next greater in another array; decreasing stack + hash map", {})])),
    N.bullet(N.rich([("Next Greater Element II", {"bold": True}), (" (Medium) — Circular array; scan 2n with index % n", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Left and right smaller boundaries per bar; monotonic stack for boundaries", {})])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), (" (Medium) — Count subarrays where each element is minimum; monotonic stack for spans", {})])),
    N.bullet(N.rich([("Stock Span Problem", {"bold": True}), (" (Medium) — Previous greater element; decreasing stack counting days", {})])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), (" (Hard) — Uses monotonic stack to compute left/right boundaries for water levels", {})])),
    N.para("These problems all share the core technique: a monotonic stack maintains elements in sorted order so 'nearest neighbor' queries can be answered in O(1) amortized per element."),
    N.callout("📚 Pattern verified via DSA_Patterns_and_SubPatterns_Guide.md: Stack/Queue → Monotonic Stack: Next Greater / Next Smaller Element", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
