# Build the portable CWRC ZIP

Use Windows x64 and the client-source commit pinned by `engine-source.json`.
Build PoseidonGame and relevant native tests using that branch's CMake setup.
The local build uses clang-cl, RelWithDebInfo, GL33, and
`CWR_HAS_VULKAN=OFF`. Source/dependency build inputs accompany the ZIP.

Preparation uses Python 3.14, fontTools and PyInstaller. Inno Setup is no
longer used. From the repository root, with the build environment active:

```powershell
python -m PyInstaller --noconfirm --distpath game-local/portable-freeze --workpath game-local/portable-freeze-build localization/zhcn-combined-arms/distribution/cwrc-prepare.spec
python localization/zhcn-combined-arms/distribution/build_release.py game-local/portable-release --client build/client-source/dist/local-labels --preparation game-local/portable-freeze/cwrc-prepare --engine-repo build/client-source --vcpkg PATH_TO_VCPKG --installed PATH_TO_VCPKG_INSTALLED_TRIPLET --build-tools PATH_TO_LOCAL_TOOLCHAIN_FILES --helper-sources PATH_TO_PYTHON_DEPENDENCY_SOURCE_ARCHIVES
```

Choose an absent release directory. The assembler includes source, licenses
and build inputs, checks the client pin, and excludes commercial game assets.
It emits `CWRC.zip` and prints its size and SHA-256.

For development reconstruction only:

```powershell
python localization/zhcn-combined-arms/distribution/make_payload.py PATH_TO_GAME/@CWRC/payload
python localization/zhcn-combined-arms/distribution/prepare.py PATH_TO_GAME
```

Preparation reuses exact table/metadata recipes and four existing builders,
including their deployment checks. It writes only inside `@CWRC`.
Delete `@CWRC/prepared.txt` to run preparation again on next launch.
No original-file restoration is needed.

Run `test_stock_csv.py` and native stringtable, language, mods, wrapping and
radio tests. The historical full localization validators additionally need
their ignored commercial fixtures; their absence is not a passing result.
Do not distribute reconstructed CSVs, campaigns, configs or mission PBOs.
