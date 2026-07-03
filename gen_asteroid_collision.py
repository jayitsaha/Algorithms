"""
gen_asteroid_collision.py
Notion in-place update for LeetCode #735 Asteroid Collision
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81bf-b8d6-c0337b7a5339"

# ── 1. Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=735,
    pattern="Stacks",
    subpatterns=["Stack Simulation with Rules"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Use a stack of right-movers; when a left-mover arrives, resolve the chain of collisions with a while loop.",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe existing body ──────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── 3. Build body ──────────────────────────────────────────────────────────────
blocks = []

# ─── Problem ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array ", {}),
        ("asteroids", {"code": True}),
        (" of integers. The absolute value is each asteroid's size; the sign is its direction: positive (+) moves right, negative (−) moves left. All asteroids travel at the same speed.\n\n"
         "If two asteroids meet: the smaller one explodes. If both are the same size, both explode. "
         "Two asteroids moving in the same direction never collide.\n\n"
         "Return the state of the asteroids after all collisions.", {})
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ("Input: ", {}),
        ("[5, 10, -5]", {"code": True}),
        (" → Output: ", {}),
        ("[5, 10]", {"code": True}),
        (". -5 meets +10 → 10 wins, -5 explodes.", {})
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ("Input: ", {}),
        ("[8, -8]", {"code": True}),
        (" → Output: ", {}),
        ("[]", {"code": True}),
        (". Tie → both explode.", {})
    ])),
    N.para(N.rich([
        ("Example 3: ", {"bold": True}),
        ("Input: ", {}),
        ("[10, 2, -5]", {"code": True}),
        (" → Output: ", {}),
        ("[10]", {"code": True}),
        (". -5 beats 2 (2 explodes), then +10 beats -5 (−5 explodes).", {})
    ])),
    N.divider()
]

# ─── Solution 1: Optimal (Stack Simulation) ───
SOLUTION_1_CODE = """\
def asteroidCollision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()          # top is smaller → top explodes, current fights on
            elif stack[-1] == -a:
                stack.pop()          # equal sizes → both explode
                alive = False
            else:
                alive = False        # top is larger → current explodes
        if alive:
            stack.append(a)
    return stack"""

blocks += [
    N.h2("Solution 1 — Stack Simulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to model a physical system: asteroids moving left and right, "
            "and only asteroids approaching each other can collide. "
            "Reframe: 'Which right-movers (positives) are still alive when each left-mover (negative) arrives?'"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive O(n²) approach: for each left-mover, scan left through the array to find right-movers. "
            "This is slow. More importantly, one left-mover can destroy multiple right-movers sequentially "
            "(e.g., -100 against [1,2,3] wipes all three) — we need a structure that keeps track of surviving "
            "right-movers and lets us access the most recent one in O(1)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The 'nearest right-mover to the left' is always the most recently added right-mover. "
            "A stack gives O(1) access to the last element. "
            "When a left-mover arrives, it fights stack[-1]. If it wins, it pops and fights stack[-1] again. "
            "This is exactly the 'while loop over a stack' pattern."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1) Push right-movers onto a stack — they're waiting for potential future conflict.\n"
            "2) When a left-mover arrives: while stack top is a right-mover, resolve collision:\n"
            "   - Top smaller: pop (top dies), current lives on to fight the next top.\n"
            "   - Equal: pop top, mark current dead (tie = both die).\n"
            "   - Top larger: mark current dead (current loses).\n"
            "3) If current is still alive after the while loop, push it.\n"
            "4) Return the final stack."
        ),
        N.callout(
            "Analogy: Think of the stack as a 'bouncer line' of rightward-moving asteroids. "
            "Each new left-mover challenges the last bouncer. If it beats them, it challenges the next one. "
            "If it loses, it's gone. The stack represents the remaining bouncers.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — Initialize empty stack to hold surviving asteroids in order."])),
    N.para(N.rich([("for a in asteroids:", {"code": True}), " — Process each asteroid left to right."])),
    N.para(N.rich([("alive = True", {"code": True}), " — Assume current asteroid survives until proven otherwise by a collision."])),
    N.para(N.rich([("while alive and a < 0 and stack and stack[-1] > 0:", {"code": True}),
                   " — Four conditions for a collision: current is alive, current moves left, stack is non-empty, top moves right."])),
    N.para(N.rich([("if stack[-1] < -a:", {"code": True}),
                   " — Top's magnitude is smaller than current's. Note: a<0 so -a is its positive magnitude."])),
    N.para(N.rich([("    stack.pop()", {"code": True}),
                   " — Top explodes. Current survives and the while loop continues — it may fight the new top."])),
    N.para(N.rich([("elif stack[-1] == -a:", {"code": True}), " — Equal magnitudes: mutual destruction."])),
    N.para(N.rich([("    stack.pop(); alive = False", {"code": True}),
                   " — Pop top (it dies) and mark current dead too. Both destroyed. Exit while loop."])),
    N.para(N.rich([("else: alive = False", {"code": True}),
                   " — Top is larger. Current asteroid explodes. Top stays on stack untouched."])),
    N.para(N.rich([("if alive: stack.append(a)", {"code": True}),
                   " — Only push if this asteroid survived. This handles: positive asteroids, and negatives that won all fights."])),
    N.para(N.rich([("return stack", {"code": True}),
                   " — Stack contains all surviving asteroids in their original relative order."])),
    N.divider()
]

# ─── Solution 2: Brute Force ───
SOLUTION_2_CODE = """\
def asteroidCollision(asteroids):
    # Brute force: repeatedly scan for collisions until none remain
    result = list(asteroids)
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(result) - 1:
            a, b = result[i], result[i + 1]
            if a > 0 and b < 0:          # adjacent collision candidate
                if a > -b:
                    result.pop(i + 1)    # b explodes
                    changed = True
                elif a < -b:
                    result.pop(i)        # a explodes
                    changed = True
                else:
                    result.pop(i)        # both explode
                    result.pop(i)
                    changed = True
            else:
                i += 1
    return result"""

blocks += [
    N.h2("Solution 2 — Brute Force (Repeated Scan)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The straightforward approach: simulate the physical collisions directly. "
            "Scan the array for adjacent pairs where a right-mover is immediately left of a left-mover. "
            "Resolve that collision, then scan again (the collision may have created a new adjacent pair)."
        ),
        N.h4("What Doesn't Work (About This Approach)"),
        N.para(
            "This works correctly but is slow. Each outer loop iteration resolves at most one collision, "
            "and we may need O(n) outer iterations for O(n) input. Total: O(n²). "
            "For n=10⁵, that is 10¹⁰ operations — too slow for an interview."
        ),
        N.h4("The Key Observation"),
        N.para(
            "This approach is useful as a reference implementation to verify correctness. "
            "State it as your starting point: 'Here's the brute force O(n²) simulation. "
            "Now let me optimize.' It shows clear thinking and sets up the stack solution."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1) Copy input to a list.\n"
            "2) Repeat: scan left-to-right for adjacent (positive, negative) pair.\n"
            "3) When found: resolve (remove the smaller, or both if equal).\n"
            "4) Mark changed=True and restart from beginning.\n"
            "5) When no collision is found in a full scan, return the list."
        )
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("result = list(asteroids)", {"code": True}), " — Work on a copy; we'll mutate it."])),
    N.para(N.rich([("while changed:", {"code": True}), " — Keep scanning until a full pass finds zero collisions."])),
    N.para(N.rich([("if a > 0 and b < 0:", {"code": True}), " — Only adjacent pair of (right-mover, left-mover) can collide."])),
    N.para(N.rich([("result.pop(...)", {"code": True}), " — Remove the loser. List.pop is O(n) here — another source of slowness."])),
    N.divider()
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (repeated scan)", "O(n²)", "O(n)", "Each outer loop resolves ≥1 collision; up to n loops"],
        ["Stack Simulation (optimal)", "O(n)", "O(n)", "Amortized: each element pushed and popped at most once"]
    ]),
    N.divider()
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack Simulation with Rules"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'The most recently added element of type X may be cancelled by the current element'\n"
        "• 'An element can trigger a cascade of backwards cancellations'\n"
        "• 'Fight the last pending element until you lose or the pool is empty'\n"
        "• Similar to: matching brackets, expression evaluation, removing adjacent duplicates",
        "🔎", "green_background"
    ),
    N.para(
        "Note: 'Stack Simulation with Rules' is the sub-pattern for problems where elements on a stack "
        "interact with incoming elements according to specific rules (unlike the simpler 'Parentheses Matching' "
        "which just does open/close matching). Classified from analysis."
    ),
    N.divider()
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Stack Simulation with Rules):"),
    N.bullet(N.rich([
        ("Remove All Adjacent Duplicates in String", {"bold": True}),
        (" (Easy, #1047) — Stack cancellation: same character meets stack top → both removed. Identical fight-the-top structure.", {})
    ])),
    N.bullet(N.rich([
        ("Valid Parentheses", {"bold": True}),
        (" (Easy, #20) — Classic rule-based stack: opening bracket pushed, closing bracket must match top.", {})
    ])),
    N.bullet(N.rich([
        ("Removing Stars From a String", {"bold": True}),
        (" (Medium, #2390) — Each '*' kills the stack top; if no top, nothing happens. Same 'fight the top' mechanic.", {})
    ])),
    N.bullet(N.rich([
        ("Daily Temperatures", {"bold": True}),
        (" (Medium, #739) — Monotonic stack: a new warmer day pops all cooler days. Chain reaction via while loop.", {})
    ])),
    N.bullet(N.rich([
        ("Next Greater Element I", {"bold": True}),
        (" (Easy, #496) — Monotonic stack; each element pops stack entries it is greater than.", {})
    ])),
    N.bullet(N.rich([
        ("Score of Parentheses", {"bold": True}),
        (" (Medium, #856) — Stack accumulates values as brackets resolve; rule-driven per bracket type.", {})
    ])),
    N.bullet(N.rich([
        ("Largest Rectangle in Histogram", {"bold": True}),
        (" (Hard, #84) — Monotonic stack; every bar pops all taller bars to its right when a smaller one arrives.", {})
    ])),
    N.para("These problems all share the core technique: use a stack to track 'unsettled' elements; use a while loop to resolve chain cancellations with the new arrival."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7 (Stacks & Queues). Sub-Pattern: Stack Simulation with Rules. Source: Analysis.", "📚", "gray_background"),
]

# ─── Embed ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("asteroid_collision")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── 4. Append in chunks ───────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks OK")
print("NOTION OK", PAGE_ID)
