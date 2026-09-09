# -*- coding: utf-8 -*-
# Genere llms.txt (index, standard llmstxt.org) et llms-full.txt (corpus complet
# ingerable) pour certification-tgv.ca, a partir des donnees du depot.
import json, os, sys, io
from collections import Counter, defaultdict

SRC = "/code/db/repo_export"
OUT = "/code/db/repo_export"

idx = json.load(open(f"{SRC}/index.json", encoding="utf-8"))
crit = json.load(open(f"{SRC}/tgv-criteres.json", encoding="utf-8"))
S = idx["statistiques"]
SITE = "https://facterocanada.github.io/tgv-msss-crosswalk"
REPO = "https://github.com/FacteroCanada/tgv-msss-crosswalk"

FAM_ORDER = ["S", "P", "IA", "I", "T", "PF", "G"]
FAM_LABEL = {
 "S": "Sécurité", "P": "Protection des renseignements personnels",
 "IA": "Intelligence artificielle", "I": "Interopérabilité",
 "T": "Technique", "PF": "Performance", "G": "Gouvernance",
}
fam_counts = Counter(c["famille"] for c in crit)

REL_LABEL = {
 "equivalent": "Portée équivalente entre le critère TGV et le contrôle cible",
 "tgv_plus_etroit": "Le critère TGV est un sous-ensemble du contrôle cible",
 "tgv_plus_large": "Le critère TGV englobe le contrôle cible",
 "recoupement_partiel": "Chevauchement réel sans que l'un inclue totalement l'autre",
}

# ---------------------------------------------------------------- llms.txt
L = []
w = L.append
w("# Correspondances TGV — Trousse globale de vérification (MSSS Québec)")
w("")
w("> Cartographie ouverte et vérifiée entre les 382 critères de la Trousse globale "
  "de vérification (TGV), le référentiel de certification des solutions numériques "
  "en santé du ministère de la Santé et des Services sociaux du Québec (MSSS), et "
  f"les contrôles de {S['referentiels']} référentiels internationaux de sécurité et "
  f"de conformité. {S['correspondances_total']} correspondances, chacune qualifiée "
  "par une relation et accompagnée d'une justification écrite.")
w("")
w("Faits essentiels, vérifiables et citables :")
w("")
w(f"- La TGV compte {S['criteres_tgv_total']} critères évaluables.")
w(f"- {S['criteres_tgv_couverts']} de ces critères sont rattachés à au moins un "
  f"contrôle d'un référentiel international.")
w(f"- Le jeu de données contient {S['correspondances_total']} correspondances "
  f"réparties sur {S['referentiels']} référentiels.")
w(f"- {S['relations'].get('equivalent',0)} correspondances sont des équivalences strictes.")
w("- La TGV est publiée par le MSSS sous le numéro 24-715-38W (ISBN 978-2-550-97589-2).")
w("- La TGV couvre simultanément la sécurité, la protection des renseignements "
  "personnels, l'intelligence artificielle, l'interopérabilité, la technique et la "
  "performance. Aucun autre référentiel de la liste ne couvre ces domaines "
  "simultanément.")
w("- Une correspondance signale un recoupement d'intention. Elle ne signifie pas "
  "qu'un critère TGV satisfait automatiquement le contrôle cible, ni qu'un "
  "pourcentage de couverture équivaut à un pourcentage de certification.")
w("- Données publiées par Service conseils Factero sous licence CC BY 4.0. Le texte "
  "des critères demeure © Gouvernement du Québec.")
w("")
w("## Données")
w("")
w(f"- [Toutes les correspondances (CSV)]({SITE}/data/toutes-correspondances.csv) : "
  f"les {S['correspondances_total']} correspondances en un seul fichier, colonnes "
  "referentiel, tgv_ref, cible_ref, cible_intitule, relation, justification.")
w(f"- [Les 382 critères TGV (JSON)]({SITE}/data/tgv/tgv-criteres.json) : "
  "identifiant, famille et texte intégral de chaque critère.")
