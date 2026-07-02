"""
dispatch.py — one-call refill helper for the orchestrator.

Each cycle:
  1. reconcile status markers -> flip flags in queue + manifest
  2. QC every html=OK slug (line count + required markers). Failing ones are
     reset (flags cleared, status + dispatched entry removed) so they re-dispatch.
  3. compute free slots = TARGET - in_flight
  4. print next `free` pending records as DISPATCH lines AND append them to
     .dispatched atomically (prevents double-launch).

Usage: python3 dispatch.py [TARGET]      (default TARGET=16)
"""
import json, os, sys, glob
import reconcile as R

TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 16
QC_MIN_LINES = 400
QC_MARKERS = ["const steps", "section-title", "--blue-mid", "ArrowRight"]


def qc_html(slug):
    p = os.path.join(R.ROOT, f"{slug}_explainer.html")
    if not os.path.exists(p):
        return False, "missing html"
    txt = open(p, encoding="utf-8", errors="ignore").read()
    lines = txt.count("\n") + 1
    if lines < QC_MIN_LINES:
        return False, f"thin ({lines} lines)"
    missing = [m for m in QC_MARKERS if m not in txt]
    if missing:
        return False, f"missing markers {missing}"
    return True, f"{lines} lines"


def main():
    # First reconcile so flags reflect status files
    r = R.reconcile()
    manifest = r["manifest"]

    # QC pass: validate html for every slug that claims html OK
    reset = []
    for f in glob.glob(os.path.join(R.STATUS, "*.json")):
        try:
            st = json.load(open(f))
        except Exception:
            continue
        slug = st.get("slug") or os.path.splitext(os.path.basename(f))[0]
        if st.get("html") == "OK":
            ok, msg = qc_html(slug)
            if not ok:
                reset.append((slug, msg))
                os.remove(f)  # drop bad status -> will re-dispatch
    if reset:
        # remove reset slugs from .dispatched and clear flags
        dp = os.path.join(R.ROOT, ".dispatched")
        bad = {s for s, _ in reset}
        if os.path.exists(dp):
            keep = [l.strip() for l in open(dp) if l.strip() and l.strip() not in bad]
            open(dp, "w").write("\n".join(keep) + ("\n" if keep else ""))
        r = R.reconcile()  # re-run so flags drop for reset slugs
        manifest = r["manifest"]

    dp = os.path.join(R.ROOT, ".dispatched")
    dispatched = set(l.strip() for l in open(dp)) if os.path.exists(dp) else set()
    done_slugs = {x["slug"] for x in manifest
                  if x.get("html_done") and x.get("notion_done")}
    in_flight = len([s for s in dispatched if s not in done_slugs])
    free = max(0, TARGET - in_flight)
    nxt = R.pending(manifest, free)

    with open(dp, "a") as fh:
        for x in nxt:
            fh.write(x["slug"] + "\n")

    print(f"PROGRESS {r['fully']}/{r['total']} | in_flight={in_flight} "
          f"| free={free} | launching={len(nxt)} | remaining={r['total']-r['fully']}")
    if reset:
        print("QC_RESET (re-dispatch):", reset)
    if r["fails"]:
        print("STATUS_FAILS:", r["fails"][:10])
    for x in nxt:
        print("DISPATCH\t" + json.dumps({
            "name": x["name"], "leetcode_number": x["leetcode_number"],
            "difficulty": x["difficulty"], "section": x["section"],
            "pattern": x["pattern"], "subpattern": x["subpattern"],
            "slug": x["slug"], "html_file": x["html_file"],
            "github_pages_url": x["github_pages_url"], "icon": x["icon"],
            "notion_page_id": x["notion_page_id"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
