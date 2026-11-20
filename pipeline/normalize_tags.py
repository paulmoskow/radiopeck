#!/usr/bin/env python3
"""RadioPeck pipeline, step 2: analyse and normalise station tags.

Reads the cleaned catalogue written by fetch_stations.py (no network needed) and
answers two questions:
  1. What is actually in the tags? (genres, geography, languages, noise, bulk-added junk)
  2. How many stations end up with a usable genre once tags are normalised?

How a tag is classified (first match wins):
  generic    "music", "radio", "fm", "hits" ... no information
  dictionary genre / format / language / geography from taxonomy.py
  decade     "80s", "1990s", "años 80"
  data       a language or place name that occurs in the stations' own fields
  compound   "jazz & blues", "rock/pop": each part is classified separately
  phrase     "música en español", "pop en inglés", "greek pop": topic + language
  fuzzy      near-miss of a known genre ("djazz" -> jazz), listed for manual review
  bulk       unknown tag that always travels with the same group of other tags
             (a sign of bulk import by one contributor, like "moi merino")
  rare       unknown tag used by a single station
  other      everything else (see "Top unmapped tags": extend taxonomy.py from it)

Original tags are never changed or dropped: derived fields are stored next to them.

Usage
  python pipeline/normalize_tags.py                      # reads data/stations.parquet
  python pipeline/normalize_tags.py --input some.json    # or any stations .json/.parquet
  python pipeline/normalize_tags.py --no-fuzzy

Outputs (in --out, default: data/tags/)
  tag_report.md         the report to read (and to send back for review)
  tag_stats.csv         one row per tag: count, category, values, top country, bundle score
  tag_map.json          raw tag -> category and canonical values (the dictionary as applied)
  stations_tags.json    per station: genres, formats, decades, geo_tags, lang_tags, ...
  stations_tags.parquet same (only if pyarrow is installed)
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import taxonomy

TIERS = [0, 5, 50]  # vote thresholds shown in the coverage table


# --------------------------------------------------------------------------- #
# Normalisation
# --------------------------------------------------------------------------- #

def strip_accents(text: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", text)
                   if unicodedata.category(ch) != "Mn")


def protect(text: str) -> str:
    """Rewrite spellings that contain separators so they survive punctuation removal."""
    text = re.sub(r"\br\s*(?:&|'n'|’n’|and)\s*b\b", "rnb", text)
    text = re.sub(r"\brock\s*(?:&|'n'|’n’|n|and)\s*roll\b", "rock and roll", text)
    text = re.sub(r"(\d)\s*['’`´]\s*s\b", r"\1s", text)  # 80's -> 80s
    return text


def norm_key(tag: str) -> str:
    """Lower case, no accents, no punctuation, single spaces."""
    text = unicodedata.normalize("NFKC", str(tag)).casefold()
    text = strip_accents(protect(text))
    text = re.sub(r"[^\w\s]|_", " ", text)
    return " ".join(text.split())


GENERIC_WORDS = {norm_key(w) for w in taxonomy.GENERIC_WORDS}


def core_key(key: str) -> str:
    """Drop generic words at both ends: 'pop music' -> 'pop'. '' if nothing is left."""
    tokens = key.split()
    while len(tokens) > 1 and tokens[0] in GENERIC_WORDS:
        tokens.pop(0)
    while len(tokens) > 1 and tokens[-1] in GENERIC_WORDS:
        tokens.pop()
    if all(t in GENERIC_WORDS for t in tokens):
        return ""
    return " ".join(tokens)


DECADE_SUFFIX = re.compile(r"^(?:19|20)?(\d)0\s?(?:s|er|ies|ers)$")
DECADE_PREFIX = re.compile(r"^(?:anos|anni|annees|jahre|years|decada de los|decada)\s+(?:19|20)?(\d)0$")


def decade_of(key: str) -> str | None:
    for pattern in (DECADE_SUFFIX, DECADE_PREFIX):
        m = pattern.match(key)
        if m:
            digit = int(m.group(1))
            return f"{1900 + digit * 10}s" if digit >= 3 else f"{2000 + digit * 10}s"
    return None


STOPWORDS = {norm_key(w) for w in taxonomy.STOPWORDS}
FREQUENCY = re.compile(r"\d{2,4}(?: \d{1,2})?(?: ?(?:fm|am|mhz|khz))?")
BITRATE = re.compile(r"\d{2,4} ?k ?(?:bps|bit(?: s)?|b(?: s)?)")
BRAND_SUFFIXES = {"comunicaciones", "medios", "network", "media", "communications",
                  "comunicacion", "multimedia", "broadcasting"}
STATION_WORDS = {"fm", "radio", "radyo"}


LANGUAGE_PREPOSITIONS = {"en", "in", "auf", "em", "na", "im"}

COMPOUND_SPLIT = re.compile(r"\s*(?:/|\+|,|;|&|\band\b|\by\b|\bund\b|\bet\b|\be\b)\s*")


def split_compound(raw: str) -> list[str]:
    text = protect(unicodedata.normalize("NFKC", str(raw)).casefold())
    return [p for p in COMPOUND_SPLIT.split(text) if p.strip()]


# --------------------------------------------------------------------------- #
# Dictionary
# --------------------------------------------------------------------------- #

Entry = tuple[str, str]  # (category, value)


class Dictionary:
    def __init__(self) -> None:
        self.lookup: dict[str, list[Entry]] = {}
        self.conflicts: list[str] = []
        self._build()
        if self.conflicts:
            raise ValueError("taxonomy.py maps the same word to different categories; "
                             "remove it from one of the lists:\n" + "\n".join(self.conflicts))

    def _add(self, raw: str, entries: list[Entry], where: str) -> None:
        key = norm_key(raw)
        if not key:
            return
        current = self.lookup.get(key)
        if current is not None and current != entries:
            self.conflicts.append(
                f"  '{raw}' (key '{key}') in {where}: already maps to "
                f"{[f'{a}:{b}' for a, b in current]}, now {[f'{a}:{b}' for a, b in entries]}")
            return
        self.lookup[key] = entries

    def _build(self) -> None:
        for genre, synonyms in taxonomy.GENRES.items():
            for s in synonyms:
                self._add(s, [("genre", genre)], f"GENRES[{genre}]")
        for raw, values in taxonomy.MULTI.items():
            self._add(raw, [tuple(v.split(":", 1)) for v in values], "MULTI")
        for fmt, synonyms in taxonomy.FORMATS.items():
            for s in synonyms:
                self._add(s, [("format", fmt)], f"FORMATS[{fmt}]")
        for lang, names in taxonomy.LANGUAGES.items():
            for s in [lang, *names]:
                self._add(s, [("language", lang)], f"LANGUAGES[{lang}]")
        for word in taxonomy.GEO_WORDS:
            self._add(word, [("geo", norm_key(word))], "GEO_WORDS")
        for word in taxonomy.GENERIC_TAGS:
            self._add(word, [("generic", "")], "GENERIC_TAGS")
        for word, decade in taxonomy.DECADE_WORDS.items():
            self._add(word, [("decade", decade)], "DECADE_WORDS")
        for name in taxonomy.BRANDS:
            key = norm_key(name)
            self._add(name, [("brand", core_key(key) or key)], "BRANDS")
        for word in taxonomy.TECH_TAGS:
            self._add(word, [("tech", "")], "TECH_TAGS")
        for feature, synonyms in taxonomy.FEATURES.items():
            for s in synonyms:
                self._add(s, [("feature", feature)], f"FEATURES[{feature}]")
        for mood, synonyms in taxonomy.MOODS.items():
            for s in synonyms:
                self._add(s, [("mood", mood)], f"MOODS[{mood}]")


class Classifier:
    def __init__(self, dictionary: Dictionary, language_keys: dict[str, str],
                 geo_keys: set[str], fuzzy: bool) -> None:
        self.lookup = dictionary.lookup
        self.language_keys = language_keys
        self.geo_keys = geo_keys
        self.fuzzy = fuzzy
        self.fuzzy_pool = [k for k, e in self.lookup.items()
                           if e[0][0] == "genre" and len(k) >= 4 and re.fullmatch(r"[a-z ]+", k)]
        self.lang_by_key = {k: e[0][1] for k, e in self.lookup.items() if e[0][0] == "language"}
        for key, lang in language_keys.items():
            self.lang_by_key.setdefault(key, lang)

    def atomic(self, raw: str) -> tuple[list[Entry], str] | None:
        key = norm_key(raw)
        if not key:
            return None
        if FREQUENCY.fullmatch(key) or BITRATE.fullmatch(key):
            return [("tech", "")], "tech"
        core = core_key(key)
        if core == "":
            return [("generic", "")], "generic"
        for candidate in (key, core):
            entries = self.lookup.get(candidate)
            if entries:
                source = "generic" if entries[0][0] in ("generic", "tech") else "dictionary"
                return entries, source
        for candidate in (key, core):
            decade = decade_of(candidate)
            if decade:
                return [("decade", decade)], "decade"
        for candidate in (key, core):
            if candidate in self.language_keys:
                return [("language", self.language_keys[candidate])], "data-language"
        for candidate in (key, core):
            if candidate in self.geo_keys:
                return [("geo", candidate)], "data-geo"
        tokens = key.split()
        if len(tokens) >= 2 and (tokens[0] == "grupo" or tokens[-1] in BRAND_SUFFIXES):
            return [("brand", key)], "brand-rule"
        return None

    def phrase(self, raw: str) -> tuple[list[Entry], str] | None:
        """Split a multi-word tag into known parts, e.g.
        'club dance electronic house trance' -> dance + electronic,
        'noticias y comentarios' -> news, 'stoner rock' -> rock."""
        tokens = norm_key(raw).split()
        n = len(tokens)
        if n < 2 or n > 8:
            return None
        entries: list[Entry] = []
        consumed, i = 0, 0
        while i < n:
            hit = None
            for j in range(min(n, i + 4), i, -1):
                found = self.atomic(" ".join(tokens[i:j]))
                if found:
                    hit = (j, found[0])
                    break
            if hit:
                j, found_entries = hit
                consumed += j - i
                for entry in found_entries:
                    if entry[0] not in ("generic", "tech") and entry not in entries:
                        entries.append(entry)
                i = j
            else:
                if tokens[i] in STOPWORDS:
                    consumed += 1
                i += 1
        if consumed < n * (0.5 if n == 2 else 0.34):
            return None
        informative = {"genre", "format", "decade", "language", "brand", "feature", "mood"}
        if any(e[0] in informative for e in entries):
            return entries, "phrase"
        if consumed == n:
            return (entries, "phrase") if entries else ([("generic", "")], "generic")
        return None

    def station_name(self, raw: str) -> tuple[list[Entry], str] | None:
        """Unknown tags that look like a station's own name ('La Z', 'Radio Lobo', 'Vive FM')."""
        key = norm_key(raw)
        tokens = key.split()
        if 2 <= len(tokens) <= 4 and (tokens[0] in {"la", "el", "los", "las"} or STATION_WORDS & set(tokens)):
            return [("brand", key)], "station-name"
        return None

    def language_phrase(self, raw: str) -> tuple[list[Entry], str] | None:
        """'música en español' -> language; 'pop en inglés' -> pop + english;
        'greek pop' / 'german rock' -> the genre + the language."""
        tokens = norm_key(raw).split()
        if len(tokens) >= 3 and tokens[-2] in LANGUAGE_PREPOSITIONS and tokens[-1] in self.lang_by_key:
            topic = self.atomic(" ".join(tokens[:-2]))
            entries = [e for e in (topic[0] if topic else []) if e[0] != "generic"]
            entries.append(("language", self.lang_by_key[tokens[-1]]))
            return entries, "language-phrase"
        if len(tokens) >= 2 and tokens[0] in self.lang_by_key:
            rest = self.atomic(" ".join(tokens[1:]))
            if rest and rest[0][0][0] in ("genre", "format"):
                return [*rest[0], ("language", self.lang_by_key[tokens[0]])], "language-phrase"
        return None

    def single(self, raw: str) -> tuple[list[Entry], str] | None:
        return self.atomic(raw) or self.language_phrase(raw)

    def classify(self, raw: str, count: int) -> tuple[list[Entry], str] | None:
        hit = self.single(raw)
        if hit:
            return hit

        parts = split_compound(raw)
        if len(parts) >= 2:
            merged: list[Entry] = []
            all_generic = True
            for part in parts:
                sub = self.single(part)
                if sub is None:
                    all_generic = False
                    continue
                if sub[0][0][0] in ("generic", "tech"):
                    continue
                all_generic = False
                for entry in sub[0]:
                    if entry not in merged:
                        merged.append(entry)
            if merged:
                return merged, "compound"
            if all_generic:
                return [("generic", "")], "generic"

        hit = self.phrase(raw)
        if hit:
            return hit

        if self.fuzzy and count >= 2:
            core = core_key(norm_key(raw))
            if re.fullmatch(r"[a-z ]{5,}", core or ""):
                match = difflib.get_close_matches(core, self.fuzzy_pool, n=1, cutoff=0.88)
                if match:
                    return self.lookup[match[0]], f"fuzzy:{match[0]}"
        return self.station_name(raw)


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #

