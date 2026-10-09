# CWRC Chinese translation mod

Free community **简体中文 / 繁體中文（臺灣）** translation for a legitimate
Windows x64 **Cold War Assault Remastered 3.05** installation. Original game
and engine: Bohemia Interactive. Unofficial and noncommercial.

Extract `CWRC.zip` beside the original `PoseidonGame.exe`, run `CWRC.cmd`,
and select Simplified or Traditional Chinese in Options > Game > Text language.
Everything is ready to use: no installer, preparation, first-run generation,
game-data scanning, registry changes or stock-file replacements. The launcher
adds CWRC without discarding other selected mods and selects English voices.
Remove it by deleting `@CWRC`, `CWRC.cmd` and `README-CWRC.txt`.
Profiles and saves remain managed by the game.

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

Campaign tables/descriptions reside in `@CWRC/localization/Campaigns`; the client
redirects only those text lookups, preserving stock campaign paths and logic.
Other content uses existing mod loaders. The original executable stays intact.
The window keeps the stock engine's Poseidon identity with a modified-client
notice, not a CWRC game brand. No trademark icon is bundled or borrowed.

## Development and licenses

[engine-source.json](engine-source.json) pins the
[client-source branch](https://github.com/oksklok/cwr-chinese/tree/client-source).
CWRR and cwr-vulkan remain separate. The Chinese-only master remains
`localization/zhcn-combined-arms/distribution/payload.json` (217 tables /
11,148 rows and three metadata recipes). Developers build overlays once;
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
