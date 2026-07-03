"""
gen_ugly_number_ii.py — Notion page update for Ugly Number II (LC #264)
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8161-a1b2-f3f6b6ee3ae7"

# ─── 1) Set page properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=264,
    pattern="Math",
    subpatterns=["Three Pointers for 2 3 5"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Three pointers merge three multiplicative streams (×2, ×3, ×5) in sorted order; advance all pointers that tie to avoid duplicates.",
    icon="🟡"
)
print("Properties set.")

# ─── 2) Wipe old body ───
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ─── 3) Build new body ───
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("An ", {}),
        ("ugly number", {"bold": True}),
        (" is a positive integer whose only prime factors are ", {}),
        ("2", {"code": True}),
        (", ", {}),
        ("3", {"code": True}),
        (", and ", {}),
        ("5", {"code": True}),
        (". Given an integer ", {}),
        ("n", {"code": True}),
        (", return the ", {}),
        ("n", {"italic": True}),
        ("th ugly number. 1 is considered an ugly number.", {}),
    ])),
    N.para("Example: n=10 → return 12. The sequence is: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, ..."),
    N.divider(),
]

# ── Solution 1 — Three Pointers (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Three Pointers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the nth number in an infinite sequence defined by 'only prime factors 2, 3, 5'. Instead of testing every integer (wasteful), can we generate the sequence directly?"),

        N.h4("What Doesn't Work"),
        N.para("Brute force: iterate all integers 1, 2, 3, ... and check each for ugliness by repeatedly dividing by 2, 3, 5. Too slow for large n — each check is O(log M) and the nth ugly number M grows exponentially."),

        N.h4("The Key Observation"),
        N.para("Every ugly number > 1 is produced by multiplying a smaller ugly number by 2, 3, or 5. So ugly numbers form three sorted 'streams': {1×2, 2×2, 3×2, ...}, {1×3, 2×3, 3×3, ...}, {1×5, 2×5, ...}. We need to merge these streams in sorted order."),

        N.h4("Building the Solution"),
        N.para("Maintain three pointers p2, p3, p5 into the ugly[] array already built. Each pointer represents the next 'base' to multiply. At each step: pick min(ugly[p2]×2, ugly[p3]×3, ugly[p5]×5), append it, advance all pointer(s) that produced that minimum (the deduplication step)."),

        N.callout(
            "Analogy: Three tape-merge. Imagine three infinite sorted tapes: A=2,4,6,8..., B=3,6,9,12..., C=5,10,15.... Read heads from each tape, always write the smallest value. Three pointers = three read-heads.",
            "🧠", "blue_background"
        ),
    ]),

    N.h3("Code"),
    N.code("""def nthUglyNumber(n: int) -> int:
    ugly = [1]           # Seed: 1 is ugly by definition
    p2 = p3 = p5 = 0    # Three pointers, all start at index 0

    while len(ugly) < n:
        c2 = ugly[p2] * 2    # Next from ×2 stream
        c3 = ugly[p3] * 3    # Next from ×3 stream
        c5 = ugly[p5] * 5    # Next from ×5 stream
        nxt = min(c2, c3, c5)    # Pick globally smallest
        ugly.append(nxt)

        if nxt == c2: p2 += 1    # Advance ×2 if it contributed
        if nxt == c3: p3 += 1    # Advance ×3 if it contributed (NOT elif!)
        if nxt == c5: p5 += 1    # Advance ×5 if it contributed (NOT elif!)

    return ugly[n - 1]    # 1-indexed: nth ugly is at index n-1"""),

    N.h3("Line by Line"),
    N.para(N.rich([("ugly = [1]", {"code": True}), (" — Seed the sequence. 1 has no prime factors; it qualifies as ugly by convention.", {})])),
    N.para(N.rich([("p2 = p3 = p5 = 0", {"code": True}), (" — All three pointers start at index 0 (value=1). Initial candidates: 1×2=2, 1×3=3, 1×5=5.", {})])),
    N.para(N.rich([("while len(ugly) < n", {"code": True}), (" — Keep generating until we have n ugly numbers.", {})])),
    N.para(N.rich([("c2 = ugly[p2] * 2", {"code": True}), (" — The candidate from the factor-2 stream: take the ugly number at pointer p2 and multiply by 2.", {})])),
    N.para(N.rich([("c3, c5", {"code": True}), (" — Same idea for factors 3 and 5.", {})])),
    N.para(N.rich([("nxt = min(c2, c3, c5)", {"code": True}), (" — The globally smallest candidate is the next element in sorted order.", {})])),
    N.para(N.rich([("ugly.append(nxt)", {"code": True}), (" — Add it to the sequence.", {})])),
    N.para(N.rich([("if nxt == c2: p2 += 1", {"code": True}), (" — If the ×2 stream contributed, advance p2. This 'uses up' ugly[p2] for the ×2 stream.", {})])),
    N.para(N.rich([("Three separate if (not elif)", {"bold": True}), (" — When two or three candidates tie (e.g., 6 = 2×3 = 3×2), all matching pointers advance in the same step. Using elif would only advance one, causing duplicates.", {})])),
    N.para(N.rich([("return ugly[n - 1]", {"code": True}), (" — 1-indexed problem: the nth ugly number is at position n-1 in 0-indexed array.", {})])),
    N.divider(),
]

