"""
gen_encode_and_decode_strings.py
Regenerate the Notion page for Encode and Decode Strings (#271) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8125-bfca-da9a3471375b"
SLUG = "encode_and_decode_strings"

# ── 1) Set properties ────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=271,
    pattern="Design",
    subpatterns=["Length Prefix or Escape"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Prefix each string with its length + '#' so the decoder counts bytes, never searches for a delimiter.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ─────────────────────────────────────────────────
ENCODE_CODE = '''\
class Codec:
    def encode(self, strs: list[str]) -> str:
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> list[str]:
        result, i = [], 0
        while i < len(s):
            j = s.index('#', i)     # find '#' starting at cursor i
            n = int(s[i:j])         # parse length from digits before '#'
            result.append(s[j+1 : j+1+n])  # slice exactly n chars of data
            i = j + 1 + n          # advance cursor past header + data
        return result
'''

ESCAPE_CODE = '''\
class CodecEscape:
    def encode(self, strs: list[str]) -> str:
        # Escape every '#' in the data as '##'; bare '#' = word boundary
        return "#".join(s.replace('#', '##') for s in strs) + "#"

    def decode(self, s: str) -> list[str]:
        result, current, i = [], [], 0
        while i < len(s):
            if s[i] == '#' and i + 1 < len(s) and s[i+1] == '#':
                current.append('#'); i += 2   # unescape '##' → '#'
            elif s[i] == '#':
                result.append(''.join(current)); current = []; i += 1
            else:
                current.append(s[i]); i += 1
        return result
'''

blocks = []

# ── Problem ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Design an algorithm to encode a list of strings to a single string, "
        "and decode it back to the original list. The encoder and decoder must be "
        "stateless — they communicate only via the encoded string. The strings may "
        "contain any Unicode character including delimiters, so a naïve single-character "
        "delimiter cannot be used. Implement ",
        ("encode(strs: list[str]) -> str", {"code": True}),
        " and ",
        ("decode(s: str) -> list[str]", {"code": True}),
        "."
    ])),
    N.divider(),
]

# ── Solution 1 — Length Prefix ────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Length-Prefix Framing (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to pack multiple strings into one, then unpack them. "
               "The challenge: the strings can contain any character, including "
               "whatever delimiter we might choose. So we cannot rely on searching "
               "for a special character to find word boundaries."),
        N.h4("What Doesn't Work"),
        N.para("Joining with a comma, pipe, or any other single character fails the "
               "moment a string contains that character. Using a non-ASCII sentinel "
               "(e.g., chr(257)) is fragile — the problem allows any Unicode content. "
               "We need a scheme that works regardless of what is inside the strings."),
        N.h4("The Key Observation"),
        N.para("Instead of marking where a word ENDS (which requires a delimiter inside "
               "data), mark how LONG it is (no delimiter inside data needed). Network "
               "protocols call this 'length-prefix framing': store the size before the "
               "payload so the receiver can count bytes, not search for terminators."),
        N.h4("Building the Solution"),
        N.para("Encode: for each string s, emit f\"{len(s)}#{s}\". Join all chunks. "
               "The '#' separates the length digits from the data. Since length fields "
               "contain only digits (0–9), and '#' is not a digit, the decoder can "
               "always unambiguously find where the length ends. "
               "Decode: maintain cursor i. From i, find the next '#' to get j. "
               "Parse s[i:j] as integer n. Slice s[j+1:j+1+n] for the word. "
               "Set i = j+1+n and repeat."),
        N.callout(
            "Analogy: Think of a shipping label. Instead of marking 'this box ends at the red line' "
            "(delimiter), you write 'this box is 42cm tall' (length prefix). "
            "The receiver measures 42cm and knows exactly where the next box starts — "
            "no matter what's inside.",
            "📦", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(ENCODE_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("def encode(self, strs)", {"code": True}),
                   " — takes a list of strings, returns a single encoded string."])),
    N.para(N.rich([("f\"{len(s)}#{s}\"", {"code": True}),
                   " — for each word, emit its character count, a '#' separator, then the raw word. "
                   "The '#' is the boundary between the length field and the data."])),
    N.para(N.rich([('"".join(...)', {"code": True}),
                   " — concatenate all chunks. No separator between chunks needed — "
                   "each chunk is self-delimiting via its length prefix."])),
    N.para(N.rich([("result, i = [], 0", {"code": True}),
                   " — output accumulator and read cursor, both initialized for the decode loop."])),
    N.para(N.rich([("while i < len(s)", {"code": True}),
                   " — continue until every character in the encoded string has been consumed."])),
    N.para(N.rich([("j = s.index('#', i)", {"code": True}),
                   " — find '#' STARTING AT POSITION i (not from 0!). "
                   "This is the most critical line: starting from i ensures we land on the current "
                   "word's separator, not one inside already-decoded data."])),
    N.para(N.rich([("n = int(s[i:j])", {"code": True}),
                   " — the substring from i to j (exclusive) contains only digits. "
                   "Convert to integer: this is the exact character count of the next word."])),
    N.para(N.rich([("result.append(s[j+1 : j+1+n])", {"code": True}),
                   " — slice starting one past '#' (at j+1) for exactly n characters. "
                   "No matter what characters are in the word — commas, hashes, anything — "
                   "we extract exactly the right content by counting."])),
    N.para(N.rich([("i = j + 1 + n", {"code": True}),
                   " — advance cursor past the '#' (j+1) and the n data bytes (+n). "
                   "i now points to the start of the next word's length header."])),
    N.divider(),
]

# ── Solution 2 — Escape Character ─────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Escape Character Encoding"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of making the delimiter rare by prepending length, we can "
               "eliminate ambiguity by escaping the delimiter whenever it appears in data."),
        N.h4("What Doesn't Work"),
        N.para("Using a bare '#' as a delimiter fails when '#' appears in the data. "
               "But if we replace every '#' in the data with '##' first, then a bare '#' "
               "unambiguously marks a word boundary."),
        N.h4("The Key Observation"),
        N.para("This is the same technique used by CSV (escaping quotes inside quoted fields) "
               "and shell escaping. The decoder distinguishes '##' (escaped '#' in data) "
               "from '#' (word boundary) by looking one character ahead."),
        N.h4("Building the Solution"),
        N.para("Encode: replace each '#' in every word with '##'. Then join words with bare '#'. "
               "Add a trailing '#' to mark the end of the last word. "
               "Decode: scan character by character. '##' → append '#' to current word. "
               "Bare '#' → finish current word, start next. Simpler invariant but more "
               "characters to process."),
        N.callout(
            "Analogy: In English text, we use quotation marks around quotes-within-quotes. "
            "The 'escape' makes the inner delimiter look different from the outer delimiter. "
            "Same idea here: '##' means literal '#', bare '#' means 'end of word'.",
            "🔤", "gray_background"
        ),
    ]),
    N.h3("Code"),
    N.code(ESCAPE_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("s.replace('#', '##')", {"code": True}),
                   " — escape every '#' in each word as '##'. After this, no bare '#' "
                   "remains in any word."])),
    N.para(N.rich([("\"#\".join(...) + \"#\"", {"code": True}),
                   " — join with bare '#' as the word delimiter. Trailing '#' marks end of "
                   "the last word (so the decoder knows to flush the final word)."])),
    N.para(N.rich([("if s[i]=='#' and s[i+1]=='#'", {"code": True}),
                   " — detected an escaped hash '##'. Append a single '#' to the current "
                   "word being built, advance i by 2."])),
    N.para(N.rich([("elif s[i]=='#'", {"code": True}),
                   " — bare '#' means word boundary. Flush the accumulated characters as a "
                   "completed word, reset the buffer, advance i by 1."])),
    N.callout(
        "Prefer Length-Prefix in interviews: it is simpler to implement, easier to explain, "
        "and has better performance when words contain many '#' characters (no escaping overhead). "
        "Escape is worth knowing as an alternative for follow-up discussions.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time (encode)", "Time (decode)", "Space"],
        ["Length-Prefix (✓ pick)", "O(S)",          "O(S)",          "O(S)"],
        ["Escape Character",       "O(S)",          "O(S)",          "O(S) worst 2S"],
    ]),
    N.para("S = total characters across all strings. Length-prefix adds O(W · log max_len) "
           "header bytes where W = number of words; in practice 2–4 bytes per word."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Length Prefix or Escape"])),
    N.callout(
        "When to recognize this pattern: "
        "'Serialize/deserialize a list of strings to a single string.' "
        "'Encode records that can contain any character.' "
        "'No safe delimiter exists.' "
        "Any problem where the data content makes delimiter-based splitting unreliable.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related serialization techniques:"),
    N.bullet(N.rich([("Serialize and Deserialize Binary Tree", {"bold": True}),
                     " (Hard) — encode a tree structure to a string; similar challenge of encoding variable-length hierarchical data (#297)"])),
    N.bullet(N.rich([("Serialize and Deserialize BST", {"bold": True}),
                     " (Medium) — exploit BST ordering to decode without null-markers, reducing space (#449)"])),
    N.bullet(N.rich([("Decode String", {"bold": True}),
                     " (Medium) — parse k[encoded_string] format; count-then-content structure mirrors length-prefix (#394)"])),
    N.bullet(N.rich([("String Compression", {"bold": True}),
                     " (Medium) — run-length encoding mixes counts with characters inline, same interleavings challenge (#443)"])),
    N.bullet(N.rich([("Design a File System", {"bold": True}),
                     " (Medium) — store structured path strings as keys; requires reliable delimiter-free parsing (#1166)"])),
    N.bullet(N.rich([("Find the Index of the First Occurrence in a String", {"bold": True}),
                     " (Easy) — substring search; closely related to how we locate '#' in the decode loop (#28)"])),
    N.para("These problems share the core insight: when data can contain any character, "
           "you must encode structure (boundaries, lengths) separately from content."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Design section. "
              "Sub-Pattern: Length Prefix or Escape. Source: Analysis.",
              "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
