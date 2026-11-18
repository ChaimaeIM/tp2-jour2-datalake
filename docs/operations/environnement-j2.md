# Fiche d'environnement technique

Relevé du 17/11/2026, sur la machine de rédaction (Windows 11).

Les versions cibles du sujet sont Hadoop 3.5.0 et NiFi 2.12.0, avec Java 17 pour Hadoop et Java 21 pour NiFi. Les versions à retenir sont celles que le formateur valide.

| Élément | Valeur relevée | Remarque |
|---|---|---|
| Système hôte | Windows 11 Home Single Language, 10.0.26200 | |
| Sous-système Linux | WSL 2, distribution Ubuntu | Arrêtée au moment du relevé. Les scripts HDFS et NiFi doivent tourner sous Ubuntu. |
| Java | OpenJDK 17, `~/java/jdk-17` (Temurin), vérifié sous Ubuntu | Utilisé par Hadoop. Le Java de Windows (`C:\java\openjdk\jdk-17`) n'est pas utilisé. |
| Java 21 | OpenJDK 21, `~/java/jdk-21`, vérifié sous Ubuntu | Requis pour NiFi 2.12.0. |
| Hadoop | 3.5.0, installé dans `~/opt/hadoop` (WSL Ubuntu 24.04.1, sans sudo) | Java 17 via `JAVA_HOME` dans `hadoop-env.sh`. Daemons NameNode et DataNode lancés. |
| Apache NiFi | 2.12.0, installé dans `~/opt/nifi` | Lancé avec Java 21, interface sur `https://localhost:8443/nifi/`. |
| Java 17 / 21 | `~/java/jdk-17`, `~/java/jdk-21` (Temurin) | Installés sans apt, faute de sudo. |
| Python | 3.14.3, `C:\Python314\python.exe` | Sert aux scripts d'inventaire et aux tests. |
| Services actifs | Aucun service HDFS ni NiFi | |
| Données | Kit TPCx-BB absent du poste | À récupérer auprès du formateur. |

## Contraintes

- Les scripts `hdfs_setup.sh` et `verify_storage.sh` sont en bash. Ils se lancent sous Ubuntu (WSL ou machine dédiée).
- NiFi écoute en local sur `https://localhost:8443/nifi`. Il ne doit pas être exposé sur le réseau.
- Le NameNode ne doit pas être formaté une seconde fois, car cette opération efface l'espace HDFS.

## Vérifications sous Ubuntu

Relevées le 17/11/2026. Les sorties sont dans `preuves/j2/hadoop/environnement.md` : versions Java 17 et 21, `hdfs version`, `jps`, configuration `core-site.xml` et `hdfs-site.xml`, NAR NiFi Hadoop.
