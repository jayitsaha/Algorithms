"""gen_range_module.py — Notion page for LeetCode #715 Range Module"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = None  # No existing page — create one

if PAGE_ID is None:
    PAGE_ID = N.create_page("Range Module", 715, "Hard", "🔴")
    print(f"Created page: {PAGE_ID}")

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=715,
    pattern="Design",
    subpatterns=["TreeMap Intervals"],
    tc="O(k log n) per add/remove, O(log n) per query",
    sc="O(n)",
    key_insight="Store non-overlapping intervals in a sorted map (start→end); floor lookup + merge sweep handles all three operations.",
    icon="🔴"
)
print("Properties set.")

# 2) Fresh page — no wipe needed (just created)

# 3) Build body blocks
SLUG = "range_module"
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a data structure that tracks ranges of numbers on a number line. "
         "Implement the RangeModule class with three methods: "),
        ("addRange(left, right)", {"code": True}),
        (" marks every real number in [left, right) as tracked; "),
        ("removeRange(left, right)", {"code": True}),
        (" stops tracking every real number in [left, right); and "),
        ("queryRange(left, right)", {"code": True}),
        (" returns True if every number in [left, right) is currently tracked, "
         "False otherwise. All intervals are half-open: left is included, right is excluded.")
    ])),
    N.divider(),
]

# ── Solution 1 — SortedDict (Interview Pick) ─────────────────────────────
blocks += [
    N.h2("Solution 1 — SortedDict / TreeMap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a dynamic set of non-overlapping, sorted intervals that supports "
               "merge-on-add and split-on-remove. The challenge is finding overlapping "
               "neighbors in O(log n) rather than scanning all n intervals."),
        N.h4("What Doesn't Work"),
        N.para("A plain list: finding overlapping intervals requires O(n) linear scan. "
               "A hash map: no ordering, so floor queries ('which interval contains point x?') "
               "are impossible without scanning all keys. A bitmap: works for small fixed ranges "
               "but uses O(MAX_INT) memory and cannot handle 10^9 range inputs."),
        N.h4("The Key Observation"),
        N.para("We only need to store interval boundaries — not every individual number. "
               "A sorted map keyed by interval start lets us do bisect_right(x)-1 to find the "
               "rightmost interval that starts at or before x. This 'floor query' is the foundation "
               "for all three operations."),
        N.h4("Building the Solution"),
        N.para("addRange: find floor interval (may overlap from left), expand boundaries, then sweep "
               "rightward absorbing any more overlapping intervals. removeRange: find all overlapping "
               "intervals, save left and right tails (portions outside the removal zone), delete "
               "overlapping entries, re-insert tails. queryRange: floor query + single bound check."),
        N.callout(
            "Analogy: Think of it like a street map of covered roads. Adding a road segment "
            "merges with adjacent covered segments. Removing a segment might split a road into "
            "two separate pieces. Querying checks if a stretch is continuously covered.",
            "🗺️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from sortedcontainers import SortedDict\n\n"
        "class RangeModule:\n"
        "    def __init__(self):\n"
        "        self.ranges = SortedDict()  # start -> end\n\n"
        "    def addRange(self, left: int, right: int) -> None:\n"
        "        i = self.ranges.bisect_right(left) - 1\n"
        "        if i >= 0:\n"
        "            s, e = self.ranges.keys()[i], self.ranges.values()[i]\n"
        "            if e >= left:  # left neighbor overlaps or touches\n"
        "                left = s\n"
        "                right = max(right, e)\n"
        "                del self.ranges[s]\n"
        "        while self.ranges:\n"
        "            j = self.ranges.bisect_left(left)\n"
        "            if j >= len(self.ranges):\n"
        "                break\n"
        "            s, e = self.ranges.keys()[j], self.ranges.values()[j]\n"
        "            if s > right:\n"
        "                break\n"
        "            right = max(right, e)\n"
        "            del self.ranges[s]\n"
        "        self.ranges[left] = right\n\n"
        "    def removeRange(self, left: int, right: int) -> None:\n"
        "        i = self.ranges.bisect_right(left) - 1\n"
        "        to_del, save = [], []\n"
        "        start_scan = i if i >= 0 else 0\n"
        "        for j in range(start_scan, len(self.ranges)):\n"
        "            s, e = self.ranges.keys()[j], self.ranges.values()[j]\n"
        "            if s >= right:\n"
        "                break\n"
        "            if e <= left:\n"
        "                continue\n"
        "            to_del.append(s)\n"
        "            if s < left:\n"
        "                save.append((s, left))\n"
        "            if e > right:\n"
        "                save.append((right, e))\n"
        "        for s in to_del:\n"
        "            del self.ranges[s]\n"
        "        for s, e in save:\n"
        "            self.ranges[s] = e\n\n"
        "    def queryRange(self, left: int, right: int) -> bool:\n"
        "        i = self.ranges.bisect_right(left) - 1\n"
        "        if i < 0:\n"
        "            return False\n"
        "        return self.ranges.values()[i] >= right\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("SortedDict()", {"code": True}),
                   " — sorted mapping of start→end; supports O(log n) bisect operations."])),
    N.para(N.rich([("bisect_right(left) - 1", {"code": True}),
                   " — finds the rightmost interval starting AT OR BEFORE left (the 'floor' interval)."])),
    N.para(N.rich([("if e >= left:", {"code": True}),
                   " — the floor interval's end reaches into our new range; it overlaps or touches."])),
    N.para(N.rich([("left = s; right = max(right, e)", {"code": True}),
                   " — expand new range to absorb the left neighbor's boundaries."])),
    N.para(N.rich([("while self.ranges ... s > right: break", {"code": True}),
                   " — sweep rightward, absorbing every interval whose start ≤ right (touching counts)."])),
    N.para(N.rich([("self.ranges[left] = right", {"code": True}),
                   " — insert the fully merged result."])),
    N.para(N.rich([("save.append((s, left))", {"code": True}),
                   " — in removeRange: save the left tail if the overlapping interval started before our removal zone."])),
    N.para(N.rich([("save.append((right, e))", {"code": True}),
                   " — save the right tail if the overlapping interval extends past our removal zone."])),
    N.para(N.rich([("return self.ranges.values()[i] >= right", {"code": True}),
                   " — queryRange: the floor interval must cover all the way to right."])),
    N.divider(),
]

# ── Solution 2 — Sorted List (no external library) ───────────────────────
blocks += [
    N.h2("Solution 2 — Sorted List with bisect (No External Library)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same interval merge/split logic, but using Python's built-in bisect module "
               "on a sorted list of [start, end] pairs instead of SortedDict."),
        N.h4("What Doesn't Work"),
        N.para("Without sortedcontainers, we cannot do O(log n) deletions by key. "
               "List insertion/deletion is O(n) in the worst case due to shifting, "
               "but the logic is simpler and doesn't require an external dependency."),
        N.h4("The Key Observation"),
        N.para("bisect_left([l]) finds the first pair with start >= l. "
               "bisect_right([l]) finds the first pair with start > l. "
               "Combined with index arithmetic, we get the same floor query."),
        N.h4("Building the Solution"),
        N.para("Use list slicing (self.ivs[i:j] = [[nl, nr]]) to atomically replace "
               "a range of absorbed intervals with the merged result. This is O(n) "
               "for shifting but very clean to write."),
    ]),
    N.h3("Code"),
    N.code(
        "import bisect\n\n"
        "class RangeModule:\n"
        "    def __init__(self):\n"
        "        self.ivs = []  # sorted list of [start, end] pairs\n\n"
        "    def addRange(self, l: int, r: int) -> None:\n"
        "        ivs = self.ivs\n"
        "        nl, nr = l, r\n"
        "        i = bisect.bisect_left(ivs, [l])\n"
        "        if i > 0 and ivs[i-1][1] >= l:  # left neighbor overlaps\n"
        "            i -= 1\n"
        "            nl = ivs[i][0]\n"
        "            nr = max(nr, ivs[i][1])\n"
        "        j = i\n"
        "        while j < len(ivs) and ivs[j][0] <= nr:\n"
        "            nr = max(nr, ivs[j][1])\n"
        "            j += 1\n"
        "        self.ivs[i:j] = [[nl, nr]]\n\n"
        "    def removeRange(self, l: int, r: int) -> None:\n"
        "        ivs = self.ivs\n"
        "        i = bisect.bisect_left(ivs, [l])\n"
        "        if i > 0 and ivs[i-1][1] > l:\n"
        "            i -= 1\n"
        "        j, ins = i, []\n"
        "        while j < len(ivs) and ivs[j][0] < r:\n"
        "            s, e = ivs[j]\n"
        "            if s < l: ins.append([s, l])\n"
        "            if e > r: ins.append([r, e])\n"
        "            j += 1\n"
        "        self.ivs[i:j] = ins\n\n"
        "    def queryRange(self, l: int, r: int) -> bool:\n"
        "        ivs = self.ivs\n"
        "        i = bisect.bisect_right(ivs, [l, float('inf')]) - 1\n"
        "        return i >= 0 and ivs[i][1] >= r\n"
    ),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "addRange", "removeRange", "queryRange", "Space"],
        ["SortedDict (Solution 1)", "O(k log n)", "O(k log n)", "O(log n)", "O(n)"],
        ["Sorted List (Solution 2)", "O(n)", "O(n)", "O(log n)", "O(n)"],
    ]),
    N.callout(
        "k = number of intervals absorbed/deleted in a single operation. "
        "In the worst case k=n (one operation merges all intervals), but amortized "
        "each interval is inserted and deleted at most once per operation.",
        "📊", "gray_background"),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "TreeMap Intervals"])),
    N.callout(
        "When to recognize this pattern: 'Design a data structure' + dynamic interval "
        "insert/remove/query + need O(log n) lookup. Key signal: you need a floor query "
        "('find the interval containing point x') — that needs a sorted structure, not a hash. "
        "Java: TreeMap.floorKey() + higherKey(). Python: SortedDict.bisect_right().",
        "🔎", "green_background"),
    N.para(N.rich([
        ("Note: ", {"italic": True}),
        ("TreeMap Intervals is classified under the Design pattern section. "
         "The sub-pattern involves maintaining a sorted map of non-overlapping intervals "
         "with floor-query-based merge/split operations.", {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same TreeMap Intervals technique:"),
]
related = [
    ("My Calendar I", "Medium", "#729 — Add events without double-booking; same sorted map floor-query pattern"),
    ("My Calendar II", "Medium", "#731 — Allow double-booking; track single+double ranges with two interval maps"),
    ("My Calendar III", "Hard", "#732 — Maximum k-booking; difference array or segment tree variant"),
    ("Data Stream as Disjoint Intervals", "Hard", "#352 — Same SortedDict approach: add integers one by one, merge into disjoint intervals"),
    ("Merge Intervals", "Medium", "#56 — One-time static merge; simpler (sort once, no dynamic updates)"),
    ("Insert Interval", "Medium", "#57 — Insert one interval into a sorted non-overlapping list; equivalent to a single addRange call"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([(name, {"bold": True}), f" ({diff}) — {note}"])))

blocks += [
    N.para("These problems share the core technique: sorted interval boundaries + floor query + merge/split sweep."),
    N.callout("📚 Pattern: Design → TreeMap Intervals. "
              "Also appears in: My Calendar series (#729, #731, #732), "
              "Data Stream as Disjoint Intervals (#352).", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# Write status
import json
status_dir = os.path.join(os.path.dirname(__file__), ".status")
os.makedirs(status_dir, exist_ok=True)
html_path = os.path.join(os.path.dirname(__file__), "range_module_explainer.html")
with open(html_path) as f:
    lines = sum(1 for _ in f)

status = {
    "slug": "range_module",
    "html": "OK",
    "notion": "OK",
    "lines": lines,
    "notion_page_id": PAGE_ID,
    "notes": "Created fresh: 7-section HTML explainer + Notion page for #715 Range Module (Hard, Design/TreeMap Intervals)"
}
status_path = os.path.join(status_dir, "range_module.json")
with open(status_path, "w") as f:
    json.dump(status, f, indent=2)

print(f"RESULT range_module | html=OK | notion=OK | lines={lines}")
