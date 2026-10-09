# Built-in terrain-map labels

The stock GOG Remastered 3.05 map labels are configuration values, **not baked
terrain lettering**. `CStaticMap::OnDraw` in
`engine/Poseidon/UI/Map/UIMap.cpp` reads `CfgWorlds/<world>/Names` in stock order;
`DrawName` uses each entry's position and decoded `name`. Its font, size, zoom
limits, distance-based label suppression and clipping remain unchanged.

| Island / internal world | Stock source | Labels localized |
| --- | --- | --- |
| Everon / Eden | `BIN/CONFIG.BIN` | 18 |
| Malden / Abel | `BIN/CONFIG.BIN` | 14 |
| Kolgujev / Cain | `BIN/CONFIG.BIN` | 0 — stock `Names` is empty |
| Nogova / Noe | `AddOns/Noe.pbo`, member `config.bin` | 30 |

## Mechanism and boundaries

Stock Eden/Abel/Cain classes use `access=3`; Noe uses `access=2`. These are
read-only (`ParamFile.hpp`, `ParamClass::Update` in `ParamFile.cpp`). A partial
add-on cannot replace their existing names. A mod's `bin/config` replaces the
whole master config, rather than merging omitted stock classes back in
(`Asset/Addon/ConfigParsers.cpp`). Therefore a small partial master config is
also unsuitable.

`build_labels.py` builds ready-made APL-SA mod copies from stock 3.05 data on
the developer machine. It changes exactly 32 master-config and 30 Noe-config `name` values
to `$STR_CWRC_MAP_<world>_<original location ID>` references. The normal ParamFile
stringtable lookup resolves those references; the existing UTF-8 sibling-shard
loader loads `mod/bin/stringtable_terrain.utf8.csv`. No engine changes are needed.

The shard supplies Chinese in English mode, as the existing patch does. Its
seven other language columns repeat each exact stock visible label (including
`Saint Phillippe` and `Velka ves`). Thus **these labels** remain stock in other
languages; this does not claim the rest of the existing English-column patch
has proper multilingual isolation yet. All internal class IDs, including stock
misspellings `SaintPhillippe`, `EnreDeux` and `Goisee`, remain untouched.

Before generation, the script verifies the two exact GOG 3.05 SHA-256 hashes
recorded in `INPUTS`. Unmodified configs must round-trip byte-for-byte; modified
configs are reparsed and compared against changes to `name` properties only.
All positions, class/key order, access modes, evaluator variables, other world
settings and non-name configuration remain stock. Both non-config Noe PBO
members remain byte-identical. The original files are never written.

Generated files remain ignored build outputs, but may ship in the ZIP under
APL-SA: Bohemia's official CWR README licenses retail game data accordingly.
See ../DISTRIBUTION.md for attribution/terms and the current ready-made workflow.
Players never run this builder. The manual commands below are development history.

## Deployment / reversal

Close the game. Deploy the existing Chinese mod and fonts first, then run from
the repo root with the existing fontTools dependency available:

```text
python localization/zhcn-combined-arms/terrain/build_labels.py game-local/Remastered
python localization/zhcn-combined-arms/terrain/build_labels.py game-local/Remastered --check
```

Outputs under `game-local/Remastered/@zhcn-prototype/`:

- `bin/config.bin` — generated full stock master with only label references changed.
- `AddOns/Noe.pbo` — local stock island archive with only its config names changed.
- `bin/stringtable_terrain.utf8.csv` — byte-identical to the repository shard.

Launch the same executable with the existing `--mod .../@zhcn-prototype` and
select 简体中文 (or use `--lang ChineseSimplified` for a disposable test).
English and other stock columns retain the original labels. See
[current language support](../LANGUAGE_SUPPORT.md). Regenerate after an authored terrain-shard update. Unsupported
stock hashes fail before output writes. Pre-existing unrelated master config or
Noe overlays are rejected; do not combine this with a config-replacement or
Noe-replacement mod without a separately reviewed merge.
Both generation and `--check` reject an existing mod `bin/config.cpp` before
any writes, including case variants such as `CONFIG.CPP` and `Config.cpp` on
case-sensitive filesystems, because the engine's filename lookup is
case-insensitive and prefers it to `config.bin`. The conflicting file is left
untouched.

