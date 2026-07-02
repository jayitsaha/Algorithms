"""
orchestrate.py — self-healing dispatcher for the endless regeneration flow.

On each wake the orchestrator runs this. It:
  1. reconciles status markers -> flips flags in queue + manifest
  2. QCs every html=OK slug; failing ones have their status dropped (re-dispatch)
  3. reconciles .inflight/ markers (mtime = launch time):
       - slug now done            -> remove marker
       - marker age > 15 min      -> timed out: bump retry count, remove marker;
                                     after MAX_RETRIES timeouts -> add to .skipped
  4. computes free = TARGET - inflight
  5. selects next `free` pending (not done, not inflight, not skipped), TOUCHES a
     fresh .inflight/<slug> marker for each, and prints DISPATCH lines.

Because markers are touched BEFORE launch, a mid-turn crash self-heals: the marker
times out in 15 min and the slug re-dispatches. No permanent phantoms.

Usage: python3 orchestrate.py [TARGET]     (default 16)
"""
import json, os, sys, glob, time
import reconcile as R

TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 16
TIMEOUT = 15 * 60
MAX_RETRIES = 1
INFLIGHT = os.path.join(R.ROOT, ".inflight")
RETRIES = os.path.join(R.ROOT, ".retries")
SKIPPED = os.path.join(R.ROOT, ".skipped")
MARK = ["const steps", "section-title", "--blue-mid", "ArrowRight"]


def qc(slug):
    p = os.path.join(R.ROOT, f"{slug}_explainer.html")
    if not os.path.exists(p):
        return False
    t = open(p, encoding="utf-8", errors="ignore").read()
    return (t.count("\n") + 1) >= 400 and all(m in t for m in MARK)


def main():
    os.makedirs(INFLIGHT, exist_ok=True)
    os.makedirs(RETRIES, exist_ok=True)

    # `recover` mode: known process restart -> all background agents are dead,
    # so clear every inflight marker (work is salvaged via HTML files + resume-check).
    if "recover" in sys.argv:
        for m in glob.glob(os.path.join(INFLIGHT, "*")):
            os.remove(m)

    r = R.reconcile()
    # QC pass: drop bad status files so they re-dispatch
    for f in glob.glob(os.path.join(R.STATUS, "*.json")):
        try:
            st = json.load(open(f))
        except Exception:
            continue
        slug = st.get("slug") or os.path.splitext(os.path.basename(f))[0]
        if st.get("html") == "OK" and not qc(slug):
            os.remove(f)
    r = R.reconcile()
    manifest = r["manifest"]
    done = {x["slug"] for x in manifest if x.get("html_done") and x.get("notion_done")}

    skipped = set()
    if os.path.exists(SKIPPED):
        skipped = set(l.strip() for l in open(SKIPPED) if l.strip())

    now = time.time()
    events = []
    for mk in glob.glob(os.path.join(INFLIGHT, "*")):
        slug = os.path.basename(mk)
        if slug in done:
            os.remove(mk)
            continue
        if now - os.path.getmtime(mk) > TIMEOUT:
            rc = os.path.join(RETRIES, slug)
            n = (int(open(rc).read()) if os.path.exists(rc) else 0) + 1
            open(rc, "w").write(str(n))
            os.remove(mk)
            if n > MAX_RETRIES:
                with open(SKIPPED, "a") as s:
                    s.write(slug + "\n")
                skipped.add(slug)
                events.append(f"{slug}:SKIP(after {n})")
            else:
                events.append(f"{slug}:timeout retry {n}")

    inflight = {os.path.basename(m) for m in glob.glob(os.path.join(INFLIGHT, "*"))}
    free = max(0, TARGET - len(inflight))

    nxt = []
    for x in manifest:
        if len(nxt) >= free:
            break
        s = x["slug"]
        if s in done or s in inflight or s in skipped:
            continue
        nxt.append(x)

    for x in nxt:
        open(os.path.join(INFLIGHT, x["slug"]), "w").write(str(now))

    remaining = r["total"] - r["fully"] - len(skipped)
    print(f"PROGRESS {r['fully']}/{r['total']} | inflight={len(inflight)} "
          f"| launching={len(nxt)} | skipped={len(skipped)} | remaining~{remaining}")
    if events:
        print("INFLIGHT_EVENTS:", events)
    if not nxt and not inflight:
        print("DRAINED (nothing in flight, nothing to launch)")
    for x in nxt:
        print("DISPATCH\t" + json.dumps({k: x[k] for k in (
            "name", "leetcode_number", "difficulty", "section", "pattern",
            "subpattern", "slug", "html_file", "github_pages_url", "icon",
            "notion_page_id")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
