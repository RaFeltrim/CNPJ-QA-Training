@echo off
REM ============================================================================
REM Test Hub - Script de Inicialização (Windows)
REM ============================================================================
REM 
REM Este script automatiza a instalação de dependências e inicialização do hub.
REM Execute-o na primeira vez para configurar o ambiente.
REM
REM Uso:
REM     start.bat
REM
REM ============================================================================

echo ============================================================
echo    Test Hub - Central de Testes Automatizados
echo ============================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale Python 3.8 ou superior.
    pause
    exit /b 1
)

echo [1/3] Verificando ambiente Python...
python --version

REM Verifica se as dependências estão instaladas
echo.
echo [2/3] Instalando dependencias do Test Hub...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias.
    pause
    exit /b 1
)

REM Verifica se pytest-json-report está instalado (necessário para relatórios detalhados)
pip show pytest-json-report >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INFO] Instalando pytest-json-report para relatorios detalhados...
    pip install pytest-json-report
)

echo.
echo [3/3] Iniciando Test Hub...
echo.
echo ============================================================
echo    Acesse: http://localhost:5000
echo    Pressione Ctrl+C para encerrar
echo ============================================================
echo.

python app.py

pause
