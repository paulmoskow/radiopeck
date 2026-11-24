# RadioPeck

Search and listen radio stations online from a catalogue of ~32,000 live streams. Work in progress: the site already searches, filters and plays (including HLS); semantic search is in development.

**Live site: https://paulmoskow.github.io/radiopeck/**

## What works today

- Station list with name search and a country filter, responsive layout for desktop and phones
- Player with the station logo, country and main tags; MP3, AAC and OGG play natively, HLS streams play through [hls.js](https://github.com/video-dev/hls.js) (Safari uses its native HLS)
- Installable as an app (PWA) with its own window and icon; lock-screen controls with the station name and cover (Media Session API)
- Unit tests (Vitest) for the helper functions
- Daily catalogue refresh and cleaning pipeline; the site is rebuilt with the fresh catalogue after every refresh (GitHub Actions)
- Tag normalisation: raw, messy tags are mapped to genres, formats, decades, brands and moods
- Language normalisation: 503 raw spellings (`español mexico`, `deutsch fränkisch`, `pt-br`...) mapped to ISO language codes with a written labelling guideline

## Install as an app

RadioPeck is a progressive web app: it opens in its own window, without the browser toolbar, and gets an icon of its own.

| Device | How |
|---|---|
| Desktop (Chrome, Edge) | Click the install icon on the right of the address bar, or menu → *Install RadioPeck* |
| Android (Chrome) | Menu (⋮) → *Install app* (or *Add to Home screen*) |
| iPhone / iPad (Safari) | Share button → *Add to Home Screen*. Safari has no install button; this is an iOS limitation. On iOS 16.4+ Chrome and Edge offer the same through their Share menu |

Playback continues with the screen locked, and the lock screen shows the station name with play and pause controls. The app shell is cached by a service worker; the station catalogue and the audio streams are never cached.

## What is planned

- Semantic search: multilingual embeddings computed in the pipeline, query embedding in the browser (Transformers.js)
- Hybrid ranking: BM25 + vectors + hard filters, with an evaluation set (recall@10, nDCG@10)
- Enrichment of stations that have no tags (from name, country, language)
- Tests for the site and the pipeline
- Natural-language search bot, map

## Data

Stations come from the community-maintained [Radio Browser](https://www.radio-browser.info/) API. The pipeline keeps only stations whose last availability check passed and that have an HTTPS stream (required on an HTTPS site), then removes duplicates by stream URL and by name + country. Raw catalogue: ~53,000 stations; after cleaning: ~32,400.

Metadata quality is the main limitation:

- **Tags.** About a third of the stations have no tags at all; after normalisation about 60% have at least a genre, format or decade.
- **Language.** 64% of stations have a language code after normalisation. For stations without one, a language is inferred from the country when one language clearly dominates it (at least 85% of labelled stations, at least 20 of them). This raises coverage to about 93%. These inferred values are stored with `source: "country"`, so they stay separable from labelled data. Their accuracy has not been measured yet.
- **Formats.** About 92% of streams play natively in a browser, ~8% are HLS. An HLS stream only plays if its server allows cross-origin requests (CORS); some will not.

## Repository layout

```
pipeline/            Python: fetch, tag and language normalisation, documents for embeddings
  fetch_stations.py, normalize_tags.py, taxonomy.py
  apply_language_map.py, enrich_language_by_country.py
  build_documents.py, build_embeddings.py
data/labels/         hand-made labels: language_map.csv, language_guidelines.md
web/                 React + TypeScript + Vite site (installable PWA)
docs/                
.github/workflows/   update-stations.yml (daily catalogue), deploy.yml (GitHub Pages)
```

The daily workflow stores the full catalogue as a workflow artifact (it is too large and changes too often to commit). The deploy workflow downloads the latest artifact, copies it to `web/public/data/` and builds the site, and it runs again after every catalogue refresh.

## Run locally

Pipeline (Python 3.11+):

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; on macOS/Linux: source .venv/bin/activate
pip install -r pipeline/requirements.txt
python pipeline/fetch_stations.py --out data     # writes data/stations.json, report.md
python pipeline/normalize_tags.py                # writes data/tags/tag_report.md
python pipeline/apply_language_map.py            # language codes from data/labels/language_map.csv
python pipeline/enrich_language_by_country.py    # adds country-based language guesses
python pipeline/build_documents.py               # one text per station, for embeddings
```

Computing embeddings needs `pip install sentence-transformers` and downloads the model on first run:

```bash
python pipeline/build_embeddings.py
```

Site (Node 20.19+ or 22.12+):

```bash
cd web
npm install
npm run dev
```

The site reads `web/public/data/stations.json`. For local development copy `data/stations.json` there; CI does this automatically on deploy.

## Tech

Python, GitHub Actions, React, TypeScript, Vite, hls.js, vite-plugin-pwa, GitHub Pages

## Author

Pavel Moskov, [github.com/paulmoskow](https://github.com/paulmoskow)