"""
gen_online_stock_span.py
Regenerate the Notion page for Online Stock Span (#901) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-812c-b4fa-c91e73afc61c"

# ── 1. Properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=901,
    pattern="Stack / Queue",
    subpatterns=["Previous Greater Element Count"],
    tc="O(1) amortized",
    sc="O(n)",
    key_insight="Store (price, span) pairs in a monotonic decreasing stack; pop & absorb spans when top ≤ today — range compression gives amortized O(1).",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ──────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design an algorithm that collects daily stock prices and returns the "),
        ("span", {"bold": True}),
        (" for the current day's price. The span is defined as the maximum number of consecutive days (starting from today and going backwards) for which the stock price was less than or equal to today's price.\n\n"),
        ("Implement the ", {}),
        ("StockSpanner", {"code": True}),
        (" class:\n• ", {}),
        ("StockSpanner()", {"code": True}),
        (" — initializes the object.\n• ", {}),
        ("int next(int price)", {"code": True}),
        (" — returns the span of the stock's price for the given ", {}),
        ("price", {"code": True}),
        (" for the current day.", {}),
    ])),
    N.divider(),
]

# Solution 1: Monotonic Stack (Optimal)
sol1_code = """class StockSpanner:
    def __init__(self):
        self.stack = []   # stores (price, span) pairs

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]   # absorb span (range compression)
        self.stack.append((price, span))
        return span"""

blocks += [
    N.h2("Solution 1 — Monotonic Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each call, find how many consecutive prior days have price ≤ today — i.e., how far back until we hit a strictly greater price. This is the classic Previous Greater Element problem, done online (one price at a time)."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: store all prices, scan backwards each call. O(n) per call, O(n²) total. Redundant — we re-examine days we've already counted in previous calls."),
        N.h4("The Key Observation"),
        N.para("If we've computed that price=75 has span=4 (it covers 4 prior days), and today=85 ≥ 75, then today automatically beats all 4 of those days too. We can absorb the entire range without re-examining each day — just store the span alongside the price."),
        N.h4("Building the Solution"),
        N.para("Maintain a monotonic decreasing stack of (price, span) pairs. For each new price:\n1. Start span=1 (today counts itself)\n2. While stack top price ≤ today: pop and add its span\n3. Push (today_price, accumulated_span)\n4. Return span\n\nEach price is pushed once and popped at most once → amortized O(1)."),
        N.callout("Analogy: Rising flood water. Stack entries are 'peaks above water'. A new high-water price floods lower peaks and absorbs their area in one step.", "🌊", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.stack = []", {"code": True}), " — initialize the monotonic decreasing stack (list of (price, span) pairs)."])),
    N.para(N.rich([("span = 1", {"code": True}), " — today always counts itself; start the running span at 1."])),
    N.para(N.rich([("while self.stack and self.stack[-1][0] <= price", {"code": True}), " — pop while the stack top's price is ≤ today's price (today beats those days)."])),
    N.para(N.rich([("span += self.stack.pop()[1]", {"code": True}), " — absorb the popped entry's pre-computed span. Range compression: a single pop can cover many days."])),
    N.para(N.rich([("self.stack.append((price, span))", {"code": True}), " — push today's compressed entry (price, accumulated span) for future reuse."])),
    N.para(N.rich([("return span", {"code": True}), " — the total consecutive days with price ≤ today, including today."])),
    N.divider(),
]

# Solution 2: Brute Force
sol2_code = """class StockSpannerBrute:
    def __init__(self):
        self.prices = []   # store all prices

    def next(self, price: int) -> int:
        self.prices.append(price)
        span = 0
        for p in reversed(self.prices):
            if p <= price:
                span += 1
            else:
                break   # first strictly greater price stops the run
        return span"""

blocks += [
    N.h2("Solution 2 — Brute Force (Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Directly simulate: for each call, scan backward through all stored prices until you find one strictly greater than today."),
        N.h4("What Doesn't Work (at scale)"),
        N.para("Every call potentially scans O(n) prior prices. For n total calls, total work is O(n²). For LeetCode constraints (up to 10^4 calls), this is 10^8 operations — too slow."),
        N.h4("The Key Observation"),
        N.para("The brute force correctly computes the span but wastes time re-examining days already analyzed in prior calls. The monotonic stack avoids this redundancy by caching spans."),
        N.h4("Building the Solution"),
        N.para("Store all prices in a list. For each new price, reverse-iterate from the end and count until you find a strictly greater price or exhaust the list."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.prices.append(price)", {"code": True}), " — record today's price in history."])),
    N.para(N.rich([("for p in reversed(self.prices)", {"code": True}), " — scan backwards from today."])),
    N.para(N.rich([("if p <= price: span += 1", {"code": True}), " — count each day with price ≤ today."])),
    N.para(N.rich([("else: break", {"code": True}), " — first price > today ends the consecutive run."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",          "Time (per call)",    "n calls total", "Space"],
        ["Brute Force",       "O(n)",               "O(n²)",         "O(n)"],
        ["Monotonic Stack ✓", "O(1) amortized",     "O(n)",          "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stack / Queue"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Previous Greater Element Count (Monotonic Stack with Span Compression)"])),
    N.callout(
        "When to recognize this pattern:\n• 'How far back until a greater/smaller element?' → Previous/Next Greater Element\n• Online (streaming) data with lookback queries → Monotonic stack\n• 'Consecutive days/elements satisfying a condition' with efficient aggregation → Store (value, count) on stack\n• Histogram, temperature, stock, building visibility — classic monotonic stack signals",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (monotonic stack / previous greater element):"),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), " (Medium) — for each day, days until a warmer temperature; offline next-greater-element with stack (#739)"])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), " (Easy) — find next greater element in nums2 for each element in nums1; classic monotonic stack (#496)"])),
    N.bullet(N.rich([("Next Greater Element II", {"bold": True}), " (Medium) — circular array variant; process array twice (#503)"])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — previous and next smaller element on both sides; most powerful monotonic stack application (#84)"])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — monotonic stack to track walls while scanning (#42)"])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), " (Medium) — count subarrays where each element is the minimum; previous/next smaller with span (#907)"])),
    N.bullet(N.rich([("132 Pattern", {"bold": True}), " (Medium) — track second-max with monotonic stack scanning right-to-left (#456)"])),
    N.para("These problems all leverage the monotonic stack's ability to efficiently answer 'what is the nearest element satisfying a comparison condition'."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue Patterns → Monotonic Stack: Next Greater\nSub-Pattern verified: Previous Greater Element Count (Analysis — span compression variant)", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("online_stock_span")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"Total blocks appended: {len(blocks)}")