def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [x.strip() for x in value.split(",") if x.strip()]
    if hasattr(value, "tolist"):
        value = value.tolist()
    if isinstance(value, (list, tuple)):
        return [str(x).strip() for x in value if x is not None and str(x).strip()]
    return []


def load_stations(path: Path) -> list[dict]:
    if path.suffix.lower() == ".parquet":
        frame = pd.read_parquet(path)
        rows = frame.to_dict(orient="records")
    else:
        rows = json.loads(path.read_text(encoding="utf-8"))
    stations = []
    for row in rows:
        stations.append({
            "stationuuid": str(row.get("stationuuid") or ""),
            "name": str(row.get("name") or ""),
            "countrycode": str(row.get("countrycode") or "").upper(),
            "country": str(row.get("country") or ""),
            "state": str(row.get("state") or ""),
            "votes": int(row.get("votes") or 0),
            "tags": list(dict.fromkeys(as_list(row.get("tags")))),
            "language": [x.casefold() for x in as_list(row.get("language"))],
        })
    return stations


# --------------------------------------------------------------------------- #
# Report helpers
# --------------------------------------------------------------------------- #

def pct(part: int, whole: int) -> str:
    return f"{100 * part / whole:.1f}%" if whole else "n/a"


def cell(part: int, whole: int) -> str:
    return f"{part} ({pct(part, whole)})"


