"""Build cwr-chinese.zip with ready-made mod content and the localization client."""
import argparse
import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from build_content import PATCH, require, digest, build_content
REPO = PATCH.parents[1]
MSVC_RUNTIME = ('msvcp140.dll', 'vcruntime140.dll', 'vcruntime140_1.dll')


def copy(source, dest):
    require(source.is_file(), f'Missing release input: {source}')
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)


def source_archive(output, engine):
    # Explicit source-only selection; retail-derived APL-SA content is packaged
    # separately from GPL code, not mixed into the corresponding-source archive.
    selected = {}
    roots = {'engine', 'apps', 'cmake', 'thirdparty', 'tests', 'scripts', 'tools', 'mserver', 'deploy', 'resources'}
    extensions = {'.c', '.cpp', '.cc', '.h', '.hpp', '.inc', '.in', '.cmake', '.txt', '.md', '.json',
                  '.rc', '.rc2', '.py', '.spec', '.iss', '.ps1', '.cmd', '.bat', '.sh', '.rs',
                  '.toml', '.lock', '.glsl', '.vert', '.frag', '.def', '.natvis', '.tpp', '.yml', '.yaml',
                  '.diff', '.patch', '.inf'}
    for base, prefix in ((engine, 'client-source'), (REPO, 'patch-source')):
        paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=base).decode().split('\0')
        for rel in sorted(set(paths)):
            p = base / rel
            if not p.is_file():
                continue
            parts = Path(rel).parts
            if base == engine:
                if len(parts) == 1:
                    if p.name not in ('LICENSE', 'CMakeLists.txt', 'CMakePresets.json', 'vcpkg.json', 'README.md', 'THIRD_PARTY_NOTICES.md'):
                        continue
                elif parts[0] not in roots or (p.suffix not in extensions and rel != 'apps/cwr/Game/localization.ico'):
                    continue  # Old engine localization is historical, not the patch source.
            else:
                if len(parts) == 1:
                    if p.name not in ('LICENSE', 'README.md', 'engine-source.json', '.gitattributes', '.gitignore'):
                        continue
                elif parts[0] != 'localization' or p.suffix not in extensions | {'.csv'}:
                    continue
                if p.suffix == '.csv' and rel != 'localization/zhcn-combined-arms/mod/bin/stringtable.csv':
                    raise ValueError(f'Stock language table in patch source: {rel}')
            selected[prefix + '/' + rel] = p
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel, p in selected.items():
            z.write(p, rel)
    return {rel: digest(p.read_bytes()) for rel, p in selected.items()}


