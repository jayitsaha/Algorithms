"""
reconcile.py — orchestrator-side bookkeeping (only the orchestrator runs this).

- Reads .status/<slug>.json markers written by regeneration agents.
- Flips html_done / notion_done in dsa_problems_queue.json (and work_manifest.json).
- Prints progress + the next N pending problems (compact) for dispatch.

Usage:
    python3 reconcile.py            # reconcile + show summary
    python3 reconcile.py next 16    # reconcile + print next 16 pending as JSON lines
"""
import json, os, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(ROOT, "dsa_problems_queue.json")
MANIFEST = os.path.join(ROOT, "work_manifest.json")
STATUS = os.path.join(ROOT, ".status")


def load(p):
    return json.load(open(p))


def save(p, d):
    json.dump(d, open(p, "w"), indent=2, ensure_ascii=False)


def reconcile():
    queue = load(QUEUE)
    manifest = load(MANIFEST)
    by_slug_q = {x["slug"]: x for x in queue}
    by_slug_m = {x["slug"]: x for x in manifest}
    done_html = done_notion = 0
    fails = []
    for f in glob.glob(os.path.join(STATUS, "*.json")):
        try:
            st = load(f)
        except Exception:
            continue
        slug = st.get("slug") or os.path.splitext(os.path.basename(f))[0]
        h = st.get("html") == "OK"
        n = st.get("notion") == "OK"
        for tbl in (by_slug_q, by_slug_m):
            if slug in tbl:
                tbl[slug]["html_done"] = h
                tbl[slug]["notion_done"] = n
        done_html += h
        done_notion += n
        if not (h and n):
            fails.append((slug, st.get("notes", "")))
    save(QUEUE, queue)
    save(MANIFEST, manifest)
    total = len(queue)
    fully = sum(1 for x in queue if x.get("html_done") and x.get("notion_done"))
    return dict(total=total, fully=fully, done_html=done_html,
                done_notion=done_notion, fails=fails, manifest=manifest)


def pending(manifest, n):
    dispatched = set()
    dp = os.path.join(ROOT, ".dispatched")
    if os.path.exists(dp):
        dispatched = set(l.strip() for l in open(dp) if l.strip())
    out = []
    for x in manifest:
        if x.get("html_done") and x.get("notion_done"):
            continue
        if x["slug"] in dispatched:
            continue
        out.append(x)
        if len(out) >= n:
            break
    return out


if __name__ == "__main__":
    r = reconcile()
    print(f"PROGRESS: {r['fully']}/{r['total']} fully done "
          f"(html={r['done_html']}, notion={r['done_notion']}), "
          f"remaining={r['total']-r['fully']}")
    if r["fails"]:
        print("FAILS:", r["fails"][:20])
    if len(sys.argv) >= 3 and sys.argv[1] == "next":
        n = int(sys.argv[2])
        for x in pending(r["manifest"], n):
            print("PENDING\t" + json.dumps({
                "name": x["name"], "leetcode_number": x["leetcode_number"],
                "difficulty": x["difficulty"], "section": x["section"],
                "pattern": x["pattern"], "subpattern": x["subpattern"],
                "slug": x["slug"], "html_file": x["html_file"],
                "github_pages_url": x["github_pages_url"], "icon": x["icon"],
                "notion_page_id": x["notion_page_id"]}, ensure_ascii=False))
