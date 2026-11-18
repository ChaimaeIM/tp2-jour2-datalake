# Commandes HDFS exécutées

Journal des commandes du TP Jour 2 (UC-03). Pour chaque commande, coller la sortie réelle dans la colonne de résultat. Une ligne vide signifie que la commande n'a pas encore été exécutée.

Environnement : Ubuntu, Hadoop 3.5.0, Java 17. Date d'exécution : à renseigner.

| Étape | Commande | Résultat | Erreur éventuelle |
|---|---|---|---|
| Accès | `hdfs dfsadmin -report` | | |
| Accès | `hdfs dfs -ls /` | | |
| Arborescence | `ingestion/scripts/hdfs_setup.sh` | | |
| Dépôt | `hdfs dfs -put <copie de store.dat> /retail-lake/raw/tpcxbb/initial/` | `-rw-r--r-- 1 chaimae_imrani supergroup 3.3 K 2026-11-17 15:33 /retail-lake/raw/tpcxbb/initial/store.dat` (put exit=0) | Première tentative depuis le chemin `/mnt/c` : échec côté client local. Relancé depuis une copie dans `~/kit-copy`, SHA-256 vérifié avant dépôt. |
| Contrôle | `tests/hdfs/verify_storage.sh ~/kit-copy/store.dat /retail-lake/raw/tpcxbb/initial/store.dat` | OK présence, OK taille 3386 octets, OK SHA-256 a936bc38…1808ef (exit=0) | |
| Incident | Arrêt des daemons HDFS et NiFi à la fermeture de la session WSL (SIGHUP) | Relance avec `setsid -f` | Corrigé |
| Vérification | `hdfs dfs -ls -h /retail-lake/raw/tpcxbb/initial` | | |
| Vérification | `hdfs dfs -du -h /retail-lake` | | |
| Contrôle | `tests/hdfs/verify_storage.sh <chemin_local_reel> /retail-lake/raw/tpcxbb/initial/<fichier>` | | |
| Permissions | `hdfs dfs -ls /retail-lake` | | |

Le chemin local doit correspondre à un fichier réellement fourni dans le kit. Aucun nom de fichier n'est déduit de l'exemple du sujet.
