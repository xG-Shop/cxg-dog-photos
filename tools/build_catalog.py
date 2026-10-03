"""Builds the CXG breed collection from the dogs made with DOGS MAKER.

    python tools/build_catalog.py --pets <[PETS] folder> [--bundle <cxg_companion>]

Reads every <model>_anims.json under --pets (the folder with the breed
resources), groups the models by family (cxg_doberman, its _juvenile and
its _puppy) and writes catalog.json at the root of this repository. Photos:
photos/<family>.webp; when missing, it is copied from the adult's resource
(<family>/<family>_photo.webp, written by DOGS MAKER).

Breeds already in catalog.json that are not on this disk are kept (the
collection only grows), and hand-written fields are kept: a "label" set here
wins over the one in the dog's json, and "store" is never touched.

--bundle also refreshes the copy that ships inside cxg_companion
(data/catalog.json + ui/breeds/), so the tablet works without internet.
"""
import argparse
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# Where the photos are served from once this repository is on GitHub.
BASE_URL = 'https://raw.githubusercontent.com/xG-Shop/cxg-dog-photos/main/'
AGES = ('puppy', 'juvenile', 'adult')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def scan(pets):
    """family -> what the dogs on disk say about it."""
    found = {}
    for table in sorted(pets.glob('*/*_anims.json')):
        data = read(table)
        family, age = data.get('family'), data.get('age')
        if not family or age not in AGES:
            continue
        entry = found.setdefault(family, {'family': family, 'ages': set()})
        entry['ages'].add(age)
        if data.get('breed'):
            entry.setdefault('label', data['breed'])
        if age == 'adult':
            entry['withers_cm'] = data.get('withers_cm')
            entry['resource'] = table.parent
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pets', type=Path, required=True, help='folder with the breed resources ([PETS])')
    parser.add_argument('--bundle', type=Path, help='cxg_companion folder to refresh')
    args = parser.parse_args()

    catalog_path = REPO / 'catalog.json'
    catalog = read(catalog_path) if catalog_path.exists() else {'version': 1, 'store': None, 'breeds': []}
    breeds = {entry['family']: entry for entry in catalog.get('breeds', [])}

    for family, dog in scan(args.pets).items():
        entry = breeds.setdefault(family, {'family': family})
        entry.setdefault('label', dog.get('label') or family)
        known = set(entry.get('ages', [])) | dog['ages']
        entry['ages'] = [age for age in AGES if age in known]
        if dog.get('withers_cm'):
            entry['withers_cm'] = dog['withers_cm']
        photo = REPO / 'photos' / f'{family}.webp'
        made = dog.get('resource') and dog['resource'] / f'{family}_photo.webp'
        if made and made.exists() and (not photo.exists() or made.stat().st_mtime > photo.stat().st_mtime):
            shutil.copyfile(made, photo)

    for family, entry in breeds.items():
        photo = REPO / 'photos' / f'{family}.webp'
        entry['photo'] = BASE_URL + f'photos/{family}.webp' if photo.exists() else None

    catalog['breeds'] = sorted(breeds.values(), key=lambda entry: entry.get('label', entry['family']))
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'catalog.json: {len(catalog["breeds"])} razas')
    for entry in catalog['breeds']:
        print(f'  {entry["family"]:<24} {entry.get("label", ""):<16} {",".join(entry.get("ages", [])):<22} {"foto" if entry["photo"] else "sin foto"}')

    if args.bundle:
        # The bundled copy points at files inside the resource (ui/breeds/).
        bundled = json.loads(json.dumps(catalog))
        target = args.bundle / 'ui' / 'breeds'
        target.mkdir(parents=True, exist_ok=True)
        for entry in bundled['breeds']:
            photo = REPO / 'photos' / f'{entry["family"]}.webp'
            if photo.exists():
                shutil.copyfile(photo, target / photo.name)
                entry['photo'] = f'breeds/{photo.name}'
            else:
                entry['photo'] = None
        (args.bundle / 'data' / 'catalog.json').write_text(json.dumps(bundled, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'Copia incluida actualizada en {args.bundle}')


if __name__ == '__main__':
    main()
