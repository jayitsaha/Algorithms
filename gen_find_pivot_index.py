import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8160-94a5-d0bfcf57858d"

print("Step 1: Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=724,
    pattern="Prefix Sum",
    subpatterns=["Left Sum == Right Sum"],
    tc="O(n)",
    sc="O(1)",
    key_insight="At pivot i: prefix_sum(i) == total - prefix_sum(i) - nums[i]. One-pass with running left_sum.",
    icon="🟢"
)
print("  Properties set OK")

print("Step 2: Wiping existing blocks...")
n = N.wipe_page(PAGE_ID)
print(f"  Wiped {n} blocks")

print("Step 3: Building new body...")

# ── Problem ──
blocks = [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of integers ", {}),
        ("nums", {"code": True}),
        (", return the ", {}),
        ("leftmost pivot index", {"bold": True}),
        (" of this array. The pivot index is the index where the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the right of the index. If the index is on the left edge of the array, then the left sum is 0 (there are no elements to the left). The same applies to the right edge. Return ", {}),
        ("-1", {"code": True}),
        (" if no such index exists.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [1,7,3,6,5,6] → output 3", {"code": True}),
        (". At index 3: left_sum = 1+7+3 = 11, right_sum = 5+6 = 11. Equal!", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Optimal One-Pass Prefix Sum ──
sol1_code = '''\
def pivotIndex(nums: list[int]) -> int:
    total = sum(nums)         # O(n) scan: total sum of all elements
    left_sum = 0              # Running left sum (starts at 0 before index 0)
    for i, num in enumerate(nums):
        right_sum = total - left_sum - num  # Derive right sum in O(1)
        if left_sum == right_sum:           # Pivot condition
            return i
        left_sum += num       # Advance left_sum AFTER the check
    return -1                 # No pivot found
'''

blocks += [
    N.h2("Solution 1 — One-Pass Prefix Sum (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need index i where sum(nums[0..i-1]) == sum(nums[i+1..n-1]). Both sums exclude nums[i] itself. Left sum grows as we scan left-to-right; right sum is everything we haven't consumed yet."),
        N.h4("What Doesn't Work"),
        N.para("Brute force computes left_sum and right_sum from scratch for every index: O(n²) time. Two separate prefix-sum arrays work in O(n) but use O(n) extra space. We can do better."),
        N.h4("The Key Observation"),
        N.para("If we know the total sum and the running left_sum, we can derive right_sum instantly: right_sum = total - left_sum - nums[i]. No second array needed — one variable does the job in O(1) per step."),
        N.h4("Building the Solution"),
        N.para("1. Compute total = sum(nums) once. 2. Scan left to right, keeping left_sum = 0 initially. 3. At each index i: right_sum = total - left_sum - nums[i]. 4. If left_sum == right_sum, return i. 5. Otherwise left_sum += nums[i] and continue. 6. If loop ends, return -1."),
        N.callout("Analogy: a seesaw. 'total' is the total weight. At each seat i, left pan holds left_sum, the board holds nums[i], and right pan holds the rest. We find the seat where both pans balance.", "⚖️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("total = sum(nums)", {"code": True}), (" — One-pass O(n) to compute the total. This anchors our right-sum derivation for every index.", {})])),
    N.para(N.rich([("left_sum = 0", {"code": True}), (" — Before the first element there are no elements to the left, so left sum is 0. The invariant: at the start of iteration i, left_sum == sum(nums[0..i-1]).", {})])),
    N.para(N.rich([("right_sum = total - left_sum - num", {"code": True}), (" — Algebraic short-circuit: right_sum = total sum − left contributions − current element. O(1) per step instead of recomputing with another loop.", {})])),
    N.para(N.rich([("if left_sum == right_sum: return i", {"code": True}), (" — Pivot condition check. We return immediately on the leftmost match (the problem asks for leftmost).", {})])),
    N.para(N.rich([("left_sum += num", {"code": True}), (" — Advance left_sum AFTER the check. If we did it before, we'd be double-counting nums[i] on both left and right sides.", {})])),
    N.para(N.rich([("return -1", {"code": True}), (" — Exhausted all indices without finding a balanced point. No pivot exists.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
sol2_code = '''\
def pivotIndex(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        left_sum  = sum(nums[:i])    # Sum of everything left of i
        right_sum = sum(nums[i+1:])  # Sum of everything right of i
        if left_sum == right_sum:
            return i
    return -1
'''

blocks += [
    N.h2("Solution 2 — Brute Force (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct reading of the problem: for each index, compute left and right sums explicitly with slices, then compare."),
        N.h4("What Doesn't Work Well"),
        N.para("Each sum() call on a slice is O(n). With n indices, total is O(n²). Fails on large inputs (10^4 elements → 10^8 operations)."),
        N.h4("The Key Observation"),
        N.para("Use this to establish the problem; then immediately ask 'can I avoid recomputing from scratch each time?' That question leads to the prefix sum insight."),
        N.h4("Building the Solution"),
        N.para("For each i from 0 to n-1: compute left=sum(nums[:i]), right=sum(nums[i+1:]). If equal, return i. If no match, return -1."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — Try each index as the potential pivot.", {})])),
    N.para(N.rich([("left_sum = sum(nums[:i])", {"code": True}), (" — Slice and sum everything to the left. O(i) work. For i=0 this is sum([]) = 0.", {})])),
    N.para(N.rich([("right_sum = sum(nums[i+1:])", {"code": True}), (" — Slice and sum everything to the right. O(n-i) work.", {})])),
    N.para(N.rich([("if left_sum == right_sum: return i", {"code": True}), (" — First (leftmost) match wins.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["One-Pass Prefix Sum ✓", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Prefix Sum", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Left Sum == Right Sum — running left_sum + algebraic right_sum derivation", {})])),
    N.callout(
        "When to recognize this pattern: 'find index where left portion equals right portion', 'balance point', 'prefix sum of one side vs. the other', or any problem where we need cumulative sums on both sides of an index.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Prefix Sum / Balance Point):"),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), (" (Medium) — Prefix sum + hash map to count subarrays with target sum (#560)", {})])),
    N.bullet(N.rich([("Range Sum Query – Immutable", {"bold": True}), (" (Easy) — Build prefix array once, answer queries in O(1) (#303)", {})])),
    N.bullet(N.rich([("Product of Array Except Self", {"bold": True}), (" (Medium) — Left-pass and right-pass products (no division) (#238)", {})])),
    N.bullet(N.rich([("Subarray Sums Divisible by K", {"bold": True}), (" (Medium) — Prefix sums modulo K + hash map (#974)", {})])),
    N.bullet(N.rich([("Running Sum of 1D Array", {"bold": True}), (" (Easy) — Build running prefix directly into output (#1480)", {})])),
    N.bullet(N.rich([("Maximum Size Subarray Sum Equals K", {"bold": True}), (" (Medium) — Prefix sum + earliest index hash map (#325)", {})])),
    N.para("These problems share the same core technique: maintain a running prefix sum and derive complementary information in O(1) instead of recomputing."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.3 (Prefix Sum Pattern)\nSub-Pattern: Left Sum == Right Sum · Source: Guide Section 1.3", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_pivot_index")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"  Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
