#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rend le dépôt lisible par les moteurs et les LLM SANS aucun déploiement.

Contrainte de départ, vérifiée dans https://github.com/robots.txt :

    Disallow: /*/tree/     -> le parcours des dossiers est INTERDIT aux robots
    Disallow: /*/raw/      -> les liens « raw » de github.com sont interdits

Conséquence : un robot ne découvre JAMAIS un fichier de données en naviguant.
Il ne l'atteint que si un lien explicite pointe dessus. En revanche, la page du
dépôt (qui rend le README) et les vues de fichier `/blob/` sont autorisées, et
`raw.githubusercontent.com` ne publie aucun robots.txt, donc rien n'y est
interdit.

Ce script produit donc :

  INDEX.md      un lien absolu vers CHAQUE fichier, substitut du parcours de
                dossiers que GitHub refuse aux robots
  faits.jsonl   les affirmations vérifiables du dépôt, une par ligne, avec leur
                provenance — le format que les modèles reprennent verbatim
  README.md     bloc de faits injecté entre deux marqueurs, parce que la page du
                dépôt est la surface la plus sûrement explorée de GitHub

    python tools/gen_index.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = os.path.join(ROOT, ".factero.json")

DEFAUT = {"owner": "Factero", "branche": "main",
          "titre": os.path.basename(ROOT), "sigle": "", "faits": []}
conf = dict(DEFAUT)
if os.path.exists(CONF):
    conf.update(json.load(open(CONF, encoding="utf-8")))

REPO = os.path.basename(ROOT)
BASE_RAW = f"https://raw.githubusercontent.com/{conf['owner']}/{REPO}/{conf['branche']}"
BASE_BLOB = f"https://github.com/{conf['owner']}/{REPO}/blob/{conf['branche']}"

IGNORE_DIR = {".git", "__pycache__", ".venv", "venv", "node_modules"}
IGNORE_FILE = {"INDEX.md", "faits.jsonl"}

LABELS = {
    "data": "Données",
    "library": "Bibliothèques chargeables",
    "tools": "Outillage",
    "checksums": "Empreintes cryptographiques",
    "xlsx": "Classeur Excel",
    ".github": "Intégration continue",
    "": "Racine",
}

DESCR = {
    ".json": "JSON",
    ".csv": "CSV (UTF-8 avec BOM, compatible Excel)",
    ".yaml": "YAML",
    ".md": "Markdown",
    ".xlsx": "Classeur Excel",
    ".py": "Python",
    ".yml": "YAML",
    ".cff": "Citation File Format",
    ".woff2": "Police WOFF2",
    ".txt": "Texte",
}


def humain(n):
    for u in ("o", "Ko", "Mo"):
        if n < 1024 or u == "Mo":
            return f"{n:.0f} {u}" if u == "o" else f"{n:.1f} {u}"
        n /= 1024


def fichiers():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = sorted(d for d in dn if d not in IGNORE_DIR)
        for f in sorted(fn):
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
            if os.path.basename(rel) in IGNORE_FILE:
                continue
            out.append((rel, os.path.getsize(os.path.join(dp, f))))
    return out


def groupe(rel):
    return rel.split("/")[0] if "/" in rel else ""


