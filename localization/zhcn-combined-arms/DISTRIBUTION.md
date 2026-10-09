# Portable distribution

CWRC is a free community translation mod for Windows x64 Remastered 3.05.
The download is `CWRC.zip`: `@CWRC/`, `CWRC.cmd`, and `README-CWRC.txt`.
First launch prepares derived overlays within `@CWRC`; later launches reuse
them. No installer, registry entries, original-file replacements, backups,
uninstaller or transaction/recovery state are involved.

The campaign resolver checks enabled mods for `localization/Campaigns/...`
tables and descriptions. It leaves mission logic, campaign discovery and
asset paths alone. Original languages are reconstructed without edits.
Other content uses the existing mod loaders. The launcher uses `--add-mod`
to retain selected mods. The game keeps its original window identity and
borrows its installed executable's icon at runtime.

Preparation is necessary for the existing terrain configuration and mission
overlays, which contain commercial source bytes. The ZIP carries Chinese-only
recipes, authored files, fonts, client, preparation utility, source and notices.
Never distribute the prepared folder. Only 582 consumed sources are recorded;
the whole-installation inventory and obsolete installer workflow are removed.

Required source formats/hashes remain those of compatible 3.05 data.
No storefront check is imposed. Original 1.96/1.99 and future updates are
outside scope, as are conflicting third-party edits to required source data.
Microsoft's x64 Visual C++ 2022 runtime is a prerequisite.

## Local ZIP acceptance — 2026-10-09

Artifact: `game-local/cwrc-zip-rc1/CWRC.zip`, **185,210,169 bytes**.
SHA-256: `8e382c4dd78aa1b46eb103a3c4d46af43f3d57260a55bb92985a4d55be1099de`.
Client: `2c7476aef1bdbfa1eae7a1c1a6575aa9d73d95f4`; packaged main: `c83614e`.

The exact ZIP was extracted and launched through `CWRC.cmd` on the disposable
GOG installation and actual Steam installation (app 65790, BuildID 24792092).
Both passed CWC Combined Arms, Resistance Contact and authored multiplayer
Shadow Killer briefing/gameplay checks. Standalone coverage was Bomberman on
GOG and Resistance War Cry on Steam. SC/TC, English/French fallback, English
voice selection and another enabled mod were verified. The GOG options UI
saved Traditional Chinese and retained it across a normal quit/relaunch.
The original window identity and installed-game icon were visually verified.

Deleting the three extracted entries through the Recycle Bin left both stock
English games working; Steam was launched normally through Steam afterward.
All 7,596 recorded Steam files were unchanged. GOG's 119 campaign originals
and remaining baseline files were unchanged; its pre-existing customized
mission overview and unrelated extras were preserved. Test profiles were isolated.

Validation passed: 94 focused client cases / 1,496 assertions; 92 core cases /
371 assertions (including campaign override, missing override and language
switch regression); three CSV tests; exact 217-table/three-metadata reconstruction
and all four builders' deployment checks. Translations/fonts are unchanged.
These were representative playability checks, not campaign playthroughs;
multiplayer was a local host, not a remote-client/network qualification.
Audio stayed muted: English voice selection and original assets were checked.

No public release yet. Before publication: final corresponding-source/license/
notice review and public release documentation.
