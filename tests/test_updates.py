"""Update discovery tests with no network traffic or real user-cache writes."""
import io
import http.client
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import update_check as updates


def release(tag, preview=False, **fields):
    return dict(tag_name=tag, prerelease=preview, draft=False, **fields)


class UpdateTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='harness-updates-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.cache = self.root / 'swg-source-harness/update-check.json'
        env = patch.dict(os.environ, {'XDG_CACHE_HOME': str(self.root), 'SWG_HARNESS_UPDATE_CHECK': '1'})
        env.start()
        self.addCleanup(env.stop)
        network = patch('update_check.urllib.request.urlopen')
        self.network = network.start()
        self.addCleanup(network.stop)

    def payload(self, data):
        self.network.return_value = io.BytesIO(json.dumps(data).encode())

    def test_extreme_timestamp_and_deep_json_cannot_break_hook(self):
        self.cache.parent.mkdir()
        self.cache.write_text(json.dumps({'attempted_at': 10 ** 400}))
        self.payload([release('v1.1.0')])
        self.assertIsNotNone(updates.check_updates('1.0.0'))
        self.network.return_value = io.BytesIO(b'[' * 1500 + b'0' + b']' * 1500)
        self.assertIsNone(updates.check_updates('1.0.0', force=True))

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO requires POSIX')
    def test_fifo_cache_is_ignored_without_opening_it(self):
        self.cache.parent.mkdir()
        os.mkfifo(self.cache)
        self.payload([release('v1.1.0')])
        self.assertIsNotNone(updates.check_updates('1.0.0'))
        import stat
        self.assertTrue(stat.S_ISFIFO(self.cache.stat().st_mode))

    def test_partial_http_response_is_advisory_only(self):
        self.network.return_value.__enter__.return_value.read.side_effect = http.client.IncompleteRead(b'partial')
        self.assertIsNone(updates.check_updates('1.0.0'))

    def test_newest_stable_preferred_and_url_is_canonical(self):
        self.payload([release('v1.2.0', html_url='https://evil.invalid/payload'),
                      release('v3.0.0-rc.1', True), release('v1.3.0')])
        notice = updates.check_updates('1.0.0')
        self.assertIn('v1.3.0', notice)
        self.assertIn(updates.RELEASE_URL, notice)
        self.assertNotIn('evil.invalid', notice)
        self.assertEqual(self.network.call_args.kwargs['timeout'], 2)

    def test_preview_only_is_labeled_and_semver_ordered(self):
        self.payload([release('v1.1.0-rc.2', True), release('v1.1.0-rc.10', True)])
        self.assertIn('preview release v1.1.0-rc.10', updates.check_updates('1.0.0'))

    def test_older_or_same_release_is_silent(self):
        self.payload([release('v1.0.0')])
        self.assertIsNone(updates.check_updates('1.0.0'))
        self.assertIsNone(updates.check_updates('2.0.0'))

    def test_fresh_cache_avoids_network_and_stale_refreshes(self):
        self.payload([release('v1.1.0')])
        with patch('update_check.time.time', return_value=100000):
            self.assertIsNotNone(updates.check_updates('1.0.0'))
        with patch('update_check.time.time', return_value=100001):
            self.assertIsNotNone(updates.check_updates('1.0.0'))
        self.assertEqual(self.network.call_count, 1)
        self.payload([release('v1.2.0')])
        with patch('update_check.time.time', return_value=200000):
            self.assertIn('v1.2.0', updates.check_updates('1.0.0'))
        self.assertEqual(self.network.call_count, 2)

    def test_timeout_is_cached_without_repeat_storm(self):
        self.network.side_effect = TimeoutError('offline')
        self.assertIsNone(updates.check_updates('1.0.0'))
        self.assertIsNone(updates.check_updates('1.0.0'))
        self.assertEqual(self.network.call_count, 1)

    def test_disabled_even_force_never_calls_network_or_writes(self):
        with patch.dict(os.environ, {'SWG_HARNESS_UPDATE_CHECK': '0'}):
            self.assertIsNone(updates.check_updates('1.0.0', force=True))
        self.network.assert_not_called()
        self.assertFalse(self.cache.exists())

    def test_malformed_metadata_and_versions_are_ignored(self):
        self.payload([None, release('../../bad'), release('1.01.0'),
                      release('1.1.0-01'), {'tag_name': 'v9.0.0', 'draft': True}])
        self.assertIsNone(updates.check_updates('1.0.0'))
        self.assertIsNone(updates.check_updates('not-a-version'))

    def test_corrupt_cache_does_not_prevent_refresh(self):
        self.cache.parent.mkdir()
        self.cache.write_text('{broken')
        self.payload([release('v1.2.0')])
        self.assertIsNotNone(updates.check_updates('1.0.0'))

    def test_force_refreshes_and_unwritable_cache_is_graceful(self):
        self.payload([release('v1.1.0')])
        updates.check_updates('1.0.0')
        self.payload([release('v1.2.0')])
        with patch('update_check.os.open', side_effect=PermissionError):
            self.assertIn('v1.2.0', updates.check_updates('1.0.0', force=True))

    def test_cache_symlink_does_not_modify_external_file(self):
        target = self.root / 'private.txt'
        target.write_text('private fixture')
        self.cache.parent.mkdir()
        try:
            self.cache.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        self.payload([])
        self.assertIsNone(updates.check_updates('1.0.0'))
        self.assertEqual(target.read_text(), 'private fixture')

    def test_cache_directory_symlink_is_not_written(self):
        target = self.root / 'elsewhere'
        target.mkdir()
        try:
            self.cache.parent.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        self.payload([])
        updates.check_updates('1.0.0')
        self.assertFalse((target / 'update-check.json').exists())


if __name__ == '__main__':
    unittest.main()
