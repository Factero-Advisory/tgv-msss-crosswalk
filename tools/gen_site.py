# -*- coding: utf-8 -*-
# Generateur du site statique certification-tgv.ca (GitHub Pages, servi depuis la racine).
# Bilingue FR/EN, JSON-LD Dataset, hreflang, sitemap. Aucune dependance externe.
import json, os, sys, html, re
from collections import Counter, defaultdict

SRC = "/code/db/repo_export"
OUT = "/code/db/site_out"
SITE = "https://factero-advisory.github.io/tgv-msss-crosswalk"
REPO = "https://github.com/Factero-Advisory/tgv-msss-crosswalk"
DATE = "2026-07-23"

idx = json.load(open(f"{SRC}/index.json", encoding="utf-8"))
crit = json.load(open(f"{SRC}/tgv-criteres.json", encoding="utf-8"))
S = idx["statistiques"]
E = html.escape

FAM_ORDER = ["S", "P", "IA", "I", "T", "PF", "G"]
FAM = {
 "S": ("Sécurité", "Security"), "P": ("Renseignements personnels", "Personal information"),
 "IA": ("Intelligence artificielle", "Artificial intelligence"),
 "I": ("Interopérabilité", "Interoperability"), "T": ("Technique", "Technical"),
 "PF": ("Performance", "Performance"), "G": ("Gouvernance", "Governance"),
}
REL = {
 "equivalent": ("Équivalent", "Equivalent", "eq"),
 "tgv_plus_etroit": ("TGV plus étroit", "TGV narrower", "sub"),
 "tgv_plus_large": ("TGV plus large", "TGV broader", "sup"),
 "recoupement_partiel": ("Recoupement partiel", "Partial overlap", "int"),
}
fam_counts = Counter(c["famille"] for c in crit)

# Noms courts pour les balises <title> (cible : moins de 70 caracteres affiches)
SHORT = {
 "soc2-type2": "SOC 2", "hipaa-nist-800-66": "NIST SP 800-66 (HIPAA)",
 "iso-27001-2022": "ISO/IEC 27001:2022", "iso-27701-2025": "ISO/IEC 27701:2025",
 "iso-42001-2023": "ISO/IEC 42001:2023", "bsi-c5-2020": "BSI C5:2020",
 "rgpd-gdpr": "RGPD", "hitrust-csf-v11": "HITRUST CSF v11", "nis2": "Directive NIS2",
 "ccb-cyberfundamentals": "CCB CyberFundamentals", "eu-ai-act": "EU AI Act",
 "hds-v2": "HDS v2.0", "iso-22301-2019": "ISO 22301:2019",
}
def short(slug, fallback): return SHORT.get(slug, fallback)

CSS = """
/* Charte Factero : jetons repris de factero.ca (theme.min.css)
   base #DDDDE3 - encre #141831 - alternes #141831/#DDDDE3 - doux #F7F7F8
   police Epilogue (variable, auto-hebergee, SIL OFL 1.1)
   bordures 3px - rayon 7px (blocs) et 10px (boutons) */
@font-face{font-family:Epilogue;font-style:normal;font-weight:100 900;font-display:swap;
src:url(FONTPATHepilogue-latin.woff2) format('woff2');
unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:Epilogue;font-style:normal;font-weight:100 900;font-display:swap;
src:url(FONTPATHepilogue-latin-ext.woff2) format('woff2');
unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
:root{--base:#DDDDE3;--ink:#141831;--soft:#F7F7F8;--paper:#fff;
--muted:#4a4f6b;--line:#141831;--accent:#cc8425;
--eq:#bfe3cd;--sub:#c6d9f2;--sup:#f4d9bf;--int:#e6e6ec;
--r:7px;--rb:10px;--bw:3px}
:root[data-theme=dark]{--base:#141831;--ink:#DDDDE3;--soft:#1c2142;--paper:#1a1f3d;
--muted:#a7abc4;--line:#DDDDE3;--eq:#1f4433;--sub:#1e3355;--sup:#4a3320;--int:#2a2f4e}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--base:#141831;--ink:#DDDDE3;
--soft:#1c2142;--paper:#1a1f3d;--muted:#a7abc4;--line:#DDDDE3;
--eq:#1f4433;--sub:#1e3355;--sup:#4a3320;--int:#2a2f4e}}
*{box-sizing:border-box}
body{margin:0;background:var(--base);color:var(--ink);
font-family:Epilogue,'Epilogue-Fallback',Arial,Helvetica,sans-serif;
font-size:1rem;line-height:1.5;-webkit-text-size-adjust:100%}
.wrap{max-width:1140px;margin:0 auto;padding:0 24px}
header.top{position:sticky;top:0;z-index:50;background:var(--base);
border-bottom:var(--bw) solid var(--line)}
header.top .wrap{display:flex;gap:20px;align-items:center;flex-wrap:wrap;
padding-top:16px;padding-bottom:16px}
.brand{font-weight:800;color:var(--ink);text-decoration:none;font-size:1.05rem;
letter-spacing:-.02em;text-transform:uppercase}
nav.main{display:flex;gap:20px;flex-wrap:wrap;margin-left:auto;align-items:center}
nav.main a{color:var(--ink);text-decoration:none;font-size:.92rem;font-weight:600;
padding-bottom:2px;border-bottom:2px solid transparent}
nav.main a:hover{border-bottom-color:var(--accent);color:var(--ink)}
.hero{background:var(--ink);color:var(--base);padding:64px 0 52px;
border-bottom:var(--bw) solid var(--line)}
.hero a{color:var(--base)}
.hero .lede{color:var(--base);opacity:.88}
h1{font-size:clamp(2rem,4.6vw,2.5rem);line-height:1.15;margin:0 0 16px;
font-weight:800;letter-spacing:-.025em}
h2{font-size:clamp(1.4rem,3vw,2rem);margin:44px 0 14px;font-weight:700;letter-spacing:-.02em}
h3{font-size:1.15rem;margin:28px 0 8px;font-weight:700}
.lede{font-size:1.1rem;max-width:68ch;margin:0 0 24px}
p{max-width:72ch}
a{color:var(--ink);text-underline-offset:3px;text-decoration-thickness:2px}
a:hover{color:var(--accent)}
main{padding:8px 0 64px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin:28px 0}
.stat{background:var(--base);color:var(--ink);border:var(--bw) solid var(--ink);
border-radius:var(--r);padding:18px}
.hero .stat{background:transparent;color:var(--base);border-color:var(--base)}
.stat b{display:block;font-size:2rem;line-height:1.05;font-weight:800;letter-spacing:-.03em}
.stat span{font-size:.82rem;font-weight:600;text-transform:uppercase;letter-spacing:.04em;opacity:.85}
.tablewrap{overflow-x:auto;border:var(--bw) solid var(--ink);border-radius:var(--r);
margin:22px 0;background:var(--paper)}
table{border-collapse:collapse;width:100%;font-size:.92rem;min-width:600px}
th{background:var(--ink);color:var(--base);text-align:left;padding:12px 14px;
font-weight:700;white-space:nowrap;font-size:.85rem;text-transform:uppercase;letter-spacing:.03em}
td{padding:12px 14px;border-top:1px solid rgba(20,24,49,.16);vertical-align:top}
:root[data-theme=dark] td{border-top-color:rgba(221,221,227,.16)}
td.num,th.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
code,.ref{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.85rem}
.ref{white-space:nowrap;font-weight:700}
.pill{display:inline-block;padding:3px 10px;border-radius:var(--r);font-size:.75rem;
font-weight:700;white-space:nowrap;color:#141831;border:2px solid rgba(20,24,49,.35)}
.pill.eq{background:var(--eq)}.pill.sub{background:var(--sub)}
.pill.sup{background:var(--sup)}.pill.int{background:var(--int)}
:root[data-theme=dark] .pill{color:#DDDDE3;border-color:rgba(221,221,227,.3)}
.note{background:var(--soft);border:var(--bw) solid var(--ink);border-radius:var(--r);
padding:18px 20px;margin:26px 0}
.note strong{font-weight:800}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin:22px 0}
.card{display:block;background:var(--paper);border:var(--bw) solid var(--ink);
border-radius:var(--r);padding:20px;text-decoration:none;color:var(--ink);
transition:transform .12s,box-shadow .12s}
.card:hover{transform:translate(-2px,-2px);box-shadow:4px 4px 0 var(--ink);color:var(--ink)}
.card b{display:block;margin-bottom:6px;font-size:1.02rem;font-weight:800}
.card span{font-size:.88rem;color:var(--muted)}
input[type=search]{width:100%;max-width:480px;padding:12px 14px;
border:var(--bw) solid var(--ink);border-radius:var(--r);
background:var(--paper);color:var(--ink);font-family:inherit;font-size:1rem}
input[type=search]::placeholder{color:var(--muted)}
.dl{display:inline-block;background:var(--ink);color:var(--base);
padding:11px 22px;border:var(--bw) solid var(--ink);border-radius:var(--rb);
text-decoration:none;font-weight:700;font-size:.95rem;margin:8px 10px 8px 0;
min-height:40px;text-align:center}
.dl:hover{background:var(--base);color:var(--ink);border-color:var(--ink)}
.hero .dl{background:var(--base);color:var(--ink);border-color:var(--base)}
.hero .dl:hover{background:transparent;color:var(--base)}
.dl.alt{background:transparent;color:var(--ink);border-color:var(--ink)}
.dl.alt:hover{background:var(--ink);color:var(--base)}
.hero .dl.alt{background:transparent;color:var(--base);border-color:var(--base)}
.hero .dl.alt:hover{background:var(--base);color:var(--ink)}
footer{border-top:var(--bw) solid var(--line);background:var(--soft);
padding:36px 0;font-size:.85rem;color:var(--muted)}
footer p{max-width:80ch}
footer a{color:var(--ink);font-weight:600}
.hidden{display:none}
@media(max-width:640px){.hero{padding:40px 0 32px}.wrap{padding:0 18px}
nav.main{gap:14px;width:100%;margin-left:0}}
"""

