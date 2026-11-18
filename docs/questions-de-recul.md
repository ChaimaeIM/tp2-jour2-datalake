# Questions de recul

**1. Rôle du NameNode.** Il gère les métadonnées de HDFS : l'arborescence, les noms, les droits, et l'emplacement de chaque bloc. Il ne stocke pas les données elles-mêmes.

**2. NameNode et DataNode.** Le NameNode est le maître et connaît la carte du système de fichiers. Les DataNodes stockent les blocs sur disque et signalent régulièrement au NameNode ce qu'ils contiennent.

**3. Découpage en blocs.** Un fichier est découpé pour être réparti sur plusieurs machines et lu en parallèle. Un bloc est aussi l'unité de réplication. La taille par défaut est de 128 Mo dans Hadoop 3.

**4. Réplication.** Chaque bloc est copié sur plusieurs DataNodes, trois par défaut. Si un nœud tombe, les données restent accessibles. En pseudo-distribué, la réplication est à 1 : il n'y a aucune tolérance à la panne.

**5. Plusieurs zones.** Chaque zone a un rôle : source, données ingérées, données nettoyées, agrégats, contrôles, journaux. On peut rejouer un traitement sans toucher à la source, et donner des droits différents selon la zone.

**6. Données sources dans Raw.** La zone Raw permet de rejouer les transformations, de prouver ce qui a été reçu, et de comparer une copie à sa source grâce au SHA-256.

**7. Rôle d'un FlowFile.** C'est l'unité de donnée qui traverse NiFi : le contenu du fichier, plus des attributs (nom, chemin, UUID, date). Il circule de processeur en processeur.

**8. Processor et Connection.** Un Processor effectue une opération (lire, router, écrire). Une Connection relie deux processeurs, transporte les FlowFiles et porte la file d'attente.

**9. Importance de la provenance.** Le dépôt de provenance enregistre chaque événement sur un FlowFile. Il permet de reconstituer le parcours d'un fichier, de diagnostiquer un échec et de répondre à un audit.

**10. Échec technique et rejet métier.** Un échec technique vient d'un service, d'un réseau ou d'un droit : il se traite par une relance après correction, et il passe par la relation `failure`. Un rejet métier vient d'une donnée qui ne respecte pas les règles (extension, structure, contenu) : il se traite par une correction de la donnée ou de la règle, et il est routé vers un dossier de rejet avec le motif.

**11. Relance sans contrôle des doublons.** Le même fichier peut être écrit deux fois, ou sous deux noms, et être compté deux fois en aval. Un conflit de noms peut aussi écraser une version. Il faut comparer les SHA-256 avant toute relance et garder la stratégie `fail`.

**12. Limites du mono-nœud.** Pas de tolérance à la panne, réplication à 1, pas de vrai parallélisme, un seul disque. Les performances ne sont pas représentatives d'un cluster.

**13. Copie locale et preuve de dépôt.** Une copie locale prouve seulement que le fichier existe sur la machine où elle a été faite. Elle ne dit rien de la présence dans HDFS, de la réplication ou de l'intégrité côté cluster. La preuve vient d'une commande HDFS (`ls`, `stat`, contrôle SHA-256 sur la sortie de `cat`).

**14. Informations à conserver pour reproduire une ingestion.** Le nom et le chemin de la source, sa taille et son SHA-256, la date, les versions des outils (Java, Hadoop, NiFi), les commandes ou le modèle de flux exporté, le chemin de destination HDFS, la stratégie de conflit, et le résultat des contrôles.
