# Chinese localization: campaigns, missions and UI

**Repository split:** the root [README](../../README.md) is the current entry
point. This directory keeps development history and terminology notes; complete
CSV/config files described below are now locally reconstructed from the
Chinese-only master, not shipped in Git. Engine changes/builds remain in the
this repository's pinned `client-source` branch. Phase 3 is complete; no public installer is released.

Personal-use Simplified Chinese patch for the complete official **1985 / 冷战危机**
and **Resistance / 抵抗力量** campaigns, all **24 official standalone missions**
and **30 official authored multiplayer missions**, using installed GOG Remastered
3.05 data and the rebuilt local client described below. Cold War Crisis was
freshly retranslated on 2026-10-08; the original GOG executable is untouched.
The directory and mod retain their prototype names for continuity. This is
selectable **简体中文 / ChineseSimplified** language pack with stock English fallback.
See [language selection, migration, deployment and current tests](LANGUAGE_SUPPORT.md).
The complete **繁體中文 / ChineseTraditional (zh-TW)** first pass now shares these
tables, with independent Taiwan-region fonts and English fallback. Simplified
and all eight stock columns are unchanged. Phase 3 regional editorial review is
complete; see [Traditional Chinese coverage and tests](TRADITIONAL_CHINESE.md).
See [typography polish and visual checks](TYPOGRAPHY.md) for title proportions,
Chinese-only wrapping and narrow key labels.
See [the residual UI pass](RESIDUAL_UI.md) for 1,579 new stock-key overrides,
56 optional display keys, all 36 wizard templates, authored multiplayer overlays,
rebuilt-client requirements, deployment and outstanding work.
All shipped Cold War Crisis authored Chinese text is freshly translated from
the current Remastered English source, as are Resistance and standalone missions.
See [the fresh CWC pass](FRESH_CWC.md) for its source, review and test results,
and [Resistance coverage, provenance, place names and limits](RESISTANCE.md).
See [standalone coverage, Bomberman tests and reversal](STANDALONE.md) for the
complete installed Single Missions inventory and this pass's limits.
The subsequent [unit-designator cleanup](UNIT_DESIGNATORS.md) uses letter-based
Chinese formations and radio codes throughout all three content sets; semantic
callsigns remain semantic. [Generated identities, group labels and the Resistance
category](GENERATED_NAMES.md) are now localized, with stock fallbacks. Identity
metadata/category support requires the rebuilt client described there; the
original installed GOG executable is unchanged.

## Final Simplified Chinese content QA

Reviewed the current global/display/terrain tables, both campaigns, 24 standalone
missions, 30 authored MP missions and 36 wizard templates for terminology/name
variants, residual Latin text, spacing/punctuation and source meaning. Suspicious
briefing fragments were checked in their composed HTML context, not rewritten
in isolation. **32 existing values corrected: 18 CWC, 0 Resistance, 4 standalone,
2 MP, 5 wizard and 3 globals**; no keys or coverage added.

- Standardized 戴维·阿姆斯特朗 / 戴维, the nickname 戴夫, 山姆·尼科尔斯 / 山姆,
  standalone 鹰眼 / 雷霆 callsigns and 德拉贡诺夫; restored 哈默中尉 and 尤谢夫上校.
- Shadow Killer's MP lost-ending now says the player lost their bearings, not
  that escape is impossible. M21's `National Match` model is described as 竞赛型,
  not 国家比赛型. Conquerors' five wizard variants use compact A代码; War Cry's
  Skalice reference uses the already mapped 斯卡利采 without redundant Latin.
- Shortened only the Chinese composed briefing heading to `简报（%s，%s %d）`:
  Status Quo's long identity/group heading no longer clips at 1280x900.

Actual rebuilt GL33/GOG 3.05 checks at 1280x900: Status Quo diary/objectives and
the 山姆 marker-link click; live English/French briefing switching; Bomberman's
M21 gear-info link and M21/SVD encyclopedia pages; Vulcan's authored 鹰眼/雷霆
radio captions; local-host Shadow Killer selection/lobby/briefing and END5
debriefing. Radio messages and END5 were **harness-triggered**, not naturally
reached/earned. No-mod English main/Bomberman briefing/M21 encyclopedia remain
stock. No missing glyphs or new clipping observed; other corrected lines were
statically checked, not individually played. Tests preserved the muted audio state.