def head(title, desc, canon, alt_lang, alt_href, lang, jsonld=None, extra_kw="", fontbase="assets/fonts/"):
    j = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{f'<meta name="keywords" content="{E(extra_kw)}">' if extra_kw else ''}
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="{lang}" href="{canon}">
<link rel="alternate" hreflang="{alt_lang}" href="{alt_href}">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="Correspondances TGV">
<meta property="og:locale" content="{'fr_CA' if lang=='fr' else 'en_CA'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="author" content="Service conseils Factero">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='12' fill='%231f3864'/><text x='32' y='44' font-size='34' font-family='sans-serif' font-weight='700' fill='white' text-anchor='middle'>T</text></svg>">
<style>{CSS.replace("FONTPATH", fontbase)}</style>
{j}"""

def shell(title, desc, canon, alt_lang, alt_href, lang, body, jsonld=None, kw="", depth=0):
    up = "../" * depth or "./"
    if lang == "fr":
        nav = (f'<a href="{up}fr/tgv.html">La TGV</a>'
               f'<a href="{up}fr/referentiels/">Référentiels</a>'
               f'<a href="{up}fr/criteres.html">Les 382 critères</a>'
               f'<a href="{up}fr/methodologie.html">Méthodologie</a>'
               f'<a href="{up}en/">EN</a>')
        foot = (f'<p><strong>Source des critères :</strong> Certification — Trousse globale de '
                f'vérification (TGV), ministère de la Santé et des Services sociaux du Québec, '
                f'publication 24-715-38W, ISBN 978-2-550-97589-2. '
                f'<a href="https://publications.msss.gouv.qc.ca/msss/document-003757/">Publication officielle</a>. '
                f'© Gouvernement du Québec.</p>'
                f'<p>Les correspondances, justifications et l\'outillage sont publiés sous '
                f'<a href="https://creativecommons.org/licenses/by/4.0/deed.fr">CC BY 4.0</a> par '
                f'<a href="https://factero.ca">Service conseils Factero</a>, Saint-Jean-sur-Richelieu, Québec. '
                f'<a href="{REPO}/blob/main/NOTICE.md">Avis de droits complet</a>.</p>'
                f'<p>Site indépendant. Ni produit, ni approuvé, ni endossé par le MSSS ou Santé Québec. '
                f'En cas de divergence, la publication officielle prévaut. '
                f'<a href="{REPO}">Dépôt GitHub</a> · <a href="{up}llms.txt">llms.txt</a></p>')
    else:
        nav = (f'<a href="{up}en/tgv.html">The TGV</a>'
               f'<a href="{up}en/frameworks/">Frameworks</a>'
               f'<a href="{up}en/methodology.html">Methodology</a>'
               f'<a href="{up}">FR</a>')
        foot = (f'<p><strong>Criteria source:</strong> Certification — Trousse globale de vérification '
                f'(TGV), Ministère de la Santé et des Services sociaux du Québec, publication '
                f'24-715-38W, ISBN 978-2-550-97589-2. '
                f'<a href="https://publications.msss.gouv.qc.ca/msss/document-003757/">Official publication</a>. '
                f'© Gouvernement du Québec.</p>'
                f'<p>Crosswalk mappings, rationales and tooling released under '
                f'<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> by '
                f'<a href="https://factero.ca">Service conseils Factero</a>, Quebec, Canada. '
                f'<a href="{REPO}/blob/main/NOTICE.md">Full rights notice</a>.</p>'
                f'<p>Independent project. Not produced, approved or endorsed by the MSSS or Santé Québec. '
                f'<a href="{REPO}">GitHub repository</a> · <a href="{up}llms.txt">llms.txt</a></p>')
    return f"""<!doctype html>
