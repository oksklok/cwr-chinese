# Chinese translation for Cold War Assault Remastered

Free, unofficial community **简体中文 / 繁體中文（臺灣）** translation for a
legitimate Windows x64 **Cold War Assault Remastered 3.05** installation.
Original engine and game: Bohemia Interactive.

Extract `cwr-chinese.zip` into the game installation folder containing
`Remastered/`, then run `Remastered/cwr-chinese.exe`. First launch defaults to
Simplified Chinese. Options > Game > Text language selects Traditional Chinese
or a stock language; the mod remembers this separately from the stock language
preference and retains earlier Chinese choices. The launcher adds
`@cwr-chinese` alongside other selected mods and uses English voices.

The ZIP is ready to use on Windows 10/11 x64, including app-local Visual C++
runtime DLLs. No installer or player-side generation is needed. Original game
files, profile/save locations and campaign progression are preserved. To remove
the translation, close the game and delete only `@cwr-chinese`,
`cwr-chinese.exe` and `README-cwr-chinese.txt` inside `Remastered/`.
Run the original executable for the stock game.

Coverage includes both CWC and Resistance campaigns, 24 standalone missions,
30 authored multiplayer missions, 36 wizard templates, UI/editor/encyclopedia,
62 terrain labels and generated display names. The Chinese-only master is
[localization/distribution/payload.json](localization/distribution/payload.json):
217 tables, 13,018 rows and 169 display-reference/Chinese HTML recipes.
Original language columns and fallback remain available.

The pinned localization client supplies Chinese language selection, separate
font sets, text wrapping and display labels. Campaign text is loaded from
`@cwr-chinese/localization/Campaigns` while stock campaign paths and logic remain
intact; other content uses the existing mod loaders. Display names do not rename
script/save/network identities or players. The window title remains `Poseidon`;
modified-program identification appears in metadata and notices. CWRC is an
internal codename. The ten existing OFL fonts are packaged unchanged; see the
[Simplified](localization/font/NOTICE.md) and
[Traditional](localization/font/ChineseTraditional/NOTICE.md) font notices.

For development, use the [build document](localization/distribution/BUILD.md)
and [terminology reference](localization/TERMINOLOGY.md).
[engine-source.json](engine-source.json) pins the matching
[client-source branch](https://github.com/oksklok/cwr-chinese/tree/client-source).
Builders reconstruct ready-made overlays from compatible retail data and verify
their exact content before packaging.

This is preparation for 1.0, with no tagged or published release. The editorial
review is complete. Final corresponding-source, license and notice review is a
separate pre-release step. Remote multiplayer NPC display-name synchronization
is outside this cleanup's scope; a full campaign playthrough is not claimed.

Code is [GPL-3.0-or-later with Section 7 terms](LICENSE). Retail-derived overlays
and Chinese adaptations are APL-SA; original material is attributed to Bohemia
Interactive and adaptations to the translation contributors. Fonts are OFL-1.1.
The ZIP includes matching source, dependency sources and separate notices.
See [component attribution and terms](localization/distribution/COMPONENTS.txt).
