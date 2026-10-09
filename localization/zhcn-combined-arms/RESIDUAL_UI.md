# Residual UI coverage: Phase 1 complete

Source: the installed, original GOG Remastered 3.05 BIN tables and addon/template
PBOs, not historical Chinese text. Campaign/standalone prose, canonical identity
metadata and the 62 terrain mappings are unchanged. Proper Chinese language
registration is now complete in [LANGUAGE_SUPPORT.md](LANGUAGE_SUPPORT.md).
This file records the Phase 1 coverage and tests; presentation polish remains.

## Added coverage

- `mod/bin/stringtable_ui.utf8.csv`: **1,579 new stock-key overrides**, bringing
  shared stock-key coverage from 1,127 to **2,706**. Menus, profiles, difficulty,
  graphics/audio/display/game/control settings and explanatory tooltips, key/device
  labels, abbreviated roster ranks and skill levels, editor dialogs and options,
  multiplayer browsing/hosting/connection/chat/status/errors, loading/death text,
  credits headings, remaining equipment names and complete encyclopedia descriptions.
  Original French/Italian/Spanish/German/Czech/Polish/Russian column text is
  preserved in UTF-8; missing stock columns retain their stock English fallback.
  Stock extraction skips separator spaces before quotes, as the engine does;
  a follow-up repaired eight shifted ammo-crate rows and 36 leading-space-only
  rows in the non-Chinese columns. Chinese values and keys are unchanged.
  Quoted-comma regressions are in `test_stock_csv.py` and the engine `[csv]`
  tests; the corrected UI validator rejects the former corrupted shard.
- `mod/bin/stringtable_ui_generated.utf8.csv`: **57 opt-in display keys**:
  30 `STR_CWRC_WIZARD_*` template/official MP selector identities, five
  `STR_CWRC_WORLD_*` island display names, and two `STR_CWRC_MASTER_*`
  server-attribution labels, plus 20 runtime/config labels described below.
  Other columns explicitly retain canonical stock text.
  The Taiwan editorial check added the previously absent existing runtime key
  `STR_DISP_OPT_CTL_GAMEPAD_REVERSE_Y`: 反转 Y 轴 / 反轉 Y 軸. All eight stock
  columns preserve its prior `Y-axis inversion` fallback. No engine change was
  needed; the existing controller page already requested this key. Both Chinese
  values and English/French switching were physically checked on that page.
  Short selectors omit verbose mode suffixes to fit narrow lists. Island selectors
  use Chinese-only names; campaign geographic wording is not changed.
- `wizard/SPTemplates/` and `wizard/Templates/`: **all 36 stock wizard banks,
  2,198 exact ordered keys**. Covers generated mission names, overviews, briefing
  rules, links, objectives/markers, radio/status, scoring and debriefing text.
  Original other-language columns remain stock. No mission/script/audio change.
- `multiplayer/MPMissions/`: **all 30 official authored mission folders / 1,511
  stock keys**, translated from installed GOG 3.05 English (reusing independently
  translated exact English matches from this project where applicable). Names,
  overviews, briefings/notes, objectives, markers, radio/status and every authored
  ending are covered. Exact keys/order and all seven other-language columns plus
  stock comments are preserved. Short mode suffixes avoid observed title clipping.
  The full installed inventory is recorded in `multiplayer/stock-hashes.json`.
  No historical Chinese wording source was used.
- **27 new mission-local display keys**: Nogova's literal loading label; Hold
  Castle's control-time label/six choices; Real Paintball's START and two legacy
  debug hints; 16 Sector Control sector/start/respawn labels across Everon/Nogova.
  `multiplayer/text-references.json` records exact display-only substitutions in
  six local-overlay files. Internal marker names, numbers, conditions, script
  identities, audio and lip-sync remain unchanged. Other languages retain the
  exact original literal (including the dormant Czech debug hints).
