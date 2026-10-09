# Run in an x64 Visual Studio developer shell. No runtime installer is needed.
param(
    [Parameter(Mandatory=$true)][string]$Output,
    [string]$EngineRepo = ''
)
$ErrorActionPreference = 'Stop'
if (!$EngineRepo) { $EngineRepo = "$PSScriptRoot/../../../build/client-source" }
$destination = [IO.Path]::GetFullPath($Output)
$iconDirectory = (Resolve-Path "$EngineRepo/apps/cwr/Game").Path
New-Item -ItemType Directory -Force -Path $destination | Out-Null
& rc.exe /nologo /i $iconDirectory /fo "$destination/launcher.res" "$PSScriptRoot/launcher.rc"
if ($LASTEXITCODE) { throw 'Launcher resources failed' }
& cl.exe /nologo /O2 /W4 /EHsc /std:c++17 /MT /DUNICODE /D_UNICODE `
    "$PSScriptRoot/launcher.cpp" /Fo"$destination/launcher.obj" /Fe"$destination/cwr-chinese.exe" `
    /link /SUBSYSTEM:WINDOWS /MACHINE:X64 "$destination/launcher.res" user32.lib
if ($LASTEXITCODE) { throw 'Launcher build failed' }
