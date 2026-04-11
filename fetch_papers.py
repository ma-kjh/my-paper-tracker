import arxiv, yaml, datetime, os

with open("config.yml") as f:
    cfg = yaml.safe_load(f)

keywords = cfg["keywords"]
max_results = cfg.get("max_results", 10)
days_limit = cfg.get("days_limit", 30)

today = datetime.date.today()
cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_limit)
os.makedirs("papers", exist_ok=True)

all_lines = [f"# Papers - {today.isoformat()} (최근 {days_limit}일)\n"]
top_lines = [f"# 🌟 Top Matches - {today.isoformat()}\n"]

for kw in keywords:
    all_lines.append(f"\n## 🔎 {kw}\n")

    top_search = arxiv.Search(
        query=kw, max_results=20,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    top_found = False
    for r in top_search.results():
        if r.published < cutoff:
            continue
        top_lines.append(f"\n## 🔎 {kw}")
        top_lines.append(f"- [{r.title}]({r.entry_id})")
        top_lines.append(f"  - {', '.join(a.name for a in r.authors[:3])}")
        top_lines.append(f"  - 📅 {r.published.date()}")
        top_lines.append(f"  - {r.summary[:400].strip()}...\n")
        top_found = True
        break
    if not top_found:
        top_lines.append(f"\n## 🔎 {kw}\n- (최근 {days_limit}일 내 매칭 논문 없음)\n")

    search = arxiv.Search(
        query=kw, max_results=max_results * 3,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    count = 0
    for r in search.results():
        if r.published < cutoff:
            break
        all_lines.append(f"- [{r.title}]({r.entry_id})")
        all_lines.append(f"  - {', '.join(a.name for a in r.authors[:3])}")
        all_lines.append(f"  - 📅 {r.published.date()}")
        all_lines.append(f"  - {r.summary[:300].strip()}...\n")
        count += 1
        if count >= max_results:
            break
    if count == 0:
        all_lines.append(f"- (최근 {days_limit}일 내 논문 없음)\n")

with open(f"papers/{today.isoformat()}.md", "w") as f:
    f.write("\n".join(all_lines))
with open("top_papers.md", "w") as f:
    f.write("\n".join(top_lines))

print(f"Saved papers/{today.isoformat()}.md and top_papers.md")
