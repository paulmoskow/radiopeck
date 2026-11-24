import json
from collections import Counter
from pathlib import Path

path = Path("web/public/data/stations.json")
data = json.loads(path.read_text(encoding="utf-8"))
stations = data if isinstance(data, list) else data.get("stations", data)


def values(station):
    """language may be a list or a comma-separated string, handle both."""
    lang = station.get("language")
    if not lang:
        return []
    if isinstance(lang, str):
        lang = lang.split(",")
    return [v.strip() for v in lang if v.strip()]


raw = Counter()
for s in stations:
    raw.update(values(s))

lowered = Counter()
for value, n in raw.items():
    lowered[value.lower()] += n

total = len(stations)
without = sum(1 for s in stations if not values(s))
multi = sum(1 for s in stations if len(values(s)) > 1)

print(f"Stations: {total}")
print(f"Without language: {without} ({without / total:.1%})")
print(f"With 2+ languages: {multi}")
print(f"Unique values as written: {len(raw)}")
print(f"Unique values after lowercasing: {len(lowered)}")
print()
print("Top 30 (lowercased):")
for value, n in lowered.most_common(30):
    print(f"  {value:<22} {n:>6}")

print()
print("Spelling variants of the top 5 (as written):")
for value, _ in lowered.most_common(5):
    variants = [(v, n) for v, n in raw.items() if v.lower() == value]
    print(f"  {value}: {variants}")

print()
print("Rare values (1 station): ", sum(1 for n in lowered.values() if n == 1))