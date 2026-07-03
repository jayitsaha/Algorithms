"""
gen_binary_search.py — Notion page builder for Binary Search (LeetCode #704)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# notion_page_id is null → create a fresh page
PAGE_ID = N.create_page("Binary Search", 704, "Easy", "🟢")
print(f"Created page: {PAGE_ID}")

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=704,
    pattern="Binary Search",
    subpatterns=["BS: Standard"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Each comparison eliminates half the remaining search space; lo ≤ hi with mid±1 guarantees O(log n) termination.",
    icon="🟢"
)
print("Properties set.")

# 2) Wipe any pre-existing content (fresh page should have none)
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# 3) Build body — exact sequence per SKILL.md Step 4b
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array "), ("nums", {"code": True}),
        (" sorted in ascending order and an integer "), ("target", {"code": True}),
        (", return the index of "), ("target", {"code": True}),
        (" if it is found in the array, or "), ("-1", {"code": True}),
        (" if it is not present. You must write an algorithm with "),
        ("O(log n)", {"code": True}), (" runtime complexity.")
    ])),
    N.divider(),
]

# ── Solution 1: Iterative Binary Search (Interview Pick) ─────────────────
blocks += [
    N.h2("Solution 1 — Iterative Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find a value in a sorted list in better than O(n) time. The key is to exploit the sorted property — each element tells us about all elements around it."),
        N.h4("What Doesn't Work"),
        N.para("A linear scan checks every element left-to-right: O(n) time. For n=1,000,000 that could be a million comparisons. The O(log n) requirement rules this out entirely."),
        N.h4("The Key Observation"),
        N.para("Because the array is sorted, when you look at nums[mid] and it is smaller than target, every element at indices ≤ mid is also smaller than target. You can eliminate half the array with one comparison."),
        N.h4("Building the Solution"),
        N.para("Maintain a search window [lo, hi]. The invariant: if target exists, it is always in [lo, hi]. Probe the midpoint: if match → done; if too small → lo = mid+1 (eliminate left half); if too large → hi = mid-1 (eliminate right half). Window strictly shrinks each iteration → terminates in O(log n) steps."),
        N.callout("Analogy: Opening a dictionary. You open to the middle. If your word comes alphabetically before that page, tear out the right half. Repeat with the remaining half. You find any word in ~17 openings in a 100,000-word dictionary.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def search(nums: list[int], target: int) -> int:\n"
        "    lo, hi = 0, len(nums) - 1\n"
        "    while lo <= hi:\n"
        "        mid = lo + (hi - lo) // 2\n"
        "        if nums[mid] == target:\n"
        "            return mid\n"
        "        elif nums[mid] < target:\n"
        "            lo = mid + 1\n"
        "        else:\n"
        "            hi = mid - 1\n"
        "    return -1"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 0, len(nums) - 1", {"code": True}), " — Initialize both boundaries inclusive. Invariant: if target exists, it is in nums[lo..hi] at all times."])),
    N.para(N.rich([("while lo <= hi:", {"code": True}), " — Loop while search space is non-empty. 'lo == hi' is still one candidate to check, so '≤' not '<'."])),
    N.para(N.rich([("mid = lo + (hi - lo) // 2", {"code": True}), " — Overflow-safe floor midpoint. Equivalent to (lo+hi)//2 in Python; safer in Java/C++."])),
    N.para(N.rich([("if nums[mid] == target:", {"code": True}), " — Exact match: we found it at index mid."])),
    N.para(N.rich([("elif nums[mid] < target:", {"code": True}), " — mid is too small. Sorted array guarantees everything at indices ≤ mid is also too small. Eliminate left half."])),
    N.para(N.rich([("lo = mid + 1", {"code": True}), " — Jump past mid (not to mid). This guarantees the window strictly shrinks and prevents infinite loops."])),
    N.para(N.rich([("hi = mid - 1", {"code": True}), " — Symmetric: mid is too large, eliminate right half. Jump below mid."])),
    N.para(N.rich([("return -1", {"code": True}), " — lo > hi: search space exhausted, target is not in the array."])),
    N.divider(),
]

# ── Solution 2: Linear Scan ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Linear Scan (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Check every element one by one until we find the target or exhaust the array."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n) time — too slow for the O(log n) requirement. But it is the correct starting point to mention before optimizing."),
        N.h4("The Key Observation"),
        N.para("No special structure needed — works on any array, sorted or not. Its simplicity makes it a useful baseline."),
        N.h4("Building the Solution"),
        N.para("Enumerate indices 0 to n-1. At each position check if nums[i] equals target. Return i on match; return -1 after the loop."),
        N.callout("Use this in an interview as your first proposal, then say 'we can do better with binary search since the array is sorted'.", "🧠", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def search_linear(nums: list[int], target: int) -> int:\n"
        "    for i, v in enumerate(nums):\n"
        "        if v == target:\n"
        "            return i\n"
        "    return -1"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for i, v in enumerate(nums):", {"code": True}), " — Visit each (index, value) pair in order."])),
    N.para(N.rich([("if v == target:", {"code": True}), " — Is this the element we want?"])),
    N.para(N.rich([("return -1", {"code": True}), " — Checked every element, not found."])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Linear Scan (Brute Force)", "O(n)", "O(1)"],
        ["Iterative Binary Search ✓", "O(log n)", "O(1)"],
        ["Recursive Binary Search", "O(log n)", "O(log n) — call stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Binary Search"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BS: Standard (Classic lo, hi, mid template)"])),
    N.callout(
        "When to recognize this pattern: sorted array + find element + O(log n) time requirement. "
        "Also: 'find first/last occurrence', 'binary search on answer space' (minimize/maximize X satisfying condition), "
        "'rotated sorted array', any monotone true/false predicate where you can eliminate half.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Search Insert Position", {"bold": True}), " (Easy) — BS returning lo when target absent; lo is the correct insertion index (#35)"])),
    N.bullet(N.rich([("First Bad Version", {"bold": True}), " (Easy) — BS for first true in boolean space; classic BS on answer (#278)"])),
    N.bullet(N.rich([("Find First and Last Position of Element in Sorted Array", {"bold": True}), " (Medium) — Two separate BS calls for leftmost and rightmost boundaries (#34)"])),
    N.bullet(N.rich([("Search in Rotated Sorted Array", {"bold": True}), " (Medium) — BS with sorted-half identification to handle the pivot (#33)"])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array", {"bold": True}), " (Medium) — BS on pivot location using sorted-half logic (#153)"])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), " (Medium) — BS on answer space; monotone feasibility check instead of element search (#875)"])),
    N.bullet(N.rich([("Search a 2D Matrix", {"bold": True}), " (Medium) — Treat 2D sorted grid as flattened 1D sorted array, apply BS (#74)"])),
    N.para("These problems all exploit sorted order (or a monotone property) to eliminate half the candidates per step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 (Binary Search) · Sub-pattern: BS: Standard", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("binary_search")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"URL: https://www.notion.so/{PAGE_ID.replace('-','')}")