<html lang="{lang}"{'' if lang=='fr' else ''}>
<head>
{head(title, desc, canon, alt_lang, alt_href, lang, jsonld, kw, up + "assets/fonts/")}
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{up if lang=='fr' else up+'en/'}">Correspondances TGV</a>
<nav class="main">{nav}</nav>
</div></header>
{body}
<footer><div class="wrap">{foot}</div></footer>
</body></html>"""

def w(path, content):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)

pages = []   # (loc, priority, changefreq)
def reg(loc, pr="0.7"):
    pages.append((loc, pr))

# ---------------------------------------------------------------- JSON-LD
DATASET = {
 "@context": "https://schema.org", "@type": "Dataset",
 "name": "Correspondances TGV vers 13 référentiels internationaux",
 "alternateName": "TGV Crosswalk",
 "description": (f"Cartographie vérifiée entre les {S['criteres_tgv_total']} critères de la "
   f"Trousse globale de vérification (TGV) du ministère de la Santé et des Services sociaux du "
   f"Québec et les contrôles de {S['referentiels']} référentiels internationaux de sécurité et de "
   f"conformité (ISO/IEC 27001:2022, SOC 2, RGPD, ISO/IEC 42001:2023, HITRUST CSF v11, NIS2, "
   f"HDS, EU AI Act et autres). {S['correspondances_total']} correspondances, chacune qualifiée "
   f"par une relation et accompagnée d'une justification écrite."),
 "url": SITE, "identifier": SITE,
 "keywords": ["TGV","Trousse globale de vérification","MSSS","Santé Québec","certification",
   "crosswalk","ISO 27001","SOC 2","RGPD","GDPR","ISO 42001","HITRUST","NIS2","HDS",
   "conformité","santé numérique","cybersécurité","Loi 25"],
 "license": "https://creativecommons.org/licenses/by/4.0/",
 "isAccessibleForFree": True, "inLanguage": ["fr-CA","en-CA"], "version": "1.0.0",
 "datePublished": DATE, "dateModified": DATE,
 "creator": {"@type":"Organization","name":"Service conseils Factero","url":"https://factero.ca",
   "address":{"@type":"PostalAddress","addressLocality":"Saint-Jean-sur-Richelieu",
     "addressRegion":"QC","addressCountry":"CA"}},
 "publisher": {"@type":"Organization","name":"Service conseils Factero","url":"https://factero.ca"},
 "isBasedOn": {"@type":"CreativeWork",
   "name":"Certification — Trousse globale de vérification (TGV)",
   "publisher":{"@type":"GovernmentOrganization",
     "name":"Ministère de la Santé et des Services sociaux du Québec"},
   "identifier":"ISBN 978-2-550-97589-2",
   "url":"https://publications.msss.gouv.qc.ca/msss/document-003757/"},
 "distribution": [
   {"@type":"DataDownload","name":"Toutes les correspondances (CSV)","encodingFormat":"text/csv",
    "contentUrl":f"{SITE}/data/toutes-correspondances.csv"},
   {"@type":"DataDownload","name":"Index et statistiques (JSON)","encodingFormat":"application/json",
    "contentUrl":f"{SITE}/data/index.json"},
   {"@type":"DataDownload","name":"Critères TGV (JSON)","encodingFormat":"application/json",
    "contentUrl":f"{SITE}/data/tgv/tgv-criteres.json"},
   {"@type":"DataDownload","name":"Classeur Excel","encodingFormat":
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "contentUrl":f"{SITE}/xlsx/Matrice-correspondance-TGV-13-referentiels.xlsx"},
 ],
 "variableMeasured":[
   {"@type":"PropertyValue","name":"Correspondances","value":S["correspondances_total"]},
   {"@type":"PropertyValue","name":"Critères TGV","value":S["criteres_tgv_total"]},
   {"@type":"PropertyValue","name":"Référentiels","value":S["referentiels"]},
 ],
}

FAQ_FR = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
 {"@type":"Question","name":"Qu'est-ce que la TGV du MSSS ?","acceptedAnswer":{"@type":"Answer",
  "text":"La Trousse globale de vérification (TGV) est le référentiel du ministère de la Santé et "
   "des Services sociaux du Québec servant à attester la conformité d'un produit ou service "
   "technologique aux exigences du réseau de la santé québécois en matière de sécurité, de "
   "protection des renseignements personnels, de performance et de technologie. Elle compte 382 "
   "critères évaluables. La vérification est menée par le Bureau de certification et "
   "d'homologation (BCH) et le certificat est valide cinq ans."}},
 {"@type":"Question","name":"Une certification ISO 27001 ou SOC 2 dispense-t-elle de la TGV ?",
  "acceptedAnswer":{"@type":"Answer","text":"Non. Ces référentiels ne répondent pas aux mêmes "
   "questions. La TGV touche 68 des 123 contrôles d'ISO/IEC 27001:2022, ce qui signifie que la "
   "documentation produite est largement réutilisable, mais une certification existante ne "
   "remplace pas la TGV, qui demeure la porte d'entrée du réseau de la santé québécois."}},
 {"@type":"Question","name":"Combien de critères compte la TGV ?","acceptedAnswer":{"@type":"Answer",
  "text":"La TGV compte 382 critères évaluables, répartis en 112 critères de sécurité, 108 de "
   "protection des renseignements personnels, 69 d'intelligence artificielle, 58 "
   "d'interopérabilité, 26 techniques, 7 de performance et 2 de gouvernance."}},
 {"@type":"Question","name":"La TGV est-elle une certification reconnue à l'international ?",
  "acceptedAnswer":{"@type":"Answer","text":"Non. La TGV est un référentiel québécois servant "
   "d'accès au réseau de la santé du Québec. Elle n'est pas reconnue comme une certification "
   "internationale. En revanche, elle couvre simultanément la sécurité, la vie privée, "
   "l'intelligence artificielle et l'interopérabilité, ce qui en fait une base de préparation "
   "efficace vers ISO/IEC 27001, SOC 2 ou ISO/IEC 42001."}},
]}

# ---------------------------------------------------------------- accueil FR
def stat_block(items):
    return ('<div class="stats">' + "".join(
        f'<div class="stat"><b>{v}</b><span>{E(l)}</span></div>' for v, l in items) + "</div>")

rows_fw = "".join(
  f'<tr><td><a href="fr/referentiels/{r["slug"]}.html">{E(r["nom"])}</a></td>'
  f'<td>{E(r["categorie"])}</td><td class="num">{r["correspondances"]}</td>'
  f'<td class="num">{r["criteres_tgv"]}</td>'
  f'<td class="num">{r["controles_cible_touches"]} / {r["controles_total"]}</td></tr>'
  for r in idx["referentiels"])

rows_fam = "".join(
  f'<tr><td>{E(FAM[f][0])}</td><td><code>{f}</code></td><td class="num">{fam_counts[f]}</td></tr>'
  for f in FAM_ORDER if fam_counts.get(f))

body = f"""<div class="hero"><div class="wrap">
<h1>Correspondances entre la TGV du MSSS et 13 référentiels internationaux</h1>
<p class="lede">La Trousse globale de vérification (TGV) est le référentiel de certification des
solutions numériques en santé au Québec. Ce site publie, critère par critère, ce que ses
{S['criteres_tgv_total']} exigences ont en commun avec ISO/IEC 27001, SOC 2, le RGPD,
ISO/IEC 42001, HITRUST et huit autres référentiels.</p>
{stat_block([(S['criteres_tgv_total'],"critères TGV"),(S['correspondances_total'],"correspondances"),
             (S['referentiels'],"référentiels"),(S['relations'].get('equivalent',0),"équivalences strictes")])}
