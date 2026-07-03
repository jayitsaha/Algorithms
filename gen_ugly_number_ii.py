"""
gen_ugly_number_ii.py — Rebuild Notion page for Ugly Number II (LC #264)
Step 0 resume: HTML already OK (998 lines, all markers present). Only Notion needed.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8161-a1b2-f3f6b6ee3ae7"
SLUG = "ugly_number_ii"

# ── 1. Set properties ────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=264,
    pattern="Math",
    subpatterns=["Three Pointers (2-3-5 Multiples)", "DP: Sequence Generation"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Track the next multiple of 2, 3, and 5 with three independent pointers; advance the one(s) producing the minimum.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ────────────────────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3. Build new body ───────────────────────────────────────────────────────
PROBLEM_STATEMENT = (
    "An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. "
    "Given an integer n, return the nth ugly number in the infinite sequence 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, …"
)

SOL1_CODE = """\
def nthUglyNumber(n: int) -> int:
    ugly = [1] * n          # dp array: ugly[i] = (i+1)-th ugly number
    p2 = p3 = p5 = 0       # three pointers: next index to multiply by 2, 3, 5

    for i in range(1, n):
        next2 = ugly[p2] * 2
        next3 = ugly[p3] * 3
        next5 = ugly[p5] * 5

        ugly[i] = min(next2, next3, next5)  # smallest candidate wins

        if ugly[i] == next2: p2 += 1   # advance the pointer that produced the min
        if ugly[i] == next3: p3 += 1   # use 'if' not 'elif': handles ties (e.g. 6=2*3=3*2)
        if ugly[i] == next5: p5 += 1

    return ugly[n - 1]
"""

SOL2_CODE = """\
import heapq

def nthUglyNumber(n: int) -> int:
    heap = [1]             # min-heap; start with seed 1
    seen = {1}             # deduplicate: avoid pushing the same number twice
    val = 1

    for _ in range(n):
        val = heapq.heappop(heap)
        for factor in (2, 3, 5):
            nxt = val * factor
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, nxt)

    return val
"""

SOL3_CODE = """\
def nthUglyNumber_brute(n: int) -> int:
    def is_ugly(num):
        for p in (2, 3, 5):
            while num % p == 0:
                num //= p
        return num == 1

    count, num = 0, 0
    while count < n:
        num += 1
        if is_ugly(num):
            count += 1
    return num
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("n = 10 → return 12 (the sequence: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12)"),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ n ≤ 1690. Note: 1 is conventionally treated as an ugly number (no prime factors)."),
    ])),
    N.divider(),
]

# ── Solution 1: Three-Pointer DP (Interview Pick) ─────────────────────────
blocks += [
    N.h2("Solution 1 — Three-Pointer DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to generate ugly numbers in sorted order. Each ugly number is either 1, "
            "or a smaller ugly number multiplied by 2, 3, or 5. So the sequence is self-referential: "
            "we can build it from previously computed values."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute-force checking every integer is O(U_n * log U_n) where U_n grows roughly as n^3 "
            "— for n=1690 that is ~2 billion iterations. "
            "A min-heap works but costs O(n log n) time and extra space for a hash set."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Every ugly number (except 1) is produced by multiplying a previous ugly number by exactly "
            "one of {2, 3, 5}. We track, for each factor, 'which is the smallest ugly I haven't yet "
            "multiplied by this factor?' Three pointers p2, p3, p5 each point to the next index in the "
            "ugly array to be promoted."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Start: ugly = [1]. At each step compute next2=ugly[p2]*2, next3=ugly[p3]*3, next5=ugly[p5]*5. "
            "Append min of the three. Advance ALL pointers whose candidate equals the minimum "
            "(using 'if' not 'elif') to handle ties like 6 = 2*3 = 3*2 — both p2 and p3 must advance."
        ),
        N.callout(
            "Analogy: Three assembly lines stamp '×2', '×3', '×5' on every ugly number in order. "
            "We always take the smallest item off whichever line(s) produced it.",
            "🏭", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("ugly = [1] * n", {"code": True}), " — Allocate the DP array; seed position 0 with 1 (the first ugly number)."])),
    N.para(N.rich([("p2 = p3 = p5 = 0", {"code": True}), " — Three pointers all start at index 0; all will first multiply ugly[0]=1."])),
    N.para(N.rich([("for i in range(1, n):", {"code": True}), " — Fill positions 1..n-1; position 0 is already seeded with 1."])),
    N.para(N.rich([("next2 = ugly[p2] * 2", {"code": True}), " — Smallest ugly number not yet multiplied by 2."])),
    N.para(N.rich([("next3 = ugly[p3] * 3", {"code": True}), " — Smallest ugly number not yet multiplied by 3."])),
    N.para(N.rich([("next5 = ugly[p5] * 5", {"code": True}), " — Smallest ugly number not yet multiplied by 5."])),
    N.para(N.rich([("ugly[i] = min(next2, next3, next5)", {"code": True}), " — The true next ugly number is the smallest of the three candidates."])),
    N.para(N.rich([("if ugly[i] == next2: p2 += 1", {"code": True}), " — Advance p2 if it contributed. Note: 'if' not 'elif'."])),
    N.para(N.rich([("if ugly[i] == next3: p3 += 1", {"code": True}), " — Multiple pointers can advance in the same step (handles ties)."])),
    N.para(N.rich([("if ugly[i] == next5: p5 += 1", {"code": True}), " — Ensures no duplicates even when two factors produce the same value."])),
    N.para(N.rich([("return ugly[n - 1]", {"code": True}), " — The nth ugly number (1-indexed)."])),
    N.callout(
        "Critical: Use 'if' not 'elif' for pointer advancement. "
        "When multiple factors produce the same minimum (e.g. 2*3=6 and 3*2=6), "
        "both pointers must advance or you will generate duplicates.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Min-Heap ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Min-Heap with Deduplication"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the nth smallest element from the infinite set of ugly numbers. "
            "A min-heap is the natural tool for 'always give me the current minimum'."
        ),
        N.h4("What Doesn't Work Without Deduplication"),
        N.para(
            "If we push val*2, val*3, val*5 without a seen set, the number 6 appears twice "
            "(from 2*3 and from 3*2). We need deduplication."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Start the heap with {1}. Pop the minimum (always an ugly number). "
            "For each popped value, push val*2, val*3, val*5 if not already seen. "
            "After n pops, the last popped value is the answer."
        ),
        N.h4("Building the Solution"),
        N.para(
            "This is essentially BFS on the ugly-number DAG where edges are 'multiply by 2/3/5'. "
            "The heap ensures we visit nodes in order. O(n log n) due to heap operations."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = [1]", {"code": True}), " — Min-heap seeded with 1 (the only ugly number less than 2)."])),
    N.para(N.rich([("seen = {1}", {"code": True}), " — Hash set to avoid pushing duplicate numbers."])),
    N.para(N.rich([("for _ in range(n):", {"code": True}), " — Pop exactly n times; the last pop is our answer."])),
    N.para(N.rich([("val = heapq.heappop(heap)", {"code": True}), " — Extract the current smallest ugly number."])),
    N.para(N.rich([("for factor in (2, 3, 5):", {"code": True}), " — Generate all children of this ugly number."])),
    N.para(N.rich([("if nxt not in seen:", {"code": True}), " — Skip if we've already scheduled this child."])),
    N.para(N.rich([("seen.add(nxt); heapq.heappush(heap, nxt)", {"code": True}), " — Mark and enqueue the new ugly number."])),
    N.para(N.rich([("return val", {"code": True}), " — After n pops, val holds the nth ugly number."])),
    N.divider(),
]

