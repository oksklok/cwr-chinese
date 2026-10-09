# CWRC client source

This branch starts at official CWR 3.05 (`ffc61838b7e756bec56aafafbf390396e639ac8f`)
and carries only the CWRC client/build/test changes from historical `87078e2`.
Engine/client source is preserved exactly; the old
Chinese tables, screenshots and Vulkan branch are not imported.
One inheritance regression now reads the identical authored display addon from
`tests/fixtures/config-replace/display-addon/config.cpp`, rather than expecting
the patch's former localization directory in this engine-only branch. All test
assertions are retained; no commercial config is used as a fixture.

Chinese patch source and release assembly live on this repository's `main`.
Use its `engine-source.json` to select the client revision. Build `PoseidonGame`,
`PoseidonCoreTests` and `PoseidonTests` using the normal CMake/vcpkg configuration
(Windows x64 RelWithDebInfo, clang-cl/MSVC runtime for the tested configuration).
GL33 is the renderer; this branch has no Vulkan implementation.

This is a new source-history/build identity, not a claim of a byte-identical
historical executable. The earlier tested local RC and its build/source hash
record remain unmodified development evidence, not a rebuilt release artifact.

Stock GOG and Steam 3.05 binaries were physically tested with Chinese config,
UTF-8 tables and fonts. UTF-8 rendering works, but Chinese registration is lost
when the stock master config-extra is restored; the normal picker excludes SC/TC.
Stock also ignores per-language fonts and the campaign text-only override path.
The existing focused localization fixes remain necessary; no new loader or
preparation system is added. Ready-made content is built on main, not by players.

The window retains the stock engine's Poseidon identity with a modified-client
notice, not a CWRC game brand. GPL Section 7 forbids branding the modified program
with Bohemia trademarks: startup/version strings are neutral and borrowing the
stock trademark icon has been removed. Game artwork still comes from the installed
game. No replacement artwork or branding subsystem is provided.
