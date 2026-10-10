# Build the ready-made ZIP

Use clean tracked checkouts of `main` and the exact `client-source` commit in
`engine-source.json`. Untracked build outputs are allowed. Requirements:
Windows x64, Visual Studio 2022 x64 build tools/SDK, CMake/Ninja, clang-cl,
vcpkg dependencies and Python with fontTools (tested 4.66.1).
Compatible retail Remastered 3.05 data is a read-only build input.

From the repository root, create a separate pinned client checkout:

```powershell
$pin = Get-Content engine-source.json | ConvertFrom-Json
git worktree add --detach build/client-source $pin.commit
```

Configure the client with its CMake/vcpkg setup, using `RelWithDebInfo`,
`CWR_HAS_VULKAN=OFF` (GL33) and build directory `build/local-labels`.
Build targets `PoseidonGame`, `PoseidonCoreTests` and `PoseidonTests`.
Use the matching dependency triplet/toolchain; retain those build inputs for
the source package. Client output is `dist/local-labels`.

In an x64 Visual Studio developer shell, build the static-CRT native launcher,
then assemble into an absent directory outside the installed game:

```powershell
./localization/distribution/build_launcher.ps1 -Output build/launcher -EngineRepo build/client-source
python localization/distribution/build_release.py PATH_TO_NEW_OUTPUT --game PATH_TO_REMASTERED --client build/client-source/dist/local-labels --launcher build/launcher/cwr-chinese.exe --engine-repo build/client-source --vcpkg PATH_TO_VCPKG --installed PATH_TO_INSTALLED_TRIPLET --build-tools PATH_TO_LOCAL_TOOLCHAIN_FILES
```

`--build-tools` contains `clang-local.cmake`, `configure.cmd`, `build.cmd`,
`build_ui_tests.cmd` and `triplets/` from the actual build.
The client uses the system-installed Microsoft Visual C++ runtime; no Microsoft
runtime DLLs or installer are bundled. See [MICROSOFT-RUNTIME.txt](MICROSOFT-RUNTIME.txt).
The launcher uses the client branch's `apps/cwr/Game/localization.ico`;
`make_icon.py` there reproduces the original gold-star icon.

The assembler rejects dirty tracked sources, a mismatched client pin and an
existing output directory. It reconstructs 217 tables / 13,018 SC/TC rows and
169 display-reference/Chinese HTML files from the Chinese-only master and
stock inputs, checking exact hashes, protected syntax and all ten font cmaps.
Existing builders create and verify terrain/UI overlays, 24 standalone and
30 multiplayer missions, and 36 templates. Each individual builder requires
an explicit `--mod-dir`; players never run these tools.

The resulting `cwr-chinese.zip` contains a top-level `Remastered/` directory,
the launcher, ready-made `@cwr-chinese`, matching source, dependency sources,
build inputs and notices. OpenAL remains a replaceable DLL. Packaging rejects
the stock executable and stray development artifacts. The command prints the
ZIP's size and SHA-256.

## Rebuilding from the bundled source

Extract `source/cwr-chinese-source.zip` to get `client-source/` and
`patch-source/`. `source/build-record.json` records both commits; the supplied
`BuildInfo.hpp` records the executable's version. No retail data is needed to
compile the client; it is needed to assemble or run the localization.

Use clang-cl 21, CMake/Ninja and the Windows SDK in an x64 VS 2022 developer
shell. Put LLVM in `source/local-build/llvm/`, as expected by the bundled
`clang-local.cmake`. The included `vcpkg-source.zip` is the build's vcpkg tree
at `2750401336fb7c95f6619657a46a7e798661341c`; use a Git checkout of that revision
in `source/local-build/vcpkg/` so vcpkg can resolve the client's manifest baseline
(`170bd3bfb152a1795b67b5c2190ab7d899fc9971`) and versioned ports. Run its
`bootstrap-vcpkg.bat`, and copy the bundled `source/dependencies/*.tar.gz` into
its `downloads/`. Git history and build tools may require network access.

From the extracted `client-source/`, with `$tools` set to the absolute
`source/local-build/` path and LLVM, CMake and Ninja on `PATH`:

```powershell
cmake -S . -B build/local-labels -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCWR_HAS_VULKAN=OFF "-DCMAKE_TOOLCHAIN_FILE=$tools/vcpkg/scripts/buildsystems/vcpkg.cmake" -DVCPKG_TARGET_TRIPLET=x64-windows-clang-local "-DVCPKG_OVERLAY_TRIPLETS=$tools/triplets" -DVCPKG_OVERLAY_PORTS=cmake/vcpkg-overlay-ports "-DVCPKG_CHAINLOAD_TOOLCHAIN_FILE=$tools/clang-local.cmake"
cmake --build build/local-labels --target PoseidonGame --parallel 6
```

The overlay builds OpenAL Soft 1.24.3 from the supplied archive and three
patches; `OpenAL-CMakeCache.txt` records the original configuration. Dated
comments added to the patches during the notice review are the only differences
from the source used for the bundled DLL. A compatible rebuilt `OpenAL32.dll`
can replace `@cwr-chinese/client/OpenAL32.dll`. The other vcpkg dependencies
retain their source archives, port recipes, installed versions and notices.

Developer checks:

```powershell
python -m unittest discover -s localization -p test_stock_csv.py
python -m unittest discover -s localization/distribution -p "test_*.py"
python localization/distribution/build_content.py PATH_TO_REMASTERED PATH_TO_NEW_CONTENT_OUTPUT
```

Run the native selection/remount, staged-install, add-mod, language/stringtable,
settings/wrapping and radio tests. The MODS regression verifies a failed
activation leaves the previously saved selection available on restart.
Test the actual ZIP with isolated `POSEIDON_USER_DIR`, `POSEIDON_CACHE_DIR`,
`POSEIDON_TEMP_DIR` and `POSEIDON_USER_CONTENT_DIR` directories: SC/TC,
settings, campaign/standalone startup, MODS apply/recovery and preference
persistence. Keep existing profiles, saves, campaign progress and stock files
untouched. Compare generated runtime content with the prior package; source,
notices and rebuilt client metadata may differ.

The root [README](../../README.md) is the player/developer entry point.
Font provenance and reproduction are in [font/NOTICE.md](../font/NOTICE.md)
and [font/ChineseTraditional/NOTICE.md](../font/ChineseTraditional/NOTICE.md).
