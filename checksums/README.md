# Intégrité et authenticité

Ce dossier permet de répondre à deux questions distinctes, qu'il ne faut pas
confondre.

| Question | Ce qui y répond |
|---|---|
| Ce fichier a-t-il été altéré depuis sa publication ? | Les **empreintes** ci-dessous |
| Ce fichier vient-il bien de Service conseils Factero ? | Une **signature**, voir plus bas |

Une empreinte prouve qu'un contenu n'a pas changé. Elle ne prouve pas qui l'a
produit : quiconque modifie un fichier peut recalculer son empreinte. Seule une
signature, adossée à une clé, établit l'origine.

---

## Vérifier l'intégrité

### Toutes les plateformes, sans dépendance

```bash
python tools/gen_checksums.py --verify
```

Recalcule les empreintes de tous les fichiers suivis et les compare au manifeste.
Sortie non nulle en cas d'écart, avec la liste des fichiers concernés.

### Linux et macOS

```bash
sha512sum -c checksums/SHA512SUMS
```

### Windows, PowerShell

```powershell
Get-Content checksums\SHA512SUMS | ForEach-Object {
  $h,$p = $_ -split '\s+',2
  $a = (Get-FileHash $p.Trim() -Algorithm SHA512).Hash.ToLower()
  if ($a -ne $h) { "ECART : $p" }
}
```

### Un seul fichier

```bash
sha512sum data/toutes-correspondances.csv
grep "data/toutes-correspondances.csv" checksums/SHA512SUMS
```

---

## Les algorithmes fournis, et lesquels utiliser

| Fichier | Algorithme | Statut | Usage |
|---|---|---|---|
| `SHA512SUMS` | SHA-512 | **Recommandé** | Référence. Utilisez celui-ci. |
| `SHA256SUMS` | SHA-256 | Recommandé | Compatibilité large de l'écosystème. |
| `manifest.json` | + BLAKE2b-512 | Moderne | RFC 7693, plus rapide à sécurité équivalente. |
| `MD5SUMS` | MD5 | **Obsolète** | Voir l'avertissement ci-dessous. |

### Avertissement sur MD5

**MD5 est cryptographiquement cassé.** Des collisions sont produites en quelques
secondes sur du matériel ordinaire depuis 2008, et des attaques par préfixe choisi
sont documentées. Un attaquant capable de modifier un fichier de ce dépôt peut
fabriquer un contenu différent présentant le **même** MD5.

Le fichier `MD5SUMS` est fourni uniquement pour un contrôle anti-corruption de
transfert, dans des environnements où seul `md5sum` est disponible. Il ne constitue
aucune garantie de sécurité ni d'authenticité. **Ne fondez aucune décision de
confiance dessus.** Utilisez `SHA512SUMS`.

---

## Vérifier l'authenticité

Trois mécanismes, du plus fort au plus simple à mettre en place.

### 1. Attestation de provenance GitHub (sans clé à gérer)

Les publications (*releases*) de ce dépôt sont accompagnées d'une attestation de
provenance signée sans clé via [Sigstore](https://www.sigstore.dev/), rattachée à
l'identité GitHub du dépôt et inscrite au journal de transparence public Rekor.

```bash
gh attestation verify checksums/SHA512SUMS --repo FacteroCanada/tgv-msss-crosswalk
```

C'est la méthode la plus robuste : aucune clé privée à protéger, et toute signature
émise est publiquement auditable.

### 2. Signature GPG détachée du manifeste

Si une signature détachée `SHA512SUMS.asc` est présente :

```bash
gpg --verify checksums/SHA512SUMS.asc checksums/SHA512SUMS
```

Signer un manifeste suffit à couvrir tout le dépôt : le manifeste engage
l'empreinte de chaque fichier.

### 3. Commits signés

```bash
git log --show-signature -1
```

---

## Régénérer après une modification

Toute modification du dépôt invalide le manifeste. Régénérez avant de commiter :

```bash
python tools/gen_checksums.py
```

La chaîne d'intégration continue exécute `--verify` à chaque poussée : un manifeste
périmé fait échouer la validation. C'est volontaire, cela rend visible toute
divergence entre le contenu publié et ses empreintes.

---

## Portée

Le manifeste couvre l'ensemble des fichiers versionnés, à l'exception du répertoire
`.git` et des manifestes eux-mêmes, qui ne peuvent se référencer sans circularité.
Les empreintes portent sur les octets exacts tels que stockés dans le dépôt. Le
fichier `.gitattributes` normalise les fins de ligne en LF, de sorte que les
empreintes sont identiques quelle que soit la plateforme d'extraction.
