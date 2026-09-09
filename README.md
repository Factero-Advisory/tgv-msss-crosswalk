<div align="center">

# Correspondances TGV — Trousse globale de vérification du MSSS

### La cartographie ouverte entre la certification TGV du Québec et 13 référentiels internationaux de sécurité et de conformité

**1302 correspondances vérifiées · 382 critères TGV · 13 référentiels**

[![Licence CC BY 4.0](https://img.shields.io/badge/donn%C3%A9es-CC%20BY%204.0-blue.svg)](LICENSE)
[![Correspondances](https://img.shields.io/badge/correspondances-1302-success.svg)](data/toutes-correspondances.csv)
[![Référentiels](https://img.shields.io/badge/r%C3%A9f%C3%A9rentiels-13-informational.svg)](#les-13-référentiels-cartographiés)
[![Site](https://img.shields.io/badge/site-GitHub%20Pages-orange.svg)](https://factero.github.io/tgv-msss-crosswalk)

**[Site web](https://factero.github.io/tgv-msss-crosswalk)** ·
**[Télécharger le classeur Excel](xlsx/)** ·
**[Méthodologie](#méthodologie-en-bref)** ·
**[English](#english)**

</div>

---

## Le problème que ce dépôt résout

Au Québec, toute solution numérique qui veut se brancher au réseau de la santé
doit passer la **Trousse globale de vérification (TGV)** du ministère de la Santé
et des Services sociaux. C'est 382 critères à documenter avec des preuves.

La question que tout le monde se pose ensuite est toujours la même : *« on a déjà
un SOC 2 / une ISO 27001, est-ce que ça compte ? »*

Personne n'avait publié la réponse. La voici, critère par critère.

Ce dépôt établit la correspondance entre **chacun des 382 critères de la TGV** et
les contrôles de **13 référentiels internationaux**, avec pour chaque lien une
relation qualifiée et une justification écrite.

---

## Les chiffres

| | |
|---|---|
| Critères TGV évaluables | **382** |
| Critères rattachés à au moins un référentiel | **286** |
| Référentiels cartographiés | **13** |
| Correspondances totales | **1302** |
| Dont équivalences strictes | **72** |

**Répartition des relations**

| Relation | Nombre | Signification |
|---|---:|---|
| TGV plus étroit | 642 | Le critère TGV est un sous-ensemble du contrôle cible |
| Recoupement partiel | 551 | Chevauchement réel, sans inclusion de part ni d'autre |
| Équivalent | 72 | Portée équivalente entre les deux exigences |
| TGV plus large | 37 | Le critère TGV englobe le contrôle cible |

---

## Les 13 référentiels cartographiés

| Référentiel | Catégorie | Correspondances | Contrôles touchés |
|---|---|---:|---|
| [SOC 2 (Trust Services Criteria)](data/crosswalks/crosswalk-soc2-type2.csv) | Attestation | 220 | 45 |
| [NIST SP 800-66 Rev. 2 (HIPAA)](data/crosswalks/crosswalk-hipaa-nist-800-66.csv) | Réglementation | 149 | 72 / 152 |
| [ISO/IEC 27001:2022](data/crosswalks/crosswalk-iso-27001-2022.csv) | Certification | 135 | 68 / 123 |
| [ISO/IEC 27701:2025](data/crosswalks/crosswalk-iso-27701-2025.csv) | Certification | 119 | 17 / 21 |
| [ISO/IEC 42001:2023](data/crosswalks/crosswalk-iso-42001-2023.csv) | Certification | 115 | 31 / 67 |
| [BSI C5:2020](data/crosswalks/crosswalk-bsi-c5-2020.csv) | Attestation | 113 | 67 / 121 |
| [RGPD / GDPR](data/crosswalks/crosswalk-rgpd-gdpr.csv) | Réglementation | 110 | 51 |
| [HITRUST CSF v11](data/crosswalks/crosswalk-hitrust-csf-v11.csv) | Certification | 101 | 82 / 132 |
| [Directive NIS2](data/crosswalks/crosswalk-nis2.csv) | Réglementation | 95 | 80 |
| [CCB CyberFundamentals 2023](data/crosswalks/crosswalk-ccb-cyberfundamentals.csv) | Cadre national | 83 | 64 |
| [EU AI Act](data/crosswalks/crosswalk-eu-ai-act.csv) | Réglementation | 43 | 31 |
| [Hébergement de données de santé (HDS) v2](data/crosswalks/crosswalk-hds-v2.csv) | Certification | 12 | 11 |
| [ISO 22301:2019](data/crosswalks/crosswalk-iso-22301-2019.csv) | Certification | 7 | 5 / 46 |

---

## Ce que la TGV couvre, et que les autres ne couvrent pas seuls

C'est le constat le plus utile de l'exercice. La TGV est le référentiel le plus
large des cinq grands cadres auxquels une entreprise en santé sera confrontée.

| Famille TGV | Critères |
|---|---:|
| Sécurité | 112 |
| Protection des renseignements personnels | 108 |
| Intelligence artificielle | 69 |
| Interopérabilité | 58 |
| Technique | 26 |
| Performance | 7 |
| Gouvernance | 2 |

ISO 27001 couvre la sécurité. Le RGPD couvre la vie privée. ISO 42001 couvre
l'intelligence artificielle. SOC 2 couvre la confiance envers un service.

La TGV couvre les quatre en même temps, plus l'interopérabilité, que personne
d'autre n'exige.

---

## Un exemple concret

Le critère **S04.02** de la TGV demande si un programme de sensibilisation et de
formation à la sécurité est en place pour tout le personnel, direction incluse.

Une seule question. Voici ce à quoi elle répond ailleurs :

| Référentiel | Contrôle | Relation |
|---|---|---|
| ISO/IEC 27001:2022 | A.6.3 — Information security awareness, education and training | **Équivalent** |
| SOC 2 | CC2.2 | TGV plus étroit |
| ISO/IEC 42001:2023 | 7.3 — Awareness | Recoupement partiel |

Vous montez la preuve une fois, elle sert trois fois. C'est exactement ce que ce
dépôt permet de repérer, sur 1302 liens.

---

## Utiliser les données

### Formats disponibles

```
data/
├── index.json                      # statistiques et catalogue des référentiels
├── toutes-correspondances.csv      # les 1302 correspondances en un fichier
├── tgv/
│   ├── tgv-criteres.json           # les 382 critères
│   └── tgv-criteres.csv
└── crosswalks/
    ├── crosswalk-iso-27001-2022.json
    ├── crosswalk-iso-27001-2022.csv
    └── ...                         # un couple JSON + CSV par référentiel
```

### Tableur

Ouvrez `data/toutes-correspondances.csv` (encodage UTF-8 avec BOM, compatible
Excel en français) ou téléchargez le [classeur Excel mis en page](xlsx/), qui
contient une page de garde, une matrice de synthèse et un onglet par référentiel.

### En ligne de commande

```bash
# Tout ce que le critère S04.02 touche, tous référentiels confondus
grep "S04.02" data/toutes-correspondances.csv

# Les 72 équivalences strictes
grep ",equivalent," data/toutes-correspondances.csv
```

### En Python

```python
import json

cw = json.load(open("data/crosswalks/crosswalk-iso-27001-2022.json", encoding="utf-8"))
print(cw["statistiques"])

for c in cw["correspondances"]:
    if c["relation"] == "equivalent":
        print(c["tgv_ref"], "->", c["cible_ref"], "|", c["cible_intitule"])
```

---

## Méthodologie en bref

1. Le **TGV est le référentiel source**. Chaque correspondance part d'un critère
   TGV vers un contrôle cible.
2. Les correspondances sont produites par analyse assistée, puis soumises à une
   **vérification contradictoire** dont le mandat est de rejeter tout lien ténu,
   de corriger les relations erronées et de ne retenir que ce qui est défendable
   devant un auditeur. À titre d'exemple, sur le référentiel HITRUST, **59 des
   160 correspondances proposées ont été rejetées**.
3. Chaque lien retenu porte une **relation qualifiée** et une **justification
   écrite**. Une flèche sans justification n'a aucune valeur en audit.

Le détail complet est dans la page Méthodologie du site.

---

## Ce que ces correspondances ne disent pas

**Couvrir 68 contrôles sur 123 ne signifie pas être à 55 % d'une certification
ISO 27001.**

Cela signifie que le travail de documentation fait pour la TGV est réutilisable
ailleurs : pas besoin de réécrire trois fois la même politique ni de recollecter
trois fois les mêmes preuves.

C'est une avance sur la **préparation**, pas sur le **certificat**. La
certification exige toujours un système de gestion, des audits internes, une
revue de direction et un organisme accrédité.

---


---

<!-- FAITS:début -->
## Faits vérifiables

Chaque affirmation ci-dessous est recalculée depuis les données du dépôt et vérifiée
en intégration continue. Version exploitable par machine : [`faits.jsonl`](https://raw.githubusercontent.com/Factero/tgv-msss-crosswalk/main/faits.jsonl).

- **Trousse globale de vérification (TGV) compte 1302 correspondances vérifiées vers 13 référentiels.**  
  *Preuve : data/index.json · champ statistiques.correspondances_total*
- **Trousse globale de vérification (TGV) présente 220 correspondances avec SOC 2 (Trust Services Criteria, AICPA 2017), touchant 45 de ses 358 contrôles.**  
  *Preuve : data/index.json · référentiel soc2-type2*
- **Trousse globale de vérification (TGV) présente 149 correspondances avec NIST SP 800-66 Rév. 2 (HIPAA Security Rule), touchant 72 de ses 152 contrôles, dont 10 équivalences strictes.**  
  *Preuve : data/index.json · référentiel hipaa-nist-800-66*
- **Trousse globale de vérification (TGV) présente 135 correspondances avec ISO/IEC 27001:2022, touchant 68 de ses 123 contrôles, dont 36 équivalences strictes.**  
  *Preuve : data/index.json · référentiel iso-27001-2022*
- **Trousse globale de vérification (TGV) présente 119 correspondances avec ISO/IEC 27701:2025, touchant 17 de ses 21 contrôles.**  
  *Preuve : data/index.json · référentiel iso-27701-2025*
- **Trousse globale de vérification (TGV) présente 115 correspondances avec ISO/IEC 42001:2023, touchant 31 de ses 67 contrôles.**  
  *Preuve : data/index.json · référentiel iso-42001-2023*
- **Trousse globale de vérification (TGV) présente 113 correspondances avec BSI C5:2020, touchant 67 de ses 121 contrôles, dont 3 équivalences strictes.**  
  *Preuve : data/index.json · référentiel bsi-c5-2020*
- **Trousse globale de vérification (TGV) présente 110 correspondances avec RGPD / GDPR (UE 2016/679), touchant 51 de ses 287 contrôles, dont 2 équivalences strictes.**  
  *Preuve : data/index.json · référentiel rgpd-gdpr*
- **Trousse globale de vérification (TGV) présente 101 correspondances avec HITRUST CSF v11, touchant 82 de ses 132 contrôles, dont 8 équivalences strictes.**  
  *Preuve : data/index.json · référentiel hitrust-csf-v11*
- **Trousse globale de vérification (TGV) présente 95 correspondances avec Directive NIS2 (annexe technique, guidance ENISA), touchant 80 de ses 351 contrôles, dont 6 équivalences strictes.**  
  *Preuve : data/index.json · référentiel nis2*
- **Trousse globale de vérification (TGV) présente 83 correspondances avec CCB CyberFundamentals Framework 2023, touchant 64 de ses 221 contrôles, dont 7 équivalences strictes.**  
  *Preuve : data/index.json · référentiel ccb-cyberfundamentals*
- **Trousse globale de vérification (TGV) présente 43 correspondances avec Règlement européen sur l'IA (EU AI Act), touchant 31 de ses 347 contrôles.**  
  *Preuve : data/index.json · référentiel eu-ai-act*
- **La TGV du MSSS couvre simultanément la sécurité, la protection des renseignements personnels, l'intelligence artificielle, l'interopérabilité, la technique et la performance. Aucun des 13 référentiels internationaux cartographiés ne couvre ces domaines simultanément.**  
  *Preuve : 382 critères répartis en 7 familles : S 112, P 108, IA 69, I 58, T 26, PF 7, G 2*
- **Une certification ISO 27001, SOC 2 ou HITRUST ne dispense pas de la TGV : elle en couvre une partie et la documentation produite est réutilisable, mais la TGV reste une porte d'entrée distincte au réseau de la santé québécois.**  
  *Preuve : 1302 correspondances qualifiées, dont seulement 72 équivalences strictes*

Index complet des fichiers, avec lien direct vers chaque contenu brut : [INDEX.md](https://github.com/Factero/tgv-msss-crosswalk/blob/main/INDEX.md).

<!-- FAITS:fin -->

## Vérifier l'intégrité des fichiers

Chaque fichier du dépôt est empreinté. Pour confirmer qu'aucun n'a été altéré :

```bash
python tools/gen_checksums.py --verify
```

Ou avec les outils système, sous Linux et macOS :

```bash
sha512sum -c checksums/SHA512SUMS
```

Les manifestes `SHA512SUMS`, `SHA256SUMS` et `MD5SUMS` sont au format coreutils,
et `checksums/manifest.json` ajoute BLAKE2b-512 et la taille de chaque fichier.

**Utilisez SHA-512.** MD5 n'est fourni que pour un contrôle anti-corruption de
transfert : il est cryptographiquement cassé depuis 2008 et ne constitue aucune
garantie d'authenticité. Le détail, ainsi que la vérification des attestations de
provenance signées via Sigstore, est dans [checksums/README.md](checksums/README.md).

## Sources et droits

Le texte des critères provient de la publication officielle du MSSS :

> **Certification — Trousse globale de vérification (TGV)**
> Ministère de la Santé et des Services sociaux du Québec
> Publication 24-715-38W · ISBN 978-2-550-97589-2
> <https://publications.msss.gouv.qc.ca/msss/document-003757/>

Ce dépôt est soumis à **deux régimes de droits distincts** : le texte des
critères appartient au Gouvernement du Québec, alors que les correspondances,
les justifications et l'outillage sont publiés sous CC BY 4.0 par Service
conseils Factero. **Lisez [NOTICE.md](NOTICE.md) avant toute réutilisation.**

Ce dépôt n'est ni produit, ni approuvé, ni endossé par le MSSS ou Santé Québec.
En cas de divergence, **la publication officielle du MSSS prévaut**.

---

## Qui maintient ce projet

[**Service conseils Factero**](https://factero.ca) accompagne les entreprises
technologiques en santé dans leurs démarches de certification, à
Saint-Jean-sur-Richelieu au Québec.

Ce travail a été produit dans le cadre de nos échanges avec le MSSS sur la TGV.
Notre position est simple : si chaque entreprise qui frappe à la porte du réseau
refait cette cartographie de son côté, on gaspille collectivement des centaines
d'heures pour arriver treize fois au même résultat. Autant que le travail soit
fait une fois, correctement, et qu'il serve à tout le monde.

Une correspondance vous semble contestable ? [Ouvrez une issue](../../issues).
Les contributions sont bienvenues, voir [CONTRIBUTING.md](CONTRIBUTING.md).

---
---

<a name="english"></a>

# TGV Crosswalk — Quebec Health Ministry Verification Framework

### Open crosswalk between Quebec's TGV health-technology certification and 13 international security and compliance frameworks

**1302 verified mappings · 382 TGV criteria · 13 frameworks**

## What this is

Any digital health solution that connects to Quebec's public health network must
pass the **Trousse globale de vérification (TGV)**, the verification framework
issued by Quebec's Ministry of Health and Social Services (MSSS). It contains 382
criteria, covering security, privacy, artificial intelligence, interoperability
and performance.

Vendors who already hold ISO 27001, SOC 2 or HITRUST certifications invariably
ask the same question: *how much of this already counts?*

This repository answers that question, criterion by criterion, for 13 frameworks.

## Key figures

| | |
|---|---|
| TGV assessable criteria | **382** |
| Criteria mapped to at least one framework | **286** |
| Frameworks crosswalked | **13** |
| Total mappings | **1302** |
| Strict equivalences | **72** |

Frameworks covered: SOC 2 (AICPA Trust Services Criteria), NIST SP 800-66 Rev. 2
(HIPAA Security Rule), ISO/IEC 27001:2022, ISO/IEC 27701:2025, ISO/IEC 42001:2023,
BSI C5:2020, GDPR, HITRUST CSF v11, NIS2 Directive, CCB CyberFundamentals,
EU AI Act, HDS v2, ISO 22301:2019.

## Why the TGV is unusually broad

Most frameworks cover one domain. ISO 27001 covers security. GDPR covers privacy.
ISO 42001 covers AI. SOC 2 covers service trust.

The TGV covers all four at once, plus interoperability, which no other framework
in this list requires. That makes it a demanding entry point, but also an
unusually efficient foundation for later certifications.

## Relationship types

Every mapping is qualified, never a bare arrow:

- **equivalent** — the TGV criterion and the target control have equivalent scope
- **tgv_plus_etroit** (narrower) — the TGV criterion is a subset of the target
- **tgv_plus_large** (broader) — the TGV criterion encompasses the target
- **recoupement_partiel** (partial overlap) — genuine overlap, neither contains
  the other

Each mapping also carries a written rationale.

## Using the data

All data is in `data/`, as JSON and CSV (UTF-8 with BOM for Excel compatibility).
A formatted Excel workbook is in `xlsx/`.

```python
import json
cw = json.load(open("data/crosswalks/crosswalk-iso-27001-2022.json", encoding="utf-8"))
print(cw["statistiques"])
```

## Important limitation

A mapping indicates **overlapping intent** between two requirements. It does not
mean a TGV criterion automatically satisfies the target control, nor that a
coverage percentage equals a certification percentage. Certification remains a
formal process conducted by an accredited body.

## Licensing

**Two distinct regimes.** The TGV criteria text is © Gouvernement du Québec
(publication 24-715-38W, ISBN 978-2-550-97589-2). The crosswalk mappings,
rationales, methodology and tooling are released under **CC BY 4.0** by Service
conseils Factero. **Read [NOTICE.md](NOTICE.md) before reusing anything.**

This repository is not produced, approved or endorsed by the MSSS or Santé
Québec. The official MSSS publication prevails in case of any discrepancy.

## Citation

```
Service conseils Factero (2026). TGV Crosswalk: mapping Quebec's health
technology verification framework to 13 international standards.
https://certification-tgv.ca
```

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.
