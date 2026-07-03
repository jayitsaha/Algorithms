"""
gen_assign_cookies.py — Notion page generator for Assign Cookies (LC #455)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Create new page (notion_page_id is null) ──────────────────────────────
print("Creating Notion page for Assign Cookies...")
PAGE_ID = N.create_page("Assign Cookies", 455, "Easy", "🟢")
print(f"Created page: {PAGE_ID}")

# ── Set properties ────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=455,
    pattern="Greedy",
    subpatterns=["Sort Both Greedy Match"],
    tc="O(n log n + m log m)",
    sc="O(1)",
    key_insight="Sort both arrays; give each child the smallest cookie that satisfies them.",
    icon="🟢"
)
print("Properties set.")

# ── Build page body ───────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two integer arrays ", {}),
        ("g", {"code": True}),
        (" (greed factors of children) and ", {}),
        ("s", {"code": True}),
        (" (cookie sizes), assign cookies to children such that a cookie ", {}),
        ("s[j]", {"code": True}),
        (" satisfies child ", {}),
        ("i", {"code": True}),
        (" if ", {}),
        ("s[j] >= g[i]", {"code": True}),
        (". Each cookie can be used for at most one child. Return the maximum number of content children.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Greedy Two-Pointer (Interview Pick) ───────────────────────
blocks += [
    N.h2("Solution 1 — Greedy Two-Pointer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to maximize the count of (child, cookie) pairs where cookie size >= child's greed. This is a maximum matching problem with a threshold condition."),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries all O(n × m) cookie-child pairs and checks each — correct but slow. There's no need to try every pair once we sort."),
        N.h4("The Key Observation"),
        N.para("For the least-greedy child, use the smallest cookie that still satisfies them. Using a bigger cookie wastes it — that bigger cookie might be the only one that can satisfy a greedier child. This local greedy choice is globally optimal (proven by exchange argument)."),
        N.h4("Building the Solution"),
        N.para("1. Sort g ascending (least greedy first) and s ascending (smallest first). 2. Use a child pointer starting at 0. 3. Sweep cookies smallest to largest: if cookie >= g[child], match them (count++, child++). Always advance cookie pointer. 4. Return count."),
        N.callout(
            "Analogy: A cafeteria giving out snacks. Give the pickiest-last kid the smallest snack that satisfies them. Don't waste a large snack on someone who'd be happy with a small one.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(
        "def findContentChildren(g, s):\n"
        "    g.sort()            # Sort greed factors ascending\n"
        "    s.sort()            # Sort cookie sizes ascending\n"
        "    child, count = 0, 0\n"
        "    for cookie in s:    # Try each cookie, smallest first\n"
        "        if child < len(g) and cookie >= g[child]:\n"
        "            count += 1  # This child is content\n"
        "            child += 1  # Move to next (greedier) child\n"
        "    return count"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("g.sort()", {"code": True}), (" — Sort greed factors in-place, ascending. Least-greedy child is now at index 0.", {})])),
    N.para(N.rich([("s.sort()", {"code": True}), (" — Sort cookie sizes in-place, ascending. Smallest cookie is now at index 0.", {})])),
    N.para(N.rich([("child, count = 0, 0", {"code": True}), (" — child pointer into g; count of satisfied children so far.", {})])),
    N.para(N.rich([("for cookie in s:", {"code": True}), (" — Iterate over each cookie, smallest to largest. The cookie is always consumed after this iteration.", {})])),
    N.para(N.rich([("if child < len(g) and cookie >= g[child]:", {"code": True}), (" — Guard against out-of-bounds + satisfaction check: is this cookie big enough for the current child?", {})])),
    N.para(N.rich([("count += 1; child += 1", {"code": True}), (" — On match: increment satisfied count, advance child pointer to next unsatisfied (greedier) child.", {})])),
    N.para(N.rich([("return count", {"code": True}), (" — Total content children after all cookies are tried.", {})])),
    N.divider(),
]

# ── Solution 2: Explicit Two-Pointer While Loop ───────────────────────────
blocks += [
    N.h2("Solution 2 — Explicit Two-Pointer While-Loop"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same greedy logic, but use explicit i (child) and j (cookie) pointers in a while-loop — both pointers are visible at all times, which can be clearer in interviews."),
        N.h4("What Doesn't Work"),
        N.para("This approach does not change the complexity but makes the pointer mechanics explicit, which helps when explaining to an interviewer."),
        N.h4("The Key Observation"),
        N.para("j always advances (cookie is consumed). i advances only on a match. When either array is exhausted, the loop ends."),
        N.h4("Building the Solution"),
        N.para("Maintain i=0 (child) and j=0 (cookie). While both have elements: if s[j] >= g[i], advance i (match). Always advance j. Return i (= number of satisfied children)."),
    ]),
    N.h3("Code"),
    N.code(
        "def findContentChildren(g, s):\n"
        "    g.sort(); s.sort()  # Sort both ascending\n"
        "    i = j = 0           # i = child pointer, j = cookie pointer\n"
        "    while i < len(g) and j < len(s):\n"
        "        if s[j] >= g[i]:  # Cookie j satisfies child i\n"
        "            i += 1        # Advance child pointer\n"
        "        j += 1            # Always consume this cookie\n"
        "    return i              # i = total satisfied children"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("i = j = 0", {"code": True}), (" — i is the child pointer; j is the cookie pointer. Both start at the smallest element.", {})])),
    N.para(N.rich([("while i < len(g) and j < len(s):", {"code": True}), (" — Continue while there are both unsatisfied children and unused cookies.", {})])),
    N.para(N.rich([("if s[j] >= g[i]: i += 1", {"code": True}), (" — Cookie j satisfies child i: advance the child pointer. (j advances regardless on the next line.)", {})])),
    N.para(N.rich([("j += 1", {"code": True}), (" — Always advance cookie pointer. If this cookie matched, it's been used. If too small, it's discarded.", {})])),
    N.para(N.rich([("return i", {"code": True}), (" — i equals how many times we advanced past a matched child — the total satisfied count.", {})])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n × m)", "O(m)"],
        ["Greedy Two-Pointer (for-loop)", "O(n log n + m log m)", "O(1)"],
        ["Greedy Two-Pointer (while-loop)", "O(n log n + m log m)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Greedy", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort Both Greedy Match", {})])),
    N.callout(
        "When to recognize this pattern: 'Maximize count of satisfied pairs with a threshold condition.' "
        "Look for: two arrays where elements are compared pairwise, need to maximize matches, "
        "one-to-one assignment. Sort both arrays and use two pointers.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Sort Both + Greedy Match):"),
    N.bullet(N.rich([("Boats to Save People", {"bold": True}), (" (Medium) — Two-pointer on sorted array to pair heaviest with lightest. (#881)", {})])),
    N.bullet(N.rich([("Advantage Shuffle", {"bold": True}), (" (Medium) — Match sorted array against sorted target greedily to maximize wins. (#870)", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Greedy assignment of tasks to time slots with cooldown period. (#621)", {})])),
    N.bullet(N.rich([("Two City Scheduling", {"bold": True}), (" (Medium) — Assign people to cities greedily by sorting on cost difference. (#1029)", {})])),
    N.bullet(N.rich([("Candy", {"bold": True}), (" (Hard) — Greedy candy distribution satisfying neighbor ordering constraints. (#135)", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), (" (Medium) — Greedy interval scheduling; sort by end time to maximize kept intervals. (#435)", {})])),
    N.para("These problems share the same core technique: sort to enable greedy local choices that compose into a globally optimal solution."),
    N.callout("📚 Pattern: Greedy — Sort Both Greedy Match. Analysis-derived classification.", "📚", "gray_background"),
]

# ── Embed section ─────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("assign_cookies")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ─────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Page URL: https://www.notion.so/{PAGE_ID.replace('-', '')}")
