"""gen_fruit_into_baskets.py — Notion update for LeetCode #904 Fruit Into Baskets."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f8-b672-fe8e18bed454"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(PAGE_ID,
    difficulty="Medium",
    number=904,
    pattern="Sliding Window",
    subpatterns=["At Most K Distinct (Sliding Window Variable)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Longest subarray with ≤2 distinct values: expand right, shrink left when 3rd type enters.",
    icon="🟡"
)
print("Properties set OK")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3) Rebuild body ─────────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are visiting a farm with a row of fruit trees. Each tree holds exactly one type of fruit. You have exactly "),
        ("2", {"bold": True}),
        (" baskets, and each basket holds only one type of fruit — but any quantity of that type. Starting from any tree, you must pick fruits moving right through consecutive trees. You cannot skip trees. Return the maximum number of fruits you can pick. (Equivalently: find the length of the longest contiguous subarray containing at most 2 distinct values.)")
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}), ("fruits = [1,2,1]", {"code": True}),
        (" → Answer: ", {}), ("3", {"bold": True}),
        (" (pick all trees, types {1,2} fit in 2 baskets)")
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}), ("fruits = [0,1,2,2]", {"code": True}),
        (" → Answer: ", {}), ("3", {"bold": True}),
        (" (best subarray is [1,2,2], types {1,2}; can't take all 4 because that needs 3 baskets)")
    ])),
    N.divider(),
]

# ── Solution 1: Variable Sliding Window ──────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Variable Sliding Window with Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Ignore the fruit/basket story. We are looking for the longest contiguous subarray with at most 2 distinct integer values. That's it."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force approach tries every possible starting index and extends rightward until a 3rd type appears — O(n²) time. For n=10⁵ that's 10¹⁰ operations: too slow."),
        N.h4("The Key Observation"),
        N.para("Two signals flag the sliding window pattern: (1) 'longest contiguous subarray' and (2) 'at most K distinct elements.' When both appear together, a variable sliding window is almost always optimal. The window expands right greedily; it shrinks left reactively the moment the constraint (at most 2 distinct types) is violated."),
        N.h4("Building the Solution"),
        N.para("Maintain a hash map basket that counts occurrences of each fruit type currently inside the window. Expand: add fruits[right] to basket. If len(basket) > 2, shrink left: decrement basket[fruits[left]], delete the key if count reaches 0, advance left. After the while loop, record res = max(res, right - left + 1)."),
        N.callout("Analogy: Think of a physical shopping cart with 2 labeled slots. Whenever a 3rd product appears, you must unload from the left end of the conveyor belt until the 3rd product's slot becomes empty and you reassign it.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def totalFruit(fruits):
    basket = {}
    left = 0
    res = 0
    for right, fruit in enumerate(fruits):
        basket[fruit] = basket.get(fruit, 0) + 1
        while len(basket) > 2:
            left_fruit = fruits[left]
            basket[left_fruit] -= 1
            if basket[left_fruit] == 0:
                del basket[left_fruit]
            left += 1
        res = max(res, right - left + 1)
    return res"""),
    N.h3("Line by Line"),
    N.para(N.rich([("basket = {}", {"code": True}), " — Hash map from fruit type → count of that type inside the current window [left, right]."])),
    N.para(N.rich([("left = 0", {"code": True}), " — Left boundary of the sliding window; starts at index 0."])),
    N.para(N.rich([("res = 0", {"code": True}), " — Running maximum of valid window sizes seen so far."])),
    N.para(N.rich([("for right, fruit in enumerate(fruits):", {"code": True}), " — Right boundary expands one position per iteration; fruit is the newly included value."])),
    N.para(N.rich([("basket[fruit] = basket.get(fruit, 0) + 1", {"code": True}), " — Add this fruit to the window. Creates a new key with count 1 if unseen, else increments existing count."])),
    N.para(N.rich([("while len(basket) > 2:", {"code": True}), " — 3 distinct types in window → invalid. Must be a while loop, not if, because one shrink step may not eliminate the extra type."])),
    N.para(N.rich([("left_fruit = fruits[left]", {"code": True}), " — Identify which fruit type is at the leftmost position of the window."])),
    N.para(N.rich([("basket[left_fruit] -= 1", {"code": True}), " — Remove one occurrence of that fruit from the window count."])),
    N.para(N.rich([("if basket[left_fruit] == 0: del basket[left_fruit]", {"code": True}), " — If we've removed ALL occurrences of that type, evict it from the map. Now len(basket) decrements by 1."])),
    N.para(N.rich([("left += 1", {"code": True}), " — Shrink window left boundary."])),
    N.para(N.rich([("res = max(res, right - left + 1)", {"code": True}), " — Window is now valid (≤ 2 types). Record its size."])),
    N.para(N.rich([("return res", {"code": True}), " — The largest valid window size ever seen."])),
    N.divider(),
]

