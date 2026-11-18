#!/usr/bin/env bash
# Contrôle un fichier stocké dans HDFS par rapport à sa source locale.
#
# Usage :
#   tests/hdfs/verify_storage.sh <fichier_local> <chemin_hdfs>
#
# Contrôles : présence dans HDFS, taille identique, SHA-256 identique.
# Le SHA-256 est calculé sur le contenu relu depuis HDFS (hdfs dfs -cat).
# Acceptable pour un TP ; pour de gros volumes, il faudrait un autre mécanisme.
# Le script est en lecture seule.
#
# Code retour : 0 si tout est conforme, 1 sinon, 2 si mauvais usage.

set -uo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 <fichier_local> <chemin_hdfs>" >&2
  exit 2
fi

local_file="$1"
hdfs_path="$2"
failures=0

if [ ! -r "$local_file" ]; then
  echo "FAIL  source locale absente ou illisible : $local_file"
  exit 1
fi

if ! hdfs dfs -test -e "$hdfs_path"; then
  echo "FAIL  chemin HDFS absent : $hdfs_path"
  exit 1
fi

echo "OK    présence : $hdfs_path"
hdfs dfs -ls -h "$hdfs_path"

local_size=$(stat -c %s "$local_file")
hdfs_size=$(hdfs dfs -stat %b "$hdfs_path")
if [ "$local_size" = "$hdfs_size" ]; then
  echo "OK    taille identique : $local_size octets"
else
  echo "FAIL  taille locale=$local_size, HDFS=$hdfs_size"
  failures=$((failures + 1))
fi

local_hash=$(sha256sum "$local_file" | awk '{print $1}')
hdfs_hash=$(hdfs dfs -cat "$hdfs_path" | sha256sum | awk '{print $1}')
if [ "$local_hash" = "$hdfs_hash" ]; then
  echo "OK    SHA-256 identique : $local_hash"
else
  echo "FAIL  SHA-256 différent"
  echo "      local : $local_hash"
  echo "      hdfs  : $hdfs_hash"
  failures=$((failures + 1))
fi

exit "$failures"