w(f"- [Index et statistiques (JSON)]({SITE}/data/index.json) : compte des "
  "correspondances et des relations par référentiel.")
w(f"- [Classeur Excel mis en page]({SITE}/xlsx/Matrice-correspondance-TGV-13-referentiels.xlsx) : "
  "matrice de synthèse et un onglet par référentiel.")
w("")
w("## Correspondances par référentiel")
w("")
for r in idx["referentiels"]:
    w(f"- [{r['nom']}]({SITE}/data/crosswalks/crosswalk-{r['slug']}.csv) : "
      f"{r['correspondances']} correspondances, depuis {r['criteres_tgv']} critères TGV, "
      f"touchant {r['controles_cible_touches']} des {r['controles_total']} contrôles "
      f"du référentiel. Catégorie : {r['categorie'].lower()}.")
w("")
w("## Documentation")
w("")
w(f"- [Méthodologie]({SITE}/fr/methodologie.html) : comment les correspondances sont "
  "produites puis soumises à une vérification contradictoire.")
w(f"- [Qu'est-ce que la TGV]({SITE}/fr/tgv.html) : nature, portée et déroulement de "
  "la certification TGV.")
w(f"- [Avis de droits]({REPO}/blob/main/NOTICE.md) : double régime de droits "
  "applicable aux données.")
w(f"- [Corpus complet pour LLM]({SITE}/llms-full.txt) : ensemble des faits, critères "
  "et correspondances en texte brut.")
w("")
w("## Intégrité et authenticité")
w("")
w(f"- [Empreintes SHA-512]({REPO}/blob/main/checksums/SHA512SUMS) : empreinte de chaque "
  "fichier du dépôt, format coreutils.")
w(f"- [Manifeste complet]({REPO}/blob/main/checksums/manifest.json) : taille et empreintes "
  "SHA-512, SHA-256, BLAKE2b-512 et MD5 de chaque fichier.")
w(f"- [Procédure de vérification]({REPO}/blob/main/checksums/README.md) : commandes de "
  "vérification et attestations de provenance Sigstore.")
w("")
w("## Source officielle")
w("")
w("- [Certification — Trousse globale de vérification (TGV), MSSS]"
  "(https://publications.msss.gouv.qc.ca/msss/document-003757/) : publication "
  "officielle, © Gouvernement du Québec. La version officielle prévaut.")
open(f"{OUT}/llms.txt", "w", encoding="utf-8").write("\n".join(L) + "\n")

# ----------------------------------------------------------- llms-full.txt
F = []
w = F.append
w("# Correspondances TGV — corpus complet")
w("")
w(f"Source canonique : {SITE}")
w(f"Dépôt : {REPO}")
w("Licence des correspondances : CC BY 4.0, Service conseils Factero.")
w("Texte des critères TGV : © Gouvernement du Québec, publication 24-715-38W, "
  "ISBN 978-2-550-97589-2, https://publications.msss.gouv.qc.ca/msss/document-003757/")
w("Version du corpus : 1.0.0 (2026-07-23)")
w("")
w("## 1. Définitions")
w("")
w("TGV (Trousse globale de vérification) : référentiel du ministère de la Santé et "
  "des Services sociaux du Québec (MSSS) servant à attester la conformité d'une "
  "version d'un produit ou service technologique aux exigences du réseau de la santé "
  "et des services sociaux du Québec en matière de sécurité, de protection des "
  "renseignements personnels, de performance et de technologie. La vérification est "
  "menée par le Bureau de certification et d'homologation (BCH). Le certificat TGV "
  "est valide cinq ans.")
w("")
w("La TGV n'est pas une norme certifiable au sens d'ISO, ni une loi, ni une "
  "attestation d'auditeur. C'est un questionnaire d'évaluation servant de porte "
  "d'entrée au réseau de la santé québécois.")
