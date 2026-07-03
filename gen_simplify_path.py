"""
gen_simplify_path.py — Regenerate Notion page for LeetCode #71 Simplify Path.
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81da-861d-d2c3b6c23e22"
SLUG = "simplify_path"

# ─────────────────────────────────────────────────
# 1) Set page properties
# ─────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=71,
    pattern="Stacks",
    subpatterns=["Stack for Directory Components"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Split on '/' to tokenize; push real names, pop on '..', skip empty/'.'; join stack with '/' prefix.",
    icon="🟡",
)
print("Properties set.")

# ─────────────────────────────────────────────────
# 2) Wipe old content
# ─────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─────────────────────────────────────────────────
# 3) Build new body
# ─────────────────────────────────────────────────
blocks = []

# ── Problem statement ──────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an absolute path for a Unix file system (a string starting with "),
        ("'/'", {"code": True}),
        ("), convert it to the simplified "),
        ("canonical path", {"bold": True}),
        (". In a Unix filesystem: "),
        (".", {"code": True}),
        (" refers to the current directory; "),
        ("..", {"code": True}),
        (" refers to the parent directory; Multiple consecutive slashes are treated as a single slash. "
         "The canonical path must: always start with '/', not end with '/' (unless it is the root), "
         "not contain '.' or '..', and not contain consecutive slashes."),
    ])),
    N.para(N.rich([
        ("Example 1: "), ("path = \"/home/\"", {"code": True}), (" → "), ("\"/home\"", {"code": True}),
        ("\nExample 2: "), ("path = \"/../\"", {"code": True}), (" → "), ("\"/\"", {"code": True}),
        ("\nExample 3: "), ("path = \"/home//foo/\"", {"code": True}), (" → "), ("\"/home/foo\"", {"code": True}),
        ("\nExample 4: "), ("path = \"/a/./b/../../c/\"", {"code": True}), (" → "), ("\"/c\"", {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1 (Optimal) ───────────────────────
SOLUTION_1_CODE = """\
def simplifyPath(path: str) -> str:
    stack = []
    for token in path.split('/'):
        if token == '..':
            if stack:
                stack.pop()
        elif token and token != '.':
            stack.append(token)
    return '/' + '/'.join(stack)"""

blocks += [
    N.h2("Solution 1 — Stack + Split (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You're navigating a filesystem. You start at root (/). Each component tells you to either descend into a directory, stay put, or go up to the parent. The question is: where do you end up after following all those instructions?"),
        N.h4("What Doesn't Work"),
        N.para("A naive regex-based approach (repeatedly collapsing '/./' and '/name/..') works but runs in O(n²) in the worst case because each pass only resolves one level of nesting. It's also fragile — every edge case (trailing slashes, root boundary, triple dots) needs a separate regex fix."),
        N.h4("The Key Observation"),
        N.para("The current path from root is exactly a stack of directory names. When you descend into a directory, you push its name. When you go up ('..'), you pop the last name. This is a perfect 1-to-1 mapping. The canonical path at any point is simply '/' + '/'.join(stack)."),
        N.h4("Building the Solution"),
        N.para("Split the path on '/' first — this converts a messy string into a clean list of tokens. Consecutive slashes produce empty-string tokens, which we ignore. Single dot tokens are ignored. '..' tokens trigger a pop (if stack is non-empty — can't go above root). Any other token is a real directory name — push it."),
        N.callout(
            "Analogy: Think of the stack as a stack of paper slips on your desk. Each paper is a directory name. Descending (push) adds a slip to the top. Going up (..) removes the top slip. The canonical path is just reading all slips from bottom to top, joined by '/'.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — Initialize an empty list to serve as our directory stack. Each element will be a confirmed directory name."])),
    N.para(N.rich([("for token in path.split('/'):", {"code": True}), " — Split on '/' to produce tokens. Leading '/' creates an empty first token; trailing '/' creates an empty last token; consecutive '//' create extra empty tokens. All are benign."])),
    N.para(N.rich([("if token == '..':", {"code": True}), " — Strict equality check. Only the string \"..\" means 'go up'. The string \"...\" is a valid directory name and does NOT match this branch."])),
    N.para(N.rich([("if stack:", {"code": True}), " — Guard against popping from an empty stack. An empty stack means we're at root, and root has no parent — so '..' at root is a no-op."])),
    N.para(N.rich([("stack.pop()", {"code": True}), " — Remove the most recently entered directory. We've ascended one level."])),
    N.para(N.rich([("elif token and token != '.':", {"code": True}), " — This branch runs when token is NOT '..'. We check: (1) token is truthy (not empty string), (2) token is not '.' (single dot = stay put). Both conditions must hold for a real directory name."])),
    N.para(N.rich([("stack.append(token)", {"code": True}), " — Descend into this directory. Its name is now the deepest level in our canonical path."])),
    N.para(N.rich([("return '/' + '/'.join(stack)", {"code": True}), " — Join all components with '/' and prefix '/'. If stack is empty, this gives '/' + '' = '/', which is the root — correct for cases like '/../'."])),
    N.divider(),
]

# ── Solution 2 (Brute Force) ───────────────────
SOLUTION_2_CODE = """\
import re

