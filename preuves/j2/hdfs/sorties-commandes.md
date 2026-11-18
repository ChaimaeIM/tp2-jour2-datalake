# Sorties des commandes HDFS

Relevé du 17/11/2026, WSL Ubuntu 24.04.1, Hadoop 3.5.0, Java 17. Commandes lancées une à une, sorties brutes.

## Accès et état du cluster
```
$ hdfs dfsadmin -report
Configured Capacity: 1081101176832 (1006.85 GB)
Present Capacity: 1016726113629 (946.90 GB)
DFS Remaining: 1016726061056 (946.90 GB)
DFS Used: 52573 (51.34 KB)
DFS Used%: 0.00%
Replicated Blocks:
	Under replicated blocks: 0
	Blocks with corrupt replicas: 0
	Missing blocks: 0
	Missing blocks (with replication factor 1): 0
	Badly Distributed Blocks: 0
	Low redundancy blocks with highest priority to recover: 0
	Pending deletion blocks: 0
Erasure Coded Block Groups: 
	Low redundancy block groups: 0
	Block groups with corrupt internal blocks: 0
	Missing block groups: 0
	Badly Distributed Blocks: 0
	Low redundancy blocks with highest priority to recover: 0
	Pending deletion blocks: 0

-------------------------------------------------
Live datanodes (1):

Name: 127.0.0.1:9866 (localhost)
Hostname: DESKTOP-H2NU8K1.
Decommission Status : Normal
Configured Capacity: 1081101176832 (1006.85 GB)
DFS Used: 52573 (51.34 KB)
Non DFS Used: 9382707875 (8.74 GB)
DFS Remaining: 1016726061056 (946.90 GB)
DFS Used%: 0.00%
DFS Remaining%: 94.05%
Configured Cache Capacity: 0 (0 B)
Cache Used: 0 (0 B)
Cache Remaining: 0 (0 B)
Cache Used%: 100.00%
Cache Remaining%: 0.00%
Xceivers: 0
Last contact: Tue Nov 17 15:47:45 CET 2026
Last Block Report: Tue Nov 17 15:32:42 CET 2026
Num of Blocks: 2


```

## Racine HDFS
```
$ hdfs dfs -ls /
Found 1 items
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake
```

## Arborescence du Data Lake
```
$ hdfs dfs -ls -R /retail-lake
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/bronze
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/bronze/tpcxbb
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/gold
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/logs
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/quality
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/raw
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:45 /retail-lake/raw/nifi
-rw-r--r--   1 chaimae_imrani supergroup       3386 2026-11-17 15:45 /retail-lake/raw/nifi/store.dat
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/raw/tpcxbb
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:33 /retail-lake/raw/tpcxbb/initial
-rw-r--r--   1 chaimae_imrani supergroup       3386 2026-11-17 15:33 /retail-lake/raw/tpcxbb/initial/store.dat
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/raw/tpcxbb/refresh
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/silver
```

## Taille des données
```
$ hdfs dfs -du -h /retail-lake
0      0      /retail-lake/bronze
0      0      /retail-lake/gold
0      0      /retail-lake/logs
0      0      /retail-lake/quality
6.6 K  6.6 K  /retail-lake/raw
0      0      /retail-lake/silver
```

## Fichier déposé (UC-03)
```
$ hdfs dfs -ls -h /retail-lake/raw/tpcxbb/initial
Found 1 items
-rw-r--r--   1 chaimae_imrani supergroup      3.3 K 2026-11-17 15:33 /retail-lake/raw/tpcxbb/initial/store.dat
```

## Fichier déposé par NiFi (UC-04)
```
$ hdfs dfs -ls -h /retail-lake/raw/nifi
Found 1 items
-rw-r--r--   1 chaimae_imrani supergroup      3.3 K 2026-11-17 15:45 /retail-lake/raw/nifi/store.dat
```

## Taille et lecture de l'entrée
```
$ hdfs dfs -stat %b octets /retail-lake/raw/tpcxbb/initial/store.dat
3386 octets
```

## Premières lignes lues depuis HDFS
```
$ bash -c hdfs dfs -cat /retail-lake/raw/tpcxbb/initial/store.dat | head -3
0|AAAAAAAAAAAAAAAA|2000-08-02||71238|Forest|217|8891512|8AM-12AM|Joshua Watson|6|Unknown|realms sublate quickly outside the epitaphs; evenly silent patterns boost! th|Randy King|1|Unknown|1|Unknown|916|1st|Boulevard|XF|Post Oak|Hinsdale County|CO|47562|United States|-7|0.06
1|AAAAAAAAAAAAAAAB|2000-07-03||18994|Hillside|244|8751339|8AM-4PM|Gary Gold|3|Unknown|close escapades across the carefully ironic grouches shall have to lose into the sauternes: sl|John Green|1|Unknown|1|Unknown|696|3rd 4th|Blvd|gcg5eGNxs|Jerusalem|Union County|TN|80145|United States|-6|0.03
2|AAAAAAAAAAAAAAAC|2000-09-01||8900|Sherwood|266|5913334|8AM-4PM|James Anderson|6|Unknown|frays may kindle over the bold ironic epitaphs! slow quick multipliers maintain among t|Raymond Kitchens|1|Unknown|1|Unknown|293|Main Fourteenth|Ct.|8pCGst|Mount Vernon|Sierra County|CA|97832|United States|-8|0.07
```

## Copie vers bronze
```
$ hdfs dfs -cp /retail-lake/raw/tpcxbb/initial/store.dat /retail-lake/bronze/tpcxbb/store.dat
```

## Contrôle de la copie bronze
```
$ hdfs dfs -ls -h /retail-lake/bronze/tpcxbb
Found 1 items
-rw-r--r--   1 chaimae_imrani supergroup      3.3 K 2026-11-17 15:48 /retail-lake/bronze/tpcxbb/store.dat
```

## Suppression contrôlée de la copie bronze
```
$ hdfs dfs -rm /retail-lake/bronze/tpcxbb/store.dat
Deleted /retail-lake/bronze/tpcxbb/store.dat
```

## Récupération du fichier depuis HDFS et comparaison
```
$ bash -c rm -rf $HOME/kit-restore && mkdir -p $HOME/kit-restore && hdfs dfs -get /retail-lake/raw/tpcxbb/initial/store.dat $HOME/kit-restore/ && sha256sum $HOME/kit-restore/store.dat /home/chaimae_imrani/kit-copy/store.dat
a936bc38692bdddc222cf86d08ed9d0feb761af26769212d789cf6729d1808ef  /home/chaimae_imrani/kit-restore/store.dat
a936bc38692bdddc222cf86d08ed9d0feb761af26769212d789cf6729d1808ef  /home/chaimae_imrani/kit-copy/store.dat
```

## Permissions de l'arborescence
```
$ hdfs dfs -ls /retail-lake
Found 6 items
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/bronze
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/gold
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/logs
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/quality
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/raw
drwxr-xr-x   - chaimae_imrani supergroup          0 2026-11-17 15:30 /retail-lake/silver
```
