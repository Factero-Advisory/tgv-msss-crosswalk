# Outillage

Scripts de génération du jeu de données et du site. Ils s'exécutent contre une
instance [CISO Assistant](https://github.com/intuitem/ciso-assistant-community)
dans laquelle la TGV et les crosswalks ont été chargés.

| Script | Rôle |
|---|---|
| `export_from_ciso_assistant.py` | Extrait les 382 critères et les 13 crosswalks vers `data/` (JSON + CSV). |
| `gen_site.py` | Génère les 35 pages du site, le sitemap et robots.txt. |
| `gen_llms_txt.py` | Génère `llms.txt` et `llms-full.txt`. |
| `validate.py` | Valide l'intégrité des données et les balises SEO. Exécuté par la CI. |

Seul `validate.py` fonctionne de façon autonome sur le dépôt, sans dépendance :

```bash
python tools/validate.py
```