- The two shortened hostage selectors are corrected to **营救人质（1～16）** and
  **营救人质（2～5）**, verified against stock Rescue hostages / Hostage Rescue.
  The 1–16 source inconsistently calls its briefing Clean Sweep (1–6 C); that stock
  content mismatch is retained rather than changing the mission or its meaning.

The 184 non-overridden keys in the audited 2,890-key BIN/addon union are intentionally
stock: key caps/symbols, numbers and formatting-only templates, model designations,
brands and credited people/song names, or empty encyclopedia subtitles. This is
not a claim that developer diagnostics or arbitrary addon text are translated.
Do not transliterate arbitrary profile/NPC/player names or technical identifiers.

## Narrow engine changes

- `Game/Mission/MissionTemplateCatalog.cpp/.hpp`: optional selector metadata,
  stock fallback preserving exact filename casing, and mod/language-aware template
  bank resolution. `UI/DisplayUIMultiplayerWizard.cpp` uses that resolver when
  extracting a generated mission. Before the fix, previews read translated mod
  tables but generation silently extracted the stock English bank.
- `UI/Locale/WorldLocalization.hpp`, `UI/DisplayUI.cpp`,
  `UI/DisplayUIMultiplayer.cpp`, `UI/DisplayUISetupMP.cpp`, `UI/OptionsUI.cpp`,
  `UI/Map/UIArcadeWaypoint.cpp`: resolve optional island display metadata; official
  public MP list rows also use optional selector metadata. List data, world names,
  mission discovery, private user mission labels and network IDs remain canonical.
- `Network/NetworkConfig.cpp`: optional localized master-server attribution;
  host parsing and exact stock English fallback remain unchanged.
- Authored MP follow-up: `UI/DisplayUIMultiplayer.cpp` suppresses duplicate bank
  identities and the stock loose row shadowed by a bank. Previously each overlay
  appeared twice on Windows (two directory-case spellings), alongside a stock
  English loose entry which bypassed it when selected. The existing mod-first
  mission resolver is unchanged. Private user missions, identifiers and stock
  no-mod selection remain intact; no Chinese-specific engine behavior is added.

No Chinese is hardcoded in the engine. Existing canonical identity/display-name
separation is untouched; `name player` still returned `David Armstrong` during
the CWC test. No engine behavior, renderer, language registration or layout redesign.

## Local deployment and reversal

Use the rebuilt `dist/local-labels/PoseidonGame.exe` with the existing isolated
Remastered installation/profile and `--mod <absolute @zhcn-prototype path>`.
The original `game-local/Remastered/PoseidonGame.exe` is not replaced.

Copy both new `stringtable_ui*.utf8.csv` files into `@zhcn-prototype/bin/`, then:

```powershell
python localization/zhcn-combined-arms/wizard/build_templates.py game-local/Remastered
python localization/zhcn-combined-arms/wizard/build_templates.py game-local/Remastered --check
python localization/zhcn-combined-arms/ui/build_addon.py game-local/Remastered
python localization/zhcn-combined-arms/ui/build_addon.py game-local/Remastered --check
python localization/zhcn-combined-arms/validate_ui.py
```

The wizard builder verifies 36 recorded stock SHA-256 hashes and all targets
before writing. It changes only each PBO's main UTF-8 table; commercial members
are copied byte-for-byte into **ignored, local-only** mod banks. Do not distribute
those stock-derived PBOs. `--check` writes nothing. A differing existing output is
rejected; after an authored update, remove only the prior generated wizard copies
before regenerating, never the original stock banks.

To reverse this pass, remove only these two new bin tables and the 36 generated
`@zhcn-prototype/{SPTemplates,Templates}/*.pbo` files listed in `wizard/stock-hashes.json`.
Also remove the authored `@zhcn-prototype/AddOns/cwrc_ui.pbo`. Its sole member is
our `ui/config.cpp`, not commercial content. The builder rejects differing existing
outputs; move only that prior generated addon aside before an authored update.
Previously generated user missions retain their copied language tables; regenerate
them from stock templates if stock text is wanted. Existing campaign/standalone
restoration still follows the main README; omitting the mod alone does not undo
the prior direct campaign-table deployment.

