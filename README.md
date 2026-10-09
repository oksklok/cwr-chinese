# Chinese translation mod for Cold War Assault Remastered

Free community **简体中文 / 繁體中文（臺灣）** translation for a legitimate
Windows x64 **Cold War Assault Remastered 3.05** installation. Original game
and engine: Bohemia Interactive. Unofficial and noncommercial.

Extract `cwr-chinese.zip` into the game installation folder containing `Remastered/`
(not inside it), run `Remastered/cwr-chinese.exe`,
and play in Simplified Chinese immediately. Choose Traditional Chinese or any
other supported language in Options > Game > Text language; the mod remembers
your choice separately from the stock game's language. Earlier SC/TC choices
are retained when no separate mod preference exists.
Everything is ready to use: no installer, preparation, first-run generation,
game-data scanning, registry changes or stock-file replacements. The launcher
adds `@cwr-chinese` without discarding other selected mods and selects English voices.
Remove it by deleting `@cwr-chinese`, `cwr-chinese.exe` and `README-cwr-chinese.txt`
inside `Remastered`; keep the game folder itself.
Profiles and saves remain managed by the game.
Run the original executable for the normal game. On Windows 10/11 x64, the
included app-local Visual C++ DLLs need no separate runtime installation.

Coverage is unchanged: CWC and Resistance campaigns, 24 standalone missions,
30 authored multiplayer missions, 36 wizard templates, UI/editor/encyclopedia,
terrain labels and generated display names. SC/TC translations and ten fonts
are complete. Original language columns and English/French fallback remain.

## Why a client is still included

Actual unmodified GOG and Steam 3.05 executables were tested with native mod
language registration, UTF-8 tables and existing fonts. UTF-8 Chinese renders,
but the normal picker excludes the two added languages after stock config
restoration. Stock does not select the existing language-specific font sets;
Traditional text shows missing glyphs. Native campaign text overlays leave
stock titles untranslated. The existing focused localization client is retained;
no general filesystem/merger/preparation system is added.

Campaign tables/descriptions reside in `@cwr-chinese/localization/Campaigns`; the client
redirects only those text lookups, preserving stock campaign paths and logic.
Other content uses existing mod loaders. The original executable stays intact.
The window title is simply `Poseidon`, with an original neutral book icon.
Modified-program identification remains in executable metadata and notices.
No trademark icon is bundled or borrowed. CWRC remains an internal codename.

## Development and licenses

[engine-source.json](engine-source.json) pins the
[client-source branch](https://github.com/oksklok/cwr-chinese/tree/client-source).
CWRR and cwr-vulkan remain separate. The Chinese-only master remains
`localization/zhcn-combined-arms/distribution/payload.json` (217 tables /
11,155 rows and eleven display-reference/Chinese HTML recipes). Developers build overlays once;
players receive the finished files. No translation or font revisions are involved.

Bohemia's [official CWR README](https://github.com/BohemiaInteractive/CWR/blob/main/README.md)
designates the retail game data APL-SA. Ready-made translated overlays therefore
ship under [APL-SA](https://old.bohemia.net/community/licenses/arma-public-license-share-alike),
with original material attributed to Bohemia Interactive and adaptations to CWRC
contributors. Code is separately [GPL-3.0-or-later with Section 7 terms](LICENSE);
fonts are OFL-1.1. Matching source, dependency sources and notices accompany the ZIP.

See [build instructions](localization/zhcn-combined-arms/distribution/BUILD.md),
[distribution/acceptance notes](localization/zhcn-combined-arms/DISTRIBUTION.md)
and [ROADMAP.md](ROADMAP.md). This remains local development: no tag, public
release or binary upload. Final source/notice review and public release notes
remain before publication.

The native-launcher distribution passed representative GOG and actual Steam 3.05 checks:
native launch, app-local runtime loading, both campaigns, standalone missions,
language selection/persistence, English/French fallback, another enabled mod,
deletion and stock English launch. Existing multiplayer content is unchanged;
its earlier physical acceptance is recorded in the distribution notes.
This is not a full campaign playthrough or remote multiplayer qualification.
The subsequent first-launch language change passed focused settings tests and
a GOG in-game SC/TC/English persistence check with the stock preference intact.