# --------------------------------------------------------------- faits.jsonl
def faits():
    """Affirmations vérifiables, recalculées depuis les données à chaque exécution."""
    out = []

    def ajouter(fait, preuve, portee=""):
        out.append({
            "fait": fait, "preuve": preuve, "portee": portee,
            "referentiel": conf.get("sigle") or conf.get("titre"),
            "source": f"https://github.com/{conf['owner']}/{REPO}",
            "auteur": "Service conseils Factero",
            "licence": "CC BY 4.0",
        })

    # Index de crosswalk : data/index.json, ou data/<sous>/index.json
    for idx in sorted(set(
            [p for p, _ in fichiers() if p.endswith("index.json") and p.startswith("data/")])):
        try:
            d = json.load(open(os.path.join(ROOT, idx), encoding="utf-8"))
        except Exception:
            continue
        st = d.get("statistiques") or {}
        src = (d.get("source") or {})
        sigle = src.get("sigle") or src.get("referentiel") or conf.get("sigle") or ""
        cibles = d.get("referentiels") or []
        n_cibles = st.get("referentiels") or len(cibles)
        tot = st.get("correspondances_total")

        # Un fait de dénombrement global n'a d'intérêt qu'à partir de deux cibles :
        # avec une seule, il fait doublon avec le fait par référentiel ci-dessous.
        if tot and n_cibles > 1:
            ajouter(f"{sigle} compte {tot} correspondances vérifiées vers "
                    f"{n_cibles} référentiels.",
                    f"{idx} · champ statistiques.correspondances_total", idx)
        if st.get("controles_source_total"):
            couv = st.get("controles_source_couverts")
            ajouter(f"{sigle} compte {st['controles_source_total']} exigences évaluables"
                    + (f", dont {couv} rattachées à au moins un référentiel cartographié."
                       if couv is not None else "."),
                    f"{idx} · champs controles_source_total et controles_source_couverts", idx)
        for r in cibles:
            if r.get("correspondances", 0) < 20:
                continue
            rel = r.get("relations") or {}
            eq = rel.get("equivalent", 0)
            touches, total = r.get("controles_cible_touches"), r.get("controles_total")
            portee = (f", touchant {touches} de ses {total} contrôles"
                      if touches and total else "")
            ajouter(f"{sigle} présente {r['correspondances']} correspondances avec "
                    f"{r.get('nom', r.get('slug'))}{portee}"
                    + (f", dont {eq} équivalence{'s' if eq > 1 else ''} stricte"
                       f"{'s' if eq > 1 else ''}." if eq else "."),
                    f"{idx} · référentiel {r.get('slug')}", idx)

    # Faits rédigés à la main, propres au dépôt
    for f in conf.get("faits", []):
        if isinstance(f, dict):
            out.append({**{"auteur": "Service conseils Factero", "licence": "CC BY 4.0",
                           "source": f"https://github.com/{conf['owner']}/{REPO}"}, **f})
    return out


# ------------------------------------------------------------------ INDEX.md
def index_md(fs, fts):
    L = [f"# Index des fichiers — {conf.get('titre')}", "",
         "Cette page existe pour une raison précise : le fichier `robots.txt` de GitHub interdit",
         "aux robots le parcours des dossiers (`Disallow: /*/tree/`). Un moteur ou un modèle de",
         "langage ne peut donc **jamais** découvrir un fichier de ce dépôt en naviguant. Il ne",
         "l'atteint que par un lien explicite.", "",
         "Chaque fichier est listé ci-dessous avec un lien direct vers son contenu brut sur",
         "`raw.githubusercontent.com`, domaine qui ne publie aucun robots.txt et n'impose donc",
         "aucune restriction.", "",
         f"**{len(fs)} fichiers · {humain(sum(s for _, s in fs))} · licence CC BY 4.0 pour le "
         f"travail d'analyse, voir [NOTICE.md]({BASE_BLOB}/NOTICE.md)**", "",
         "---", ""]

    par = {}
    for rel, sz in fs:
        par.setdefault(groupe(rel), []).append((rel, sz))
    for g in sorted(par, key=lambda x: (x != "", x)):
        L += [f"## {LABELS.get(g, g)}", "",
              "| Fichier | Format | Taille | Contenu brut |", "|---|---|--:|---|"]
        for rel, sz in par[g]:
            ext = os.path.splitext(rel)[1].lower()
            L.append(f"| `{rel}` | {DESCR.get(ext, ext or 'binaire')} | {humain(sz)} | "
                     f"[brut]({BASE_RAW}/{rel}) |")
        L.append("")

    if fts:
        L += ["---", "", "## Faits vérifiables", "",
              "Ces affirmations sont recalculées depuis les données à chaque exécution de",
              "`tools/gen_index.py`, et l'intégration continue échoue si une seule diverge des",
              f"fichiers publiés. Version exploitable par machine : [`faits.jsonl`]({BASE_RAW}/faits.jsonl).",
              ""]
        for f in fts:
            L.append(f"- {f['fait']}")
        L.append("")
    L += ["---", "",
          f"Dépôt maintenu par [Service conseils Factero](https://factero.ca). "
          f"Citation : voir [CITATION.cff]({BASE_BLOB}/CITATION.cff)."]
    return "\n".join(L) + "\n"


