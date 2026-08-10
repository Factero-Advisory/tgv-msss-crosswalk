# -*- coding: utf-8 -*-
# Exporte le referentiel TGV + les 13 crosswalks vers des formats ouverts
# (JSON / CSV / YAML chargeable CISO Assistant) pour le depot public.
import json, csv, re, sys, sqlite3, os
from collections import Counter, defaultdict

OUT = "/code/db/repo_export"
os.makedirs(OUT, exist_ok=True)
conn = sqlite3.connect("/code/db/ciso-assistant.sqlite3"); cur = conn.cursor()

TGV_PREFIX = "urn:intuitem:risk:req_node:tgv-msss-qc-2026"

# ---------- 1. Referentiel TGV ----------
cur.execute("""SELECT urn, ref_id, name, description, assessable, parent_urn
               FROM core_requirementnode WHERE urn LIKE ?""", (TGV_PREFIX + "%",))
rows = cur.fetchall()
byurn = {r[0]: r for r in rows}

FAMILLES = {
 "P":  ("Protection des renseignements personnels", "Personal information protection"),
 "PF": ("Performance", "Performance"),
 "S":  ("Securite", "Security"),
 "T":  ("Technique", "Technical"),
 "I":  ("Interoperabilite", "Interoperability"),
 "IA": ("Intelligence artificielle", "Artificial intelligence"),
 "G":  ("Gouvernance", "Governance"),
}
def famille(ref):
    m = re.match(r"^(IA|PF|[A-Z])", ref or "")
    return m.group(1) if m else "?"

criteria = []
for urn, ref, name, desc, assess, parent in rows:
    if not assess or not ref:
        continue
    texte = (desc or name or "").strip()
    texte = re.sub(r"\s+", " ", texte)
    f = famille(ref)
    criteria.append({
        "ref": ref,
        "famille": f,
        "famille_fr": FAMILLES.get(f, ("Autre", "Other"))[0],
        "famille_en": FAMILLES.get(f, ("Autre", "Other"))[1],
        "texte": texte,
        "urn": urn,
    })
criteria.sort(key=lambda c: (c["famille"], c["ref"]))

