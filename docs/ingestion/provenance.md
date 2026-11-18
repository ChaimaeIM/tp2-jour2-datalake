# Provenance des données

Date : 17/11/2026.

La provenance répond à trois questions : d'où vient le fichier, quelle est sa copie dans HDFS, et qui l'a déposée, quand et avec quels outils.

## Informations conservées

| Information | Source de l'information | Où elle est conservée |
|---|---|---|
| Nom du fichier source | Inventaire (`inventory.py`) | `docs/ingestion/inventaire-sources.md` |
| Chemin local de la source | Inventaire | Même fichier |
| Taille en octets | Inventaire, `stat` | Même fichier |
| Empreinte SHA-256 | Inventaire, `sha256sum` | Même fichier |
| Chemin HDFS de destination | Commande `hdfs dfs` ou PutHDFS | `preuves/j2/hdfs/` ou `preuves/j2/nifi/` |
| Résultat du contrôle de stockage | `tests/hdfs/verify_storage.sh` | `preuves/j2/hdfs/` |
| Date du dépôt | Journal de la commande ou de NiFi | `/retail-lake/logs/` (copie) et preuves |
| Identifiant FlowFile et événements | Provenance NiFi | Capture dans `preuves/j2/nifi/` |
| Versions des outils | Relevé d'environnement | `docs/operations/environnement-j2.md` |

## Exemple réel : store.dat

| Information | Valeur |
|---|---|
| Source | `retail_project/data/store/store.dat` (3386 octets) |
| Copie de travail UC-03 | `~/kit-copy/store.dat`, SHA-256 identique à la source |
| Dépôt UC-03 | `/retail-lake/raw/tpcxbb/initial/store.dat`, 15:33, `hdfs dfs -put` |
| Dépôt UC-04 | `/retail-lake/raw/nifi/store.dat`, 15:45, PutHDFS, FlowFile avec événements RECEIVE puis SEND |
| Preuves | `preuves/j2/hdfs/sorties-commandes.md`, `preuves/j2/nifi/provenance-events.json` |

## Règles

- La source originale n'est jamais modifiée ni déplacée.
- Le SHA-256 relie la source à sa copie. Un dépôt est considéré conforme quand la taille et le SHA-256 correspondent.
- Une copie locale n'est pas une preuve de dépôt HDFS. La preuve est la sortie de `hdfs dfs -ls` et le résultat de `verify_storage.sh`.
- Un fichier de démonstration généré pour un test doit porter un nom ou une mention qui indique qu'il est synthétique.
