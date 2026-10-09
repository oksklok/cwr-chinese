# Distribution plan and installation core

Local Windows release-candidate installer built and tested; nothing published or tagged.
Target: Windows x64 Remastered 3.05. This practical audit is not a legal opinion.

## Practical installation layout (RC2)

RC2 checks 582 consumed sources rather than the entire 7,596-file GOG inventory.
561 retain exact hashes for table/offset/config reconstruction and the existing
terrain, wizard and MP builders. The other 21 add-ons contribute only referenced
global table rows: their PBO format must parse and all reconstructed table hashes
must match; unrelated members may differ. The original executable must be PE x64
and report 3.05, without a storefront-specific executable hash. Other assets,
extra missions and separately installed mods are ignored. Required-source edits,
unrecognized CWRC output/state, unsafe paths, running target games and insufficient
space still stop installation with an explanation. Original 1.96/1.99 and future
versions are unsupported.
An added base `BIN/config.cpp` conflicts with the required binary config and is
rejected explicitly; modifications in separate mod folders remain selectable.

All 24 standalone missions now use locally reconstructed mod PBOs, including the
Resistance subdirectory. Their original files remain untouched. Authored MP,
Templates/SPTemplates, shared bin overlays and ten Chinese fonts already load
through the mod and retain that route. Campaign translations and two campaign
description edits retain the original loose deployment and exact backup/restore:
`QFBank::ScanPatchFiles` gives existing loose files precedence over campaign banks.
A physical sparse-bank trial still showed English campaign names/subtitles, so
no engine precedence redesign is introduced merely to eliminate these replacements.

The shortcut uses `--add-mod @zhcn-prototype --voice English`. This appends CWRC
to an explicit `--mod` list or the existing `mods.cfg` selection format; the MODS
screen now saves choices and retains actual game-local/managed/workshop paths.
Reinstall does not retain an obsolete absolute copy of the appended mod. Profiles
and saves remain in the game's existing paths. RC2 owns 239 files with 119 original
backups. Same-artifact reinstall is a verified no-op; older/different CWRC requires
normal uninstall first. Legacy receipts remain restorable. Failed/interrupted
installation uses the existing journal/recovery path; later user edits are retained.

An actual installed Steam 3.05 tree (BuildID 24792092) is available. Initial data
checks match GOG; exact RC2 installer and runtime acceptance are in progress.
The RC1 sections below are retained historical evidence, not RC2 acceptance.

## Dedicated patch repository

Patch development now lives in `oksklok/cwr-chinese`. Its Chinese-only master,
ten unchanged fonts, authored recipes, builders, installer/core and notes were
split from CWR commit `87078e2`; no commercial files, full stock-language tables,
client binaries or engine history were imported into main. Required client source
now lives on this repository's `client-source` branch, official 3.05 plus only
CWRC source/test changes, pinned in root `engine-source.json`; the old GitHub fork
is no longer a source dependency. `build_release.py --engine-repo` includes
matching client and patch sources in distinct source-archive roots.

The local RC reported below predates the split and is retained under this
checkout's ignored `game-local/cwrc-release-candidate/`, with its SHA-256 record.
Its matching source/build record and test installations moved alongside it;
the installer and build-record bytes are unchanged. It was not rebuilt, uploaded
or re-labelled as a new tested artifact. Build tools/dependencies and validation
backups are now local to this checkout; the old CWR folder is not required.
The split was checked by exact payload/font comparison, complete local table/
metadata reconstruction, existing validators/deployment checks and core/helper
regressions. Physical RC acceptance below is prior evidence, not a new game run.

Client-history separation: the `client-source` branch starts at official 3.05 and
preserves the tested runtime/client/build source exactly. The only follow-up is
a test-fixture path change plus a byte-identical copy of the authored UI addon
under test fixtures, so regressions no longer require the old localization tree.
The rebuilt client/core/full-test targets pass, including 91 focused cases /
1,576 assertions (language/display/identity/radio/font/wrapping, CSV and MP paths).
The source assembler checks the fixture against the canonical authored addon and
includes both branches' matching source. The new executable is **not** byte-identical
to the old RC; new Git/build identity and paths are recorded, not substituted into
the historical RC. Original source/RC records and local development assets stay intact.

## What can be shipped