# ── Solution 2: Brute Force ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force Nested Loops"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible starting index. For each start, extend rightward adding fruits one by one. Stop when the 3rd distinct type appears."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n²) time — for each of n starting positions we scan up to n ending positions. With n=10⁵, this is 10¹⁰ operations, leading to Time Limit Exceeded on LeetCode."),
        N.h4("The Key Observation"),
        N.para("The brute force is a valid conceptual starting point to propose in an interview, then immediately offer to optimize."),
        N.h4("Building the Solution"),
        N.para("Two nested loops: outer loop picks the start i, inner loop extends j rightward adding fruits to a set. When the set reaches size 3, break and try the next starting position."),
    ]),
    N.h3("Code"),
    N.code(
"""def totalFruit(fruits):
    res = 0
    for i in range(len(fruits)):
        basket = set()
        for j in range(i, len(fruits)):
            basket.add(fruits[j])
            if len(basket) > 2:
                break
            res = max(res, j - i + 1)
    return res"""),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(fruits)):", {"code": True}), " — O(n) starting positions."])),
    N.para(N.rich([("basket = set()", {"code": True}), " — Track distinct types seen since start i (a set suffices here since we don't need counts)."])),
    N.para(N.rich([("basket.add(fruits[j])", {"code": True}), " — Extend window to index j."])),
    N.para(N.rich([("if len(basket) > 2: break", {"code": True}), " — 3rd type encountered — no point extending further from this start."])),
    N.para(N.rich([("res = max(res, j - i + 1)", {"code": True}), " — Record best length seen."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(1)"],
        ["Variable Sliding Window (optimal)", "O(n)", "O(1)"],
    ]),
    N.para("The sliding window achieves O(n) because each element enters the window exactly once (right scan) and exits at most once (left shrink). Total work = O(2n) = O(n). The basket map holds at most 3 keys momentarily, so space is effectively O(1) — bounded by the constant 2 (or 3 during transition)."),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window (variable-size)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "At Most K Distinct (Sliding Window Variable) — specifically K=2 here."])),
    N.callout(
        "When to recognize this pattern: (1) You need the LONGEST/SHORTEST contiguous subarray/substring. "
        "(2) There is a constraint involving AT MOST K distinct elements. "
        "(3) The window becomes invalid by adding one element → shrink from left until valid. "
        "(4) You need to know when an element FULLY LEAVES the window → use a count map, not just a set.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same At Most K Distinct sliding window technique:"),
    N.bullet(N.rich([("Longest Substring with At Most Two Distinct Characters", {"bold": True}), " (Medium) — Identical problem on a string. LeetCode #159."])),
    N.bullet(N.rich([("Longest Substring with At Most K Distinct Characters", {"bold": True}), " (Medium) — Direct generalization: replace 2 with K. LeetCode #340."])),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), " (Medium) — At most 1 occurrence per type; same expand/shrink mechanic. LeetCode #3."])),
    N.bullet(N.rich([("Max Consecutive Ones III", {"bold": True}), " (Medium) — At most K zeros allowed inside window; same pattern. LeetCode #1004."])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), " (Hard) — Must contain all chars of t; harder validity condition but same shrink idea. LeetCode #76."])),
    N.bullet(N.rich([("Subarrays with K Different Integers", {"bold": True}), " (Hard) — Exactly K distinct = atMost(K) - atMost(K-1). LeetCode #992."])),
    N.para("These problems share the core pattern: maintain a window with a hash map of counts, expand right freely, and shrink left reactively when the count-of-distinct constraint is violated."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.4–1.5 (Sliding Window: Dynamic/Variable). Sub-Pattern: At Most K Distinct.", "📚", "gray_background"),
]

# ── Interactive Explainer Embed ───────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("fruit_into_baskets")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
