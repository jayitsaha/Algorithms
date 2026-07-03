"""Notion update script for Happy Number (#202)."""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8184-bfd0-d82592b515a2"

# ── 1) Set properties ──────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=202,
    pattern="Linked List",
    subpatterns=["Fast-Slow Pointer"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Model digit-square-sum as implicit linked list; Floyd's fast-slow detects cycle vs fixed-point-1.",
    icon="🟢"
)
print("Properties set OK")

# ── 2) Wipe existing body ──────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks")

# ── 3) Build body ─────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para("Write an algorithm to determine if a number n is happy. A happy number is defined by: starting with any positive integer, replace it with the sum of the squares of its digits and repeat the process until the number either equals 1 (happy) or loops endlessly in a cycle that never includes 1 (not happy). Return true if n is a happy number, and false if not."),
    N.callout(
        N.rich([
            ("Example — Happy: ", {"bold": True}),
            "n=19 → 1²+9²=82 → 8²+2²=68 → 6²+8²=100 → 1²+0²+0²=1. Return True.\n",
            ("Example — Not Happy: ", {"bold": True}),
            "n=2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → ... (cycle). Return False."
        ]),
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1: Floyd's Cycle Detection ──────────────────────
blocks += [
    N.h2("Solution 1 — Floyd's Fast-Slow Pointer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The transformation f(n) = digit-square-sum maps every positive integer to exactly one next value. This is identical to a linked list where each node has a unique 'next' pointer. The question becomes: does this implicit linked list reach the node '1', or does it cycle endlessly?"),
        N.h4("What Doesn't Work"),
        N.para("A naive while loop 'while n != 1: n = f(n)' runs forever for non-happy numbers since they cycle. We need a termination condition for the non-happy case without knowing the cycle in advance."),
        N.h4("The Key Observation"),
        N.para("Any sequence that is bounded and deterministic must eventually revisit a value. Once a value repeats, the sequence cycles. So we need cycle detection. This is exactly the Linked List Cycle problem in disguise."),
        N.h4("Building the Solution"),
        N.para("Floyd's algorithm: run two pointers through the sequence — slow advances 1 step, fast advances 2 steps. If the sequence has a cycle, fast will eventually lap slow and they will meet inside that cycle. If the sequence reaches 1 (a fixed point: f(1)=1), both will reach 1. In both cases, they meet. Check where they meet: if at 1, happy; otherwise not."),
        N.callout("Analogy: Two runners on a circular track. The faster runner will always lap the slower one if the track loops. If the track ends at a finish line (value 1), both reach it together.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def isHappy(n: int) -> bool:\n"
        "    def digit_sq_sum(x):\n"
        "        total = 0\n"
        "        while x:\n"
        "            x, d = divmod(x, 10)  # d = last digit\n"
        "            total += d * d\n"
        "        return total\n"
        "\n"
        "    slow = n\n"
        "    fast = digit_sq_sum(n)  # hare starts 1 step ahead\n"
        "    while slow != fast:\n"
        "        slow = digit_sq_sum(slow)               # 1 step\n"
        "        fast = digit_sq_sum(digit_sq_sum(fast)) # 2 steps\n"
        "    return slow == 1  # met at 1 = happy; met elsewhere = cycle"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def digit_sq_sum(x)", {"code": True}), " — Helper that extracts each digit via divmod(x, 10) and sums their squares. This is the 'next pointer' of the implicit linked list."])),
    N.para(N.rich([("x, d = divmod(x, 10)", {"code": True}), " — Splits off the last digit d; x becomes the remaining number. Cleaner than x % 10 + x // 10 separately."])),
    N.para(N.rich([("total += d * d", {"code": True}), " — Squares the digit and accumulates. After the while loop, total is the digit-square-sum."])),
    N.para(N.rich([("slow = n; fast = digit_sq_sum(n)", {"code": True}), " — Tortoise starts at n; hare starts one step ahead. This ensures slow != fast on first loop iteration."])),
    N.para(N.rich([("while slow != fast:", {"code": True}), " — Loop until they meet. For happy numbers they meet at 1; for non-happy they meet inside the 4-cycle."])),
    N.para(N.rich([("fast = digit_sq_sum(digit_sq_sum(fast))", {"code": True}), " — Hare takes 2 steps (apply f twice). This is what makes it gain on the tortoise."])),
    N.para(N.rich([("return slow == 1", {"code": True}), " — After they meet, check the meeting value. Only 1 means happy. Any other value (4, 89, etc.) means they met in the non-1 cycle."])),
    N.divider(),
]

# ── Solution 2: Hash Set ──────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Hash Set (Clearest Intent)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A cycle means we visit the same value twice. The simplest way to detect a revisit: remember every value we've seen. As we apply the transformation, if we encounter a value in our 'seen' set — it's a cycle. If we reach 1 before that, it's happy."),
        N.h4("What Doesn't Work"),
        N.para("Without tracking seen values, we can't distinguish 'not reached 1 yet' from 'cycling forever'. We'd loop infinitely."),
        N.h4("The Key Observation"),
        N.para("The sequence is bounded (large numbers shrink rapidly) so it must revisit a value in O(log n) steps. Storing all visited values is O(log n) space — acceptable, just not optimal."),
        N.h4("Building the Solution"),
        N.para("Maintain a set 'seen'. Loop: if n=1, return True; if n in seen, return False (cycle detected); otherwise add n to seen and advance n = digit_sq_sum(n)."),
    ]),
    N.h3("Code"),
    N.code(
        "def isHappy(n: int) -> bool:\n"
        "    seen = set()\n"
        "    while n != 1 and n not in seen:\n"
        "        seen.add(n)\n"
        "        n = sum(int(d) ** 2 for d in str(n))\n"
        "    return n == 1"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("seen = set()", {"code": True}), " — Set to record every value we compute. If we see a repeat, we know we're in a cycle."])),
    N.para(N.rich([("while n != 1 and n not in seen:", {"code": True}), " — Two exit conditions: reached 1 (happy) or seen before (cycle, not happy)."])),
    N.para(N.rich([("n = sum(int(d)**2 for d in str(n))", {"code": True}), " — Pythonic digit-square-sum: convert to string, take each char as int, square, sum. Equivalent to the divmod approach."])),
    N.para(N.rich([("return n == 1", {"code": True}), " — After the loop: if n=1 we exited because happy; otherwise we exited because n was in 'seen' (cycle)."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Floyd's Fast-Slow (Interview Pick)", "O(log n)", "O(1)"],
        ["Hash Set", "O(log n)", "O(log n)"],
        ["Hardcode Known Cycle", "O(log n)", "O(1)"],
    ]),
    N.para(N.rich([
        ("Why O(log n)?", {"bold": True}),
        " Large numbers shrink rapidly — a d-digit number maps to at most 81d. Any number with more than 3 digits maps into the sub-1000 range. The 'tail' before entering a cycle or reaching 1 is O(log n) steps. Inside the cycle (length 8), Floyd's needs ≤8 more iterations."
    ])),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Fast-Slow Pointer (Detect Cycle in Sequence)"])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            "Each value in a sequence has exactly one deterministic 'next' value (like a linked list node). The question is 'does the sequence reach a target, or loop forever?' If O(1) space is required, use Floyd's. If space is not a concern, a hash set suffices."
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Floyd's Algorithm Deep-Dive ───────────────────────────────
blocks += [
    N.h2("🔬 Algorithm Deep-Dive: Floyd's Cycle Detection"),
    N.para("Robert W. Floyd invented this in 1967 for the 'rho' problem in number theory, then it became standard for linked list cycle detection. Also called 'tortoise and hare.'"),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        "If a cycle of length L exists, fast gains 1 step on slow per iteration. Within L iterations of both entering the cycle, fast laps slow. They meet at a position inside the cycle."
    ])),
    N.para(N.rich([
        ("For this problem: ", {"bold": True}),
        "Happy numbers have f(1)=1, so 1 is a fixed point. Both pointers reach 1 and trivially meet there. Non-happy numbers enter the 8-element cycle {4,16,37,58,89,145,42,20}; fast catches slow within 8 more steps."
    ])),
    N.code(
        "# Floyd's template for implicit linked list\n"
        "def detect_cycle_or_target(start, next_fn, target):\n"
        "    slow = start\n"
        "    fast = next_fn(start)\n"
        "    while slow != fast:\n"
        "        slow = next_fn(slow)\n"
        "        fast = next_fn(next_fn(fast))\n"
        "    return slow == target  # met at target = no real cycle (or fixed point)"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Fast-Slow Pointer / Detect Cycle):"),
    N.bullet(N.rich([("Linked List Cycle", {"bold": True}), " (Easy) — Classic Floyd's on an actual linked list. Does a cycle exist? (#141)"])),
    N.bullet(N.rich([("Linked List Cycle II", {"bold": True}), " (Medium) — Find the node where the cycle begins (Floyd's phase 2). (#142)"])),
    N.bullet(N.rich([("Find the Duplicate Number", {"bold": True}), " (Medium) — Model array as implicit linked list; Floyd's finds duplicate in O(1) space. (#287)"])),
    N.bullet(N.rich([("Circular Array Loop", {"bold": True}), " (Medium) — Detect cycle in an array where each element points to the next index. (#457)"])),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), " (Easy) — Fast-slow pointers: when fast hits end, slow is at middle. (#876)"])),
    N.para("These problems all share the same core technique: use two pointers at different speeds to detect cycles or find midpoints without extra space."),
    N.divider(),
]

# ── Interactive Explainer Embed ───────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("happy_number")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
