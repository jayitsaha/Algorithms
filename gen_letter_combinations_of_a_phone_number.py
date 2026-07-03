"""
gen_letter_combinations_of_a_phone_number.py
Notion in-place update for LeetCode #17 — Letter Combinations of a Phone Number
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8102-8e33-e525f9d292f5"
SLUG = "letter_combinations_of_a_phone_number"


def lbl(code_text, explanation):
    """Helper: bold code snippet + plain explanation."""
    return N.para(N.rich([
        (code_text, {"code": True}),
        (" — " + explanation, {}),
    ]))


# ── 1) Set page properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=17,
    pattern="Backtracking",
    subpatterns=["Digit to Letters Mapping"],
    tc="O(4^n * n)",
    sc="O(n)",
    key_insight="Map each digit to its letters; DFS picks one letter per digit position, enumerating the full Cartesian product.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Rebuild body ───────────────────────────────────────────────────────────
SOLUTION1 = """\
def letterCombinations(digits: str) -> list[str]:
    if not digits: return []          # Edge case: empty input
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi',
        '5': 'jkl', '6': 'mno', '7': 'pqrs',
        '8': 'tuv', '9': 'wxyz'
    }
    result = []

    def backtrack(index, current):
        if index == len(digits):       # Base case: complete combination
            result.append(current)
            return
        for letter in phone[digits[index]]:
            backtrack(index + 1, current + letter)  # No undo needed

    backtrack(0, "")
    return result
"""

SOLUTION2 = """\
from collections import deque

def letterCombinations(digits: str) -> list[str]:
    if not digits: return []
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi',
        '5': 'jkl', '6': 'mno', '7': 'pqrs',
        '8': 'tuv', '9': 'wxyz'
    }
    queue = deque([""])
    for digit in digits:
        for _ in range(len(queue)):   # Expand current layer only
            combo = queue.popleft()
            for letter in phone[digit]:
                queue.append(combo + letter)
    return list(queue)
