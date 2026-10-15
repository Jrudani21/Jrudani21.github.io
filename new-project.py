"""Add a project card to index.html.

  python new-project.py <github-repo-or-url> "<title>" <model|forecast|apps|ai|auto> "<metric>" "<one-line blurb>" [tag ...]

Example:
  python new-project.py fraud-graph "Fraud Rings - Neo4j Graph" ai "Rings found" "Clusters card fraud into rings." Neo4j Cypher Python

The card goes at the top of the grid. Run, review `git diff`, commit, push.
"""
import html, re, sys

if len(sys.argv) < 6 or sys.argv[3] not in ("model", "forecast", "apps", "ai", "auto"):
    sys.exit(__doc__)
repo, title, cat, metric, blurb, *tags = sys.argv[1:]
url = repo if repo.startswith("http") else f"https://github.com/Jrudani21/{repo}"
e = html.escape
card = f'''    <a href="{e(url)}" target="_blank" rel="noopener" class="project" data-cat="{cat}">
      <div>
        <h3>{e(title)}</h3>
        <p>{e(blurb)}</p>
        <div class="tags">{"".join(f'<span class="tag{" hl" if i == 0 else ""}">{e(t)}</span>' for i, t in enumerate(tags))}</div>
      </div>
      <div class="project-side"><div class="project-score">{e(metric)}</div><div class="project-link">github ↗</div></div>
    </a>

'''
p = "index.html"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
marker = '<div class="stagger" id="projectList">' + nl
assert marker in s, "projectList not found"
s = s.replace(marker, marker + nl + card.replace("\n", nl), 1)
open(p, "w", encoding="utf-8", newline="").write(s)
print("added:", title)
