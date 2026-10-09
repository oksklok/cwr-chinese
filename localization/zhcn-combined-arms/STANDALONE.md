# Official standalone missions / 单人任务

Complete text-table coverage for the installed GOG Remastered **3.05** Single
Missions menu, checked on 2026-10-07. Both campaigns remain frozen. This is a
local-only language patch, not an installer. Current selectable language and
stock-column restoration are documented in [LANGUAGE_SUPPORT.md](LANGUAGE_SUPPORT.md).

## Installed inventory and coverage

The actual installed directories are `game-local/Remastered/Missions/` (18
mission folders) and its `Resistance/` subgroup (six). Each mission has a main
`stringtable.utf8.csv`, used by its UTF-8 briefing/overview HTML and runtime
text references. There is no shared standalone-root stringtable in this install.
Complete replacement English-column tables are in `standalone/`, with the
original relative paths/casing preserved. Keep English text and English voices.

The game enumerates these folders for Single Missions: `OptionsUIImpl.cpp`
loads the mod/base `Missions` trees and resolves each mission's title from its
own table. No separate fixed Skirmishes inventory was found. The five
`SPTemplates` cooperative PBOs belong to the generated mission wizard, not this
24-mission menu; multiplayer and generated/custom missions are outside this pass.

| Folder relative to `Missions/` | Original title | Chinese title | Keys |
| --- | --- | --- | ---: |
| `01TakeTheCar.ABEL` | 01: Steal the Car | 01：夺车行动 | 48 |
| `02Infantry.Abel` | 02: Ambush | 02：伏击 | 120 |
| `03Bomberman.CAIN` | 03: Bomberman | 03：爆破专家 | 61 |
| `04Helitrain.ABEL` | 04: Ground Attack | 04：对地攻击 | 45 |
| `05HeavyMetal.Eden` | 05: Heavy Metal | 05：重金属 | 40 |
| `06Ninjas.EDEN` | 06: Clean Sweep | 06：全面清剿 | 42 |
| `07ShadowKiller.ABEL` | 07: Shadow Killer | 07：暗影杀手 | 64 |
| `08LoneWolf.Cain` | 08: Lone Wolf | 08：独狼 | 30 |
| `09SniperTeam.Cain` | 09: Sniper Team | 09：狙击小组 | 40 |
| `10Commander.ABEL` | 10: Commander | 10：指挥官 | 44 |
| `11CleanSweepII.EDEN` | 11: Clean Sweep II | 11：全面清剿II | 37 |
| `A01Revenge.Abel` | A1: Revenge | A1：复仇 | 46 |
| `A02Vulcan.ABEL` | A2: Vulcan | A2：火神 | 62 |
| `B01HeliTrain2.cain` | B01: Ground Attack II | B01：对地攻击II | 45 |
| `B02HMMWV.abel` | B02: HMMWV | B02：悍马 | 46 |
| `B03Chinook.eden` | B03: Chinook | B03：支奴干 | 48 |
| `C01Convoy.Eden` | C01: Convoy | C01：护送车队 | 128 |
| `C02Battlefields.Eden` | C02: Battlefields | C02：战场 | 40 |
| `Resistance/CamelAttack.Noe` | Camel Attack | 骆驼出击 | 40 |
| `Resistance/R01WarCry.Noe` | 01: War Cry | 01：战吼 | 44 |
| `Resistance/R02Laser.Noe` | 02: Laser | 02：激光引导 | 50 |
| `Resistance/R03UnderHill.noe` | 03: Under the hill | 03：山下阻击 | 37 |
| `Resistance/R04RatHole.noe` | 04: Rat's Nest | 04：鼠巢 | 54 |
| `Resistance/R05TankPlatoon.Noe` | 05: Tank Platoon | 05：坦克排 | 73 |

**24 folders; 1,282 original keys preserved plus two caption aliases = 1,284
localized keys.** Coverage includes every existing mission title/overview,
briefing, note/intel/training page, objective, localizable marker/waypoint label,
dialogue/subtitle, scripted radio, hint and debriefing value. Empty source values
stay empty. Unused stock Czech `Nadpis`/`PopisTextEndN` end-page stubs have generic
Chinese headings/descriptions, not invented narrative endings.

The text was translated directly from the installed English tables. No
historical standalone text was incorporated. CWC has since also been freshly
translated from Remastered English; historical CWC material is development
history only, not a source or credit for current shipped text.
Shared character/military terminology and existing place mappings were reused.
Minor source display typos were corrected (Lollise → Lolisse,
Saint Phillippe → Saint Philippe). Steal the Car's legacy reload instruction now
says **R**, matching Remastered's default `SDL_SCANCODE_R` rather than old **V**.

Two stock text references can be repaired without touching scripts:

- Convoy: `STRCAMP_r30` aliases the translated `STRCAMP_c01r30`, matching the
  exact spelling requested by the stock radio definition.
