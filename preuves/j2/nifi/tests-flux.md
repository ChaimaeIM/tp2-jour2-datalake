# Tests du flux GetFile vers PutHDFS

Date : 17/11/2026. Flux exécuté sur NiFi 2.12.0 (Java 21), HDFS 3.5.0 (Java 17), WSL Ubuntu 24.04.1.

Le détail de la configuration est dans `configuration-flux.md`. La provenance est dans `provenance-events.json`, et les extraits du journal dans `journal-extraits.txt`.

## Test 1 : transfert nominal

| Élément | Résultat |
|---|---|
| Fichier source | Copie de travail de `store.dat`, 3386 octets, placée dans `~/data/nifi/input/` |
| Lecture par GetFile | Événement RECEIVE à 15:45:25 |
| Envoi par PutHDFS | Événement SEND vers `hdfs://localhost:9000/retail-lake/raw/nifi/store.dat` à 15:45:26 |
| Dossier d'entrée après lecture | Vide (`Keep Source File = false`) |
| Présence dans HDFS | `/retail-lake/raw/nifi/store.dat`, 3386 octets |
| Intégrité | SHA-256 identique à la source (`a936bc38...1808ef`) |
| Résultat | Réussi |

## Test 2 : erreur contrôlée (conflit de nom)

| Élément | Résultat |
|---|---|
| Action | Même fichier redéposé dans le dossier d'entrée |
| Lecture par GetFile | Événement RECEIVE à 15:46:25 |
| Comportement PutHDFS | Fichier pénalisé et routé vers `failure`, motif : « file with same name already exists » |
| Traitement de l'échec | `LogAttribute` journalise le FlowFile à 15:46:55 |
| Dans HDFS | Une seule copie, inchangée (3386 octets, 15:45) |
| Résultat | Échec identifié et contenu sans écrasement |

Le FlowFile en échec est resté visible dans le journal. Il n'a pas été supprimé, comme le demande le sujet.

## Captures commentées

- `01-canvas-flux.png` : canvas NiFi. GetFile, PutHDFS et LogAttribute sont en marche. La file `success` de PutHDFS contient 1 FlowFile (3,31 Ko) : le transfert est en cours ou terminé vers le Funnel, comme décrit dans `flux-nifi.md`.
- `03-configuration-puthdfs.png` : propriétés de PutHDFS. `Directory` vaut `/retail-lake/raw/nifi` et `Conflict Resolution Strategy` vaut `fail`, comme prévu dans le sujet. La propriété `Hadoop Configuration Resources` pointe vers `core-site.xml` et `hdfs-site.xml`.
- `04-provenance.png` : quatre événements pour le fichier `store.dat`. Deux RECEIVE (GetFile, 15:45:25 et 15:46:25) et un SEND suivi d'un ATTRIBUTES_MODIFIED (PutHDFS, 15:45:26). Le second RECEIVE correspond au test d'erreur contrôlée : le fichier est lu, puis refusé par PutHDFS.
- `../hdfs/05-hdfs-raw-nifi.png` : `store.dat` présent dans `/retail-lake/raw/nifi`, taille 3,31 Ko, réplication 1, propriétaire `chaimae_imrani`. Le fichier est bien arrivé dans HDFS.
- `../hdfs/02-namenode-overview.png` : interface du NameNode, version 3.5.0, safe mode désactivé, 2 blocs. Le cluster est en état actif.

## Captures (liste initiale)

- `01-canvas-flux.png` : canvas NiFi du flux GetFile, PutHDFS, LogAttribute, avec les files et les compteurs.

Les données de configuration et de provenance sont aussi fournies en texte et en JSON.

## Ce qui n'a pas été fait
- Test de droits sur le dossier d'entrée : non réalisé pour ne pas altérer le reste de l'environnement.
