# Selectable Chinese languages

Simplified Chinese remains unchanged. A separate selectable 繁體中文 /
ChineseTraditional (zh-TW) first pass now uses the same registry, persistence,
English fallback and runtime switching, with `Fonts/ChineseTraditional/`.
See [Traditional Chinese coverage, fonts and current limits](TRADITIONAL_CHINESE.md).
The following records the completed Simplified Chinese migration.

Current language is **ChineseSimplified / 简体中文**, not an English-column
replacement. Use the rebuilt `dist/local-labels/PoseidonGame.exe`, working directory
`game-local/Remastered`, and the absolute `--mod .../@zhcn-prototype` path.
Under Options → Game → Text language select 简体中文, then leave the dialog normally.
The existing settings writer persists `textLanguage="ChineseSimplified"`; keep
`voiceLanguage="English"`. No language CLI argument is needed for normal use.

## Mechanism and migration

- Mod `bin/config-extra.cpp` extends existing `CfgLanguages` with UTF-8, English
  fallback, English audio and a language-specific font directory. The winning
  mod's extra is reapplied after restoring remaster defaults from the stock extra;
  removing the mod leaves the original eight-language registry.
- All **11,135 existing Chinese cells across 216 tables** were moved unchanged
  into `ChineseSimplified`; an exact pre-migration wording/ordered-key audit passed.
  Original English/French/Italian/Spanish/German/Czech/Polish/Russian values were
  restored from verified stock sources using the engine's CSV/encoding rules.
  Existing caption/reference repairs and the byte-identical Combined Arms mirror
  remain. Authored coverage is CWC 78 folders/1,928 keys, Resistance 39/1,310,
  standalone 24/1,284, multiplayer 30/(1,511 stock + 27 display keys), wizard
  36/2,198; shared stock globals remain **2,706**. Terrain remains 62 entries.
- Eleven campaign/chapter display keys reuse the already-finished wording.
  Optional `nameKey` metadata leaves the original campaign `name` literals intact,
  preserving exact no-mod fallback. Resistance's two existing Viktor/Victor
  identities now use a separate canonical-only table key plus their existing
  display key. Its Chinese cell is stock English `Victor Troska`; all eight stock
  cells exactly retain the original name, including Czech `Viktor Troska` and
  Polish `Wiktor Troska`. This one additional non-display metadata key is not
  included in the 1,310 authored translation count. Script/save/network names must
  not acquire Chinese text or lose their original other-language spelling.
- Missing language columns and empty Chinese cells fall back to stock English.
  `LocalizeStringWithFallback()` returns the exact supplied fallback pointer for
  missing/empty keys, not a dangling missing-key diagnostic. Found pointers are
  borrowed until the table reloads.
- The five unchanged fonts are deployed under
  `@zhcn-prototype/Fonts/ChineseSimplified/`. Registry metadata opts into this
  routing only for Chinese. Language switches refresh font caches before existing
  display callbacks. Stock languages use stock fonts; no TTF bytes/design changed.
- Wizard generation preserves raw Intel title/description references when saving
  a generated mission. Otherwise a title generated in Chinese becomes a Chinese
  literal even after switching to English. Original user-entered literals remain
  literals. No mission logic, scripts, original audio or lip-sync is changed.

## Deployment and reversal

The README's current manual deployment copies all tables, campaign display
metadata and `mod/bin/config-extra.cpp`, puts fonts in the language subdirectory,
and runs the existing terrain/wizard/MP/UI builders. Validators check deployment
equality and all eight stock columns; builders still create ignored local-only
stock-derived overlays, never redistribute commercial assets.

For an older English-column installation, close the game first. Verify and retire
the previous **five flat** `@zhcn-prototype/Fonts/cwr_*.ttf` copies; leaving them
there still overrides stock fonts. Likewise, the old 36 wizard and 30 MP banks
must be retired only after validating them against their previous supported build,
then regenerated: builders intentionally reject unrecognized pre-existing output.
This installation's verified banks were archived under
`game-local/localization-backup/language-migration-banks`, not deleted.
Do not overwrite any original-source backup with localized files.

Disabling the mod restores the stock language registry, global text and fonts.
Directly deployed campaign/standalone tables now retain stock language columns;
complete asset reversal still follows their original hash-checked backup inventories.
Remove only patch-owned extras/overlays for full reversal. The original GOG
executable and commercial PBOs/base fonts remain untouched.

## Runtime checks and validation

Rebuilt GL33 client, isolated GOG Remastered 3.05 installation, 1280×900:

- UI language stepper: English → 简体中文 → English → Français → 简体中文;
  stock settings text/fonts returned immediately. Normal exit and restart without
  `--lang` retained Chinese text and English voices. Main/settings labels readable.
- CWC Combined Arms: Chinese briefing/objectives, generated identity/group title,
  gameplay HUD and opening M16A2 dialogue. Live English/French switching restored
  stock briefing text, markers, names and fonts. `name player` was David Armstrong.
- Resistance: introductory news subtitles, Crossroad briefing/map and gameplay
  actions. Nogova's Dolina label appeared as 多利纳. Canonical name was Victor Troska.
  A bounded `setIdentity "Viktor"` harness check returned stock `Wiktor Troska`
  in Polish and `Victor Troska` in Chinese, while display names followed the selected
  language. The canonical-key fix was deployed and retested in this briefing.
- Bomberman: Chinese briefing/objectives/markers, playable gameplay, equipment and
  M21 encyclopedia description. Live English restored stock encyclopedia/markers.
- Editor: unit-properties dialog, ranks, side/class/player choices and controls.
- Wizard Clean Sweep: actual newly generated mission briefing/gameplay; Chinese
  Morton label, then stock English title/body/markers/terrain after live switching.
  The discovered cached-title bug was fixed, rebuilt and physically retested.
- Authored Everon Sector Control: selection, local single-host lobby, briefing,
  terrain labels, playable gameplay and time/HUD text. French switching restored
  stock mission/briefing/group/terrain text. No second client or online session.
- No-mod English: stock main menu/campaign label and Bomberman briefing/objectives,
  generated group label and fonts. No Chinese leak appeared in these comparisons.

All five localization validators and terrain/wizard/MP/UI deployment `--check`
commands pass, including UTF-8, formats/links/references, five-font glyph coverage,
stock columns and original commercial hashes. Stock CSV regressions: 3 pass.
Client, core-test and normal UI-test builds pass. Focused stringtable/language/config
tests: 56 cases/222 assertions; Chinese loader tests: 2/20; language/font/settings/
campaign/wizard tests: 20/121. Core excluding external-data: 826 passed, four
game-data scans skipped, 6,373 assertions passed. Broader UI `[localization]`:
9 passed, six failed because required `packages/Remaster` data fixtures are absent;
this remains a fixture limitation, not a full-suite PASS.

Limits: no full campaign replay, exhaustive foreign-language UI walk, online/second-
client checks or new ending/debriefing playthrough. All eight columns are statically
validated; English/French received representative runtime checks. Eleven previously
documented stock standalone audio references have no source captions. Existing
key-label clipping and mixed Latin/title-font proportions were subsequently
addressed in [the typography pass](TYPOGRAPHY.md), together with Chinese wrapping.
Windows automatic primary-language selection stays conservative (`win32=0` avoids
treating Traditional Chinese as Simplified); explicit selection works. Traditional
Chinese's first pass is now implemented; regional editorial review and distribution
remain separate unfinished work. Neither Chinese pass redesigns layouts.
