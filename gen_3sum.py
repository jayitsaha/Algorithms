"""gen_3sum.py — Regenerate the 3Sum Notion page in-place (rich, hand-authored)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8119-a199-d311dda420ce"

# ── 1. Properties ──────────────────────────────────────────────────────────
print("Setting properties…")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=15,
    pattern="Array Manipulation",
    subpatterns=["Sort + Fix One + Two Pointers", "Two Pointer: Opposite Direction"],
    tc="O(n²)",
    sc="O(1)",
    key_insight="Sort, fix one element as pivot, then two-pointer converge on the rest — skip duplicate pivots and pointers for uniqueness.",
    icon="🟡",
)
print("Properties OK")

# ── 2. Wipe old content ────────────────────────────────────────────────────
print("Wiping old page body…")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── 3. Build blocks ────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return all unique triplets ", {}),
        ("[nums[i], nums[j], nums[k]]", {"code": True}),
        (" such that ", {}),
        ("i", {"code": True}),
        (", ", {}),
        ("j", {"code": True}),
        (", ", {}),
        ("k", {"code": True}),
        (" are pairwise distinct and ", {}),
        ("nums[i] + nums[j] + nums[k] == 0", {"code": True}),
        (". The solution set must not contain duplicate triplets.", {}),
    ])),
    N.para("Example: nums = [-1, 0, 1, 2, -1, -4]  →  [[-1,-1,2], [-1,0,1]]"),
    N.divider(),
]

# ── Solution 1: Sort + Two Pointers (Interview Pick) ─────────────────────
blocks += [
    N.h2("Solution 1 — Sort + Fix One + Two Pointers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Find all unique groups of three numbers that cancel each other out (sum to zero). This is a search problem in 3D space (all triples of indices)."),
        N.h4("What Doesn't Work"),
        N.para("Three nested loops — O(n³) — is too slow for n up to 3000. Using a set for deduplication on top of O(n³) work is still O(n³) with worse constants. We need a smarter structure."),
        N.h4("The Key Observation"),
        N.para("If we sort the array, fixing one element reduces the problem: find two numbers in the sorted remainder that sum to -fixed. Two-pointer finds that pair in O(n) by exploiting the monotone property: moving L right strictly increases the partial sum; moving R left strictly decreases it."),
        N.h4("Building the Solution"),
        N.para("1) Sort. 2) Outer loop fixes nums[i] as first element. 3) Inner two-pointer from i+1 to n-1 finds complements. 4) Skip duplicate values at all three pointers to prevent duplicate triplets. 5) Early break when nums[i] > 0 (sorted → all sums are positive from here)."),
        N.callout("Analogy: Like searching a phonebook (sorted). You don't scan every page randomly — you open to a section, then scan left/right. Sorting is the organization that enables efficient convergence.", "🧠", "blue_background"),
    ]),
]

sol1_code = '''\
def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()                                     # Enable two-pointer + dup detection
    result = []
    for i in range(len(nums) - 2):                  # Fix first element
        if nums[i] > 0: break                       # All remaining sums are positive
        if i > 0 and nums[i] == nums[i-1]: continue # Skip duplicate fixed values
        L, R = i + 1, len(nums) - 1                # Two pointers on remainder
        while L < R:
            s = nums[i] + nums[L] + nums[R]
            if s == 0:
                result.append([nums[i], nums[L], nums[R]])
                while L < R and nums[L] == nums[L+1]: L += 1  # Skip L dups
                while L < R and nums[R] == nums[R-1]: R -= 1  # Skip R dups
                L += 1; R -= 1                      # Advance past found triplet
            elif s < 0: L += 1                      # Sum too small → bigger left
            else: R -= 1                            # Sum too big  → smaller right
    return result\
'''

blocks += [
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("nums.sort()", {"code": True}), (" — In-place sort in O(n log n). This is the prerequisite that makes two-pointer and duplicate skipping possible.", {})])),
    N.para(N.rich([("for i in range(len(nums) - 2)", {"code": True}), (" — Outer loop fixes the first triplet element. Stop at n-3 to leave room for L and R.", {})])),
    N.para(N.rich([("if nums[i] > 0: break", {"code": True}), (" — Early termination: sorted array means every subsequent element is also positive, so all sums are positive — no triplet possible.", {})])),
    N.para(N.rich([("if i > 0 and nums[i] == nums[i-1]: continue", {"code": True}), (" — Skip duplicate fixed values. Without this, [-1,-1,0,1] would yield [-1,0,1] twice.", {})])),
    N.para(N.rich([("L, R = i + 1, len(nums) - 1", {"code": True}), (" — Two pointers at opposite ends of the unsearched subarray.", {})])),
    N.para(N.rich([("s = nums[i] + nums[L] + nums[R]", {"code": True}), (" — Current triplet sum.", {})])),
    N.para(N.rich([("result.append([...])", {"code": True}), (" — Found a zero-sum triplet; record it.", {})])),
    N.para(N.rich([("while L < R and nums[L] == nums[L+1]: L += 1", {"code": True}), (" — Skip over any consecutive equal values at L before advancing.", {})])),
    N.para(N.rich([("while L < R and nums[R] == nums[R-1]: R -= 1", {"code": True}), (" — Same for R.", {})])),
    N.para(N.rich([("L += 1; R -= 1", {"code": True}), (" — Advance both pointers past the recorded triplet. Required after dup-skip loops.", {})])),
    N.para(N.rich([("elif s < 0: L += 1", {"code": True}), (" — Sum too small; moving L right gives a larger value.", {})])),
    N.para(N.rich([("else: R -= 1", {"code": True}), (" — Sum too large; moving R left gives a smaller value.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force (for context) ──────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force O(n³) (For Reference Only)"),
    N.toggle_h3("💡 Intuition: Why This Fails", [
        N.h4("Reframe the Problem"),
        N.para("Try all combinations of three indices and check if they sum to zero."),
        N.h4("What Doesn't Work"),
        N.para("Three nested loops generate O(n³) triples. For n=3000 (LeetCode constraint), this is 27 billion operations — Time Limit Exceeded. Use a set to deduplicate, but this adds overhead without helping the fundamental complexity issue."),
        N.h4("The Key Observation"),
        N.para("We only mention this to establish the baseline. Interviewers want you to move quickly to the O(n²) solution. Describe brute force in one sentence, then pivot."),
    ]),
]

sol2_code = '''\
def threeSum_brute(nums):               # TLE at n > 500 — describe verbally only
    n, seen = len(nums), set()
    for i in range(n):                  # Three nested loops → O(n³)
        for j in range(i+1, n):
            for k in range(j+1, n):
                if nums[i]+nums[j]+nums[k] == 0:
                    seen.add(tuple(sorted([nums[i],nums[j],nums[k]])))
    return [list(t) for t in seen]\
'''

blocks += [
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (3 loops)", "O(n³)", "O(n) for set"],
        ["Sort + Two Pointers", "O(n²)", "O(1) extra"],
        ["Hash Set per fixed i", "O(n²)", "O(n) per iteration"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Fix One + Two Pointers", {})])),
    N.callout(
        "When to recognize this pattern: problem asks for all unique k-tuples summing to a target; "
        "array can be sorted; need unique combinations without duplicates; "
        "\"no duplicates\" + \"sum to target\" + sortable input → this exact template.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Sort + Fix + Two Pointers):"),
    N.bullet(N.rich([("Two Sum II — Input Array Is Sorted", {"bold": True}), (" (Easy) — Pure two-pointer 2Sum; the inner loop of 3Sum (#167)", {})])),
    N.bullet(N.rich([("3Sum Closest", {"bold": True}), (" (Medium) — Identical structure; minimize |sum - target| instead of finding == (#16)", {})])),
    N.bullet(N.rich([("4Sum", {"bold": True}), (" (Medium) — Two outer fixed loops + two-pointer inner = O(n³) (#18)", {})])),
    N.bullet(N.rich([("3Sum Smaller", {"bold": True}), (" (Medium) — Count triplets < target; when s < target, add R-L to count (#259)", {})])),
    N.bullet(N.rich([("Valid Triangle Number", {"bold": True}), (" (Medium) — Fix largest side, two-pointer count valid pairs (#611)", {})])),
    N.bullet(N.rich([("Container With Most Water", {"bold": True}), (" (Medium) — Two-pointer convergence for a different optimization (#11)", {})])),
    N.para("These problems share the same insight: sorting enables monotone two-pointer search, reducing the search space by one dimension for each fixed element."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.2 (Two Pointers Pattern)", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("3sum")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks…")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
