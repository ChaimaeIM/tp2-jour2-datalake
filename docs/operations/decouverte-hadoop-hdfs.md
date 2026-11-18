# Fiche de découverte Hadoop et HDFS

Date : 17/11/2026. Relevé sur WSL Ubuntu 24.04.1 (installation dans l'espace utilisateur, sans sudo).

Les sorties brutes sont dans `preuves/j2/hadoop/environnement.md` et `preuves/j2/hdfs/sorties-commandes.md`.

## Installation

| Élément | Valeur |
|---|---|
| Version Hadoop | 3.5.0 |
| Chemin | `~/opt/hadoop` (lien vers `~/opt/hadoop-3.5.0`) |
| Java utilisé par Hadoop | OpenJDK 17, `~/java/jdk-17` |
| Configuration | `core-site.xml`, `hdfs-site.xml` dans `~/opt/hadoop/etc/hadoop/` |
| Stockage NameNode | `~/hadoop-data/namenode` |
| Stockage DataNode | `~/hadoop-data/datanode` |

Le sujet prévoit `/opt/hadoop`. Le dossier est sous `~` faute de droits root, le reste de la configuration suit le sujet.

## Configuration utilisée

- `fs.defaultFS` = `hdfs://localhost:9000`
- `dfs.replication` = 1 (mode pseudo-distribué, une seule machine)

## État des composants

| Composant | État relevé | Remarque |
|---|---|---|
| NameNode | En cours d'exécution | Lancé avec `hdfs --daemon` puis `setsid -f`. |
| DataNode | En cours d'exécution, 1 nœud vivant | Adresse 127.0.0.1:9866. |
| Blocs | 2 blocs, 0 sous-répliqué, 0 corrompu, 0 manquant | Relevé par `hdfs dfsadmin -report`. |
| Espace | 1006,85 Go configurés, 946,90 Go restants | Données utilisées : 51 Ko. |

Le démarrage via `start-dfs.sh` n'a pas été utilisé : il passe par SSH, et sshd n'est pas installé (pas de sudo). Les deux daemons sont lancés directement avec `hdfs --daemon start`.

## Rôle des composants

- **NameNode** : tient les métadonnées (arborescence, droits, emplacement des blocs). Sans lui, les blocs ne sont pas accessibles.
- **DataNode** : stocke les blocs sur disque et rapporte au NameNode ce qu'il contient.

## Type d'environnement

Architecture mono-nœud pseudo-distribuée : NameNode et DataNode sur la même machine, réplication à 1. C'est un environnement pédagogique. Il n'offre aucune tolérance à la panne et ne représente pas un cluster de production.

## Erreurs de démarrage rencontrées

Voir `docs/operations/erreurs-et-corrections.md` : arrêt des daemons à la fermeture de la session WSL (SIGHUP), relancé ensuite en mode détaché.