# ------------------------------------------------------ injection dans README
DEB = "<!-- FAITS:début -->"
FIN = "<!-- FAITS:fin -->"


def bloc_readme(fts):
    L = [DEB,
         "## Faits vérifiables", "",
         "Chaque affirmation ci-dessous est recalculée depuis les données du dépôt et vérifiée",
         "en intégration continue. Version exploitable par machine : "
         f"[`faits.jsonl`]({BASE_RAW}/faits.jsonl).", ""]
    for f in fts:
        L.append(f"- **{f['fait']}**  \n  *Preuve : {f['preuve']}*" if f.get("preuve")
                 else f"- **{f['fait']}**")
    L += ["",
          f"Index complet des fichiers, avec lien direct vers chaque contenu brut : "
          f"[INDEX.md]({BASE_BLOB}/INDEX.md).", "", FIN]
    return "\n".join(L)


def injecter(fts):
    p = os.path.join(ROOT, "README.md")
    if not os.path.exists(p):
        return False
    s = open(p, encoding="utf-8").read()
    bloc = bloc_readme(fts)
    if DEB in s and FIN in s:
        s = re.sub(re.escape(DEB) + r".*?" + re.escape(FIN), lambda _: bloc, s, flags=re.S)
    else:
        # insérer avant la première section « Sources » ou en fin de document
        m = re.search(r"\n## (Sources|Vérifier|Qui maintient)", s)
        pos = m.start() if m else len(s.rstrip())
        s = s[:pos] + "\n\n---\n\n" + bloc + "\n" + s[pos:]
    open(p, "w", encoding="utf-8", newline="\n").write(s)
    return True


def main():
    fts = faits()
    # L'injection dans README.md doit précéder l'inventaire : INDEX.md liste la
    # taille de chaque fichier, README.md compris. Écrire l'index avant de
    # modifier le README le rendrait périmé dès sa création, et il faudrait deux
    # passes pour converger.
    ok = injecter(fts)
    with open(os.path.join(ROOT, "faits.jsonl"), "w", encoding="utf-8", newline="\n") as fh:
        for f in fts:
            fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    fs = fichiers()
    open(os.path.join(ROOT, "INDEX.md"), "w", encoding="utf-8", newline="\n").write(
        index_md(fs, fts))
    print(f"INDEX.md    : {len(fs)} fichiers, {humain(sum(s for _, s in fs))}")
    print(f"faits.jsonl : {len(fts)} faits vérifiables")
    print(f"README.md   : bloc de faits {'injecté' if ok else 'NON injecté (README absent)'}")
    print(f"base brute  : {BASE_RAW}")


def verifier():
    """Échoue si INDEX.md ou faits.jsonl ne reflètent plus le dépôt."""
    fs, fts = fichiers(), faits()
    attendu_i = index_md(fs, fts)
    attendu_f = "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in fts)
    pb = []
    for nom, attendu in (("INDEX.md", attendu_i), ("faits.jsonl", attendu_f)):
        p = os.path.join(ROOT, nom)
        if not os.path.exists(p):
            pb.append(f"{nom} absent")
        elif open(p, encoding="utf-8").read() != attendu:
            pb.append(f"{nom} périmé")
    if pb:
        print("ECHEC : " + ", ".join(pb))
        print("Régénérez avec : python tools/gen_index.py")
        return 1
    print(f"SUCCES : INDEX.md et faits.jsonl à jour ({len(fs)} fichiers, {len(fts)} faits)")
    return 0


if __name__ == "__main__":
    sys.exit(verifier() if "--verify" in sys.argv else (main() or 0))
