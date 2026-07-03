"""
gen_count_of_range_sum.py — Notion IN-PLACE update for Count of Range Sum (#327).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ca-9358-db0ad3b55adc"

# ── 1) Set properties ───────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=327,
    pattern="Sorting",
    subpatterns=["Merge Sort + Range Count"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Build prefix sums; count pairs with difference in [lower,upper] via modified merge sort with two-pointer window during merge.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and two integers ", {}),
        ("lower", {"code": True}),
        (" and ", {}),
        ("upper", {"code": True}),
        (", return the number of range sums ", {}),
        ("sum(i, j)", {"code": True}),
        (" that lie in ", {}),
        ("[lower, upper]", {"code": True}),
        (" inclusive. A range sum ", {}),
        ("sum(i, j)", {"code": True}),
        (" is defined as the sum of elements in ", {}),
        ("nums", {"code": True}),
        (" from index ", {}),
        ("i", {"code": True}),
        (" to ", {}),
        ("j", {"code": True}),
        (" inclusive.", {}),
    ])),
    N.para("Example: nums = [-2, 5, -1], lower = -2, upper = 2 → Answer: 3. The valid range sums are: sum(0,0)=-2, sum(0,2)=2, sum(2,2)=-1."),
    N.callout(
        "Constraints: 1 ≤ n ≤ 10⁵, -2³¹ ≤ nums[i] ≤ 2³¹-1. Use long/int64 in Java/C++ to avoid overflow; Python handles big integers natively.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 1: Merge Sort ──
blocks += [
    N.h2("Solution 1 — Merge Sort on Prefix Sums (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define prefix sums: pre[k] = nums[0]+…+nums[k-1] with pre[0]=0. Then sum(i,j) = pre[j+1] - pre[i]. The question becomes: how many pairs (i < j+1) in the prefix-sum array have pre[j] - pre[i] ∈ [lower, upper]? This is a pair-counting problem on an n+1 element array."),
        N.h4("What Doesn't Work"),
        N.para("Brute force checks all O(n²) pairs. For n=10⁵ that is 10¹⁰ operations — far too slow. We need to count valid partners for each prefix-sum element in sub-linear time per element."),
        N.h4("The Key Observation"),
        N.para("If the left portion of the prefix-sum array is SORTED, then for any right-half element val, the valid left-half elements form a contiguous window [val-upper, val-lower]. Two monotone pointers can track this window as val increases, advancing only forward — O(n) total per merge level."),
        N.h4("Building the Solution"),
        N.para("Merge sort naturally gives us a sorted left half and a sorted right half at each level. We count cross-pairs (i in left, j in right) during the merge step, then perform the standard merge. Recursion handles pairs entirely within each half. O(n) per level × O(log n) levels = O(n log n)."),
        N.callout("Analogy: Imagine two sorted lines of people. For each person in Line B, you slide a window along Line A to count how many satisfy the condition — no one in Line A is ever re-visited as you move along Line B.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Count During Merge"),
    N.para("Origin: Merge sort (von Neumann, 1945). Counting cross-pair statistics during merge is a classic divide-and-conquer extension, popularized in Kleinberg & Tardos 'Algorithm Design' Ch. 5 (Count Inversions). The recurrence T(n)=2T(n/2)+O(n) solves to O(n log n) by Master Theorem Case 2."),
    N.para("Core invariant: After merge_sort(lo..hi) returns, the subarray is sorted AND all valid pairs with BOTH endpoints within [lo..hi] have been counted. The merge step counts exactly the 'cross-pairs' (i in left half, j in right half), which are missed by both recursive sub-calls."),
    N.para("Generalization: Any 'count pairs (i<j) with f(arr[i], arr[j]) satisfying a condition expressible as a window' problem can use this pattern: Count Inversions (#arr[i]>arr[j]), Reverse Pairs (#493: arr[i]>2*arr[j]), Count Smaller After Self (#315)."),
    N.h3("Code"),
    N.code("""def countRangeSum(nums, lower, upper):
    n = len(nums)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i+1] = pre[i] + nums[i]

    count = [0]

    def merge_sort(arr):
        if len(arr) <= 1:
            return
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        merge_sort(left)
        merge_sort(right)

        # COUNT cross-pairs BEFORE standard merge
        lo_ptr = hi_ptr = 0
        for val in right:
            # Advance lo_ptr past elements too small: val - left[i] > upper
            while lo_ptr < len(left) and left[lo_ptr] < val - upper:
                lo_ptr += 1
            # Advance hi_ptr past elements still in range: val - left[i] >= lower
            while hi_ptr < len(left) and left[hi_ptr] <= val - lower:
                hi_ptr += 1
            count[0] += hi_ptr - lo_ptr  # [lo_ptr, hi_ptr) all valid

        # Standard merge
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]; i += 1
            else:
                arr[k] = right[j]; j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]; i += 1; k += 1
        while j < len(right):
            arr[k] = right[j]; j += 1; k += 1

    merge_sort(pre)
    return count[0]"""),
    N.h3("Line by Line"),
    N.para(N.rich([("pre = [0]*(n+1)", {"code": True}), (" — Prefix sum array of length n+1. pre[0]=0 sentinel; pre[k]=sum of nums[0..k-1].", {})])),
    N.para(N.rich([("merge_sort(arr)", {"code": True}), (" — Recursive function that both sorts arr in place and accumulates count. Takes a subarray (copy) and writes back.", {})])),
    N.para(N.rich([("lo_ptr = hi_ptr = 0", {"code": True}), (" — Two monotone pointers into the sorted left half. Only advance, never retreat. Total movement per call: O(len(left)).", {})])),
    N.para(N.rich([("while left[lo_ptr] < val - upper: lo_ptr += 1", {"code": True}), (" — Skip left elements where val - left[i] > upper (sum too large). left[lo_ptr] is the first element in the window.", {})])),
    N.para(N.rich([("while left[hi_ptr] <= val - lower: hi_ptr += 1", {"code": True}), (" — Advance past elements where val - left[i] >= lower (still valid). hi_ptr points one past the last valid element.", {})])),
    N.para(N.rich([("count[0] += hi_ptr - lo_ptr", {"code": True}), (" — All elements in [lo_ptr, hi_ptr) give a valid range sum with val. This is the number of valid pairs for this particular right-half element.", {})])),
    N.para(N.rich([("Standard merge block", {"bold": True}), (" — After counting, merge left and right into arr. This sorting enables efficient window queries in ancestor merge calls.", {})])),
    N.callout(
        "Warning: Count BEFORE merge. Once merged, you cannot distinguish which elements came from left vs right half. The window counting relies on the separation.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force (O(n²), for understanding)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Directly enumerate all O(n²) subarrays, compute each sum, and check if it's in [lower, upper]."),
        N.h4("What Doesn't Work"),
        N.para("This works correctly but is O(n²) time. For n=10⁵ that's 10¹⁰ operations — times out. Use only to verify the optimal solution on small inputs."),
        N.h4("The Key Observation"),
        N.para("To avoid recomputing sum(i,j) from scratch each time, extend it incrementally: sum(i,j+1) = sum(i,j) + nums[j+1]. Inner loop is O(n) per starting index."),
    ]),
    N.h3("Code"),
    N.code("""def countRangeSum(nums, lower, upper):
    count = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]  # extend sum incrementally
            if lower <= s <= upper:
                count += 1
    return count"""),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(nums)):", {"code": True}), (" — Starting index of range. O(n) choices.", {})])),
    N.para(N.rich([("s += nums[j]", {"code": True}), (" — Extend sum incrementally rather than recomputing from scratch. Inner loop is still O(n).", {})])),
    N.para(N.rich([("if lower <= s <= upper:", {"code": True}), (" — Direct range check. Simple but called O(n²) times.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Merge Sort (optimal)", "O(n log n)", "O(n)"],
        ["SortedList + bisect", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sorting", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Merge Sort + Range Count", {})])),
    N.callout(
        "When to recognize this pattern: Problem asks to count pairs (i < j) satisfying a comparison between array elements. The condition can be expressed as 'is arr[i] in some window defined by arr[j]?' Sorting one side enables a monotone two-pointer window query. Keywords: 'count pairs', 'range sums', 'inversions', 'reverse pairs', 'smaller after self'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 'count during merge sort' technique:"),
    N.bullet(N.rich([("Count Inversions", {"bold": True}), (" — Classic version. Condition: arr[i] > arr[j] for i < j. Simpler condition, same merge structure.", {})])),
    N.bullet(N.rich([("Count Smaller Numbers After Self", {"bold": True}), (" (#315, Hard) — Per-element merge-sort counting. Same pattern, per-element accumulation.", {})])),
    N.bullet(N.rich([("Reverse Pairs", {"bold": True}), (" (#493, Hard) — Count pairs where nums[i] > 2*nums[j], i < j. Nearly identical code, different window condition.", {})])),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), (" (#560, Medium) — Prefix sums + hash map. Exact sum match (not a range); hash is sufficient.", {})])),
    N.bullet(N.rich([("Subarray Sums Divisible by K", {"bold": True}), (" (#974, Medium) — Prefix sum mod k + frequency array. No sorting needed.", {})])),
    N.bullet(N.rich([("Sort an Array", {"bold": True}), (" (Medium) — Understand pure merge sort before the modified version.", {})])),
    N.para("These problems share the same core technique: divide-and-conquer pair counting using the monotone window property on sorted sub-arrays."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Sorting section: Merge Sort + Range Count sub-pattern.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("count_of_range_sum")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
