import json
from collections import Counter
from pathlib import Path

path = Path("web/public/data/stations.json")
data = json.loads(path.read_text(encoding="utf-8"))
stations = data if isinstance(data, list) else data.get("stations", data)

total = len(stations)
hls = sum(1 for s in stations if s.get("hls"))
codecs = Counter((s.get("codec") or "").strip().upper() or "(empty)" for s in stations)

print(f"Total stations: {total}")
print(f"HLS: {hls} ({hls / total:.1%})")
print()
print("Codec distribution:")
for codec, n in codecs.most_common():
    print(f"  {codec:<12} {n:>6}  {n / total:.1%}")

# HLS vs codec: HLS streams are often AAC, so look at them separately.
hls_codecs = Counter((s.get("codec") or "").strip().upper() or "(empty)" for s in stations if s.get("hls"))
print()
print("Codecs among HLS stations:")
for codec, n in hls_codecs.most_common():
    print(f"  {codec:<12} {n:>6}")

# Spot check: URLs that do not look like a plain stream.
suffixes = Counter()
for s in stations:
    url = (s.get("url_resolved") or "").split("?")[0].lower()
    ext = url.rsplit(".", 1)[-1] if "." in url.rsplit("/", 1)[-1] else "(none)"
    suffixes[ext if len(ext) <= 5 else "(other)"] += 1
print()
print("URL extensions:")
for ext, n in suffixes.most_common(12):
    print(f"  {ext:<10} {n:>6}")