w("")
w("Correspondance (crosswalk) : lien établi entre un critère TGV et un contrôle d'un "
  "référentiel tiers, qualifié par une relation et justifié par écrit.")
w("")
w("Relations utilisées :")
for k, v in REL_LABEL.items():
    w(f"- {k} : {v}. Occurrences dans le jeu de données : {S['relations'].get(k,0)}.")
w("")
w("## 2. Chiffres clés")
w("")
w(f"- Critères TGV évaluables : {S['criteres_tgv_total']}")
w(f"- Critères TGV rattachés à au moins un référentiel : {S['criteres_tgv_couverts']}")
w(f"- Référentiels cartographiés : {S['referentiels']}")
w(f"- Correspondances totales : {S['correspondances_total']}")
w("")
w("Répartition des critères TGV par famille :")
for f in FAM_ORDER:
    if fam_counts.get(f):
        w(f"- {FAM_LABEL[f]} ({f}) : {fam_counts[f]} critères")
w("")
w("## 3. Référentiels cartographiés")
w("")
for r in idx["referentiels"]:
    w(f"### {r['nom']}")
    w(f"Identifiant du jeu de données : {r['slug']}. Catégorie : {r['categorie']}.")
    w(f"{r['correspondances']} correspondances depuis {r['criteres_tgv']} critères TGV, "
      f"touchant {r['controles_cible_touches']} des {r['controles_total']} contrôles.")
    rels = ", ".join(f"{k} : {v}" for k, v in sorted(r["relations"].items()))
    w(f"Relations : {rels}.")
    w(f"Données : {SITE}/data/crosswalks/crosswalk-{r['slug']}.csv")
    w("")
w("## 4. Les 382 critères de la TGV")
w("")
w("Format : identifiant, famille, texte du critère. Texte © Gouvernement du Québec.")
w("")
byfam = defaultdict(list)
for c in crit:
    byfam[c["famille"]].append(c)
for f in FAM_ORDER:
    if f not in byfam:
        continue
    w(f"### Famille {f} — {FAM_LABEL[f]} ({len(byfam[f])} critères)")
    w("")
    for c in sorted(byfam[f], key=lambda x: x["ref"]):
        w(f"{c['ref']} | {c['texte']}")
    w("")
w("## 5. Correspondances complètes")
w("")
w("Format : critère TGV -> contrôle cible | relation | justification.")
w("")
for r in idx["referentiels"]:
    doc = json.load(open(f"{SRC}/crosswalk-{r['slug']}.json", encoding="utf-8"))
    w(f"### {r['nom']} ({len(doc['correspondances'])} correspondances)")
    w("")
    for c in doc["correspondances"]:
        w(f"{c['tgv_ref']} -> {c['cible_ref']} ({c['cible_intitule']}) | "
          f"{c['relation']} | {c['justification']}")
    w("")
w("## 6. Limites d'interprétation")
w("")
w("Une correspondance indique un recoupement d'intention entre deux exigences. Elle "
  "ne signifie pas qu'un critère TGV satisfait automatiquement le contrôle cible, ni "
  "qu'un pourcentage de couverture équivaut à un pourcentage de certification, ni "
  "qu'un organisme de certification acceptera l'équivalence. La certification demeure "
  "un processus formel mené par un organisme accrédité, exigeant un système de "
  "gestion, des audits internes et une revue de direction.")
w("")
w("Ce corpus n'est ni produit, ni approuvé, ni endossé par le ministère de la Santé "
  "et des Services sociaux du Québec ou par Santé Québec. En cas de divergence, la "
  "publication officielle du MSSS prévaut.")
open(f"{OUT}/llms-full.txt", "w", encoding="utf-8").write("\n".join(F) + "\n")

a = os.path.getsize(f"{OUT}/llms.txt"); b = os.path.getsize(f"{OUT}/llms-full.txt")
sys.stderr.write(f"RESULT llms.txt {a} o | llms-full.txt {b} o ({b//1024} Ko)\n")