<a class="dl" href="data/toutes-correspondances.csv">Télécharger les données (CSV)</a>
<a class="dl alt" href="xlsx/Matrice-correspondance-TGV-13-referentiels.xlsx">Classeur Excel</a>
</div></div>
<main><div class="wrap">

<h2>Pourquoi ce site existe</h2>
<p>Toute solution numérique qui veut se brancher au réseau de la santé québécois doit passer la
TGV. La question qui suit est invariablement la même : « on a déjà un SOC 2 ou une ISO 27001,
est-ce que ça compte ? »</p>
<p>Personne n'avait publié la réponse. La voici, sous forme de {S['correspondances_total']}
correspondances qualifiées et justifiées.</p>

<h2>Les 13 référentiels cartographiés</h2>
<div class="tablewrap"><table>
<thead><tr><th>Référentiel</th><th>Catégorie</th><th class="num">Correspondances</th>
<th class="num">Critères TGV</th><th class="num">Contrôles touchés</th></tr></thead>
<tbody>{rows_fw}</tbody></table></div>

<h2>Ce que la TGV couvre</h2>
<p>C'est le constat le plus utile de l'exercice : la TGV est plus large que chacun des grands
référentiels pris isolément. ISO 27001 traite la sécurité, le RGPD la vie privée, ISO 42001
l'intelligence artificielle, SOC 2 la confiance envers un service. La TGV traite les quatre en
même temps, plus l'interopérabilité, que personne d'autre n'exige.</p>
<div class="tablewrap"><table>
<thead><tr><th>Famille</th><th>Préfixe</th><th class="num">Critères</th></tr></thead>
<tbody>{rows_fam}</tbody></table></div>

<h2>Un exemple concret</h2>
<p>Le critère <span class="ref">S04.02</span> demande si un programme de sensibilisation et de
formation à la sécurité est en place pour tout le personnel, direction incluse. Une seule
question, à laquelle répondent simultanément :</p>
<div class="tablewrap"><table>
<thead><tr><th>Référentiel</th><th>Contrôle</th><th>Relation</th></tr></thead><tbody>
<tr><td>ISO/IEC 27001:2022</td><td><span class="ref">A.6.3</span> Information security awareness,
education and training</td><td><span class="pill eq">Équivalent</span></td></tr>
<tr><td>SOC 2</td><td><span class="ref">CC2.2</span></td>
<td><span class="pill sub">TGV plus étroit</span></td></tr>
<tr><td>ISO/IEC 42001:2023</td><td><span class="ref">7.3</span> Awareness</td>
<td><span class="pill int">Recoupement partiel</span></td></tr>
</tbody></table></div>
<p>Vous montez la preuve une fois, elle sert trois fois. C'est ce que ce jeu de données permet de
repérer, sur {S['correspondances_total']} liens.</p>

<div class="note"><strong>Ce que ces correspondances ne disent pas.</strong> Couvrir 68 contrôles
sur 123 ne signifie pas être à 55&nbsp;% d'une certification ISO 27001. Cela signifie que la
documentation produite pour la TGV est réutilisable ailleurs. C'est une avance sur la préparation,
pas sur le certificat. La certification exige toujours un système de gestion, des audits internes,
une revue de direction et un organisme accrédité.</div>

<h2>Explorer</h2>
<div class="cards">
<a class="card" href="fr/tgv.html"><b>Qu'est-ce que la TGV</b><span>Nature, portée, déroulement et
durée de la certification.</span></a>
<a class="card" href="fr/criteres.html"><b>Les {S['criteres_tgv_total']} critères</b>
<span>Liste complète et recherche instantanée.</span></a>
<a class="card" href="fr/referentiels/"><b>Les 13 référentiels</b><span>Une page de
correspondances par référentiel.</span></a>
<a class="card" href="fr/methodologie.html"><b>Méthodologie</b><span>Comment les correspondances
sont produites et vérifiées.</span></a>
</div>

