import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8159-b240-fdfcc087e719"
SLUG = "find_all_possible_recipes_from_given_supplies"

# ── 1) Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2115,
    pattern="Graph",
    subpatterns=["Topo Sort with Initial Set"],
    tc="O(V+E)",
    sc="O(V+E)",
    key_insight="Build ingredient→recipe DAG; seed Kahn's BFS with all supplies; recipes reaching indegree 0 are makeable.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ── 3) Build body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You have a list of strings ", {}),
        ("recipes", {"code": True}),
        (" and a list of lists ", {}),
        ("ingredients", {"code": True}),
        (" where ", {}),
        ("ingredients[i]", {"code": True}),
        (" is the list of ingredients needed to make ", {}),
        ("recipes[i]", {"code": True}),
        (". A recipe can be used as an ingredient for other recipes. You also have a list of ", {}),
        ("supplies", {"code": True}),
        (" containing all items you initially have an unlimited supply of. Return a list of all recipes you can create. You may return the answer in any order.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Kahn's Topological Sort with Initial Set (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to figure out which recipes can be made given a starting pantry. A recipe is makeable if all its ingredients are either in the pantry OR are themselves makeable recipes. This is exactly a dependency resolution problem — the kind package managers solve every day."),
        N.h4("What Doesn't Work"),
        N.para("Naive approach: for each recipe, check if all ingredients are available; if not, skip it. Repeat until no new recipes are added. This is O(R × V) and re-checks everything on every pass. It also doesn't cleanly handle chains of arbitrary depth."),
        N.h4("The Key Observation"),
        N.para("This is a DAG (directed acyclic graph) dependency problem. An edge from ingredient to recipe means 'ingredient must exist before recipe can be made.' Supplies are the roots of this graph — they have no prerequisites. Kahn's BFS naturally processes nodes in dependency order."),
        N.h4("Building the Solution"),
        N.para("1. Convert supplies to a set. 2. Build graph: for each recipe, add edges ingredient→recipe for every non-supply ingredient. Track indegree (unsatisfied prerequisites) per recipe. 3. Seed BFS queue with all supplies + recipes already at indegree 0. 4. BFS: dequeue item, if recipe add to result, then decrement dependents' indegrees and enqueue any reaching 0. 5. Return result."),
        N.callout("Analogy: Think of it like a factory. Supplies are raw materials arriving at the dock. Recipes are assembly lines. An assembly line starts only when all its inputs arrive. Kahn's BFS models exactly when each line starts, chaining outputs to downstream lines.", "🏭", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kahn's Algorithm"),
    N.para(N.rich([
        ("Kahn's Algorithm ", {"bold": True}),
        ("(Arthur Kahn, 1962) is a BFS-based topological sort for DAGs. It solves 'process nodes only after all prerequisites are done' in O(V+E).", {}),
    ])),
    N.code(
        "# Kahn's Algorithm Template\n"
        "from collections import defaultdict, deque\n"
        "def kahns_topo_sort(n_nodes, edges):\n"
        "    graph = defaultdict(list)  # u -> [v, ...] (u must come before v)\n"
        "    indegree = [0] * n_nodes\n"
        "    for u, v in edges:\n"
        "        graph[u].append(v)\n"
        "        indegree[v] += 1\n"
        "    queue = deque(i for i in range(n_nodes) if indegree[i] == 0)\n"
        "    order = []\n"
        "    while queue:\n"
        "        node = queue.popleft()\n"
        "        order.append(node)\n"
        "        for neighbor in graph[node]:\n"
        "            indegree[neighbor] -= 1\n"
        "            if indegree[neighbor] == 0:\n"
        "                queue.append(neighbor)\n"
        "    return order  # len < n_nodes if cycle exists"
    ),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("Every node in the queue has indegree 0 — all its prerequisites have been processed. Processing a node means removing its outgoing edges, which may bring other nodes to indegree 0. The 'Initial Set' variant seeds the queue with pre-given nodes (supplies) in addition to zero-indegree recipe nodes.", {}),
    ])),
    N.h3("Code"),
    N.code(
        "from collections import defaultdict, deque\n\n"
        "def findAllRecipes(recipes, ingredients, supplies):\n"
        "    supplies_set = set(supplies)        # O(1) lookup\n"
        "    recipe_set = set(recipes)           # O(1) lookup\n"
        "    graph = defaultdict(list)           # ingredient -> [recipes that need it]\n"
        "    indegree = {r: 0 for r in recipes}  # unsatisfied non-supply deps\n\n"
        "    for recipe, ings in zip(recipes, ingredients):\n"
        "        for ing in ings:\n"
        "            if ing not in supplies_set:  # skip if already available\n"
        "                graph[ing].append(recipe)\n"
        "                indegree[recipe] += 1\n\n"
        "    # Seed: all supplies + recipes already at indegree 0\n"
        "    queue = deque(supplies)\n"
        "    for r in recipes:\n"
        "        if indegree[r] == 0:\n"
        "            queue.append(r)\n\n"
        "    result = []\n"
        "    while queue:\n"
        "        item = queue.popleft()\n"
        "        if item in recipe_set:\n"
        "            result.append(item)\n"
        "        for dependent in graph[item]:\n"
        "            indegree[dependent] -= 1\n"
        "            if indegree[dependent] == 0:\n"
        "                queue.append(dependent)\n\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("supplies_set = set(supplies)", {"code": True}), (" — Convert to set for O(1) membership tests. Without this, the inner loop becomes O(S) per ingredient check.", {})])),
    N.para(N.rich([("graph = defaultdict(list)", {"code": True}), (" — Adjacency list. Edge ing→recipe means 'ing must be ready before recipe.' defaultdict avoids KeyError on missing keys.", {})])),
    N.para(N.rich([("indegree = {r: 0 for r in recipes}", {"code": True}), (" — Initialize all recipe indegrees to 0. We only increment for non-supply ingredients.", {})])),
    N.para(N.rich([("if ing not in supplies_set:", {"code": True}), (" — Key optimization. Supply ingredients are already satisfied at t=0, so we don't build edges for them and don't count them toward indegrees.", {})])),
    N.para(N.rich([("graph[ing].append(recipe); indegree[recipe] += 1", {"code": True}), (" — Add edge and increment. This recipe now has one more unsatisfied dependency.", {})])),
    N.para(N.rich([("queue = deque(supplies)", {"code": True}), (" — Seed BFS with all supplies. They are unconditionally available — no prerequisites needed.", {})])),
    N.para(N.rich([("if indegree[r] == 0: queue.append(r)", {"code": True}), (" — Recipes whose only ingredients are supplies are also immediately ready.", {})])),
    N.para(N.rich([("if item in recipe_set: result.append(item)", {"code": True}), (" — Filter: only collect recipes, not supplies. Supplies were given to us, not made by us.", {})])),
    N.para(N.rich([("indegree[dependent] -= 1; if == 0: queue.append", {"code": True}), (" — Propagate availability. Each time an item becomes available, unlock all recipes that were waiting on it.", {})])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — DFS with Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Can I make recipe X? Recursively: can I make all of X's ingredients? If any ingredient is a supply, yes for free. If any ingredient is a recipe, recursively ask if it can be made. Memoize to avoid re-computation."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization re-visits nodes exponentially. Cycles cause infinite recursion without explicit guards."),
        N.h4("The Key Observation"),
        N.para("Setting memo[item] = False before the recursive call acts as both cycle detection AND memoization: if we visit item again mid-DFS, we return False (cycle detected). After resolution, we overwrite with the real result."),
        N.h4("Building the Solution"),
        N.para("Build a ing_map: recipe→ingredients. For each recipe, call can_make(recipe). Inside can_make: base cases for supplies and unknown items. Set memo[item] = False (visiting), then recursively check all ingredients. Update memo to actual result."),
        N.callout("Analogy: Think of it like a recipe book lookup: 'Can I make burger? Needs sandwich. Can I make sandwich? Needs bread. Can I make bread? Needs yeast+flour — both supplies. Yes! So bread=True, sandwich=True, burger=True.' DFS follows this natural lookup chain.", "📖", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def findAllRecipes(recipes, ingredients, supplies):\n"
        "    supply_set = set(supplies)\n"
        "    ing_map = {r: ingredients[i] for i, r in enumerate(recipes)}\n"
        "    memo = {}  # False = visiting (cycle guard) or blocked; True = makeable\n\n"
        "    def can_make(item):\n"
        "        if item in supply_set: return True     # base: it's a supply\n"
        "        if item not in ing_map: return False   # unknown item\n"
        "        if item in memo: return memo[item]     # cached or cycle (False)\n"
        "        memo[item] = False  # mark as 'currently visiting'\n"
        "        result = all(can_make(ing) for ing in ing_map[item])\n"
        "        memo[item] = result\n"
        "        return result\n\n"
        "    return [r for r in recipes if can_make(r)]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("ing_map = {r: ingredients[i] ...}", {"code": True}), (" — Maps recipe name to its ingredient list for O(1) lookup in the recursive function.", {})])),
    N.para(N.rich([("memo = {}", {"code": True}), (" — Dual purpose: memoization cache AND cycle guard. Setting False before recursion means any revisit during the same DFS path returns False (cycle).", {})])),
    N.para(N.rich([("if item not in ing_map: return False", {"code": True}), (" — Item is not a supply and not a recipe — it's an unknown ingredient that can never be obtained. Recipe is blocked.", {})])),
    N.para(N.rich([("memo[item] = False  # mark visiting", {"code": True}), (" — Critical: if a recursive call reaches this item again before it resolves, it returns False (correctly identifies a cycle).", {})])),
    N.para(N.rich([("result = all(can_make(ing) ...)", {"code": True}), (" — ALL ingredients must be makeable. If any returns False, the recipe is blocked.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Kahn's Topological Sort (Interview Pick)", "O(V+E)", "O(V+E)"],
        ["DFS with Memoization", "O(V+E)", "O(V) memo + O(V) stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Topo Sort with Initial Set", {})])),
    N.callout(
        "When to recognize this pattern: 'X requires Y before it can be made/done.' Chain of dependencies. "
        "Some items given for free (initial set). Find which nodes are reachable. "
        "Package managers, build systems, course schedules with some already-completed courses.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [N.h2("🔗 Related Problems"), N.para("Problems using the same technique:")]
related = [
    ("Course Schedule", "Medium", "Detect cycle in course prerequisite graph using Kahn's BFS (#207)"),
    ("Course Schedule II", "Medium", "Return topological order of all courses — Kahn's gives the order directly (#210)"),
    ("Parallel Courses", "Medium", "Min semesters to finish all courses; BFS level-by-level (#1136)"),
    ("Minimum Height Trees", "Medium", "Remove leaves iteratively (Kahn's in reverse) to find centroid(s) (#310)"),
    ("Find Eventual Safe States", "Medium", "Reverse graph + Kahn's: nodes that reach only terminal nodes (#802)"),
    ("Alien Dictionary", "Hard", "Build char-ordering graph from sorted words, then topo sort (#269)"),
    ("Sort Items by Groups Respecting Dependencies", "Hard", "Two-level topo sort: within groups and between groups (#1203)"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff})", {}),
        (f" — {note}", {}),
    ])))
blocks.append(N.para("These problems share the same core technique: model dependencies as directed edges, then use Kahn's BFS to process nodes in topological order."))
blocks.append(N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 17.3 — Topological Sort → Topo Sort with Initial Set", "📚", "gray_background"))

# ── Embed ──
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
print(f"NOTION OK — {len(blocks)} blocks appended to {PAGE_ID}")
