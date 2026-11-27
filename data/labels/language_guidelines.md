# Language labelling guidelines

Goal: map every raw `language` value from the catalogue to a language code.

## Code format
- ISO 639-1 (two letters: `en`, `es`, `de`) whenever the language has one.
- Otherwise ISO 639-3 or 639-2 (three letters, e.g. `yue`, `nan`, `gsw`); the `note` column says so.
- Several languages in one value: codes joined with `|` in the order written, e.g. `en|pt|es`.
- Not a language, or impossible to tell: `?`.

## Rules
1. **Region and dialect labels collapse to the base language.** `american english`, `brazilian portuguese`, `español mexico`, `deutsch fränkisch` -> `en`, `pt`, `es`, `de`. The region is not kept.
2. **Native names, typos and truncations map to the intended language.** `română`, `espanish`, `deutch`, `hind` -> `ro`, `es`, `de`, `hi`.
3. **A country name used as a language maps to its dominant official language, only when there is one clear choice.** `romania` -> `ro`, `spain` -> `es`. Multilingual or unclear countries (`canada`, `usa`, `africa`, `belgie`) -> `?`.
4. **Chinese varieties.** `chinese` and `mandarin` -> `zh`. `cantonese` -> `yue`, `hokkien`, `teochew` and `chaoshan dialect` -> `nan`, `hakka` -> `hak`.
5. **Language groups with no single code** (`gaelic`, `creole`, `pidgin`, `kreyol`): `?`, unless the value names the exact language (`haitian creole` -> `ht`).
6. **Genres, tags, places and junk** (`rock`, `80s`, `online radio`, `willemstad`, `111`): `?`.
7. **Moldovan = Romanian** (`ro`), because Moldovan has no separate ISO code.
8. When unsure, use `?` rather than guess. A wrong code is worse than a missing one.

## Known judgement calls to review
- `norwegian`, `norsk` -> `no` (macrolanguage; not split into `nb`/`nn`).
- `filipino` -> `fil`, `tagalog` -> `tl` (kept separate).
- `amazigh`, `berbere`, `tamazight` -> `ber` (family code).
- `tonga` -> `to` (could also be a place name).
- `java` -> `jv` (could also be the programming language).
- `yugoslavian`, `bohemian`, `guangdong`, `mexicano`, `hindu` -> `?`.