| Material | Finding and proposed treatment |
| --- | --- |
| Fresh SC/TC translations | Authored by this project, but translations of copyrighted game text are adaptations, not automatically independent GPL works. Publisher documentation places game data under APL-SA. Use an explicit APL-SA content declaration, attribution and modification notice before release. |
| Original scripts/builders and code-like configuration/metadata | Repository GPL-3.0-or-later plus Section 7 terms apply to project source, except separately licensed components. Classify stock-derived text/config fragments as game-data adaptations rather than treating everything as GPL. |
| Rebuilt client | Binary redistribution is expressly permitted, conditionally. The local RC uses neutral CWRC program identity and includes matching source/build scripts, dependency sources/patches, GPL plus additional terms, modification notices and disclaimers. Final public source/notice review remains a release gate. |
| Ten hybrid SC/TC fonts | OFL 1.1 permits modified-font redistribution. Keep OFL, all contributor notices and renamed families; do not use reserved font names, claim endorsement, or sell fonts alone. See both font notices. |
| Dependencies | Audit the actual linked/bundled versions, not just the manifest. Permissive components need their notices; OpenAL needs LGPL compliance and matching patched source. Microsoft runtimes have separate redistribution terms. |
| Commercial-derived banks/configs and original GOG files | Exclude from the download. Generate overlays locally from verified user-owned inputs; never package our test installation, original executable, mission/audio/terrain payloads or backups. |

