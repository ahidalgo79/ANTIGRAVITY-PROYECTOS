@echo off
title OpenCode + Antigravity (Ollama limitado)
color 0B
echo ============================================================
echo   OpenCode + ANTIGRAVITY-PROYECTOS
echo   Ollama con limites de recursos (CPU sin AVX2 / RAM baja)
echo ============================================================
echo.

rem --- Limites de Ollama para evitar congelamiento del sistema ---
set OLLAMA_MAX_LOADED_MODELS=1
set OLLAMA_NUM_PARALLEL=1
set OLLAMA_CONTEXT_LENGTH=2048
set OLLAMA_NUM_THREADS=2
set OLLAMA_KEEP_ALIVE=1m

echo [1/3] Cerrando Ollama si estaba corriendo...
taskkill /f /im ollama.exe >nul 2>&1
taskkill /f /im "ollama app.exe" >nul 2>&1
timeout /t 3 /nobreak >nul

echo [2/3] Iniciando Ollama con limites aplicados...
start "Ollama" ollama serve
timeout /t 6 /nobreak >nul

echo [3/3] Lanzando opencode desde el vault...
cd /d "%USERPROFILE%\Documents\ANTIGRAVITY-PROYECTOS"

if not exist "opencode.json" (
    echo.
    echo AVISO: no se encontro opencode.json en %CD%
    echo Si tu vault esta en otra ruta, edita este archivo (linea cd /d).
    echo.
)

opencode

echo.
echo Sesion de opencode terminada.
echo Ollama queda en segundo plano. Para apagarlo: taskkill /f /im ollama.exe
pause
