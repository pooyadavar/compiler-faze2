@echo off
set ANTLR_JAR=..\antlr-4.13.1-complete.jar
set GRAMMAR=ObfuMiniC
set OUTPUT_DIR=..\obfuscator\parser

if not exist %ANTLR_JAR% (
    echo [ERROR] ANTLR jar not found at %ANTLR_JAR%
    exit /b 1
)

if not exist %OUTPUT_DIR% (
    mkdir %OUTPUT_DIR%
)

java -jar %ANTLR_JAR% -Dlanguage=Python3 %GRAMMAR%.g4 -visitor -o %OUTPUT_DIR%

echo [OK] ANTLR parser generated at %OUTPUT_DIR%
