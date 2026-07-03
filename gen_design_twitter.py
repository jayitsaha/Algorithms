"""
Notion page rebuild for Design Twitter (LeetCode #355).
Run from /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81bf-9b1e-da41efff0aa2"

# ── 1. Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=355,
    pattern="Design",
    subpatterns=["Hash Maps + Heap Merge"],
    tc="O(F log F)",
    sc="O(T + U·F)",
    key_insight="getNewsFeed is Merge K Sorted Lists: max-heap lazily merges F sorted tweet histories in O(F log F).",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build blocks ───────────────────────────────────────────────────────

SOLUTION_1_CODE = '''import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.ts = 0                         # global monotonic clock
        self.tweets = defaultdict(list)     # uid -> [(ts, tweetId), ...]
        self.follows = defaultdict(set)     # uid -> {followeeId, ...}

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.ts += 1
        self.tweets[userId].append((self.ts, tweetId))

    def getNewsFeed(self, userId: int) -> list[int]:
        heap = []
        followees = self.follows[userId] | {userId}   # always include self
        for uid in followees:
            if self.tweets[uid]:
                i = len(self.tweets[uid]) - 1
                ts, tid = self.tweets[uid][i]
                heapq.heappush(heap, (-ts, tid, uid, i))
        result = []
        while heap and len(result) < 10:
            neg_ts, tid, uid, i = heapq.heappop(heap)
            result.append(tid)
            if i > 0:
                i -= 1
                ts, tid2 = self.tweets[uid][i]
                heapq.heappush(heap, (-ts, tid2, uid, i))
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].discard(followeeId)  # discard = no KeyError'''

SOLUTION_2_CODE = '''def getNewsFeed_brute(self, userId: int) -> list[int]:
    all_tweets = []
    for uid in self.follows[userId] | {userId}:
        all_tweets.extend(self.tweets[uid])   # collect ALL tweets
    all_tweets.sort(reverse=True)             # sort by timestamp desc: O(T log T)
    return [tid for _, tid in all_tweets[:10]]'''

blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a simplified version of Twitter where users can:\n",{}),
        ("postTweet(userId, tweetId)",{"code":True}),(" — store a new tweet\n",{}),
        ("getNewsFeed(userId)",{"code":True}),(" — return the 10 most recent tweet IDs from the user's feed (own tweets + followees), sorted newest first\n",{}),
        ("follow(followerId, followeeId)",{"code":True}),(" — follow another user\n",{}),
        ("unfollow(followerId, followeeId)",{"code":True}),(" — unfollow another user",{}),
    ])),
    N.divider(),
]

# Solution 1 — Heap Merge
blocks += [
    N.h2("Solution 1 — HashMap + Max-Heap Merge (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Three methods are trivial (O(1) list/set operations). The challenge is getNewsFeed: return the 10 most recent tweets across up to F followed users, sorted newest first, without loading all tweets."),
        N.h4("What Doesn't Work"),
        N.para("Collecting all tweets from all followees and sorting them — O(T log T) per call where T = total tweets. A user following 1000 people each with 10,000 tweets means sorting 10 million tweets for each feed request. Unacceptable."),
        N.h4("The Key Observation"),
        N.para("Each user's tweet list is already sorted by time (we appended in order). Getting a merged result from F sorted lists is exactly the Merge K Sorted Lists problem — solvable with a heap in O(F log F + 10 log F) = O(F log F)."),
        N.h4("Building the Solution"),
        N.para("Seed the heap with the most recent tweet from each followee. Each heap entry stores (−timestamp, tweetId, userId, listIndex) so we know which list to advance. Pop the global newest, emit it, push that user's next tweet. Repeat up to 10 times."),
        N.callout(
            "Analogy: Think of F sorted stacks of newspaper issues (newest on top). A heap lets you always grab the globally newest issue across all stacks, then flip to the next on that same stack.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.ts = 0",{"code":True}),(" — Global monotonic counter. Every postTweet increments it before storing, so timestamps are strictly unique and increasing.",{})])),
    N.para(N.rich([("self.tweets = defaultdict(list)",{"code":True}),(" — Maps userId to a list of (ts, tweetId) tuples. Newest tweet is at the tail (index len−1).",{})])),
    N.para(N.rich([("self.follows = defaultdict(set)",{"code":True}),(" — Maps userId to a set of followeeIds. Sets give O(1) add, discard, and membership test.",{})])),
    N.para(N.rich([("self.ts += 1; self.tweets[userId].append((self.ts, tweetId))",{"code":True}),(" — Increment clock first, then append. Appending to a list is O(1) amortized.",{})])),
    N.para(N.rich([("followees = self.follows[userId] | {userId}",{"code":True}),(" — Set union ensures the user always sees their own tweets even without an explicit self-follow.",{})])),
    N.para(N.rich([("heapq.heappush(heap, (-ts, tid, uid, i))",{"code":True}),(" — Negate ts so Python's min-heap acts as a max-heap on recency. Include uid and i so we can advance the right list later.",{})])),
    N.para(N.rich([("while heap and len(result) < 10",{"code":True}),(" — Drain loop. Stop at 10 results OR when all followees' tweets are exhausted (heap empty).",{})])),
    N.para(N.rich([("neg_ts, tid, uid, i = heapq.heappop(heap)",{"code":True}),(" — Pop the globally most recent tweet.",{})])),
    N.para(N.rich([("if i > 0: heapq.heappush(heap, (-ts, tid2, uid, i-1))",{"code":True}),(" — Lazy advance: only load the next tweet from this user if we need it. Heap stays size ≤ F.",{})])),
    N.para(N.rich([("self.follows[followerId].discard(followeeId)",{"code":True}),(" — discard (not remove) silently no-ops if followeeId not present. Prevents KeyError on invalid unfollows.",{})])),
    N.callout("Time: O(F log F) for getNewsFeed, O(1) for all other operations. Space: O(T + U·F) total.", "⏱️", "gray_background"),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute Force: Collect All, Sort"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Merge multiple tweet lists into one sorted result. The simplest approach: dump everything into one big list and sort."),
        N.h4("What Doesn't Work (at Scale)"),
        N.para("Sorting all T tweets every time getNewsFeed is called costs O(T log T). If T is millions, this fails. But it's correct and easy to code — propose it first to show you can start simple."),
        N.h4("The Key Observation"),
        N.para("Good enough for small inputs. Shows you understand the problem before optimizing. Always propose brute force first in interviews, then offer to optimize."),
        N.h4("Building the Solution"),
        N.para("Collect all (ts, tweetId) tuples from all followees into one list. Sort descending by ts. Return first 10 tweetIds."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("all_tweets.extend(self.tweets[uid])",{"code":True}),(" — Gather ALL (ts, tweetId) pairs from every followee, including self.",{})])),
    N.para(N.rich([("all_tweets.sort(reverse=True)",{"code":True}),(" — Python tuples sort lexicographically; (ts, tweetId) sorts by ts first. reverse=True gives newest first.",{})])),
    N.para(N.rich([("return [tid for _, tid in all_tweets[:10]]",{"code":True}),(" — Extract tweetIds from top 10 (ts, tweetId) pairs.",{})])),
    N.callout("Time: O(T log T) per getNewsFeed where T = total tweets of all followees. Fine for small inputs, unacceptable at scale.", "⚠️", "yellow_background"),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Method", "Brute Force", "Heap Merge (Optimal)"],
        ["postTweet", "O(1)", "O(1)"],
        ["follow / unfollow", "O(1)", "O(1)"],
        ["getNewsFeed", "O(T log T)", "O(F log F)"],
        ["Space (total)", "O(T + U·F)", "O(T + U·F)"],
    ]),
    N.para("T = total tweets stored, F = followees per user, U = number of users. Since F << T in real systems, Heap Merge wins decisively on the hot path."),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold":True}), ("Design (Data Structure Design — combined hash maps + heap)",{})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold":True}), ("Hash Maps + Heap Merge (equivalent to Merge K Sorted Lists pattern applied to a system design context)",{})])),
    N.callout(
        "When to recognize this pattern: any problem that says 'design a system with multiple sorted data streams and return top K globally' — "
        "especially when loading all data upfront is too expensive and you need lazy/on-demand merging.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold":True}), (" (Hard) — The canonical form: same heap-merge pattern on linked list nodes instead of tweet arrays",{})])),
    N.bullet(N.rich([("Find K Pairs with Smallest Sums", {"bold":True}), (" (Medium) — Heap merge over row-sorted 2D pairs; same lazy push-next structure",{})])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold":True}), (" (Easy) — Simpler heap design; maintains min-heap of size K",{})])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold":True}), (" (Medium) — HashMap + heap ranking; same two-structure pattern",{})])),
    N.bullet(N.rich([("LRU Cache", {"bold":True}), (" (Medium) — Classic design: O(1) get/put with doubly linked list + hashmap",{})])),
    N.bullet(N.rich([("Smallest Range Covering Elements from K Lists", {"bold":True}), (" (Hard) — Advanced heap merge; tracks min across K sorted lists simultaneously",{})])),
    N.para("These problems share the same core technique: use a heap to lazily merge multiple sorted sources, advancing only the pointer you just consumed."),
    N.callout("📚 Pattern: Design → Hash Maps + Heap Merge. This is equivalent to the 'Merge K Sorted' sub-pattern applied in a system design context.", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("design_twitter")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic":True,"color":"gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
