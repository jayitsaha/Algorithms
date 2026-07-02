# DSA Regeneration Agent Brief (ONE problem per agent)

You are regenerating **one** DSA problem from scratch, with care. The previous bulk-generated
content was thin/templated garbage and is being fully replaced. Your output must be
**educational, hand-authored, and format-identical** to the gold standard.

**Finish within ~12 minutes. Work on ONLY your assigned problem.**

## Inputs (given in your task prompt)
A manifest record: `name, leetcode_number, difficulty, section, pattern, subpattern, slug,
html_file, github_pages_url, icon, notion_page_id`.
- `notion_page_id` = the EXISTING Notion page to update **in-place**. If it is `null`, create one.

## Authoritative references — READ THESE FIRST
1. **Skill (the detailed prompting):** `/Users/j0s0yz3/.wibey/skills/dsa-pipeline/SKILL.md`
   Follow it fully — Step 2 (multiple solutions + intuition + deep-dive), Step 4 (Notion body
   structure), the HTML Design System, the Comprehensive Educational Structure, and the
   DP Deep-Dive Guidelines if your problem is DP.
2. **Canonical HTML template (match its structure & CSS EXACTLY):**
   `/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/valid_anagram_explainer.html`
   Copy its `<style>` design tokens verbatim (light+dark). Reuse its section framework,
   collapsible cards, concept boxes, var-tracker, code panel with active-line highlight,
   progress dots, Prev/Next/Reset, keyboard nav (← →), legend. Adapt the *visualization*
   to your problem's data structure; keep the *design system and section skeleton* identical.
3. **Pattern guide (verify classification / related problems):**
   `/Users/j0s0yz3/Documents/PersonalSkillUp/DSA_Patterns_and_SubPatterns_Guide.md`
4. **Notion helper (use it; do NOT hand-roll curl):**
   `/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/notion_lib.py`

## Step 0 — Resume check (avoid redoing finished work after a restart)
Before starting, check for prior progress on THIS slug:
- If `<slug>_explainer.html` already exists AND has ≥700 lines AND contains all of
  `const steps`, `section-title`, `--blue-mid`, `ArrowRight`, it is already good —
  **do NOT rewrite it**; keep it and move to the Notion step.
- For Notion: `python3 -c "import notion_lib as N; print(len(N.get_children('<page_id>')))"`.
  If it already returns ≥ 30 blocks (and page_id is not null), the body was already
  rebuilt — you may skip the wipe/rewrite and just ensure properties are set, then finish.
- Only regenerate the parts that are missing/thin. This makes restart-recovery cheap.

