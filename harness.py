#!/usr/bin/env python3
"""Provider-neutral, unsigned local submission preflight. No project approval."""
import argparse
import hashlib
import json
import math
import os
import stat
import re
from contextlib import contextmanager
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from update_check import check_updates

VERSION = '0.2.0'
SCHEMA = 'swg-local-preflight/v1'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    result = subprocess.run(['git', '--no-optional-locks', '-c', 'core.fsmonitor=false',
                             '-C', str(root), *args],
                            capture_output=True, timeout=60, env=env)
    if result.returncode:
        raise ValueError('Git inspection failed; check repository and revision.')
    return result.stdout


def snapshot(workspace):
    root = Path(workspace).resolve()
    top = Path(git(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
    if root != top:
        raise ValueError('Use the repository root, not a subdirectory.')
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    states = []
    flags = []
    visited = set()

    def inspect_tree(path):
        resolved = path.resolve()
        if resolved in visited:
            raise ValueError('Repeated submodule path during inspection.')
        visited.add(resolved)
        prefix = path.relative_to(root).as_posix()
        status = git(path, 'status', '--porcelain=v1', '--untracked-files=all',
                     '--ignore-submodules=none')
        states.append({'path': prefix, 'dirty': bool(status), 'digest': digest(status)})
        for entry in git(path, 'ls-files', '-v', '-z').split(b'\0'):
            if entry and (entry[:1].islower() or entry[:1] == b'S'):
                flags.append(prefix + '/' + entry[2:].decode('utf-8', 'replace'))
        for entry in git(path, 'ls-files', '--stage', '-z').split(b'\0'):
            if entry.startswith(b'160000 '):
                child = path / os.fsdecode(entry.split(b'\t', 1)[1])
                if (child / '.git').exists():
                    inspect_tree(child)

    inspect_tree(root)
    subs = git(root, 'submodule', 'status', '--recursive').decode().splitlines()
    if git(root, 'rev-parse', 'HEAD').decode().strip() != head:
        raise ValueError('HEAD changed during inspection; use a stable checkout.')
    return {'head': head, 'tree': git(root, 'rev-parse', head + '^{tree}').decode().strip(),
            'clean': not flags and not any(x['dirty'] for x in states),
            'submodules': subs, 'index_flags': sorted(flags),
            'status_digest': digest(encoded(states))}


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as out:
        json.dump(value, out, indent=2, ensure_ascii=True)
        out.write('\n')


def outside_workspace(path, workspace):
    path = Path(path).resolve()
    root = Path(workspace).resolve()
    if path == root or root in path.parents:
        raise ValueError('Store task/report files outside the inspected workspace.')


def valid_text(value):
    return isinstance(value, str) and bool(value.strip())


def preflight(workspace, task):
    if not isinstance(task, dict) or task.get('schema') != 'swg-task/v1':
        raise ValueError('Expected a swg-task/v1 object.')
    identity = snapshot(workspace)
    problems = []
    for field in ('repository', 'goal', 'expected_behavior', 'environment', 'base', 'ai_contribution', 'ai_pr_text'):
        if not valid_text(task.get(field)):
            problems.append('Complete task field: ' + field)
    if identity['index_flags']:
        problems.append('Index assume-unchanged/skip-worktree flags prevent clean inspection; use a full checkout without these flags.')
    if not identity['clean']:
        problems.append('Commit or preserve workspace changes before producing a candidate report.')
    if any(s.startswith(('-', '+', 'U')) for s in identity['submodules']):
        problems.append('Initialize submodules and reconcile their pinned revisions.')
    base = task.get('base')
    resolved_base = None
    paths = []
    if valid_text(base):
        # Only object IDs are accepted: no option/ref injection or moving branch names.
        if len(base) not in (40, 64) or any(c not in '0123456789abcdef' for c in base):
            problems.append('base must be a full lowercase Git commit ID.')
        else:
            resolved_base = git(workspace, 'rev-parse', '--verify', base + '^{commit}').decode().strip()
            paths = [p.decode('utf-8', 'replace') for p in git(workspace, 'diff', '--name-only', '-z', resolved_base, identity['head'], '--').split(b'\0') if p]
            if not paths:
                problems.append('No committed changes relative to base.')
    checks = task.get('checks')
    if not isinstance(checks, list) or not checks:
        problems.append('Describe at least one relevant validation check.')
        checks = []
    records = []
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            problems.append('Check %d must be an object.' % index)
            continue
        for field in ('name', 'command_or_steps', 'expected', 'observed'):
            if not valid_text(check.get(field)):
                problems.append('Check %d missing %s.' % (index, field))
        if check.get('status') != 'passed':
            problems.append('Check %d is not reported passed.' % index)
        if check.get('tested_commit') != identity['head']:
            problems.append('Check %d is not bound to candidate HEAD.' % index)
        evidence = check.get('evidence')
        if not isinstance(evidence, dict) or not valid_text(evidence.get('path')):
            problems.append('Check %d needs a local evidence file and SHA-256.' % index)
            continue
        p = Path(evidence['path']).expanduser()
        if not p.is_absolute():
            problems.append('Check %d evidence path must be absolute.' % index)
            continue
        expected = evidence.get('sha256')
        try:
            hasher = hashlib.sha256()
            with regular_file(p) as stream:
                before = os.fstat(stream.fileno())
                if before.st_size > 512 * 1024 * 1024:
                    raise ValueError('Evidence exceeds 512 MiB; provide a focused log.')
                total = 0
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    total += len(chunk)
                    if total > 512 * 1024 * 1024:
                        raise ValueError('Evidence exceeds 512 MiB.')
                    hasher.update(chunk)
                after = os.fstat(stream.fileno())
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    raise ValueError('Evidence changed while being read.')
            actual = hasher.hexdigest()
        except (OSError, ValueError):
            problems.append('Check %d evidence file unavailable, non-regular, changing or too large.' % index)
            continue
        if actual != expected:
            problems.append('Check %d evidence digest does not match.' % index)
        # Publish only the digest, not the local path or potentially secret log contents.
        if valid_text(check.get('name')):
            records.append({'check': check['name'], 'sha256': actual, 'origin': 'contributor-supplied'})
    if snapshot(workspace) != identity:
        raise ValueError('Workspace changed during collection; rerun on a stable checkout.')
    return {'schema': SCHEMA, 'harness_version': VERSION,
            'created_at': datetime.now(timezone.utc).isoformat(), 'candidate': identity,
            'base': resolved_base, 'changed_paths': paths, 'task_digest': digest(encoded(task)),
            'evidence': records, 'problems': problems,
            'local_status': 'needs-information' if problems else 'preflight-complete',
            'review_eligible': False, 'signed': False,
            'verification_boundary': 'Structure and local file hashes only. Tests are contributor reports, not executed or independently verified. No project intake approval.'}


@contextmanager
def regular_file(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError('Input must be a regular file, not a link or special file.')
    flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_BINARY', 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError('Input must be a regular file.')
        yield stream


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('Duplicate JSON field is not allowed.')
        value[key] = item
    return value


def reject_constant(value):
    raise ValueError('Non-finite JSON number is not allowed.')


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError('Non-finite JSON number is not allowed.')
    return number


def read_json(path):
    with regular_file(path) as stream:
        data = stream.read(2 * 1024 * 1024 + 1)
    if len(data) > 2 * 1024 * 1024:
        raise ValueError('JSON input exceeds 2 MiB.')
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=reject_constant, parse_float=finite_float)


def hex_value(value, lengths):
    return isinstance(value, str) and len(value) in lengths and re.fullmatch('[0-9a-f]+', value) is not None


def validate_report(report):
    required = {'schema', 'harness_version', 'created_at', 'candidate', 'base',
                'changed_paths', 'task_digest', 'evidence', 'problems', 'local_status',
                'review_eligible', 'signed', 'verification_boundary', 'integrity_sha256'}
    if not isinstance(report, dict) or set(report) != required or report.get('schema') != SCHEMA:
        raise ValueError('Unsupported or malformed report schema.')
    for field in ('harness_version', 'created_at', 'verification_boundary'):
        if not valid_text(report[field]):
            raise ValueError('Malformed report field: ' + field)
    try:
        when = datetime.fromisoformat(report['created_at'].replace('Z', '+00:00'))
        if when.tzinfo is None:
            raise ValueError()
    except ValueError:
        raise ValueError('Report timestamp needs an explicit timezone.')
    if not hex_value(report['task_digest'], (64,)) or not hex_value(report['integrity_sha256'], (64,)):
        raise ValueError('Malformed report digest.')
    if report['base'] is not None and not hex_value(report['base'], (40, 64)):
        raise ValueError('Malformed report base.')
    for field in ('changed_paths', 'problems'):
        if not isinstance(report[field], list) or not all(valid_text(x) for x in report[field]):
            raise ValueError('Malformed report list: ' + field)
    if not isinstance(report['candidate'], dict) or not isinstance(report['evidence'], list):
        raise ValueError('Malformed candidate or evidence.')
    for record in report['evidence']:
        if (not isinstance(record, dict) or set(record) != {'check', 'sha256', 'origin'}
                or not valid_text(record['check']) or not hex_value(record['sha256'], (64,))
                or record['origin'] != 'contributor-supplied'):
            raise ValueError('Malformed evidence record.')
    complete = report['local_status'] == 'preflight-complete'
    if report['local_status'] not in ('preflight-complete', 'needs-information'):
        raise ValueError('Unknown preflight status.')
    if complete and (report['problems'] or not report['evidence'] or not report['changed_paths'] or report['base'] is None):
        raise ValueError('Complete report is missing required evidence or contains problems.')
    if not complete and not report['problems']:
        raise ValueError('Incomplete report must explain its problems.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=VERSION)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('init', 'inspect', 'check', 'verify'):
        cmd = sub.add_parser(name)
        cmd.add_argument('--workspace', required=True)
        if name in ('init', 'check'):
            cmd.add_argument('--output', required=True)
        if name == 'check':
            cmd.add_argument('--task', required=True)
        if name == 'verify':
            cmd.add_argument('--report', required=True)
    updates = sub.add_parser('updates', help='Check for a newer GitHub release; never install it.')
    updates.add_argument('--force', action='store_true', help='Bypass the daily cache (unless checks are disabled).')
    args = parser.parse_args(argv)
    try:
        notice = check_updates(VERSION, force=args.command == 'updates' and args.force)
        if args.command == 'updates':
            print(notice or 'No update notice: the check may be current, cached, disabled or unavailable.')
            return 0
        if notice:
            print(notice, file=sys.stderr)
        if args.command == 'inspect':
            print(json.dumps(snapshot(args.workspace), indent=2))
            return 0
        if args.command == 'init':
            outside_workspace(args.output, args.workspace)
            identity = snapshot(args.workspace)
            task = {'schema': 'swg-task/v1', 'repository': '', 'base': identity['head'],
                    'goal': '', 'expected_behavior': '', 'environment': '',
                    'ai_contribution': '', 'ai_pr_text': '', 'checks': [{
                        'name': '', 'command_or_steps': '', 'expected': '', 'observed': '',
                        'status': 'not-run', 'tested_commit': '',
                        'evidence': {'path': '', 'sha256': ''}}]}
            write_new(args.output, task)
            print('Task template created. Fill it in after performing your checks.')
            return 0
        if args.command == 'check':
            outside_workspace(args.output, args.workspace)
            report = preflight(args.workspace, read_json(args.task))
            report['integrity_sha256'] = digest(encoded(report))
            write_new(args.output, report)
            print(report['local_status'] + ': unsigned local report; not review approval.')
            for problem in report['problems']:
                print('- ' + problem)
            return 1 if report['problems'] else 0
        report = read_json(args.report)
        validate_report(report)
        checksum = report.pop('integrity_sha256', None)
        if checksum != digest(encoded(report)):
            raise ValueError('Report integrity mismatch.')
        if report.get('review_eligible') is not False or report.get('signed') is not False:
            raise ValueError('Local reports cannot assert trusted review eligibility.')
        current = snapshot(args.workspace)
        if current != report.get('candidate') or not current['clean']:
            raise ValueError('Report is stale or workspace is dirty.')
        if report['base'] is not None:
            paths = [p.decode('utf-8', 'replace') for p in git(args.workspace, 'diff', '--name-only', '-z', report['base'], current['head'], '--').split(b'\0') if p]
            if paths != report['changed_paths']:
                raise ValueError('Reported changes do not match base and candidate.')
        if report.get('local_status') != 'preflight-complete' or report.get('problems') != []:
            print('Local checksum and candidate match, but preflight is incomplete. Resolve reported problems and rerun check.')
            return 1
        print('Local checksum and clean candidate match. Not a signature, test verification or project approval.')
        return 0
    except (ValueError, OSError, RecursionError, subprocess.SubprocessError) as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
