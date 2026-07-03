import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-810b-b945-ff636a73fa38"

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=301,
    pattern="Backtracking",
    subpatterns=["BFS or DFS + Pruning"],
    tc="O(n * 2^n)",
    sc="O(n * 2^n)",
    key_insight="BFS by removal count ensures minimum removals; first level with valid strings is the answer.",
    icon="🔴"
)
print("Properties set OK")

# 2) Wipe existing body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# 3) Build body
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string s containing letters, "), ("(", {"code": True}), (" and "), (")", {"code": True}),
        (", remove the "), ("minimum number", {"bold": True}), (" of invalid parentheses to make the input string valid. "
         "Return all possible results in any order. A string is valid if every open paren has a matching close paren "
         "and nesting is correct."),
    ])),
    N.para(N.rich([
        ("Example: "), ('"()())()"', {"code": True}), (" → "),
        ('"()()()"', {"code": True}), (" and "), ('"(())()"', {"code": True}),
        (" (both require exactly 1 removal)"),
    ])),
    N.divider(),
]

# ── Solution 1 BFS ──
blocks += [
    N.h2("Solution 1 — BFS Level-by-Level (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're searching a state space where each state is a string, and edges connect strings "
               "that differ by one removed paren. We want all states at minimum graph distance from the "
               "original that satisfy the 'valid' property."),
        N.h4("What Doesn't Work"),
        N.para("Greedy gives only ONE optimal answer, not all. Naive backtracking (DFS without depth control) "
               "might produce answers at different removal depths, mixing minimum and non-minimum solutions."),
        N.h4("The Key Observation"),
        N.para("BFS processes all states at depth d before depth d+1. The first depth where any valid string "
               "appears is exactly the minimum number of removals. All valid strings at that depth are answers."),
        N.h4("Building the Solution"),
        N.para("Seed BFS with original string. For each level: check validity of each string. If found valid, "
               "set a 'found' flag. When 'found' is True, continue checking current level strings but don't "
               "generate next-level children. Use a visited set to deduplicate identical strings from different "
               "removal orders."),
        N.callout("Analogy: BFS is like widening ripples in water — the first ripple (depth) to reach a valid "
                  "state is guaranteed the shortest. Stop generating new ripples once you find valid states at the current ring.",
                  "🌊", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "def removeInvalidParentheses(s: str):\n"
        "    def is_valid(t):\n"
        "        count = 0\n"
        "        for c in t:\n"
        "            if c == '(':   count += 1\n"
        "            elif c == ')': count -= 1\n"
        "            if count < 0:  return False  # unmatched ')'\n"
        "        return count == 0  # must be fully balanced\n"
        "    queue = deque([s])\n"
        "    visited = {s}\n"
        "    found = False\n"
        "    result = []\n"
        "    while queue:\n"
        "        cur = queue.popleft()\n"
        "        if is_valid(cur):\n"
        "            result.append(cur)\n"
        "            found = True\n"
        "        if found: continue  # don't generate next-level children\n"
        "        for i in range(len(cur)):\n"
        "            if cur[i] not in '()': continue  # never remove letters\n"
        "            nxt = cur[:i] + cur[i+1:]\n"
        "            if nxt not in visited:\n"
        "                visited.add(nxt)\n"
        "                queue.append(nxt)\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("is_valid(t)", {"code": True}), (" — O(n) scan: balance += 1 for '(', -= 1 for ')'. Return False if balance ever < 0 (unmatched ')') or != 0 at end.")])),
    N.para(N.rich([("queue = deque([s])", {"code": True}), (" — BFS starts with the original string. deque gives O(1) popleft.")])),
    N.para(N.rich([("visited = {s}", {"code": True}), (" — deduplication set. Different removal orders can produce identical strings; process each unique string only once.")])),
    N.para(N.rich([("found = False", {"code": True}), (" — flag: have we hit the minimum-removal depth? Once True, we stop generating deeper children.")])),
    N.para(N.rich([("cur = queue.popleft()", {"code": True}), (" — BFS dequeue: processes in FIFO order, guaranteeing level-by-level traversal.")])),
    N.para(N.rich([("if is_valid(cur): result.append(cur); found = True", {"code": True}), (" — If valid, collect it and mark the minimum level.")])),
    N.para(N.rich([("if found: continue", {"code": True}), (" — CRITICAL: skip child generation for current string. 'continue' not 'break' — we still need to check other current-level strings for validity.")])),
    N.para(N.rich([("if cur[i] not in '()': continue", {"code": True}), (" — Only remove parentheses, never letters. Letters are invariant.")])),
    N.para(N.rich([("nxt = cur[:i] + cur[i+1:]", {"code": True}), (" — String slicing to remove position i. O(n) per child.")])),
    N.divider(),
]

# ── Solution 2 DFS ──
blocks += [
    N.h2("Solution 2 — DFS + Budget Pruning (Optimal Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Pre-determine exactly how many '(' and ')' must be removed. Then DFS tries every combination of keeping/skipping characters, pruning branches that exceed the budget or produce structurally invalid paths."),
        N.h4("What Doesn't Work"),
        N.para("Plain DFS without budgets would explore solutions with too many or too few removals, mixing non-minimum answers with minimum ones."),
        N.h4("The Key Observation"),
        N.para("Scan left-to-right: a ')' with no preceding unmatched '(' is excess (right_rem++). Each '(' without a subsequent closing match is excess (left_rem++). These two counts are the exact removal budgets."),
        N.h4("Building the Solution"),
        N.para("DFS with parameters: index, left_rem (budget for '(' removals), right_rem (budget for ')' removals), l_cnt (open parens kept), r_cnt (close parens kept). Prune: skip only the FIRST in a run of consecutive identical parens to avoid duplicate results. Only keep ')' when r_cnt < l_cnt."),
        N.callout("Dedup insight: removing any of '(((' at positions 0,1,2 yields the same string '((' — so only try removing position 0 (first of the run).", "🔑", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def removeInvalidParentheses(s: str):\n"
        "    # Step 1: count exactly how many '(' and ')' are excess\n"
        "    left_rem = right_rem = 0\n"
        "    for c in s:\n"
        "        if c == '(':\n"
        "            left_rem += 1      # tentatively open — may be unmatched\n"
        "        elif c == ')':\n"
        "            if left_rem: left_rem -= 1  # close matches an open\n"
        "            else: right_rem += 1         # no open to match — excess\n"
        "    result = set()\n"
        "    def dfs(idx, l_rem, r_rem, l_cnt, r_cnt, path):\n"
        "        if idx == len(s):\n"
        "            if l_rem == 0 and r_rem == 0 and l_cnt == r_cnt:\n"
        "                result.add(path)   # all excess removed, balanced\n"
        "            return\n"
        "        c = s[idx]\n"
        "        if c not in '()':  # letters: always keep\n"
        "            dfs(idx+1, l_rem, r_rem, l_cnt, r_cnt, path+c)\n"
        "            return\n"
        "        # Option A: skip (remove) — only first in consecutive run\n"
        "        if c == '(' and l_rem > 0 and (idx == 0 or s[idx-1] != '('):\n"
        "            dfs(idx+1, l_rem-1, r_rem, l_cnt, r_cnt, path)\n"
        "        if c == ')' and r_rem > 0 and (idx == 0 or s[idx-1] != ')'):\n"
        "            dfs(idx+1, l_rem, r_rem-1, l_cnt, r_cnt, path)\n"
        "        # Option B: keep the paren\n"
        "        if c == '(':\n"
        "            dfs(idx+1, l_rem, r_rem, l_cnt+1, r_cnt, path+c)\n"
        "        elif r_cnt < l_cnt:  # only keep ')' if there's an unmatched '('\n"
        "            dfs(idx+1, l_rem, r_rem, l_cnt, r_cnt+1, path+c)\n"
        "    dfs(0, left_rem, right_rem, 0, 0, \"\")\n"
        "    return list(result)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("left_rem / right_rem", {"code": True}), (" — One-pass scan counts exactly how many '(' and ')' are unmatched. This is the removal budget.")])),
    N.para(N.rich([("idx == len(s)", {"code": True}), (" — Base case: processed all characters. Check that both budgets hit zero and open count equals close count.")])),
    N.para(N.rich([("if c not in '()'", {"code": True}), (" — Letters are always kept. Skip removal logic entirely.")])),
    N.para(N.rich([("s[idx-1] != '(' condition", {"code": True}), (" — Dedup pruning: only remove the FIRST paren in a consecutive run of identical chars. Prevents exploring equivalent removal subsets.")])),
    N.para(N.rich([("elif r_cnt < l_cnt", {"code": True}), (" — Key validity pruning: only keep ')' when there's an unmatched '(' before it. This prevents paths that would never be valid.")])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS with visited set", "O(n × 2^n)", "O(n × 2^n)"],
        ["DFS + Budget Pruning", "O(2^n) pruned", "O(n) stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Backtracking")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BFS or DFS + Pruning")])),
    N.callout(
        "When to recognize this pattern: 'Remove minimum X to achieve property Y, return ALL solutions' → BFS by removal count. "
        "When you see exhaustive search + minimum cost + all results, BFS naturally combines these. "
        "Also recognize: state space where nodes differ by one local operation (one removal, one swap, one letter change).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS or DFS + Pruning technique:"),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), (" (Easy) — The is_valid() helper from this problem; check one string for balance (#20)")])),
    N.bullet(N.rich([("Generate Parentheses", {"bold": True}), (" (Medium) — DFS with open/close counts to enumerate all n-pair valid strings (#22)")])),
    N.bullet(N.rich([("Minimum Remove to Make Valid Parentheses", {"bold": True}), (" (Medium) — Greedy stack gives ONE optimal answer, not all (#1249)")])),
    N.bullet(N.rich([("Word Ladder", {"bold": True}), (" (Hard) — BFS on string states, each level = one character substitution (#127)")])),
    N.bullet(N.rich([("Expression Add Operators", {"bold": True}), (" (Hard) — DFS backtracking over operator placements in a digit string (#282)")])),
    N.bullet(N.rich([("Restore IP Addresses", {"bold": True}), (" (Medium) — DFS + pruning to enumerate all valid IPs from a digit string (#93)")])),
    N.para("These problems share the same core technique: exhaustive search in a string state space with pruning to avoid non-optimal or invalid branches."),
    N.callout("Reference: Pattern = Backtracking. Sub-Pattern = BFS or DFS + Pruning. Source: Analysis (problem-specific classification for minimum-removal + all-results constraint combination).", "📚", "gray_background"),
]

# ── Interactive Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("remove_invalid_parentheses")),
    N.para(N.rich([("Step through the BFS algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