<div class="note">
<p><strong>Portée de ce site.</strong> Il publie des correspondances entre exigences, rien de plus.
Il ne remplace ni la lecture de la trousse officielle, ni un audit, ni l'avis du Bureau de
certification et d'homologation. Une correspondance signale un recoupement d'intention entre deux
exigences : elle n'établit pas qu'un critère TGV satisfait automatiquement le contrôle visé.</p>
<p>Une correspondance vous semble contestable ? <a href="{REPO}/issues">Signalez-la</a>. Les
justifications sont publiées précisément pour pouvoir être discutées.</p>
</div>
</div></main>"""

w("index.html", shell(
  "Correspondances TGV du MSSS vers ISO 27001, SOC 2 et RGPD",
  f"Cartographie ouverte des {S['criteres_tgv_total']} critères de la TGV (MSSS Québec) vers "
  f"{S['referentiels']} référentiels : ISO 27001, SOC 2, RGPD, ISO 42001, HITRUST. "
  f"{S['correspondances_total']} correspondances justifiées, données libres.",
  f"{SITE}/", "en", f"{SITE}/en/", "fr", body,
  jsonld=[DATASET, FAQ_FR],
  kw="TGV, Trousse globale de vérification, MSSS, certification TGV, Santé Québec, ISO 27001, "
     "SOC 2, RGPD, ISO 42001, HITRUST, conformité santé Québec, Loi 25", depth=0))
reg(f"{SITE}/", "1.0")

# ------------------------------------------------- pages referentiel (FR + EN)
crit_by_ref = {c["ref"]: c for c in crit}

def fw_page(r, lang):
    doc = json.load(open(f"{SRC}/crosswalk-{r['slug']}.json", encoding="utf-8"))
    cs = doc["correspondances"]
    fr = lang == "fr"
    canon = f"{SITE}/{'fr/referentiels' if fr else 'en/frameworks'}/{r['slug']}.html"
    alt = f"{SITE}/{'en/frameworks' if fr else 'fr/referentiels'}/{r['slug']}.html"
    rows = []
    for c in cs:
        lab, labe, cls = REL[c["relation"]]
        tgvtxt = crit_by_ref.get(c["tgv_ref"], {}).get("texte", "")
        rows.append(
          f'<tr id="{E(c["tgv_ref"])}-{E(re.sub(chr(92)+"W","",c["cible_ref"]))}">'
          f'<td><span class="ref">{E(c["tgv_ref"])}</span></td>'
          f'<td>{E(tgvtxt)}</td>'
          f'<td><span class="ref">{E(c["cible_ref"])}</span></td>'
          f'<td>{E(c["cible_intitule"])}</td>'
          f'<td><span class="pill {cls}">{E(lab if fr else labe)}</span></td>'
          f'<td>{E(c["justification"])}</td></tr>')
    relsum = " · ".join(
        f'{E(REL[k][0] if fr else REL[k][1])} : {v}'
        for k, v in sorted(r["relations"].items(), key=lambda x: -x[1]))
    sh = short(r["slug"], r["nom"])
    if fr:
        t = f"TGV → {sh} : {r['correspondances']} correspondances"
        d = (f"Correspondances entre les critères de la Trousse globale de vérification (TGV) du "
             f"MSSS et {r['nom']} : {r['correspondances']} liens qualifiés et justifiés, touchant "
             f"{r['controles_cible_touches']} contrôles.")
        h = ["Réf. TGV","Critère TGV","Réf. cible","Intitulé du contrôle","Relation","Justification"]
        lede = (f"{r['correspondances']} correspondances établies depuis {r['criteres_tgv']} "
                f"critères de la TGV, touchant {r['controles_cible_touches']} des "
                f"{r['controles_total']} contrôles de ce référentiel.")
        dl = f'<a class="dl" href="{SITE}/data/crosswalks/crosswalk-{r["slug"]}.csv">Télécharger ce crosswalk (CSV)</a><a class="dl alt" href="{SITE}/data/crosswalks/crosswalk-{r["slug"]}.json">JSON</a>'
        back = '<p><a href="./">← Tous les référentiels</a></p>'
    else:
        t = f"TGV → {sh} crosswalk: {r['correspondances']} mappings"
        d = (f"Crosswalk between Quebec's TGV health technology verification framework (MSSS) and "
             f"{r['nom']}: {r['correspondances']} qualified, rationale-backed mappings covering "
             f"{r['controles_cible_touches']} controls.")
        h = ["TGV ref","TGV criterion","Target ref","Control title","Relationship","Rationale"]
        lede = (f"{r['correspondances']} mappings from {r['criteres_tgv']} TGV criteria, covering "
                f"{r['controles_cible_touches']} of {r['controles_total']} controls in this framework.")
        dl = f'<a class="dl" href="{SITE}/data/crosswalks/crosswalk-{r["slug"]}.csv">Download this crosswalk (CSV)</a><a class="dl alt" href="{SITE}/data/crosswalks/crosswalk-{r["slug"]}.json">JSON</a>'
        back = '<p><a href="./">← All frameworks</a></p>'
    body = f"""<div class="hero"><div class="wrap">
{back}<h1>TGV → {E(r['nom'])}</h1><p class="lede">{E(lede)}</p>
{stat_block([(r['correspondances'], "correspondances" if fr else "mappings"),
             (r['criteres_tgv'], "critères TGV" if fr else "TGV criteria"),
             (f"{r['controles_cible_touches']}/{r['controles_total']}",
              "contrôles touchés" if fr else "controls covered")])}
<p style="color:var(--muted);font-size:14px">{relsum}</p>{dl}
</div></div><main><div class="wrap">
<div class="tablewrap"><table><thead><tr>{''.join(f'<th>{E(x)}</th>' for x in h)}</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
</div></main>"""
    jl = {"@context":"https://schema.org","@type":"Dataset","name":t,"description":d,
          "url":canon,"license":"https://creativecommons.org/licenses/by/4.0/",
          "isAccessibleForFree":True,"creator":{"@type":"Organization","name":"Service conseils Factero"},
          "distribution":[{"@type":"DataDownload","encodingFormat":"text/csv",
            "contentUrl":f"{SITE}/data/crosswalks/crosswalk-{r['slug']}.csv"}]}
    w(f"{'fr/referentiels' if fr else 'en/frameworks'}/{r['slug']}.html",
      shell(t, d, canon, "en" if fr else "fr", alt, lang, body, jsonld=jl,
            kw=f"TGV, {r['nom']}, crosswalk, correspondance, MSSS, certification", depth=2))
    reg(canon, "0.8")

for r in idx["referentiels"]:
    fw_page(r, "fr"); fw_page(r, "en")

# ------------------------------------------------- index des referentiels
for lang in ("fr", "en"):
    fr = lang == "fr"
    canon = f"{SITE}/{'fr/referentiels' if fr else 'en/frameworks'}/"
    alt = f"{SITE}/{'en/frameworks' if fr else 'fr/referentiels'}/"
    cards = "".join(
      f'<a class="card" href="{r["slug"]}.html"><b>{E(r["nom"])}</b>'
      f'<span>{r["correspondances"]} {"correspondances" if fr else "mappings"} · '
      f'{r["controles_cible_touches"]}/{r["controles_total"]} '
      f'{"contrôles" if fr else "controls"}</span></a>' for r in idx["referentiels"])
    t = ("Les 13 référentiels cartographiés depuis la TGV" if fr
         else "The 13 frameworks crosswalked from the TGV")
    d = ("Correspondances de la TGV du MSSS vers ISO 27001, SOC 2, RGPD, ISO 42001, HITRUST, NIS2, "
         "HDS, BSI C5, ISO 27701, ISO 22301, EU AI Act, HIPAA et CCB CyberFundamentals." if fr
         else "Crosswalks from Quebec's TGV to ISO 27001, SOC 2, GDPR, ISO 42001, HITRUST, NIS2, "
              "HDS, BSI C5, ISO 27701, ISO 22301, EU AI Act, HIPAA and CCB CyberFundamentals.")
    body = f"""<div class="hero"><div class="wrap"><h1>{E(t)}</h1>
