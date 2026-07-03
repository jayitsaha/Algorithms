"""
gen_maximum_swap.py — Regenerate Notion page for Maximum Swap (LeetCode #670).
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81ef-946d-c174020cc191"
SLUG = "maximum_swap"

print(f"Step 1: Setting properties on page {PAGE_ID}...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=670,
    pattern="Greedy",
    subpatterns=["Find Rightmost Larger"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Build last[d]=rightmost index; scan left-to-right and swap with rightmost occurrence of the largest available larger digit.",
    icon="🟡"
)
print("Properties set.")

print("Step 2: Wiping old content...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

print("Step 3: Building new body...")
blocks = []

# ── Problem ──────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a non-negative integer ", {}),
        ("num", {"code": True}),
        (", you may swap two digits at most once to get the maximum valued number. Return the maximum valued number you can get.\n\n", {}),
        ("Example 1: ", {"bold": True}), ("num = 2736", {"code": True}), (" → ", {}), ("7236", {"code": True}),
        (" (swap '2' and '7')\n", {}),
        ("Example 2: ", {"bold": True}), ("num = 9973", {"code": True}), (" → ", {}), ("9973", {"code": True}),
        (" (no swap improves it)\n", {}),
        ("Constraints: ", {"bold": True}), ("0 ≤ num ≤ 10^8", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Greedy ──────────────────────────────────
SOL1_CODE = """\
def maximumSwap(num: int) -> int:
    digits = list(str(num))
    last = {int(d): i for i, d in enumerate(digits)}
    for i, d in enumerate(digits):
        for k in range(9, int(d), -1):
            if k in last and last[k] > i:
                digits[i], digits[last[k]] = digits[last[k]], digits[i]
                return int(''.join(digits))
    return num
"""

blocks += [
    N.h2("Solution 1 — Greedy + Last-Occurrence Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You have a number and one swap token. The question is: which two positions should you swap to make the number as large as possible? Rephrased: which digit should move to which position to maximize the leading (most significant) digits?"),
        N.h4("What Doesn't Work"),
        N.para("Trying all O(n²) pairs works for n ≤ 9 digits but requires no insight. For larger inputs or a scalable solution, we need a smarter approach. Also, simply swapping the two largest digits in the number doesn't work — 9999 proves that equal digits give no gain, and 1993 shows you want to bring the 9 to position 0, not swap the two 9s with each other."),
        N.h4("The Key Observation"),
        N.para("Numbers are compared left to right. The leftmost digit dominates all others. If we can place a larger digit at the leftmost improvable position, that single change beats any rearrangement of later digits. So: scan left to right; at the first position where a larger digit exists to the right, perform the swap there. The 'rightmost' occurrence of the best digit is chosen to maximize the benefit in case of ties."),
        N.h4("Building the Solution"),
        N.para("1. Convert num to a digit list.\n2. Build last[d] = rightmost index of digit d (one pass; later indices overwrite earlier ones automatically).\n3. Scan left to right. At each position i, try digits 9, 8, …, digits[i]+1. The first k where last[k] > i gives our swap — execute and return.\n4. If no position triggered a swap, the number is already in non-increasing order (already maximal). Return num."),
        N.callout("Analogy: You have a hand of cards face-down in order. You get one swap. Go from the left: pick up the first card that isn't already the highest available, and swap it with the highest card sitting to its right (take the rightmost if tied). That's your best single trade.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("digits = list(str(num))", {"code": True}), (" — Convert the integer to a list of digit characters: 2736 → ['2','7','3','6']. We need a mutable sequence to swap in place.", {})])),
    N.para(N.rich([("last = {int(d): i for i, d in enumerate(digits)}", {"code": True}), (" — Build the last-occurrence map. Dict comprehension: for each (i, d) pair, map int(d) → i. When the same digit appears multiple times, later i overwrites earlier i → rightmost index is stored automatically. O(n) time.", {})])),
    N.para(N.rich([("for i, d in enumerate(digits):", {"code": True}), (" — Greedy scan left to right. i is the current position, d is the digit character.", {})])),
    N.para(N.rich([("for k in range(9, int(d), -1):", {"code": True}), (" — Try candidate digits from 9 down to int(d)+1. We always try the largest possible improvement first. int(d) converts the char to a number for comparison.", {})])),
    N.para(N.rich([("if k in last and last[k] > i:", {"code": True}), (" — Two conditions: (1) digit k actually appears in the number, (2) its rightmost occurrence is strictly to the right of position i. Both must hold to perform a valid, improving swap.", {})])),
    N.para(N.rich([("digits[i], digits[last[k]] = digits[last[k]], digits[i]", {"code": True}), (" — Swap the current digit with the rightmost occurrence of the larger digit k. Python simultaneous assignment handles this without a temp variable.", {})])),
    N.para(N.rich([("return int(''.join(digits))", {"code": True}), (" — Reconstruct the number from the modified digit list and return. We stop immediately — one swap is all we're allowed.", {})])),
    N.para(N.rich([("return num", {"code": True}), (" — If we scanned all positions and never found an improving swap, the number is already in non-increasing order (e.g., 9731). Return original.", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force ─────────────────────────────
SOL2_CODE = """\
def maximumSwap(num: int) -> int:
    digits = list(str(num))
    best = num
    for i in range(len(digits)):
        for j in range(i + 1, len(digits)):
            digits[i], digits[j] = digits[j], digits[i]   # swap
            best = max(best, int(''.join(digits)))          # update best
            digits[i], digits[j] = digits[j], digits[i]   # undo swap
    return best
