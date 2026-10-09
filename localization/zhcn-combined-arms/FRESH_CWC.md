# Fresh Cold War Crisis translation — 2026-10-08

## Source and coverage

All **1,928 campaign keys**, across **78 mission/support folders and the shared
root table**, were processed against the current GOG Remastered 3.05 English
source. The original installed mission CSVs are preserved in
`game-local/localization-backup/1985-original/`, with their reversal-manifest
SHA-256 hashes verified before translation. The original, untouched installed
`Campaigns/1985/stringtable.csv` supplies the shared English column.

These are the originals from this installation, not English extracted from an
old OFP release. The two established stock-caption repairs remain:
Training `STRM_00v16a` translates the English of `STRM_00v16`, and Killdozer
`STR_END` supplies “Mission completed” for the existing script reference.

The previous Chinese sentences were not translation input. A disposable helper
read their **ordered keys and HTML tag/attribute metadata only**, retaining the
tested formatting and link repairs. Fresh worksheets were written from English;
complete replacement CSVs were then produced mechanically. Worksheets, source
copies and audit receipts remain ignored under `game-local/`, not shipped tooling.

No historical Chinese CWC wording is intentionally used as a translation source.
The README now identifies the shipped CWC text as fresh Remastered-English
translation, removes historical-translation reuse credits/licensing caveats,
and distinguishes previous prototype screenshots from current evidence.
Resistance and standalone source/provenance are unchanged; their documentation
only updates cross-references to the now-fresh CWC translation.

## Conventions and review

Retained project character names include 阿姆斯特朗、加斯托夫斯基、哈默、尼科尔斯、
贝尔霍夫、福利、科兹洛夫斯基、布莱克、古巴 and 安吉丽娜. Callsigns include
熊爸爸、黑熊、白狼 and 鹰眼. The subsequent [unit-designator pass](UNIT_DESIGNATORS.md)
replaces functional phonetic words with A小队/B小队, Y排, N编队 and other
context-appropriate letter-based forms. Ranks use 列兵、下士、中士、中尉、上尉、少校、上校 and
将军; terminology distinguishes 弹匣、装填、装甲输送车、步兵战车 and weapon/model
designations. Geographic spellings remain unchanged. The later
[selective bilingual-name retirement](BILINGUAL_NAMES.md) uses Chinese-only
town names where the same island's terrain overlay confirms coverage, including
Status Quo's destination choices; island/unlabelled-place references remain bilingual.

Dialogue, narration, diaries, tutorials, objectives, debriefings and support
cutscenes were rewritten from English, then reviewed as Chinese text. Examples
include Camping's letter-guessing joke (G / Gun / Jeep / Grass, retained explicitly
so the joke still works), Alert's wager, Armstrong's negotiations with the
resistance, Hammer's bravado, Nicholls's personal diary and the nuclear-threat
finale. Obvious English typos are rendered by their intended meaning, without
rewriting events or inventing captions for untranscribed audio.

