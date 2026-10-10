import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_evidence.py'
spec = importlib.util.spec_from_file_location('ledger_validator', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'tests/fixtures/synthetic-ledger.json').read_text())

    def errors(self):
        return validator.validate(self.data)[0]

    def test_valid_ledger_and_unknown_date(self):
        self.assertEqual(self.errors(), [])

    def test_duplicate_ids_and_dangling_hypotheses(self):
        self.data['evidence'].append(copy.deepcopy(self.data['evidence'][0]))
        self.data['evidence'][1]['hypothesis_ids'] = ['H99']
        errors = ' '.join(self.errors())
        self.assertIn('duplicate evidence id', errors)
        self.assertIn('unknown hypothesis H99', errors)

    def test_snippet_is_not_verified_support_or_quote(self):
        self.data['evidence'][0]['access'] = 'snippet'
        errors = ' '.join(self.errors())
        self.assertIn('unverified lead cannot contain', errors)
        self.assertIn('stance=context', errors)

    def test_unavailable_lead_can_be_retained_honestly(self):
        self.data['evidence'][0].update(access='unavailable', excerpt=None, stance='context')
        errors, warnings = validator.validate(self.data)
        self.assertFalse(errors)
        self.assertTrue(any('no inspected original' in item for item in warnings))

    def test_invalid_and_impossible_dates(self):
        for bad_date in ('2026-02-30', '20261010', 20261010, '2026-10-11'):
            self.data['evidence'][0]['published_at'] = bad_date
            with self.subTest(date=bad_date):
                self.assertTrue(self.errors())

    def test_spending_requires_reported_action(self):
        self.data['evidence'][0].update(payment_signal='reported_spend', behavior=None)
        self.assertIn('reported_spend requires', ' '.join(self.errors()))

    def test_malformed_nested_values_do_not_crash(self):
        for field in ('source_type', 'access', 'payment_signal', 'stance', 'identity_basis', 'hypothesis_ids', 'url'):
            for value in ([], {}, 7):
                data = copy.deepcopy(self.data)
                data['evidence'][0][field] = value
                with self.subTest(field=field, value=value):
                    self.assertTrue(validator.validate(data)[0])
        for field in ('hypotheses', 'search_log', 'evidence'):
            data = copy.deepcopy(self.data)
            data[field] = [None]
            self.assertTrue(validator.validate(data)[0])
        self.assertTrue(validator.validate([])[0])

    def test_empty_research_is_valid_but_warned(self):
        self.data.update(evidence=[], search_log=[])
        errors, warnings = validator.validate(self.data)
        self.assertFalse(errors)
        self.assertTrue(any('no explicit counterevidence' in item for item in warnings))
        self.assertTrue(any('no inspected original' in item for item in warnings))

    def test_repeated_url_is_warning_not_extra_identity(self):
        extra = copy.deepcopy(self.data['evidence'][0])
        extra['id'] = 'E2'
        self.data['evidence'].append(extra)
        errors, warnings = validator.validate(self.data)
        self.assertFalse(errors)
        self.assertTrue(any('repeated URL' in item for item in warnings))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'ledger.json'
            for content, expected in ((json.dumps(self.data), 0), ('{}', 1), ('{bad json', 2)):
                path.write_text(content)
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)


if __name__ == '__main__':
    unittest.main()
