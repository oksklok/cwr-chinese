# Ready-to-use distribution

This is a free community translation mod for Windows 10/11 x64 Remastered 3.05.
`cwr-chinese.zip` contains `Remastered/`, with `@cwr-chinese/`, `cwr-chinese.exe`
and `README-cwr-chinese.txt` inside. Extract into the top-level game installation
folder containing Remastered, then run Remastered/cwr-chinese.exe, which preserves
other selected mods. Select SC/TC in the game's normal text-language menu.
Delete those three entries inside Remastered to remove it; keep Remastered itself.
Stock assets/executable, saves and
unrelated mods are untouched. The README uses a distinct name to avoid replacing
a game's existing README.

All content is ready-made: 218 translated tables, 169 display-reference/Chinese HTML files,
24 standalone banks, 30 multiplayer banks, 36 templates, terrain and UI overlays,
ten Chinese fonts, localization client/OpenAL, source and notices. No player-side
Python, PyInstaller, preparation executable/marker, source inventory validation,
installer, registry, backup or recovery machinery remains.

## In-game editorial follow-up — 2026-10-10

`game-local/cwr-chinese-editorial-final/cwr-chinese.zip`: **132,422,708 bytes**;
SHA-256 `ce540aebf65544fd58a8508bac4fbe2e7b9be6ad10a002256180f46de1826ea1`.
Packaged main `c29eeb9`, unchanged client `a151692`. Previous editorial ZIP preserved.

Seven SC/TC keys corrected after isolated GOG mission checks: Killdozer's Zulu
support unit, Hold Malden's actual gunner action, Hold City's capture ending,
and four East-side Demolition Squad briefing fragments. West's flag-ownership
wording was verified correct and retained; the original tank-commander speaker
label remains an editorial choice. Stock languages, links, logic, fonts and
client are unchanged. Checks used controlled radio/flag/end states, not full
playthroughs or a Steam acceptance rerun.

Passed: exact seven-key/stock-column comparison, ten-font coverage, eight existing
CSV/packaging/template tests, all content builders and deployment checks, ZIP CRC
and packaged-table equality. Only two campaign tables and two MP banks changed
outside source/receipts; all MP non-table members and other shipped assets are
byte-identical. The rebuilt ZIP was not subjected to another in-game run.

## Consolidated linguistic corrections — 2026-10-10

`game-local/cwr-chinese-editorial/cwr-chinese.zip`: **132,422,240 bytes**;
SHA-256 `9a75c704abf82988f222311c620f87cbdef818d32ca76e2ea04a7e185d4a98c3`.
Packaged main `0cb594a`, unchanged client `a151692`. Previous polish ZIP preserved.

Applied the master workbook's 441 actionable recommendations: 401 string keys
across 130 tables and 40 linked HTML paragraphs in 15 wizard templates. Five
editorial questions and optional/rejected proposals remain unapplied. English
and other stock-language cells, links, placeholders, mission logic and existing
font outlines/metrics are preserved. Only 15 required characters were added to
each Traditional font subset; Simplified fonts and the client remain unchanged.

Passed: reconstruction of all 217 tables / 11,155 bilingual entries, exact
comparison with the approved replacements, existing CSV/format/link checks,
ten-font coverage, all content builders and deployment checks, and eight focused
CSV/packaging/template tests. The new template test checks that Chinese HTML is
added without changing stock HTML or scripts. Actual Steam inputs reconstructed
the same 386 table/HTML/reference files as GOG. Archive CRC, player-facing layout,
unchanged client/runtime/launcher and Simplified fonts were verified in the ZIP.
This pass is not a new in-game
GOG/Steam acceptance run; earlier physical results below are historical.

## Native executable test

On 2026-10-09 the actual stock GOG and Steam executables (3.05, identical SHA-256
`b501e6e6e617b65570ff313cbf3ec5a3ac758a2897710c0491417d830972e7e5`) were launched
directly with an isolated native probe mod and profiles. The probe supplied
CfgLanguages through master config-extra and an addon, UTF-8 translations, fonts,
one standalone mission and sparse campaign text banks.

