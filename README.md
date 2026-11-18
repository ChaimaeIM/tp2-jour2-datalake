# Retail Intelligence Platform : TP Jour 2

Hadoop, HDFS et ingestion des données (UC-03 et UC-04).

| | |
|---|---|
| Auteur | CHAIMAE IMRANI |
| Formation | IPSSI Nice, Mastère Développement, Data & IA, 5e année |
| Identifiant TP | TP-J2-UC03-UC04 |
| Date de rédaction | 17/11/2026 |

## Objet du dépôt

Ce dépôt regroupe le travail du Jour 2 sur la plateforme Retail Intelligence. Il couvre deux choses : le stockage de la donnée dans un Data Lake HDFS, et le flux d'ingestion qui doit alimenter ce stockage avec NiFi.

Le sujet travaille sur le jeu synthétique TPCx-BB. Le but n'est pas de lancer le benchmark, mais de stocker proprement des données réelles, de garder leur provenance et de contrôler ce qui arrive dans HDFS.

## Concepts

### Hadoop et HDFS

HDFS est le système de fichiers distribué de Hadoop. Il s'appuie sur deux types de services :

- le **NameNode** tient les métadonnées : arborescence, droits, emplacement des blocs. Il ne stocke pas les données.
- les **DataNodes** stockent les blocs de données et signalent au NameNode ce qu'ils contiennent.

Un fichier est découpé en **blocs** (128 Mo par défaut). Chaque bloc est copié sur plusieurs DataNodes : c'est la **réplication**. Avec une réplication de 3, un fichier survit à la perte d'un nœud. En mode pseudo-distribué, comme dans ce TP, la réplication est à 1 : il n'y a aucune tolérance à la panne. Ce mode sert à apprendre les commandes, pas à produire.

### Data Lake et zones

Un Data Lake range la donnée par zones, selon son niveau de transformation :

| Zone | Rôle |
|---|---|
| Raw | Copie de la source, telle que reçue. Jamais modifiée. |
| Bronze | Donnée ingérée, format homogène, provenance ajoutée. |
| Silver | Donnée nettoyée et conforme (Jour 3). |
| Gold | Agrégats métier (Jour 3). |
| Quality | Résultats des contrôles. |
| Logs | Journaux d'ingestion et de contrôle. |

La zone Raw est la plus importante : elle permet de rejouer toute la chaîne sans retélécharger la source, et de prouver ce qui a été reçu.

### Apache NiFi

NiFi déplace et route la donnée. Ses éléments de base :

- **FlowFile** : le contenu d'un fichier, plus ses attributs (nom, chemin, UUID).
- **Processor** : une opération (lire un fichier, écrire dans HDFS, router).
- **Connection** : le lien entre deux processeurs. Elle transporte les FlowFiles et porte une file d'attente.
- **Process Group** : un conteneur pour regrouper les éléments d'un flux.
- **Controller Service** : un service partagé entre processeurs (par exemple une configuration Hadoop).
- **Provenance Repository** : l'historique de chaque événement sur chaque FlowFile. C'est lui qui permet de reconstituer le parcours d'un fichier.

### Deux méthodes de dépôt

Le TP présente volontairement deux façons de déposer un fichier dans HDFS :

- **UC-03, dépôt manuel** : `hdfs dfs -put` vers `/retail-lake/raw/tpcxbb/initial/`. Sert à apprendre les commandes HDFS.
- **UC-04, dépôt automatisé** : un flux NiFi `GetFile` vers `PutHDFS`, vers `/retail-lake/raw/nifi/`. Sert à automatiser le transfert, sans relancer une commande pour chaque fichier.

Les deux destinations sont différentes pour ne pas écraser le premier dépôt.

## Ce qui a été réalisé

