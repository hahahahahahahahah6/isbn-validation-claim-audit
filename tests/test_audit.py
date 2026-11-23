import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from isbn_validation_claim_audit.audit import audit, evidence, matches, prose
from isbn_validation_claim_audit.phrases import ISBNVALIDATION, NOISBNVALIDATION, GENERIC_NAMES

ROOT = Path(__file__).resolve().parents[1]

class AuditTests(unittest.TestCase):
    def test_phrases(self):
        for phrase in ISBNVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertTrue(matches(phrase)[0])
        for phrase in NOISBNVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertEqual(matches(phrase)[0], [])
                self.assertTrue(matches(phrase)[1])
        self.assertEqual(matches('```\nvalidate isbn\n```'), ([], []))

    def test_routes(self):
        for name in ('is_isbn10', 'is_isbn13', 'notisbn', 'Isbn'):
            for source in (f'import isbnlib as lib\nlib.{name}(x)', f'from isbnlib import {name} as f\nf(x)'):
                with self.subTest(source=source): self.assertTrue(evidence(source))
        for name in ('validate', 'is_valid', 'isbn_type'):
            for source in (f'import stdnum\nstdnum.isbn.{name}(x)', f'import stdnum.isbn\nstdnum.isbn.{name}(x)', f'from stdnum import isbn as i\ni.{name}(x)', f'from stdnum.isbn import {name} as f\nf(x)'):
                with self.subTest(source=source): self.assertTrue(evidence(source))
        for name in GENERIC_NAMES:
            for source in (f'obj.{name}(x)', f'from somewhere import {name} as f\nf(x)', f'obj = object()\nobj.{name}(x)', f'factory().{name}(x)'):
                with self.subTest(source=source): self.assertTrue(evidence(source))

    def test_not_evidence(self):
        sources = ['import isbnlib', 'import stdnum', 'import isbnlib\n# isbnlib.is_isbn13(x)', '"validate isbn"', 'import isbnlib\nisbnlib.is_isbn13', 'x.isbn13', 'def broken(:', 'import subprocess\nsubprocess.run(["validator"])', 'import isbnlib\nisbnlib = None\nisbnlib.is_isbn13(x)', 'from isbnlib import is_isbn13\ndef is_isbn13(x): pass\nis_isbn13(x)', 'from elsewhere import validate_isbn\nwith thing() as validate_isbn: pass\nvalidate_isbn(x)', 'from urllib.parse import urlparse, urlsplit\nurlparse(x)\nurlsplit(x)', 'import re\nre.match("[0-9]+", x)\nre.search("x", x)\nre.fullmatch("x", x)', 'import barcode\nbarcode.ISBN13(x)\nbarcode.ISBN10(x)\nbarcode.get(x)\nbarcode.generate(x)', 'pay(x)\nextract(x)']
        for name in ('is_isbn10','is_isbn13','notisbn','Isbn','validate','is_valid','isbn_type'):
            sources.extend((f'{name}(x)', f'unknown.{name}(x)'))
        for name in ('canonical','clean','mask','to_isbn10','to_isbn13','ean13','EAN13','GTIN13','check_digit10','check_digit13','get_isbnlike','get_canonical_isbn','cover','desc','doi','editions','info','meta','ren','isbn_from_words'):
            sources.append(f'import isbnlib\nisbnlib.{name}(x)')
        for name in ('compact','split','format','to_isbn10','to_isbn13'):
            sources.append(f'import stdnum.isbn\nstdnum.isbn.{name}(x)')
        for name in ('url','ipv4','ipv6','email','card_number','domain'):
            sources.append(f'import validators\nvalidators.{name}(x)')
        for source in sources:
            with self.subTest(source=source): self.assertFalse(evidence(source))
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('validate isbn'); (p/'a.py').write_text('import isbnlib'); (p/'b.py').write_text('isbnlib.is_isbn13(x)')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'HIGH')

    def test_findings_and_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('validate isbn'); (p/'tests').mkdir(); (p/'tests/test_x.py').write_text('import isbnlib\nisbnlib.is_isbn13(x)')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'MEDIUM')
            for args, code in (([],0), (['--fail-on','medium'],2)):
                result=subprocess.run([sys.executable,'-m','isbn_validation_claim_audit','audit',d,'--json']+args, capture_output=True, text=True)
                self.assertEqual(result.returncode,code); self.assertIn('findings',json.loads(result.stdout))
            (p/'app.py').write_text('import isbnlib\nisbnlib.Isbn(x)'); (p/'README.md').write_text('no isbn validation')
            self.assertEqual(audit(p)['findings'][0]['severity'], 'HIGH')
            self.assertFalse(audit(p, ['app.py'])['findings'])

    def test_self_audit(self):
        self.assertFalse(audit(ROOT)['findings'])
        self.assertFalse(audit(ROOT/'README.md')['findings'])

    def test_limitations_prose(self):
        text=(ROOT/'README.md').read_text().split('## Limitations',1)[1].split('## Differentiation',1)[0]
        self.assertEqual(matches(text), ([], []))
        self.assertTrue(prose(text))

if __name__ == '__main__':
    unittest.main()
