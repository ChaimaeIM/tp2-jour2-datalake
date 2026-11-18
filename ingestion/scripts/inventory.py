#!/usr/bin/env python3
"""Inventaire lecture seule des fichiers sources avant ingestion.

Pour chaque fichier des dossiers donnés, le script affiche une ligne de tableau
Markdown : nom, format, taille, nombre de lignes, nombre de colonnes, empreinte
SHA-256 et observations. Aucun fichier n'est modifié ni déplacé.

Limite : le comptage suppose un enregistrement par ligne. Un champ CSV entre
guillemets contenant un saut de ligne fausse le comptage. Le script ne le détecte pas.

Exemples :
    python3 inventory.py /data/nifi/input
    python3 inventory.py --recursive ./sources > docs/ingestion/inventaire-brut.md
"""
import argparse
import codecs
import csv
import hashlib
import os
import sys

CHUNK = 1 << 20
SNIFF_BYTES = 8192

KNOWN_FORMATS = {
    ".csv": "CSV",
    ".tsv": "TSV",
    ".dat": "DAT",
    ".json": "JSON",
    ".parquet": "Parquet",
    ".txt": "Texte",
}
# None : séparateur détecté automatiquement
FIXED_DELIMITERS = {".csv": None, ".tsv": "\t", ".dat": "|"}
# Les fichiers .dat du kit TPCx-BB n'ont pas d'en-tête
HAS_HEADER = {".csv": True, ".tsv": True, ".dat": False}


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_lines_and_check_utf8(path):
    """Retourne (nombre de lignes, fichier valide en UTF-8). Lecture par blocs."""
    decoder = codecs.getincrementaldecoder("utf-8")()
    lines = 0
    last_byte = b""
    is_utf8 = True
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            lines += chunk.count(b"\n")
            last_byte = chunk[-1:]
            if is_utf8:
                try:
                    decoder.decode(chunk)
                except UnicodeDecodeError:
                    is_utf8 = False
    if last_byte not in (b"", b"\n"):
        lines += 1  # dernière ligne sans saut de ligne final
    if is_utf8:
        try:
            decoder.decode(b"", final=True)
        except UnicodeDecodeError:
            is_utf8 = False
    return lines, is_utf8


def inspect_header(path, delimiter, has_header=True):
    """Retourne (liste des colonnes de la première ligne utile, observations)."""
    notes = []
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
        sample = fh.read(SNIFF_BYTES)
    non_empty = [line for line in sample.splitlines() if line.strip()]
    first_line = non_empty[0] if non_empty else ""
    if sample.lstrip("\r\n") != sample:
        notes.append("ligne vide en debut de fichier")

    if delimiter is None:
        try:
            delimiter = csv.Sniffer().sniff(sample, delimiters=",;|\t").delimiter
        except csv.Error:
            delimiter = ","
            notes.append("separateur non detecte, virgule supposee")

    header = next(csv.reader([first_line], delimiter=delimiter), [])
    if not has_header:
        return header, notes
    if any(not col.strip() for col in header):
        notes.append("nom de colonne vide dans l'en-tete")
    if len(set(header)) != len(header):
        notes.append("noms de colonnes dupliques")
    return header, notes


def inspect_file(path):
    name = os.path.basename(path)
    ext = os.path.splitext(name)[1].lower()
    fmt = KNOWN_FORMATS.get(ext, "Inconnu")
    size = os.path.getsize(path)

    row = {
        "name": name,
        "format": fmt,
        "size": size,
        "lines": "n/a",
        "columns": "n/a",
        "sha256": sha256_of(path),
        "notes": [],
    }
    notes = row["notes"]

    if fmt == "Inconnu":
        notes.append("extension non reconnue")
    if size == 0:
        notes.append("fichier vide")
        return row
    if fmt == "Parquet":
        notes.append("format binaire, structure non lue")
        return row

    lines, is_utf8 = count_lines_and_check_utf8(path)
    row["lines"] = lines
    if not is_utf8:
        notes.append("encodage non UTF-8")

    if ext in FIXED_DELIMITERS:
        header, header_notes = inspect_header(path, FIXED_DELIMITERS[ext], HAS_HEADER[ext])
        row["columns"] = len(header)
        notes.extend(header_notes)
    return row


def collect(directories, recursive):
    for directory in directories:
        if not os.path.isdir(directory):
            raise SystemExit(f"dossier introuvable : {directory}")
        if recursive:
            for root, _, files in os.walk(directory):
                for name in sorted(files):
                    yield os.path.join(root, name)
        else:
            for name in sorted(os.listdir(directory)):
                path = os.path.join(directory, name)
                if os.path.isfile(path):
                    yield path


def render_markdown(rows):
    out = [
        "| Fichier | Format | Taille (o) | Lignes | Colonnes | SHA-256 | Observations |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for r in rows:
        observations = "; ".join(r["notes"]) or "-"
        out.append(
            f"| {r['name']} | {r['format']} | {r['size']} | {r['lines']} "
            f"| {r['columns']} | {r['sha256']} | {observations} |"
        )
    return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inventaire lecture seule de fichiers sources.")
    parser.add_argument("directories", nargs="+", help="dossiers à inventorier")
    parser.add_argument("--recursive", action="store_true", help="parcourir les sous-dossiers")
    args = parser.parse_args(argv)

    rows = [inspect_file(path) for path in collect(args.directories, args.recursive)]
    print(render_markdown(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
