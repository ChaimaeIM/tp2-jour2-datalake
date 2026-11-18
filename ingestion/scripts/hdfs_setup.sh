#!/usr/bin/env bash
# Crée l'arborescence du Data Lake dans HDFS.
#
# Sans danger à relancer : mkdir -p ne fait rien si le dossier existe déjà.
# Ne formate pas le NameNode et ne supprime rien.
#
# Usage (après start-dfs.sh, avec Java 17) :
#   ingestion/scripts/hdfs_setup.sh

set -euo pipefail

if ! command -v hdfs >/dev/null 2>&1; then
  echo "hdfs introuvable : vérifier HADOOP_HOME, PATH et JAVA_HOME" >&2
  exit 1
fi

ROOT=/retail-lake
DIRS=(
  "$ROOT/raw/tpcxbb/initial"
  "$ROOT/raw/tpcxbb/refresh"
  "$ROOT/raw/nifi"
  "$ROOT/bronze/tpcxbb"
  "$ROOT/silver"
  "$ROOT/gold"
  "$ROOT/quality"
  "$ROOT/logs"
)

for dir in "${DIRS[@]}"; do
  hdfs dfs -mkdir -p "$dir"
  echo "ok  $dir"
done

echo
hdfs dfs -ls -R "$ROOT"
