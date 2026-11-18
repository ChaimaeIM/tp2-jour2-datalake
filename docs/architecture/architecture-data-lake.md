# Architecture du Data Lake

Date : 17/11/2026. Projet : Retail Intelligence Platform, TP Jour 2.

## Arborescence HDFS

```
/retail-lake/
├── raw/
│   ├── tpcxbb/
│   │   ├── initial/        dépôt initial, fichiers TPCx-BB tels que reçus
│   │   └── refresh/        dépôts ultérieurs (nouveaux lots)
│   └── nifi/               destination du flux NiFi (UC-04), distincte de l'UC-03
├── bronze/
│   └── tpcxbb/             données ingérées, format homogène, sans transformation métier
├── silver/                 données nettoyées et conformes (Jour 3)
├── gold/                   agrégats métier prêts à l'usage (Jour 3)
├── quality/                rapports de contrôle qualité
└── logs/                   journaux d'ingestion et de contrôle
```

Le script `ingestion/scripts/hdfs_setup.sh` crée cette arborescence. La structure suit la proposition du sujet. Elle n'est pas imposée par Hadoop.

## Rôle des zones

| Zone | Contenu | Règle |
|---|---|---|
| Raw | Copie des fichiers source, sans modification | Jamais écrasée. Un nouveau lot va dans `refresh/`. |
| Bronze | Données ingérées, avec métadonnées de provenance | Pas de filtrage métier. |
| Silver | Données nettoyées, typées, dédoublonnées | Produite à partir de Bronze uniquement. |
| Gold | Indicateurs et agrégats pour les usages métier | Produite à partir de Silver. |
| Quality | Résultats des contrôles (comptages, rejets, anomalies) | Un rapport par exécution. |
| Logs | Journaux d'exécution des flux et des scripts | Ne jamais supprimer sans archivage. |

## Raw et Bronze

Raw garde le fichier exactement comme il a été reçu. Si une transformation est fausse, on peut la refaire depuis Raw sans retélécharger la source. Le SHA-256 relevé à l'inventaire permet de prouver que la copie Raw n'a pas changé.

Bronze est la première version exploitable : même contenu, format homogène, provenance ajoutée. Les transformations métier arrivent plus tard, en Silver.

## Pourquoi séparer les zones

Séparer les données brutes, les données transformées, les contrôles et les journaux permet :

- de rejouer un traitement depuis la source ;
- de savoir à quel niveau une anomalie est apparue ;
- de donner des droits d'accès différents selon la zone ;
- de ne pas mélanger un résultat de contrôle avec une donnée métier.

## Convention de nommage

Modèle proposé pour les fichiers déposés :

```
<source>_<domaine>_<date-de-reception>_<lot>.<extension>
```

Exemple de forme (aucun fichier de ce nom n'existe dans le projet) : `tpcxbb_ventes-magasin_20261117_initial.csv`.

- `source` : jeu d'origine (ici `tpcxbb`).
- `domaine` : domaine métier du kit (ventes, retours, produits...).
- `date-de-reception` : date au format AAAAMMJJ, si elle est connue.
- `lot` : `initial` ou `refresh`, ou un numéro de lot.

Les noms sont en minuscules, sans espaces ni accents, pour éviter les problèmes côté Linux, HDFS et NiFi.

## Provenance

La provenance est décrite dans `docs/ingestion/provenance.md`. Le lien entre une source et sa copie dans HDFS repose sur le nom, la taille et le SHA-256.
