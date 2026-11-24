import json
from collections import Counter, defaultdict
from pathlib import Path

STATIONS = Path("web/public/data/stations.json")
LANGS = Path("data/tags/stations_languages.json")
OUT = Path("data/tags/stations_languages_enriched.json")
RULES_OUT = Path("data/tags/country_language_rules.json")

MIN_SHARE = 0.85      # the top language must cover at least this share of the country
MIN_STATIONS = 20     # ignore countries with too few labelled stations


def dominant_language(counter, total, min_share=MIN_SHARE, min_stations=MIN_STATIONS):
    """Return (code, share) if one language clearly dominates, otherwise None"""
    if total < min_stations:
        return None
    code, n = counter.most_common(1)[0]
    share = n / total
    if share < min_share:
        return None
    return code, share


def main():
    data = json.loads(STATIONS.read_text(encoding="utf-8"))
    stations = data if isinstance(data, list) else data.get("stations", data)
    known = json.loads(LANGS.read_text(encoding="utf-8"))  # uuid -> [codes]

    # 1. Per country: how many labelled stations speak each language
    per_country = defaultdict(Counter)
    labelled = Counter()
    for s in stations:
        codes = known.get(s["stationuuid"])
        country = s.get("country")
        if codes and country:
            labelled[country] += 1
            per_country[country].update(codes)

    # 2. Which countries have a dominant language
    rules = {}
    skipped = []
    for country, counter in per_country.items():
        result = dominant_language(counter, labelled[country])
        if result:
            rules[country] = {"code": result[0], "share": round(result[1], 3), "n": labelled[country]}
        else:
            skipped.append((country, labelled[country], counter.most_common(2)))

    # 3. Apply the rules to stations without a language
    enriched = {uuid: {"codes": codes, "source": "label"} for uuid, codes in known.items()}
    added = 0
    for s in stations:
        uuid = s["stationuuid"]
        country = s.get("country")
        if uuid not in enriched and country in rules:
            enriched[uuid] = {"codes": [rules[country]["code"]], "source": "country"}
            added += 1

    OUT.write_text(json.dumps(enriched, ensure_ascii=False), encoding="utf-8")
    RULES_OUT.write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")

    total = len(stations)
    print(f"Countries with a dominant language: {len(rules)}")
    print(f"Countries skipped (mixed or too small): {len(skipped)}")
    print(f"Stations enriched from country: {added}")
    print(f"Stations with a language now: {len(enriched)} ({len(enriched) / total:.1%})")
    print(f"Still without language: {total - len(enriched)} ({1 - len(enriched) / total:.1%})")
    print()
    print("Biggest skipped countries:")
    for country, n, top in sorted(skipped, key=lambda x: -x[1])[:12]:
        print(f"  {country:<28} {n:>5}  {top}")


if __name__ == "__main__":
    main()