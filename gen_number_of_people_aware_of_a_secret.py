"""
gen_number_of_people_aware_of_a_secret.py
Regenerates the Notion page for LeetCode #2327 — Number of People Aware of a Secret
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81bc-8dcb-f4c0d99af0f5"
SLUG    = "number_of_people_aware_of_a_secret"

# ── 1. Properties ────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 2327,
    pattern     = "Queues",
    subpatterns = ["Queue with Delay/Forget"],
    tc          = "O(n)",
    sc          = "O(n)",
    key_insight = "Batch learners by day; active sharers form a sliding window in dp — maintain O(1) running sum.",
    icon        = "🟡",
)
print("Properties set.")

# ── 2. Wipe existing blocks ───────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3. Build body ─────────────────────────────────────────────────────────────
PROBLEM_STMT = (
    "On day 1, one person discovers a secret. Each person who knows the secret will "
    "share it with a new person every day for the period of days after learning it — "
    "starting delay days later and ending forget days after they first learned it. "
    "Return the number of people who know the secret at the end of day n, modulo 10^9+7.\n\n"
    "Constraints: 2 <= n <= 1000, 1 <= delay < forget <= n."
)

SOL1_CODE = """\
def peopleAwareOfSecret(n: int, delay: int, forget: int) -> int:
    MOD = 10**9 + 7
    dp = [0] * (n + 1)   # dp[i] = people who first learned on day i
    dp[1] = 1
    share = 0             # running count of currently active sharers
    for d in range(2, n + 1):
        # Batch that just cleared their delay — they start sharing today
        if d - delay >= 1:
            share += dp[d - delay]
        # Batch that just forgot — remove from active pool
        if d - forget >= 1:
            share -= dp[d - forget]
        share %= MOD
        dp[d] = share     # each sharer teaches 1 new person → dp[d] new learners
    # Only count people who haven't forgotten by day n
    lo = max(1, n - forget + 1)
    return sum(dp[lo:n + 1]) % MOD
"""

SOL2_CODE = """\
def peopleAwareOfSecret_brute(n: int, delay: int, forget: int) -> int:
    MOD = 10**9 + 7
    dp = [0] * (n + 1)
    dp[1] = 1
    for d in range(2, n + 1):
        lo = max(1, d - forget + 1)   # earliest still-active learner day
        hi = max(0, d - delay)        # latest cleared-delay learner day
        dp[d] = sum(dp[lo:hi + 1]) % MOD  # O(n) per day → O(n^2) total
    return sum(dp[max(1, n - forget + 1):n + 1]) % MOD