## Step 1 — Solve (with care)
- Produce **2–4 solutions**, brute-force → optimal. For EACH: approach name, **Intuition**
  (reframe / what-doesn't-work / key observation / how-to-discover / analogy), clean Python,
  **line-by-line** explanation, time & space complexity with justification, when-to-use.
- If a named algorithm is used (Kadane, Boyer-Moore, KMP, Dijkstra, Union-Find, etc.) add an
  **Algorithm Deep-Dive** (origin, invariant, why it works, when to recognize).
- Mark the interview pick.

## Step 2 — HTML explainer (format-identical to canonical)
Write a single self-contained file to:
`/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/<slug>_explainer.html`
(overwrite the thin existing one). Requirements — must all be present:
- `<title>#<number> · <Name></title>`; header with problem-number, h1, subtitle, tags
  (difficulty / pattern / complexity).
- **7 collapsible card sections**: (1) Understanding the Problem, (2) The Algorithm,
  (3) Why It Works: The Invariant, (4) The Code (Annotated), (5) 🎤 Interview Strategy,
  (6) Interactive Walkthrough, (7) Summary & Key Takeaways.
- concept boxes: insight (green) / warning (amber) / key-concept (blue) / danger (red).
- ≥1 diagram (state machine / decision tree / comparison panels). **500–1000 words** prose.
- **Interactive Walkthrough**: data-structure viz adapted to the problem, live variable
  tracker with change-highlight, code panel with per-step active-line highlight, info card
  (phase badge + step counter + title + prose), progress dots, Prev/Next/Reset, keyboard nav,
  legend. Hand-author `const steps=[...]` with enough steps (8–15+) that every meaningful
  state change is its own step; each step carries `activeLine`, variable values, explanation.
- Self-contained (only Google Fonts external). Expect **~700–950 lines**. A 15KB/80-line file
  is a FAIL — that is the garbage you are replacing.

## Step 3 — Notion (update IN-PLACE via notion_lib)
Write a script `gen_<slug>.py` next to notion_lib.py and run it. Pattern:
```python
import notion_lib as N
PAGE_ID = "<notion_page_id>"          # or None -> create
if PAGE_ID is None:
    PAGE_ID = N.create_page("<Name>", <number>, "<Difficulty>", "<icon>")
# 1) properties
N.set_properties(PAGE_ID, difficulty="<Difficulty>", number=<number>,
    pattern="<Pattern>", subpatterns=["<Subpattern>", ...],
    tc="<optimal time>", sc="<optimal space>", key_insight="<one line>", icon="<icon>")
# 2) wipe the old bulk body
N.wipe_page(PAGE_ID)
# 3) rebuild body — EXACT sequence from SKILL.md Step 4b:
blocks = []
blocks += [N.h2("Problem"), N.para("<statement, with code() spans for var names>"), N.divider()]
# For EACH solution:
blocks += [N.h2("Solution 1 — <Approach> (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"), N.para("..."),
        N.h4("What Doesn't Work"), N.para("..."),
        N.h4("The Key Observation"), N.para("..."),
        N.h4("Building the Solution"), N.para("..."),
        N.callout("Analogy: ...", "🧠", "blue_background")]),
    N.h3("Code"), N.code("<python>"),
    N.h3("Line by Line"),
    N.para(N.rich([("line", {"code":True}), " — explanation"])),  # one per meaningful line
    N.divider()]
# (repeat for Solution 2, 3 ...)
blocks += [N.h2("Complexity"),
    N.table([["Solution","Time","Space"], ["<name>","O(..)","O(..)"], ...]), N.divider()]
blocks += [N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold":True}), "<Pattern>"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold":True}), "<Subpattern>"])),
    N.callout("When to recognize this pattern: <signals>", "🔎", "green_background"), N.divider()]
blocks += [N.h2("🔗 Related Problems"), N.para("Problems using the same technique:")]
blocks += [N.bullet(N.rich([("<Problem>", {"bold":True}), " (<Diff>) — <note>"])) for ...]  # 5–10
blocks += [N.divider(), N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("<slug>")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic":True,"color":"gray"})]))]
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
```
For DP problems, also include the Why-is-this-DP section, recurrence-relation code block,
state-machine notes, and BOTH tabulation + memoization solutions (per SKILL.md DP guidelines).

## Step 4 — Status marker (REQUIRED, last action)
Write `/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/.status/<slug>.json`:
```json
{"slug":"<slug>","html":"OK","notion":"OK","lines":<html_line_count>,"notes":"<short>"}
```
Use `"FAIL"` (not OK) for any step that failed, with the reason in notes. Then print:
`RESULT <slug> | html=OK | notion=OK | lines=<n>`

## Hard constraints
- Do **NOT** modify `dsa_problems_queue.json`, `work_manifest.json`, `*.backup.json`,
  `notion_lib.py`, `AGENT_BRIEF.md`, or any of the 60 non-JSON gold base files.
- Do **NOT** `git push` or `git commit`.
- Notion **update in-place** (given page_id) — do not create duplicates.
- Handle Notion 429s (notion_lib already retries). If a step truly fails, record FAIL in the
  status file and still finish — do not hang.
- Stay on your ONE assigned problem. Finish in ~12 min.
