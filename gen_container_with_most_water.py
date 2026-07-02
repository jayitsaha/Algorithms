"""
Notion updater for: Container With Most Water (LC #11)
Run from the Algorithms directory alongside notion_lib.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-816c-a911-e2ed89359efc"
SLUG = "container_with_most_water"

# ── 1. Properties ────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=11,
    pattern="Two Pointers",
    subpatterns=["Opposite Direction (Greedy)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Start at widest span; always move the shorter-wall pointer inward — it is the bottleneck and the only move that can improve area.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing content ─────────────────────────────────────────────────
print("Wiping old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks.")

# ── 3. Build body ────────────────────────────────────────────────────────────
print("Building blocks...")

blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer array ", {}),
        ("height", {"code": True}),
        (" of length ", {}),
        ("n", {"code": True}),
        (". There are ", {}),
        ("n", {"code": True}),
        (" vertical lines drawn such that the two endpoints of the ", {}),
        ("i", {"code": True}),
        ("-th line are ", {}),
        ("(i, 0)", {"code": True}),
        (" and ", {}),
        ("(i, height[i])", {"code": True}),
        (". Find two lines that together with the x-axis form a container that holds the most water. Return the maximum amount of water a container can store.", {})
    ])),
    N.callout(
        N.rich([
            ("Area formula: ", {"bold": True}),
            ("min(height[left], height[right]) × (right − left)", {"code": True}),
            (". The shorter wall is always the bottleneck.", {})
        ]),
        "📐", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1: Brute Force ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the maximum of min(height[i], height[j]) × (j − i) over all pairs i < j. The simplest reading: check every pair."),
        N.h4("What Doesn't Work at Scale"),
        N.para("n can be up to 100,000. n² = 10,000,000,000 operations — this will TLE for large inputs. Good for understanding correctness, not for the actual submission."),
        N.h4("The Key Observation"),
        N.para("For each left wall, we could scan every right wall and compute the area. The maximum over all pairs is the answer. Completely correct, just slow."),
        N.h4("Building the Solution"),
        N.para("Two nested loops: outer picks the left wall (index i), inner picks every right wall (index j > i). Compute area each time, track the maximum."),
        N.callout("Analogy: Checking every table in a restaurant to find the most spacious spot — correct, but you'd check all of them even if the first one was perfect.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def maxArea_brute(height: list[int]) -> int:\n"
        "    n = len(height)\n"
        "    best = 0\n"
        "    for i in range(n):\n"
        "        for j in range(i + 1, n):\n"
        "            area = min(height[i], height[j]) * (j - i)\n"
        "            best = max(best, area)\n"
        "    return best",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(height)", {"code": True}), (" — store length for loop bounds.")])),
    N.para(N.rich([("best = 0", {"code": True}), (" — running maximum, starts at 0 (area is always non-negative).")])),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — outer loop: pick each possible left wall index.")])),
    N.para(N.rich([("for j in range(i + 1, n):", {"code": True}), (" — inner loop: pick every right wall to the right of i.")])),
    N.para(N.rich([("area = min(height[i], height[j]) * (j - i)", {"code": True}), (" — area = shorter wall height × horizontal distance.")])),
    N.para(N.rich([("best = max(best, area)", {"code": True}), (" — update maximum if this pair is better.")])),
    N.para(N.rich([("return best", {"code": True}), (" — maximum area over all n(n-1)/2 pairs.")])),
    N.divider(),
]

# ── Solution 2: Two Pointer (Optimal) ────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Two Pointer: Opposite Direction Greedy (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to pick one pair (left, right). Two forces: wider container is better (more width); taller bottleneck is better (more height). Can we avoid checking all pairs?"),
        N.h4("What Doesn't Work"),
        N.para("Always picking the tallest walls is wrong — width matters too. Picking just the outermost pair is also wrong — it may have a very short bottleneck wall."),
        N.h4("The Key Observation"),
        N.para("Start with the widest container (left=0, right=n-1). The only way to improve area while reducing width is to replace the shorter wall with a taller one. Moving the shorter pointer inward is the only action that can achieve this. Moving the taller pointer inward keeps the same bottleneck with less width — provably worse."),
        N.h4("Building the Solution"),
        N.para("Initialize left=0, right=n-1. At each step: (1) compute area, update max. (2) Move the pointer at the shorter wall inward. Repeat until left >= right. The skipped pairs are all bounded by the current area — so no optimal pair is missed."),
        N.callout("Analogy: Two people holding a plank from opposite ends. The plank height is limited by the shorter person. To raise it, you ask the shorter person to step inward — maybe they'll find someone taller. Asking the taller person to step in loses span without fixing the height constraint.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def maxArea(height: list[int]) -> int:\n"
        "    left, right = 0, len(height) - 1\n"
        "    max_area = 0\n"
        "    while left < right:\n"
        "        h = min(height[left], height[right])\n"
        "        w = right - left\n"
        "        max_area = max(max_area, h * w)\n"
        "        if height[left] < height[right]:\n"
        "            left += 1\n"
        "        else:\n"
        "            right -= 1\n"
        "    return max_area",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("left, right = 0, len(height) - 1", {"code": True}), (" — pointers start at outermost walls — widest possible container.")])),
    N.para(N.rich([("max_area = 0", {"code": True}), (" — running maximum; starts at 0.")])),
    N.para(N.rich([("while left < right:", {"code": True}), (" — loop while there is a valid container (two distinct walls).")])),
    N.para(N.rich([("h = min(height[left], height[right])", {"code": True}), (" — shorter wall sets the water level — anything taller spills.")])),
    N.para(N.rich([("w = right - left", {"code": True}), (" — horizontal distance between the two walls.")])),
    N.para(N.rich([("max_area = max(max_area, h * w)", {"code": True}), (" — update if this container beats the current best.")])),
    N.para(N.rich([("if height[left] < height[right]:", {"code": True}), (" — left wall is the bottleneck. Moving right would keep same bottleneck with less width — suboptimal.")])),
    N.para(N.rich([("left += 1", {"code": True}), (" — advance left; skipped pairs (old_left, x<right) all have area ≤ current area.")])),
    N.para(N.rich([("else: right -= 1", {"code": True}), (" — right is the bottleneck (or equal). Retreat right; same skipping argument applies.")])),
    N.para(N.rich([("return max_area", {"code": True}), (" — all pairs considered or eliminated — guaranteed optimal.")])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n²)", "O(1)", "Checks every pair — TLE for large n"],
        ["Two Pointer (Optimal)", "O(n)", "O(1)", "Single pass, each pointer moves at most n steps total"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Opposite Direction (Greedy)")])),
    N.callout(
        "When to recognize this pattern: (1) Finding an optimal pair from an array. (2) Objective depends on BOTH the values at the pair AND the distance between them. (3) A greedy argument exists: one pointer-move direction is provably suboptimal — so you can eliminate it without checking. (4) You want O(n) instead of O(n²).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Opposite-Direction Two-Pointer technique:"),
    N.bullet(N.rich([("Two Sum II — Input Array Is Sorted", {"bold": True}), (" (Medium) — Sorted array; move left if sum too small, right if too large. Same convergence argument.")])),
    N.bullet(N.rich([("3Sum", {"bold": True}), (" (Medium) — Fix one element; apply this exact two-pointer shrink on the remaining subarray.")])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), (" (Hard) — Related water problem but asks for total water over ALL positions, not one container. Uses max-left/max-right tracking.")])),
    N.bullet(N.rich([("Valid Palindrome", {"bold": True}), (" (Easy) — Simplest form of opposite-direction two pointers: compare characters from both ends until they meet.")])),
    N.bullet(N.rich([("Boats to Save People", {"bold": True}), (" (Medium) — Greedy pair matching: heaviest + lightest. Move the heavier pointer if they don't fit — identical structural pattern.")])),
    N.bullet(N.rich([("Minimize Maximum Pair Sum in Array", {"bold": True}), (" (Medium) — Sort, then pair min with max using opposite-direction pointers to minimize the maximum pair sum.")])),
    N.para("These problems all share the core technique: two pointers converging from opposite ends, with a greedy argument proving one direction of movement is always safe to eliminate."),
    N.callout("📚 Reference: Two Pointers → Opposite Direction (Greedy) sub-pattern. Verified against DSA Patterns and Sub-Patterns Guide.", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all ───────────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