"""

blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# Solution 1 — Optimal sliding window DP
blocks += [
    N.h2("Solution 1 — Sliding-Window DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to count how many people know a secret at end of day n, "
            "given a chain-reaction spread with fixed delay and expiry. Tracking "
            "individuals is impossible because the population grows exponentially."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A BFS/DFS that tracks each person individually would require O(2^n) "
            "nodes. Even a simulation with person objects fails — there can be "
            "millions of people by day n=1000. We need an aggregate view."
        ),
        N.h4("The Key Observation"),
        N.para(
            "All people who learned on the same day have identical future behavior: "
            "same start-sharing day (L+delay), same forget day (L+forget). "
            "So dp[L] = count who learned on day L is exact, not approximate. "
            "The recurrence becomes: dp[d] = sum(dp[L] for L in sharing window). "
            "And that window is contiguous — a sliding window in the dp array."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: dp[1]=1. Step 2: For each day d, the active sharing window is "
            "L in [d-forget+1, d-delay]. Step 3: Maintain a running 'share' variable "
            "that tracks window sum in O(1): add dp[d-delay] when new batch enters, "
            "subtract dp[d-forget] when old batch leaves. Step 4: At end, sum only "
            "dp[n-forget+1..n] — people who haven't forgotten."
        ),
        N.callout(
            "Analogy: Imagine a relay race where each runner waits 'delay' laps before "
            "passing the baton, and runs for 'forget-delay' laps total. At any time, "
            "only a window of runners is active. Track the window, not individuals.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("MOD = 10**9 + 7", {"code": True}), " — Standard modulus to prevent integer overflow on return."])),
    N.para(N.rich([("dp = [0]*(n+1); dp[1] = 1", {"code": True}), " — Initialize dp array. Day 1 has exactly one learner."])),
    N.para(N.rich([("share = 0", {"code": True}), " — Running sum of currently active sharers. Maintained in O(1) per step."])),
    N.para(N.rich([("if d - delay >= 1: share += dp[d-delay]", {"code": True}), " — Batch who learned on day d-delay has now cleared their delay; they start sharing today."])),
    N.para(N.rich([("if d - forget >= 1: share -= dp[d-forget]", {"code": True}), " — Batch who learned on day d-forget forgets today; remove from active pool."])),
    N.para(N.rich([("share %= MOD", {"code": True}), " — Modulo after subtraction (Python % is always non-negative, so this handles negative results correctly)."])),
    N.para(N.rich([("dp[d] = share", {"code": True}), " — Active sharers each tell one new person, so dp[d] = share."])),
    N.para(N.rich([("sum(dp[lo:n+1]) % MOD", {"code": True}), " — Sum only people who haven't forgotten by day n. lo = max(1, n-forget+1)."])),
    N.divider(),
]

# Solution 2 — Brute force
blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: Directly Sum the Window Each Day", [
        N.h4("Reframe the Problem"),
        N.para("Same dp[d] formulation. Instead of maintaining a running sum, recompute the full window sum from scratch each day."),
        N.h4("What Doesn't Work at Scale"),
        N.para("For each of n days, we sum up to n-1 previous values — giving O(n²) total. For n=1000 this is 10^6 operations and passes, but for larger n it would TLE."),
        N.h4("The Key Observation"),
        N.para("The brute force is valuable as a stepping stone: write it first for correctness, then optimize by noting the window shifts by 1 each step — yielding the O(n) sliding window version."),
        N.h4("Building the Solution"),
        N.para("For each day d: lo = max(1, d-forget+1), hi = max(0, d-delay). dp[d] = sum(dp[lo..hi]). Final answer: sum(dp[n-forget+1..n])."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("lo = max(1, d-forget+1)", {"code": True}), " — Earliest day still within the active-sharing window (clamped to day 1)."])),
    N.para(N.rich([("hi = max(0, d-delay)", {"code": True}), " — Latest day that has cleared the delay (0 means no valid index → empty window)."])),
    N.para(N.rich([("dp[d] = sum(dp[lo:hi+1])", {"code": True}), " — Sum the contiguous window directly. O(n) per day, O(n²) overall."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time",  "Space", "Notes"],
        ["Brute Force (O(n²))",   "O(n²)", "O(n)",  "Correct but slow for large n"],
        ["Sliding Window DP ✓",   "O(n)",  "O(n)",  "Interview-optimal, O(1) per step"],
    ]),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Queues"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Queue with Delay/Forget — propagation with fixed-delay start and fixed-duration expiry, solved via sliding window DP"])),
    N.callout(
        "When to recognize this pattern: 'each person waits X days then starts doing Y, "
        "and stops after Z days' → index DP by day, maintain active pool as sliding window sum. "
        "Signals: time-indexed spread, fixed delay, fixed expiry, count-at-end-of-day.",
        "🔎", "green_background"
    ),
    N.para("Note: The Queue with Delay/Forget sub-pattern is classification based on analysis — "
           "it combines queue-based simulation concepts with sliding-window DP optimization."),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or adjacent technique:"),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock with Cooldown", {"bold": True}), " (Medium) — Fixed cooldown delay before re-entering active state (#309)"])),
    N.bullet(N.rich([("Domino and Tromino Tiling", {"bold": True}), " (Medium) — DP recurrence over fixed sliding window of previous states (#790)"])),
    N.bullet(N.rich([("Jump Game VII", {"bold": True}), " (Medium) — Sliding window reachability DP on boolean array (#1871)"])),
    N.bullet(N.rich([("Number of Flowers in Full Bloom", {"bold": True}), " (Hard) — Track active intervals with delay/expiry events (#2251)"])),
    N.bullet(N.rich([("Count Vowels Permutation", {"bold": True}), " (Hard) — Day-indexed DP where each state depends on previous window (#1220)"])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Deque-based sliding window on array (#239)"])),
    N.bullet(N.rich([("House Robber", {"bold": True}), " (Medium) — DP where each choice has delayed consequences (#198)"])),
    N.para("These problems share the core technique: aggregate by time index, maintain an active window in O(1) per step."),
    N.callout("📚 Pattern: Queue with Delay/Forget — Analysis-based classification combining queue simulation + sliding window DP optimization.", "📚", "gray_background"),
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

# ── 4. Append blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
