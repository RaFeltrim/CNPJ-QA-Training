@echo off
REM Script para executar testes localmente no Windows
REM Simula pipeline CI/CD

echo ============================================================================
echo   CNPJ VALIDATOR - CI/CD LOCAL (Shift Left Testing)
echo ============================================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado! Instale Python 3.7+
    exit /b 1
)

echo [1/6] Instalando dependencias...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias
    exit /b 1
)
echo [OK] Dependencias instaladas
echo.

echo [2/6] Verificando formatacao (Black)...
black --check src/cnpj_validator/
if errorlevel 1 (
    echo [AVISO] Codigo nao esta formatado. Execute: black src/cnpj_validator/
) else (
    echo [OK] Codigo formatado corretamente
)
echo.

echo [3/6] Executando linting (Flake8)...
flake8 src/cnpj_validator/ --max-line-length=100 --statistics
if errorlevel 1 (
    echo [AVISO] Problemas de linting encontrados
) else (
    echo [OK] Linting passou
)
echo.

echo [4/6] Executando testes unitarios...
pytest tests/ -v -m "not integration" --tb=short
if errorlevel 1 (
    echo [ERRO] Testes unitarios falharam
    exit /b 1
)
echo [OK] Testes unitarios passaram
echo.

echo [5/6] Executando testes de integracao...
pytest tests/test_integration.py -v
if errorlevel 1 (
    echo [ERRO] Testes de integracao falharam
    exit /b 1
)
echo [OK] Testes de integracao passaram
echo.

echo [6/6] Gerando relatorio de cobertura...
pytest --cov=cnpj_validator --cov-report=html --cov-report=term-missing
if errorlevel 1 (
    echo [AVISO] Problemas ao gerar cobertura
) else (
    echo [OK] Relatorio gerado em reports/coverage/index.html
)
echo.

echo ============================================================================
echo   TODOS OS TESTES PASSARAM! Pipeline Local Completo
echo ============================================================================
echo.
echo Proximos passos:
echo   1. Commit suas mudancas: git add . ^&^& git commit -m "mensagem"
echo   2. Push para repositorio: git push
echo   3. CI/CD remoto sera executado automaticamente
echo.
