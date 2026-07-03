"""gen_daily_temperatures.py — Notion update for Daily Temperatures (#739)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81cf-9572-c1ca68306cdc"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=739,
    pattern="Stack",
    subpatterns=["Next Greater Index Difference"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Use a monotonic decreasing stack of indices; when a warmer day arrives, pop and record the wait as i - prev.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of integers ", {}),
        ("temperatures", {"code": True}),
        (" representing the daily temperatures, return an array ", {}),
        ("answer", {"code": True}),
        (" such that ", {}),
        ("answer[i]", {"code": True}),
        (" is the number of days you have to wait after the ", {}),
        ("i", {"code": True}),
        ("-th day to get a warmer temperature. If there is no future day for which this is possible, keep ", {}),
        ("answer[i] == 0", {"code": True}),
        (" instead.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("Input: temperatures = [73,74,75,71,69,72,76,73]  →  Output: [1,1,4,2,1,1,0,0]", {"code": True}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ temperatures.length ≤ 100,000; 30 ≤ temperatures[i] ≤ 100", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Monotonic Stack (Optimal / Interview Pick) ──
sol1_code = """\
def dailyTemperatures(temps: list[int]) -> list[int]:
    n = len(temps)
    answer = [0] * n         # Default 0: "no warmer day" for all positions
    stack = []               # Stack holds INDICES of unresolved days

    for i in range(n):
        # While current day is warmer than the day at stack top
        while stack and temps[i] > temps[stack[-1]]:
            prev = stack.pop()          # Pop the cold waiting day
            answer[prev] = i - prev     # Wait = current index - cold day index
        stack.append(i)      # Push current; it now waits for ITS warmer day

    # Remaining stack entries stay 0 — already initialized correctly
    return answer"""

blocks += [
    N.h2("Solution 1 — Monotonic Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each temperature, we need to find the nearest future temperature that is strictly greater. The answer is the index difference. This is the classic 'next greater element' problem, dressed up as a weather question."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach scans forward from each day until it finds a warmer one — O(n²) worst case. With temperatures in decreasing order ([100,99,98,...,1]), every day scans all remaining days and finds nothing. For n=100,000 that's 5 billion comparisons."),
        N.h4("The Key Observation"),
        N.para("The inefficiency comes from re-examining already-visited days. Can we remember 'pending' days without rescanning? If we maintain a stack of unresolved days in decreasing temperature order, then a new warmer day instantly resolves ALL colder pending days in one pass down the stack."),
        N.h4("Building the Solution"),
        N.para("Maintain a stack of day indices whose warmer future we haven't found yet. The temperatures on the stack decrease from bottom to top. For each new day i: pop any stack entry whose temperature is less than temps[i] — that entry's answer is i - prev. Then push i. After scanning all days, remaining entries have no warmer future and keep their 0."),
        N.callout(
            "Analogy: Imagine people waiting in a queue for a sunny day. When sunshine (warmer temp) arrives, everyone colder in the queue gets their 'wait time' stamped and leaves. Only those who remain didn't get their sunny day.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Monotonic Stack"),
    N.para(N.rich([
        ("Monotonic Stack", {"bold": True}),
        (" — A stack that maintains elements in strictly increasing or strictly decreasing order. For 'next greater element' variants, we use a ", {}),
        ("monotonically decreasing", {"bold": True}),
        (" stack (temperatures decrease bottom-to-top). When a new element breaks the monotone property, we pop until it's restored.", {}),
    ])),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("At every step, the stack holds indices i₁ < i₂ < ... < iₖ such that temps[i₁] ≥ temps[i₂] ≥ ... ≥ temps[iₖ]. Each index represents a day still waiting for its warmer future.", {}),
    ])),
    N.para(N.rich([
        ("Why it works: ", {"bold": True}),
        ("When we pop index prev at step i, day i is the NEAREST warmer day for prev. If any intermediate day k (prev < k < i) had been warmer than temps[prev], we would have already popped prev at step k. Reaching step i with prev still on the stack proves no closer warmer day exists.", {}),
    ])),
    N.para(N.rich([
        ("O(n) amortized: ", {"bold": True}),
        ("Each index is pushed exactly once and popped at most once. Total push+pop operations ≤ 2n regardless of how many pops occur per iteration. The while loop inside the for loop does NOT make this O(n²).", {}),
    ])),
    N.para(N.rich([
        ("Recognize when: ", {"bold": True}),
        ("'For each element, find the next/previous greater/smaller element.' 'How many steps until a larger/smaller value?' 'Largest rectangle' or 'trapping rain water' variants.", {}),
    ])),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("answer = [0] * n", {"code": True}), (" — Initialize all answers to 0. Days that never find a warmer future keep this default. No post-processing needed for 'no answer' cases.", {})])),
    N.para(N.rich([("stack = []", {"code": True}), (" — Empty stack to hold indices of days waiting for a warmer future.", {})])),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — Scan every day exactly once, left to right.", {})])),
    N.para(N.rich([("while stack and temps[i] > temps[stack[-1]]:", {"code": True}), (" — Current day is warmer than the most recently unresolved day. Both conditions needed: non-empty stack AND strictly warmer temperature.", {})])),
    N.para(N.rich([("prev = stack.pop()", {"code": True}), (" — Remove the cold day from the waiting room. Its wait just ended.", {})])),
    N.para(N.rich([("answer[prev] = i - prev", {"code": True}), (" — The wait is simply the index difference. Day i is guaranteed to be the nearest warmer day for prev.", {})])),
    N.para(N.rich([("stack.append(i)", {"code": True}), (" — Push current day's index. It now waits in the queue for ITS warmer future.", {})])),
    N.para(N.rich([("return answer", {"code": True}), (" — Any indices remaining in the stack found no warmer day. Their answer stays 0, already set during initialization.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
sol2_code = """\
def dailyTemperatures_brute(temps: list[int]) -> list[int]:
    n = len(temps)
    answer = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temps[j] > temps[i]:
                answer[i] = j - i
                break          # Only the NEAREST warmer day matters
    return answer"""

blocks += [
    N.h2("Solution 2 — Brute Force"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest reading of the problem: for each day i, scan j = i+1, i+2, ... and stop at the first j where temps[j] > temps[i]. The answer is j - i, or 0 if no such j exists."),
        N.h4("What Doesn't Work"),
        N.para("Nothing is wrong logically — brute force is always correct. The issue is performance: in the worst case (temperatures strictly decreasing), no day ever finds a warmer one, and we do n-1 + n-2 + ... + 1 = n(n-1)/2 comparisons. For n=100,000 that exceeds any reasonable time limit."),
        N.h4("The Key Observation"),
        N.para("Brute force is the right starting point in an interview — show you understand the problem before optimizing. Then explain that the redundancy is re-examining days that are already 'cooler than the current candidate' and that we could remember unresolved days more efficiently."),
        N.h4("Building the Solution"),
        N.para("Two nested loops: outer iterates over each day i, inner scans all future days j looking for the first warmer one. Break as soon as found. Record j - i as the wait."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — Outer loop: process each day.", {})])),
    N.para(N.rich([("for j in range(i + 1, n):", {"code": True}), (" — Inner loop: scan forward from i+1.", {})])),
    N.para(N.rich([("if temps[j] > temps[i]:", {"code": True}), (" — Found a strictly warmer day.", {})])),
    N.para(N.rich([("answer[i] = j - i; break", {"code": True}), (" — Record the wait and stop — only the NEAREST warmer day counts.", {})])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(1) extra"],
        ["Monotonic Stack (optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stack / Queue (Monotonic Stack)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Next Greater Index Difference — a variant of Monotonic Stack: Next Greater Element that records index differences instead of values", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("'For each element, find the nearest future element that is greater/smaller.' 'How many steps until a larger/smaller value?' 'What is the span/wait until a condition is met?' Any problem where each element looks rightward for the first element satisfying a comparison.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Monotonic Stack — Next Greater/Smaller):"),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), (" (Easy) — Same stack logic; results stored in hash map for a second array lookup (#496)", {})])),
    N.bullet(N.rich([("Next Greater Element II", {"bold": True}), (" (Medium) — Circular array variant; process the doubled array with modular indexing (#503)", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Monotonic stack finds previous/next smaller bar to bound each rectangle's width (#84)", {})])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), (" (Hard) — Monotonic stack pops resolve trapped water volumes between taller boundaries (#42)", {})])),
    N.bullet(N.rich([("Online Stock Span", {"bold": True}), (" (Medium) — Count consecutive days with price ≤ today; stack accumulates cumulative spans (#901)", {})])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), (" (Medium) — Monotonic stack determines each element's contribution as minimum of subarrays (#907)", {})])),
    N.bullet(N.rich([("Removing Stars From a String", {"bold": True}), (" (Medium) — Stack-based sequential element removal (#2390)", {})])),
    N.para("These problems share the core technique: maintain a monotonic stack so that each element's 'governing' neighbor can be determined in O(1) amortized per element."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue Patterns → Monotonic Stack: Next Greater", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("daily_temperatures")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