To reverse **only this addition**, with the game closed remove those three exact
generated files, not their directories or stock counterparts. Alternatively,
launching without the mod restores stock map labels immediately. Neither option
reverses campaign/standalone CSV replacements; their original reversal
instructions still apply. No stock backup needs to be overwritten.

## Glossary

All 62 exact stock labels and their Chinese forms are in
[locally reconstructed `stringtable_terrain.utf8.csv`](../distribution/payload.json).
Existing campaign and standalone mappings are reused. These 17 newly encountered
Nogova labels use transliterations, not semantic translations:

| Stock label | Chinese | Stock label | Chinese |
| --- | --- | --- | --- |
| Paseky | 帕塞基 | Mala ves | 马拉韦斯 |
| Kvilda | 克维尔达 | Lany | 拉尼 |
| Kost | 科斯特 | Mokra vrata | 莫克拉弗拉塔 |
| Frymburk | 弗林布尔克 | Slapy | 斯拉皮 |
| Varta | 瓦尔塔 | Loukov | 洛乌科夫 |
| Trosky | 特罗斯基 | Joudov | 约乌多夫 |
| Vidlakov | 维德拉科夫 | Bitov | 比托夫 |
| St. Sedlo | 斯特塞德洛 | Okrouhlo | 奥克罗乌赫洛 |
| Bor | 博尔 | | |

`St. Sedlo` is retained as the verified stock spelling; its abbreviation is not
silently expanded to an assumed saint/place name. No locations are invented
for Kolgujev, and names absent from stock `Names` (for example Nová Ves or
Kiusk) do not acquire a new built-in label.

## Verification and remaining limits

Actual installed GOG 3.05 `PoseidonGame.exe`, GL33, 1280×900, isolated test profile:

- Combined Arms preview/play: Chinese built-in 雷吉纳、莱维、拉兰斯、迪拉斯、
  韦尔农; keyboard pan to 蒙蒂尼亚克、格拉韦特、昂特尔德、普罗万、菲加里、莫顿.
  Original objective markers and moving unit/waypoint icons remained visible.
- Pathfinder preview/play: 圣玛丽、沙普瓦、康孔、勒波尔; pan north to 乌当、杜尔当、
  阿吕迪、拉特里尼泰、拉尔什、圣路易. Objectives and mission markers displayed.
- Resistance Occupation (10a) preview/play: 米罗夫、莫德拉瓦、彼得罗维采;
  pan southeast to 利帕尼、拉尼、博尔、维尔卡韦斯、马拉韦斯 and nearby new names.
  Nogova's original terrain loaded from the local derived PBO normally.
- Incursion preview/play: Kolgujev terrain, briefing, markers and map opened
  normally; no stock town labels existed to translate.
- French with the mod enabled: Everon editor map retained stock Latin labels
  Montignac, Gravette, Provins, Figari and Le Moule. English without the mod
  showed the same stock labels. Other language columns were checked statically.

Zoom and keyboard panning were exercised; no missing glyphs, mojibake or new
label-to-label collisions appeared. Stock high-zoom names can be large, and
mission markers can overlap town lettering at their unchanged positions
(notably Pathfinder's Sainte Marie/Chapoi targets). Map gadgets and screen
edges still occlude/clip content normally. Other resolutions/zoom combinations
and third-party terrains/mod combinations are untested.

All three existing localization validators pass with unchanged campaign prose,
keys, references, marker targets and caption repairs. The generator's `--check`
passes complete 62-entry coverage, strict CSV/UTF-8, all five font cmaps, semantic
preservation and deployment equality. The validators still confirm 7,461 older
unrelated installed files unchanged; the three new mod files are separately
verified by the builder. No engine/UI source, fonts, scripts, audio or lip-sync
changed; no affected engine build/tests were required.

Marker links are preserved statically, but **successful link clicks were not
verified in this pass**: injected pointer movement did not move the game's
internal UI cursor reliably. This is not a claim that a clicked link passed.
No full mission playthrough was performed.

The initial terrain-overlay pass did not change bilingual prose. The subsequent
[selective retirement review](../BILINGUAL_NAMES.md) removes town-name Latin
suffixes only where this same-island mapping confirms a Chinese built-in label.
Island and unlabelled-place references remain bilingual. The updated text
requires these overlays; do not deploy it alone onto Latin-only terrain maps.
