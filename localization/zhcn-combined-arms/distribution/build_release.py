"""Build CWRC.zip from the client, preparation tool and Chinese-only master."""
import argparse
import importlib.metadata
import json
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from make_payload import assemble
from prepare import PATCH, require, digest
REPO = PATCH.parents[1]


def copy(source, dest):
    require(source.is_file(), f'Missing release input: {source}')
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)


def source_archive(output, engine):
    # Explicit source-only selection; never include game-local, assets, packages,
    # stock-language localization CSVs, original icons or generated commercial banks.
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
                elif parts[0] not in roots or p.suffix not in extensions:
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    for name in ('client', 'preparation', 'vcpkg', 'installed', 'build-tools', 'helper-sources'):
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
    out = release / 'files/@CWRC'
    assemble(out / 'payload')
    for name in ('PoseidonGame.exe', 'OpenAL32.dll'):
        copy(args.client / name, out / 'client' / name)
    shutil.copytree(args.preparation, out / 'prepare')
    for name in ('CWRC.cmd', 'README-CWRC.txt'):
        copy(Path(__file__).with_name(name), release / 'files' / name)
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
    for file in args.helper_sources.iterdir():
        require(file.name.endswith(('.tar.gz', '.tar.xz', '.zip')), 'Source archive expected')
        copy(file, out / 'source/helper-dependencies' / file.name)
        if file.name.startswith(('openssl-', 'libffi-')):
            with tarfile.open(file) as archive:
                for member in archive.getmembers():
                    if member.isfile() and Path(member.name).name.upper() in ('LICENSE', 'LICENSE.TXT', 'COPYING', 'NOTICE'):
                        data = archive.extractfile(member).read()
                        relative = Path(*Path(member.name).parts[1:])
                        require('..' not in relative.parts, 'Unsafe notice path')
                        dest = out / 'notices/helper' / file.name.split('-', 1)[0] / relative
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes(data)
    for distribution in ('PyInstaller', 'fonttools', 'altgraph', 'packaging', 'pyinstaller-hooks-contrib', 'pywin32-ctypes'):
        d = importlib.metadata.distribution(distribution)
        for file in d.files or []:
            if 'license' in str(file).lower() or Path(str(file)).name.lower() in ('copying.txt', 'copying', 'authors.txt'):
                if d.locate_file(file).is_file():
                    copy(d.locate_file(file), out / 'notices/helper' / distribution / Path(str(file)).name)
    python_license = Path(sys.base_prefix) / 'LICENSE.txt'
    copy(python_license, out / 'notices/helper/Python.txt')
    copy(args.installed.parent / 'vcpkg/status', out / 'source/vcpkg-status.txt')
    copy(engine / 'build/local-labels/generated/Poseidon/Core/BuildInfo.hpp', out / 'source/BuildInfo.hpp')
    for name in ('clang-local.cmake', 'configure.cmd', 'build.cmd', 'build_ui_tests.cmd'):
        copy(args.build_tools / name, out / 'source/local-build' / name)
    shutil.copytree(args.build_tools / 'triplets', out / 'source/local-build/triplets')
    cache = args.vcpkg / 'buildtrees/openal-soft/x64-windows-clang-local-rel/CMakeCache.txt'
    copy(cache, out / 'source/OpenAL-CMakeCache.txt')

    source_archive(out / 'source/CWRC-source.zip', engine)
    record = {'client_commit': commit,
              'patch_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip(),
              'python': sys.version}
    (out / 'source/build-record.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    # Generated commercial overlays never enter the distributable.
    forbidden = {'.pbo', '.ext', '.sqm', '.sqs', '.paa', '.pac', '.wrp', '.p3d', '.wav', '.ogg', '.pdb', '.log', '.ico'}
    with zipfile.ZipFile(release / 'CWRC.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in sorted((release / 'files').rglob('*')):
            if file.is_file():
                relative = file.relative_to(release / 'files').as_posix()
                require(file.suffix.lower() not in forbidden, f'Unexpected commercial/generated artifact: {relative}')
                require(file.suffix.lower() != '.csv' or relative == '@CWRC/payload/mod/bin/stringtable.csv',
                        f'Reconstructed stock table: {relative}')
                archive.write(file, relative)
    archive = release / 'CWRC.zip'
    print(f'{archive}: {archive.stat().st_size} bytes; SHA-256 {digest(archive.read_bytes())}')


if __name__ == '__main__':
    main()