json.dump(criteria, open(f"{OUT}/tgv-criteres.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
with open(f"{OUT}/tgv-criteres.csv", "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["ref", "famille", "famille_fr", "texte"])
    for c in criteria:
        w.writerow([c["ref"], c["famille"], c["famille_fr"], c["texte"]])

fam_counts = Counter(c["famille"] for c in criteria)
sys.stderr.write(f"RESULT TGV: {len(criteria)} criteres evaluables | familles {dict(fam_counts)}\n")

# ---------- 2. Crosswalks ----------
CW = json.load(open("/code/db/tgv_mappings_export.json", encoding="utf-8"))
META = {
 "soc2-2017":            ("soc2-type2", "SOC 2 (Trust Services Criteria, AICPA 2017)", "Attestation"),
 "nist-sp-800-66-rev2":  ("hipaa-nist-800-66", "NIST SP 800-66 Rev. 2 (HIPAA Security Rule)", "Reglementation"),
 "iso27001-2022":        ("iso-27001-2022", "ISO/IEC 27001:2022", "Certification"),
 "iso27701-2025":        ("iso-27701-2025", "ISO/IEC 27701:2025", "Certification"),
 "iso42001-2023":        ("iso-42001-2023", "ISO/IEC 42001:2023", "Certification"),
 "bsi-c5-2020":          ("bsi-c5-2020", "BSI C5:2020", "Attestation"),
 "gdpr":                 ("rgpd-gdpr", "RGPD / GDPR (UE 2016/679)", "Reglementation"),
 "hitrust-csf-v11":      ("hitrust-csf-v11", "HITRUST CSF v11", "Certification"),
 "annex-technical-and-methodological-requirements-nis2": ("nis2", "Directive NIS2 (annexe technique, guidance ENISA)", "Reglementation"),
 "ccb-cff-2023-03-01":   ("ccb-cyberfundamentals", "CCB CyberFundamentals Framework 2023", "Cadre national"),
 "ai-act":               ("eu-ai-act", "Reglement europeen sur l'IA (EU AI Act)", "Reglementation"),
 "hds-v2023-a":          ("hds-v2", "Hebergement de Donnees de Sante (HDS) v2.0", "Certification"),
 "iso22301-2019":        ("iso-22301-2019", "ISO 22301:2019", "Certification"),
}
REL_FR = {"equal": "equivalent", "subset": "tgv_plus_etroit",
          "superset": "tgv_plus_large", "intersect": "recoupement_partiel"}

index, all_pairs = [], []
for f in CW:
    frag = f["target_fw_urn"].split(":framework:")[-1]
    if frag not in META:
        sys.stderr.write(f"RESULT IGNORE framework inconnu: {frag}\n"); continue
    slug, label, cat = META[frag]
    pairs = []
    for r in f["pairs"]:
        cible_txt = re.sub(r"\s+", " ", (r["tgt_name"] or r.get("tgt_desc") or "")).strip()
        pairs.append({
            "tgv_ref": r["tgv_ref"],
            "cible_ref": (r.get("tgt_dref") or r["tgt_ref"] or ""),
            "cible_intitule": cible_txt,
            "relation": REL_FR.get(r["rel"], r["rel"]),
            "justification": (r.get("annotation") or "").strip(),
        })
        all_pairs.append(dict(pairs[-1], referentiel=slug))
    pairs.sort(key=lambda p: (p["tgv_ref"], p["cible_ref"]))
    doc = {
        "referentiel": {"slug": slug, "nom": label, "categorie": cat,
                        "controles_total": f["target_total_controls"]},
        "source": {"referentiel": "TGV", "nom": "Trousse globale de verification (MSSS Quebec)"},
        "statistiques": {
            "correspondances": len(pairs),
            "criteres_tgv": len({p["tgv_ref"] for p in pairs}),
            "controles_cible_touches": len({r["tgt_urn"] for r in f["pairs"]}),
            "relations": dict(Counter(p["relation"] for p in pairs)),
        },
        "correspondances": pairs,
    }
    json.dump(doc, open(f"{OUT}/crosswalk-{slug}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    with open(f"{OUT}/crosswalk-{slug}.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["tgv_ref", "cible_ref", "cible_intitule", "relation", "justification"])
        for p in pairs:
            w.writerow([p["tgv_ref"], p["cible_ref"], p["cible_intitule"], p["relation"], p["justification"]])
    index.append({"slug": slug, "nom": label, "categorie": cat,
                  "correspondances": len(pairs),
                  "criteres_tgv": doc["statistiques"]["criteres_tgv"],
                  "controles_cible_touches": doc["statistiques"]["controles_cible_touches"],
                  "controles_total": f["target_total_controls"],
                  "relations": doc["statistiques"]["relations"]})

index.sort(key=lambda x: -x["correspondances"])
couverts = sorted({p["tgv_ref"] for p in all_pairs})
json.dump({
    "titre": "Correspondances TGV vers referentiels internationaux",
    "source": {
        "referentiel": "Trousse globale de verification (TGV)",
        "editeur": "Ministere de la Sante et des Services sociaux du Quebec",
        "publication": "24-715-38W", "isbn": "978-2-550-97589-2",
        "url": "https://publications.msss.gouv.qc.ca/msss/document-003757/",
    },
    "statistiques": {
        "criteres_tgv_total": len(criteria),
        "criteres_tgv_couverts": len(couverts),
        "referentiels": len(index),
        "correspondances_total": sum(i["correspondances"] for i in index),
        "relations": dict(Counter(p["relation"] for p in all_pairs)),
    },
    "referentiels": index,
}, open(f"{OUT}/index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# CSV consolide (toutes correspondances)
with open(f"{OUT}/toutes-correspondances.csv", "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["referentiel", "tgv_ref", "cible_ref", "cible_intitule", "relation", "justification"])
    for p in sorted(all_pairs, key=lambda x: (x["referentiel"], x["tgv_ref"])):
        w.writerow([p["referentiel"], p["tgv_ref"], p["cible_ref"], p["cible_intitule"],
                    p["relation"], p["justification"]])

sys.stderr.write(f"RESULT crosswalks: {len(index)} referentiels, "
                 f"{sum(i['correspondances'] for i in index)} correspondances, "
                 f"{len(couverts)}/{len(criteria)} criteres TGV couverts\n")
sys.stderr.write(f"RESULT fichiers ecrits dans {OUT}: {len(os.listdir(OUT))}\n")
