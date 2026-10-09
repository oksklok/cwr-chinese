# Local Windows release candidate

Build only on Windows x64. No game assets are release inputs. End users need
neither Python nor development tools; these instructions are for builders.
The patch and engine are now separate repositories. Clone the engine repository
and check out the exact revision in root `engine-source.json`; do not build from
CWRR. Client CMake commands below run in that engine checkout, helper/installer
commands in this patch checkout.

1. Build `PoseidonGame`, `PoseidonCoreTests` and `PoseidonTests` with the repository
   CMake/vcpkg setup. The tested configuration is RelWithDebInfo, clang-cl,
   MSVC v14.44.35207 CRT, static vcpkg dependencies except replaceable OpenAL.
   Keep `CWR_HAS_VULKAN` disabled. The archive includes the actual local triplet,
   chainload toolchain and configure/build commands for reference; replace their
   local compiler paths with your installation. Use the recorded vcpkg revision
   and dependency source hashes, not a moving baseline. No GOG data is needed to
   compile the client. The GOG files are used only for local acceptance testing.
2. In a private Python 3.14 environment, install `PyInstaller==6.22.0` and
   `fonttools==4.66.1`. Freeze the helper:

   ```powershell
   python -m PyInstaller --clean --noconfirm --distpath game-local/cwrc-freeze --workpath game-local/cwrc-freeze-build localization/zhcn-combined-arms/distribution/cwrc-helper.spec
   ```

3. Assemble safe payload/client/helper/source/notices with `build_release.py`.
   Supply `--engine-repo` pointing to the clean pinned engine checkout.
   Supply the built client, frozen helper, vcpkg checkout/installed directory,
   compiler-wrapper directory, Inno Setup directory and downloaded helper source archives. It rejects
   an existing output directory and never reads the commercial game tree.
4. Compile `CWRC.iss` with Inno Setup 6.7.3, supplying absolute `/DPackageDir`
   and `/DOutputDir` paths. Setup installs per-user; choose a writable legitimate
   Remastered folder. The normal Windows uninstaller runs exact restoration
   before removing wrapper components. Conflicts abort cleanup and retain backups.
5. Test THAT installer in a disposable, source-hash-verified GOG 3.05 copy. Audit
   installed package hashes against `package-manifest.json` and reject any PBO,
   stock-language table, original executable, backup or developer artifact.

`source/CWRC-source.zip` contains `client-source/` (the pinned engine) and
`patch-source/` (this repository); run client builds in the former and helper
builds in the latter. The source build record records both revisions and file
hashes. Matching source includes every client/helper build input and the four builders,
but not commercial terrain/mission files or full stock-language localization
tables. Chinese content is provided by `payload/payload.json`; locally reconstruct
the tested tables from a legitimate installation rather than shipping stock text.
Dependency source archives and exact vcpkg port patches are supplied alongside it.
Unused tool/demo resource scripts are included so root CMake configuration works;
their original icons are deliberately absent. Build the three specified client/test
targets, not all unrelated tools. External/commercial test fixtures are not shipped.
OpenAL is dynamically loaded: rebuild the included 1.24.3 source with its included
vcpkg port and three patches, then replace `crwc-client/OpenAL32.dll` for debugging
library modifications. Use `LIBTYPE=SHARED`, bundled fmt disabled, WASAPI/DirectSound
enabled, examples/utilities disabled; the captured OpenAL CMake cache records all
actual flags. No reverse-engineering restriction is imposed for this purpose.

This is not a public-release approval. Independently inspect notices, matching
source/build completeness, neutral branding and the exact artifact before release.