def package_zip(files, output, stock_executable, vc_redist):
    # Check the complete staging tree before creating an archive. APL-SA game
    # data and the three selected Microsoft redistributables are permitted.
    entries = sorted(file for file in files.rglob('*') if file.is_file())
    stock_hash = digest(stock_executable.read_bytes())
    runtime_hashes = {f'@cwr-chinese/client/{name}': digest((vc_redist / name).read_bytes())
                      for name in MSVC_RUNTIME}
    forbidden = {'.pdb', '.log', '.ico', '.py', '.pyc', '.spec'}
    for file in entries:
        relative = file.relative_to(files).as_posix()
        if file.name.lower().startswith(('vcruntime', 'msvcp')):
            require(relative in runtime_hashes and digest(file.read_bytes()) == runtime_hashes[relative],
                    f'Unexpected or stale Microsoft runtime: {relative}')
        require(file.suffix.lower() not in forbidden or relative.startswith('@cwr-chinese/source/'),
                f'Unexpected runtime artifact: {relative}')
        if file.suffix.lower() == '.exe':
            require(relative in ('@cwr-chinese/client/PoseidonGame.exe', 'cwr-chinese.exe'),
                    f'Unexpected executable: {relative}')
            require(digest(file.read_bytes()) != stock_hash, f'Original game executable leaked: {relative}')
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in entries:
            archive.write(file, file.relative_to(files).as_posix())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    for name in ('game', 'client', 'launcher', 'vc-redist', 'vcpkg', 'installed', 'build-tools'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--engine-repo', type=Path, default=REPO / 'build/client-source')
    args = parser.parse_args()
    engine = args.engine_repo.resolve()
    pin = json.loads((REPO / 'engine-source.json').read_text(encoding='utf-8'))
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=engine).decode().strip()
    require(commit == pin['commit'], 'Client source differs from engine-source.json')
    require(not subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=engine).strip(),
            'Commit the client before packaging')
    release = args.output.resolve()
    require(not release.exists(), 'Choose an absent output directory')
    out = release / 'files/@cwr-chinese'
    build_content(args.game, out)
    for name in ('PoseidonGame.exe', 'OpenAL32.dll'):
        copy(args.client / name, out / 'client' / name)
    for name in MSVC_RUNTIME:
        copy(args.vc_redist / name, out / 'client' / name)
    copy(args.launcher, release / 'files/cwr-chinese.exe')
    copy(Path(__file__).with_name('README-cwr-chinese.txt'), release / 'files/README-cwr-chinese.txt')
    copy(Path(__file__).with_name('MICROSOFT-RUNTIME.txt'), out / 'notices/MICROSOFT-RUNTIME.txt')
    copy(REPO / 'LICENSE', out / 'notices/GPL.txt')
    copy(engine / 'THIRD_PARTY_NOTICES.md', out / 'notices/VENDORED.md')
    copy(Path(__file__).with_name('COMPONENTS.txt'), out / 'notices/COMPONENTS.txt')
    copy(Path(__file__).with_name('BUILD.md'), out / 'source/BUILD.md')
    copy(PATCH / 'font/OFL.txt', out / 'notices/OFL.txt')
    for directory in args.installed.joinpath('share').iterdir():
        if (directory / 'copyright').is_file():
            copy(directory / 'copyright', out / 'notices/third-party' / (directory.name + '.txt'))
        for name in ('vcpkg.spdx.json', 'vcpkg-spdx-resources.json'):
            if (directory / name).is_file():
                copy(directory / name, out / 'source/dependencies' / directory.name / name)
    # Actual dependency sources cached by the build, including OpenAL 1.24.3.
    # No tools/binaries from vcpkg/downloads enter the payload.
    downloads = args.vcpkg / 'downloads'
    for file in sorted(downloads.glob('*.tar.gz')):
        copy(file, out / 'source/dependencies' / file.name)
    shutil.copytree(engine / 'cmake/vcpkg-overlay-ports', out / 'source/vcpkg-overlay-ports')
    subprocess.run(['git', '-C', str(args.vcpkg), 'archive', '--format=zip',
                    '--output=' + str(out / 'source/vcpkg-source.zip'), 'HEAD'], check=True)
    copy(args.installed.parent / 'vcpkg/status', out / 'source/vcpkg-status.txt')
    copy(engine / 'build/local-labels/generated/Poseidon/Core/BuildInfo.hpp', out / 'source/BuildInfo.hpp')
    for name in ('clang-local.cmake', 'configure.cmd', 'build.cmd', 'build_ui_tests.cmd'):
        copy(args.build_tools / name, out / 'source/local-build' / name)
    shutil.copytree(args.build_tools / 'triplets', out / 'source/local-build/triplets')
    cache = args.vcpkg / 'buildtrees/openal-soft/x64-windows-clang-local-rel/CMakeCache.txt'
    copy(cache, out / 'source/OpenAL-CMakeCache.txt')

    source_archive(out / 'source/cwr-chinese-source.zip', engine)
    record = {'client_commit': commit,
              'patch_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip()}
    (out / 'source/build-record.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    archive = release / 'cwr-chinese.zip'
    package_zip(release / 'files', archive, args.game / 'PoseidonGame.exe', args.vc_redist)
    print(f'{archive}: {archive.stat().st_size} bytes; SHA-256 {digest(archive.read_bytes())}')


if __name__ == '__main__':
    main()