<p class="lede">{E(d)}</p></div></div><main><div class="wrap">
<div class="cards">{cards}</div></div></main>"""
    w(f"{'fr/referentiels' if fr else 'en/frameworks'}/index.html",
      shell(t, d, canon, "en" if fr else "fr", alt, lang, body, depth=2))
    reg(canon, "0.9")

# ------------------------------------------------- les 382 criteres (FR)
crows = "".join(
  f'<tr data-s="{E((c["ref"]+" "+c["texte"]).lower())}">'
  f'<td><span class="ref">{E(c["ref"])}</span></td>'
  f'<td>{E(FAM[c["famille"]][0])}</td><td>{E(c["texte"])}</td></tr>'
  for c in sorted(crit, key=lambda x: (FAM_ORDER.index(x["famille"]) if x["famille"] in FAM_ORDER else 9, x["ref"])))
body = f"""<div class="hero"><div class="wrap">
<h1>Les {S['criteres_tgv_total']} critères de la TGV</h1>
<p class="lede">Liste complète des critères évaluables de la Trousse globale de vérification,
avec leur famille et leur libellé officiel. Utilisez la recherche pour filtrer instantanément.</p>
<input type="search" id="q" placeholder="Rechercher un critère, un mot, un identifiant…"
 aria-label="Rechercher parmi les critères">
<p id="cnt" style="color:var(--muted);font-size:14px;margin-top:10px">{S['criteres_tgv_total']} critères affichés</p>
</div></div><main><div class="wrap">
<div class="tablewrap"><table id="t">
<thead><tr><th>Réf.</th><th>Famille</th><th>Critère</th></tr></thead>
<tbody>{crows}</tbody></table></div>
<div class="note">Texte des critères © Gouvernement du Québec, publication 24-715-38W.
La <a href="https://publications.msss.gouv.qc.ca/msss/document-003757/">version officielle</a>
fait foi.</div>
</div></main>
<script>
(function(){{var q=document.getElementById('q'),rows=document.querySelectorAll('#t tbody tr'),
c=document.getElementById('cnt');
q.addEventListener('input',function(){{var v=q.value.toLowerCase().trim(),n=0;
rows.forEach(function(r){{var m=!v||r.dataset.s.indexOf(v)>-1;r.classList.toggle('hidden',!m);if(m)n++;}});
c.textContent=n+' critère'+(n>1?'s':'')+' affiché'+(n>1?'s':'');}});}})();
</script>"""
w("fr/criteres.html", shell(
  f"Les {S['criteres_tgv_total']} critères de la TGV — liste complète et recherche",
  f"Liste complète et cherchable des {S['criteres_tgv_total']} critères de la Trousse globale de "
  f"vérification (TGV) du MSSS : sécurité, renseignements personnels, intelligence artificielle, "
  f"interopérabilité, technique, performance.",
  f"{SITE}/fr/criteres.html", "en", f"{SITE}/en/", "fr", body,
  kw="critères TGV, liste TGV, 382 critères, Trousse globale de vérification, MSSS", depth=1))
reg(f"{SITE}/fr/criteres.html", "0.9")

# ------------------------------------------------- page TGV (FR + EN)
TGV_FR = f"""<div class="hero"><div class="wrap">
<h1>Qu'est-ce que la TGV du MSSS ?</h1>
<p class="lede">La Trousse globale de vérification est le référentiel qui conditionne l'accès des
solutions numériques au réseau de la santé et des services sociaux du Québec.</p>
</div></div><main><div class="wrap">
<h2>Définition</h2>
<p>La TGV sert à attester la conformité d'une version d'un produit ou service technologique aux
exigences du réseau de la santé et des services sociaux du Québec en matière de sécurité, de
protection des renseignements personnels, de performance et de technologie.</p>
<p>Elle compte <strong>{S['criteres_tgv_total']} critères évaluables</strong>. La vérification est
menée par le Bureau de certification et d'homologation (BCH), en collaboration avec des partenaires
spécialisés en cybersécurité et en protection des renseignements personnels.</p>

<h2>Ce que la TGV n'est pas</h2>
<p>C'est la confusion la plus fréquente, et elle coûte cher. Quatre types de documents circulent
sous le mot « conformité », et ils ne répondent pas aux mêmes questions.</p>
<div class="tablewrap"><table>
<thead><tr><th>Type</th><th>Exemple</th><th>Nature</th></tr></thead><tbody>
<tr><td>Norme certifiable</td><td>ISO/IEC 27001, ISO/IEC 42001</td>
<td>Un organisme accrédité vérifie et délivre un certificat.</td></tr>
<tr><td>Loi</td><td>RGPD, Loi 25</td>
<td>Ne se certifie pas. On la respecte ou on est en infraction.</td></tr>
<tr><td>Attestation</td><td>SOC 2 Type 1 et Type 2</td>
<td>Un rapport signé par un auditeur, pas un certificat.</td></tr>
<tr><td>Questionnaire d'accès</td><td><strong>TGV</strong></td>
<td>Une porte d'entrée, remplie avec des preuves.</td></tr>
</tbody></table></div>

<h2>Déroulement et durée</h2>
<p>La démarche se déroule en deux temps. D'abord un accompagnement à la préparation par le bureau
de certification, dont la durée dépend de la maturité du produit et de l'organisation, et qui
s'étend généralement de une à six semaines. Ensuite la vérification de la TGV par une firme externe
spécialisée, menée sur trente jours ouvrables.</p>
<p>Le certificat TGV est <strong>valide cinq ans</strong>, sous réserve du suivi post-certification.</p>

<h2>Portée : le référentiel le plus large</h2>
<p>La TGV couvre simultanément des domaines que les autres référentiels traitent séparément.</p>
<div class="tablewrap"><table><thead><tr><th>Famille</th><th class="num">Critères</th></tr></thead>
<tbody>{''.join(f'<tr><td>{E(FAM[f][0])}</td><td class="num">{fam_counts[f]}</td></tr>' for f in FAM_ORDER if fam_counts.get(f))}</tbody></table></div>
<p>ISO 27001 traite la sécurité. Le RGPD traite la vie privée. ISO 42001 traite l'intelligence
artificielle. SOC 2 traite la confiance envers un service. La TGV traite les quatre, plus
l'interopérabilité, que personne d'autre n'exige.</p>