| Élément | Statut | Où le trouver |
|---|---|---|
| Fiche d'environnement | Relevée. Hadoop 3.5.0 et NiFi 2.12.0 installés et démarrés dans WSL Ubuntu. | `docs/operations/environnement-j2.md`, `docs/operations/decouverte-hadoop-hdfs.md`, `preuves/j2/hadoop/` |
| Script de création de l'arborescence HDFS | Exécuté. Arborescence créée et vérifiée avec `hdfs dfs -ls -R`. | `ingestion/scripts/hdfs_setup.sh` |
| Architecture du Data Lake et convention de nommage | Rédigée. | `docs/architecture/architecture-data-lake.md` |
| Script d'inventaire des fichiers sources | Écrit, 8 tests unitaires passés. | `ingestion/scripts/inventory.py`, `tests/ingestion/test_inventory.py` |
| Script de contrôle de stockage HDFS | Exécuté sur `store.dat` : présence, taille et SHA-256 OK. | `tests/hdfs/verify_storage.sh` |
| Inventaire des fichiers TPCx-BB | Réalisé : 36 fichiers relevés (`data/` et `data_refresh/`). Noms de colonnes non déduits, les `.dat` n'ont pas d'en-tête. | `docs/ingestion/inventaire-sources.md`, `docs/ingestion/inventaire-brut.md` |
| Dépôt HDFS (UC-03) | Réalisé pour `store.dat` (3386 octets). Contrôle présence, taille et SHA-256 : OK. | `preuves/j2/hdfs/commandes-hdfs.md` |
| Flux NiFi GetFile vers PutHDFS | Construit et exécuté : transfert nominal OK, erreur contrôlée OK. Écart : `success` relié à un Funnel, l'auto-terminate n'ayant pas été appliqué via l'API. | `docs/ingestion/flux-nifi.md`, `ingestion/nifi/flux-getfile-puthdfs.json`, `preuves/j2/nifi/` |
| Gestion d'erreur et procédure de reprise | Erreur contrôlée exécutée (conflit de nom). Procédure rédigée. Tableau des erreurs complété. | `docs/operations/procedures-reprise.md`, `docs/operations/erreurs-et-corrections.md`, `preuves/j2/nifi/tests-flux.md` |
| Provenance | Événements réels récupérés via l'API NiFi (RECEIVE, SEND, ATTRIBUTES_MODIFIED). | `docs/ingestion/provenance.md`, `preuves/j2/nifi/provenance-events.json` |
| Réponses aux questions de recul | Rédigées. | `docs/questions-de-recul.md` |

Les preuves sont des sorties texte, JSON et captures d'écran, rangées dans `preuves/j2/`. La capture du canvas NiFi est dans `preuves/j2/nifi/01-canvas-flux.png`, et celle de l'interface NameNode (version 3.5.0, safe mode désactivé, 2 blocs) dans `preuves/j2/hdfs/02-namenode-overview.png`. La capture du dossier `/retail-lake/raw/nifi` contenant `store.dat` (3,31 Ko, répliqué 1 fois) est dans `preuves/j2/hdfs/05-hdfs-raw-nifi.png`. Les propriétés de PutHDFS sont dans `preuves/j2/nifi/03-configuration-puthdfs.png`, et les événements de provenance dans `preuves/j2/nifi/04-provenance.png`.

## Structure du dépôt

```
retail-intelligence-platform/
├── docs/
│   ├── architecture/
│   │   └── architecture-data-lake.md
│   ├── ingestion/
│   │   ├── flux-nifi.md
│   │   ├── inventaire-sources.md
│   │   └── provenance.md
│   ├── operations/
│   │   ├── decouverte-hadoop-hdfs.md
│   │   ├── decouverte-nifi.md
│   │   ├── environnement-j2.md
│   │   ├── erreurs-et-corrections.md
│   │   └── procedures-reprise.md
│   └── questions-de-recul.md
├── ingestion/
│   ├── nifi/
│   │   └── flux-getfile-puthdfs.json   export du flux GetFile vers PutHDFS
│   └── scripts/
│       ├── hdfs_setup.sh      création de l'arborescence HDFS
│       └── inventory.py       inventaire lecture seule des sources
├── tests/
│   ├── hdfs/
│   │   └── verify_storage.sh  contrôle présence, taille et SHA-256 dans HDFS
│   └── ingestion/
│       └── test_inventory.py  tests unitaires de l'inventaire
├── preuves/
│   └── j2/
│       ├── hadoop/            captures de l'environnement Hadoop
│       ├── hdfs/              journal des commandes HDFS
│       └── nifi/              captures du flux et de la provenance
└── README.md
```

