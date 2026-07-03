"""
gen_maximum_xor_of_two_numbers_in_an_array.py
Regenerates the Notion page for LeetCode #421 — Maximum XOR of Two Numbers in an Array
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8129-b1bf-cd8d89436414"
SLUG = "maximum_xor_of_two_numbers_in_an_array"

# ── 1) Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=421,
    pattern="Tries",
    subpatterns=["Bit Trie"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Insert all numbers into a bit trie MSB-first; for each number greedily traverse trie choosing opposite bits to maximize XOR.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────────
print("Wiping old page content...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return the maximum result of ", {}),
        ("nums[i] XOR nums[j]", {"code": True}),
        (", where ", {}),
        ("0 ≤ i ≤ j < n", {"code": True}),
        (". Constraints: 1 ≤ n ≤ 3×10⁴, 0 ≤ nums[i] ≤ 2³¹ − 1.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ("nums = [3, 10, 5, 25, 2, 8] → 28 (= 5 XOR 25). ", {}),
            ("5 = 00101, 25 = 11001, XOR = 11100 = 28.", {"code": True}),
        ]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1 — Bit Trie ──
SOLUTION_1_CODE = """\
def findMaximumXOR(nums: list[int]) -> int:
    max_num = max(nums)
    if max_num == 0:
        return 0
    L = max_num.bit_length()   # e.g., 25 (11001) -> L=5

    # Array-based trie: trie[node][bit] = child_node_id
    # 0 means "no child" (root occupies index 0, children start at 1)
    trie = [[0, 0]]

    def insert(num: int) -> None:
        node = 0
        for i in range(L - 1, -1, -1):       # MSB first
            bit = (num >> i) & 1              # extract bit i
            if not trie[node][bit]:           # child missing?
                trie.append([0, 0])           # create new node
                trie[node][bit] = len(trie) - 1
            node = trie[node][bit]            # walk down

    def query(num: int) -> int:
        node, xor_val = 0, 0
        for i in range(L - 1, -1, -1):
            bit = (num >> i) & 1
            want = 1 - bit                    # opposite bit -> XOR bit = 1
            if trie[node][want]:              # can we achieve a 1 here?
                xor_val |= (1 << i)           # set bit i of result
                node = trie[node][want]
            else:
                node = trie[node][bit]        # forced: XOR bit = 0
        return xor_val

    for num in nums:
        insert(num)

    return max(query(num) for num in nums)
"""

blocks += [
    N.h2("Solution 1 — Bit Trie (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to find two numbers in the array whose bitwise XOR is as large as possible. XOR produces 1 when bits differ and 0 when they match — so maximizing XOR means finding two numbers that are as 'opposite' as possible in their binary representation."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all O(n²) pairs and XOR them. For n=3×10⁴, this is 9×10⁸ operations — Time Limit Exceeded. We need a smarter structure."),
        N.h4("The Key Observation"),
        N.para("Greedy works bit-by-bit from MSB to LSB. Bit k is worth 2^k, which exceeds the sum of all lower bits (2^(k-1)+...+1 = 2^k-1). So maximizing higher bits is strictly optimal. For each query number's bit, we need: 'does any number in the array have the OPPOSITE bit here?' A trie answers this in O(1) per bit."),
        N.h4("Building the Solution"),
        N.para("1. Insert all numbers into a bit trie, MSB-first. 2. For each number x, traverse the trie greedily: at each bit level, try to go to the child for (1 - current_bit). If it exists, we get a 1 in the result; otherwise forced to same-bit path. 3. The maximum of all query results is the answer."),
        N.callout("Analogy: Think of the trie as a 'bit mirror'. For any number you hold up, the trie shows you if its perfect complement exists in the array.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Binary Prefix Tree (Bit Trie)"),
    N.para(N.rich([
        ("A ", {}),
        ("Bit Trie", {"bold": True}),
        (" (binary trie / binary prefix tree) stores integers bit-by-bit from MSB to LSB. Each node has at most two children (bit=0, bit=1). Paths from root to depth L represent all distinct L-bit prefixes of the inserted numbers. Invented as a generalization of tries for binary strings; widely used in competitive programming for XOR-related problems.", {}),
    ])),
    N.code("""\
