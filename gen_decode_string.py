"""gen_decode_string.py — Notion update for LeetCode #394 Decode String"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-816a-b182-f89998069554"

# ── 1) Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=394,
    pattern="Recursion",
    subpatterns=["Recursive Parsing"],
    tc="O(n·k)",
    sc="O(n)",
    key_insight="Nested brackets form a recursive structure; use two stacks to save/restore context at each depth.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old bulk body ──
n_deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {n_deleted} old blocks.")

# ── 3) Build body ──
STACK_SOL = """\
def decodeString(s: str) -> str:
    k_stack = []          # saved repeat-counts from outer levels
    str_stack = []        # saved partial strings from outer levels
    current_string = ""   # decoded output at current nesting depth
    current_k = 0         # digit accumulator (handles multi-digit k)
    for ch in s:
        if ch.isdigit():
            current_k = current_k * 10 + int(ch)
        elif ch == '[':
            k_stack.append(current_k)
            str_stack.append(current_string)
            current_k = 0
            current_string = ""
        elif ch == ']':
            k = k_stack.pop()
            prev = str_stack.pop()
            current_string = prev + k * current_string
        else:
            current_string += ch
    return current_string"""

RECURSIVE_SOL = """\
def decodeString(s: str) -> str:
    def parse(i: int):
        result = ""
        while i < len(s) and s[i] != ']':
            if s[i].isdigit():
                k = 0
                while i < len(s) and s[i].isdigit():
                    k = k * 10 + int(s[i]); i += 1
                i += 1                     # skip '['
                inner, i = parse(i)        # recurse into bracket
                i += 1                     # skip ']'
                result += k * inner
            else:
                result += s[i]; i += 1
        return result, i
    return parse(0)[0]"""

blocks = []

# ── Problem section ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an encoded string, return its decoded string. The encoding rule is: ",{}),
        ("k[encoded_string]", {"code": True}),
        (", where the ", {}),
        ("encoded_string", {"code": True}),
        (" inside the brackets is repeated exactly ", {}),
        ("k", {"code": True}),
        (" times. You may assume the input string is always valid — no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that all the digits are only for those repeat numbers, k. For example, there won't be input like ", {}),
        ("3a", {"code": True}),
        (" or ", {}),
        ("2[4]", {"code": True}),
        (".", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Stack ──
blocks += [
    N.h2("Solution 1 — Two-Stack Iterative (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to expand compressed notation like 3[abc] → abcabcabc. The tricky part is nesting: 2[a2[b]] means the inner group must be expanded first, then the outer group uses that result."),
        N.h4("What Doesn't Work"),
        N.para("Scanning left-to-right naively and trying to expand each bracket as you find its ']' won't work — by the time you reach ']', you've moved past the 'k' digit that tells you how many times to repeat. You need to remember k across the bracket."),
        N.h4("The Key Observation"),
        N.para("The brackets create a nested recursive structure. When you enter a '[', you need to save your current state (k and the string built so far) and start fresh. When you exit ']', you restore the saved state and expand. This is exactly what a stack does."),
        N.h4("Building the Solution"),
        N.para("Use two stacks: k_stack for repeat counts, str_stack for partial strings. At '[': push current_k and current_string, then reset both to 0 and \"\". At ']': pop k and prev_str, then current_string = prev_str + k * current_string. Letters append directly. Digits accumulate with current_k = current_k * 10 + int(ch) for multi-digit support."),
        N.callout("Analogy: Think of brackets like nested folders. '[' = open a subfolder (save where you were). ']' = close the subfolder and paste its content (repeated) back into the parent.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(STACK_SOL),
    N.h3("Line by Line"),
    N.para(N.rich([("k_stack = []", {"code":True}), " — Stack of repeat-counts saved when we enter each '['. Popped when we hit the matching ']'."])),
    N.para(N.rich([("str_stack = []", {"code":True}), " — Stack of partial strings saved at each nesting depth. Popped and prepended when we expand a bracket group."])),
    N.para(N.rich([("current_string = \"\"", {"code":True}), " — The decoded output being built at the current nesting depth. Reset to \"\" each time we enter a bracket."])),
    N.para(N.rich([("current_k = 0", {"code":True}), " — Digit accumulator. Reset to 0 each time we enter a bracket. Handles multi-digit counts."])),
    N.para(N.rich([("current_k = current_k * 10 + int(ch)", {"code":True}), " — Shift-and-add digit accumulation. Correctly parses '12' as twelve (not 1 then 2)."])),
    N.para(N.rich([("k_stack.append(current_k); str_stack.append(current_string)", {"code":True}), " — Save both pieces of state before diving into the inner bracket."])),
    N.para(N.rich([("current_k = 0; current_string = \"\"", {"code":True}), " — CRITICAL RESET. Without this, the inner level inherits the outer level's state."])),
    N.para(N.rich([("k = k_stack.pop(); prev = str_stack.pop()", {"code":True}), " — Retrieve the repeat count and prefix that belong to the bracket we just closed."])),
    N.para(N.rich([("current_string = prev + k * current_string", {"code":True}), " — The expansion: prefix from outer level + inner content repeated k times."])),
    N.para(N.rich([("current_string += ch", {"code":True}), " — Plain letter: just append. No stack interaction needed."])),
    N.para(N.rich([("return current_string", {"code":True}), " — After all characters processed, this holds the fully decoded string."])),
    N.divider(),
]

# ── Solution 2 — Recursive ──
blocks += [
    N.h2("Solution 2 — Recursive Parser"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each '[...]' group is a self-contained sub-problem. A recursive function that returns (decoded_string, next_index) maps perfectly: call it to decode everything between the current '[' and its matching ']', then the outer call uses that result."),
        N.h4("What Doesn't Work"),
        N.para("Pure string operations (split, replace) can't handle nesting easily because you'd need to process innermost brackets first and the logic becomes error-prone."),
        N.h4("The Key Observation"),
        N.para("A recursive function naturally 'pauses' at ']' (returning) and the caller continues from where the recursion left off. We thread the current index through each call to avoid re-parsing."),
        N.h4("Building the Solution"),
        N.para("parse(i) scans from index i until it hits ']' (or end of string). When it sees a digit, it parses the full number k, skips '[', recurses to get the inner string, skips ']', and appends k * inner. Letters append directly."),
        N.callout("The recursive approach is equivalent to the stack approach — each recursive call IS a stack frame. The stack approach just makes the call stack explicit.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(RECURSIVE_SOL),
    N.h3("Line by Line"),
    N.para(N.rich([("def parse(i):", {"code":True}), " — Recursive helper that decodes from position i until it hits ']' or end. Returns (decoded_string, position_after_last_char)."])),
    N.para(N.rich([("while i < len(s) and s[i] != ']':", {"code":True}), " — Process characters until we hit the matching close bracket (our return signal) or end of input."])),
    N.para(N.rich([("k = k * 10 + int(s[i]); i += 1", {"code":True}), " — Accumulate multi-digit number, advancing i for each digit."])),
    N.para(N.rich([("inner, i = parse(i)", {"code":True}), " — Recursive call: decode everything inside the bracket. Returns the inner decoded string AND the new scan position (right at ']')."])),
    N.para(N.rich([("i += 1", {"code":True}), " (after parse) — Skip the ']' that parse stopped at. Now i points past the bracket group."])),
    N.para(N.rich([("return result, i", {"code":True}), " — Return both the decoded string and the current position so the caller knows where to continue scanning."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two-Stack Iterative", "O(n·k)", "O(d) stacks"],
        ["Recursive Parser", "O(n·k)", "O(d) call stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold":True}), "Recursion"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold":True}), "Recursive Parsing — nested bracket expansion using stack to simulate recursive descent"])),
    N.callout("When to recognize this pattern: balanced nested delimiters (brackets, parentheses); 'decode/expand/evaluate' with nesting; need to save context before entering sub-structure and restore after; expression parsing with depth.", "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Basic Calculator II", {"bold":True}), " (Medium) — Parse arithmetic with +, -, *, / using a stack to handle operator precedence (#227)"])),
    N.bullet(N.rich([("Valid Parentheses", {"bold":True}), " (Easy) — Classic balanced bracket matching — the simplest form of this pattern (#20)"])),
    N.bullet(N.rich([("Number of Atoms", {"bold":True}), " (Hard) — Parse chemical formulas like Fe2(SO4)3 — identical nested expansion with a stack (#726)"])),
    N.bullet(N.rich([("Flatten Nested List Iterator", {"bold":True}), " (Medium) — Recursively unwrap nested lists; same depth-first pattern (#341)"])),
    N.bullet(N.rich([("Mini Parser", {"bold":True}), " (Medium) — Deserialize nested list string with brackets — near-identical stack approach (#385)"])),
    N.bullet(N.rich([("Ternary Expression Parser", {"bold":True}), " (Medium) — Right-to-left stack parse of nested ternary conditions (#439)"])),
    N.para("These problems all share the same core technique: use a stack to save context when entering a nested scope, and restore+combine when exiting."),
]

# ── Interactive Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("decode_string")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic":True, "color":"gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"Total blocks appended: {len(blocks)}")
