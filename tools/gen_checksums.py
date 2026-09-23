#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere les manifestes d'empreintes cryptographiques du depot.

Produit, dans checksums/ :
  SHA512SUMS      format coreutils, verifiable par `sha512sum -c`
  SHA256SUMS      idem, `sha256sum -c`
  MD5SUMS         idem, `md5sum -c`  (LEGACY : MD5 est casse, cf. checksums/README.md)
  manifest.json   metadonnees par fichier (taille + 4 empreintes)

Les fichiers sont lus en binaire et les empreintes calculees sur les octets exacts
du depot. Aucune dependance externe.

    python tools/gen_checksums.py
"""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "checksums")

# Repertoires jamais integres au manifeste
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache", "site_out"}
# Fichiers jamais integres : les manifestes eux-memes (auto-reference) et leurs signatures
SKIP_FILES = {"SHA512SUMS", "SHA256SUMS", "MD5SUMS", "manifest.json",
              "SHA512SUMS.asc", "SHA512SUMS.sig", "SHA512SUMS.pem"}

ALGOS = ("sha512", "sha256", "md5", "blake2b")


def iter_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
            if rel.startswith("checksums/") and fn in SKIP_FILES:
                continue
            yield rel, full


def digests(path):
    h = {a: (hashlib.blake2b(digest_size=64) if a == "blake2b" else hashlib.new(a))
         for a in ALGOS}
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            for x in h.values():
                x.update(chunk)
    return {a: h[a].hexdigest() for a in ALGOS}


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    entries = []
    for rel, full in iter_files():
        d = digests(full)
        entries.append({"path": rel, "bytes": os.path.getsize(full), **d})

    entries.sort(key=lambda e: e["path"])

    # Manifestes au format coreutils : "<empreinte>  <chemin>" (deux espaces, mode binaire *)
    for algo, fname in (("sha512", "SHA512SUMS"), ("sha256", "SHA256SUMS"), ("md5", "MD5SUMS")):
        lines = [f"{e[algo]}  {e['path']}" for e in entries]
        with open(os.path.join(OUTDIR, fname), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")

    total = sum(e["bytes"] for e in entries)
    manifest = {
        "schema": "https://certification-tgv.ca/checksums/manifest.schema.json",
        "repository": "https://github.com/Factero-Advisory/tgv-msss-crosswalk",
        "site": "https://certification-tgv.ca",
        "generator": "tools/gen_checksums.py",
        "algorithms": {
            "sha512": {"status": "recommande", "bits": 512,
                       "note": "Empreinte de reference pour verifier l'integrite."},
            "sha256": {"status": "recommande", "bits": 256,
                       "note": "Compatibilite large de l'ecosysteme."},
            "blake2b": {"status": "moderne", "bits": 512,
                        "note": "RFC 7693. Plus rapide que SHA-2 a securite equivalente."},
            "md5": {"status": "OBSOLETE", "bits": 128,
                    "note": "Casse depuis 2008 (collisions triviales). Fourni uniquement "
                            "pour un controle anti-corruption de transfert. Ne constitue "
                            "AUCUNE garantie de securite ni d'authenticite."},
        },
        "files_count": len(entries),
        "total_bytes": total,
        "files": entries,
    }
    with open(os.path.join(OUTDIR, "manifest.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    print(f"{len(entries)} fichiers empreintes, {total} octets au total")
    print(f"Manifestes ecrits dans {os.path.relpath(OUTDIR, ROOT)}/")
    return 0


def verify():
    """Recalcule et compare au manifeste existant. Code de sortie non nul si ecart."""
    mf = os.path.join(OUTDIR, "manifest.json")
    if not os.path.exists(mf):
        print("ERREUR : checksums/manifest.json absent", file=sys.stderr)
        return 1
    ref = {e["path"]: e for e in json.load(open(mf, encoding="utf-8"))["files"]}
    cur = {rel: full for rel, full in iter_files()}

    problems = []
    for path in sorted(set(ref) | set(cur)):
        if path not in cur:
            problems.append(f"MANQUANT   {path}")
        elif path not in ref:
            problems.append(f"NON SUIVI  {path}")
        else:
            d = digests(cur[path])
            if d["sha512"] != ref[path]["sha512"]:
                problems.append(f"MODIFIE    {path}")

    if problems:
        print(f"ECHEC : {len(problems)} ecart(s) entre le depot et le manifeste\n")
        for p in problems:
            print(" ", p)
        print("\nRegenerez avec : python tools/gen_checksums.py")
        return 1
    print(f"SUCCES : {len(ref)} fichiers conformes au manifeste (SHA-512)")
    return 0


if __name__ == "__main__":
    sys.exit(verify() if "--verify" in sys.argv else main())
