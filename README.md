# CWRC Chinese localization

Unofficial **简体中文 / 繁體中文（台灣）** localization for a legitimate Windows x64
GOG Cold War Assault Remastered **3.05** installation. Original game and engine:
Bohemia Interactive. Not affiliated with or endorsed by Bohemia Interactive.

This repository is now the source of truth for the Chinese patch. The engine
continues in [oksklok/CWR](https://github.com/oksklok/CWR), pinned by
[engine-source.json](engine-source.json). CWRR/Vulkan is a separate project.
The old CWR localization directory is retained as development history; do not
edit both copies. No engine history, commercial assets or release binaries are
imported here.

## Status

Simplified and Taiwan Traditional Chinese text, language selection and fonts are
complete. Coverage includes CWC, Resistance, 24 standalone missions, 30 authored
multiplayer missions, 36 wizard templates, shared UI/editor/encyclopedia text,
terrain labels and generated display names. English voices and all eight stock
languages are preserved.

The Windows installer **local RC** passed installation, launch, uninstall,
reinstall, interrupted-install recovery and user-edit preservation checks.
It is not a public release: final corresponding-source/license/notice review,
public documentation and final artifact testing remain. See [ROADMAP.md](ROADMAP.md)
and [distribution findings](localization/zhcn-combined-arms/DISTRIBUTION.md).
No download is published by this repository split.

## Source layout

- `localization/zhcn-combined-arms/distribution/payload.json`: canonical
  Chinese-only master, 217 tables / 11,148 row records, plus stock-reference and
  display-repair recipes. It contains no eight-column stock-language tables.
- The same directory contains the existing restoration core, frozen-helper
  entry point, Inno Setup wrapper and release assembler.
- `font/`, `terrain/`, `wizard/`, `multiplayer/`, `ui/`: ten finished fonts,
  notices, authored configuration and existing local-only overlay builders.
- Existing validators and notes are retained. Full CSVs/configs/PBOs are
  reconstructed locally from the user's verified game, never checked in.
  The retained prototype directory/mod names are deliberate compatibility seams.

## Development

Use the pinned separate engine checkout to build the client. Supply it via
`build_release.py --engine-repo PATH`; the assembler includes matching source
from both repositories. See [build instructions](localization/zhcn-combined-arms/distribution/BUILD.md).
Builders need Python and fontTools; players will not need development tools.

Assemble the unchanged safe payload (choose an absent output):

```powershell
python localization/zhcn-combined-arms/distribution/make_payload.py assemble game-local/payload
```

Reconstruct against a **clean, verified** legitimate GOG 3.05 installation:

```powershell
python localization/zhcn-combined-arms/distribution/install_core.py reconstruct "C:\path\to\Remastered" --payload game-local/payload --output game-local/reconstructed
```

Every reconstructed table and metadata file must match its recorded hash.
Reconstruction does not install or modify the game. Keep generated output ignored.
Never hand-edit stock-language cells or weaken expected hashes to hide differences.
The inherited `make_payload.py export` is a legacy developer operation requiring
the original CWR inventories/full working tables, not the workflow for this
Chinese-only checkout. Authoring changes must be verified through local
reconstruction before updating the master hashes.

Run the existing core/helper tests from `distribution/`, and `test_stock_csv.py`
from the patch directory. For the five full historical validators, reconstruct
locally first, copy the four builder scripts into their corresponding reconstructed
subdirectories, and set these process-scoped variables:

```powershell
$env:CWRC_TRANSLATION_ROOT = (Resolve-Path game-local/reconstructed).Path
$env:CWRC_VALIDATION_REPO = 'C:\Users\KyouKyou\Downloads\CWR'
```

The second variable points only to the existing **local** deployed test game and
original backup inventories. Nothing is copied into Git. Run `validate_campaign.py`,
`validate_resistance.py`, `validate_standalone.py`, `validate_multiplayer.py`, and
`validate_ui.py`; the four deployment checks use `install_core.run_builders` with
the reconstructed root and `check=True`. Without the required local fixtures these
are not fixture-free tests; absence is not a passing result.

## Licensing and attribution

Code: [GPL-3.0-or-later with inherited Section 7 terms](LICENSE).
Chinese game-text adaptations/display recipes: **APL-SA**, original material
by Bohemia Interactive, Chinese translations/adaptations by CWRC contributors.
[APL-SA terms](https://www.bohemia.net/en/licenses/arma-public-license-share-alike)
are separate from the GPL code license. Fonts: **OFL-1.1**, with contributor
notices under both font directories. See
[component declarations](localization/zhcn-combined-arms/distribution/COMPONENTS.txt).
No historical Chinese localization supplies the shipped CWC wording.

The separate client/dependency bundle must include exact matching source and
notices, including replaceable OpenAL and its patched source. An engine Git link
alone is not the binary compliance bundle. Profiles, saves, unrelated mods and
original assets must be preserved during installation/removal.
