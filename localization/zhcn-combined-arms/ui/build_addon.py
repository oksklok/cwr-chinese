"""Pack the authored display-only config (no stock/commercial members)."""
import argparse
import struct
from pathlib import Path


def payload():
    data = Path(__file__).with_name('config.cpp').read_bytes()
    return b'config.cpp\0' + struct.pack('<5I', 0, 0, 0, 0, len(data)) + bytes(21) + data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    game = args.game.resolve()
    if not (game / 'PoseidonGame.exe').is_file():
        raise ValueError('Not a Remastered game directory')
    target = game / '@zhcn-prototype/AddOns/cwrc_ui.pbo'
    expected = payload()
    if target.exists():
        if target.read_bytes() != expected:
            raise ValueError(f'Differing existing addon; leave it untouched: {target}')
    elif args.check:
        raise ValueError(f'Missing authored UI addon: {target}')
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(expected)
    print('PASS: authored UI addon equality (one config.cpp; no commercial assets)')


if __name__ == '__main__':
    main()
