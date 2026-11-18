# Environnement Hadoop et Java

Relevé du 17/11/2026, WSL Ubuntu 24.04.1.

## Java 17 (Hadoop)
```
$ /home/chaimae_imrani/java/jdk-17/bin/java -version
openjdk version "17.0.21" 2026-10-20
OpenJDK Runtime Environment Temurin-17.0.21+9 (build 17.0.21+9)
OpenJDK 64-Bit Server VM Temurin-17.0.21+9 (build 17.0.21+9, mixed mode, sharing)
```

## Java 21 (NiFi)
```
$ /home/chaimae_imrani/java/jdk-21/bin/java -version
openjdk version "21.0.13" 2026-10-20 LTS
OpenJDK Runtime Environment Temurin-21.0.13+9 (build 21.0.13+9-LTS)
OpenJDK 64-Bit Server VM Temurin-21.0.13+9 (build 21.0.13+9-LTS, mixed mode, sharing)
```

## Version Hadoop
```
$ hdfs version
Hadoop 3.5.0
Source code repository https://github.com/apache/hadoop.git -r dbcc7cd797100e6b32cd84f85b53a5193a5f9af0
Compiled by cnauroth on 2026-03-24T16:56Z
Compiled on platform linux-x86_64
Compiled with protoc 3.25.5
From source with checksum 64582ed0a62a169c39a19c734a8f33b5
This command was run using /home/chaimae_imrani/opt/hadoop-3.5.0/share/hadoop/common/hadoop-common-3.5.0.jar
```

## Processus Java Hadoop
```
$ /home/chaimae_imrani/java/jdk-17/bin/jps -l
597 org.apache.hadoop.hdfs.server.namenode.NameNode
601 org.apache.hadoop.hdfs.server.datanode.DataNode
3433 jdk.jcmd/sun.tools.jps.Jps
1961 org.apache.nifi.NiFi
```

## Services NiFi
```
$ bash -c ps -eo args | grep org.apache.nifi.NiFi | grep -v grep | cut -c1-120
your 131072x1 screen size is bogus. expect trouble
/home/chaimae_imrani/java/jdk-21/bin/java --class-path /home/chaimae_imrani/opt/nifi-2.12.0/lib/jul-to-slf4j-2.0.19.jar:
```

## Version NiFi (lib)
```
$ bash -c ls /home/chaimae_imrani/opt/nifi-2.12.0/lib | grep -E '^nifi-(hadoop|standard)-(nar|libraries-nar)' 
nifi-hadoop-libraries-nar-2.12.0.nar
nifi-hadoop-nar-2.12.0.nar
nifi-standard-nar-2.12.0.nar
```

## Configuration core-site.xml
```
$ cat /home/chaimae_imrani/opt/hadoop/etc/hadoop/core-site.xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
```

## Configuration hdfs-site.xml
```
$ cat /home/chaimae_imrani/opt/hadoop/etc/hadoop/hdfs-site.xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///home/chaimae_imrani/hadoop-data/namenode</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///home/chaimae_imrani/hadoop-data/datanode</value>
  </property>
</configuration>
```
