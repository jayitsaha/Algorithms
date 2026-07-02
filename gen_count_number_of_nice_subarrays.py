"""
gen_count_number_of_nice_subarrays.py
Rebuild the Notion page for Count Number of Nice Subarrays (#1248) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81b6-b126-ecf9f28ac702"
SLUG    = "count_number_of_nice_subarrays"

# ─── 1) Properties ───────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1248,
    pattern="Sliding Window",
    subpatterns=["AtMost(K) - AtMost(K-1)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="exactly(k) = atMost(k) - atMost(k-1); each atMost uses a variable sliding window.",
    icon="🟡",
)

# ─── 2) Wipe old content ─────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Deleted {wiped} blocks.")

# ─── 3) Build new body ───────────────────────────────────────────────────────
print("Building blocks...")

PROBLEM_STMT = (
    "Given an integer array nums and an integer k, return the number of nice subarrays — "
    "contiguous subarrays that contain exactly k odd numbers. "
    "A number is odd if num % 2 == 1."
)

SOL1_CODE = """\
def numberOfSubarrays(nums, k):
    def atMost(goal):
        if goal < 0: return 0          # guard: atMost(-1) = 0
        res = left = odds = 0
        for right, num in enumerate(nums):
            odds += num % 2            # 1 if odd, 0 if even
            while odds > goal:         # window invalid
                odds -= nums[left] % 2
                left += 1
            res += right - left + 1    # all sub-windows ending at right
        return res
    return atMost(k) - atMost(k - 1)  # exactly k = difference
"""

SOL2_CODE = """\
def numberOfSubarrays(nums, k):
    count = {0: 1}          # prefix sum 0 seen once (empty prefix)
    prefix = res = 0
    for num in nums:
        prefix += num % 2   # running count of odds from index 0
        res += count.get(prefix - k, 0)   # starts giving exactly k odds
        count[prefix] = count.get(prefix, 0) + 1
    return res
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — AtMost Sliding Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to count contiguous subarrays where exactly k elements are odd. "
            "The naive approach checks all O(n²) subarrays. We want O(n)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Standard sliding window expands right and shrinks left when a condition is violated. "
            "For 'exactly k odds' there is no single monotone shrink condition — a window is invalid "
            "both when it has too many odds AND when it has too few. A single window cannot encode both."
        ),
        N.h4("The Key Observation"),
        N.para(
            "'At most k odds' IS monotone: adding more elements to a window can only increase or maintain "
            "the odd count, never decrease it. So atMost(k) has a clean shrink condition. "
            "And by set subtraction: exactly(k) = atMost(k) - atMost(k-1)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Implement a helper atMost(goal) using two pointers. right expands one step at a time. "
            "When odds > goal, advance left. At each right, all sub-windows [left..right] are valid, "
            "counting as right-left+1. Run the helper twice and subtract."
        ),
        N.callout(
            "Analogy: 'At most k' is like a budget. You can always cut costs (shrink left). "
            "'Exactly k' is like hitting a target — you'd need to cut AND grow simultaneously, "
            "which a single pointer can't do. So compute 'at most k' and 'at most k-1', then subtract.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def atMost(goal):", {"code": True}), " — Helper function. Returns count of subarrays with at most goal odd numbers."])),
    N.para(N.rich([("if goal < 0: return 0", {"code": True}), " — Guard for the k=0 case: atMost(-1) must be 0, not undefined."])),
    N.para(N.rich([("res = left = odds = 0", {"code": True}), " — Initialize result accumulator, left pointer, and odd count in window."])),
    N.para(N.rich([("for right, num in enumerate(nums):", {"code": True}), " — right pointer scans every element once from left to right."])),
    N.para(N.rich([("odds += num % 2", {"code": True}), " — Adds 1 for odd numbers, 0 for even. Clean trick with no if-statement."])),
    N.para(N.rich([("while odds > goal:", {"code": True}), " — Window has too many odds — shrink from the left until valid."])),
    N.para(N.rich([("odds -= nums[left] % 2", {"code": True}), " — Remove the leftmost element's contribution to the odd count."])),
    N.para(N.rich([("left += 1", {"code": True}), " — Advance left pointer, shrinking the window."])),
    N.para(N.rich([("res += right - left + 1", {"code": True}), " — Every starting index from left to right gives a valid subarray ending at right. Count them all at once."])),
    N.para(N.rich([("return atMost(k) - atMost(k - 1)", {"code": True}), " — Set subtraction: cancels subarrays with 0..k-1 odds, leaving exactly k."])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — Prefix Sum (Alternative O(n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Think of each number's 'odd parity' (1 if odd, 0 if even) as a value to sum. "
            "Then 'subarray with exactly k odds' becomes 'subarray with parity-sum = k'. "
            "This is identical to Subarray Sum Equals K (#560)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Define prefix[i] = number of odd elements in nums[0..i]. "
            "A subarray nums[j+1..i] has exactly k odds iff prefix[i] - prefix[j] = k, "
            "i.e., prefix[j] = prefix[i] - k. "
            "Count how many prior prefixes equal prefix[i] - k using a hash map."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Maintain a running prefix (odd count from index 0). At each position, "
            "look up count[prefix - k] — the number of starting points that give exactly k odds. "
            "Record the current prefix in the hash map for future lookups."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("count = {0: 1}", {"code": True}), " — The empty prefix has parity-sum 0. Initialize with one occurrence."])),
    N.para(N.rich([("prefix += num % 2", {"code": True}), " — Running count of odd numbers seen from the start."])),
    N.para(N.rich([("res += count.get(prefix - k, 0)", {"code": True}), " — Each past prefix equal to prefix-k gives a subarray with exactly k odds ending here."])),
    N.para(N.rich([("count[prefix] = ...", {"code": True}), " — Record this prefix sum so future positions can use it."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Prefix Sum", "O(n)", "O(n)"],
        ["AtMost Sliding Window (Interview Pick)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window (Dynamic Size)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "AtMost(K) - AtMost(K-1)"])),
    N.callout(
        "When to recognize this pattern: "
        "'Count subarrays/substrings with EXACTLY k [property]' where [property] is monotone "
        "(adding more elements can only increase it). "
        "The 'at most' helper has a clean shrink condition; subtract two calls to get the exact count.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same AtMost(K) - AtMost(K-1) technique:"),
    N.bullet(N.rich([("Subarrays with K Different Integers", {"bold": True}), " (Hard) — Identical template; counts subarrays with exactly k distinct values (#992)"])),
    N.bullet(N.rich([("Binary Subarrays With Sum", {"bold": True}), " (Medium) — atMost on binary array; exact = atMost(S) - atMost(S-1) (#930)"])),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), " (Medium) — Prefix sum sibling of this problem for value sums instead of odd count (#560)"])),
    N.bullet(N.rich([("Number of Substrings Containing All Three Characters", {"bold": True}), " (Medium) — Sliding window on character counts (#1358)"])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), " (Medium) — atMost(2 distinct) applied directly as a longest-window problem (#904)"])),
    N.bullet(N.rich([("Longest Subarray of 1's After Deleting One Element", {"bold": True}), " (Medium) — atMost(1 zero) variable window (#1493)"])),
    N.para("These problems share the same core technique: decompose exact-k into atMost(k) minus atMost(k-1)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.5 (Sliding Window — Dynamic Size)", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
