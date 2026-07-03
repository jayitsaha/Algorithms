"""Notion regeneration script for Flood Fill (LeetCode #733)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81d8-8655-c9daf6e1fc3b"
SLUG = "flood_fill"

# ── Step 1: Set page properties ──────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=733,
    pattern="Graph Traversal",
    subpatterns=["DFS/BFS from Start"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="DFS from the seed pixel; painting to new color serves as the visited mark — no extra set needed.",
    icon="🟢",
)
print("Properties set.")

# ── Step 2: Wipe old content ──────────────────────────────────────────────
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

# ── Step 3: Build new body blocks ─────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("An image is represented by an ", {}),
        ("m × n", {"bold": True}),
        (" integer grid ", {}),
        ("image", {"code": True}),
        (" where ", {}),
        ("image[i][j]", {"code": True}),
        (" represents the pixel value. You are also given three integers ", {}),
        ("sr", {"code": True}),
        (", ", {}),
        ("sc", {"code": True}),
        (", and ", {}),
        ("color", {"code": True}),
        (". Perform a flood fill on the image starting from pixel (", {}),
        ("sr", {"code": True}),
        (", ", {}),
        ("sc", {"code": True}),
        ("). To perform a flood fill, consider the starting pixel, plus any pixels connected 4-directionally to the starting pixel of the same color as the starting pixel, plus any pixels connected 4-directionally to those pixels (also with the same color), and so on. Replace the color of all of the aforementioned pixels with ", {}),
        ("color", {"code": True}),
        (". Return the modified image.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: DFS Recursive ──────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — DFS Recursive (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of the paint-bucket tool in image editors. You click on a pixel, and the tool floods outward in 4 directions, recoloring every connected pixel that shares the clicked color. It stops where the color changes. We need to implement exactly this behavior."),

        N.h4("What Doesn't Work"),
        N.para("Nested loops alone cannot work — you don't know in advance which pixels are connected. You'd need to check connectivity, which is inherently recursive/iterative in nature. A simple scan of the grid doesn't respect the 4-connectivity constraint."),

        N.h4("The Key Observation"),
        N.para("The image is an implicit graph. Each pixel is a node; 4-directional neighbors are edges. Flood Fill is simply: 'traverse all nodes reachable from the start node that have the same color, and paint them.' This is DFS or BFS by definition."),

        N.h4("Building the Solution"),
        N.para("1) Capture orig = image[sr][sc]. 2) Guard: if orig == color, return early (prevents infinite loop). 3) DFS from (sr, sc): if out of bounds or image[r][c] ≠ orig → return. Otherwise paint image[r][c] = color (this marks it visited!), then recurse into 4 neighbors. 4) Return image."),

        N.callout(
            "Analogy: DFS is like dipping a brush at (sr, sc) and letting paint flow in 4 directions. The paint naturally stops at color boundaries. Painting first = marking the pixel so paint doesn't reflood it.",
            "🧠", "blue_background"
        ),
    ]),

    N.h3("Code"),
    N.code(
        "def floodFill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:\n"
        "    orig = image[sr][sc]\n"
        "    if orig == color:          # CRITICAL: prevents infinite recursion\n"
        "        return image\n"
        "\n"
        "    def dfs(r: int, c: int) -> None:\n"
        "        if r < 0 or r >= len(image):      # row OOB\n"
        "            return\n"
        "        if c < 0 or c >= len(image[0]):   # col OOB\n"
        "            return\n"
        "        if image[r][c] != orig:            # wrong color or already visited\n"
        "            return\n"
        "        image[r][c] = color                # paint = mark visited\n"
        "        dfs(r - 1, c)   # up\n"
        "        dfs(r + 1, c)   # down\n"
        "        dfs(r, c - 1)   # left\n"
        "        dfs(r, c + 1)   # right\n"
        "\n"
        "    dfs(sr, sc)\n"
        "    return image"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("orig = image[sr][sc]", {"code": True}), (" — save the color we're replacing; this is the only color DFS will spread into.", {})])),
    N.para(N.rich([("if orig == color: return image", {"code": True}), (" — CRITICAL early exit. If the seed is already the target color, painting doesn't change values, so the 'visited' check (image[r][c] != orig) never triggers → infinite recursion. Always guard this.", {})])),
    N.para(N.rich([("if r < 0 or r >= len(image): return", {"code": True}), (" — row boundary check. Grid coordinates must stay within [0, rows).", {})])),
    N.para(N.rich([("if c < 0 or c >= len(image[0]): return", {"code": True}), (" — column boundary check. Grid coordinates must stay within [0, cols).", {})])),
    N.para(N.rich([("if image[r][c] != orig: return", {"code": True}), (" — stop if: (a) this is a boundary pixel with a different color, or (b) this pixel was already painted (= visited). Both cases correctly stop spread.", {})])),
    N.para(N.rich([("image[r][c] = color", {"code": True}), (" — paint BEFORE recursing. This is the visited marker. Any neighbor that recurses back here will see the new color ≠ orig and stop immediately — no infinite loop.", {})])),
    N.para(N.rich([("dfs(r-1,c); dfs(r+1,c); dfs(r,c-1); dfs(r,c+1)", {"code": True}), (" — explore all 4 cardinal directions. Order doesn't matter for correctness, only for traversal order.", {})])),
    N.para(N.rich([("return image", {"code": True}), (" — the grid was modified in-place. Just return the reference.", {})])),
    N.divider(),
]

# ── Solution 2: BFS Iterative ──────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — BFS Iterative (Safe for Large Grids)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal as DFS — visit all connected same-color pixels and paint them. BFS visits neighbors level by level instead of depth-first, using an explicit queue rather than the call stack."),

        N.h4("What Doesn't Work (vs DFS)"),
        N.para("Recursive DFS can hit Python's default recursion limit (~1000) on large inputs. A 1000×1000 all-same-color grid would need up to 1,000,000 recursive calls — certain stack overflow. BFS avoids this with an explicit queue."),

        N.h4("The Key Observation"),
        N.para("BFS with a deque is O(m·n) time and space — identical to DFS. The only difference is traversal order: BFS spreads in 'rings' outward from the start, while DFS dives deep first. For Flood Fill, order doesn't matter — all connected pixels must be visited regardless."),

        N.h4("Building the Solution"),
        N.para("1) Same orig == color guard. 2) Paint the seed pixel and enqueue it. 3) While queue is not empty: dequeue (r,c), check all 4 neighbors — if in bounds and orig color, paint them (mark visited) and enqueue them. The paint-before-enqueue prevents double-enqueuing."),

        N.callout("Key detail: paint the pixel BEFORE adding it to the queue, not after dequeuing. If you paint after dequeue, two neighbors could both enqueue the same cell before either processes it.", "⚠️", "yellow_background"),
    ]),

    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "\n"
        "def floodFill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:\n"
        "    orig = image[sr][sc]\n"
        "    if orig == color:\n"
        "        return image\n"
        "\n"
        "    rows, cols = len(image), len(image[0])\n"
        "    image[sr][sc] = color          # paint seed before enqueuing\n"
        "    queue = deque([(sr, sc)])\n"
        "\n"
        "    while queue:\n"
        "        r, c = queue.popleft()\n"
        "        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n"
        "            nr, nc = r + dr, c + dc\n"
        "            if 0 <= nr < rows and 0 <= nc < cols:\n"
        "                if image[nr][nc] == orig:\n"
        "                    image[nr][nc] = color   # paint before enqueue\n"
        "                    queue.append((nr, nc))\n"
        "\n"
        "    return image"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("image[sr][sc] = color; queue = deque([(sr, sc)])", {"code": True}), (" — paint the seed pixel FIRST, then enqueue it. This ensures no other cell enqueues it again.", {})])),
    N.para(N.rich([("r, c = queue.popleft()", {"code": True}), (" — dequeue the next pixel to process. popleft() is O(1) with deque (unlike list.pop(0) which is O(n)).", {})])),
    N.para(N.rich([("for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]", {"code": True}), (" — the 4 cardinal directions encoded as (row-delta, col-delta).", {})])),
    N.para(N.rich([("if image[nr][nc] == orig:", {"code": True}), (" — only enqueue neighbors that still have the original color (unvisited). Already-painted cells have color ≠ orig.", {})])),
    N.para(N.rich([("image[nr][nc] = color; queue.append((nr, nc))", {"code": True}), (" — paint (mark visited) then enqueue. Order is crucial — painting before appending prevents duplicate entries.", {})])),
    N.divider(),
]

# ── Complexity table ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["DFS Recursive (Interview Pick)", "O(m·n)", "O(m·n)", "Cleanest; recursion stack = space"],
        ["BFS Iterative", "O(m·n)", "O(m·n)", "No recursion limit; explicit queue"],
        ["DFS Iterative (explicit stack)", "O(m·n)", "O(m·n)", "DFS order; avoids Python limit"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph Traversal (DFS / BFS on Implicit Grid Graph)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS/BFS from Start — explores a connected region beginning at a seed node, visiting all reachable same-color cells.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Spread from a starting cell to all connected cells'\n"
        "• 'Fill / paint / infect all reachable cells of a given type'\n"
        "• '4-directional (or 8-directional) connectivity on a grid'\n"
        "• Any connected-component marking problem on a 2D grid",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: The visited marker trick (painting = visited) is the key pattern insight. It applies to any in-place graph traversal where the node's value can encode 'visited' state.", {"italic": True})])),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DFS/BFS from Start technique on grids:"),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — Count connected land components; DFS/BFS flood-fill each unvisited island cell (#200)", {})])),
    N.bullet(N.rich([("Max Area of Island", {"bold": True}), (" (Medium) — Same DFS, but track pixel count per component; return maximum (#695)", {})])),
    N.bullet(N.rich([("Pacific Atlantic Water Flow", {"bold": True}), (" (Medium) — Multi-source BFS from two ocean borders; find cells reachable from both (#417)", {})])),
    N.bullet(N.rich([("Surrounded Regions", {"bold": True}), (" (Medium) — DFS from border 'O' cells to mark safe; flip remaining surrounded 'O' to 'X' (#130)", {})])),
    N.bullet(N.rich([("Island Perimeter", {"bold": True}), (" (Easy) — Count exposed edges of the single island using the same 4-dir grid logic (#463)", {})])),
    N.bullet(N.rich([("Rotting Oranges", {"bold": True}), (" (Medium) — Multi-source BFS from all rotten oranges; min time to spread rot through all fresh (#994)", {})])),
    N.bullet(N.rich([("01 Matrix", {"bold": True}), (" (Medium) — BFS from all 0-cells simultaneously to compute min distance for each cell (#542)", {})])),
    N.para("These problems share the core technique: DFS or BFS traversal starting from one or more seed cells on a grid, spreading to connected same-type cells."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph Traversal section · Sub-Pattern: DFS/BFS from Start", "📚", "gray_background"),
]

# ── Interactive Visual Explainer embed ─────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
