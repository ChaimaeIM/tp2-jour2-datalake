# Inventaire des sources TPCx-BB

Date du relevé : 17/11/2026.

Source : dossier `retail_project` (sous-dossiers `data/` pour le chargement initial et `data_refresh/` pour les lots de rafraîchissement). Le relevé complet, généré par le script, est dans `docs/ingestion/inventaire-brut.md`. Il couvre 36 fichiers : 24 dans `data/`, 12 dans `data_refresh/`.

Les tables présentes correspondent aux domaines listés dans le sujet : magasin, web, retours, produits, clients, magasins, stocks, promotions, navigation web et avis produits.

Les fichiers `.dat` sont séparés par `|` et n'ont pas d'en-tête. Les noms de colonnes ne sont donc pas connus à partir du kit. Le nombre de colonnes est relevé, mais aucun nom n'est déduit.

Provenance : le dossier ne contient ni README ni notice. L'origine exacte (version du générateur, paramètre de scale) reste à confirmer auprès du formateur.

## Méthode

Chaque fichier est inspecté en lecture seule :

```bash
python3 ingestion/scripts/inventory.py /chemin/du/kit/tpcxbb > docs/ingestion/inventaire-brut.md
```

Le script donne le format, la taille, le nombre de lignes, le nombre de colonnes, le SHA-256 et les anomalies (fichier vide, encodage non UTF-8, en-tête dupliqué). Les colonnes et les types sont ensuite relevés à la main, après lecture de l'en-tête.

Les domaines listés dans le sujet (ventes magasin, ventes web, retours, produits, clients, magasins, stocks, promotions, navigation web, avis produits) sont des pistes de recherche. Seuls les fichiers réellement présents sont inscrits ici.

## Matrice d'inventaire

| Fichier | Format | Taille (o) | Lignes | Observations |
|---|---|---:|---:|---|
| store.dat | DAT (séparateur `\|`) | 3386 | 12 | Déposé en UC-03 et en UC-04. 29 colonnes. Pas d'en-tête. |
| store_sales.dat | DAT (séparateur `\|`) | 92764700 | 667579 | 23 colonnes. Pas d'en-tête. Non déposé. |
| web_sales.dat | DAT (séparateur `\|`) | 133790574 | 668052 | 34 colonnes. Pas d'en-tête. Non déposé. |
| customer.dat | DAT (séparateur `\|`) | 13279063 | 99000 | 18 colonnes. Pas d'en-tête. Non déposé. |
| item.dat | DAT (séparateur `\|`) | 6799286 | 17820 | 22 colonnes. Pas d'en-tête. Non déposé. |

Les 36 fichiers sont dans `docs/ingestion/inventaire-brut.md`.

## Fiche par fichier retenu

Une fiche par fichier utilisé pour le dépôt.

| Information | Valeur |
|---|---|
| Nom | store.dat |
| Chemin réel | `retail_project/data/store/store.dat` |
| Format constaté | Texte, séparateur `\|`, un enregistrement par ligne |
| Taille | 3386 octets |
| Structure (nombre de colonnes, noms) | 29 colonnes. Pas d'en-tête, donc pas de noms. |
| Types observés ou déduits | Non déduits. Pas de schéma dans le kit. Les premières lignes montrent des entiers, des codes alphanumériques et des dates. |
| Volume (lignes) | 12 |
| Provenance (kit, version, origine) | Kit `retail_project` fourni pour le TP. Version du générateur non documentée. À confirmer auprès du formateur. |
| Limites | Pas d'en-tête, pas de schéma. Le nombre de colonnes vient du comptage des séparateurs. Aucune anomalie d'encodage. |
| SHA-256 | `a936bc38692bdddc222cf86d08ed9d0feb761af26769212d789cf6729d1808ef` |