# Core invariant: every number inserted into the trie has a unique path
# from root (bit L-1) to leaf (bit 0). The path for n and m share a
# prefix of length k iff (n >> (L-k)) == (m >> (L-k)).
#
# For XOR maximization: if optimal pair is (a, b) with a XOR b = OPT,
# then when querying for a, at every bit where a and b differ, b's bit
# path exists in the trie (since b was inserted). Greedy always finds it.
#
# Why array-based? Avoids Python object overhead.
# trie = [[0, 0]] means: root at index 0, children at [0]=bit0 child, [1]=bit1 child.
# 0 = no child. New nodes appended: index 1, 2, 3, ...
""", "python"),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("L = max_num.bit_length()", {"code": True}), (" — determines how many bit levels the trie needs. 25→5 bits; 10^9→30 bits.", {})])),
    N.para(N.rich([("trie = [[0, 0]]", {"code": True}), (" — root node at index 0. Each entry [a, b] stores child node IDs for bit=0 and bit=1.", {})])),
    N.para(N.rich([("bit = (num >> i) & 1", {"code": True}), (" — extract bit i: right-shift num by i positions, mask off all but the lowest bit.", {})])),
    N.para(N.rich([("if not trie[node][bit]:", {"code": True}), (" — child missing (ID=0 means null). Create and link new node.", {})])),
    N.para(N.rich([("want = 1 - bit", {"code": True}), (" — the opposite bit. If num's bit is 0, we want to find a number whose bit is 1 (XOR=1).", {})])),
    N.para(N.rich([("xor_val |= (1 << i)", {"code": True}), (" — set bit i of our result to 1. Bitwise OR with 2^i.", {})])),
    N.para(N.rich([("return max(query(num) for num in nums)", {"code": True}), (" — query every number; the best partner might be any other number.", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
SOLUTION_2_CODE = """\
def findMaximumXOR_brute(nums: list[int]) -> int:
    ans = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):    # j >= i so i == j is allowed (XOR with self = 0)
            ans = max(ans, nums[i] ^ nums[j])
    return ans
"""

blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: Why We Start Here", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible pair (i, j) and compute their XOR, keeping a running maximum."),
        N.h4("What Doesn't Work (for large n)"),
        N.para("O(n²) pairs × O(1) XOR operation = O(n²) total. For n = 3×10⁴: 9×10⁸ operations. Python executes ~10⁷ simple ops/sec → ~90 seconds. LeetCode allows ~2 seconds. TLE."),
        N.h4("The Key Observation"),
        N.para("This is correct but too slow. Mention it first in an interview to show you understand the problem, then explain you can reduce to O(n) with a bit trie."),
        N.h4("Building the Solution"),
        N.para("Straightforward double loop. Start j=i not j=0 because XOR is symmetric (a^b = b^a) and to avoid counting pairs twice (though it wouldn't change the max)."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("for j in range(i, len(nums)):", {"code": True}), (" — j starts at i so the pair (i, i) is included (gives 0, which never beats a real pair unless all zeros).", {})])),
    N.para(N.rich([("nums[i] ^ nums[j]", {"code": True}), (" — XOR operator in Python. O(1) per pair.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Bit Trie (optimal)", "O(n × L) = O(n)", "O(n × L) = O(n)"],
    ]),
    N.para("L = bit_length of max element ≤ 31 for 32-bit integers — treated as a constant. Trie stores at most n × L nodes total."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Tries (Binary Prefix Tree)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Bit Trie — store integers bit-by-bit MSB-first; greedy opposite-bit traversal for XOR maximization", {})])),
    N.callout(
        "When to recognize this pattern: Problem asks 'maximize/minimize XOR of two elements' or 'for each query, find element with max XOR'; binary search for prefix match; need to answer 'does a number with this binary prefix exist?' in sub-linear time per query.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Bit Trie / XOR optimization):"),
    N.bullet(N.rich([("Maximum XOR With an Element From Array", {"bold": True}), (" (Hard) — Offline queries with upper bound constraint; sort queries + trie (#1707)", {})])),
    N.bullet(N.rich([("Maximum XOR of Two Non-Overlapping Subtrees", {"bold": True}), (" (Hard) — Tree DP for subtree XOR sums, then query trie (#2479)", {})])),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), (" (Medium) — Build the core trie data structure from scratch (#208)", {})])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), (" (Hard) — Trie + DFS backtracking on a character grid (#212)", {})])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), (" (Medium) — Trie to find shortest matching prefix in a sentence (#648)", {})])),
    N.bullet(N.rich([("Maximum XOR for Each Query", {"bold": True}), (" (Medium) — Bitwise complement thinking on prefix XOR (#1829)", {})])),
    N.para("These problems share the core technique: store binary prefixes in a trie; exploit trie structure for O(bits) per query."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Tries section. Sub-Pattern: Bit Trie. Source: Analysis (Bit Trie for XOR maximization is a canonical technique, not explicitly listed in guide).", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
