"""
gen_number_of_visible_people_in_a_queue.py
Regenerates the Notion page for LC #1944 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8113-8fde-e218dd41235d"
SLUG = "number_of_visible_people_in_a_queue"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1944,
    pattern="Stack",
    subpatterns=["Monotonic Stack (Decreasing)"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Process right-to-left with a decreasing monotone stack; each pop = one visible person, plus 1 if a taller blocker remains on the stack.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build full body ─────────────────────────────────────────────────────
PROBLEM_STMT = (
    "There are n people standing in a queue numbered 0 to n-1 from left to right. "
    "You are given an array heights of n integers where heights[i] is the height of the i-th person. "
    "A person i can see person j (j > i) if and only if every person between them is strictly shorter "
    "than min(heights[i], heights[j]). Return an array answer of length n where answer[i] is the "
    "number of people person i can see to their right."
)

BRUTE_CODE = """\
def canSeePersonsCount(heights: list[int]) -> list[int]:
    n = len(heights)
    ans = [0] * n
    for i in range(n):
        max_h = 0
        for j in range(i + 1, n):
            if heights[j] > max_h:
                ans[i] += 1        # j is visible (taller than anyone between i and j)
            max_h = max(max_h, heights[j])
            if heights[j] >= heights[i]:
                break              # taller wall blocks everything beyond
    return ans
# Time: O(n^2)  Space: O(1)"""

OPTIMAL_CODE = """\
def canSeePersonsCount(heights: list[int]) -> list[int]:
    n = len(heights)
    ans = [0] * n
    stack = []                         # monotone decreasing stack of heights

    for i in range(n - 1, -1, -1):    # right to left
        count = 0
        while stack and stack[-1] < heights[i]:
            stack.pop()                # person i can see over this shorter person
            count += 1
        if stack:
            count += 1                 # taller/equal blocker is also visible
        ans[i] = count
        stack.append(heights[i])       # push i as a candidate for people to the left

    return ans
# Time: O(n)  Space: O(n)"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# Solution 1 — Brute Force
blocks += [
    N.h2("Solution 1 — Brute Force: Nested Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each person i, scan everyone to their right. A person j is visible if no one between i and j is as tall as min(heights[i], heights[j]). Equivalently, track a 'max height seen so far': j is visible if heights[j] exceeds that max (or j is the immediate right neighbour). Once heights[j] >= heights[i], stop — everything beyond is blocked from i's perspective."),
        N.h4("What Doesn't Work at Scale"),
        N.para("This O(n^2) scan works correctly but is too slow for n=100,000 (10^10 operations). Each person independently re-scans the same elements — massive redundancy."),
        N.h4("The Key Observation"),
        N.para("Every right-side scan from person i is doing work that, partially, was already done for person i+1. The right side has structure we can pre-summarize."),
        N.h4("Building the Solution"),
        N.para("For each i (left to right): initialize max_h=0. Scan j from i+1: if heights[j] > max_h, it is visible (increment count). Always update max_h. Stop when heights[j] >= heights[i] since that wall blocks everything beyond."),
        N.callout("Analogy: Standing in a crowd and checking if you can see the stage — you count each head you see over before a taller person blocks your sightline.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), " — process each person as the observer."])),
    N.para(N.rich([("max_h = 0", {"code": True}), " — track the tallest person seen between i and j so far."])),
    N.para(N.rich([("if heights[j] > max_h:", {"code": True}), " — person j is visible because no taller wall stands between i and j."])),
    N.para(N.rich([("max_h = max(max_h, heights[j])", {"code": True}), " — update the running maximum blocking height."])),
    N.para(N.rich([("if heights[j] >= heights[i]: break", {"code": True}), " — found a wall at least as tall as person i; nothing beyond is visible to i."])),
    N.divider(),
]

# Solution 2 — Optimal (Interview Pick)
blocks += [
    N.h2("Solution 2 — Monotonic Stack: Right-to-Left (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each person i, how many people to their right can they see before hitting a taller wall? This is essentially a 'next greater element' problem with counting — exactly the territory of monotonic stacks."),
        N.h4("What Doesn't Work"),
        N.para("Left-to-right processing: when we handle person i, we don't know the right side yet. We'd need to scan forward for each i — that's O(n^2)."),
        N.h4("The Key Observation"),
        N.para("If we process right to left, by the time we handle person i, the entire right side is already summarized in the stack. The stack holds only the 'relevant' heights — those that could be seen from the left — in strictly decreasing order. Shorter heights behind taller ones are irrelevant."),
        N.h4("Building the Solution"),
        N.para("Process right to left. For each i: while the stack top is shorter than heights[i], pop it (person i can see that shorter person, count++). If the stack is still non-empty after all pops, there is one more visible person: the taller blocker at the top (+1). Then push heights[i] and store the count."),
        N.callout("The '+1 for the remaining stack top' is the most common bug. After all shorter people are counted via pops, there is one final visible person: the first one taller than you, who blocks everything beyond them.", "⚠️", "red_background"),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — monotone decreasing stack of heights; will hold right-side candidates."])),
    N.para(N.rich([("for i in range(n - 1, -1, -1):", {"code": True}), " — scan from right (n-1) to left (0)."])),
    N.para(N.rich([("count = 0", {"code": True}), " — reset visibility count for this person."])),
    N.para(N.rich([("while stack and stack[-1] < heights[i]:", {"code": True}), " — pop all shorter people: person i can see over them (they're visible but not blockers)."])),
    N.para(N.rich([("stack.pop();  count += 1", {"code": True}), " — remove from stack (they'd be hidden from further-left people by i anyway); count one more visible person."])),
    N.para(N.rich([("if stack:  count += 1", {"code": True}), " — the remaining top is >= heights[i]. Person i CAN see them (the taller wall itself is visible), but cannot see past them."])),
    N.para(N.rich([("ans[i] = count", {"code": True}), " — record total visible count for person i."])),
    N.para(N.rich([("stack.append(heights[i])", {"code": True}), " — push i's height onto the stack as a candidate for people to the left."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (Nested Scan)", "O(n²)", "O(1)"],
        ["Monotonic Stack (Optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stack / Monotonic Stack"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Monotonic Stack (Decreasing) — processed right to left, counting elements popped before a taller blocker"])),
    N.callout(
        "When to recognize: 'How many can you see before a taller one blocks?' / 'Next Greater Element with counting' / Heights or buildings in a line where one element blocks future visibility. Requires O(n) when naive O(n²) scan is obvious.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same monotone stack technique:"),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), " (Medium) — next greater element with day-distance; same decreasing stack right-to-left structure."])),
    N.bullet(N.rich([("Next Greater Element I & II", {"bold": True}), " (Medium) — classic monotone stack: first element larger than each in the array."])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — previous/next smaller element using an ascending monotone stack."])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — blocking + max heights dynamic; can be solved with monotone stack."])),
    N.bullet(N.rich([("Buildings With an Ocean View", {"bold": True}), " (Medium) — right-to-left scan, keep only decreasing heights, very similar structure."])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), " (Medium) — monotone stack counts contribution of each element as a minimum."])),
    N.para("These problems all share the core insight: a monotone stack efficiently answers 'next greater/smaller' queries in O(n) by making each element enter and exit the stack at most once."),
    N.callout("📚 Guide Reference: Stack & Queue section — Monotonic Stack (Decreasing)", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4) Append all blocks ───────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
