import csv
import json
from collections import Counter
from pathlib import Path

src = Path("web/public/data/stations.json")
out = Path("data/labels/language_map.csv")
TOP = None

data = json.loads(src.read_text(encoding="utf-8"))
stations = data if isinstance(data, list) else data.get("stations", data)

counts = Counter()
for s in stations:
    lang = s.get("language") or []
    if isinstance(lang, str):
        lang = lang.split(",")
    counts.update(v.strip() for v in lang if v.strip())

total = sum(counts.values())
out.parent.mkdir(parents=True, exist_ok=True)

covered = 0
with out.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["value", "count", "coverage", "code"])
    for value, n in counts.most_common(TOP):
        covered += n
        w.writerow([value, n, f"{covered / total:.1%}", ""])

print(f"Wrote {len(counts)} rows to {out}; coverage reaches {covered / total:.1%}")