# ── Solution 2 — Min-Heap ──
blocks += [
    N.h2("Solution 2 — Min-Heap (More Flexible, O(n log n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal: generate ugly numbers in sorted order. But instead of tracking three specific pointers into one array, use a priority queue (min-heap) to always extract the current minimum."),

        N.h4("What Doesn't Work"),
        N.para("A naive heap without deduplication would insert 6 twice (once as 2×3, once as 3×2). We need a 'seen' set to prevent re-inserting values already in the heap."),

        N.h4("The Key Observation"),
        N.para("Every time we pop a number x from the heap, x is the next ugly number. We then push x×2, x×3, x×5 (if not seen) as candidates for future positions. The heap automatically gives us the minimum at each step."),

        N.h4("Building the Solution"),
        N.para("Initialize heap=[1], seen={1}. Pop n times; each pop gives the next ugly number. After each pop, try pushing pop_val×2, pop_val×3, pop_val×5 if not in seen."),
    ]),

    N.h3("Code"),
    N.code("""import heapq

def nthUglyNumber(n: int) -> int:
    heap = [1]     # Min-heap seeded with 1
    seen = {1}     # Track what's in the heap to avoid duplicates
    cur = 1

    for _ in range(n):          # Extract n times
        cur = heapq.heappop(heap)
        for factor in (2, 3, 5):
            nxt = cur * factor
            if nxt not in seen:
                heapq.heappush(heap, nxt)
                seen.add(nxt)

    return cur    # After n extractions, cur is the nth ugly"""),

    N.h3("Line by Line"),
    N.para(N.rich([("heap = [1]; seen = {1}", {"code": True}), (" — Min-heap and seen set, both seeded with 1.", {})])),
    N.para(N.rich([("for _ in range(n): cur = heapq.heappop(heap)", {"code": True}), (" — Extract the minimum n times. After the n-th extraction, cur is the nth ugly number.", {})])),
    N.para(N.rich([("for factor in (2,3,5): if nxt not in seen: heappush", {"code": True}), (" — Generate three candidates from cur; only add each if not already present to avoid duplicates.", {})])),
    N.para(N.rich([("return cur", {"code": True}), (" — The value of the last pop is the answer.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (check every int)", "O(n × log M)", "O(1)"],
        ["Min-Heap", "O(n log n)", "O(n)"],
        ["Three Pointers (Optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Math — sequence generation with multiplicative structure", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Three Pointers for 2·3·5 — merge three multiplicative sorted streams using index pointers into a single shared array", {})])),
    N.callout(
        "When to recognize this pattern: Problem asks for nth number in sequence defined by specific prime factors. 'Only prime factors are 2, 3, 5 (or similar set)'. Need O(n) generation without sorting or set membership.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same three-pointer / k-way merge technique:"),
    N.bullet(N.rich([("Ugly Number", {"bold": True}), (" (Easy, LC #263) — Check if a single number is ugly: divide repeatedly by 2/3/5 until 1 or non-divisible.", {})])),
    N.bullet(N.rich([("Super Ugly Number", {"bold": True}), (" (Medium, LC #313) — Generalize: k prime factors instead of 3. Use k pointers instead of p2/p3/p5.", {})])),
    N.bullet(N.rich([("Nth Magical Number", {"bold": True}), (" (Hard, LC #878) — Nth number divisible by a or b. Uses LCM math, related generation idea.", {})])),
    N.bullet(N.rich([("Merge k Sorted Lists", {"bold": True}), (" (Hard, LC #23) — Classic k-way sorted merge; same 'always pick minimum head' pattern, but with linked lists.", {})])),
    N.bullet(N.rich([("Kth Smallest Element in Sorted Matrix", {"bold": True}), (" (Medium, LC #378) — Min-heap to extract kth element from structured 2D sorted sequence.", {})])),
    N.bullet(N.rich([("Find K Pairs with Smallest Sums", {"bold": True}), (" (Medium, LC #373) — Min-heap over pairs from two sorted arrays; same 'generate candidates from structure' idea.", {})])),
    N.bullet(N.rich([("Smallest Range Covering Elements from K Lists", {"bold": True}), (" (Hard, LC #632) — Multi-stream merge with heap tracking range.", {})])),
    N.para("These problems share the same core technique: structured generation from sorted streams using pointer(s) or a min-heap."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math / Three Pointers for 2·3·5 sub-pattern", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("ugly_number_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4) Append blocks ───
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
