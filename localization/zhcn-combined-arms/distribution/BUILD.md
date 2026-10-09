# Build cwr-chinese.zip

Developer requirements: Windows x64, Python with fontTools, compatible retail
Remastered 3.05 data, and the client-source commit pinned by engine-source.json.
Build PoseidonGame and relevant native tests with the branch's CMake/vcpkg setup
(tested: clang-cl, RelWithDebInfo, GL33, CWR_HAS_VULKAN=OFF).

```powershell
# In an x64 Visual Studio 2022 developer shell (static CRT, GUI subsystem):
./localization/zhcn-combined-arms/distribution/build_launcher.ps1 -Output build/launcher
python localization/zhcn-combined-arms/distribution/build_release.py game-local/cwr-chinese-public --game PATH_TO_REMASTERED --client build/client-source/dist/local-labels --launcher build/launcher/cwr-chinese.exe --vc-redist PATH_TO_VC_REDIST_X64_CRT --engine-repo build/client-source --vcpkg PATH_TO_VCPKG --installed PATH_TO_INSTALLED_TRIPLET --build-tools PATH_TO_LOCAL_TOOLCHAIN_FILES
```

`--vc-redist` is Visual Studio's `VC/Redist/MSVC/14.44.35112/x64/Microsoft.VC143.CRT`,
not System32. Only msvcp140.dll, vcruntime140.dll and vcruntime140_1.dll are copied.
PE imports of the client/OpenAL and these DLLs require no further non-OS runtime.
Windows 10/11 supplies UCRT. See MICROSOFT-RUNTIME.txt for redistribution terms.
The client and launcher share the original neutral icon in client-source's
`apps/cwr/Game/localization.ico`; `make_icon.py` reproduces it without external tools.

Choose an absent output directory outside the game. Existing builders construct
and check 217 tables, three metadata edits, campaign text, 24 standalone and
30 multiplayer missions, 36 templates, terrain and UI overlays. Exact output
hashes preserve completed translations and original language columns. The game
is read-only. Retail-derived adaptations ship ready-made under APL-SA; no
Python, fontTools, PyInstaller, preparation executable or source-file checking
runs on the player's machine. There is no preparation marker or first-run path.

The assembler checks the client pin and includes corresponding source,
dependency sources/notices and build inputs, including replaceable OpenAL.
It emits cwr-chinese.zip and prints size/SHA-256. Font files remain unchanged.

For content-only developer checks:

```powershell
python localization/zhcn-combined-arms/distribution/build_content.py PATH_TO_REMASTERED game-local/content-check
python -m unittest discover -s localization/zhcn-combined-arms -p test_stock_csv.py
python -m unittest discover -s localization/zhcn-combined-arms/distribution -p test_build_release.py
```

Run the existing native language/stringtable/mod/wrapping/radio tests. Historical
full localization validators require ignored retail fixtures; absence is not a
passing result. Physically test the actual ZIP on both available storefront
installations using isolated profiles. Do not publish/tag a release yet.

Before ZIP creation, staging rejects the original executable (compared with the
developer's stock build input) and vcruntime*/msvcp* files except the three exact
redistributables in the client directory, compared to the selected REDIST input. These are
developer packaging checks, not player-side installation checks.
