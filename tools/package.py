"""Build a reproducible release from immutable committed Git blobs."""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}

    def git(*args):
        result = subprocess.run(['git', '--no-optional-locks', '-c', 'core.fsmonitor=false',
                                 '-C', str(root), *args], capture_output=True, env=env, timeout=60)
        if result.returncode:
            raise ValueError('Packaging requires a committed Git source checkout.')
        return result.stdout

    if git('status', '--porcelain=v1', '--untracked-files=no', '--ignore-submodules=none'):
        raise ValueError('Commit tracked changes before packaging.')
    head = git('rev-parse', 'HEAD').decode().strip()
    entries = []
    for raw in git('ls-tree', '-r', '-z', head).split(b'\0'):
        if not raw:
            continue
        meta, name = raw.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = name.decode('utf-8')
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Release only supports regular committed files: ' + name)
        path = root / name
        if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
            raise ValueError('Linked release paths are unsupported: ' + name)
        if not path.is_file():
            raise ValueError('Missing release file: ' + name)
        entries.append((name, mode, oid))
    version_source = git('show', head + ':harness.py').decode()
    match = re.search(r"^VERSION = '([0-9]+\.[0-9]+\.[0-9]+)'$", version_source, re.M)
    if not match:
        raise ValueError('Committed harness version missing.')
    version = match.group(1)
    prefix = 'swg-source-harness-' + version
    out = root / 'dist'
    if out.is_symlink():
        raise ValueError('Release output directory must not be a symlink.')
    out.mkdir(exist_ok=True)
    archive = out / (prefix + '.zip')
    checksum_file = archive.with_suffix('.zip.sha256')
    if archive.is_symlink() or checksum_file.is_symlink():
        raise ValueError('Release outputs must not be symlinks.')
    with tempfile.TemporaryDirectory(prefix='.package-', dir=out) as temp:
        candidate = Path(temp) / archive.name
        with zipfile.ZipFile(candidate, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for name, mode, oid in sorted(entries):
                info = zipfile.ZipInfo(prefix + '/' + name, (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = int(mode, 8) << 16
                z.writestr(info, git('cat-file', 'blob', oid))
            info = zipfile.ZipInfo(prefix + '/RELEASE.json', (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, json.dumps({'version': version, 'commit': head}, sort_keys=True) + '\n')
        checksum = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if archive.exists() and hashlib.sha256(archive.read_bytes()).hexdigest() != checksum:
            raise ValueError('Version already packaged with different contents; bump VERSION or use a fresh checkout.')
        checksum_candidate = Path(temp) / checksum_file.name
        checksum_candidate.write_text(checksum + '  ' + archive.name + '\n', encoding='utf-8')
        # No existing artifact is touched until input validation and ZIP generation succeed.
        os.replace(candidate, archive)
        os.replace(checksum_candidate, checksum_file)
    print(archive)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        sys.exit(2)
