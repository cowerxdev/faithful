import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from faithful import faithful


class FaithfulTests(unittest.TestCase):
    def test_grounding_and_missing_tokens(self):
        source = 'Alpha offers 12 models and an API. Builders test Alpha.'
        good = {'summary': 'Alpha offers 12 models. Alpha has an API.', 'why_builder_cares': 'Builders test Alpha.'}
        self.assertEqual('', faithful(good, source))
        bad = {'summary': 'Nova offers 13 models. Alpha uses phantom9.', 'why_builder_cares': 'Builders test vEngine.'}
        reason = faithful(bad, source)
        for item in ('name Nova', 'number 13', 'product phantom9', 'product vEngine'):
            self.assertIn(item, reason)

    def test_format_and_cli(self):
        self.assertIn('two sentences', faithful({'summary': 'Alpha works.', 'why_builder_cares': 'Builders benefit.'}, 'Alpha Builders'))
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp, 'source.txt')
            summary = Path(tmp, 'summary.json')
            source.write_text('Alpha has 12 models. Builders test Alpha.')
            summary.write_text(json.dumps({'summary': 'Alpha has 12 models. Alpha works.', 'why_builder_cares': 'Builders test Alpha.'}))
            run = subprocess.run([sys.executable, '-m', 'faithful', str(source), str(summary)], capture_output=True, text=True)
            self.assertEqual(0, run.returncode, run.stderr)
            self.assertIn('PASS', run.stdout)
