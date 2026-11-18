# Procédure de reprise après échec d'ingestion

Date : 17/11/2026. Cette procédure couvre le flux GetFile vers PutHDFS.

## 1. Identifier un traitement en échec

- Dans NiFi, le processeur PutHDFS affiche des erreurs, ou des FlowFiles restent dans la relation `failure`.
- Les journaux NiFi (`/opt/nifi/logs/nifi-app.log`) contiennent le motif de l'erreur.
- Un dépôt est réussi si le fichier est bien présent dans `/retail-lake/raw/nifi` avec la bonne taille et le bon SHA-256.

## 2. Retrouver le fichier source

- Le nom du fichier est dans les attributs du FlowFile (événements de provenance).
- L'original se trouve hors de `/data/nifi/input`, car GetFile consomme la copie de travail. On le retrouve grâce au nom et au SHA-256 inscrits dans `docs/ingestion/inventaire-sources.md`.

## 3. Éviter les doublons

- Vérifier avant toute relance : `hdfs dfs -ls /retail-lake/raw/nifi`.
- Comparer le SHA-256 du fichier source avec celui de la copie HDFS, avec `tests/hdfs/verify_storage.sh`.
- Si le fichier est déjà présent et conforme, ne pas relancer.
- La stratégie `fail` de PutHDFS empêche l'écrasement, mais pas une copie sous un autre nom. Il faut donc contrôler le contenu avant de relancer.

## 4. Relancer le traitement

1. Corriger la cause (droits, chemin, service arrêté).
2. Replacer une copie de travail dans `/data/nifi/input`. Ne jamais déplacer l'original.
3. Démarrer GetFile. Surveiller les compteurs et la file.

## 5. Vérifier le résultat

```bash
tests/hdfs/verify_storage.sh /chemin/copie_source.csv /retail-lake/raw/nifi/<nom_du_fichier>
```

Le script doit afficher trois lignes `OK` : présence, taille, SHA-256. Noter la date et le résultat dans `preuves/j2/hdfs/`.
