# Fiche de découverte Apache NiFi

Date : 17/11/2026. Version NiFi 2.12.0, Java 21, WSL Ubuntu 24.04.1.

## Installation et état relevé

| Élément | Valeur |
|---|---|
| Chemin | `~/opt/nifi` (lien vers `~/opt/nifi-2.12.0`) |
| Démarrage | `nifi.sh run` en mode détaché, `JAVA_HOME` sur Java 21 |
| Adresse | `https://localhost:8443/nifi/` (réponse HTTP 200) |
| Authentification | Identifiants générés au premier démarrage, lus dans `nifi-app.log`. Non versionnés. |
| Composants ajoutés | `nifi-hadoop-nar` et `nifi-hadoop-libraries-nar` en 2.12.0, pour PutHDFS |
| Services nécessaires à l'ingestion | HDFS (NameNode, DataNode), accessible sur `hdfs://localhost:9000` |

Le NAR Hadoop n'est pas inclus dans la distribution binaire 2.12.0. Il a été ajouté en version identique depuis Maven Central.

## Concepts et rôle dans le flux

- **FlowFile** : le contenu d'un fichier et ses attributs (nom, chemin, UUID, taille). C'est l'unité qui traverse le flux. Dans le test, le FlowFile contient le fichier `store.dat` (3386 octets).
- **Processor** : une opération. GetFile lit le fichier d'entrée, PutHDFS écrit dans HDFS, LogAttribute journalise un FlowFile en échec.
- **Connection** : le lien entre deux composants. Elle porte la relation (`success` ou `failure`) et une file d'attente visible dans l'interface.
- **Process Group** : le conteneur du flux. Le flux du TP est dans le groupe racine.
- **Controller Service** : un service partagé entre processeurs (par exemple une connexion à un cluster). Le flux du TP n'en utilise pas : PutHDFS reçoit ses fichiers de configuration Hadoop directement dans ses propriétés.
- **Provenance Repository** : l'historique des événements de chaque FlowFile (RECEIVE, SEND, ATTRIBUTES_MODIFIED). Il permet de reconstituer le parcours d'un fichier.

## Relations de sortie

- GetFile : `success`.
- PutHDFS : `success` (dépôt terminé), `failure` (échec d'écriture, par exemple conflit de nom).
- LogAttribute : `success`.

## Sécurité

- L'interface n'est accessible que depuis la machine locale.
- Le mot de passe généré a été exposé dans une sortie de commande pendant le TP. Il a été remplacé le 17/11/2026 (voir `erreurs-et-corrections.md`, erreur 10). Le nouveau est stocké hors du dépôt, dans `~/.nifi-credentials`.
- Aucun identifiant n'est écrit dans le dépôt.