def md_table(headers: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(str(c).replace("|", "/") for c in row) + " |" for row in rows]
    return "\n".join(lines)


def coverage(results: list[dict], min_votes: int) -> tuple[int, dict[str, int]]:
    sub = [r for r in results if r["votes"] >= min_votes]

    def informative(r):
        return bool(r["genres"] or r["formats"] or r["decades"])

    return len(sub), {
        "Has at least one raw tag": sum(1 for r in sub if r["tags"]),
        "Has at least one genre": sum(1 for r in sub if r["genres"]),
        "Has a genre or a format": sum(1 for r in sub if r["genres"] or r["formats"]),
        "Has a genre, format or decade": sum(1 for r in sub if informative(r)),
        "Only unmapped tags (no genre, format or decade)":
            sum(1 for r in sub if not informative(r) and r["other_tags"]),
        "Nothing informative (no tags, or only generic/bulk/geo/language tags)":
            sum(1 for r in sub if not informative(r) and not r["other_tags"]),
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, help="stations .parquet or .json (default: data/stations.parquet)")
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--out", type=Path, help="output directory (default: <data-dir>/tags)")
    ap.add_argument("--min-bulk-count", type=int, default=100,
                    help="a tag must be on at least this many stations to be tested for bulk import")
    ap.add_argument("--bulk-score", type=float, default=0.7,
                    help="bundle score from which an unmapped tag counts as bulk-added")
    ap.add_argument("--no-fuzzy", action="store_true", help="disable near-miss matching")
    ap.add_argument("--top-unmapped", type=int, default=80)
    args = ap.parse_args()

    path = args.input
    if path is None:
        parquet, js = args.data_dir / "stations.parquet", args.data_dir / "stations.json"
        path = parquet if parquet.exists() else js
    if not path.exists():
        print(f"Input not found: {path}. Run pipeline/fetch_stations.py first.", file=sys.stderr)
        return 1
    out = args.out or (args.data_dir / "tags")
    out.mkdir(parents=True, exist_ok=True)

    stations = load_stations(path)
    print(f"Loaded {len(stations)} stations from {path}")

    # ---- counts -----------------------------------------------------------
    counts: Counter[str] = Counter()
    countries: dict[str, Counter] = defaultdict(Counter)
    for s in stations:
        for tag in s["tags"]:
            counts[tag] += 1
            countries[tag][s["countrycode"] or "??"] += 1

    # ---- classification ---------------------------------------------------
    language_keys: dict[str, str] = {}
    geo_keys: set[str] = set()
    for s in stations:
        for lang in s["language"]:
            language_keys.setdefault(norm_key(lang), lang)
        for field in (s["country"], s["state"]):
            key = norm_key(field)
            if key:
                geo_keys.add(key)
    language_keys.pop("", None)

    classifier = Classifier(Dictionary(), language_keys, geo_keys, fuzzy=not args.no_fuzzy)
    info: dict[str, dict] = {}
    for tag, count in counts.items():
        hit = classifier.classify(tag, count)
        if hit:
            entries, source = hit
            cats = sorted({c for c, _ in entries})
            info[tag] = {"entries": entries, "source": source, "category": "+".join(cats)}
        else:
            info[tag] = {"entries": [], "source": "", "category": "unmapped"}

    # ---- bundles: tags that always travel together ------------------------
    heavy = {t for t, c in counts.items() if c >= args.min_bulk_count}
    cooc: dict[str, Counter] = {t: Counter() for t in heavy}
    for s in stations:
        present = [t for t in s["tags"] if t in heavy]
        for t in present:
            cooc[t].update(u for u in s["tags"] if u != t)
    bundle_score: dict[str, float] = {}
    for t in heavy:
        probs = [n / counts[t] for _, n in cooc[t].most_common(3)]
        probs += [0.0] * (3 - len(probs))
        bundle_score[t] = sum(probs) / 3

    for tag, rec in info.items():
        if rec["category"] != "unmapped":
            continue
        if tag in heavy and bundle_score[tag] >= args.bulk_score:
            rec["category"], rec["source"] = "bulk", "bundle"
        elif counts[tag] == 1:
            rec["category"], rec["source"] = "rare", "singleton"
        else:
            rec["category"], rec["source"] = "other", "unmapped"

    # ---- per-station fields -----------------------------------------------
    results: list[dict] = []
    for s in stations:
        fields: dict[str, list[str]] = {k: [] for k in
                                        ("genres", "formats", "decades", "geo_tags", "lang_tags",
                                         "brand_tags", "features", "moods", "other_tags")}
        target = {"genre": "genres", "format": "formats", "decade": "decades",
                  "geo": "geo_tags", "language": "lang_tags", "brand": "brand_tags",
                  "feature": "features", "mood": "moods"}
        for tag in s["tags"]:
            rec = info[tag]
            if rec["category"] in ("other", "rare"):
                fields["other_tags"].append(tag)
            elif rec["category"] == "bulk":
                continue
            else:
                for category, value in rec["entries"]:
                    if category in ("generic", "tech"):
                        continue
                    bucket = fields[target[category]]
                    if value not in bucket:
                        bucket.append(value)
        inferred = fields["lang_tags"] if (not s["language"] and fields["lang_tags"]) else []
        results.append({**s, **fields, "language_inferred": inferred})

    # ---- outputs ----------------------------------------------------------
    stats_rows = []
    for tag, c in counts.most_common():
        rec = info[tag]
        top_cc, top_n = countries[tag].most_common(1)[0]
        stats_rows.append({
            "tag": tag, "stations": c, "category": rec["category"], "source": rec["source"],
            "values": "|".join(f"{a}:{b}" for a, b in rec["entries"] if a not in ("generic", "tech")),
            "key": norm_key(tag), "top_country": top_cc,
            "top_country_share": round(top_n / c, 3),
            "bundle_score": round(bundle_score[tag], 3) if tag in bundle_score else "",
        })
    pd.DataFrame(stats_rows).to_csv(out / "tag_stats.csv", index=False, encoding="utf-8-sig")

    tag_map = {t: {"category": r["category"], "source": r["source"],
                   "values": [list(e) for e in r["entries"] if e[0] not in ("generic", "tech")]}
               for t, r in info.items()}
    (out / "tag_map.json").write_text(json.dumps(tag_map, ensure_ascii=False, indent=1), encoding="utf-8")

    keep = ["stationuuid", "name", "countrycode", "votes", "tags", "genres", "formats",
            "decades", "geo_tags", "lang_tags", "brand_tags", "features", "moods", "other_tags",
            "language_inferred"]
    out_rows = [{k: r[k] for k in keep} for r in results]
    (out / "stations_tags.json").write_text(json.dumps(out_rows, ensure_ascii=False), encoding="utf-8")
    try:
        pd.DataFrame(out_rows).to_parquet(out / "stations_tags.parquet", index=False)
    except ImportError:
        print("pyarrow not installed: skipped stations_tags.parquet", file=sys.stderr)

    report = render_report(path, results, counts, info, countries, bundle_score, cooc, args)
    (out / "tag_report.md").write_text(report, encoding="utf-8")
    print(report)
    return 0


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

