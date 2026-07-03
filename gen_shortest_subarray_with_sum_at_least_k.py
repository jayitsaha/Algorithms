"""
gen_shortest_subarray_with_sum_at_least_k.py
Rebuild the Notion page for LC #862 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-812a-8113-d0b2013994b3"
SLUG    = "shortest_subarray_with_sum_at_least_k"

# ── 1. Set properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Hard",
    number      = 862,
    pattern     = "Stack & Queue",
    subpatterns = ["Prefix Sum + Monotonic Deque"],
    tc          = "O(n)",
    sc          = "O(n)",
    key_insight = "Prefix sums turn subarray sum into pair search; monotone deque finds shortest pair in O(n)",
    icon        = "🔴",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array "), ("nums", {"code": True}),
        (" and an integer "), ("k", {"code": True}),
        (", return the length of the shortest non-empty subarray of "),
        ("nums", {"code": True}), (" with a sum of at least "), ("k", {"code": True}),
        (". Return "), ("-1", {"code": True}), (" if there is no such subarray."),
    ])),
    N.para(N.rich([
        ("Constraints: "), ("1 ≤ nums.length ≤ 10⁵", {"code": True}),
        (", "), ("-10⁵ ≤ nums[i] ≤ 10⁵", {"code": True}),
        (", "), ("1 ≤ k ≤ 10⁹", {"code": True}),
        (". The array can contain negative numbers — this is the key difficulty."),
    ])),
    N.divider(),
]

# ── Solution 1: Optimal ──
sol1_intuition = [
    N.h4("Reframe the Problem"),
    N.para("We need the shortest contiguous subarray with sum ≥ k. Instead of directly thinking about subarrays, transform: define prefix[j] = nums[0]+...+nums[j-1] (with prefix[0]=0). Then sum of nums[i..j-1] = prefix[j] − prefix[i]. The problem becomes: find the minimum j−i with i < j and prefix[j] − prefix[i] ≥ k."),
    N.h4("What Doesn't Work"),
    N.para("Sliding window (two pointers) works perfectly when all numbers are positive: expand right until sum ≥ k, then shrink left. With negatives, extending the window can DECREASE the sum and shrinking can INCREASE it — the monotone invariant breaks. We cannot use two pointers."),
    N.h4("The Key Observation"),
    N.para("In the prefix array, we need: for each right boundary j, find the largest index i < j such that prefix[i] ≤ prefix[j] − k (which gives the shortest subarray). A monotone increasing deque of prefix indices gives us this in O(1) amortised — the front always holds the smallest prefix value seen so far."),
    N.h4("Building the Solution"),
    N.para("For each j: (1) Pop from front while prefix[j] − prefix[front] ≥ k — valid pair found, record length j−front, pop since future j' > j gives longer subarray from same front. (2) Pop from back while prefix[j] ≤ prefix[back] — back is dominated by j (smaller prefix AND later index), so back can never yield a shorter answer than j. (3) Push j. Each index is pushed and popped at most once → O(n) total."),
    N.callout("Analogy: Think of the deque as a queue of job applications. When a better candidate (smaller prefix value, later index) arrives, it makes older worse candidates irrelevant — discard them from the back. When the front candidate finally gets a match (valid pair found), it gets hired and leaves — discard from front.", "🧠", "blue_background"),
]

blocks += [
    N.h2("Solution 1 — Prefix Sum + Monotonic Deque (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol1_intuition),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "\n"
        "def shortestSubarray(nums: list[int], k: int) -> int:\n"
        "    n = len(nums)\n"
        "    # Build prefix sum array of length n+1\n"
        "    prefix = [0] * (n + 1)\n"
        "    for i in range(n):\n"
        "        prefix[i + 1] = prefix[i] + nums[i]\n"
        "\n"
        "    dq = deque()          # monotone increasing deque of indices\n"
        "    ans = float('inf')    # track shortest valid length\n"
        "\n"
        "    for j in range(n + 1):   # j = right boundary in prefix\n"
        "        # Step 1: check front for valid pairs\n"
        "        while dq and prefix[j] - prefix[dq[0]] >= k:\n"
        "            ans = min(ans, j - dq.popleft())\n"
        "        # Step 2: prune dominated back entries\n"
        "        while dq and prefix[j] <= prefix[dq[-1]]:\n"
        "            dq.pop()\n"
        "        # Step 3: push current index\n"
        "        dq.append(j)\n"
        "\n"
        "    return ans if ans != float('inf') else -1",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("prefix = [0] * (n + 1)", {"code": True}), " — allocate n+1 prefix sums; prefix[0] = 0 represents the empty prefix before any element."])),
    N.para(N.rich([("prefix[i+1] = prefix[i] + nums[i]", {"code": True}), " — running total: prefix[j] = nums[0] + ... + nums[j-1]. Sum of nums[i..j-1] = prefix[j] − prefix[i]."])),
    N.para(N.rich([("dq = deque()", {"code": True}), " — the monotone increasing deque. Stores indices into prefix. Front = smallest prefix value. Maintains: if i, j both in deque with i before j, then prefix[i] < prefix[j]."])),
    N.para(N.rich([("for j in range(n + 1):", {"code": True}), " — j iterates all n+1 positions in the prefix array (0 through n). At j, prefix[j] is the total sum of nums[0..j-1]."])),
    N.para(N.rich([("while dq and prefix[j] - prefix[dq[0]] >= k:", {"code": True}), " — front-pop: the pair (dq[0], j) gives a valid subarray. Record length j − dq[0] and pop the front. Popping is safe: any later j' > j would give length j' − dq[0] > j − dq[0] — strictly worse."])),
    N.para(N.rich([("ans = min(ans, j - dq.popleft())", {"code": True}), " — update best answer with this valid length. popleft() removes the front in O(1)."])),
    N.para(N.rich([("while dq and prefix[j] <= prefix[dq[-1]]:", {"code": True}), " — back-pop: current index j dominates the back. If prefix[j] ≤ prefix[back], then j is both a later index AND has a smaller or equal prefix value. For any future right boundary r: the pair (j, r) is shorter than (back, r) and still satisfies ≥ k if (back, r) did. Back is useless."])),
    N.para(N.rich([("dq.pop()", {"code": True}), " — remove the dominated back index in O(1). Repeat until deque is empty or back strictly dominates j."])),
    N.para(N.rich([("dq.append(j)", {"code": True}), " — push j as a new candidate left boundary. The deque remains monotone increasing."])),
    N.para(N.rich([("return ans if ans != float('inf') else -1", {"code": True}), " — if ans was never updated, no valid subarray exists. Return -1."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
sol2_intuition = [
    N.h4("Reframe the Problem"),
    N.para("Same problem — enumerate all subarrays and find the shortest with sum ≥ k."),
    N.h4("What Doesn't Work"),
    N.para("This approach is O(n²) — correct but times out for n > ~10,000. For each starting index i we extend to every ending index j, accumulating the running sum."),
    N.h4("The Key Observation"),
    N.para("For a fixed starting index i, the first j ≥ i where the running sum exceeds k gives the shortest subarray starting at i. Once we find that j, we break — no need to extend further."),
    N.h4("Building the Solution"),
    N.para("Double loop: outer loop over start index i, inner loop extends right accumulating sum, break as soon as sum ≥ k. Track global minimum length. O(n²) time, O(1) space."),
]

blocks += [
    N.h2("Solution 2 — Brute Force Nested Loops"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol2_intuition),
    N.h3("Code"),
    N.code(
        "def shortestSubarray_brute(nums: list[int], k: int) -> int:\n"
        "    n, ans = len(nums), float('inf')\n"
        "    for i in range(n):\n"
        "        curr = 0\n"
        "        for j in range(i, n):\n"
        "            curr += nums[j]\n"
        "            if curr >= k:\n"
        "                ans = min(ans, j - i + 1)\n"
        "                break  # shortest from this i; move to next i\n"
        "    return ans if ans != float('inf') else -1",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), " — try every possible starting index i for the subarray."])),
    N.para(N.rich([("for j in range(i, n):", {"code": True}), " — extend the subarray from i to j, accumulating elements."])),
    N.para(N.rich([("if curr >= k:", {"code": True}), " — found a valid subarray nums[i..j]. Length = j − i + 1."])),
    N.para(N.rich([("break", {"code": True}), " — earliest valid j for this i gives shortest subarray starting at i. No need to extend further."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                    "Time",     "Space"],
        ["Brute Force (nested loops)",  "O(n²)",    "O(1)"],
        ["Prefix Sum + Monotonic Deque","O(n)",     "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stack & Queue (Section 6 — Monotonic Queue sub-section)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Prefix Sum + Monotonic Deque — combine prefix sums with a monotone increasing deque of indices to find the minimum-length pair satisfying a sum condition in O(n)."])),
    N.callout(
        "When to recognize this pattern: (1) 'Shortest/longest subarray with sum ≥/≤ k' AND the array contains negative numbers. (2) The sliding window invariant breaks because sum is not monotone as window grows. (3) 'For each right boundary j, find the best left boundary i < j' — a classic monotone queue setup. (4) Any DP recurrence of the form dp[j] = max/min over a range of previous dp values.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique (Monotonic Queue / Prefix Sum + Deque):"),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Canonical monotone deque: maintain window maximum in O(n) for a fixed-size sliding window (#239)"])),
    N.bullet(N.rich([("Minimum Size Subarray Sum", {"bold": True}), " (Medium) — Same goal but all numbers positive → classic two-pointer sliding window O(n), no deque needed (#209)"])),
    N.bullet(N.rich([("Max Value of Equation", {"bold": True}), " (Hard) — Maximize yi + yj + |xi − xj| subject to |xi − xj| ≤ k; monotone deque optimization (#1499)"])),
    N.bullet(N.rich([("Constrained Subsequence Sum", {"bold": True}), " (Hard) — DP with range constraint: dp[j] = nums[j] + max(dp[j-k..j-1]); sliding window maximum via deque (#1425)"])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), " (Medium) — DP with sliding window max: dp[j] = nums[j] + max(dp[j-k..j-1]); same deque pattern (#1696)"])),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), " (Medium) — Prefix sum + hash map; same prefix-sum reframing but no negatives → hash map instead of deque (#560)"])),
    N.para("These problems share the core insight: prefix sums enable pair-search, and a monotone deque enables O(1) amortised access to the optimal historical value."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 6.4 — Monotonic Queue (Deque)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append in chunks ──
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page.")
print(f"NOTION OK {PAGE_ID}")
