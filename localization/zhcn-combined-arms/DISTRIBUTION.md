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

Local ZIP GOG and Steam acceptance is pending. Historical RC5 installer
results do not qualify the ZIP. No public release is authorized yet.
Before publication: final corresponding-source/license/notice review and
public release documentation.
