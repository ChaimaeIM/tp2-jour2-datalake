# Tableau des erreurs et corrections

Date : 17/11/2026. Chaque erreur rencontrée pendant le TP est consignée ici, avec sa cause et sa correction.

| # | Moment | Erreur observée | Cause | Correction | Preuve |
|---|---|---|---|---|---|
| 1 | Installation | `sudo` demande un mot de passe, `apt` impossible | Pas de droits root configurés dans WSL | Installation de tout dans l'espace utilisateur : JDK Temurin 17 et 21, Hadoop et NiFi dans `~/opt` | `preuves/j2/hadoop/environnement.md` |
| 2 | Démarrage HDFS | `start-dfs.sh` impossible, pas de sshd | Pas de root pour installer et lancer OpenSSH | Démarrage direct des daemons : `hdfs --daemon start namenode` et `datanode` | `docs/operations/decouverte-hadoop-hdfs.md` |
| 3 | Démarrage HDFS | NameNode et DataNode arrêtés peu après le démarrage (SIGHUP) | Les daemons étaient rattachés à la session WSL qui s'est fermée | Relance avec `setsid -f` pour les détacher du terminal | `preuves/j2/hdfs/sorties-commandes.md` |
| 4 | Dépôt UC-03 | `hdfs dfs -put` sans message, fichier absent, puis `Connection refused` sur `localhost:9000` | Le NameNode était arrêté (erreur 3), le `put` précédent ne pouvait pas aboutir | Relance des daemons, puis nouveau dépôt | Journal `commandes-hdfs.md` |
| 5 | Dépôt UC-03 | `put: No such file or directory` alors que le fichier existe | Chemin `/mnt/c/...` contenant un espace, lu par le client local | Copie du fichier dans `~/kit-copy/`, dépôt depuis la copie, SHA-256 comparé avant et après | `preuves/j2/hdfs/sorties-commandes.md` |
| 6 | Flux NiFi | Le processeur `PutHDFS` n'existe pas dans la liste des types | Les NAR Hadoop ne sont pas dans la distribution binaire 2.12.0 | Ajout des NAR officiels de la même version (`nifi-hadoop-nar` et `nifi-hadoop-libraries-nar` 2.12.0) depuis Maven Central, puis redémarrage | `preuves/j2/nifi/configuration-flux.md` |
| 7 | Flux NiFi | `success` de PutHDFS et LogAttribute reste invalide (non connecté, non auto-terminé) | L'API REST 2.12.0 n'a pas persisté le paramètre d'auto-terminate (tentatives avec `autoTerminatedRelationships` et `relationships`) | Connexion de `success` vers un Funnel, pour que le flux soit valide. Écart documenté dans `flux-nifi.md` | `ingestion/nifi/flux-getfile-puthdfs.json` |
| 8 | Flux NiFi | Dossier d'entrée `/data/nifi/input` impossible à créer | Création dans `/` réservée à root | Dossier placé dans `~/data/nifi/` (input, archive, error) | `preuves/j2/nifi/configuration-flux.md` |
| 9 | Test d'erreur | Le fichier redéposé n'est pas écrit dans HDFS | Comportement attendu : stratégie `fail` sur un fichier de même nom | Routage vers `failure`, puis `LogAttribute`. Conservé comme test contrôlé | `preuves/j2/nifi/journal-extraits.txt`, `docs/ingestion/flux-nifi.md` |
| 10 | Sécurité | Le mot de passe généré par NiFi s'est affiché dans une sortie de commande | Masquage `sed` mal écrit pour le format `Generated Password [...]` | Mot de passe NiFi remplacé le 17/11/2026 (`nifi.sh set-single-user-credentials`), nouvelle connexion vérifiée (HTTP 201). Identifiants stockés hors du dépôt, dans `~/.nifi-credentials` (mode 600) | Aucune trace dans le dépôt |

## Points à retenir

- Les erreurs 1 à 3 viennent de l'environnement, pas du flux.
- L'erreur 6 demande de vérifier la liste des composants avant de construire le flux.
- L'erreur 7 est un écart réel avec le sujet. Le flux fonctionne, mais le succès s'accumule dans le Funnel au lieu de disparaître.
- L'erreur 10 doit être traitée avant tout partage du dépôt.
