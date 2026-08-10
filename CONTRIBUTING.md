# Contribuer

Ce dépôt vit des corrections que ses utilisateurs lui apportent. Une correspondance
contestée est une contribution utile, même sans proposition de remplacement.

## Contester ou proposer une correspondance

Ouvrez une *issue* avec le gabarit « Contester une correspondance ». Précisez la
référence du critère TGV, celle du contrôle cible, et votre argument. Citez le texte
des deux exigences quand c'est possible : c'est ce qui permet de trancher vite.

Les correspondances de ce dépôt ont été produites puis filtrées par une relecture
contradictoire, mais aucun filtre n'est parfait sur 1302 liens. Si vous préparez une
certification et qu'un auditeur a rejeté une équivalence publiée ici, c'est
précisément le retour qui a le plus de valeur.

## Modifier les données

Les fichiers sous `data/` sont générés. Ne les modifiez pas à la main dans une *pull
request* sans le signaler, car la prochaine génération écraserait votre changement.
Décrivez plutôt la correction voulue dans l'issue, elle sera intégrée à la source.

Avant de soumettre, lancez la validation :

```bash
python tools/validate.py
```

Elle vérifie l'intégrité des données, la cohérence entre JSON et CSV, et les balises
des 35 pages du site. La CI exécute la même commande.

## Corriger le site ou la documentation

Les pages HTML sont générées elles aussi. Pour une correction de fond (formulation,
erreur factuelle, lien mort), ouvrez une issue ou une *pull request* décrivant le
changement voulu.

## Ce qui ne sera pas intégré

Le texte des critères de la TGV ne peut pas être modifié : il est reproduit tel que
publié par le MSSS. Si vous constatez un écart avec la publication officielle, c'est
un bogue de notre côté et le signalement est bienvenu. La
[version officielle](https://publications.msss.gouv.qc.ca/msss/document-003757/)
fait toujours foi.
