# Ready-to-use distribution

CWRC is a free community translation mod for Windows x64 Remastered 3.05.
`CWRC.zip` contains `@CWRC/`, `CWRC.cmd` and `README-CWRC.txt`.
Extract into Remastered and run CWRC.cmd, which enables the mod while preserving
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
It retains the stock engine's Poseidon window identity with a modified notice.
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
and future updates are outside scope. Microsoft x64 VC++ 2022 runtime is required.

## Acceptance

The prior working preparation-based ZIP remains preserved at
`game-local/cwrc-zip-rc1/CWRC.zip`. Replacement ZIP physical acceptance is pending
the ready-content build; its result will be recorded here before task completion.

No public release yet. Final corresponding-source/notice review and public
release documentation remain before publication.
