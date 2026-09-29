"""Best-effort release notices; never downloads or executes release contents."""
import json
import os
from pathlib import Path
import re
import time
import stat
import tempfile
import urllib.request

API_URL = 'https://api.github.com/repos/Akilleez-QA/swg-source-harness/releases?per_page=20'
RELEASE_URL = 'https://github.com/Akilleez-QA/swg-source-harness/releases/tag/'
INTERVAL = 24 * 60 * 60
_SEMVER = re.compile(r'^v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$')


def _version(value):
    if not isinstance(value, str) or len(value) > 150:
        return None
    match = _SEMVER.fullmatch(value)
    if not match:
        return None
    prerelease = match[4]
    if prerelease and any(p.isdigit() and len(p) > 1 and p[0] == '0' for p in prerelease.split('.')):
        return None
    # Numeric prerelease identifiers sort before textual identifiers; stable last.
    pre = tuple((0, int(p)) if p.isdigit() else (1, p) for p in prerelease.split('.')) if prerelease else ()
    return (int(match[1]), int(match[2]), int(match[3]), not bool(prerelease), pre)


def _cache_path():
    base = os.environ.get('XDG_CACHE_HOME')
    if not base and os.name == 'nt':
        base = os.environ.get('LOCALAPPDATA')
    base = Path(base).expanduser().resolve() if base else (Path.home() / '.cache').resolve()
    return base / 'swg-source-harness/update-check.json'


def _safe_path(path):
    # Reject symlinks at every existing component, including the cache file.
    return path.is_absolute() and not any(p.is_symlink() for p in (path, *path.parents))


def _read_cache(path):
    try:
        if not _safe_path(path) or not path.is_file():
            return {}
        flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_BINARY', 0)
        fd = os.open(path, flags)
        with os.fdopen(fd, 'rb') as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                return {}
            raw = stream.read(4097)
        if len(raw) > 4096:
            return {}
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, RecursionError):
        return {}


def _write_cache(path, value):
    temp = None
    try:
        if not _safe_path(path) or (path.exists() and not path.is_file()):
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        if not _safe_path(path):
            return
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix='.update-', delete=False) as stream:
            temp = Path(stream.name)
            json.dump(value, stream)
        os.replace(temp, path)
    except (OSError, ValueError):
        pass
    finally:
        if temp is not None:
            try:
                temp.unlink(missing_ok=True)
            except OSError:
                pass


def _notice(current, release):
    if not isinstance(release, dict):
        return None
    tag = release.get('tag')
    version = _version(tag)
    if not version or version <= current:
        return None
    preview = release.get('preview') is True or not version[3]
    label = 'preview release' if preview else 'release'
    return 'New harness %s %s available: %s%s' % (label, tag, RELEASE_URL, tag)


def _check_updates(current_version, *, force=False):
    """Return a newer-release notice or None; opt-out also applies to force."""
    if os.environ.get('SWG_HARNESS_UPDATE_CHECK', '').strip() == '0':
        return None
    current = _version(current_version)
    if current is None:
        return None
    path = _cache_path()
    cache = _read_cache(path)
    now = time.time()
    attempted = cache.get('attempted_at')
    if not force and type(attempted) in (int, float) and 0 <= attempted <= now and now - attempted < INTERVAL:
        return _notice(current, cache.get('release'))
    # Record even failed attempts to avoid repeated network requests offline.
    cache = {'attempted_at': now}
    _write_cache(path, cache)
    try:
        request = urllib.request.Request(API_URL, headers={'Accept': 'application/vnd.github+json',
                                                          'User-Agent': 'swg-source-harness-update-check'})
        with urllib.request.urlopen(request, timeout=2) as response:
            payload = response.read(512 * 1024 + 1)
        if len(payload) > 512 * 1024:
            return None
        releases = json.loads(payload)
        if not isinstance(releases, list):
            return None
        candidates = []
        for release in releases:
            if not isinstance(release, dict) or release.get('draft') is not False:
                continue
            version = _version(release.get('tag_name'))
            if version is None or type(release.get('prerelease')) is not bool:
                continue
            preview = release['prerelease'] or not version[3]
            candidates.append((version, {'tag': release['tag_name'], 'preview': preview}))
        stable = [c for c in candidates if not c[1]['preview']]
        selected = max(stable or candidates, key=lambda c: c[0])[1] if candidates else None
        cache['release'] = selected
        _write_cache(path, cache)
        return _notice(current, selected)
    except (OSError, ValueError, TypeError, RecursionError):
        return None


def check_updates(current_version, *, force=False):
    """Advisory failures must never change a contribution command's outcome."""
    try:
        return _check_updates(current_version, force=force)
    except Exception:
        # Includes truncated HTTP responses and platform-specific cache errors.
        # Process interrupts/SystemExit still propagate. This is not a pass claim.
        return None
