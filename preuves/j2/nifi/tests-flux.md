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

## Ce qui n'a pas été fait

- Captures d'écran de l'interface NiFi : l'environnement n'a pas de navigateur piloté. Les données de configuration et de provenance sont fournies en texte et en JSON à la place.
- Test de droits sur le dossier d'entrée : non réalisé pour ne pas altérer le reste de l'environnement.
