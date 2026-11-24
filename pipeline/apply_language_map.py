import csv
import json
from collections import Counter
from pathlib import Path

STATIONS = Path("web/public/data/stations.json")
LANG_MAP = Path("data/labels/language_map.csv")
OUT = Path("data/tags/stations_languages.json")


def load_map(path):
    """value -> list of codes. '?' and empty codes are left out."""
    mapping = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            code = row["code"].strip()
            if code and code != "?":
                mapping[row["value"]] = code.split("|")
    return mapping


def raw_values(station):
    lang = station.get("language") or []
    if isinstance(lang, str):
        lang = lang.split(",")
    return [v.strip() for v in lang if v.strip()]


def codes_for(station, mapping):
    """Return the station's language codes, in order, without duplicates."""
    result = []
    for value in raw_values(station):
        for code in mapping.get(value, []):
            if code not in result:
                result.append(code)
    return result


def main():
    data = json.loads(STATIONS.read_text(encoding="utf-8"))
    stations = data if isinstance(data, list) else data.get("stations", data)
    mapping = load_map(LANG_MAP)

    result = {}
    stats = Counter()
    for s in stations:
        raw = raw_values(s)
        codes = codes_for(s, mapping)
        if codes:
            result[s["stationuuid"]] = codes
        stats["with_raw_language"] += bool(raw)
        stats["with_code"] += bool(codes)
        stats["raw_but_no_code"] += bool(raw) and not codes

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")

    total = len(stations)
    print(f"Stations: {total}")
    print(f"With raw language: {stats['with_raw_language']}")
    print(f"With a language code: {stats['with_code']} ({stats['with_code'] / total:.1%})")
    print(f"Raw language but no code: {stats['raw_but_no_code']}")
    print(f"Still without language: {total - stats['with_code']} ({1 - stats['with_code'] / total:.1%})")
    print()
    print("Top codes:", Counter(c for codes in result.values() for c in codes).most_common(15))


if __name__ == "__main__":
    main()