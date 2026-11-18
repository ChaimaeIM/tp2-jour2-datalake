"""Tests unitaires du script d'inventaire.

Lancement depuis la racine du dépôt :
    python tests/ingestion/test_inventory.py
"""
import hashlib
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ingestion", "scripts"))

import inventory  # noqa: E402


class InspectFileTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, data):
        path = os.path.join(self.tmp.name, name)
        with open(path, "wb") as fh:
            fh.write(data)
        return path

    def test_semicolon_csv_header_and_lines(self):
        path = self.write("ventes.csv", b"id;nom;prix\n1;a;2.5\n2;b;3\n")
        row = inventory.inspect_file(path)
        self.assertEqual(row["format"], "CSV")
        self.assertEqual(row["columns"], 3)
        self.assertEqual(row["lines"], 3)
        self.assertEqual(row["notes"], [])

    def test_last_line_without_newline_is_counted(self):
        path = self.write("petit.csv", b"a,b\n1,2")
        row = inventory.inspect_file(path)
        self.assertEqual(row["lines"], 2)
        self.assertEqual(row["columns"], 2)

    def test_leading_blank_line_is_skipped(self):
        path = self.write("audit.csv", b"\nmaxItems,numCompetitors\n18000,89099\n")
        row = inventory.inspect_file(path)
        self.assertEqual(row["columns"], 2)
        self.assertIn("ligne vide en debut de fichier", row["notes"])

    def test_pipe_dat_without_header(self):
        path = self.write("store_sales.dat", b"1|1|1|1\n2|2|2|2\n")
        row = inventory.inspect_file(path)
        self.assertEqual(row["format"], "DAT")
        self.assertEqual(row["columns"], 4)
        self.assertEqual(row["lines"], 2)
        self.assertEqual(row["notes"], [])

    def test_empty_file_is_reported(self):
        path = self.write("vide.csv", b"")
        row = inventory.inspect_file(path)
        self.assertIn("fichier vide", row["notes"])

    def test_non_utf8_is_reported(self):
        path = self.write("latin.csv", b"id,nom\n1,\xe9t\xe9\xff\n")
        row = inventory.inspect_file(path)
        self.assertIn("encodage non UTF-8", row["notes"])

    def test_duplicate_header_is_reported(self):
        path = self.write("dup.csv", b"id,id,nom\n1,2,a\n")
        row = inventory.inspect_file(path)
        self.assertIn("noms de colonnes dupliques", row["notes"])

    def test_sha256_matches_hashlib(self):
        data = b"contenu de test\n" * 1000
        path = self.write("data.csv", data)
        row = inventory.inspect_file(path)
        self.assertEqual(row["sha256"], hashlib.sha256(data).hexdigest())

    def test_unknown_extension_is_reported(self):
        path = self.write("notes.xyz", b"abc\n")
        row = inventory.inspect_file(path)
        self.assertEqual(row["format"], "Inconnu")
        self.assertIn("extension non reconnue", row["notes"])

    def test_render_contains_header_and_row(self):
        path = self.write("ventes.csv", b"id,nom\n1,a\n")
        table = inventory.render_markdown([inventory.inspect_file(path)])
        self.assertIn("| Fichier | Format |", table)
        self.assertIn("| ventes.csv | CSV |", table)


if __name__ == "__main__":
    unittest.main()
