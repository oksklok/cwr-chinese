"""Thin frozen entry point for CWRC Setup; file ownership stays in install_core.

GPL-3.0-or-later with the repository Section 7 terms.
"""
import argparse
import shutil
import sys
from pathlib import Path

import install_core as core


def main():
    if getattr(sys, 'frozen', False):
        core.PATCH = Path(sys._MEIPASS) / 'runtime'
    if sys.stdout:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('install', 'uninstall', 'recover'))
    parser.add_argument('game', type=Path)
    parser.add_argument('--package', type=Path, default=Path(sys.executable).parent.parent)
    parser.add_argument('--wrapper-dir', type=Path)
    args = parser.parse_args()
    game = args.game.resolve()
    try:
        if (game / core.STATE / 'pending.json').exists():
            print('STEP 5 Recovering the interrupted installation', flush=True)
            core.recover(game)
        if args.operation == 'install':
            if args.wrapper_dir and not (game / core.STATE / 'receipt.json').exists():
                parent = args.wrapper_dir.resolve()
                while not parent.exists():
                    parent = parent.parent
                if parent.stat().st_dev == game.stat().st_dev:
                    manifest, _ = core.load_payload(args.package / 'payload')
                    components = sum(p.stat().st_size for p in args.package.rglob('*') if p.is_file())
                    need = core.required_space(game, args.package / 'payload', manifest, args.package / 'client') + components
                    core.require(shutil.disk_usage(game).free > need,
                                 f'Insufficient space including wrapper components: need {need // 1024**2 + 1} MiB free')
            core.install(game, args.package / 'payload', args.package / 'client')
        elif args.operation == 'recover':
            if (game / core.RETIRED).exists():
                core.resume_retired(game)
        elif (game / core.STATE).exists() or (game / core.RETIRED).exists():
            print('STEP 10 Verifying backups and restoring original files', flush=True)
            if core.uninstall(game):
                return 2
        print('STEP 100 Operation completed', flush=True)
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f'ERROR: {error}', flush=True)
        print('Original backups and recovery metadata are retained whenever restoration is incomplete.', flush=True)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