All five validators and four deployment checks pass, including font coverage,
stock columns, original-asset hashes and Combined Arms mirror equality. A
before/after audit also preserves ordered keys, extra fields, HTML, formats,
references and literal breaks. Client/core/UI builds pass; focused language/
stringtable/identity/config tests pass (58 cases / 246 assertions), wrap/font/
binding tests pass (23 / 173), stock-CSV tests pass (3); core excluding external
data passes (826 / 6,373 assertions, four scans skipped). This is not a full-suite
or every-ending replay claim; existing external UI-fixture limitations remain.
The standalone validator permits only the exact verified shorter Chinese
briefing heading alongside its existing exact roster-suffix repair; other
baseline wording protections remain intact.

No known actionable Simplified Chinese content issue remains from this review.
Intentional Latin models/brands/keycaps, minor names/callsigns, the I-Spy spelling
joke, CO explanation and dormant stock ending placeholders remain; source audio
without captions is not given invented transcripts. All eight stock languages,
canonical identities, engine/UI/layout/font/mission-logic/audio files and terrain
mapping are unchanged. Phase 2 is complete; Traditional Chinese/distribution
remain separate, unstarted phases.

## Mixed CJK/Latin spacing

The full current table set was reviewed, including resolved briefing HTML
fragments and composed global action/radio/statistics templates. Against
`0ee788a`, spacing-only edits affect **15 CWC, 21 Resistance, 62 standalone and
177 global values**. No keys were added; the overlay remains at 1,101. The
Combined Arms mirror needed no edits and remains byte-identical to its campaign table.

- One ASCII space separates Chinese prose from distinct Latin/model/key/code
  tokens: 前往 Ff52、M16A2 步枪、按 Enter、使用 Shift+W、代号 A.
  Roman-numeral variants use 全面清剿 II. Retained Latin names/callsigns use
  Sutherland 少校、Firefly 基地、Swordfish 基地; their wording is not translated here.
- Compact letter-based formations/calls stay joined: A小队、Y坦克排、N编队、
  A一号、F代码. Dates, quantities, calibres, directions and ordinary numbered
  labels stay joined: 1985年、5吨、7.62毫米、第3步兵营、12点钟方向、结局5说明.
  Distinct clock times use 行动于 10:30 开始; bilingual names stay 艾弗隆（Everon）.
- Tokens keep their internal spelling/spacing. Chinese punctuation stays attached.
  Generic name/model placeholders receive separators in templates such as
  装填 %s and 将 %s 放入 %s; numeric placeholders in ordinary Chinese quantities
  remain joined. No conditional engine spacing or generated-label change was added.

All three validators pass, including deployed equality and five-font coverage.
A disposable audit verifies exact ordered keys, protected syntax and that removing
ASCII spaces restores every pre-pass value; 7,461 non-target installed file hashes
are unchanged. The standalone validator's old global baseline now permits only
ASCII-space differences, retaining wording, key and placeholder checks.

Actual GOG 3.05 / GL33, existing mod/fonts and isolated profile, 1280x900:
stock editor **Preview** of CWC Pathfinder shows 行动于 10:30 开始 and the
M60 机枪 HUD; Bomberman shows its plan/code references, M21 狙击步枪 HUD and
the composed 装填 M21 弹匣 / 背起 M21 狙击步枪 / 丢下 M21 弹匣 actions.
No missing glyphs, mojibake or new clipping observed. Bomberman's LAW note and
other changed lines were statically checked, not individually played; no full
playthrough, campaign progression or debriefing is claimed. Existing narrow-page
proper-name/punctuation wrapping remains later QA. Tests stayed muted; Caps Lock
and the original audio state were restored. Engine/UI, fonts, mission logic,
audio/lip-sync, geographic policy and deployment architecture are unchanged.

## Coverage and files

- `campaign/1985/missions/`: complete replacement main UTF-8 tables for all
  **78 folders: 42 numbered playable mission/branch folders and 36 cutscene,
  ending, award and punishment support folders**. Covers existing names,
  overviews, plans, objectives, markers, diary/intel/tactical notes, dialogue,
  scripted radio, debriefings and ending text. Empty English source stays empty.
