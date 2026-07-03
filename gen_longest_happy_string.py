"""
gen_longest_happy_string.py
Notion IN-PLACE update for LeetCode #1405 Longest Happy String
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c0-a018-e30882ae3945"
SLUG = "longest_happy_string"

# ─── 1. Set properties ───────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1405,
    pattern="Heaps",
    subpatterns=["Greedy + Heap"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Always pick the most-abundant character; if it would create a triple, use the 2nd-most abundant for one step to break the streak.",
    icon="🟡"
)
print("Properties set.")

# ─── 2. Wipe old content ─────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── 3. Build body blocks ─────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given three integers ", {}),
        ("a", {"code": True}),
        (", ", {}),
        ("b", {"code": True}),
        (", and ", {}),
        ("c", {"code": True}),
        (", return the longest possible ", {}),
        ("happy string", {"bold": True}),
        (". A happy string is one that: (1) uses only 'a', 'b', 'c' characters, (2) uses at most ", {}),
        ("a", {"code": True}),
        (" 'a's, ", {}),
        ("b", {"code": True}),
        (" 'b's, and ", {}),
        ("c", {"code": True}),
        (" 'c's, and (3) does not contain 'aaa', 'bbb', or 'ccc' as a substring. If there are multiple valid answers, return any. If none exists, return an empty string.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Max Heap Greedy (Interview Pick) ──
SOL1_CODE = """\
import heapq

def longestDiverseString(a: int, b: int, c: int) -> str:
    heap = []
    for cnt, ch in [(a, 'a'), (b, 'b'), (c, 'c')]:
        if cnt > 0:
            heapq.heappush(heap, (-cnt, ch))  # negate for max-heap
    res = []
    while heap:
        cnt, ch = heapq.heappop(heap)
        cnt = -cnt
        # Triple check: would appending ch create 3 in a row?
        if len(res) >= 2 and res[-1] == ch and res[-2] == ch:
            if not heap:
                break  # stuck: no fallback available
            cnt2, ch2 = heapq.heappop(heap)
            cnt2 = -cnt2
            res.append(ch2)            # use second char to break streak
            if cnt2 - 1 > 0:
                heapq.heappush(heap, (-(cnt2 - 1), ch2))
            heapq.heappush(heap, (-cnt, ch))  # restore top (unused)
        else:
            res.append(ch)             # safe: use top char
            if cnt - 1 > 0:
                heapq.heappush(heap, (-(cnt - 1), ch))
    return ''.join(res)
"""

blocks += [
    N.h2("Solution 1 — Max Heap Greedy (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're building a string character by character. At each position, we must choose which character to place. We want to maximize string length, so we should never waste a position if we can help it. The only constraint is: don't place the same character three times in a row."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all orderings of the characters — exponential time, impossible for large counts. Round-robin (a, b, c, a, b, c, ...): doesn't account for unequal counts — if c=100, a=1, b=1 we'd use most c's as wasted slots. Greedily placing 2 of the top character at once: risks creating triples if the previous character was the same."),
        N.h4("The Key Observation"),
        N.para("The character with the highest remaining count is the most 'dangerous' — if we ignore it for too long, we'll be left with only it and can't place more than 2 more. So always prefer the highest-count character. Only deviate when it would create a triple — then use the second-highest for exactly one step."),
        N.h4("Building the Solution"),
        N.para("Step 1: Track counts in a max-heap. Step 2: Pop the highest-count character. Step 3: Can we safely append it? Check: are the last 2 characters already this character? If YES — use the second-highest for one step instead, then push the top back. If NO — append it, decrement count, push back. Step 4: Repeat until heap is empty or we're stuck."),
        N.callout("Analogy: Imagine a dish where you can't have 3 scoops of the same flavor in a row. You always fill with your favorite flavor — unless the last 2 scoops were already that flavor, in which case you take one scoop of your second-favorite to reset.", "🍨", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = []", {"code": True}), " — Initialize the max-heap (will hold (-count, char) tuples)."])),
    N.para(N.rich([("for cnt, ch in [(a,'a'),(b,'b'),(c,'c')]:", {"code": True}), " — Iterate over each character type with its count."])),
    N.para(N.rich([("if cnt > 0: heapq.heappush(heap, (-cnt, ch))", {"code": True}), " — Only add non-zero counts. Negate cnt because Python's heapq is a min-heap; negation simulates max-heap behavior."])),
    N.para(N.rich([("res = []", {"code": True}), " — Build result as a list for O(1) append; join at the end."])),
    N.para(N.rich([("cnt, ch = heapq.heappop(heap)", {"code": True}), " — Pop the tuple with the smallest first element = largest count (due to negation)."])),
    N.para(N.rich([("cnt = -cnt", {"code": True}), " — Un-negate to recover the actual remaining count."])),
    N.para(N.rich([("if len(res)>=2 and res[-1]==ch and res[-2]==ch:", {"code": True}), " — Triple check: would appending ch now create 3 in a row? We need BOTH conditions: last char = ch AND second-last char = ch."])),
    N.para(N.rich([("if not heap: break", {"code": True}), " — If there's no second character to use as fallback, we're stuck. This is the optimal stopping point."])),
    N.para(N.rich([("cnt2, ch2 = heapq.heappop(heap)", {"code": True}), " — Pop the second-best character to use as a streak-breaker."])),
    N.para(N.rich([("res.append(ch2)", {"code": True}), " — Append the second character (not the top one) to break the streak."])),
    N.para(N.rich([("if cnt2 - 1 > 0: heapq.heappush(...ch2)", {"code": True}), " — Push ch2 back if it has remaining supply."])),
    N.para(N.rich([("heapq.heappush(heap, (-cnt, ch))", {"code": True}), " — Push the original top character back — we didn't use it this step, so count is unchanged."])),
    N.para(N.rich([("res.append(ch) / if cnt-1>0: heapq.heappush(...ch)", {"code": True}), " — Normal case: append the top character, decrement count, push back if any remaining."])),
    N.para(N.rich([("return ''.join(res)", {"code": True}), " — Join the list into a single string."])),
    N.divider(),
]

# ── Solution 2: Simple Sort Greedy ──
SOL2_CODE = """\
def longestDiverseString(a: int, b: int, c: int) -> str:
    counts = {'a': a, 'b': b, 'c': c}
    res = []
    while True:
        # Sort 3 chars descending by count — O(1) since only 3 items
        order = sorted(counts, key=lambda x: -counts[x])
        placed = False
        for ch in order:
            if counts[ch] == 0:
                continue
            if len(res) >= 2 and res[-1] == ch and res[-2] == ch:
                continue  # would create triple — skip
            res.append(ch)
            counts[ch] -= 1
            placed = True
            break  # picked first valid char in sorted order
        if not placed:
            break  # no valid placement found: stop
    return ''.join(res)
