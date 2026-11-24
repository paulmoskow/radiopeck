import json
import re
from pathlib import Path

STATIONS = Path("web/public/data/stations.json")
TAGS = Path("data/tags/stations_tags.json")
LANGS = Path("data/tags/stations_languages_enriched.json")
OUT = Path("data/embeddings/documents.jsonl")

LANG_NAMES = {
    "en": "English", "es": "Spanish", "de": "German", "fr": "French", "zh": "Chinese",
    "pt": "Portuguese", "ru": "Russian", "it": "Italian", "el": "Greek", "ro": "Romanian",
    "nl": "Dutch", "ar": "Arabic", "pl": "Polish", "hi": "Hindi", "tr": "Turkish",
    "ta": "Tamil", "sr": "Serbian", "ne": "Nepali", "id": "Indonesian", "hu": "Hungarian",
    "uk": "Ukrainian", "bg": "Bulgarian", "cs": "Czech", "sv": "Swedish", "ca": "Catalan",
    "ja": "Japanese", "ko": "Korean", "fi": "Finnish", "da": "Danish", "no": "Norwegian",
    "he": "Hebrew", "th": "Thai", "hr": "Croatian", "sk": "Slovak", "lv": "Latvian",
}

COUNTRY_ALIASES = {
    "Bolivarian Republic Of Venezuela": "Venezuela",
    "Islamic Republic Of Iran": "Iran",
    "Republic Of North Macedonia": "North Macedonia",
    "State Of Palestine": "Palestine",
    "Taiwan, Republic Of China": "Taiwan",
    "United Republic Of Tanzania": "Tanzania",
    "The Congo": "Republic of the Congo",
    "The Democratic Republic Of The Congo": "DR Congo",
    "The Democratic Peoples Republic Of Korea": "North Korea",
    "The Republic Of Korea": "South Korea",
    "The Falkland Islands Malvinas": "Falkland Islands",
    "The Cocos Keeling Islands": "Cocos Islands",
    "The Holy See": "Vatican City",
    "The Lao Peoples Democratic Republic": "Laos",
    "The Republic Of Moldova": "Moldova",
    "The Russian Federation": "Russia",
    "The United Kingdom Of Great Britain And Northern Ireland": "United Kingdom",
    "The United States Of America": "United States",
    "The United States Minor Outlying Islands": "US Minor Outlying Islands",
}

def clean_name(name):
    """Drop technical suffixes like '| MP3' or '- 128 kbps' from the station name."""
    return re.sub(r"\s*[|\-–]\s*(MP3|AAC\+?|OGG|FLAC|HD|\d+\s*kbps)\s*$", "", name, flags=re.I).strip()

def clean_country(country):
    """Short, everyday country name; strips a leading 'The ' for the rest."""
    if not country:
        return country
    return COUNTRY_ALIASES.get(country, country.removeprefix("The "))

def document_text(name, country, languages, tags):
    """Build the text that will be embedded for one station"""
    parts = [f"{name}."]
    if country:
        parts.append(f"Country: {country}.")
    if languages:
        parts.append(f"Language: {', '.join(languages)}.")

    fields = [
        ("Genres", "genres"),
        ("Format", "formats"),
        ("Decade", "decades"),
        ("Mood", "moods"),
        ("Features", "features"),
        ("Place", "geo_tags"),
        ("Brand", "brand_tags"),
    ]
    for label, key in fields:
        values = tags.get(key) or []
        if values:
            parts.append(f"{label}: {', '.join(values)}.")

    return " ".join(parts)


def is_weak(tags):
    """A station is 'weak' if it has no genre, format, decade or mood."""
    return not (tags["genres"] or tags["formats"] or tags["decades"] or tags["moods"])


def main():
    stations = json.loads(STATIONS.read_text(encoding="utf-8"))
    stations = stations if isinstance(stations, list) else stations.get("stations", stations)
    by_uuid = {s["stationuuid"]: s for s in stations}
    tag_records = json.loads(TAGS.read_text(encoding="utf-8"))
    langs = json.loads(LANGS.read_text(encoding="utf-8"))


    OUT.parent.mkdir(parents=True, exist_ok=True)
    weak_count = 0
    with OUT.open("w", encoding="utf-8") as f:
        for t in tag_records:
            uuid = t["stationuuid"]
            s = by_uuid.get(uuid)
            if not s:
                continue
            codes = langs.get(uuid, {}).get("codes", [])
            names = [LANG_NAMES.get(c, c) for c in codes]
            weak = is_weak(t)
            weak_count += weak
            record = {
                "id": uuid,
                "text": document_text(clean_name(s["name"]), clean_country(s.get("country", "")), names, t),
                "weak": weak,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote {len(tag_records)} documents to {OUT}; weak: {weak_count}")
    # Look at a few by eye: this is the part that decides search quality.
    with OUT.open(encoding="utf-8") as f:
        for _, line in zip(range(8), f):
            print(" ", json.loads(line)["text"])


if __name__ == "__main__":
    main()