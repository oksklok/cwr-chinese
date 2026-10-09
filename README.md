# CWRC Chinese localization

Unofficial **简体中文 / 繁體中文（台灣）** localization for a legitimate Windows x64
GOG Cold War Assault Remastered **3.05** installation. Original game and engine:
Bohemia Interactive. Not affiliated with or endorsed by Bohemia Interactive.

This repository is the source of truth for the Chinese patch. Its
[`client-source` branch](https://github.com/oksklok/cwr-chinese/tree/client-source)
contains the required engine/client source, pinned by
[engine-source.json](engine-source.json). It starts at official 3.05 and contains
only CWRC source/test changes. CWRR/Vulkan is a separate repository.
The old CWR localization directory is retained as development history; do not
edit both copies. No engine history, commercial assets or release binaries are
imported into `main`; neither branch depends on the old GitHub fork.

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

Use a checkout of this repository's pinned `client-source` branch to build the client:

```powershell
git worktree add --detach build/client-source db89dd646838e7d2486121151b9266900f072f8d
```

If already present, use that checkout rather than creating another. The worktree
is backed by this repository's `.git`, never the old CWR repository. Supply it via
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
$env:CWRC_VALIDATION_REPO = (Resolve-Path .).Path
```

The second variable points to this checkout's ignored `game-local/Remastered`
test game and `game-local/localization-backup` inventories. Their recorded file
hashes are unchanged; only absolute inventory paths were relocated. Nothing is copied
into Git. Run `validate_campaign.py`,
`validate_resistance.py`, `validate_standalone.py`, `validate_multiplayer.py`, and
`validate_ui.py`; the four deployment checks use `install_core.run_builders` with
the reconstructed root and `check=True`. Without the required local fixtures these
are not fixture-free tests; absence is not a passing result.

Local retained assets: the unchanged historical RC and its SHA-256 record are
under `game-local/cwrc-release-candidate/`; its exact matching source/build record
remains under `game-local/cwrc-rc1-package-release/`. The compiler tools are under
`game-local/.tools/build-tools/`, dependencies under
`build/legacy-cwrc/local-labels/vcpkg_installed/`, and old build/client outputs under
`build/legacy-cwrc/` and `dist/legacy-cwrc/`. These are private ignored assets,
not release inputs unless explicitly selected. Active client builds use
`build/client-source/build/local-labels/`. No old CWR folder is required.
Relocation checks passed: fresh client/core/full-test rebuild, 91 focused native
cases / 1,576 assertions, 25 core/helper and 3 CSV Python tests, all five localization
validators and four overlay checks. Both Chinese main menus rendered from the new
game path; initialization checks exited 0. Menu smoke tests were bounded and
terminated explicitly when the unfocused menu paused its timeout, not recorded as
natural exits. These checks do not constitute a new installer acceptance run.

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
