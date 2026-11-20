# RadioPeck

Search internet radio stations from a catalogue of ~32,000 live streams. Work in progress: the site already searches, filters and plays; semantic search is the next milestone.

**Live site: https://paulmoskow.github.io/radiopeck/**

## What works today

- Station list with name search and a country filter
- Built-in player (click a station to listen; HLS streams are not supported yet)
- Daily catalogue refresh and cleaning pipeline (GitHub Actions)
- Tag normalisation: raw, messy tags are mapped to genres, formats, decades, brands and moods

## What is planned

- Semantic search: multilingual embeddings computed in the pipeline, query embedding in the browser (Transformers.js)
- Hybrid ranking: BM25 + vectors + hard filters
- Enrichment of stations that have no tags (from name, country, language)
- Natural-language search bot, map

## Data

Stations come from the community-maintained [Radio Browser](https://www.radio-browser.info/) API. The pipeline keeps only stations whose last availability check passed and that have an HTTPS stream (required on an HTTPS site), then removes duplicates by stream URL and by name + country. Raw catalogue: ~53,000 stations; after cleaning: ~32,400.

Metadata quality is the main limitation. About a third of the stations have no tags at all, and after normalisation about 60% have at least a genre, format or decade. 

## Repository layout

```
pipeline/            Python: fetch_stations.py, normalize_tags.py, taxonomy.py
web/                 React + TypeScript + Vite site
  public/data/       stations.json served to the site
.github/workflows/   update-stations.yml (daily catalogue), deploy.yml (GitHub Pages)
```

## Run locally

Pipeline (Python 3.11+):

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; on macOS/Linux: source .venv/bin/activate
pip install -r pipeline/requirements.txt
python pipeline/fetch_stations.py      # writes data/stations.json, report.md
python pipeline/normalize_tags.py      # writes data/tags/tag_report.md
```

Site (Node 20.19+ or 22.12+):

```bash
cd web
npm install
npm run dev
```

The site reads `web/public/data/stations.json`. For now this file is copied from `data/` by hand.

## Tech

Python, pandas, GitHub Actions, React, TypeScript, Vite, GitHub Pages
