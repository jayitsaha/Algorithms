"""
gen_logger_rate_limiter.py — Notion in-place update for Logger Rate Limiter (#359)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8109-a524-cb39066d5695"

# ── 1) Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=359,
    pattern="Design",
    subpatterns=["Hash Map Timestamp"],
    tc="O(1)",
    sc="O(n)",
    key_insight="Store message→last_allowed_timestamp; only update on True, never on deny.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old content ─────────────────────────────────────────────────────────
print("Wiping old blocks...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ── 3) Build body blocks ────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a logger system that receives a stream of messages along with their timestamps. Each unique message should only be printed at most once every 10 seconds. Given a message and a timestamp (in seconds), return "),
        ("True", {"bold": True}),
        (" if the message should be printed, "),
        ("False", {"bold": True}),
        (" otherwise. Implement the "),
        ("Logger", {"code": True}),
        (" class with: "),
        ("Logger()", {"code": True}),
        (" initializes the object; "),
        ("shouldPrint(timestamp, message)", {"code": True}),
        (" returns True if the message should be printed based on the rate-limit rule."),
    ])),
    N.divider(),
]

# Solution 1 — Hash Map Timestamp (Interview Pick)
SOLUTION1_CODE = '''\
class Logger:
    def __init__(self):
        self.log = {}   # message -> last_allowed_timestamp

    def shouldPrint(self, timestamp: int, message: str) -> bool:
        # Deny: message seen and still within 10-second cooldown
        if message in self.log and timestamp - self.log[message] < 10:
            return False
        # Allow: new message OR cooldown expired; reset the clock
        self.log[message] = timestamp
        return True
'''

blocks += [
    N.h2("Solution 1 — Hash Map Timestamp (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For every incoming (timestamp, message) pair, we need to answer: 'Has this exact message been printed within the last 10 seconds?' The minimum state needed per message is exactly one number: when was it last printed."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force approach stores all (timestamp, message) pairs and scans the full list on each query — O(n) per call, where n grows with every request. In a high-throughput logging system, this degrades to seconds of latency per query."),
        N.h4("The Key Observation"),
        N.para("For each unique message, only the MOST RECENT allowed timestamp matters. Earlier allowed timestamps are irrelevant — whether I was allowed at t=1 and t=11 doesn't matter once I've been allowed at t=11. This telescopes: one timestamp per unique message is all we need."),
        N.h4("Building the Solution"),
        N.para("Use a hash map: self.log = {}. On each call, look up the message in O(1). If absent: allow it, store timestamp. If present: check timestamp - self.log[message] >= 10. If so: allow, update. If not: deny WITHOUT updating. The update rule (only on allow) is the critical invariant."),
        N.callout(
            "Analogy: A nightclub with a 10-minute re-entry rule. The bouncer keeps a ledger of LAST ENTRY time for each patron. When they try to re-enter, the bouncer checks elapsed time. If denied, the ledger does not update — the clock stays anchored to the last successful entry.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.log = {}", {"code": True}), " — Initialize an empty dictionary. Maps message string → timestamp of last successful (allowed) print. Empty at construction."])),
    N.para(N.rich([("if message in self.log", {"code": True}), " — O(1) average-case hash map lookup. If the message has never been seen, skip to the allow branch."])),
    N.para(N.rich([("timestamp - self.log[message] < 10", {"code": True}), " — Compute elapsed time since last allowed print. If < 10 seconds, the cooldown is still active."])),
    N.para(N.rich([("return False", {"code": True}), " — Suppress the message. Critically, we do NOT touch self.log here — the stored timestamp must remain anchored to the last TRUE return."])),
    N.para(N.rich([("self.log[message] = timestamp", {"code": True}), " — Reset the cooldown clock: record this timestamp as the new 'last allowed time' for this message. Covers both new messages and expired cooldowns."])),
    N.para(N.rich([("return True", {"code": True}), " — Allow the print. Both new message (absent from map) and expired cooldown flow here."])),
    N.divider(),
]

# Solution 2 — Brute Force
SOLUTION2_CODE = '''\
class LoggerBrute:
    def __init__(self):
        self.calls = []  # all (timestamp, message) pairs ever received

    def shouldPrint(self, timestamp: int, message: str) -> bool:
        # Scan ALL history for a recent matching message
        for ts, msg in self.calls:
            if msg == message and timestamp - ts < 10:
                return False
        self.calls.append((timestamp, message))  # log every call
        return True
'''

blocks += [
    N.h2("Solution 2 — Brute Force (List Scan) · O(n) per call"),
    N.toggle_h3("💡 Intuition: Why Start Here", [
        N.h4("Reframe the Problem"),
        N.para("Keep a complete record of every call. When checking a new message, scan history for any recent occurrence."),
        N.h4("What Doesn't Work"),
        N.para("Storing every call means both memory and query time grow with every request. After 1,000,000 calls, each query scans 1,000,000 records."),
        N.h4("The Key Observation"),
        N.para("This establishes a baseline — correctness without optimization — useful to mention first in interviews before proposing the O(1) hash map approach."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.calls = []", {"code": True}), " — Stores every (timestamp, message) pair received by shouldPrint, growing indefinitely."])),
    N.para(N.rich([("for ts, msg in self.calls:", {"code": True}), " — O(n) linear scan through all historical calls. n = total number of calls made so far."])),
    N.para(N.rich([("if msg == message and timestamp - ts < 10:", {"code": True}), " — Check if this historical record is (a) the same message and (b) within the last 10 seconds."])),
    N.para(N.rich([("self.calls.append(...)", {"code": True}), " — Always log the current call (both allowed and denied) — inefficient, adds noise."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time per Call", "Space"],
        ["Brute Force (list scan)", "O(n) — n total calls", "O(n) — stores all calls"],
        ["Hash Map Timestamp (optimal)", "O(1) average", "O(m) — m unique messages"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Hash Map Timestamp"])),
    N.callout(
        "When to recognize this pattern: A class with persistent state; each query can be answered by one stored value per key; rate-limiting / cooldown / deduplication in time window; O(1) per call expected. Signal: 'print at most once every N seconds' or 'limit to K per window'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Hash Map Timestamp / Design pattern:"),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium) — Persistent-state design; doubly-linked list + hash map for O(1) get/put with eviction"])),
    N.bullet(N.rich([("Time Based Key-Value Store", {"bold": True}), " (Medium) — Hash map + sorted timestamps; binary search for most-recent value at or before given time"])),
    N.bullet(N.rich([("Design Hit Counter", {"bold": True}), " (Medium) — Count hits in past 3000ms; sliding window with monotone deque or circular buffer"])),
    N.bullet(N.rich([("Number of Recent Calls", {"bold": True}), " (Easy) — Count pings in past 3000ms; O(1) amortized with monotone queue"])),
    N.bullet(N.rich([("Design HashMap", {"bold": True}), " (Easy) — Build the underlying data structure used in this solution from scratch"])),
    N.bullet(N.rich([("First Unique Character in a String", {"bold": True}), " (Easy) — Same one-value-per-key frequency map intuition; O(1) query"])),
    N.para("These problems all share the core technique: maintain a minimal per-key state (timestamp, count, or value) in a hash map to answer each query in O(1) without re-scanning history."),
    N.callout("📚 Pattern reference: Design section — Hash Map with Timestamp sub-pattern. Related to Design Hit Counter (sliding window) and LRU Cache (eviction policy).", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("logger_rate_limiter")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append all blocks ────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
