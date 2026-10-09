"""Assemble Chinese-only text and authored assets; no commercial game data."""
import argparse
import json
from pathlib import Path
from build_content import PATCH, digest, require

def payload_file(file):
    data = file.read_bytes()
    if file.relative_to(PATCH).as_posix() == 'multiplayer/text-references.json':
        recipes = json.loads(data)
        data = (json.dumps({name: {member: [edit[:3] for edit in edits] for member, edits in members.items()}
                           for name, members in recipes.items()}, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return data


def assemble(output):
    """Assemble safe data from the committed recipe and existing authored assets."""
    require(not output.exists(), 'Choose an absent payload output')
    recipe = Path(__file__).with_name('payload.json').read_bytes()
    manifest = json.loads(recipe)
    # The recipe has keys, Chinese values, references and hashes, not stock columns.
    data = {rel: payload_file(PATCH / rel) for rel in manifest['files']}
    require(all(digest(value) == manifest['files'][rel] for rel, value in data.items()), 'Authored payload asset differs')
    output.mkdir(parents=True)
    (output / 'payload.json').write_bytes(recipe)
    for rel, value in data.items():
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(value)
    print('PASS: Chinese-only payload assembled; ten finished fonts; no commercial game data/client')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    assemble(parser.parse_args().output.resolve())