def simplifyPath_bruteforce(path: str) -> str:
    # Normalize slashes, then repeatedly collapse . and .. references
    p = path
    while True:
        prev = p
        p = re.sub(r'/+', '/', p)               # collapse multiple slashes
        p = re.sub(r'/\\.(?=/|$)', '', p)        # remove /. (current dir)
        p = re.sub(r'/[^/]+/\\.\\.(?=/|$)', '', p)  # collapse /name/..
        p = re.sub(r'^/\\.\\.', '', p)           # remove .. at root
        if p == prev:
            break
    return p or '/'"""

blocks += [
    N.h2("Solution 2 — Brute Force Regex (Illustrative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of parsing tokens, try to apply the rules as string transformations: collapse double slashes, remove /./patterns, collapse /name/.. patterns."),
        N.h4("What Doesn't Work Well"),
        N.para("Nested '..' patterns require multiple passes. The input '/a/../b/../c' needs one pass to resolve '/a/..' to '' and '/b/..' to '' in sequence. A single-pass regex can't handle arbitrary nesting depth."),
        N.h4("The Key Observation"),
        N.para("Each regex pass only resolves one level of nesting. We need a fixed-point loop: keep applying until no more changes happen. This works but costs O(n) passes × O(n) regex work = O(n²) overall."),
        N.h4("Building the Solution"),
        N.para("Apply four regex substitutions in sequence, repeating until the string stabilizes. This is correct but slower and more fragile than the stack approach."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("re.sub(r'/+', '/', p)", {"code": True}), " — Collapse any run of two or more consecutive slashes into a single slash."])),
    N.para(N.rich([("re.sub(r'/\\.(?=/|$)', '', p)", {"code": True}), " — Remove any '/.' that is followed by another '/' or end of string (current directory reference)."])),
    N.para(N.rich([("re.sub(r'/[^/]+/\\.\\.(?=/|$)', '', p)", {"code": True}), " — Remove any '/name/..' sequence — ascending one level."])),
    N.para(N.rich([("if p == prev: break", {"code": True}), " — Fixed-point detection. If no substitution changed the string, we're done."])),
    N.para(N.rich([("return p or '/'", {"code": True}), " — Edge case: if the entire path normalized to empty string (e.g., root after removing everything), return '/'."])),
    N.divider(),
]

# ── Complexity table ───────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",         "Time",    "Space", "Notes"],
        ["Stack + Split ✓",  "O(n)",    "O(n)",  "Single pass; optimal; handles all edge cases"],
        ["Regex loop",       "O(n²)",   "O(n)",  "Fragile; avoid in interviews"],
    ]),
    N.divider(),
]

# ── Pattern classification ─────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack for Directory Components"])),
    N.callout(
        "When to recognize this pattern: The problem involves navigating a hierarchy where some moves are forward (push) and others undo previous moves (pop). Key signals: filesystem paths with '..' references; backspace/delete characters in strings; undo/redo sequences; bracket matching.",
        "🔎", "green_background"),
    N.divider(),
]

# ── Related problems ───────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Evaluate Reverse Polish Notation", {"bold": True}), " (Medium) — Stack for operands; operators pop two and push result (#150)"])),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Stack for open brackets; closing bracket triggers pop (#20)"])),
    N.bullet(N.rich([("Backspace String Compare", {"bold": True}), " (Easy) — Stack for characters; '#' triggers pop, just like '..' pops here (#844)"])),
    N.bullet(N.rich([("Basic Calculator II", {"bold": True}), " (Medium) — Stack for operands through operator precedence (#227)"])),
    N.bullet(N.rich([("Remove All Adjacent Duplicates In String", {"bold": True}), " (Easy) — Stack where matching char at top triggers a pop (#1047)"])),
    N.bullet(N.rich([("Decode String", {"bold": True}), " (Medium) — Two stacks (counts + strings) for nested bracket expansion (#394)"])),
    N.bullet(N.rich([("Mini Parser", {"bold": True}), " (Medium) — Stack for nested NestedInteger structures; similar token processing (#385)"])),
    N.para("These problems all share the core technique: use a stack where certain tokens 'undo' or 'cancel' the most recent stack entry."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue Patterns section. Sub-Pattern: Stack for Directory Components (confirmed).", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─────────────────────────────────────────────────
# 4) Append blocks
# ─────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