## Reproduire le travail

Prérequis : Ubuntu avec SSH local, Java 17 (Hadoop) et Java 21 (NiFi), Hadoop 3.5.0 et NiFi 2.12.0 installés. Le kit TPCx-BB fourni par le formateur.

```bash
# 1. Vérifier l'environnement
java -version
hadoop version
jps

# 2. Démarrer HDFS (Java 17), en daemons détachés (pas de SSH)
source ~/tp2-env.sh
export JAVA_HOME=$JAVA_HOME_HADOOP
setsid -f hdfs namenode > ~/opt/hadoop/logs/nn-run.out 2>&1 < /dev/null
setsid -f hdfs datanode > ~/opt/hadoop/logs/dn-run.out 2>&1 < /dev/null
hdfs dfsadmin -report

# 3. Créer l'arborescence du Data Lake
ingestion/scripts/hdfs_setup.sh

# 4. Inventorier les sources (lecture seule)
python3 ingestion/scripts/inventory.py /chemin/du/kit > docs/ingestion/inventaire-brut.md

# 5. Déposer un fichier réel (UC-03)
hdfs dfs -put /chemin/reel/fichier.csv /retail-lake/raw/tpcxbb/initial/
tests/hdfs/verify_storage.sh /chemin/reel/fichier.csv /retail-lake/raw/tpcxbb/initial/fichier.csv

# 6. Flux NiFi (UC-04) : démarrer NiFi avec Java 21, puis importer
#    ingestion/nifi/flux-getfile-puthdfs.json (ou recréer le flux selon docs/ingestion/flux-nifi.md)
export JAVA_HOME=$JAVA_HOME_NIFI
setsid -f ~/opt/nifi/bin/nifi.sh run > ~/opt/nifi/logs/nifi-run.out 2>&1 < /dev/null

# 7. Arrêt : flux NiFi (GetFile), puis NiFi, puis HDFS
~/opt/nifi/bin/nifi.sh stop
hdfs --daemon stop datanode
hdfs --daemon stop namenode
```

Chemins HDFS utilisés :

- `/retail-lake/raw/tpcxbb/initial` : dépôt UC-03
- `/retail-lake/raw/nifi` : dépôt UC-04
- `/retail-lake/logs`, `/retail-lake/quality`, `/retail-lake/bronze/tpcxbb`, `/retail-lake/silver`, `/retail-lake/gold` : zones préparées pour le Jour 3

Pour les tests unitaires du script d'inventaire, lancer depuis la racine du dépôt :

```bash
python3 tests/ingestion/test_inventory.py
```

## Limites

- L'environnement est mono-nœud et pseudo-distribué. Ce n'est pas un cluster de production : la réplication est à 1 et il n'y a aucune haute disponibilité.
- L'origine exacte du kit (version, paramètre de volume) n'est pas documentée dans le dossier. À confirmer avec le formateur.
- Hadoop 3.5.0 et NiFi 2.12.0 sont installés dans WSL Ubuntu, dans l'espace utilisateur (sans sudo). HDFS tourne en daemons, sans SSH.
- Le flux a un écart avec le sujet : la relation `success` est reliée à un Funnel, pas auto-terminée. Détails dans `docs/ingestion/flux-nifi.md`.
- Un seul fichier du kit est déposé (`store.dat`). C'est le minimum du socle. Le reste du kit n'est pas déposé.
- Le contrôle SHA-256 relit le fichier entier depuis HDFS. C'est acceptable pour un TP, pas pour de gros volumes.

## Sécurité

Aucun mot de passe, jeton ou identifiant généré par NiFi n'est versionné dans ce dépôt. Les identifiants de l'interface NiFi sont lus dans les journaux locaux au premier démarrage, et doivent rester hors du dépôt.
