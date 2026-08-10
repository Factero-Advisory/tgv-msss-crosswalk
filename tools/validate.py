#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validation du depot : integrite des donnees, coherence des pages, balises SEO.

Utilise uniquement la bibliotheque standard. Lance par la CI et executable en local :

    python tools/validate.py
"""
import json, csv, os, re, sys, html.parser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://facterocanada.github.io/tgv-msss-crosswalk"
err, warn = [], []


def E(m): err.append(m)
def W(m): warn.append(m)


def p(*a): return os.path.join(ROOT, *a)


# ---------------------------------------------------------------- 1. Donnees
idx = json.load(open(p("data", "index.json"), encoding="utf-8"))
crit = json.load(open(p("data", "tgv", "tgv-criteres.json"), encoding="utf-8"))
S = idx["statistiques"]

if len(crit) != S["criteres_tgv_total"]:
    E(f"index.json annonce {S['criteres_tgv_total']} criteres, le fichier en contient {len(crit)}")

refs = [c["ref"] for c in crit]
if len(refs) != len(set(refs)):
    dup = [r for r in set(refs) if refs.count(r) > 1]
    E(f"identifiants TGV en double : {dup[:8]}")
for c in crit:
    if not c["texte"].strip():
        E(f"critere {c['ref']} sans texte")
    if not re.match(r"^[A-Z]{1,2}\d", c["ref"]):
        W(f"identifiant TGV inhabituel : {c['ref']}")

VALID_REL = {"equivalent", "tgv_plus_etroit", "tgv_plus_large", "recoupement_partiel"}
known = set(refs)
total = 0
rel_counts = {}
for r in idx["referentiels"]:
    f = p("data", "crosswalks", f"crosswalk-{r['slug']}.json")
    if not os.path.exists(f):
        E(f"crosswalk manquant : {r['slug']}"); continue
    doc = json.load(open(f, encoding="utf-8"))
    cs = doc["correspondances"]
    total += len(cs)
    if len(cs) != r["correspondances"]:
        E(f"{r['slug']} : index annonce {r['correspondances']}, fichier en contient {len(cs)}")
    seen = set()
    for c in cs:
        if c["tgv_ref"] not in known:
            E(f"{r['slug']} : critere TGV inconnu {c['tgv_ref']}")
        if c["relation"] not in VALID_REL:
            E(f"{r['slug']} : relation invalide '{c['relation']}' sur {c['tgv_ref']}")
        if not c["justification"].strip():
            E(f"{r['slug']} : justification vide sur {c['tgv_ref']} -> {c['cible_ref']}")
        if not c["cible_intitule"].strip():
            W(f"{r['slug']} : intitule de controle vide sur {c['cible_ref']}")
        # Identite reelle d'une correspondance : critere source + controle cible.
        # Le controle cible se distingue par sa reference ET son intitule : dans
        # certains referentiels (NIST SP 800-66), plusieurs controles distincts
        # partagent la reference de section HIPAA dont ils dependent.
        k = (c["tgv_ref"], c["cible_ref"], c["cible_intitule"])
        if k in seen:
            E(f"{r['slug']} : correspondance en double {k[:2]}")
        seen.add(k)
        rel_counts[c["relation"]] = rel_counts.get(c["relation"], 0) + 1
    # le CSV doit refleter le JSON
    cf = p("data", "crosswalks", f"crosswalk-{r['slug']}.csv")
    if not os.path.exists(cf):
        E(f"CSV manquant : {r['slug']}")
    else:
        n = sum(1 for _ in csv.DictReader(open(cf, encoding="utf-8-sig")))
        if n != len(cs):
            E(f"{r['slug']} : CSV {n} lignes vs JSON {len(cs)}")

if total != S["correspondances_total"]:
    E(f"total des correspondances : index {S['correspondances_total']}, somme reelle {total}")
if rel_counts != S["relations"]:
    E(f"repartition des relations incoherente : index {S['relations']} vs reel {rel_counts}")

# CSV consolide
cons = p("data", "toutes-correspondances.csv")
n = sum(1 for _ in csv.DictReader(open(cons, encoding="utf-8-sig")))
if n != total:
    E(f"toutes-correspondances.csv : {n} lignes, attendu {total}")

couverts = set()
for r in idx["referentiels"]:
    doc = json.load(open(p("data", "crosswalks", f"crosswalk-{r['slug']}.json"), encoding="utf-8"))
    couverts |= {c["tgv_ref"] for c in doc["correspondances"]}
if len(couverts) != S["criteres_tgv_couverts"]:
    E(f"criteres couverts : index {S['criteres_tgv_couverts']}, reel {len(couverts)}")


# ---------------------------------------------------------------- 2. Pages
class Meta(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self._t = False
        self.desc = None
        self.canon = None
        self.hreflang = []
        self.jsonld = []
        self._ld = False
        self.h1 = 0
        self._h1 = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._t = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href")
        elif tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang.append((a["hreflang"], a.get("href")))
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False
        if tag == "script":
            self._ld = False

    def handle_data(self, d):
        if self._t:
            self.title = (self.title or "") + d
        if self._ld:
            self.jsonld.append(d)


pages = []
for dirpath, _dn, fn in os.walk(ROOT):
    if ".git" in dirpath:
        continue
    for f in fn:
        if f.endswith(".html"):
            pages.append(os.path.join(dirpath, f))

for f in sorted(pages):
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    m = Meta()
    m.feed(open(f, encoding="utf-8").read())
    if not m.title:
        E(f"{rel} : <title> absent")
    elif len(m.title) > 70:
        W(f"{rel} : title de {len(m.title)} caracteres (>70, risque de troncature)")
    if not m.desc:
        E(f"{rel} : meta description absente")
    elif not (50 <= len(m.desc) <= 320):
        W(f"{rel} : meta description de {len(m.desc)} caracteres")
    if not m.canon:
        E(f"{rel} : lien canonique absent")
    elif not m.canon.startswith(SITE):
        E(f"{rel} : canonique hors domaine ({m.canon})")
    if m.h1 != 1:
        E(f"{rel} : {m.h1} balise(s) h1, attendu exactement 1")
    langs = {h for h, _ in m.hreflang}
    if not {"fr", "en"} <= langs:
        E(f"{rel} : hreflang incomplet ({sorted(langs)})")
    for blob in m.jsonld:
        try:
            json.loads(blob)
        except json.JSONDecodeError as ex:
            E(f"{rel} : JSON-LD invalide ({ex})")

# ---------------------------------------------------------------- 3. Fichiers requis
for f in ["README.md", "LICENSE", "NOTICE.md", "CITATION.cff",
          "robots.txt", "sitemap.xml", "llms.txt", "llms-full.txt", ".gitignore",
          "checksums/SHA512SUMS", "checksums/manifest.json",
          "assets/fonts/epilogue-latin.woff2", "assets/fonts/OFL.txt",
          "xlsx/Matrice-correspondance-TGV-13-referentiels.xlsx"]:
    if not os.path.exists(p(f)):
        E(f"fichier requis absent : {f}")

# Le site est servi sur l'URL GitHub Pages du projet. Le domaine
# certification-tgv.ca reste dedie a la page de services de Factero : aucun
# fichier CNAME ne doit etre present, sinon Pages revendiquerait le domaine.
if os.path.exists(p("CNAME")):
    E("un fichier CNAME est present : il detournerait certification-tgv.ca vers ce site")

sm = open(p("sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
if len(locs) != len(set(locs)):
    E("URL en double dans sitemap.xml")
for loc in locs:
    sub = loc[len(SITE):].lstrip("/")
    cand = p(sub) if sub else p("index.html")
    if sub.endswith("/"):
        cand = p(sub, "index.html")
    if not os.path.exists(cand):
        E(f"sitemap : {loc} ne correspond a aucun fichier ({sub or 'index.html'})")

# ---------------------------------------------------------------- Rapport
print(f"Criteres TGV            : {len(crit)}")
print(f"Criteres couverts       : {len(couverts)}")
print(f"Referentiels            : {len(idx['referentiels'])}")
print(f"Correspondances         : {total}")
print(f"Relations               : {rel_counts}")
print(f"Pages HTML              : {len(pages)}")
print(f"URL au sitemap          : {len(locs)}")
print()
for m in warn:
    print(f"AVERTISSEMENT : {m}")
for m in err:
    print(f"ERREUR : {m}")
print()
if err:
    print(f"ECHEC : {len(err)} erreur(s), {len(warn)} avertissement(s)")
    sys.exit(1)
print(f"SUCCES : validation complete, {len(warn)} avertissement(s)")
