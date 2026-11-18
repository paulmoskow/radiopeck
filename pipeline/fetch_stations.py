#!/usr/bin/env python3
"""RadioPeck pipeline, step 1: fetch, clean and profile the Radio Browser catalogue.

What it does
  1. Downloads the full station catalogue (including broken stations, so the
     funnel can show how many are lost at each step).
  2. Applies the cleaning steps one by one and records the count after each.
  3. Writes the cleaned catalogue plus a profile of metadata quality
     (tags, language, country, votes), which tells us what the search can
     realistically rely on.

Usage
  python pipeline/fetch_stations.py                    # fetch from the API
  python pipeline/fetch_stations.py --save-raw         # also keep the raw dump
  python pipeline/fetch_stations.py --input raw.json   # reuse a saved dump (no network)

Outputs (in --out, default: data/)
  stations.json     cleaned catalogue, compact fields
  stations.parquet  same data (only if pyarrow is installed)
  funnel.json       counts after every cleaning step
  report.md         human-readable report: funnel + metadata profile
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

# Radio Browser asks API clients to identify themselves. Put your repo URL here
# or set the RADIOPECK_USER_AGENT environment variable.
USER_AGENT = os.environ.get("RADIOPECK_USER_AGENT", "RadioPeck/0.1")

# Server discovery: the API is served by several mirrors. The discovery
# endpoint and the fallback hosts below are NOT checked against the docs yet,
# so confirm them at https://api.radio-browser.info/ before the first run.
DISCOVERY_URL = "https://all.api.radio-browser.info/json/servers"
FALLBACK_SERVERS = [
    "https://de1.api.radio-browser.info",
    "https://de2.api.radio-browser.info",
    "https://fi1.api.radio-browser.info",
]

KEEP_COLUMNS = [
    "stationuuid", "name", "url_resolved", "homepage", "favicon",
    "tags", "country", "countrycode", "state", "language",
    "codec", "bitrate", "hls", "votes", "clickcount",
    "geo_lat", "geo_long",
]

POPULARITY_THRESHOLDS = [0, 1, 5, 10, 50, 100]
MAX_TAG_LENGTH = 40  # longer "tags" are almost always sentences or junk


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #

def discover_servers(session: requests.Session) -> list[str]:
    """Return API mirrors in random order (spreads load across servers)."""
    try:
        resp = session.get(DISCOVERY_URL, timeout=30)
        resp.raise_for_status()
        servers = [f"https://{item['name']}" for item in resp.json() if item.get("name")]
    except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
        print(f"Server discovery failed ({exc}); using fallback list.", file=sys.stderr)
        servers = []
    servers = servers or list(FALLBACK_SERVERS)
    random.shuffle(servers)
    return servers


def fetch_catalogue(page_size: int = 10000, max_pages: int = 30) -> list[dict]:
    """Download every station, broken ones included, page by page."""
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    servers = discover_servers(session)
    print(f"Using {len(servers)} server(s), first: {servers[0]}")

    rows: list[dict] = []
    offset = 0
    for page in range(max_pages):
        params = {"hidebroken": "false", "order": "name", "limit": page_size, "offset": offset}
        batch = None
        for server in servers:
            try:
                resp = session.get(f"{server}/json/stations/search", params=params, timeout=120)
                resp.raise_for_status()
                batch = resp.json()
                break
            except (requests.RequestException, ValueError) as exc:
                print(f"  {server} failed on page {page}: {exc}", file=sys.stderr)
        if batch is None:
            raise RuntimeError("All Radio Browser servers failed; try again later.")
        rows.extend(batch)
        print(f"  page {page}: +{len(batch)} (total {len(rows)})")
        if len(batch) < page_size:
            break
        offset += page_size
        time.sleep(1)  # be polite to a free community API
    return rows


# --------------------------------------------------------------------------- #
# Cleaning helpers
# --------------------------------------------------------------------------- #

def split_csv(value) -> list[str]:
    """The API returns tags/languages as comma-separated strings; accept lists too."""
    if isinstance(value, list):
        items = value
    elif isinstance(value, str):
        items = value.split(",")
    else:
        items = []
    return [str(x).strip() for x in items if x is not None and str(x).strip()]


def clean_tags(value) -> list[str]:
    """Lower-case, strip '#', drop junk and duplicates, keep original order."""
    seen: dict[str, None] = {}
    for raw in split_csv(value):
        tag = unicodedata.normalize("NFKC", raw).casefold().lstrip("#").strip()
        tag = " ".join(tag.split())
        if tag and len(tag) <= MAX_TAG_LENGTH and not tag.isdigit():
            seen.setdefault(tag, None)
    return list(seen)


def name_key(name: str) -> str:
    text = unicodedata.normalize("NFKC", name or "").casefold()
    return " ".join(re.sub(r"[\W_]+", " ", text).split())


def stream_key(url: str) -> str:
    return re.sub(r"^https?://", "", (url or "").strip().lower()).rstrip("/")


def to_frame(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    for col in KEEP_COLUMNS + ["url", "lastcheckok"]:
        if col not in df.columns:
            df[col] = None

    for col in ["stationuuid", "name", "url_resolved", "homepage", "favicon",
                "country", "countrycode", "state", "codec"]:
        df[col] = df[col].fillna("").astype(str).str.strip()
    df["countrycode"] = df["countrycode"].str.upper()

    for col in ["votes", "clickcount", "bitrate"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["lastcheckok"] = pd.to_numeric(df["lastcheckok"], errors="coerce").fillna(0).astype(int) == 1
    df["hls"] = pd.to_numeric(df["hls"], errors="coerce").fillna(0).astype(int) == 1
    df["geo_lat"] = pd.to_numeric(df["geo_lat"], errors="coerce")
    df["geo_long"] = pd.to_numeric(df["geo_long"], errors="coerce")

    df["tags"] = df["tags"].map(clean_tags)
    df["language"] = df["language"].map(lambda v: [x.casefold() for x in split_csv(v)])
    return df


# --------------------------------------------------------------------------- #
# Funnel
# --------------------------------------------------------------------------- #

def run_funnel(df: pd.DataFrame, min_votes: int) -> tuple[pd.DataFrame, list[dict]]:
    funnel: list[dict] = []

    def record(key: str, label: str, frame: pd.DataFrame) -> pd.DataFrame:
        funnel.append({"step": key, "label": label, "count": int(len(frame))})
        return frame

    df = record("raw", "Records downloaded", df)
    df = record("unique_uuid", "After removing repeated station IDs (pagination overlap)",
                df.drop_duplicates(subset="stationuuid"))
    df = record("check_ok", "Stream passed the last availability check",
                df[df["lastcheckok"]])
    df = record("has_url", "Has a resolved stream URL",
                df[df["url_resolved"] != ""])
    df = record("https", "Stream URL is HTTPS (required on a GitHub Pages site)",
                df[df["url_resolved"].str.lower().str.startswith("https://")])

    # Keep the most popular record when the same station is listed several times.
    df = df.sort_values(["votes", "clickcount"], ascending=False, kind="stable")
    df = df.assign(_stream=df["url_resolved"].map(stream_key))
    df = record("dedup_stream", "After removing duplicate stream URLs",
                df.drop_duplicates(subset="_stream"))
    df = df.assign(_name=df["name"].map(name_key))
    df = df[df["_name"] != ""]
    df = record("dedup_name", "After removing same name + country duplicates",
                df.drop_duplicates(subset=["_name", "countrycode"]))
    df = df.drop(columns=["_stream", "_name"])

    if min_votes > 0:
        df = record("min_votes", f"Votes >= {min_votes}", df[df["votes"] >= min_votes])

    return df.reset_index(drop=True), funnel


# --------------------------------------------------------------------------- #
# Profile of metadata quality
# --------------------------------------------------------------------------- #

def pct(part: int, whole: int) -> str:
    return f"{100 * part / whole:.1f}%" if whole else "n/a"


def profile(df: pd.DataFrame) -> dict:
    n = len(df)
    tag_counts = df["tags"].map(len)
    tag_counter = Counter(t for tags in df["tags"] for t in tags)
    lang_counter = Counter(l for langs in df["language"] for l in langs)

    thresholds = []
    for t in POPULARITY_THRESHOLDS:
        sub = df[df["votes"] >= t]
        m = len(sub)
        sub_tags = sub["tags"].map(len)
        thresholds.append({
            "min_votes": t,
            "stations": m,
            "with_1plus_tags": int((sub_tags >= 1).sum()),
            "with_3plus_tags": int((sub_tags >= 3).sum()),
            "with_language": int((sub["language"].map(len) > 0).sum()),
        })

    return {
        "stations": n,
        "tag_buckets": {
            "0 tags": int((tag_counts == 0).sum()),
            "1-2 tags": int(((tag_counts >= 1) & (tag_counts <= 2)).sum()),
            "3-5 tags": int(((tag_counts >= 3) & (tag_counts <= 5)).sum()),
            "6+ tags": int((tag_counts >= 6).sum()),
        },
        "unique_tags": len(tag_counter),
        "tags_used_once": sum(1 for c in tag_counter.values() if c == 1),
        "top_tags": tag_counter.most_common(25),
        "fields": {
            "language": int((df["language"].map(len) > 0).sum()),
            "country code": int((df["countrycode"] != "").sum()),
            "state/region": int((df["state"] != "").sum()),
            "coordinates": int(df["geo_lat"].notna().sum()),
            "homepage": int((df["homepage"] != "").sum()),
            "favicon": int((df["favicon"] != "").sum()),
            "bitrate known": int((df["bitrate"] > 0).sum()),
        },
        "top_languages": lang_counter.most_common(10),
        "top_countries": df["countrycode"].replace("", "??").value_counts().head(15).items(),
        "codecs": df["codec"].str.upper().replace("", "UNKNOWN").value_counts().head(8).items(),
        "hls": int(df["hls"].sum()),
        "thresholds": thresholds,
    }


def md_table(headers: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def render_report(funnel: list[dict], prof: dict, generated_at: str) -> str:
    n = prof["stations"]
    first = funnel[0]["count"]
    parts = [f"# RadioPeck catalogue report\n\nGenerated: {generated_at}\n"]

    parts.append("## Filtering funnel\n")
    prev = None
    rows = []
    for step in funnel:
        kept = pct(step["count"], first)
        lost = "" if prev is None else f"-{prev - step['count']}"
        rows.append([step["label"], step["count"], kept, lost])
        prev = step["count"]
    parts.append(md_table(["Step", "Stations", "Of raw", "Lost"], rows))

    parts.append(f"\n\n## Metadata quality ({n} stations after cleaning)\n")
    parts.append(md_table(
        ["Tags per station", "Stations", "Share"],
        [[k, v, pct(v, n)] for k, v in prof["tag_buckets"].items()],
    ))
    parts.append(
        f"\n\nUnique tags: {prof['unique_tags']}; "
        f"used by a single station only: {prof['tags_used_once']} "
        f"({pct(prof['tags_used_once'], prof['unique_tags'])}).\n"
    )
    parts.append(md_table(
        ["Field filled in", "Stations", "Share"],
        [[k, v, pct(v, n)] for k, v in prof["fields"].items()],
    ))

    parts.append("\n\n## Volume vs popularity\n")
    parts.append(md_table(
        ["Min votes", "Stations", "With 1+ tags", "With 3+ tags", "With language"],
        [[t["min_votes"], t["stations"],
          pct(t["with_1plus_tags"], t["stations"]),
          pct(t["with_3plus_tags"], t["stations"]),
          pct(t["with_language"], t["stations"])] for t in prof["thresholds"]],
    ))

    parts.append("\n\n## Top tags\n")
    parts.append(", ".join(f"{t} ({c})" for t, c in prof["top_tags"]))
    parts.append("\n\n## Top languages\n")
    parts.append(", ".join(f"{t} ({c})" for t, c in prof["top_languages"]))
    parts.append("\n\n## Top countries\n")
    parts.append(", ".join(f"{t} ({c})" for t, c in prof["top_countries"]))
    parts.append("\n\n## Codecs\n")
    parts.append(", ".join(f"{t} ({c})" for t, c in prof["codecs"]))
    parts.append(f"\n\nHLS streams (need hls.js in Chrome/Firefox): {prof['hls']} ({pct(prof['hls'], n)})\n")
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, help="reuse a raw JSON dump instead of calling the API")
    ap.add_argument("--save-raw", action="store_true", help="save the raw API response to <out>/stations_raw.json")
    ap.add_argument("--out", type=Path, default=Path("data"), help="output directory (default: data)")
    ap.add_argument("--min-votes", type=int, default=0, help="drop stations below this vote count (default: keep all)")
    ap.add_argument("--page-size", type=int, default=10000)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    if args.input:
        rows = json.loads(args.input.read_text(encoding="utf-8"))
        print(f"Loaded {len(rows)} raw records from {args.input}")
    else:
        rows = fetch_catalogue(page_size=args.page_size)
        if args.save_raw:
            (args.out / "stations_raw.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

    df, funnel = run_funnel(to_frame(rows), args.min_votes)
    if df.empty:
        print("No stations left after cleaning; check the input.", file=sys.stderr)
        return 1

    prof = profile(df)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    out_df = df[KEEP_COLUMNS]
    out_df.to_json(args.out / "stations.json", orient="records", force_ascii=False)
    try:
        out_df.to_parquet(args.out / "stations.parquet", index=False)
    except ImportError:
        print("pyarrow not installed: skipped stations.parquet", file=sys.stderr)

    (args.out / "funnel.json").write_text(
        json.dumps({"generated_at": generated_at, "funnel": funnel}, indent=2), encoding="utf-8")
    report = render_report(funnel, prof, generated_at)
    (args.out / "report.md").write_text(report, encoding="utf-8")

    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
