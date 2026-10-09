# Generated identity, group and category labels

This pass addresses configured story identities, generated group display names
and the official standalone folder category. It does not expand general UI
coverage. Selectable Chinese and current deployment are now documented in
[LANGUAGE_SUPPORT.md](LANGUAGE_SUPPORT.md); older tests below used the prototype.

## Sources and implementation

- `Campaigns/1985/description.ext`, `Campaigns/resistance/description.ext` and
  `Missions/02Infantry.Abel/description.ext` contain literal `CfgIdentities/name`
  values. Add optional `nameKey` metadata to 15, six and six assignments,
  respectively: **27 references to 25 distinct names**. Original `name`, class
  identifiers, faces, speakers and pitches remain intact. Existing localized
  Viktor/Victor entries now use a canonical-only table key (Chinese falls back to
  `Victor Troska`, while all stock language spellings remain exact) with their
  existing localized key in separate `nameKey` metadata, preventing Chinese script names.
- `AIUnit::Load` and the existing `setIdentity` implementation retain the stock
  name in `AIUnitInfo::_name` and read an optional separate `_displayNameKey`.
  UI headers, rosters, equipment/debriefing pages, HUD/cursor and targeting menus
  use `GetDisplayName()`; a missing/empty translation falls back to the canonical
  name. The scripting `name` command, statistics, face/player-name lookup and
  network payload continue to use the canonical field. A silent
  `TryLocalizeString` avoids missing-string debug messages for absent metadata.
  Arbitrary profile/player names are never matched or translated.
  Changed engine files: `AI/AIUnit.cpp`, `Game/Commands/GameStateExtUi.cpp`,
  `UI/OptionsUIImpl.cpp`, `UI/Locale/Stringtable/Stringtable.cpp/.hpp`, and new
  `UI/Locale/IdentityLocalization.hpp` (all beneath `engine/Poseidon/`). The
  compatibility follow-up also changes `AI/VehicleAI.hpp`, `AI/AICenterImpl.cpp`,
  `World/Entities/Infantry/Person.cpp`, `Network/NetworkClientOnMessage.cpp` and
  the six UI display consumers above. Profile assignments/network reception
  clear presentation metadata; no arbitrary-name matching is introduced.
- `CfgWorlds/GroupNames` and `GroupColors` already reference stock stringtable
  keys. Add **26** overrides: 12 phonetic letter labels, three numeric labels,
  four semantic callsigns and seven colors in `stringtable_groups.utf8.csv`.
  Its other seven columns preserve the stock values, transcoded from their
  original per-column codepages to UTF-8 and checked against the stock table.
  Known-stock coverage is now **1,127 keys**, while the existing 1,101-key file
  is byte-identical. No group construction, radio, save or network code changes.
- `DisplaySingleMission::ScanMissionDirectory` previously displayed the literal
  directory name plus `...`. Its Resistance branch now optionally resolves
  `STR_SINGLE_CATEGORY_RESISTANCE`, while retaining the original directory in
  list data and leaving mission discovery/navigation unchanged.

The separate `mod/bin/stringtable_generated.utf8.csv` has **26 custom keys**:
25 identities and one category. Chinese now uses ChineseSimplified. All eight
stock columns explicitly preserve each original name and `Resistance`; the same
display-key mechanism is used, with no Chinese literal in engine source.

## Names and formation conventions

David Armstrong → 戴维·阿姆斯特朗; James Gastovski → 詹姆斯·加斯托夫斯基;
Robert Hammer → 罗伯特·哈默; Sam Nichols → 山姆·尼科尔斯.
Other story identities retain established Chinese narrative names, including
贝尔霍夫、科兹洛夫斯基、福利、布莱克、古巴、安吉丽娜 and 斯托扬.
Several stock full-name literals disagree with narrative names (e.g. Berghoff's
`Arnold Wesley`); Chinese uses the established narrative name, while the exact
stock literal remains the fallback in every other shipped column.

Generated phonetics use **A组/B组/C组/.../Y组/Z组**. The generic configuration
does not encode squad/platoon echelon, so it must not call every group a 小队
or 排. Context-specific authored forms such as A小队、A排、N编队 are unchanged.
The number in `A组 8` is the stock unit/member ID, not a renamed group ID.
Numbered groups use 二号/三号/六号; Buffalo/Guardian/Convoy/Fox use 水牛/卫士/
车队/狐狸. Group colors use 黑色/红色/绿色/蓝色/黄色/橙色/粉红色.
Canonical group letter/color names, script identity classes and group archive
fields are unchanged; semantic callsigns in authored dialogue remain unchanged.

## Build, deployment and reversal

**Identity metadata and the category hook require a rebuilt client.** The
original GOG `game-local/Remastered/PoseidonGame.exe` and its DLLs are untouched;
that client ignores `nameKey` and retains the folder category. Group overrides
use the existing data path and do not require a new client.

The verified local build is `dist/local-labels/PoseidonGame.exe` (GL33), with its
own adjacent OpenAL DLL. Launch it with Remastered as the working directory and
the absolute `@zhcn-prototype` mod path; see the main README. Build outputs and
tools are ignored, not a release package. No installer is supplied.