Authored MP deployment uses the existing mod and rebuilt client:

```powershell
python localization/zhcn-combined-arms/multiplayer/build_missions.py game-local/Remastered
python localization/zhcn-combined-arms/multiplayer/build_missions.py game-local/Remastered --check
python localization/zhcn-combined-arms/validate_multiplayer.py
```

The builder preflights all 30 stock tree hashes and existing targets before
writing `@zhcn-prototype/MPMissions/<original folder>.pbo`. It preserves every
member byte except the main CSV and manifest-listed display references. These
are **ignored, local-only, commercial-derived banks: never distribute them**.
For an authored update, move only those prior generated copies aside before
rebuilding. Reverse MP deployment by removing only those 30 generated copies;
omitting the mod restores stock authored MP text without altering originals.

## Authored multiplayer verification

- CWC, Resistance, standalone and UI validators still pass. The MP validator
  passes 30/1,511+27 coverage, strict UTF-8, exact keys/order, stock foreign/comment
  columns, formats/references/HTML/line breaks, all five unchanged fonts and
  deployment equality. All 30 original mission tree hashes match; 333 non-text
  bank members remain byte-identical. Terrain (62 labels) and wizard (36 banks)
  deployment checks pass. Stock CSV Python regressions: 3 tests pass.
- Rebuilt client/Core/normal-test builds succeed. Core: 823 passed / 6,336 assertions, four
  unavailable game-data scans skipped, external-data suites excluded. Focused
  wizard/generated-name/CSV tests: 12 cases / 81 assertions pass. Normal-client
  master/UI tests: 2 cases / 9 assertions pass. Earlier broader
  external-data test limitations above are not claimed fixed.
- Actual GL33 client with GOG 3.05 data, Chinese mod, isolated profile and local
  host only: Hostage Rescue (Everon) selection/lobby/role assignment, briefing,
  notes, objectives/map, running infantry gameplay and verified walking input.
  Its summary was checked **after aborting**, not completing the rescue.
- Hold Castle (Nogova): selection/lobby, 控制时长 and 30/60/90秒 choices, briefing
  and stock automatic ending summary. A solo host reaches the end immediately;
  no sustained competitive gameplay or earned victory is claimed.
- Sector Control (Everon): selection/lobby, readable shortened title, briefing,
  Chinese sector/start map labels, running gameplay/timer. Debug teleport to S1
  exercised the unchanged capture trigger and visible 1号区域由西方阵营控制 message.
  Dense nearby markers still overlap at that zoom, as with the stock layout;
  no geometry/font redesign was made. Marker-link clicks were attempted but
  map recentering was not reliably observed, so that interaction remains unverified.
- War Cry (Nogova): selection/lobby, briefing/objectives/map and running infantry.
  Debug invocation of its existing r01r04 radio event displayed the full Chinese
  熊爸爸/S狙击组/大天使阵位 message; not a natural full mission progression.
- Rebuilt client **without the mod**, separate stock profile: English official
  mission selection, Hold Castle lobby/roles (Time to hold; 30/60/90 s), briefing
  prose, group heading and stock terrain labels. The mod does not alter originals.
- Full assembled briefing-page review corrected fragment joins (rescue targets,
  respawn instructions, aircraft starts, vehicle cache, crossroads and objectives)
  against English; no extra units or mission instructions were invented.
- No missing glyphs or mojibake were observed. Stock models/codes, established
  Swordfish callsign and unused DescriptionEnd/PopisTextEnd scaffolding are
  intentional exceptions. The retained scaffolding does not correspond to any
  END trigger used by those missions. Skalice remains bilingual (no terrain label).