- `campaign/1985/stringtable.utf8.csv`: shared names, labels and markers.
  Together with mission tables: **1,928 keys**, including two missing-caption repairs.
- `campaign/1985/description.ext`: eight campaign/chapter display-name
  assignments and 15 optional identity `nameKey` fields; behavior remains stock.
- `mod/bin/stringtable.utf8.csv`: **1,101 selected global overrides** (the original
  995 keys, plus 99 Resistance-related and seven standalone-related additions) covering
  ordinary squad/radio commands and replies, movement, formation, combat,
  status, vehicle/inventory actions, weapon/ammunition/equipment/vehicle names,
  waypoints, HUD, briefing/debriefing, campaign menus/statistics and dates.
  Unspecified keys retain English. `mod/bin/stringtable.csv` remains the
  header-only entry point; no complete base global table is copied.
- `mod/bin/stringtable_groups.utf8.csv`: 26 generated group/color overrides,
  bringing pre-UI-pass known-stock coverage to **1,127**; seven other languages retain their
  original values. `stringtable_generated.utf8.csv` adds 25 identity metadata
  keys and one category key, also with explicit stock-language fallbacks.
- `mod/bin/stringtable_ui.utf8.csv` brings shared stock-key coverage to **2,706**;
  `stringtable_ui_generated.utf8.csv` adds 56 optional UI display keys. New tables
  preserve stock other-language columns. `wizard/` covers 36 template banks / 2,198
  keys, with a local-only overlay builder. See RESIDUAL_UI.md before deployment.
- `multiplayer/MPMissions/`: all 30 authored MP tables / 1,511 stock keys plus
  27 display-only literal references. Other languages stay stock. The builder
  creates ignored local-only mission banks; original installed missions remain
  untouched. `validate_multiplayer.py` checks source hashes, text contracts,
  unchanged commercial members, font coverage and deployment equality.
- `mission/stringtable.utf8.csv`: retained, superseded Combined Arms prototype;
  its values agree with the full campaign version. Deploy the `campaign` tree.
- `font/`: all five final hybrid fonts and existing helper/licenses are unchanged.
  Every new character is covered by all five; no rebuild was necessary.
- `validate_campaign.py`: focused checks against this backed-up local 3.05
  installation, not an extraction/translation framework or installer.
- `campaign/resistance/`: 39 mission/support tables, a shared table and four
  campaign/chapter display labels and six identity metadata fields; **1,310 keys**, including two stock-reference
  repairs. `validate_resistance.py` checks this campaign and whole-install hashes.
- `standalone/`: 24 complete main mission tables, **1,284 keys** including two
  missing-caption spelling repairs. Deploy under `Remastered/Missions/`, retaining
  its `Resistance/` subgroup. `validate_standalone.py` checks coverage, text,
  deployment, fonts and unrelated installed files against its original baseline;
  Subsequently updated campaign CSVs are checked by their respective campaign
  validators; the baseline permits only documented display/config metadata.
  Ambush also has a stock-derived `description.ext` with six identity metadata
  fields; its original requires a separate exact-file backup/restoration.
- `../../docs/zhcn-standalone/`: selected actual-game standalone evidence.
- `../../docs/zhcn-1985/`: historical client-only screenshots from the earlier pass.
  `../../docs/zhcn-prototype/` retains the previous typography evidence.

The generated-label pass adds narrowly scoped engine localization hooks; see
GENERATED_NAMES.md. Original GOG executable, mission script/logic, HTML template,
sound, lip-sync and font bytes are unchanged. Game assets, backups, temporary tools
and the isolated test profile stay ignored under `game-local/`.

## Current translation source and preserved conventions

The shipped CWC text is a fresh translation of the installed GOG Remastered
3.05 English campaign. Verified original backups supply the English column of
the 78 mission tables; the untouched installed legacy root table supplies the
shared campaign text. All **1,928 keys** were processed against that English.
The previous Chinese sentences were not used as drafts or wording input.
Historical Chinese localization is no longer a source or credit for shipped CWC
wording, and translation-reuse licensing caveats from the prototype no longer
apply. This does not grant rights to redistribute Bohemia's original game assets.

