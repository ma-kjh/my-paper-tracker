import arxiv, yaml, datetime, os

with open("config.yml") as f:
    cfg = yaml.safe_load(f)

keywords = cfg["keywords"]
max_results = cfg.get("max_results", 10)

today = datetime.date.today().isoformat()
os.makedirs("papers", exist_ok=True)

all_lines = [f"# Papers - {today}\n"]
top_lines = [f"# 🌟 Top Matches - {today}\n"]

for kw in keywords:
    all_lines.append(f"\n## 🔎 {kw}\n")
    # 관련도순 (최상위 매칭용)
    top_search = arxiv.Search(
        query=kw, max_results=1,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    for r in top_search.results():
        top_lines.append(f"\n## 🔎 {kw}")
        top_lines.append(f"- [{r.title}]({r.entry_id})")
        top_lines.append(f"  - {', '.join(a.name for a in r.authors[:3])}")
        top_lines.append(f"  - {r.summary[:400].strip()}...\n")

    # 최신순 (일반 수집용)
    search = arxiv.Search(
        query=kw, max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    for r in search.results():
        all_lines.append(f"- [{r.title}]({r.entry_id})")
        all_lines.append(f"  - {', '.join(a.name for a in r.authors[:3])}")
        all_lines.append(f"  - {r.summary[:300].strip()}...\n")

with open(f"papers/{today}.md", "w") as f:
    f.write("\n".join(all_lines))
with open("top_papers.md", "w") as f:
    f.write("\n".join(top_lines))

print(f"Saved papers/{today}.md and top_papers.md")
