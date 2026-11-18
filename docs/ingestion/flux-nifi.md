# Flux NiFi : GetFile vers PutHDFS

Date : 17/11/2026.

Statut : flux construit et exécuté sur NiFi 2.12.0. Deux tests réalisés (transfert nominal, erreur contrôlée). Un écart avec le sujet sur la relation `success` de PutHDFS, détaillé plus bas.

Fichiers liés :
- `ingestion/nifi/flux-getfile-puthdfs.json` : export du groupe racine, importable dans NiFi.
- `preuves/j2/nifi/configuration-flux.md` : propriétés relevées via l'API REST.
- `preuves/j2/nifi/tests-flux.md` : résultats des tests.
- `preuves/j2/nifi/provenance-events.json` : événements de provenance.
- `preuves/j2/nifi/journal-extraits.txt` : extraits du journal NiFi.

## Schéma

```
GetFile ──success──> PutHDFS ──success──> Funnel (écart, voir ci-dessous)
                        │
                        └──failure──> LogAttribute ──success──> Funnel
```

Le flux obligatoire compte deux processeurs. Le troisième (LogAttribute) traite la relation `failure`, comme le demande le sujet. UpdateAttribute et RouteOnAttribute relèvent de l'étape 12 et ne sont pas réalisés.

## Dossiers utilisés

| Dossier | Rôle |
|---|---|
| `~/data/nifi/input` | Entrée de GetFile. Ne contient que la copie de travail du fichier de test. |
| `~/data/nifi/archive` | Créé, non utilisé par le flux obligatoire. |
| `~/data/nifi/error` | Créé, non utilisé par le flux obligatoire. |
| `/retail-lake/raw/nifi` | Destination HDFS. Distincte de `raw/tpcxbb/initial`, qui contient le dépôt UC-03. |

Le sujet prévoit `/data/nifi/`. Ce dossier est sous `~` car sa création dans `/` demande les droits root.

Le fichier envoyé par NiFi est une copie de travail. L'original et le dépôt UC-03 ne sont pas touchés.

## Processeurs

### GetFile

| Propriété | Valeur | Raison |
|---|---|---|
| Input Directory | `/home/chaimae_imrani/data/nifi/input` | Dossier d'entrée. |
| Keep Source File | `false` | Le fichier est consommé après lecture. |
| Recurse Subdirectories | `false` | Pas de parcours récursif. |
| Polling Interval | 30 sec (défaut) | Le fichier est repris au prochain passage. |

### PutHDFS

| Propriété | Valeur | Raison |
|---|---|---|
| Hadoop Configuration Resources | `/home/chaimae_imrani/opt/hadoop/etc/hadoop/core-site.xml,/home/chaimae_imrani/opt/hadoop/etc/hadoop/hdfs-site.xml` | Accès au NameNode `hdfs://localhost:9000`. |
| Directory | `/retail-lake/raw/nifi` | Destination du dépôt. |
| Conflict Resolution Strategy | `fail` | Un fichier déjà présent fait échouer le transfert. Rien n'est écrasé. |

PutHDFS n'est pas dans la distribution binaire 2.12.0. Il a fallu ajouter `nifi-hadoop-nar` et `nifi-hadoop-libraries-nar` en version 2.12.0, depuis Maven Central (voir `docs/operations/erreurs-et-corrections.md`, erreur 6).

## Écart avec le sujet : relation success de PutHDFS

Le sujet demande de configurer `success` en Auto-terminate. Via l'API REST de NiFi 2.12.0, le paramètre d'auto-terminate n'a pas été pris en compte : les requêtes sont acceptées, mais la relation reste non connectée et non terminée, et le processeur reste invalide.

Pour que le flux soit valide, `success` de PutHDFS et de LogAttribute est relié à un Funnel. Conséquence : chaque FlowFile réussi reste visible dans la file du Funnel au lieu de disparaître. C'est la seule différence avec le comportement attendu. Dans l'interface graphique, la même opération devrait permettre l'auto-terminate : à refaire si l'on dispose d'un accès UI.

## Ordre de démarrage et d'arrêt

1. Démarrer HDFS (daemons NameNode et DataNode).
2. Démarrer NiFi avec Java 21, en mode détaché.
3. Démarrer PutHDFS et LogAttribute, puis GetFile.
4. Arrêt : arrêter GetFile, attendre que les files se vident, arrêter NiFi, puis arrêter HDFS.

## Tests

Voir `preuves/j2/nifi/tests-flux.md`.

- Transfert nominal : le fichier arrive dans `/retail-lake/raw/nifi/`, taille et SHA-256 identiques à la source.
- Erreur contrôlée : un fichier de même nom est refusé par PutHDFS et routé vers `failure`, puis journalisé par LogAttribute.

## Gestion des erreurs

La relation `failure` n'est pas supprimée. Les FlowFiles en échec sont routés vers LogAttribute, qui les journalise. Ils ne sont supprimés qu'après examen.

Ne pas relancer le flux plusieurs fois sans comprendre le premier résultat : cela crée des doublons ou des conflits de noms.

## Provenance

Chaque FlowFile produit trois événements : RECEIVE (GetFile), SEND (PutHDFS) et ATTRIBUTES_MODIFIED (PutHDFS). Le fichier `preuves/j2/nifi/provenance-events.json` les contient avec l'identifiant FlowFile, le nom, l'heure et le chemin HDFS.

## Solution de repli

Non nécessaire : le flux a été exécuté sur l'environnement prévu. Le contrôle de stockage est couvert par `tests/hdfs/verify_storage.sh`.