Development history only: an earlier prototype reused historical material
preserved by TZKdeveloperIF and attributed to 天人互动. That wording has now been
replaced. Earlier screenshots are retained as historical test evidence, not
evidence of the current translation or a source for it.

Independently established conventions and technical fixes retained:

- Consistent main-character names (阿姆斯特朗、加斯托夫斯基、哈默、尼科尔斯、
  贝尔霍夫、福利、科兹洛夫斯基、布莱克、古巴、安吉丽娜) and radio callsigns
  (熊爸爸、黑熊、白狼). Geographic names now use consistent Chinese names,
  with Chinese-only names for towns covered by the same island's terrain overlay.
  Unlabelled places and island names retain useful Latin navigation references.
- Corrected visible spellings to Kolgujev, Houdan, Chapoi and Riviere; script-facing
  identifiers, marker names and link attributes are preserved, not renamed.
- 弹匣 is consistent; M60 machine gun and M60 tank remain distinct.
- After Montignac's secondary end-objective link restored to `Konec2`; Rescue's
  malformed `Start` link/quoting repaired and hostage `Rukoj` link restored.
- Training `STRM_00v16a` added as an alias of its existing caption, because a stock
  speech definition referenced the missing spelling; Killdozer `STR_END` added
  for its existing scripted mission-completion radio. No scripts changed.
- Proven layout breaks, Camping's opening `<B>` and repaired links retained.
  The fresh pass preserves pre-rewrite HTML metadata and literal `\n` tokens.

### Geographic-name policy

Towns confirmed in the same island's 62-entry terrain shard now use Chinese-only
names throughout briefings, objectives, diary/intel, visible labels, debriefings
and destination replies. This includes Status Quo's town destinations. Unlabelled
places (Lolisse, Nová Ves and Kiusk) and island names (Everon, Malden, Kolgujev and
Nogova) retain useful `中文名（Latin Name）` navigation references; short titles
and routine dialogue can still use Chinese. Do not infer coverage from this
glossary alone: use the actual terrain shard and mission island. Case variants
share one mapping; `St Pierre`,
`St Pierre's` and the legacy typo `St. Piere` resolve to `Saint Pierre`.

| Latin name | Chinese name | Latin name | Chinese name |
| --- | --- | --- | --- |
| Everon | 艾弗隆 | Malden | 马尔登 |
| Kolgujev | 科尔古耶夫 | Morton | 莫顿 |
| Montignac | 蒙蒂尼亚克 | Chapoi | 沙普瓦 |
| Le Moule | 勒穆勒 | La Riviere | 拉里维耶尔 |
| Houdan | 乌当 | La Pessagne | 拉佩萨涅 |
| La Trinite | 拉特里尼泰 | Dourdan | 杜尔当 |
| Goisse | 瓜斯 | Arudy | 阿吕迪 |
| Lolisse | 洛利斯 | Levie | 莱维 |
| Regina | 雷吉纳 | Provins | 普罗万 |
| Saint Pierre | 圣皮埃尔 | Vernon | 韦尔农 |
| Sainte Marie | 圣玛丽 | Vigny | 维尼 |
| Durras | 迪拉斯 | Laruns | 拉兰斯 |
| Larche | 拉尔什 | Tyrone | 蒂龙 |
| Meaux | 莫 | Saint Philippe | 圣菲利普 |
| Chotain | 绍坦 | Gravette | 格拉韦特 |
| Entre Deux | 昂特尔德 | Figari | 菲加里 |
| Lamentin | 拉芒坦 | | |

This changes visible CSV values only. Exact keys/casing, row order, placeholders,
all existing HTML tags/attributes (including marker targets), mission filenames
and internal identifiers are unchanged. Weapon models, character names and
non-geographic callsigns are untouched. No font rebuild, engine/UI edit, mission
logic or audio change was needed; the existing validator and deployment check
pass with all five fonts covering the new text.