<h2>Faut-il faire la TGV avant ou après ISO 27001 ?</h2>
<p>Si votre marché est le réseau de la santé québécois, la TGV vient en premier : c'est la porte
d'entrée, et elle force à documenter sécurité, vie privée et intelligence artificielle en même
temps. Les correspondances publiées ici montrent que ce travail couvre ensuite
68 des 123 contrôles d'ISO/IEC 27001:2022 et 31 des 67 contrôles d'ISO/IEC 42001:2023.</p>
<div class="note"><strong>Attention à l'arithmétique.</strong> Toucher 68 contrôles sur 123 n'est
pas être à 55&nbsp;% d'une certification. C'est une avance sur la préparation documentaire, pas sur
le certificat.</div>

<h2>Source officielle</h2>
<p>Le document de référence est publié par le ministère de la Santé et des Services sociaux :
<a href="https://publications.msss.gouv.qc.ca/msss/document-003757/">Certification — Trousse globale
de vérification (TGV)</a>, publication 24-715-38W, ISBN 978-2-550-97589-2.</p>
</div></main>"""
w("fr/tgv.html", shell(
  "Qu'est-ce que la TGV du MSSS ? Certification santé Québec",
  "La Trousse globale de vérification (TGV) du MSSS en clair : définition, 382 critères, "
  "déroulement, durée, validité de cinq ans, et différence avec ISO 27001, SOC 2 et le RGPD.",
  f"{SITE}/fr/tgv.html", "en", f"{SITE}/en/tgv.html", "fr", TGV_FR, jsonld=FAQ_FR,
  kw="TGV, qu'est-ce que la TGV, certification TGV, MSSS, BCH, Santé Québec, santé numérique", depth=1))
reg(f"{SITE}/fr/tgv.html", "0.9")

TGV_EN = f"""<div class="hero"><div class="wrap">
<h1>What is Quebec's TGV framework?</h1>
<p class="lede">The Trousse globale de vérification (TGV) is the verification framework that gates
access for digital health solutions to Quebec's public health and social services network.</p>
</div></div><main><div class="wrap">
<h2>Definition</h2>
<p>The TGV attests that a given version of a technology product or service complies with the
requirements of Quebec's health and social services network regarding security, protection of
personal information, performance and technology. It contains
<strong>{S['criteres_tgv_total']} assessable criteria</strong>.</p>
<p>Verification is carried out by the Bureau de certification et d'homologation (BCH) together with
specialised cybersecurity and privacy partners. The TGV certificate is valid for five years.</p>

<h2>What the TGV is not</h2>
<p>The TGV is not an ISO-style certifiable standard, not a law, and not an auditor's attestation.
It is a market-access questionnaire, completed with evidence.</p>

<h2>Unusually broad scope</h2>
<div class="tablewrap"><table><thead><tr><th>Family</th><th class="num">Criteria</th></tr></thead>
<tbody>{''.join(f'<tr><td>{E(FAM[f][1])}</td><td class="num">{fam_counts[f]}</td></tr>' for f in FAM_ORDER if fam_counts.get(f))}</tbody></table></div>
<p>ISO 27001 covers security. GDPR covers privacy. ISO 42001 covers AI. SOC 2 covers service trust.
The TGV covers all four at once, plus interoperability, which none of the others require. That
makes it demanding, but also an efficient foundation for later certifications.</p>

<h2>Official source</h2>
<p><a href="https://publications.msss.gouv.qc.ca/msss/document-003757/">Certification — Trousse
globale de vérification (TGV)</a>, Ministère de la Santé et des Services sociaux du Québec,
publication 24-715-38W, ISBN 978-2-550-97589-2.</p>
</div></main>"""
w("en/tgv.html", shell(
  "What is Quebec's TGV framework? Health technology certification (MSSS)",
  "Quebec's Trousse globale de vérification (TGV) explained: 382 criteria, five-year certificate, "
  "and how it compares to ISO 27001, SOC 2 and GDPR.",
  f"{SITE}/en/tgv.html", "fr", f"{SITE}/fr/tgv.html", "en", TGV_EN,
  kw="TGV Quebec, Quebec health certification, MSSS, health technology compliance Canada", depth=1))
reg(f"{SITE}/en/tgv.html", "0.8")

# ------------------------------------------------- methodologie
def methodo(lang):
    fr = lang == "fr"
    rel_rows = "".join(
      f'<tr><td><span class="pill {v[2]}">{E(v[0] if fr else v[1])}</span></td>'
      f'<td><code>{k}</code></td><td class="num">{S["relations"].get(k,0)}</td></tr>'
      for k, v in REL.items())
    if fr:
        t = "Méthodologie des correspondances TGV"
        d = ("Comment les 1302 correspondances entre la TGV et 13 référentiels sont produites, "
             "qualifiées, justifiées puis soumises à une vérification contradictoire.")
        body = f"""<div class="hero"><div class="wrap"><h1>Méthodologie</h1>
<p class="lede">{E(d)}</p></div></div><main><div class="wrap">
<h2>1. La TGV comme référentiel source</h2>
<p>Chaque correspondance part d'un critère de la TGV vers un contrôle du référentiel cible, jamais
l'inverse. La TGV est traitée comme la source de vérité, ce qui garantit que le jeu de données
répond à la question réellement posée par les fournisseurs : « ce que le Québec me demande,
où est-ce que ça compte ailleurs ? »</p>

<h2>2. Production puis vérification contradictoire</h2>
<p>Les correspondances sont d'abord produites par analyse assistée, référentiel par référentiel.
Elles sont ensuite soumises à une seconde lecture dont le mandat explicite est de <em>rejeter</em> :
liens ténus, relations mal qualifiées, justifications circulaires ou hors sujet.</p>
<p>Ce filtre n'est pas cosmétique. Sur le référentiel HITRUST, <strong>59 des 160 correspondances
proposées ont été rejetées</strong>, soit un peu plus du tiers. Seules les 101 survivantes figurent
dans le jeu de données.</p>

<h2>3. Une relation qualifiée pour chaque lien</h2>
<p>Une flèche entre deux cases ne vaut rien en audit. Chaque correspondance précise la nature du
recoupement, du point de vue du critère TGV.</p>
<div class="tablewrap"><table><thead><tr><th>Relation</th><th>Valeur</th>
<th class="num">Occurrences</th></tr></thead><tbody>{rel_rows}</tbody></table></div>

<h2>4. Une justification écrite par correspondance</h2>
<p>Chaque lien est accompagné d'une justification qui explique pourquoi il tient et pourquoi la
relation choisie est la bonne. C'est ce qui permet de défendre le tableau devant un auditeur, et
c'est ce qui distingue ce jeu de données d'un simple rapprochement de mots-clés.</p>