Both rendered Simplified Chinese when selected through the diagnostic harness;
Bomberman briefing and gameplay worked, with English voice selection. Wrapping
was readable in that briefing. But both normal language pickers cycled from
English to Russian, omitting SC/TC; forced Chinese still displayed English as
the selected option. Stock master config-extra restoration overwrites the mod
language registry. Steam also showed missing Traditional glyphs despite both
language font folders being present: stock ignores fontDirectory. Original
campaign titles stayed English. These are observed stock limitations, not a
claim that stock lacks UTF-8 support. Diagnostic forced language is not a usable
player launch workflow. Existing focused client fixes are retained.

The client redirects campaign CSV/description, Chinese briefing HTML and mission-definition lookup,
retaining stock campaign discovery and saves. Definition edits only replace
display literals with stringtable references; scripts and mission logic stay
unchanged. Other mod loading stays native.
Its window title is simply Poseidon; metadata and notices identify the modified client.
GPL Section 7 prohibits Bohemia trademark branding of a modified program, so
the borrowed stock icon and branded executable/startup strings were removed.

## Ready-made asset licensing

The official [CWR README](https://github.com/BohemiaInteractive/CWR/blob/main/README.md)
explicitly assigns retail game data (including missions) to APL-SA.
[APL-SA sections 2–3](https://old.bohemia.net/community/licenses/arma-public-license-share-alike)
permit noncommercial Arma-only sharing/adaptation, with attribution, modification
notices and share-alike licensing. Therefore reconstructed multilingual tables,
descriptions, mission/template banks and terrain/config overlays can ship
ready-made under APL-SA, separately from GPL code and OFL fonts. Their retained
stock bytes are not grounds for requiring player-side preparation.
No original executable or standalone playable game is distributed.
See distribution/COMPONENTS.txt for attribution, license links and disclaimers.

Only Windows x64 Remastered 3.05 is targeted. No storefront/hash lock is imposed
on players. Conflicting configuration/total-conversion mods, original 1.96/1.99
and future updates are outside scope. Three Microsoft x64 VC++ 2022 runtime DLLs
are included beside the client under Microsoft's redistribution terms; Windows
supplies UCRT. No VC++ installation step is needed. The native launcher is built
with a static CRT, forwards optional arguments and has no console window.
Both executables use an original gold five-pointed star icon, not proprietary artwork.

## Briefing and presentation polish — 2026-10-10

`game-local/cwr-chinese-polish/cwr-chinese.zip`: **132,384,581 bytes**;
SHA-256 `0a5a7bf2dba6e94c577d566fb72186fa63387c41272e7dadbc792417f542c014`.
Packaged main `b895f86`, client `a151692`. The previous visual-pass ZIP remains
byte-identical. The final ZIP was extracted into the GOG test installation's
top-level directory and launched through its native launcher: current client,
Chinese Heavy Metal briefing and the previously selected personal mod verified.
Windows title-bar/taskbar star verified; extracted launcher/client icons and live
small/large window icons match. Fonts, terrain and UI addons match the prior ZIP
byte-for-byte; the original executable is unchanged. No public release was made.

One focused briefing review covered both campaigns, all 24 standalone missions
and 30 authored multiplayer missions. Finite Chinese-only HTML variants cover
20 Resistance, 24 standalone and 21 multiplayer briefings (130 SC/TC files).
The client permits these two Chinese briefing filenames through its existing
campaign-text lookup; original HTML and other-language behavior stay unchanged.
Fragment corrections include Heavy Metal's rendezvous sentence, Shadow Killer's
fuel-station objective, and missing endings in Ambush/Tank Platoon/Clean Sweep.
185 bilingual rows changed in total, including 138 geographic-name rows. Chinese
prose no longer appends Latin island/unlabelled-place names. Terrain labels,
links/targets, keys, stock columns, mission logic, voices and font files are unchanged.

Keyboard rows now separate action/primary/secondary geometry and click targets,
with bounded hover scrolling before the scrollbar. Font size was not reduced.
Only Chinese campaign-book serif text loses the extra 0.75 horizontal squeeze;
English, the book perspective, font style and already-corrected screens are unchanged.
The existing icon generator now makes a gold star shared by both executables.

GOG physical checks covered SC/TC/English Heavy Metal and Shadow Killer briefing
text, CWC Combined Arms and Resistance Contact, Chinese-only island prose,
campaign-book typography, both binding edits and long-name hover scrolling.
Tested marker links: Heavy Metal join; Shadow Killer pumpa/Konvoj1/End1;
Combined Arms Regina; Contact Start/Kon1. All four missions reached gameplay.
Captures: `game-local/public-captures/*polish*`. Steam gameplay was not repeated
in this bounded pass; previous GOG/Steam distribution acceptance is recorded below.

Passed: 81 UI/font/wrap/scroll cases (4,568 assertions), 56 stringtable/date cases
(264 assertions), four packaging tests, three stock-CSV tests, and existing
content reconstruction/deployment checks. No new audit tool or player machinery.

## Earlier bounded usability pass — 2026-10-10

`game-local/cwr-chinese-visual/cwr-chinese.zip`: **132,297,921 bytes**;
SHA-256 `e521ac03e7d10e3214c426cf17e7fde7422b14ba69de6aae67b6dca3a289682f`.
Packaged main `8127f13`, client `08a7cb6`. The previous mission-QA ZIP is preserved.

The ZIP now puts its three player-facing entries under `Remastered/`. Extract
into the parent game directory on both GOG and Steam. No launcher changes.
Chinese mono text no longer receives the extra 0.75 3D horizontal squeeze,
including the mission book's HTML overview. Font files, heights, title/serif
proportions and stock-language typography are unchanged. Chinese handwriting
keeps its face and metrics with 0.3 px less synthetic stroke erosion; ink was
already opaque black. Settings labels/hints retain scrolling with Chinese-sized
budgets. Binding values gain unused right margin; long names still scroll on hover.
Numeric `%m` enables Chinese dates. Two Chinese-only Bomberman HTML variants
remove 14 literal link-adjacent spaces; original HTML, targets and text remain.

GOG before/after inspection covered settings, mission book, MODS, LAN browser,
handwriting, bindings and editor dates. SC/TC showed `周五，5月10日` /
`週五，5月10日`; English remained `Fri, May 10`. English settings/briefing
comparison passed. Bomberman SC/TC spacing and Start/Dot_6/Kon marker links passed.
The final ZIP was extracted into both top-level game directories and launched
through the native launcher with isolated test profiles. Steam reached the Chinese
Bomberman briefing and gameplay with English voices; its three marker links passed.
GOG retained the separately enabled personal mod. Both stock executable hashes
remain unchanged. Test mod extractions remain present: the execution layer blocked
cleanup commands, so removal was not re-tested in this pass. No stock files changed.

Build/content/deployment checks passed (217 tables, 24 standalone, 30 multiplayer,
36 templates and terrain/UI overlays), as did 80 focused UI/font/wrap/scroll tests
(4,552 assertions), 56 stringtable/date tests (261 assertions), four ZIP tests and
three stock-CSV tests. No mission/geographic-name/audio changes or wider UI audit.

## Mission display-text QA — 2026-10-10

`game-local/cwr-chinese-mission-qa/cwr-chinese.zip`: **132,286,462 bytes**;
SHA-256 `3eb03843160d20fb225683394b0f954c88378da9fd9d609796dd34fecf8e57cf`.
Packaged main `443c916`, client `c4bd5a9`. Previous working ZIPs are preserved.

One bounded pass inspected 875 mission definition/script files across both
official campaigns, all 24 standalone and all 30 authored multiplayer missions.
Fixed Lone Wolf's destroy/leave waypoints, Sniper Team's two literal enemy-base
markers, Ambush's location card, Camel Attack/Bridge loading captions, CWC
Status Quo's Pub marker and Combined Arms' conditional WORKING MESSAGE.
Reused existing keys for Sniper Team/Camel Attack; six new bilingual rows retain
the exact stock literals in other languages. Unused Resistance prototype
scripts, cheat-only debug hints, identifiers and already-localized MP references
were excluded. No further live omissions were found in this bounded pass.

Also corrected only the generic Get In waypoint to 登乘, eight Shadow Killer SC
radio lines in each of SP/MP to 剑鱼 (TC already 劍魚), and the three MODS catalog/
source labels to 在线模组 / 線上模組. Narrative boarding text is unchanged.
Campaign definition lookup reuses the existing localization overlay search;
two mission.sqm derivatives change only display references, not mission logic.

Exact ZIP physically checked on disposable GOG 3.05 with an isolated profile:
Lone Wolf waypoint, Sniper Team warning marker and Ambush post-intro loading
card in SC/TC/English; Status Quo's Pub marker in TC/English; MODS catalog in SC;
Combined Arms briefing and playable start. Campaign selection used the existing
unlock helper only in the disposable profile. Captures: `game-local/public-captures/qa-*`
and numbered `*_qa-*`. Not a full playthrough or a Steam gameplay retest.

Passed: client build; 95 focused client cases / 1,575 assertions; 56 stringtable
core cases / 259 assertions; three CSV and four packaging tests; all four content
builders and their deployment checks. Reconstructed 217 tables / nine reference
files; 11,154 bilingual rows, exactly 20 corrected rows and six additions, all
existing stock-language columns preserved; all ten unchanged fonts cover the text.
No remaining in-scope blocker. No public release or tag.

## First-launch language update — 2026-10-09

`game-local/cwr-chinese-language/cwr-chinese.zip`: **132,258,450 bytes**;
SHA-256 `890c38133e65496b926bcd505c0918b0e50948b471050e11bfdacd3e3d5e9d57`.
Packaged main `0221893`, client `28918ce`. Earlier ZIPs are preserved.

With the mod's Chinese languages registered, one `cwr-chinese-language.cfg`
in the normal user settings directory stores the text choice. A missing mod
preference starts in SC, retaining an earlier SC/TC value from `game.cfg`.
Established mod preferences, including English/French, take priority. Mod saves
leave the stock text/voice language fields intact. No launcher or content changes.

Passed: client build and 12 focused settings cases / 138 assertions, including
old SC/TC choices, stock English/French, persisted TC/English/French and no-mod
behavior. Practical check on disposable GOG 3.05 with the exact ZIP: existing
stock English -> first mod launch SC -> normal menu change/quit/relaunch TC ->
normal menu change/quit/relaunch English -> original executable still English.
The stock language fields and original executable stayed unchanged. The copied
test profile's stale reference to an already-removed test addon was removed
before the successful sequence. No Steam or broad gameplay retest in this pass.

## Native-launcher ZIP acceptance — 2026-10-09

Artifact: `game-local/cwr-chinese-public/cwr-chinese.zip`, **132,253,867 bytes**.
SHA-256: `924c06c32856bedf7329ac4d0a09938ab08014ae13b7a8fc83168ad3fb0a8a42`.
Packaged main: `9504b08310da25ea73f6efdde040cb584b9b4232`.
Client: `4902d20085ab60e5e3bfb10fb6dd73b8d14307df` (pinned by main).
The previous ready-made ZIP below remains byte-identical.

This exact archive was extracted into disposable GOG and actual Steam 3.05
(app 65790, BuildID 24792092). Both native launchers worked with no arguments,
from a different working directory; forwarded window/log arguments also worked,
including a quoted path with spaces. The launcher is a 405,504-byte x64 GUI
executable importing only USER32/KERNEL32, with no console or external CRT.
The client and OpenAL loaded all three VC++ DLLs from `@cwr-chinese/client`,
not System32; only OS UCRT came from Windows. No redistributable installation
was performed. This was module-path/import verification on the available PC,
not a separate pristine-Windows VM test. DLL file version: 14.44.35211.0.

Both passed normal SC/TC selection, English voice selection, other saved mod
loading (independent addon class verified), CWC Combined Arms, Resistance
Contact and standalone Bomberman Chinese briefings and playable mission starts.
English/French text switching also passed. Normal quit/relaunch retained TC on
GOG and SC on Steam. The window title was Poseidon; both small and large live
window icons matched the embedded original neutral artwork. Modified-client
identification remains in file metadata and notices. Captures: `game-local/public-captures`.

After deleting the three extracted entries and temporary test addon via Recycle
Bin, stock English worked on both, including Steam's normal launch route.
Both stock executables and the 119 original campaign files were unchanged;
profiles, saves, existing personal mods and additional missions were preserved.
No restoration or preparation ran. Finished translations and fonts are unchanged.

Passed: launcher/client builds, 94 client cases / 1,496 assertions, 92 core cases /
371 assertions, three CSV tests, four packaging tests (including stale runtime
and stock-executable rejection), content reconstruction and deployment checks.
Audio remained muted; English voice selection was checked, not audibly assessed.
Multiplayer was not replayed in this presentation-only pass; prior results follow.

## Previous ready-made ZIP acceptance — 2026-10-09

Artifact: `game-local/cwrc-ready/CWRC.zip`, **131,907,425 bytes**.
SHA-256: `527d97204c3d841ffce3176777bc5334adb241372dece74cfa57aa771d3b0500`.
Packaged main: `29c872b2e4e37425b8e486b397e148d5b22ea3f5`.
Client: `9e4e11de9cdcbc6c316593501cd82e9496ce4787` (pinned by main).
The prior ZIP at `game-local/cwrc-zip-rc1/CWRC.zip` remains byte-identical.

The exact archive was extracted into the disposable GOG installation and the
actual Steam installation (app 65790, BuildID 24792092), then launched through
its unchanged CWRC.cmd with isolated test profiles. Both passed:

- Normal SC/TC language-picker selection and English voice selection.
- CWC Combined Arms: Chinese briefing, mission text/subtitles and gameplay;
  live SC/TC/English/French switching with the appropriate fonts.
- Resistance Contact: SC/TC briefing, localized terrain labels and mission start.
- Authored multiplayer Shadow Killer: localized role screen, briefing and local
  hosted gameplay (SC on GOG, TC on Steam).
- Standalone briefing/gameplay: Bomberman on GOG; Resistance War Cry on Steam.
- Another saved mod remained selected and its independent CfgPatches class was
  loaded, not merely listed. GOG's pre-existing personal mod/extra mission remained.
- Normal menu selection, quit and relaunch retained TC on GOG and SC on Steam.
  Both mod directories had exactly the extracted file set: no first-run outputs.

Removing the three CWRC entries and our test addon (recoverably via Recycle Bin)
left both stock games working in English. GOG used its original executable;
Steam was also launched through the normal Steam protocol and its actual stock
Remastered process/window verified. Separate direct stock launches with the same
saved TC/SC test profiles also returned to English without editing those profiles.
Original executables and all 119 formerly
replaced campaign files remained byte-identical. No restoration was needed.
Profiles/saves and unrelated files were not removed. Test captures are under
`game-local/native-captures`, `ready-captures` and `portable-captures`.

Passed: client/native builds; 94 focused client cases / 1,496 assertions;
92 core cases / 371 assertions; three CSV tests in the fontTools environment;
217-table/three-metadata exact reconstruction; all four builders' deployment
checks. Finished translations/master and fonts are unchanged. These are focused
tests and representative playability checks, not full campaign playthroughs or
remote multiplayer qualification. Audio stayed muted; English voice selection
and retained original voice assets were checked, not an audible listening test.

No public release yet. Final corresponding-source/notice review and public
release documentation remain before publication.
