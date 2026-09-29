#!/usr/bin/env python3
"""Provider-neutral, unsigned local submission preflight. No project approval."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = '0.1.1'
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
    status = git(root, 'status', '--porcelain=v1', '--untracked-files=all', '--ignore-submodules=none')
    subs = git(root, 'submodule', 'status', '--recursive').decode().splitlines()
    return {'head': head, 'tree': git(root, 'rev-parse', head + '^{tree}').decode().strip(),
            'clean': not bool(status), 'submodules': subs,
            'status_digest': digest(status)}


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
        if not p.is_file() or p.is_symlink():
            problems.append('Check %d evidence file unavailable.' % index)
            continue
        hasher = hashlib.sha256()
        with p.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                hasher.update(chunk)
        actual = hasher.hexdigest()
        if actual != expected:
            problems.append('Check %d evidence digest does not match.' % index)
        # Publish only the digest, not the local path or potentially secret log contents.
        records.append({'check': check.get('name'), 'sha256': actual, 'origin': 'contributor-supplied'})
    if snapshot(workspace) != identity:
        raise ValueError('Workspace changed during collection; rerun on a stable checkout.')
    return {'schema': SCHEMA, 'harness_version': VERSION,
            'created_at': datetime.now(timezone.utc).isoformat(), 'candidate': identity,
            'base': resolved_base, 'changed_paths': paths, 'task_digest': digest(encoded(task)),
            'evidence': records, 'problems': problems,
            'local_status': 'needs-information' if problems else 'preflight-complete',
            'review_eligible': False, 'signed': False,
            'verification_boundary': 'Structure and local file hashes only. Tests are contributor reports, not executed or independently verified. No project intake approval.'}


def read_json(path):
    with Path(path).open('rb') as stream:
        data = stream.read(2 * 1024 * 1024 + 1)
    if len(data) > 2 * 1024 * 1024:
        raise ValueError('JSON input exceeds 2 MiB.')
    return json.loads(data)


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
    args = parser.parse_args(argv)
    try:
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
        if not isinstance(report, dict) or report.get('schema') != SCHEMA:
            raise ValueError('Unsupported report schema.')
        checksum = report.pop('integrity_sha256', None)
        if checksum != digest(encoded(report)):
            raise ValueError('Report integrity mismatch.')
        if report.get('review_eligible') is not False or report.get('signed') is not False:
            raise ValueError('Local reports cannot assert trusted review eligibility.')
        current = snapshot(args.workspace)
        if current != report.get('candidate') or not current['clean']:
            raise ValueError('Report is stale or workspace is dirty.')
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