"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(
        "Given a string digits containing digits from 2-9 inclusive, return all possible "
        "letter combinations that the number could represent on a phone keyboard. "
        "Return the answer in any order.\n\n"
        "Example: digits=\"23\" → [\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]\n"
        "digits=\"\" → []   |   digits=\"2\" → [\"a\",\"b\",\"c\"]"
    ),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Recursive Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We must pick one letter for each digit, independently. With digits='23', "
            "digit 2 gives {a,b,c} and digit 3 gives {d,e,f}. We want every pairing — "
            "the Cartesian product. Building it one position at a time with DFS is backtracking."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Nested loops only work for a fixed number of digits (2 loops for 2 digits, 3 for 3). "
            "We need a general solution for n digits. Iterating over all 4^n strings directly "
            "is awkward without a recursive framework."
        ),
        N.h4("The Key Observation"),
        N.para(
            "At each position index, we have a small fixed choice: 3 or 4 letters. "
            "After making that choice, the remaining problem is identical in shape but one digit shorter. "
            "This self-similarity is exactly what recursion models."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Define backtrack(index, current): if index==len(digits) we have a complete combo — append it. "
            "Otherwise, loop through each letter for digits[index], recurse with index+1 and current+letter. "
            "Python string immutability means current is never mutated, so no explicit undo step."
        ),
        N.callout(
            "Analogy: dialing one digit at a time on a T9 phone. Each key press narrows which letters "
            "you could have meant. At the end of the sequence, every possible reading is a leaf of the recursion tree.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION1, "python"),
    N.h3("Line by Line"),
    lbl("if not digits: return []", "Guard: empty input has no combinations. Return immediately before starting recursion."),
    lbl("phone = {...}", "Static lookup table mapping each digit character to its letter string."),
    lbl("result = []", "Shared accumulator that the nested closure will append complete combos to."),
    lbl("def backtrack(index, current):", "Closure captures result, phone, digits. index = digit we're choosing for; current = combo built so far."),
    lbl("if index == len(digits):", "Base case: every digit has been assigned a letter. current is a complete n-character combination."),
    lbl("result.append(current)", "Collect the complete combination into our shared result list."),
    lbl("for letter in phone[digits[index]]:", "Iterate over each possible letter (3 or 4) for the current digit."),
    lbl("backtrack(index+1, current+letter)", "Recurse: advance to next digit, extend the combo. No explicit undo because string concatenation creates a new object."),
    lbl("backtrack(0, \"\")", "Kick off the recursion from digit 0 with an empty combo string."),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Iterative BFS (Queue-based)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of depth-first recursion, process digits left to right, "
            "expanding a layer of partial combinations for each digit. "
            "This is BFS: each level of the queue corresponds to one digit."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Generating all strings up front requires knowing the count in advance. "
            "BFS naturally handles variable-length inputs by expanding one digit at a time."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Start with queue=[\"\"]. For each digit, pop every current partial combo and "
            "push len(phone[digit]) new combos, one per letter. After all digits, the queue "
            "contains only complete combinations."
        ),
        N.h4("Building the Solution"),
        N.para(
            "The 'for _ in range(len(queue))' guard is critical: it ensures we expand only "
            "the current layer, not newly appended elements (which would cause an infinite loop)."
        ),
        N.callout(
            "Trade-off: the queue holds all partial results simultaneously — O(4^n * n) peak memory. "
            "Backtracking only holds the call stack O(n) at any moment. Prefer backtracking in interviews.",
            "⚖️", "gray_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION2, "python"),
    N.h3("Line by Line"),
    lbl("queue = deque([\"\"])", "Seed with one empty partial combo."),
    lbl("for digit in digits:", "Process each digit left to right — one BFS level per digit."),
    lbl("for _ in range(len(queue)):", "Expand exactly the current layer, not new additions. len(queue) evaluated once at loop start."),
    lbl("combo = queue.popleft()", "Take a partial combo of length k (one char per digit processed so far)."),
    lbl("queue.append(combo + letter)", "Extend with each possible letter — produces (k+1)-length combos."),
    lbl("return list(queue)", "After all digits processed, queue holds every complete n-character combination."),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Working Space"],
        ["Backtracking (Interview Pick)", "O(4^n * n)", "O(n) call stack"],
        ["Iterative BFS", "O(4^n * n)", "O(4^n * n) queue"],
    ]),
    N.para(
        "n = len(digits). Both solutions produce O(4^n * n) total output. "
        "The factor of n comes from building strings of length n at each leaf. "
        "For practical inputs (n <= 4) this is at most ~1024 operations."
    ),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Backtracking (combinatorial enumeration)", {})])),
    N.para(N.rich([
        ("Sub-Pattern(s): ", {"bold": True}),
        ("Digit to Letters Mapping — build Cartesian product via DFS, one choice per digit position", {}),
    ])),
    N.callout(
        "When to recognize this pattern: (1) 'Return ALL possible combinations/arrangements'. "
        "(2) Independent choice at each position from a small fixed set. "
        "(3) Want Cartesian product enumeration without hardcoded nested loops. "
        "Signal phrase: 'all possible letter combinations the number could represent'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Backtracking / combinatorial enumeration):"),
    N.bullet(N.rich([
        ("Generate Parentheses", {"bold": True}),
        (" (Medium, #22) — All valid n-pair parenthesis strings; DFS with open/close count constraints", {}),
    ])),
    N.bullet(N.rich([
        ("Combinations", {"bold": True}),
        (" (Medium, #77) — Choose k numbers from 1 to n; backtracking with start index to avoid repeats", {}),
    ])),
    N.bullet(N.rich([
        ("Permutations", {"bold": True}),
        (" (Medium, #46) — All orderings of an array; backtracking with a 'used' boolean array", {}),
    ])),
    N.bullet(N.rich([
        ("Subsets", {"bold": True}),
        (" (Medium, #78) — Power set of an array; include/exclude decision at each element", {}),
    ])),
    N.bullet(N.rich([
        ("Combination Sum", {"bold": True}),
        (" (Medium, #39) — All combos summing to target, values reusable; backtracking with sum pruning", {}),
    ])),
    N.bullet(N.rich([
        ("Word Search", {"bold": True}),
        (" (Medium, #79) — Find word in 2D grid; backtracking on grid positions with visited marks", {}),
    ])),
    N.bullet(N.rich([
        ("Sudoku Solver", {"bold": True}),
        (" (Hard, #37) — Fill sudoku with constraint backtracking; aggressive pruning via row/col/box sets", {}),
    ])),
    N.para(
        "These problems share the core structure: make a choice at each step, recurse to the next "
        "decision point, collect all valid leaf states."
    ),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md — Backtracking section. "
        "Sub-Pattern: Digit to Letters Mapping (Analysis classification).",
        "📚", "gray_background"
    ),
    N.divider(),
]

# ── Interactive Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch the recursion tree unfold as each combination is built and collected.",
         {"italic": True, "color": "gray"}),
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
