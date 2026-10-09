# CWRC client source

This branch starts at official CWR 3.05 (`ffc61838b7e756bec56aafafbf390396e639ac8f`)
and carries only the CWRC client/build/test changes from historical `87078e2`.
Engine/client and synthetic regression fixtures are preserved exactly; the old
Chinese tables, screenshots and Vulkan branch are not imported.

Chinese patch source and release assembly live on this repository's `main`.
Use its `engine-source.json` to select the client revision. Build `PoseidonGame`,
`PoseidonCoreTests` and `PoseidonTests` using the normal CMake/vcpkg configuration
(Windows x64 RelWithDebInfo, clang-cl/MSVC runtime for the tested configuration).
GL33 is the renderer; this branch has no Vulkan implementation.

This is a new source-history/build identity, not a claim of a byte-identical
historical executable. The earlier tested local RC and its build/source hash
record remain unmodified development evidence, not a rebuilt release artifact.