Deploy the new generated-name and group shards alongside existing mod tables. Campaign
description files are already covered by their original reversal inventories.
Ambush additionally requires backing up/restoring the exact
`Missions/02Infantry.Abel/description.ext` file. Its verified original is at
`game-local/localization-backup/standalone-original/02Infantry.Abel/description.ext`;
the older 24-target reversal inventory covers CSVs only. The standalone
description preserves stock bytes after stripping six metadata lines, except
one final newline. Never replace an original backup with localized content.

Without the mod, these new identity/category keys are absent and stock literal
fallbacks apply; group keys come from stock tables. Full patch reversal still
requires restoring in-place mission/campaign CSVs and descriptions. Display
names resolve the active language when the UI is refreshed, not when identity
is assigned. New saves keep the canonical `name` and add the optional
`displayNameKey` metadata; absent keys default to empty in old saves. No save
version or network schema changes. Older readers ignore the extra property.
This is backwards-compatible optional metadata, not byte-identical archives.
Saves made by the initial `56138f0` client may already contain translated names
without that metadata. They are not guessed/migrated: replay the mission to
recreate canonical identities. Stock saves without metadata retain stock names.

## Verification

- Built `PoseidonGame` and `PoseidonCoreTests`, Clang 21.1.8, RelWithDebInfo.
- After the compatibility fix, `[generated-names]`: **5 cases / 50 assertions**,
  including canonical-field/context preservation, clearing stale opt-in data,
  a binary identity save/load and a legacy save with no display metadata.
  Stringtable and
  localized-ParamFile tests: **57 / 209**; broader stringtable/ParamFile focused
  run: **345 / 1,234**. Five pre-existing disabled-test warnings remain; this is
  not a claim that the complete engine test suite was run.
- All three campaign/standalone validators pass, including configuration
  fallback/baseline checks, deployed byte equality and all five fonts. Terrain
  `build_labels.py --check` passes its 62 labels and stock-input hashes.
  No campaign/standalone prose, terrain output, font, mission script, voice,
  lip-sync or original executable changes. The Combined Arms mirror remains
  byte-identical. Validators allow only the narrowly documented metadata/config
  additions and exact new group-key set.
  The copied Ambush description retains stock trailing whitespace: Git's
  staged whitespace check flags those pre-existing lines. The check passes
  excluding that exact stock-derived file; validators verify its otherwise
  byte-exact preservation rather than stripping/reformatting it.
- Actual rebuilt GL33 client against isolated GOG 3.05 data/profile, 1280×900:
  Flashpoint campaign replay shows **任务简报（戴维·阿姆斯特朗，A组 8）**.
  Combined Arms loads its Chinese plan/objectives and normal truck gameplay,
  including existing Chinese HUD/radio replies. No full mission completion.
- Single Missions shows **抵抗力量...**; opening it displays the six original
  Resistance missions and parent navigation. No directory renaming.
- Ambush loads normally and its briefing roster shows **詹姆斯·艾布拉姆斯**;
  the generated header shows **C组 黑色 2**. The user-entered **KyouKyou** name
  remains unchanged. The runtime identity query agrees with the visible roster.
- Fresh launch without the mod shows **David Armstrong, Alpha 8** and
  **Resistance...**. This is a comparison of the new labels, not a full patch
  reversal: existing Chinese CSVs remain deployed and need their mod fonts.
- French with the mod retains **Resistance...**, **David Armstrong** and stock
  group labels; optional-name unit tests also
  verify French stock-name fallback and synthetic future Simplified/Traditional
  columns. No claim that the entire existing English-column patch is language-
  isolated: that remains the proper-language roadmap phase.

Chinese-label screens showed no new missing glyphs, mojibake or clipping.
Tests stayed muted and normal-profile progress was untouched. The campaign
unlock helper operated only on the disposable test profile.

Compatibility follow-up: installed CWC/Resistance/standalone loose scripts and
embedded mission initializers contain no active scripting `name` queries or
comparisons. This does not prove custom-script compatibility by itself; the
canonical-field fix is what preserves that contract.

Actual rebuilt-client Flashpoint replay shows the Chinese briefing identity
while `(name player) == "David Armstrong"` is true. A labelled disposable binary
world save was made with the existing `triSaveGame` helper; the live identity was
then changed to James and a probe variable altered. `triLoadGame` restores
**David Armstrong** and the original probe value. The refreshed in-mission
roster displays **戴维·阿姆斯特朗**, 贝尔霍夫、福利 and 科兹洛夫斯基. Switching
to French restores their stock name literals; `name player` stays English in
both cases. This exercises the real `World::SaveBin/LoadBin` path, not a natural
pause-menu save/full mission completion. No mission files or normal-profile
progress changed. Multiplayer sessions/old-reader loading remain untested;
display metadata is deliberately not transmitted over the stock network path.

## Remaining limits

Random/generated NPC-name pools, user/profile names (deliberately untouched),
existing roster rank abbreviations/skill labels (`Col.`, `Corp.`, `Expert`),
unrelated loading/config literals, wizard/editor/multiplayer strings and general
residual English belong to the next coverage audit. Individual identities and
all group/color combinations were statically checked, not each visually played.
Old translated saves, multiplayer interoperability and all seven non-Chinese
languages were not exhaustively exercised; their identifiers/data columns are
preserved. Remote units can retain canonical English display names when no
local identity assignment supplies the optional display key.
Archived statistics/name snapshots and chat/network identity labels remain
canonical; translating those safely at presentation boundaries is not part of
this bounded compatibility fix.
