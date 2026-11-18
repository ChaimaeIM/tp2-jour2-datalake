# Configuration du flux NiFi

Relevé via l'API REST de NiFi 2.12.0 le 17/11/2026.

## GetFile

- Type : `org.apache.nifi.processors.standard.GetFile`
- Bundle : `nifi-standard-nar` 2.12.0
- État : RUNNING, validation : VALID

| Propriété | Valeur |
|---|---|
| Input Directory | /home/chaimae_imrani/data/nifi/input |
| File Filter | [^\.].* |
| Batch Size | 10 |
| Keep Source File | false |
| Recurse Subdirectories | false |
| Polling Interval | 30 sec |
| Ignore Hidden Files | true |
| Minimum File Age | 0 sec |
| Minimum File Size | 0 B |

Relations : success (auto-terminate : False)

## PutHDFS

- Type : `org.apache.nifi.processors.hadoop.PutHDFS`
- Bundle : `nifi-hadoop-nar` 2.12.0
- État : RUNNING, validation : VALID

| Propriété | Valeur |
|---|---|
| Hadoop Configuration Resources | /home/chaimae_imrani/opt/hadoop/etc/hadoop/core-site.xml,/home/chaimae_imrani/opt/hadoop/etc/hadoop/hdfs-site.xml |
| Directory | /retail-lake/raw/nifi |
| Conflict Resolution Strategy | fail |
| Append Mode | DEFAULT |
| Writing Strategy | writeAndRename |
| Compression Codec | NONE |
| Ignore Locality | false |
| Resource Transfer Source | FLOWFILE_CONTENT |

Relations : failure (auto-terminate : False), success (auto-terminate : False)

## LogAttribute

- Type : `org.apache.nifi.processors.standard.LogAttribute`
- Bundle : `nifi-standard-nar` 2.12.0
- État : RUNNING, validation : VALID

| Propriété | Valeur |
|---|---|
| Log Level | info |
| Log Payload | false |
| Attributes to Log Regular Expression | .* |
| Log FlowFile Properties | true |
| Output Format | Line per Attribute |
| Character Set | UTF-8 |

Relations : success (auto-terminate : False)

## Connexions

| Source | Relation | Destination |
|---|---|---|
| LogAttribute | success | Funnel |
| PutHDFS | success | Funnel |
| GetFile | success | PutHDFS |
| PutHDFS | failure | LogAttribute |
