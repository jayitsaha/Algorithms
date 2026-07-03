"""
gen_exclusive_time_of_functions.py
Regenerates the Notion page for Exclusive Time of Functions (LC #636) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81cf-bb1a-c67682764f24"
SLUG = "exclusive_time_of_functions"

# ── 1. Set page properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=636,
    pattern="Stacks",
    subpatterns=["Stack + Time Tracking"],
    tc="O(m)",
    sc="O(n)",
    key_insight="Use a stack + prev bookmark: credit elapsed time to current runner at every start/end event; +1 on end (inclusive timestamp).",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Rebuild body ──────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given ", {}),
        ("n", {"code": True}),
        (" functions and their execution logs as a list of strings in the format ",{}),
        ('"fn_id:type:timestamp"', {"code": True}),
        (", compute the exclusive execution time of each function. A function's exclusive time is the time it spent running WITHOUT being interrupted by a callee. Functions can interrupt each other — when function B starts while A is running, A pauses and B runs exclusively.", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("n=2, logs=[\"0:start:0\",\"1:start:2\",\"1:end:5\",\"0:end:6\"] → ", {}),
        ("[3, 4]", {"code": True}),
        (". fn0 ran at t=0,1 and t=6 (3 units); fn1 ran at t=2,3,4,5 (4 units).", {})
    ])),
    N.divider(),
]

# Solution 1 — Stack + Previous Timestamp (Optimal)
blocks += [
    N.h2("Solution 1 — Stack + Previous Timestamp (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have nested start/end events and need to partition total CPU time among functions. Which function 'owns' any given time unit? The one currently running — i.e., the most recently started but not yet ended function. This is LIFO order: the last one to start is the first to end."),
        N.h4("What Doesn't Work"),
        N.para("Simulating every time unit (brute force): if timestamps can be up to 10^9, we'd loop billions of times. We need to jump directly between events and compute elapsed time mathematically."),
        N.h4("The Key Observation"),
        N.para("At each event (start or end), we know the PREVIOUS event's timestamp (stored in prev). The interval [prev, ts-1] or [prev, ts] belongs entirely to whoever is currently on top of the stack. So at every event: credit the current runner for that interval, then update the stack and prev."),
        N.h4("Building the Solution"),
        N.para("1. Maintain a stack of active function IDs (call hierarchy).\n2. Track prev = the first unaccounted time unit.\n3. On start at ts: credit top-of-stack for ts-prev units (start ts belongs to new fn). Push new fn, set prev=ts.\n4. On end at ts: credit top for ts-prev+1 units (end ts is inclusive). Pop, set prev=ts+1."),
        N.callout("Analogy: prev is like a parking meter receipt. Every time you pull in or out, you settle the elapsed cost for whoever was parked. The +1 on end events accounts for the current hour still being billed.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def exclusiveTime(n: int, logs: list[str]) -> list[int]:
    result = [0] * n   # exclusive time accumulator for each function
    stack = []         # call stack: fn_ids of currently "running" functions
    prev = 0           # last settled timestamp (first unaccounted unit)

    for log in logs:
        fn_id, log_type, ts = log.split(":")
        fn_id, ts = int(fn_id), int(ts)

        if log_type == "start":
            if stack:
                # Credit current runner: it ran from prev to ts-1 (ts belongs to new fn)
                result[stack[-1]] += ts - prev
            stack.append(fn_id)
            prev = ts           # new fn owns from ts onward
        else:  # "end"
            # Credit ending fn: it ran from prev through ts (inclusive)
            result[stack.pop()] += ts - prev + 1
            prev = ts + 1       # next fn resumes from the unit AFTER this end

    return result"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("result = [0] * n", {"code": True}), (" — Output array. Each index stores exclusive time for that function ID.", {})])),
    N.para(N.rich([("stack = []", {"code": True}), (" — Call stack storing function IDs. Top-of-stack is the currently active function.", {})])),
    N.para(N.rich([("prev = 0", {"code": True}), (" — The 'last accounting checkpoint'. All time before prev has been credited. The current runner accumulates from prev onward.", {})])),
    N.para(N.rich([("fn_id, log_type, ts = log.split(':')", {"code": True}), (" — Split each log string into its three components.", {})])),
    N.para(N.rich([("fn_id, ts = int(fn_id), int(ts)", {"code": True}), (" — Convert string IDs and timestamps to integers for arithmetic.", {})])),
    N.para(N.rich([("if stack: result[stack[-1]] += ts - prev", {"code": True}), (" — On start: if something is running, credit it for ts-prev units. No +1: the start timestamp ts belongs to the NEW function, not the current one.", {})])),
    N.para(N.rich([("stack.append(fn_id)", {"code": True}), (" — Push the new function. It is now the active runner.", {})])),
    N.para(N.rich([("prev = ts", {"code": True}), (" — New function's accounting starts at ts.", {})])),
    N.para(N.rich([("result[stack.pop()] += ts - prev + 1", {"code": True}), (" — On end: pop the finishing function and credit it ts-prev+1 units. The +1 is essential: the end timestamp is the LAST unit the function owns (inclusive).", {})])),
    N.para(N.rich([("prev = ts + 1", {"code": True}), (" — After an end, the next segment starts from ts+1. If we set prev=ts instead, unit ts would be double-counted in the next accounting.", {})])),
    N.callout(
        "Off-by-one rule: START events use ts-prev (no +1). END events use ts-prev+1 (+1). After END, prev=ts+1. Verify: fn starts at t=2, ends at t=5 → 5-2+1=4 units (t=2,3,4,5). ✓",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute Force (Per-Unit Simulation)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For every time unit from 0 to max_timestamp, determine which function is running and increment its counter."),
        N.h4("What Doesn't Work"),
        N.para("This is conceptually simple but O(T) where T can be up to 10^9 — way too slow. It's useful for correctness verification on small inputs."),
        N.h4("The Key Observation"),
        N.para("The stack approach computes the same result but skips directly between events instead of stepping one unit at a time."),
        N.h4("Building the Solution"),
        N.para("Track the active function at each unit. When start event: push to running stack. When end event: pop. Credit the function on top for each unit it appears."),
    ]),
    N.h3("Code"),
    N.code(
"""# Conceptual only — too slow for large timestamps
def exclusiveTime_brute(n: int, logs: list[str]) -> list[int]:
    result = [0] * n
    active = []  # stack: active functions over time
    events = {}

    for log in logs:
        fn_id, log_type, ts = log.split(":")
        events.setdefault(int(ts), []).append((log_type, int(fn_id)))

    # Walk every unit (only works if max_ts is small)
    max_ts = max(events)
    for t in range(max_ts + 1):
        if t in events:
            for typ, fn in sorted(events[t], key=lambda x: x[0] == 'start', reverse=True):
                if typ == 'start':
                    active.append(fn)
                else:
                    active.pop()
                    result[fn] += 1
                    continue
        if active:
            result[active[-1]] += 1

    return result"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("This approach", {"bold": True}), (" iterates every time unit and uses a stack to track the active function. O(T) time — unsuitable for large timestamps but illustrates correctness.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Stack + prev (optimal)", "O(m) — m=log entries", "O(n+d) — n result, d stack depth"],
        ["Brute Force", "O(T) — T=max timestamp", "O(n+d)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stacks", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Stack + Time Tracking", {})])),
    N.callout(
        "When to recognize this pattern: Functions/processes that interrupt each other (LIFO resume order) → call stack. 'Exclusive' time per entity → credit elapsed time at every stack transition. Start/end event logs with nested structure → push on start, pop on end. Any problem where LIFO determines ownership of a shared resource.",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: ", {"italic": True}), ("Stack + Time Tracking is a problem-specific sub-pattern refined from the general Stack pattern. The key technique (prev bookmark + +1 on end events) is specific to this class of interval-credit problems.", {"italic": True})])),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related Stack technique:"),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), (" (Easy) — Classic stack push/pop for matching balanced brackets (#20)", {})])),
    N.bullet(N.rich([("Minimum Remove to Make Valid Parentheses", {"bold": True}), (" (Medium) — Stack tracks indices of unmatched brackets (#1249)", {})])),
    N.bullet(N.rich([("Flatten Nested List Iterator", {"bold": True}), (" (Medium) — Stack-based lazy traversal of nested structure (#341)", {})])),
    N.bullet(N.rich([("Remove All Adjacent Duplicates in String II", {"bold": True}), (" (Medium) — Stack stores (char, count) pairs; credit on pop — same deferred-credit pattern (#1209)", {})])),
    N.bullet(N.rich([("Basic Calculator II", {"bold": True}), (" (Medium) — Stack manages deferred operations; analogous to paused callers resuming (#227)", {})])),
    N.bullet(N.rich([("Number of Visible People in a Queue", {"bold": True}), (" (Hard) — Monotonic stack for computing 'line of sight' with time-tracking analog (#1944)", {})])),
    N.para("These problems share the core technique: a stack maintains LIFO ownership of a resource, and accounting happens at each push/pop transition."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stacks section. Sub-Pattern: Stack + Time Tracking · Source: Analysis", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4. Append all blocks ─────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