<h2>5. Limites assumées</h2>
<p>Une correspondance signale un recoupement d'intention entre deux exigences. Elle ne signifie pas
qu'un critère TGV satisfait automatiquement le contrôle cible, ni qu'un taux de couverture équivaut
à un taux de certification, ni qu'un organisme de certification acceptera l'équivalence.</p>
<p>Les taux de couverture publiés doivent d'ailleurs se lire avec prudence : certains référentiels
sont décomposés en sous-articles très fins, ce qui écrase mécaniquement le pourcentage sans que la
couverture réelle soit moindre. C'est pourquoi le nombre de correspondances est mis en avant plutôt
que le pourcentage.</p>
</div></main>"""
    else:
        t = "TGV crosswalk methodology"
        d = ("How the 1302 mappings between Quebec's TGV and 13 frameworks are produced, "
             "qualified, justified and adversarially reviewed.")
        body = f"""<div class="hero"><div class="wrap"><h1>Methodology</h1>
<p class="lede">{E(d)}</p></div></div><main><div class="wrap">
<h2>1. TGV as the source framework</h2>
<p>Every mapping runs from a TGV criterion to a target control, never the reverse. This answers the
question vendors actually ask: what Quebec requires of me, where else does it count?</p>
<h2>2. Production, then adversarial review</h2>
<p>Mappings are produced framework by framework, then passed to a second reading whose explicit
mandate is to <em>reject</em>: thin links, mis-qualified relationships, circular or off-topic
rationales. On HITRUST, <strong>59 of 160 proposed mappings were rejected</strong>. Only the 101
survivors are published.</p>
<h2>3. Every link carries a qualified relationship</h2>
<div class="tablewrap"><table><thead><tr><th>Relationship</th><th>Value</th>
<th class="num">Count</th></tr></thead><tbody>{rel_rows}</tbody></table></div>
<h2>4. Every link carries a written rationale</h2>
<p>A bare arrow is worthless in an audit. Each mapping explains why it holds and why the chosen
relationship is correct.</p>
<h2>5. Stated limits</h2>
<p>A mapping indicates overlapping intent. It does not mean a TGV criterion automatically satisfies
the target control, nor that a coverage rate equals a certification rate. Coverage percentages
should be read with care: some frameworks are decomposed into very fine sub-articles, which
mechanically deflates the percentage without reducing real coverage. This is why mapping counts are
presented ahead of percentages.</p>
</div></main>"""
    fn = "fr/methodologie.html" if fr else "en/methodology.html"
    canon = f"{SITE}/{fn}"
    alt = f"{SITE}/{'en/methodology.html' if fr else 'fr/methodologie.html'}"
    w(fn, shell(t, d, canon, "en" if fr else "fr", alt, lang, body, depth=1))
    reg(canon, "0.7")

methodo("fr"); methodo("en")

# ------------------------------------------------- accueil EN
rows_fw_en = "".join(
  f'<tr><td><a href="frameworks/{r["slug"]}.html">{E(r["nom"])}</a></td>'
  f'<td class="num">{r["correspondances"]}</td>'
  f'<td class="num">{r["controles_cible_touches"]} / {r["controles_total"]}</td></tr>'
  for r in idx["referentiels"])
body_en = f"""<div class="hero"><div class="wrap">
<h1>TGV Crosswalk — Quebec's health technology framework mapped to 13 international standards</h1>
<p class="lede">Any digital health solution connecting to Quebec's public health network must pass
the Trousse globale de vérification (TGV), a {S['criteres_tgv_total']}-criterion framework issued by
the province's Ministry of Health. This site publishes, criterion by criterion, what it has in
common with ISO/IEC 27001, SOC 2, GDPR, ISO/IEC 42001, HITRUST and eight other frameworks.</p>
{stat_block([(S['criteres_tgv_total'],"TGV criteria"),(S['correspondances_total'],"mappings"),
             (S['referentiels'],"frameworks"),(S['relations'].get('equivalent',0),"strict equivalences")])}
<a class="dl" href="{SITE}/data/toutes-correspondances.csv">Download the data (CSV)</a>
<a class="dl alt" href="{SITE}/xlsx/Matrice-correspondance-TGV-13-referentiels.xlsx">Excel workbook</a>
</div></div><main><div class="wrap">
<h2>Frameworks covered</h2>
<div class="tablewrap"><table><thead><tr><th>Framework</th><th class="num">Mappings</th>
<th class="num">Controls covered</th></tr></thead><tbody>{rows_fw_en}</tbody></table></div>
<h2>Why the TGV is unusually broad</h2>
<p>Most frameworks cover one domain. ISO 27001 covers security, GDPR covers privacy, ISO 42001
covers AI, SOC 2 covers service trust. The TGV covers all four at once, plus interoperability,
which no other framework here requires.</p>
<div class="note"><strong>Important limitation.</strong> A mapping indicates overlapping intent. It
does not mean a TGV criterion automatically satisfies the target control, nor that a coverage
percentage equals a certification percentage. Certification remains a formal process conducted by an
accredited body.</div>
<div class="cards">
<a class="card" href="tgv.html"><b>What is the TGV</b><span>Scope, process, five-year validity.</span></a>
<a class="card" href="frameworks/"><b>13 frameworks</b><span>One crosswalk page each.</span></a>
<a class="card" href="methodology.html"><b>Methodology</b><span>How mappings are produced and reviewed.</span></a>
</div>
</div></main>"""
w("en/index.html", shell(
  "TGV Crosswalk: Quebec health framework to ISO 27001 & SOC 2",
  f"Open crosswalk of Quebec's {S['criteres_tgv_total']}-criterion TGV health technology framework "
  f"to {S['referentiels']} international standards. {S['correspondances_total']} qualified mappings, "
  f"free data under CC BY 4.0.",
  f"{SITE}/en/", "fr", f"{SITE}/", "en", body_en, jsonld=DATASET,
  kw="TGV, Quebec health certification, crosswalk, ISO 27001 mapping, SOC 2, GDPR, HITRUST", depth=1))
reg(f"{SITE}/en/", "0.9")

# ------------------------------------------------- sitemap + robots
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, pr in pages:
    sm.append(f"<url><loc>{loc}</loc><lastmod>{DATE}</lastmod>"
              f"<changefreq>monthly</changefreq><priority>{pr}</priority></url>")
sm.append("</urlset>")
w("sitemap.xml", "\n".join(sm))
w("robots.txt", f"""User-agent: *
Allow: /

# Corpus optimise pour les modeles de langage
# LLM-oriented corpus
# {SITE}/llms.txt
# {SITE}/llms-full.txt

Sitemap: {SITE}/sitemap.xml
""")

sys.stderr.write(f"RESULT site genere: {len(pages)} pages indexables\n")
files = sum(len(f) for _, _, f in os.walk(OUT))
sys.stderr.write(f"RESULT fichiers HTML/XML/TXT ecrits: {files}\n")