"""

blocks += [
    N.h2("Solution 2 — Simple Sort Greedy"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same greedy logic but without the heap overhead. Since we only have 3 character types, sorting 3 items is O(1) per step. This gives a simpler implementation for the specific 3-character case."),
        N.h4("What Doesn't Work"),
        N.para("This approach doesn't generalize to k > 3 character types efficiently — sorting k items per iteration would be O(k log k) per step. For the general case, the heap is better."),
        N.h4("The Key Observation"),
        N.para("With only 3 character types, we can sort all three each step in O(1) (constant 3 comparisons). Iterate through the sorted order and pick the first character that's valid (non-zero count, no triple risk). This is exactly the same greedy choice as the heap version, just expressed differently."),
        N.h4("Building the Solution"),
        N.para("Sort the 3 characters by remaining count. For each in order: if count > 0 AND won't create a triple: pick it, decrement, break. If no character was placed: stop. This is clean and correct for the 3-character constraint."),
        N.callout("When to prefer this: in an interview, you might propose this simpler version first for the 3-char case, then mention that the heap version generalizes to k character types.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("counts = {'a': a, 'b': b, 'c': c}", {"code": True}), " — Store counts in a dict for easy update."])),
    N.para(N.rich([("order = sorted(counts, key=lambda x: -counts[x])", {"code": True}), " — Sort 3 chars by count descending. With 3 items this is O(1)."])),
    N.para(N.rich([("for ch in order:", {"code": True}), " — Try each character in order of preference (highest count first)."])),
    N.para(N.rich([("if counts[ch] == 0: continue", {"code": True}), " — Skip exhausted characters."])),
    N.para(N.rich([("if len(res)>=2 and res[-1]==ch and res[-2]==ch: continue", {"code": True}), " — Skip if adding this would create a triple."])),
    N.para(N.rich([("res.append(ch); counts[ch] -= 1; placed = True; break", {"code": True}), " — Pick the first valid character: append, decrement, mark placed, break out of the for loop."])),
    N.para(N.rich([("if not placed: break", {"code": True}), " — No valid character was found: every option is either exhausted or would triple. Stop."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Max Heap Greedy (Interview Pick)", "O(n log 3) = O(n)", "O(3) = O(1)"],
        ["Simple Sort Greedy", "O(n)", "O(1)"],
        ["Brute Force (backtracking)", "O(n!)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Heaps"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Greedy + Heap — Repeatedly extract the maximum-count element from a heap to make greedy decisions, with a fallback to the second-best element when the top would violate a local constraint."])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) 'Maximize string/sequence length' with a 'no k consecutive same elements' constraint. (2) 'Arrange tasks/characters' with a cooldown or separation requirement. (3) You repeatedly need 'the most frequent available item' across iterations. (4) The greedy choice is obvious (take the most abundant) but has a local exception (the triple/consecutive constraint).", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Greedy + Heap for constrained sequence construction):"),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), " (Medium) — Schedule CPU tasks with n-unit cooldown; greedily pick most frequent available task each cycle. (#621)"])),
    N.bullet(N.rich([("Reorganize String", {"bold": True}), " (Medium) — Rearrange string so no two adjacent characters are the same; max-heap over 26 letters. (#767)"])),
    N.bullet(N.rich([("Rearrange String k Distance Apart", {"bold": True}), " (Hard) — Same character must be at least k positions apart; greedy + heap + queue. (#358)"])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), " (Medium) — Minimum meeting rooms needed; greedy assignment using min-heap of end times. (#253)"])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), " (Medium) — Extract k most frequent elements; max-heap over frequency counts. (#347)"])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), " (Easy) — Maintain k-size heap for running kth largest. (#703)"])),
    N.para("These problems share the core technique: a heap provides efficient access to the most valuable item, while greedy logic determines when to use a fallback."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Heaps → Sub-Pattern: Greedy + Heap", "📚", "gray_background"),
]

# ── Visual Explainer Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ─── 4. Append all blocks ─────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