# ── Solution 3: Brute Force ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force (Educational Only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Check every positive integer and count how many are ugly."),
        N.h4("What Doesn't Work"),
        N.para(
            "The 1690th ugly number is 2,123,366,400 — we'd loop through 2+ billion integers. "
            "O(U_n * log U_n) — absolutely TLE for n > ~500."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A number is ugly iff dividing out all factors of 2, 3, 5 leaves 1. "
            "This check is O(log num) per number, but the outer loop dominates."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def is_ugly(num):", {"code": True}), " — Helper: True if num's only prime factors are 2, 3, 5."])),
    N.para(N.rich([("for p in (2, 3, 5): while num % p == 0: num //= p", {"code": True}), " — Strip all factors of 2, 3, and 5."])),
    N.para(N.rich([("return num == 1", {"code": True}), " — If nothing remains, all prime factors were in {2,3,5}."])),
    N.para(N.rich([("while count < n: num += 1; if is_ugly(num): count += 1", {"code": True}), " — Scan upward, counting ugly numbers."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                    "Time",             "Space"],
        ["Three-Pointer DP (Optimal)",  "O(n)",             "O(n)"],
        ["Min-Heap",                    "O(n log n)",       "O(n)"],
        ["Brute Force",                 "O(U_n · log U_n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math / Sequence Generation"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Three Pointers (2-3-5 Multiples), DP: Sequence Generation"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Asked for the nth element of a sequence defined by multiplying existing elements by a fixed prime set.\n"
        "• Phrase 'prime factors limited to {2, 3, 5}' (or any small set) in the problem.\n"
        "• Variants: Super Ugly Number (arbitrary primes → k pointers), Ugly Number III (binary search on count).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same three-pointer / k-pointer sequence generation technique:"),
    N.bullet(N.rich([("Ugly Number (LC 263)", {"bold": True}), " (Easy) — is_ugly predicate; base problem for understanding the definition."])),
    N.bullet(N.rich([("Super Ugly Number (LC 313)", {"bold": True}), " (Medium) — Generalize to k arbitrary primes with k pointers; direct extension."])),
    N.bullet(N.rich([("Ugly Number III (LC 1201)", {"bold": True}), " (Medium) — Count ugly numbers up to x via inclusion-exclusion + binary search on the answer."])),
    N.bullet(N.rich([("Nth Magical Number (LC 878)", {"bold": True}), " (Hard) — Binary search for nth number divisible by a or b; related count-based approach."])),
    N.bullet(N.rich([("Merge K Sorted Lists (LC 23)", {"bold": True}), " (Hard) — Min-heap merging; structurally identical to the heap solution here."])),
    N.bullet(N.rich([("Count Primes (LC 204)", {"bold": True}), " (Medium) — Sieve of Eratosthenes; complementary view of eliminating non-ugly numbers."])),
    N.bullet(N.rich([("K-th Smallest Prime Fraction (LC 786)", {"bold": True}), " (Hard) — Binary search on answer; nth element from structured infinite set."])),
    N.para(
        "These problems share the core technique: generate a structured infinite sequence by "
        "tracking 'what is the next element each generator produces?' via k pointers or a min-heap."
    ),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math / Sequence Generation section.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