- War Cry: its copied outro requests `STR_c02n01`; add `任务完成`, supported by
  the corresponding stock Battlefields key. No outro/mission code changed.

## Shared overlay and geography

The original standalone pass added seven global overrides, **1,101 total**, leaving
the previous 1,094 values unchanged at that time. Subsequent spacing-only edits
are documented in [mixed CJK/Latin spacing](README.md#mixed-cjklatin-spacing).
The seven additions are:

| Key | Chinese value | Use |
| --- | --- | --- |
| `STR_DISP_SINGLE_TITLE` | 单人任务 | Mission book heading |
| `STR_SINGLE_OPEN` | 打开 | Category navigation |
| `STR_SINGLE_PLAY` | 开始 | Mission launch |
| `STR_SINGLE_RESUME` | 继续（%d/%d/%d %d:%02d） | Saved-mission resume; placeholders retained |
| `STR_RADIO` | 无线电 | Mission radio menu heading |
| `STR_RADIO_CUSTOM` | 自定义 | Shared radio reply submenu |
| `STR_OBJECTIVE_UPDATED` | 任务计划已更新 | Vulcan's scripted plan-update hint |

Existing overlay covers the encountered infantry/demolition/aircraft/tank
equipment, vehicle actions, status and commands. No duplicate base table added.
The plan-update hint and dated resume path were checked statically, not triggered
live in this pass.

New geographic mappings actually used by these missions:

| Latin | Chinese |
| --- | --- |
| Saint Louis | 圣路易 |
| Cancon | 康孔 |
| Le Port | 勒波尔 |
| Kiusk | 基乌斯克 |
| Skalice | 斯卡利采 |
| Opatov | 奥帕托夫 |

Other island/town names reuse the campaign mappings (including 艾弗隆、马尔登、
科尔古耶夫 and Resistance's 诺戈瓦 locations). Navigation/overview/intel and
localizable geographic labels now use Chinese-only town names when confirmed in
the same island's terrain shard. Island names, 洛利斯（Lolisse） and
基乌斯克（Kiusk） retain useful bilingual references; ordinary radio/dialogue and
short titles can use Chinese. Original marker identifiers, HTML attributes, keys, filenames,
callsigns and model designations are not renamed. Built-in terrain town labels
come from configuration, not baked textures, and can now use the separate
[Chinese terrain overlay](terrain/README.md). The [selective retirement
review](BILINGUAL_NAMES.md) changes 70 standalone values; Bomberman's Kolgujev
reference and all its other text remain unchanged.

## Actual-game checks

Direct launch of the installed `Remastered/PoseidonGame.exe`, OpenGL 3.3,
1280×900 window, English text/voices, subtitles on, Cadet, isolated
`game-local/test-profile`. Output was already muted and remained so; original
audio/lip-sync hashes and English voice selection were verified, not auditioned.
No normal-profile progress was changed. Not a complete mission playthrough.

- **Bomberman:** Chinese menu title/overview; plan, two objectives, map markers,
  phase/unit notes and 0-0-1/0-0-2 instructions; M21/gear labels; normal on-foot
  HUD; mission radio menu; actually issued Bravo and Charlie orders and observed
  their Chinese acknowledgements; placed one satchel and verified timer,
  detonation/disarm action labels. Did not naturally destroy the convoy/town or
  detonate the placed charge. **Success debriefing was forced with the built-in
  `ENDMISSION` cheat** and displayed Chinese heading, body, objectives, statistics
  and restart/continue controls. Final briefing, shorter unit notes and radio/
  reply-menu labels were checked after relaunch with the final shared overlay.
- **Ambush:** intro dialogue subtitle, bilingual Dourdan/Houdan briefing,
  objectives and markers; note page and successfully opened its linked training
  notes; M16/grenade gear; normal gameplay subtitles and waypoint/HUD. The
  remainder of the intro was skipped with Space, not fully watched.
- **Ground Attack II:** menu/overview, bilingual Kiusk convoy briefing,
  objectives/markers, on-foot equipment/boarding waypoint; actually boarded the
  Apache and checked cockpit speed/height/armor/fuel, cannon, convoy waypoint and
  flight-action labels. Intro skipped with Space. **No flight/combat completion.**
- **Shadow Killer:** night briefing with bilingual route/escape locations,
  objectives/markers; actual opening seven-minute radio warning, suppressed-HK
  HUD, target waypoint and demolition/night-vision actions. No assault completion.
- **Tank Platoon:** Resistance standalone menu/overview, bilingual Mirov plan,
  objectives/markers and tactical notes; actual M1A1 commander cockpit, ammunition,
  objective waypoint, tank/crew actions and squad bar. Intro skipped with Space.
  No full tank battle or fifteen-minute support/ending path.
- Scrolled root mission book through its final entries and inspected the six
  Resistance entries. All 24 titles resolved in Chinese.

Selected captures: [Bomberman selection](../../docs/zhcn-standalone/bomberman-final-selection.png),
[plan](../../docs/zhcn-standalone/bomberman-final-plan.png),
[notes](../../docs/zhcn-standalone/bomberman-final-notes.png),
[radio menu](../../docs/zhcn-standalone/bomberman-final-radio-menu.png),
[Bravo reply](../../docs/zhcn-standalone/bomberman-bravo-reply.png),
[Charlie/actions](../../docs/zhcn-standalone/bomberman-actions-radio.png),
[placed charge](../../docs/zhcn-standalone/bomberman-placed-charge.png),
[forced debrief](../../docs/zhcn-standalone/bomberman-debrief.png),
[Ambush training notes](../../docs/zhcn-standalone/ambush-training-notes.png),
[Apache cockpit](../../docs/zhcn-standalone/ground-attack2-board-action.png),
[night radio](../../docs/zhcn-standalone/shadow-killer-gameplay.png), and
[tank cockpit](../../docs/zhcn-standalone/tank-platoon-cockpit.png).

## Validation and limits

All three existing/focused validators pass with the final deployed tables:

```text
python localization/zhcn-combined-arms/validate_campaign.py
python localization/zhcn-combined-arms/validate_resistance.py
python localization/zhcn-combined-arms/validate_standalone.py
```

Standalone checks require the local original backup and fontTools: all 24
installed mission folders, exact key/case/order (except the two documented
aliases), strict UTF-8 and row shape, no duplicate keys/replacement characters,
placeholders, `$STR_` references, HTML tags/attributes/marker targets and `\n`
tokens, all five fonts' coverage, backup hashes and deployed byte equality.
**All 7,580 other installed game files retain their pre-pass SHA-256 hashes**,
including both campaigns, executable/UI resources, HTML, scripts, voices and
lip-sync. No engine/UI/font/mission-logic/audio files changed.

Known limits:

- Eleven stock audio-caption references have no English transcript in the
  installed tables: Chinook `STRCAMP_b02r05`, `STRCAMP_b02r08`; Convoy
  `STRCAMP_c01r20`, `r21`, `r22`, `r23`, `r39`, `r40`, `v09`, `v10` (each with
  the `STRCAMP_c01` prefix); Tank Platoon `STRD_R05v09`. They remain stock;
  **no invented captions**. Two source-supported aliases are repaired above.
- The later [generated-label pass](GENERATED_NAMES.md) localizes `Resistance...`
  through an optional engine lookup without renaming the directory, and adds
  six Ambush identity metadata fields. These require its rebuilt client.
  Minor character/callsign names,
  key labels such as `Backspace`, models and
  English artwork remain. These are not missing mission prose.
- No missing glyphs or mojibake appeared in checked screens; fonts are unchanged.
  Stock wrapping can put Chinese punctuation or a closing bilingual parenthesis
  at the start of a line. Long untested pages/other resolutions may need small
  text-only tuning. No UI/layout redesign attempted.
- All other mission branches, late dialogues and alternate/failure debriefs are
  statically validated, not manually played. Wizard/custom/multiplayer content
  and obscure shared settings/editor text are not claimed localized.

## Deployment and reversal

The subsequent [unit-designator cleanup](UNIT_DESIGNATORS.md) updates 115 values
across these missions, including Bomberman's B小队/C小队, Infantry's A排,
Revenge's B组 and aircraft N一号. Generated radio sender labels are now covered
by the separate [generated-label pass](GENERATED_NAMES.md);
semantic callsigns, geographic policy and caption repairs are unchanged.

Close the game first. The current local patch is deployed. Before a fresh
deployment, back up all 24 corresponding installed CSVs under `Missions/` with
relative paths retained, plus the previous shared mod overlay. **Never overwrite
English originals with already-localized tables.** Also back up Ambush's exact
`02Infantry.Abel/description.ext` before copying the added identity metadata.
Copy `standalone/` CSVs and that description file
to their matching `Missions/` paths and the new shared overlay to the existing
`@zhcn-prototype/bin/`; retain the existing five fonts. The README's redeployment
example includes these steps and the unchanged mod/English launch settings.

This installation's ignored backup is
`game-local/localization-backup/standalone-original/`: `reversal.json` records
24 exact targets, all originally present, and their original SHA-256 hashes;
`before-hashes.json` is the whole-install baseline. To undo **only this pass**,
verify each backup hash and restore those 24 CSVs to the same relative paths
under `Remastered/Missions/`. Restore `pre-standalone-global.utf8.csv` to
`Remastered/@zhcn-prototype/bin/stringtable.utf8.csv` to return to the previous
1,094-key overlay. This preserves both translated campaigns and all fonts.
Do not delete a mission/campaign directory or touch saves. Merely disabling the
mod does not reverse in-place mission-table replacements. The later Ambush
description backup is separately verified against the original whole-install
baseline; it is not part of the older 24-CSV reversal inventory. Restore it too
when undoing identity metadata; never delete its mission directory.