"""

blocks += [
    N.h2("Solution 2 — Brute Force: Try All Pairs"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible pair of positions (i, j) with i < j. Swap those two digits, compute the resulting number, and track the maximum. After trying all pairs, return the best result."),
        N.h4("What Doesn't Work Here"),
        N.para("This is O(n²) in the number of digit pairs. For n ≤ 9 (since 10^8 has 9 digits), it's effectively O(81) = O(1) in practice. However, it provides no insight into why a particular swap is optimal — it's mechanical enumeration."),
        N.h4("The Key Observation"),
        N.para("The 'undo' step (swapping back) is crucial: it restores the digit list to its original state after each attempt, so the next pair is evaluated from the original number. Without the undo, subsequent pairs would be evaluated on a modified number."),
        N.h4("Building the Solution"),
        N.para("Two nested loops over all pairs. Swap, evaluate, undo. Time O(n²), Space O(n). Use this as a warm-up solution before deriving the greedy."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("best = num", {"code": True}), (" — Initialize best to the original number (no swap is also a valid option).", {})])),
    N.para(N.rich([("for i in range(len(digits)): for j in range(i+1, ...)", {"code": True}), (" — Try all pairs (i, j) with i < j. No need to try j < i since that's the same swap.", {})])),
    N.para(N.rich([("digits[i], digits[j] = digits[j], digits[i]", {"code": True}), (" — Swap positions i and j.", {})])),
    N.para(N.rich([("best = max(best, int(''.join(digits)))", {"code": True}), (" — Compute the new number and update best if it's larger.", {})])),
    N.para(N.rich([("digits[i], digits[j] = digits[j], digits[i]  # undo", {"code": True}), (" — Restore the original digit order so the next pair is evaluated from the original.", {})])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all pairs)", "O(n²)", "O(n)"],
        ["Greedy + Last-Occurrence Map ✓", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Greedy — locally optimal choice (leftmost improvable position, largest available digit) is globally optimal.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Find Rightmost Larger — precompute last-occurrence map; scan left-to-right and swap with rightmost occurrence of the best larger digit.", {})])),
    N.callout(
        "When to recognize this pattern:\n• 'Maximize a number with at most k digit swaps'\n• 'Which digit should move left to improve the number?'\n• Need rightmost occurrence of something → dict comprehension with enumerate (later entries overwrite earlier ones)\n• Lexicographic comparison of digit sequences → greedy from most significant position",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same greedy digit-manipulation technique:"),
    N.bullet(N.rich([("Next Permutation", {"bold": True}), (" (Medium) — Find rightmost position where a swap improves lexicographic order; same 'rightmost' reasoning (#31)", {})])),
    N.bullet(N.rich([("Largest Number", {"bold": True}), (" (Medium) — Arrange integers to form largest concatenated string; greedy comparator for each pair (#179)", {})])),
    N.bullet(N.rich([("Remove K Digits", {"bold": True}), (" (Medium) — Greedily remove k digits using monotonic stack to minimize the resulting number (#402)", {})])),
    N.bullet(N.rich([("Monotone Increasing Digits", {"bold": True}), (" (Medium) — Greedy right-to-left digit correction to make non-decreasing; rightmost scan same as here (#738)", {})])),
    N.bullet(N.rich([("Create Maximum Number", {"bold": True}), (" (Hard) — Select k digits from two arrays to form largest number; extends Maximum Swap greedy logic (#321)", {})])),
    N.bullet(N.rich([("Maximum Difference Between Increasing Elements", {"bold": True}), (" (Easy) — Track rightmost max/min while scanning; same 'look for best to the right' idea (#2016)", {})])),
    N.para("These problems share the core technique: identify the leftmost position that can be improved, and greedily find the best digit to bring there using a precomputed lookup."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Greedy section. Sub-Pattern: Find Rightmost Larger. Source: Analysis (greedy digit manipulation with last-occurrence map).", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