Earlier geographic-name spot-checks (2026-10-07) at 1280x900 covered Tank Training's bilingual objectives
and map, Battle of Houdan's bilingual briefing and opening tank radio order
(`乌当`), and Tank Rally's bilingual Chapoi plan/objective beside the map. The
later La Riviere tank order was checked statically, not reached through combat.
No missing glyphs or clipped place names appeared. Stock wrapping can still put
a closing parenthesis at the start of a line (seen in the Houdan briefing).
Built-in terrain-map labels now have a separate **62-key** UTF-8 shard and a
local-only GOG 3.05 data-overlay builder: Everon 18, Malden 14, Nogova 30;
Kolgujev has no stock town-label entries. Names originate in `CfgWorlds/Names`,
not terrain textures. Stock files remain intact, and no commercial config/PBO
is redistributed. The existing 1,101-key shared overlay is unchanged. See
[terrain mechanism, glossary, deployment and tests](terrain/README.md).
New Nogova mappings supplement the campaign/standalone glossaries there.
The selective [bilingual-name retirement](BILINGUAL_NAMES.md) changes only
redundant town-name suffixes: 144 CWC, 26 Resistance and 70 standalone values,
plus four byte-identical Combined Arms mirror values. No global overrides,
terrain mapping, generated terrain assets or fonts changed. Fresh deployments
must include the generated Chinese terrain overlays before using this text.

Chinese is in separate **ChineseSimplified / ChineseTraditional columns**. Select 简体中文 or 繁體中文 under
Options → Game → Text language; retain English voices. English and all seven
other stock columns are restored, even with the mod enabled. Briefing/title previews consult
the main mission CSV directly, requiring complete replacement tables rather
than extra shards. Runtime keys are case-sensitive, unlike the HTML preview
resolver: exact original key spelling is preserved.

## Deployment and reversal

Close the game before copying/restoring files. The current installation is
already deployed. Original files and a reversal inventory are retained at
`game-local/localization-backup/1985-original/`. **Never overwrite this backup
with localized files.** `reversal.json` records all 80 targets, original existence
and backup hashes. `before-hashes.json` records the installed campaign before
this pass. The earlier verified English Combined Arms backup was used instead
of backing up its previously localized CSV.

For a fresh installation, first back up each corresponding installed file from
the patch's 80-file `campaign/1985` tree, preserving relative paths. Record absent
files too: the tested 3.05 campaign-root `stringtable.utf8.csv` did not exist;
the legacy `stringtable.csv` is left intact. A localized Combined Arms CSV is
not an English original.

Manual redeployment from the repository root, after backup:

```powershell
$patch = Join-Path $PWD 'localization\zhcn-combined-arms'
$game = Join-Path $PWD 'game-local\Remastered'
foreach ($campaign in @('1985', 'resistance')) {
    $source = Join-Path $patch "campaign\$campaign"
    $target = Join-Path $game "Campaigns\$campaign"
    foreach ($file in Get-ChildItem -LiteralPath $source -File -Recurse) {
        $relative = $file.FullName.Substring($source.Length + 1)
        Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $target $relative)
    }
}
$source = Join-Path $patch 'standalone'
foreach ($file in Get-ChildItem -LiteralPath $source -File -Recurse) {
    $relative = $file.FullName.Substring($source.Length + 1)
    Copy-Item -LiteralPath $file.FullName -Destination (Join-Path "$game\Missions" $relative)
}
New-Item -ItemType Directory -Force -Path "$game\@zhcn-prototype\bin", "$game\@zhcn-prototype\Fonts\ChineseSimplified", "$game\@zhcn-prototype\Fonts\ChineseTraditional" | Out-Null
foreach ($file in Get-ChildItem -LiteralPath "$patch\mod\bin" -Filter '*.csv' -File) {
    Copy-Item -LiteralPath $file.FullName -Destination "$game\@zhcn-prototype\bin"
}
foreach ($role in @('title', 'body', 'mono', 'serif', 'hand')) {
    Copy-Item -LiteralPath "$patch\font\cwr_$role.ttf" -Destination "$game\@zhcn-prototype\Fonts\ChineseSimplified\cwr_$role.ttf"
    Copy-Item -LiteralPath "$patch\font\ChineseTraditional\cwr_$role.ttf" -Destination "$game\@zhcn-prototype\Fonts\ChineseTraditional\cwr_$role.ttf"
}
Copy-Item -LiteralPath "$patch\mod\bin\config-extra.cpp" -Destination "$game\@zhcn-prototype\bin"
python "$patch\terrain\build_labels.py" $game
if ($LASTEXITCODE -ne 0) { throw 'Chinese terrain overlay generation failed; do not launch with incomplete navigation labels' }
python "$patch\wizard\build_templates.py" $game
python "$patch\multiplayer\build_missions.py" $game
python "$patch\ui\build_addon.py" $game
$client = Join-Path $PWD 'dist\local-labels\PoseidonGame.exe'
if (!(Test-Path -LiteralPath $client)) { throw 'Build the generated-label client first; see GENERATED_NAMES.md' }
Start-Process -FilePath $client -WorkingDirectory $game -ArgumentList @(
    '--mod', "$game\@zhcn-prototype"
)
```

