"""Package tracked working-tree sources; no Git history or untracked files."""
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness import VERSION
root = Path(__file__).resolve().parents[1]
files = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z']).split(b'\0')
out = root / 'dist'
out.mkdir(exist_ok=True)
archive = out / ('swg-source-harness-' + VERSION + '.zip')
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for raw in sorted(filter(None, files)):
        name = raw.decode()
        p = root / name
        if p.is_symlink() or not p.is_file():
            raise SystemExit('Refusing non-regular tracked file: ' + name)
        info = zipfile.ZipInfo('swg-source-harness-' + VERSION + '/' + name, (2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, p.read_bytes())
checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(checksum + '  ' + archive.name + '\n')
print(archive)
