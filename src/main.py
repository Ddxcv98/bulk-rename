import os
import shutil
import subprocess
import sys
import uuid

from pathlib import Path


def get_rename_map(path: Path) -> dict[str, str]:
    edit_file = f"/tmp/{uuid.uuid4().hex}"
    source = sorted(map(lambda p: p.name, path.iterdir()))
    target = set()
    m = {}

    with open(edit_file, 'w') as file:
        for s in source:
            file.write(f"{s}\n")

    subprocess.run([os.getenv('EDITOR'), edit_file])

    with open(edit_file) as file:
        for s in source:
            line = file.readline()

            if not line:
                sys.stderr.write('Number of lines was not preserved.\n')
                exit(1)

            name = line.strip()

            if not name:
                m[s] = None
                continue

            if name in target:
                sys.stderr.write('Duplicated names found.\n')
                exit(1)

            m[s] = name
            target.add(name)

    os.remove(edit_file)
    return m


def rename_files(path: Path, m: dict[str, str]):
    tmp_path = Path(f"/tmp/{uuid.uuid4().hex}")
    tmp_path.mkdir()
    moved = {}
    removed = set()

    for key, value in m.items():
        if key == value or key in removed:
            continue

        source = moved.get(key) or path.joinpath(key)

        if not value:
            source.unlink()
            removed.add(key)
            continue

        target = path.joinpath(value)

        if target.exists():
            new_path = tmp_path.joinpath(value)
            shutil.move(target.as_posix(), new_path.as_posix())
            moved[value] = new_path

        shutil.move(source.as_posix(), target.as_posix())

    tmp_path.rmdir()
    pass


def main():
    path = Path().resolve()
    m = get_rename_map(path)
    rename_files(path, m)


if __name__ == '__main__':
    main()
