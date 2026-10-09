# Ready-to-use distribution

This is a free community translation mod for Windows 10/11 x64 Remastered 3.05.
`cwr-chinese.zip` contains `@cwr-chinese/`, `cwr-chinese.exe` and `README-cwr-chinese.txt`.
Extract into Remastered and run cwr-chinese.exe, which enables the mod while preserving
other selected mods. Select SC/TC in the game's normal text-language menu.
Delete those three entries to remove it; stock assets/executable, saves and
unrelated mods are untouched. The README uses a distinct name to avoid replacing
a game's existing README.

All content is ready-made: 217 translated tables, three metadata adaptations,
24 standalone banks, 30 multiplayer banks, 36 templates, terrain and UI overlays,
ten unchanged fonts, localization client/OpenAL, source and notices. No player-side
Python, PyInstaller, preparation executable/marker, source inventory validation,
installer, registry, backup or recovery machinery remains.

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

The client redirects only campaign CSV/description lookup, retaining stock
campaign discovery, mission logic and saves. Other mod loading stays native.
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
Both executables use an original neutral book icon, not proprietary artwork.

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