- No online session, second-client network synchronization, complete authored
  match, all alternate endings or every radio event was tested. No captions were
  invented for audio without source text. Fonts, canonical identities, original
  GOG executable/PBOs, commercial assets and campaigns are unchanged by this pass.

## Validation and actual-game evidence

- All three existing localization validators pass: CWC 78/1,928; Resistance
  39/1,310; standalone 24/1,284. The standalone baseline explicitly accepts this
  new stock-key shard, retaining all earlier wording/repair checks. Its 11 existing
  unresolved stock audio references remain unchanged; no captions were invented.
- `validate_ui.py` passes exact stock keys/other-language text, formats/references,
  HTML/links, line breaks, duplicate/malformed checks, all 36 ordered wizard tables
  and all five font cmaps. Four explicitly checked bracketed option labels are
  literal text, not HTML. Terrain and wizard `--check` pass deployment equality,
  original input hashes and unchanged non-text commercial payloads.
- Client, PoseidonCoreTests and PoseidonTests builds succeed. Core tests excluding
  explicitly external-game-data suites: **819 cases / 6,321 assertions pass**.
  Focused wizard/generated-name checks: **8 cases / 66 assertions pass**;
  normal-client master/UI/localization subset: **5 cases / 41 assertions pass**.
  The broader normal-client localization selection is not green: six data-dependent
  cases fail because this checkout lacks their expected `packages/Remaster` data
  paths. No full-suite PASS is claimed.
- Actual rebuilt GL33 client, installed 3.05 data, English voices, isolated profile,
  1280x900: Chinese main menu; graphics, controls/binding and difficulty screens;
  editor toolbar/terrain map and Chinese island selectors; SP wizard selector;
  LAN browser, official MP selectors, generated Team Flag Fight lobby and rules.
  Generated output now contains the translated CSV; lobby shows 时间、获胜分数、
  20/25/30分钟. Role assignment and generated briefing navigation work locally.
- CWC Flashpoint regression: localized identity/group briefing heading, map,
  running Chinese dialogue/radio and existing HUD hints; canonical scripting name
  remains English. Equipment links opened M16, M60 and newly translated Stinger
  description pages, with readable text/images/参数 links. No observed glyph boxes
  or mojibake. One clipped graphics tooltip was shortened; island/mission selector
  labels were shortened after observing clipping. Existing Latin/title-font
  proportions and narrow key-name clipping remain presentation QA.
- Rebuilt client **without the mod**, separate profile: actual main/options and
  editor island selectors return stock English (CAMPAIGN GAME, Quality Preset,
  Everon/Malden). Unit tests also check French fallback. New shard other-language
  columns are statically checked against stock; this does not repair the older
  prototype's English-column-only mission/global files in other languages.
- Existing validators confirm 7,458 unrelated installed files unchanged, including
  the GOG executable, scripts/audio/lip-sync and the five fonts. Tests stayed muted;
  no persistent power setting or audio-volume change was made.

## Phase 1 closeout: residual audit and runtime QA

- Rechecked the 184 intentional stock-key exceptions, stock BIN config/resource,
  Remastered UI resources and addon configs, and engine text-display consumers.
  No known reasonably localizable official UI/prose omission remains. Brand/model
  names, keycaps, song/person names, arbitrary profile/NPC names, technical error
  details and developer/cheat diagnostics intentionally remain stock. Dormant OFP
  demo/promotional resources and the unused legacy warrant renderer are not
  Remastered player flows; they were not rewritten.
- **19 new display translations**: category-reset title/body/button, mod-remount
  failure, joystick buttons 9/10, G36 full-auto mode, generic Music SFX and 11
  Resistance music-list labels. New custom keys preserve the original English
  literal in all other columns. The 2,706 stock-key count is unchanged.
