# CWRC Chinese translation mod

Free community **简体中文 / 繁體中文（臺灣）** translation for a legitimate
Windows x64 **Cold War Assault Remastered 3.05** installation. Original game
and engine: Bohemia Interactive. Unofficial and noncommercial.

CWRC is distributed as a ZIP. Extract beside the original `PoseidonGame.exe`
and run `CWRC.cmd`. On first launch a small preparation utility reads the
required game data and builds local overlays **only inside `@CWRC`**.
Choose ChineseSimplified or ChineseTraditional in Options > Game > Language.
The launcher adds CWRC to the existing mod selection and selects English voices.
Remove CWRC by closing the game and deleting `@CWRC`, `CWRC.cmd` and
`README-CWRC.txt`. Original game files are never replaced.

SC/TC translations and fonts are complete: CWC and Resistance campaigns,
24 standalone missions, 30 authored multiplayer missions, 36 wizard templates,
shared UI/editor/encyclopedia, terrain labels and generated display names.
Original language columns and fallback remain available.

## Implementation

The modified client reads campaign tables and descriptions from enabled mods'
`localization/Campaigns/...` folders. All other campaign paths retain their
existing behavior. The 117 tables and two descriptions are generated inside
CWRC, with no loose-file replacements, backup system or installer.

Preparation reuses the Chinese-only master and existing builders. It checks
582 consumed sources, retaining hashes where reconstruction depends on exact
bytes. It ignores unrelated assets, extra missions and other mods. Generated
commercial overlays must never be redistributed; share the original ZIP only.

The window retains the original game's identity. Its Windows icon is loaded
from the installed executable at runtime; proprietary artwork is not bundled.

## Development

The [client-source branch](https://github.com/oksklok/cwr-chinese/tree/client-source)
contains the modified official 3.05 engine. [engine-source.json](engine-source.json)
pins the required commit. CWRR and cwr-vulkan are separate projects.

The Chinese-only master is
`localization/zhcn-combined-arms/distribution/payload.json`:
217 tables / 11,148 rows, plus three metadata recipes. Completed translations
and ten fonts are unchanged. See [build instructions](localization/zhcn-combined-arms/distribution/BUILD.md),
[distribution notes](localization/zhcn-combined-arms/DISTRIBUTION.md) and
[ROADMAP.md](ROADMAP.md). Installer history remains in Git.

Local ZIP acceptance is in progress; there is no public release yet.
Final source/license/notice review and public release documentation remain.

## Licenses

Code: [GPL-3.0-or-later with inherited Section 7 terms](LICENSE).
Chinese adaptations: [APL-SA](https://www.bohemia.net/en/licenses/arma-public-license-share-alike),
original material by Bohemia Interactive, adaptations by CWRC contributors.
Fonts: OFL-1.1 with contributor notices. These licenses are separate.
The ZIP includes matching source and dependency notices, including source for
the replaceable OpenAL DLL. See [component declarations](localization/zhcn-combined-arms/distribution/COMPONENTS.txt).
