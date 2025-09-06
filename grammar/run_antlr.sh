#!/bin/bash

ANTLR_JAR=../antlr-4.13.1-complete.jar
GRAMMAR=ObfuMiniC
OUTPUT_DIR=../obfuscator/parser

if [ ! -f "$ANTLR_JAR" ]; then
  echo 
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

java -jar "$ANTLR_JAR" -Dlanguage=Python3 "${GRAMMAR}.g4" -visitor -o "$OUTPUT_DIR"

echo 