def render_report(path, results, counts, info, countries, bundle_score, cooc, args) -> str:
    n = len(results)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    assignments = sum(counts.values())
    out = [f"# RadioPeck tag report\n\nGenerated: {stamp}  \nInput: {path} ({n} stations)\n"]

    out.append("## Station coverage after normalisation\n")
    headers = ["Metric"]
    cols = []
    for tier in TIERS:
        total, data = coverage(results, tier)
        headers.append("All stations" if tier == 0 else f"Votes >= {tier}")
        cols.append((total, data))
    rows = []
    for metric in cols[0][1]:
        rows.append([metric] + [cell(data[metric], total) for total, data in cols])
    rows.insert(0, ["Stations in group"] + [str(total) for total, _ in cols])
    out.append(md_table(headers, rows))

    lacking = [r for r in results if not r["language"]]
    inferred = [r for r in lacking if r["language_inferred"]]
    out.append(f"\n\n**Language.** {cell(n - len(lacking), n)} stations have a language in the catalogue; "
               f"{cell(len(inferred), len(lacking))} of the {len(lacking)} without one get a language from "
               f"their tags; after inference {cell(n - len(lacking) + len(inferred), n)} have a language.\n")

    out.append("## What the tags are\n")
    by_cat: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for tag, rec in info.items():
        by_cat[rec["category"]][0] += 1
        by_cat[rec["category"]][1] += counts[tag]
    order = sorted(by_cat, key=lambda c: -by_cat[c][1])
    out.append(md_table(
        ["Category", "Unique tags", "Share of unique", "Tag uses", "Share of uses"],
        [[c, by_cat[c][0], pct(by_cat[c][0], len(info)), by_cat[c][1], pct(by_cat[c][1], assignments)]
         for c in order]))
    out.append(f"\n\nUnique tags: {len(info)}; tag uses: {assignments}. "
               "Categories: generic = no information; bulk = unknown tag that always travels "
               "with the same group of tags; rare = used by one station; other = unmapped.\n")

    genre_counter = Counter(g for r in results for g in r["genres"])
    format_counter = Counter(f for r in results for f in r["formats"])
    decade_counter = Counter(d for r in results for d in r["decades"])
    out.append("## Genres (stations per canonical genre)\n")
    out.append(", ".join(f"{g} ({c})" for g, c in genre_counter.most_common(40)) or "none")
    out.append("\n\n## Formats\n")
    out.append(", ".join(f"{g} ({c})" for g, c in format_counter.most_common(20)) or "none")
    out.append("\n\n## Decades\n")
    out.append(", ".join(f"{g} ({c})" for g, c in sorted(decade_counter.items())) or "none")
    brand_counter = Counter(b for r in results for b in r["brand_tags"])
    out.append("\n\n## Networks and brands\n")
    out.append(", ".join(f"{g} ({c})" for g, c in brand_counter.most_common(20)) or "none")
    feature_counter = Counter(f for r in results for f in r["features"])
    out.append("\n\n## Features the station states about itself (not verified)\n")
    out.append(", ".join(f"{g} ({c})" for g, c in feature_counter.most_common()) or "none")
    mood_counter = Counter(f for r in results for f in r["moods"])
    out.append("\n\n## Moods and activities\n")
    out.append(", ".join(f"{g} ({c})" for g, c in mood_counter.most_common()) or "none")

    out.append("\n\n## Tags that travel in bundles\n")
    out.append("Tags on many stations that nearly always appear together with the same other tags. "
               "A natural tag such as `jazz` has a low score; a bulk-imported group has a high one. "
               f"Unmapped tags with a score of {args.bulk_score} or more are excluded from search as bulk.\n")
    bundle_rows = []
    for tag in sorted(bundle_score, key=lambda t: -counts[t]):
        if bundle_score[tag] < args.bulk_score:
            continue
        together = ", ".join(f"{u} {n_ / counts[tag]:.0%}" for u, n_ in cooc[tag].most_common(3))
        bundle_rows.append([tag, counts[tag], info[tag]["category"], f"{bundle_score[tag]:.2f}", together])
    out.append(md_table(["Tag", "Stations", "Category", "Bundle score", "Most common companions"],
                        bundle_rows[:25]) if bundle_rows else "No bundles found at this threshold.")

    sets = Counter(tuple(sorted(r["tags"])) for r in results if len(r["tags"]) >= 3)
    common_sets = [(s, c) for s, c in sets.most_common(10) if c >= 10]
    out.append("\n\n## Most common identical tag sets\n")
    out.append(md_table(["Stations", "Tags"],
                        [[c, ", ".join(s[:8]) + (" ..." if len(s) > 8 else "")] for s, c in common_sets])
               if common_sets else "No tag set is shared by 10 or more stations.")

    out.append("\n\n## Tags concentrated in one country\n")
    conc = []
    for tag, c in counts.items():
        if c < 200:
            continue
        cc, k = countries[tag].most_common(1)[0]
        if k / c >= 0.9:
            conc.append([tag, c, cc, f"{k / c:.0%}", info[tag]["category"]])
    conc.sort(key=lambda r: -r[1])
    out.append(md_table(["Tag", "Stations", "Country", "Share", "Category"], conc[:15])
               if conc else "No tag with 200+ stations is 90% from one country.")

    out.append("\n\n## Top unmapped tags (extend taxonomy.py from this list)\n")
    unmapped = sorted((t for t, r in info.items() if r["category"] == "other"), key=lambda t: -counts[t])
    rows = []
    for t in unmapped[:args.top_unmapped]:
        cc, k = countries[t].most_common(1)[0]
        rows.append([t, counts[t], f"{cc} {k / counts[t]:.0%}"])
    out.append(md_table(["Tag", "Stations", "Top country"], rows) if rows else "none")

    fuzzy = sorted((t for t, r in info.items() if r["source"].startswith("fuzzy:")), key=lambda t: -counts[t])
    out.append("\n\n## Near-miss matches to review (fuzzy)\n")
    out.append(md_table(["Tag", "Stations", "Matched to", "Genre"],
                        [[t, counts[t], info[t]["source"].split(":", 1)[1], info[t]["entries"][0][1]]
                         for t in fuzzy[:30]]) if fuzzy else "none")

    compound = sorted((t for t, r in info.items() if r["source"] == "compound"), key=lambda t: -counts[t])
    out.append("\n\n## Compound tags that were split\n")
    out.append(md_table(["Tag", "Stations", "Became"],
                        [[t, counts[t], ", ".join(f"{a}:{b}" for a, b in info[t]["entries"])]
                         for t in compound[:15]]) if compound else "none")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.exit(main())