All entries were processed. The six formerly Latin-only unit-marker values
(Turning the Tide's Bravo; Return to Eden's Bravo/Charlie/November; Search and
Destroy's Zulu/November) have since become B小队, C小队, N编队 or Z坦克分队
in the unit-designator pass. They are no longer intentional English exceptions.

Eleven empty English values remain empty: Air Assault, Wake-up Call and Incursion's
empty intel heading/body pairs; `STR_x00v15`; `STR_x06v20`, `STR_x06v21`,
`STR_x06v22`; and root `STRC_01`. No caption was invented for them.
Simple Chinese labels/titles may coincide with prior versions because they were
independently translated to the same natural wording, not retained as legacy prose.
The already-correct campaign/chapter display labels were reviewed against English
and left unchanged. Latin minor names, product names, callsigns, model numbers,
coordinates, key labels and internal references remain where appropriate.

## Static validation and unchanged files

All three existing validators pass after deployment:

- CWC: **78 folders, 1,928 keys, 1,101 global overrides**.
- Resistance: **39 folders, 1,310 keys**.
- Standalone: **24 folders, 1,284 keys**; its seven earlier global additions remain.

An additional disposable audit against the pre-rewrite metadata verifies exact
ordered keys/case, all literal `\n` tokens, original HTML tags/attributes and
empty-source handling across the 1,928 CWC keys. Existing validators check strict
UTF-8, duplicate/malformed rows, placeholders, `$STR_` references, links/marker
targets, deployment equality and coverage in all five unchanged fonts.

The existing Resistance/standalone validators only add the **79 CWC CSV targets**
to their later-pass exemptions, because their old whole-install baselines contain
the previous CWC wording. They still protect CWC's non-CSV files. No validator
architecture was redesigned. A fresh whole-install baseline independently verifies
**7,526 non-target files unchanged**, with no files added or removed in Remastered.
That includes all Resistance/standalone prose, global overlay, fonts, executable,
engine/UI resources, campaign configuration, scripts, HTML, audio and lip-sync.
The original CWC validator also verifies its 3,706 unrelated campaign-file hashes.

The shared overlay is **unchanged: zero new or changed global overrides**. No
engine/UI, font, mission logic, audio or lip-sync changes were needed. Deployment
and reversal remain exactly as documented in the README. The Combined Arms
prototype mirror is kept identical to the new campaign table.

## Current in-game checks

Fresh-text checks were performed on **2026-10-08** in the installed
`game-local/Remastered/PoseidonGame.exe`, version **3.05 / GL33**, with the existing
Chinese mod, English language column and isolated `game-local/test-profile`.
The ordinary campaign menu and stock campaign-unlock cheat selected missions;
no missions were copied into an editor or altered for testing. Previous-pass
screenshots are not the evidence for these checks.

| Mission | Fresh text visually verified |
| --- | --- |
| Flashpoint / 战火初燃 | Campaign-list title/preview, map-only briefing and start marker, opening helicopter conversation subtitles, controls hint and waypoint HUD. Its stock `showNotepad = 0` intentionally hides the notebook. |
| Combined Arms / 联合作战 | Campaign title/preview, plan and objectives, bilingual Regina references, diary with continuation arrow, truck conversation subtitles, waypoint HUD and in-mission map; failure debriefing and objective list. |
| Battle of Houdan / 乌当之战 | Briefing/objectives and Houdan/Dourdan references, opening tank squad radio, ammunition HUD, commander/vehicle actions. |
| Airborne / 空中运输 | Briefing/objectives and Montignac reference, pilot diary, helicopter-control hints, Blackhawk target name and pickup waypoint; entered the helicopter. No full flight or evacuation was completed. |
| Incursion / 潜入 | Late-campaign briefing/objectives/markers, full visible diary page, opening scripted radio, document waypoint and suppressed-HK HUD. |

Combined Arms' failure debriefing was **forced with the stock `endmission` cheat**,
not earned by completing its objectives. No whole mission, campaign finale,
success branch or complete campaign playthrough is claimed. Later triggered
dialogue, alternate outcomes and every diary continuation/tactical-note page
remain statically validated rather than individually observed. Tests were muted;
unchanged audio/lip-sync hashes establish preservation of the original voices,
not an audible listening test.

A final Combined Arms pass made its introductory subtitle less literal and
shortened the plan wording. Keeping “村” after the Regina link avoids a lone
full stop at the next line's start. The resulting text was reloaded and checked
in the actual mission map and opening conversation. No new manual `<br>` tags
or font/UI changes were introduced.

No missing-glyph boxes, mojibake, clipped subtitles or blocked reading were
observed in these checks. Existing notebook wrapping can still leave punctuation
at a line start, especially in Combined Arms' longer diary, and split a Latin
name across lines in Airborne's briefing. At this rewrite milestone, base-map
town names and identity headers still retained stock Latin text. Subsequently,
the [terrain overlay](terrain/README.md) and [selective name retirement](BILINGUAL_NAMES.md)
localized covered towns and removed their redundant suffixes; generated identity
headers remain a later roadmap item. Original captures below predate those passes.

Selected current screenshots are in [`docs/zhcn-1985-fresh`](../../docs/zhcn-1985-fresh):
campaign selection; Flashpoint dialogue; Combined Arms map, diary, dialogue and
forced debriefing; tank radio/HUD; Airborne briefing/controls; and Incursion
diary/radio. Temporary keyboard state was restored and the test game was closed.