- Three narrowly changed engine files: `UI/Options/BindingsPage.cpp`,
  `UI/DisplayUIMultiplayer.cpp`, `UI/DisplayUI.cpp`. They resolve optional keys
  with exact stock fallbacks; no Chinese is hardcoded and reset/input/mod behavior
  is unchanged. `ui/config.cpp` overrides only 13 stock display properties.
  The G36 inheritance chain is explicitly retained because `ParamClass::Update`
  replaces bases; `[cwrc-ui]` parses the actual authored config and verifies
  inherited weapon properties, magazine count and unchanged full-auto settings.
- **One existing value repaired**: `STR_BRIEF_GROUP_LEADER` becomes
  `（小队队长）`, separating a directly appended roster suffix from the name.
  The standalone validator allows exactly this observed composition repair.
- Actual rebuilt GL33 client with isolated GOG 3.05 data/profile, 1280x900:
  Combined Arms' populated ten-person roster shows translated ranks and
  新兵/老兵/专家, with the repaired leader suffix; Ground Attack's populated pilot
  roster also works. Editor unit-properties and full rank dropdown, trigger/effects
  controls and translated Resistance music entries render correctly. An invalid
  variable name produces `变量名无效！`; the unsaved unit was cancelled.
- Profile selection/edit (face/voice/ID controls), LAN browser, remote-IP and port
  dialogs were inspected without an online connection or profile changes.
  The Chinese category-reset confirmation fits and was cancelled without resetting.
  G36's HUD displays `G36 全自动` after adding the stock weapon/ammunition to a
  disposable Bomberman run and cycling its normal firing modes.
- Ground Attack's briefing hyperlink was actually clicked: the red active link
  recentered the map from the entry area to the convoy location. Combined Arms
  still shows Chinese identity/group headings, dialogue/radio and map/HUD text;
  scripting `name player` remains `David Armstrong`.
- Completion/failure QA: forced Combined Arms END1 (its authored retreat ending),
  forced Bomberman END1 success and END2 failure show readable Chinese objectives,
  summary/ending text, score/time and statistics link. Forced player damage in
  Combined Arms opens the Chinese death/quotation/retry/end screen. These are real
  rendered UI checks, **not earned endings or a campaign/match playthrough**.
- No-mod comparison with a separate profile: main/settings and category-reset
  title/body/buttons return English. Stock English's existing long reset-body
  clipping was not redesigned; the Chinese version fits. Omitting the mod still
  does not reverse directly deployed campaign/standalone CSVs (see reversal above).
- Fresh validation: CWC 78/1,928, Resistance 39/1,310, standalone 24/1,284,
  authored MP 30/(1,511+27), UI 1,579 stock + 56 custom, and all terrain/wizard/MP/UI
  addon deployment checks pass. Stock CSV regressions: 3 tests pass. Five-font
  coverage and original commercial input hashes pass; 7,458 unrelated files remain
  unchanged. No font, mission logic, audio/lip-sync or original GOG executable/PBO
  changes; CWRR is untouched.
- Client/core/normal UI builds pass. Core excluding external-data suites:
  **824 cases / 6,347 assertions pass, four game-data scans skip**.
  Focused normal-client binding/confirmation/master UI: **17 cases / 94 assertions
  pass**. Broader normal `[localization]`: **7 pass, 6 fail** because its required
  `packages/Remaster` fixtures are absent; this pre-existing limitation remains,
  not a full-suite PASS.

Limits: rare remount failures and hardware joystick button 9/10 rendering are
source/format/glyph checked but were not individually provoked. Not every warning,
loading variant, multiplayer ending or second-client/online path is exercised.
The 11 documented stock standalone audio references remain without source captions;
none were invented. These are bounded test/source limits, not known untranslated
official authored text. Narrow Page-key labels and Latin/title-font proportions
were subsequently addressed in [TYPOGRAPHY.md](TYPOGRAPHY.md). The language pass restores
all eight stock columns, moves Chinese into ChineseSimplified, and verifies live
English/French switching and language-specific fonts; see LANGUAGE_SUPPORT.md.
