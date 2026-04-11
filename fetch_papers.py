import arxiv, yaml, datetime, os

with open("config.yml") as f:
    cfg = yaml.safe_load(f)

keywords = cfg["keywords"]
max_results = cfg.get("max_results", 10)

today = datetime.date.today().isoformat()
os.makedirs("papers", exist_ok=True)

lines = [f"# Papers - {today}\n"]
for kw in keywords:
    lines.append(f"\n## 🔎 {kw}\n")
    search = arxiv.Search(
        query=kw,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    for r in search.results():
        lines.append(f"- **[{r.title}]({r.entry_id})**")
        lines.append(f"  - {', '.join(a.name for a in r.authors[:3])}")
        lines.append(f"  - {r.summary[:300].strip()}...\n")

with open(f"papers/{today}.md", "w") as f:
    f.write("\n".join(lines))

print(f"Saved papers/{today}.md")
