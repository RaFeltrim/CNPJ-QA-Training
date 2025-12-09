#!/bin/bash
# Script para executar testes localmente no Linux/Mac
# Simula pipeline CI/CD

set -e  # Parar em caso de erro

echo "============================================================================"
echo "  CNPJ VALIDATOR - CI/CD LOCAL (Shift Left Testing)"
echo "============================================================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python não encontrado! Instale Python 3.7+"
    exit 1
fi

echo "[1/6] Instalando dependências..."
pip install -q -r requirements.txt
echo "[OK] Dependências instaladas"
echo ""

echo "[2/6] Verificando formatação (Black)..."
if black --check src/cnpj_validator/; then
    echo "[OK] Código formatado corretamente"
else
    echo "[AVISO] Código não está formatado. Execute: black src/cnpj_validator/"
fi
echo ""

echo "[3/6] Executando linting (Flake8)..."
if flake8 src/cnpj_validator/ --max-line-length=100 --statistics; then
    echo "[OK] Linting passou"
else
    echo "[AVISO] Problemas de linting encontrados"
fi
echo ""

echo "[4/6] Executando testes unitários..."
pytest tests/ -v -m "not integration" --tb=short
echo "[OK] Testes unitários passaram"
echo ""

echo "[5/6] Executando testes de integração..."
pytest tests/test_integration.py -v
echo "[OK] Testes de integração passaram"
echo ""

echo "[6/6] Gerando relatório de cobertura..."
pytest --cov=src/cnpj_validator --cov-report=html --cov-report=term-missing
echo "[OK] Relatório gerado em reports/coverage/index.html"
echo ""

echo "============================================================================"
echo "  TODOS OS TESTES PASSARAM! Pipeline Local Completo ✓"
echo "============================================================================"
echo ""
echo "Próximos passos:"
echo "  1. Commit suas mudanças: git add . && git commit -m 'mensagem'"
echo "  2. Push para repositório: git push"
echo "  3. CI/CD remoto será executado automaticamente"
echo ""