Use the mod's absolute path and Remastered as the working directory. Base fonts
are never overwritten. Terrain generation requires the existing fontTools
dependency and exact supported stock inputs; see [terrain deployment](terrain/README.md).
For disposable tests only, set `POSEIDON_USER_DIR` to
`game-local/test-profile`; clear that environment override before using your
normal profile. Current tests use selectable Chinese text, English voices,
subtitles enabled and Cadet. Earlier sections record English-column prototype tests.
An existing prototype must also retire its five flat `@zhcn-prototype/Fonts/cwr_*.ttf`
copies after checking their hashes; otherwise those files still override stock
fonts. See LANGUAGE_SUPPORT.md for the bounded migration/reversal details.

To reverse this installation, close the game and read `reversal.json`. Verify
backup hashes and restore each `Existed: true` entry to its exact relative path
under `game-local/Remastered/Campaigns/1985`. For an originally absent entry,
remove only that exact newly added file (here, root `stringtable.utf8.csv`).
Do not delete the campaign directory. Launch without `--mod` to disable global/
font overrides. Existing saves are not touched.

Resistance has its own **41-target** backup/reversal inventory at
`game-local/localization-backup/resistance-original/`. Back up that campaign
separately before a fresh deployment; see [Resistance reversal](RESISTANCE.md#deployment-and-reversal).
Disabling the mod alone does not restore either campaign's replacement CSVs.
Standalone missions also require their own originals restored; see
[standalone deployment/reversal](STANDALONE.md#deployment-and-reversal).

## Verification performed

Static checks passed across all 78 folders: exact-case keys, no duplicate keys
or replacement characters, strict UTF-8, original placeholders and HTML anchors,
briefing token resolution, no newly unresolved literal script/speech references,
deployment equality and new-character coverage in all five unchanged fonts.
All **3,706 unrelated installed campaign files** match their pre-pass SHA-256
hashes, including scripts, audio, lip-sync and HTML. Eight display labels and
15 optional identity metadata fields are the only campaign-config differences.
The replacement configuration deliberately preserves stock whitespace too.
The fresh wording pass does not alter that configuration.

Run from the repo root with fontTools 4.66.1 available:

```text
python localization/zhcn-combined-arms/validate_campaign.py
python localization/zhcn-combined-arms/validate_resistance.py
python localization/zhcn-combined-arms/validate_standalone.py
```

Earlier, pre-retranslation actual-game checks at 1280x900 (development history):

- Campaign/menu selection, early/late mission titles, rank/duration and kill
  statistics; Chinese previews load from the main mission tables.
- Training: opening tutorial prompts, control instructions and on-foot input.
- Combined Arms: plan/objectives/map marker, truck dialogue subtitles,
  disembarkation, weapon/ammunition inventory actions and squad status replies.
  Diary/tactical-note pagination was tested in the preceding font pass.
- Tank Training: plan/objectives/map markers, multi-line tutorial, nearby M60
  crew-position actions and success debriefing. Tank driving was not tested.
- Airborne: plan/objectives, tutorial, Black Hawk pilot entry, cockpit speed/
  height/armor/fuel/weapon HUD and vehicle actions. Not a flight test.
- Incursion: night briefing/objectives/markers, diary, scripted opening radio,
  status-command menu and success debriefing/summary/restart controls.

Built-in `CAMPAIGN` unlock selected missions in the isolated profile.
`ENDMISSION` exercised real success-debriefing screens for Tank Training and
Incursion: these are **not natural completion or end-to-end playthrough claims**.
English voice selection and unchanged sound/lip-sync hashes are verified; audio
was not independently auditioned because the PC's already-muted output was
preserved. Other missions/endings are statically checked, not all manually played.

Selected evidence: [campaign book](../../docs/zhcn-1985/campaign-title.png),
[Combined Arms briefing](../../docs/zhcn-1985/combined-briefing.png) and
[subtitles](../../docs/zhcn-1985/combined-subtitles.png),
[tank tutorial](../../docs/zhcn-1985/tank-tutorial.png),
[helicopter HUD/actions](../../docs/zhcn-1985/helicopter-hud.png),
[Incursion diary](../../docs/zhcn-1985/incursion-diary.png),
[radio](../../docs/zhcn-1985/incursion-radio.png),
[status commands](../../docs/zhcn-1985/status-commands.png), and
[debriefing](../../docs/zhcn-1985/debriefing.png). Images show representative
checks during the earlier pass. Current rewrite checks are recorded separately
in [FRESH_CWC.md](FRESH_CWC.md).

## Known limits

- Chinese built-in terrain labels require generating the local overlays from
  the exact supported GOG 3.05 assets; other versions, third-party terrains and
  config-replacement mods are unverified. Places absent from stock terrain
  definitions do not gain invented map labels. Bilingual navigation references
  remain for unlabelled places and islands. Some minor non-geographic names/callsigns,
  random NPC-name pools, key labels such as `Backspace`, and baked-in English logo/
  cover artwork are intentionally unchanged.
- Fifteen stock speech-definition references have no caption in either source
  (some may be unused clips). They remain stock; no invented transcript is
  supplied. The two actionable missing references above are repaired.
- Official encyclopedia descriptions, editor/multiplayer/settings text and wizard
  templates are covered by the expanded overlay; see [RESIDUAL_UI.md](RESIDUAL_UI.md).
  Arbitrary third-party content is outside this patch.
- No missing glyphs, mojibake or obvious clipping appeared in representative
  screens. The later [typography pass](TYPOGRAPHY.md) adds Chinese-only punctuation
  boundaries to notebook and plain-control wrapping. Untested long pages or other
  resolutions may still need local line-break QA.
- Every branch transition, alternate ending/debriefing and late scripted caption
  has not been manually exercised. Report missed strings with mission name and
  screenshot; preserve keys/placeholders when correcting them.

## Existing fonts and provenance

| Role file | Chinese family/weight | Retained Latin face/weight | CJK horizontal factor |
| --- | --- | --- | --- |
| `cwr_title.ttf` | Noto Sans SC Bold 700 | Oswald 700 | 1 / 0.628 = 1.592357 |
| `cwr_body.ttf` | Noto Sans SC Medium 500 | Roboto 700 | 1 |
| `cwr_mono.ttf` | Noto Sans SC Medium 500 | UnuarangaKuriero (Courier Prime) 700 | 1 / 0.8 = 1.25 |
| `cwr_serif.ttf` | Noto Serif SC SemiBold 600 | Vollkorn 700 | 1 / 0.935 = 1.069519 |
| `cwr_hand.ttf` | LXGW WenKai Medium 500 | Caveat 600 | 1 / 1.05 = 0.952381 |

Added CJK outlines/advances compensate stock role widths. The Chinese-only title
asset now compensates Oswald by the same 1/.628 factor; the other four Latin
faces are unchanged. Original face styling, vertical metrics and engine/UI sizes
are retained. Fonts include the
6,763 GB2312 Han characters and common punctuation, not complete pan-CJK coverage.
[font/NOTICE.md](font/NOTICE.md) records upstream links, source hashes, copyrights,
OFL licenses, modifications and reproduction instructions. Existing helper:

```text
python localization/zhcn-combined-arms/font/build_font.py SOURCE_DIRECTORY game-local/Remastered/fonts
```

Ordinary UTF-8/full mission tables/partial global/font replacements remain
viable. Campaign translation required no engine, UI or typography changes;
the later generated-identity/category feature requires its narrowly patched
client, as documented in GENERATED_NAMES.md.
