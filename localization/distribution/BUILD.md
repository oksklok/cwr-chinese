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
python localization/distribution/build_release.py PATH_TO_NEW_OUTPUT --game PATH_TO_REMASTERED --client build/client-source/dist/local-labels --launcher build/launcher/cwr-chinese.exe --vc-redist PATH_TO_VC_REDIST_X64_CRT --engine-repo build/client-source --vcpkg PATH_TO_VCPKG --installed PATH_TO_INSTALLED_TRIPLET --build-tools PATH_TO_LOCAL_TOOLCHAIN_FILES
```

`--build-tools` contains `clang-local.cmake`, `configure.cmd`, `build.cmd`,
`build_ui_tests.cmd` and `triplets/` from the actual build.
`--vc-redist` is Visual Studio's
`VC/Redist/MSVC/14.44.35112/x64/Microsoft.VC143.CRT`, not System32.
Only msvcp140.dll, vcruntime140.dll and vcruntime140_1.dll are bundled.
Windows 10/11 supplies UCRT; see [MICROSOFT-RUNTIME.txt](MICROSOFT-RUNTIME.txt).
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
the stock executable, stray development artifacts and unapproved/stale Microsoft
runtime DLLs. The command prints the ZIP's size and SHA-256.

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
Final corresponding-source/license/notice review is a separate pre-release
step. Do not tag or publish as part of this cleanup.