The publisher's [source README](https://github.com/BohemiaInteractive/CWR/blob/main/README.md)
and [game page](https://store.steampowered.com/app/65790/) distinguish GPL code from
APL-SA assets. [APL-SA](https://www.bohemia.net/en/licenses/arma-public-license-share-alike)
permits adaptation/sharing with attribution, noncommercial/game-use restrictions
and share-alike; translation is explicitly adaptation. Although not a blanket ban
on asset redistribution, our release policy remains **translation-only payloads
and locally generated commercial-derived overlays**. Local generation does not
exempt distributed translations from those obligations. No historical Chinese
translation wording is a shipped source.
Keep these as separately licensed code/data/font components; do not impose the
content's noncommercial restriction on the GPL client or patcher.

## Binary and dependency gates

[LICENSE](../../LICENSE) and the [upstream license](https://github.com/BohemiaInteractive/CWR/blob/main/LICENSE)
provide a binary grant; compliance, not public source availability, is the gate.
`VersionNo.h` and `apps/cwr/Game/version.rc2` now identify the modified client as
CWRC, with Bohemia attribution and an unofficial-modification notice. Its original
game icon resource was removed (neutral Windows application icon); SDL window
title and startup error/warning titles use CWRC. Internal CWR protocol/profile
identifiers stay unchanged. Stock in-game textures/logos remain the user's original
commercial content, not compiled/bundled branding; this does not rebrand game assets.

Inspected the current link rule, PE imports, local triplet and installed notices:
most dependencies are static; `OpenAL32.dll` is loaded separately. Alongside
SDL3/enkiTS (zlib), include version-exact notices for MIT/BSD/curl components:
spdlog/fmt, cJSON, zstd, curl, Opus, Vorbis/Ogg, CLI11, mimalloc and ImGui.
FreeType requires its chosen license and credit; also include its transitive
libpng, zlib, bzip2 and Brotli notices and vendored glad/Khronos/RenderDoc notices
where incorporated. The root third-party summary is not the complete version-exact
binary notice bundle: the link contains additional transitive libraries.
Exclude PDBs, tests, PBO plugin and development tools from the package.

Ship a replaceable, isolated OpenAL DLL with its actual LGPL/auxiliary notices
and exact 1.24.3 source plus the applied vcpkg overlay patches. Publish the matching
client/patcher source archive and build configuration beside the download;
a moving branch or upstream-only link is insufficient. Exclude commercial
data/screenshots from that archive.

PE imports require the Microsoft v14 C++ runtime. Prefer detecting the existing
runtime and offering Microsoft's official prerequisite installer if missing;
[redistribution eligibility](https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files?view=msvc-170)
must be checked before bundling it. Do not copy Windows/system DLLs or GOG's runtime
files into the patch. The local `game-local/EULA.txt` covers Microsoft/Inno
components, not a separate grant over Bohemia game assets.

## Simplest installation approach

Use an [Inno Setup](https://jrsoftware.org/files/is/license.txt) Windows installer
with a small frozen helper reusing the existing builders. Bundle Python privately
via [PyInstaller](https://pyinstaller.org/en/stable/license.html); users install no
Python or development tools. Include [Python runtime notices](https://docs.python.org/3/license.html)
and fontTools MIT/external notices for existing glyph checks. Exclude OpenCC,
source fonts and font rebuilding tools. Audit the exact frozen dependencies.

Download contents: rebuilt neutral client and required isolated dependencies;
ten final OFL fonts; **key + ChineseSimplified + ChineseTraditional** translation
payloads; original display-reference/config additions and supported-input hashes;
installer/helper and notices. Do not blindly ship current full CSVs or copied
`description.ext` files: they contain stock text/configuration. Reconstruct all
eight stock columns/order/extras from the user's tables, append Chinese values
and apply only the established reference/nameKey repairs locally. Chinese-only
payloads must retain sufficient identifiers/reference recipes to reproduce the
current tested tables, including campaign-root and canonical-only metadata.

1. Locate the existing Remastered directory; close the game. Preflight every
   affected input/hash, permissions, space and conflicting patch output before
   writing. Initially accept only verified clean 3.05 or a receipt-recognized
   installation of this patch, not an arbitrary modified game.
2. Back up each replaced loose CSV/config file byte-for-byte outside the mod,
   recording original existence/hash. Reconstruct and stage tables plus existing
   terrain/wizard/MP/UI overlays locally. Stock PBOs, base fonts and GOG executable
   stay untouched. Use the existing loose campaign/standalone deployment path;
   do not introduce an untested campaign-overlay design.
3. Keep the rebuilt executable/OpenAL in a patch-owned client directory; shortcut
   uses the legitimate game directory as working directory and explicit mod path.
   Preserve profiles/saves and English voices. Verify staging/deployment before
   committing changes; roll back interrupted/failed installations from backups.
4. Uninstall removes only receipt-owned files whose installed hashes still match,
   restores exact backed-up bytes and removes originally absent additions.
   Preserve later user edits, profiles/saves and unrecognized files; report any
   restore conflict instead of overwriting. Never recursively delete a game root.
   Reinstall/upgrades use the same original backup, not translated files as stock.

## Implemented developer installation core

`distribution/payload.json` contains 217 table recipes / 11,148 ordered row
records: keys, unchanged SC/TC cells, stock-reference recipes and supported-input
hashes, **not the eight stock-language values**. This includes canonical-only
metadata and the retained prototype mirror. Three loose display-config edits are
reference-only byte-range instructions, not copied commercial configuration.
The assembly command copies the ten existing finished fonts, their OFL/notices,
authored language/UI configuration and compact builder recipes; no executable,
commercial mission/config, PBO or original game asset enters the payload.
Component declarations are separate: GPL code (including repository Section 7
terms), APL-SA Chinese adaptations with Bohemia attribution/modification notice,
and OFL fonts. The full public source/license/dependency notice bundle is still a
release gate, not replaced by these manifest declarations.

Run from the repository root with the existing Python/fontTools environment:

```powershell
python localization/zhcn-combined-arms/distribution/make_payload.py assemble game-local/distribution-payload
python localization/zhcn-combined-arms/distribution/install_core.py install "C:\Games\CWA\Remastered" --payload game-local/distribution-payload --local-client dist/local-labels
python localization/zhcn-combined-arms/distribution/install_core.py uninstall "C:\Games\CWA\Remastered"
```

`--local-client` is a private, already rebuilt client/OpenAL input; neither is
bundled in the safe payload. The helper stages on the same volume using hardlinks,
reuses the existing stock CSV reader and all four builders, and checks generated
bytes before deployment. It verifies 7,596 stock hashes, rejects extra stock-tree
inputs/conflicting files/reparse paths, checks conservative free space/write
access and refuses a running target game. Separate unrelated mods/profiles/saves
are left alone. `.crwc-install/receipt.json` records installed/original hashes and
original absence; 144 replaced loose files have byte-exact backups. The client
lives in `crwc-client`, never replaces GOG's executable, and must be launched with
the game directory as working directory plus its explicit `@zhcn-prototype` mod.

Same-payload reinstall is a checked no-op retaining the original backups; a
different payload/client requires uninstall first (no upgrade system). Uninstall
preserves later edits/deletions and retains their receipt/backups, returning 2
for restoration conflicts. Resolve a conflict deliberately before retrying;
never silently overwrite it. `recover GAME` uses the pending write journal after
an interrupted install. Backup preparation publishes the complete state directory
atomically; retirement keeps its journal until bounded cleanup finishes and can
resume through install, recover or uninstall. Complete restoration temp files
are recognized by either recorded original or installed hash. Unknown/corrupt
state or an unrecognized partial temp
file stops recovery for inspection rather than being deleted. Do not delete
backups to bypass these checks. Interruptions after commit preserve the installed
receipt/backups for recognized reinstall or exact uninstall, rather than retiring them.

Acceptance used only `game-local/install-core-test/Remastered`, a separate copy
restored against independent original inventories/reversal hashes; the development
installation was not an acceptance target. All 217 reconstructed tables and three
metadata files match known-good bytes. All four overlay outputs and both font/
language registrations match; 234 localization files match the development
deployment, with four additional installed OFL/attribution files. Two private
runtime files bring the receipt to 240 managed files. Fresh install, identical
reinstall, exact 7,596-file/hash restoration, deliberate mission-CSV edit
preservation and rollback failure injection pass. Both Chinese selections persist
after restart; actual Combined Arms briefings (SC/TC/English/French), Bomberman
briefing/markers and gameplay, no-mod English menu and Chinese multiplayer selector
were inspected at 1280x900. Restart/no-mod/selector captures used the existing
game framebuffer capture while leaving a Windows firewall prompt untouched.

After the firewall prompt was cleared, a fresh install through the current helper
was checked with authored `1-4_C_ShadowKiller.Abel`: local-host selector, lobby/role
assignment, assembled briefing/objectives/notes, live TC/SC/English/French switching,
mission start, HUD, natural mission radio and bounded keyboard movement. The
in-mission fuel-station link passed the real HTML hit-test/click route. No-mod
English separately passed selector, lobby, briefing and gameplay with stock radio.
234 localization files still match the known-good deployment exactly; checked
reinstall and exact uninstallation/restoration were repeated. No second client,
online match, complete mission or multiplayer ending is claimed.

**Radio live-switch fix:** `SentenceParams::AddAzimutRelDir` and `AddDistance`
in `engine/Poseidon/AI/AIRadio.cpp` now resolve the selected registered string ID
when generating a message, rather than caching translated strings for the process
lifetime. Speech tokens, direction calculations and distance bins are unchanged.
The focused regression failed before the fix and now covers every clock direction,
distance bin and boundary across TC/SC/English/French and back (1,039 assertions).
The rebuilt private client was freshly installed through the current helper;
its deployed hash matches the build. Shadow Killer lobby/briefing/gameplay and
fresh generated movement/watch radio were checked at 1280x900 while switching
TC → SC → English → French → English → TC → SC. New clock words follow the
selected language and render correctly; English voice selection remains unchanged.
No-mod English lobby/briefing/gameplay and generated radio were checked separately.

Existing chat history is a snapshot, not retranslated by this fix. Old TC messages
can temporarily show unsupported regional glyphs under SC/stock fonts until they
fade; freshly generated messages do not. Distance-bin switching is exhaustively
covered by the regression; natural French target reporting was also observed,
but no claim is made of a physical test of every distance or the `far` word.
Five localization validators, four builder generation/deployment checks,
21 installation-core regressions and three stock-CSV tests pass. Client/core/full
test targets build; 86 focused engine cases / 1,549 assertions pass. Exact
7,596-file/hash restoration was verified again after testing. External-data suite
limits are unchanged. Only the two radio text-resolution paths changed in the
engine; translations, fonts, mission logic/audio, original commercial assets,
the development installation and inherited Return to Eden content remain untouched.
Core runtime acceptance is complete within these bounds. Windows-wrapper and
exact local RC acceptance are recorded below; public-release review remains pending.

## Decisions before public packaging / release

- Independently review the final matching source/build and dependency-license bundle
  before public release. No general binary copyright prohibition was found; do not
  substitute an upstream-only source link or ship commercial-derived overlays.
- Finalize public README/credits/known limitations, including the retained stock
  Return to Eden defect and cached old-language chat glyph limitation. The RC is
  unsigned; no clean-machine/minimum-runtime or SmartScreen reputation claim is made.
- Dedicated public repository, tag, public release artifact and its final recheck
  remain separate tasks. No publication, tag or installer upload was performed.

## Windows local RC acceptance

`distribution/CWRC.iss` wraps `windows_helper.py`/the existing installation core.
Inno owns only per-user wrapper components and shortcuts; the helper owns every
game-file operation. Its restoration runs before Windows uninstall cleanup and
any conflict aborts that cleanup. A selected existing Remastered folder is verified
against all original hashes. Microsoft v14 x64 runtime 14.44.35207 or newer is
checked, with Microsoft's official prerequisite URL; runtime DLLs are not bundled.

Local artifact: `game-local/cwrc-release-candidate/CWRC-3.05-rc1-setup.exe`,
178,577,174 bytes, SHA-256
`121559976420da1a1eebcd2af3bf19538058ac90aa6aa97333f7e0db2cbcd894`.
The exact installer was tested against the separate verified clean
`game-local/install-core-test/Remastered`, not the development installation.

The extracted package contains 197 inventoried files (226,147,350 bytes), plus
its manifest: rebuilt client/OpenAL, private frozen helper, 217 Chinese-only table
recipes/11,148 row records, ten unchanged fonts, authored display/config recipes,
licenses/notices and matching source/build inputs. No stock-language table, original
executable, commercial PBO/mission/terrain/audio asset, backup, PDB, test executable
or development installation is included. Installed extraction hashes match the
inventory; compiled repository translation units and configure-time resource scripts
are present in the source archive, excluding original commercial icons/fixtures.

Actual dependencies/notices include OpenAL Soft 1.24.3 (replaceable LGPL DLL, source
and all three applied port patches), SDL 3.4.10, fmt 12.1.0, spdlog 1.15.1,
curl 8.20.0 and the actual installed transitive notices/SPDX records. The frozen
helper uses Python 3.14.6, PyInstaller 6.22.0 and fontTools 4.66.1; matching Python,
OpenSSL 3.5.7, libffi 3.4.4 and helper dependency sources/notices are included.
Inno Setup 6.7.3 attribution/license is retained. GPL code, APL-SA Chinese adaptations
and OFL fonts are declared separately. See `distribution/BUILD.md` and the installed
component notices/build record for exact inputs, versions, hashes and rebuild steps.

The corrected core space bound is about 291 MiB for actual reconstructed/staged
outputs, backups, runtime, one replacement temporary and filesystem slack. It no
longer counts hardlinked untouched stock assets as copies. The wrapper accounts
for its additional approximately 216 MiB on the game volume when shared; Inno
temporarily extracts another approximately 216 MiB. Allow about 0.75 GiB free
before launch on this single-volume layout, excluding the already downloaded EXE.

Acceptance results:

- Ordinary wizard fresh install and normal Windows uninstall passed. All 217
  tables, three metadata edits, four overlays and both font/language registrations
  reconstruct exactly; 240 receipt-owned outputs match. Original GOG executable
  and banks stay untouched. The initial early `{app}` expansion bug was fixed by
  placing game selection after directory initialization; the final wizard passed.
- The installed Start-menu shortcut launches the packaged CWRC client with the
  correct game working directory/mod and English voice selection. SC and TC were
  selected through settings and persisted over restarts. Combined Arms briefing/
  objectives/identity, Contact's Nogova map/briefing, Bomberman's map/objectives and
  Shadow Killer local-host selector/lobby/briefing/gameplay/radio passed. Contact
  and Bomberman used the existing isolated test-mission route after shortcut launch;
  Shadow Killer used normal host/menu navigation. English/French switching retained
  stock text; the fuel-station link passed the real briefing hit-test/click route.
- Recognized reinstall leaves the original receipt/backups unchanged. A running
  game causes a clear failed install without disturbing the installed state.
- A deliberately edited Bomberman CSV is preserved; uninstall returns failure
  before removing any wrapper component and retains all 144 backups/receipt. After
  resolving that test-only edit from its original backup, retry restores exactly.
- Setup was forcibly stopped after receipt commit/pending-journal removal, before
  its wrapper INI existed. All 240 outputs and original backups survived. Rerunning
  the same installer recognized the receipt, finished wrapper installation without
  replacing backups, and subsequently uninstalled normally.
- Exact original 7,596-file/hash inventories were verified after removal, including
  after interruption/retry. Wrapper directory, Windows uninstall registration and
  shortcuts are removed; separate test profiles/saves remain untouched by removal.
  The byte-original GOG executable was then launched without the patch and its
  stock English menu/fonts inspected physically.
- Five localization validators, four overlay deployment checks, 25 installer/helper
  regressions, three optimized stock-CSV tests, client/core/full-test builds and
  86 focused engine cases / 1,549 assertions pass. Broad external-fixture test-suite
  limits are unchanged. No second client, online match, mission ending or exhaustive
  gameplay acceptance is claimed.

Font attribution includes Adobe/Noto, LXGW/Klee, Iansui, Oswald, Roboto,
Courier Prime/Quote-Unquote Apps, Vollkorn and Caveat; copy
[SC/Latin notices](font/NOTICE.md), [TC notices](font/ChineseTraditional/NOTICE.md)
and [OFL](font/OFL.txt) with the package. Credit Bohemia's original work, identify
our translations/client modifications, and retain warranty/non-endorsement notices.
Installer/helper and final dependency notices must accompany the installed package.
