"""
Notion updater for LeetCode #374 — Guess Number Higher or Lower
Pattern: Binary Search / Classic Binary Search
"""
import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81a6-bcd1-eb945708546f"

# ─── 1. Set properties ───────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=374,
    pattern="Binary Search",
    subpatterns=["Classic Binary Search"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Always guess the midpoint of [lo, hi]; each call to guess() halves the search space.",
    icon="🟢"
)
print("Properties set OK")

# ─── 2. Wipe old body ────────────────────────────────────────────────────────
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks")

# ─── 3. Build new body ───────────────────────────────────────────────────────
blocks = []

# ── Problem Statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are playing the Guess Game. I pick a number from ", {}),
        ("1", {"code": True}),
        (" to ", {}),
        ("n", {"code": True}),
        (". You guess a number. I will tell you whether the number I picked is higher or lower than your guess.\n\n", {}),
        ("You call a pre-defined API ", {}),
        ("guess(num)", {"code": True}),
        (" which returns one of three possible results:\n", {}),
        ("  -1", {"code": True}),
        (": My number is lower than your guess (i.e., your guess is higher).\n", {}),
        ("   1", {"code": True}),
        (": My number is higher than your guess (i.e., your guess is lower).\n", {}),
        ("   0", {"code": True}),
        (": Your guess is equal to my number (correct!).\n\n", {}),
        ("Return the number that I picked.\n\nExample: n=10, pick=6 → return 6", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Binary Search (Interview Pick) ──
sol1_code = """\
# The API pre-defined in the problem:
# def guess(num: int) -> int:
#     if pick < num: return -1   # guess too high
#     elif pick > num: return 1  # guess too low
#     else: return 0             # correct

class Solution:
    def guessNumber(self, n: int) -> int:
        lo, hi = 1, n
        while lo <= hi:
            mid = lo + (hi - lo) // 2   # overflow-safe midpoint
            result = guess(mid)
            if result == 0:
                return mid               # found it
            elif result == -1:
                hi = mid - 1             # guess was too high; search lower half
            else:
                lo = mid + 1             # guess was too low; search upper half
"""

intuition_children_1 = [
    N.h4("Reframe the Problem"),
    N.para("We have an implicit sorted sequence 1, 2, 3, …, n and an oracle (guess()) that tells us whether our probe is too high, too low, or exact. We want to find the target value with the fewest probes. This is exactly the binary search problem — just without an explicit array."),
    N.h4("What Doesn't Work"),
    N.para("Linear scan (try 1, 2, 3, …) takes O(n) calls — up to a billion calls for n=10⁹. We need something logarithmic. Any approach that doesn't use the directional feedback to eliminate half the range at each step wastes information."),
    N.h4("The Key Observation"),
    N.para("Every call to guess() is a 3-way comparison that partitions the remaining candidates into three groups: too low, exact, too high. If we always probe the midpoint of our current [lo, hi] window, we eliminate the larger half plus one (the midpoint) in each step. This gives us O(log n) total probes."),
    N.h4("Building the Solution"),
    N.para("Initialize lo=1, hi=n. Each iteration: compute mid = lo + (hi-lo)//2. Call guess(mid). If 0 → return mid. If -1 (too high) → hi = mid-1. If 1 (too low) → lo = mid+1. The range [lo, hi] always contains the pick (our invariant) and strictly shrinks each iteration, guaranteeing termination."),
    N.callout(
        "Analogy: Imagine a number line printed on paper. You fold the paper in half repeatedly. Each fold eliminates exactly half the remaining numbers. After log₂(n) folds, you're left with exactly one number — the answer. Binary search is this folding operation.",
        "🧠", "blue_background"
    ),
]

blocks += [
    N.h2("Solution 1 — Classic Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition_children_1),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 1, n", {"code": True}), " — Initialize search boundaries: lo is the smallest possible pick (1), hi is the largest (n). The pick is guaranteed to be in [1, n]."])),
    N.para(N.rich([("while lo <= hi:", {"code": True}), " — Continue while the search space is non-empty. Since a valid pick always exists, we always return before lo > hi."])),
    N.para(N.rich([("mid = lo + (hi - lo) // 2", {"code": True}), " — Compute midpoint safely. Mathematically equivalent to (lo+hi)//2 but avoids 32-bit integer overflow when lo+hi > INT_MAX (critical in Java/C++)."])),
    N.para(N.rich([("result = guess(mid)", {"code": True}), " — Call the oracle API. This is the 'comparison' in binary search — tells us which half contains the answer."])),
    N.para(N.rich([("if result == 0: return mid", {"code": True}), " — Exact match. mid is the pick. Return immediately."])),
    N.para(N.rich([("elif result == -1: hi = mid - 1", {"code": True}), " — Our guess was too high. The pick is below mid. Eliminate mid and everything above it by setting hi = mid-1."])),
    N.para(N.rich([("else: lo = mid + 1", {"code": True}), " — result==1: our guess was too low. The pick is above mid. Eliminate mid and everything below it by setting lo = mid+1."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
sol2_code = """\
class Solution:
    def guessNumber_brute(self, n: int) -> int:
        for num in range(1, n + 1):
            if guess(num) == 0:
                return num
        # Never reached (problem guarantees valid pick)
"""

intuition_children_2 = [
    N.h4("Reframe the Problem"),
    N.para("Check every candidate from 1 to n until we find the pick. Simple and correct, but ignores the directional information from guess()."),
    N.h4("What Doesn't Work"),
    N.para("For n = 10⁹, this makes up to a billion API calls. Completely infeasible in practice."),
    N.h4("The Key Observation"),
    N.para("This approach treats guess() as a yes/no oracle (is this the answer?) rather than a directional oracle (which way to go?). It wastes the -1 vs 1 information entirely."),
    N.h4("Building the Solution"),
    N.para("Simply iterate: for num in range(1, n+1), check guess(num) == 0. This is O(n) in the worst case and only useful for understanding the problem structure — never for actual use."),
]

blocks += [
    N.h2("Solution 2 — Brute Force Linear Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition_children_2),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for num in range(1, n + 1):", {"code": True}), " — Try every number from 1 to n in ascending order."])),
    N.para(N.rich([("if guess(num) == 0: return num", {"code": True}), " — If this is the pick, return it. In the worst case (pick=n), we make n calls."])),
    N.callout(
        "⚠️ Never propose brute force as your final answer. It is only useful to establish a baseline before optimizing to binary search.",
        "⚠️", "red_background"
    ),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n)", "O(1)", "Up to n=10⁹ calls — unusable"],
        ["Binary Search ✓", "O(log n)", "O(1)", "≤30 calls for n=10⁹; optimal"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Binary Search — searching for a value in an ordered (implicit or explicit) space by halving the candidate range at each step."])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Classic Binary Search — the standard lo/hi/mid template applied to an integer range with a comparison oracle. Directly equivalent to searching a sorted array for an exact target."])),
    N.callout(
        "When to recognize this pattern: (1) The answer lives in a bounded, ordered range. (2) You have a comparison function (oracle) that tells you which direction to search. (3) You want O(log n) over O(n). Key phrase: 'find the hidden value' or 'search in [1, n]'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sub-pattern (Classic Binary Search):"),
    N.bullet(N.rich([("Binary Search", {"bold": True}), " (Easy) — Find target in a sorted array; the explicit-array version of this exact lo/hi/mid template (#704)"])),
    N.bullet(N.rich([("First Bad Version", {"bold": True}), " (Easy) — isBadVersion() oracle replaces guess(); binary search the first True in a monotone predicate; nearly identical code (#278)"])),
    N.bullet(N.rich([("Search Insert Position", {"bold": True}), " (Easy) — Lower-bound binary search: where would target be inserted if not found? (#35)"])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), " (Medium) — Binary search on the answer (eating speed), not an index; canFinish(speed) is the oracle (#875)"])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), " (Medium) — Binary search for minimum feasible capacity; canShip(capacity) is the oracle (#1011)"])),
    N.bullet(N.rich([("Find Peak Element", {"bold": True}), " (Medium) — Binary search where comparison is nums[mid] vs nums[mid+1]; no explicit target needed (#162)"])),
    N.bullet(N.rich([("Search in Rotated Sorted Array", {"bold": True}), " (Medium) — Binary search with extra invariant bookkeeping to identify the sorted half (#33)"])),
    N.para("These problems all share the same core technique: maintain [lo, hi] and halve the search space each iteration using a comparison oracle."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 (Binary Search → Classic Binary Search)", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("guess_number_higher_or_lower")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4. Append all blocks ────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
