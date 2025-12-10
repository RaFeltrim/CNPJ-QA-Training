#!/bin/bash
# ============================================================================
# Test Hub - Script de Inicialização (Linux/Mac)
# ============================================================================
# 
# Este script automatiza a instalação de dependências e inicialização do hub.
# Execute-o na primeira vez para configurar o ambiente.
#
# Uso:
#     chmod +x start.sh
#     ./start.sh
#
# ============================================================================

echo "============================================================"
echo "   Test Hub - Central de Testes Automatizados"
echo "============================================================"
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado. Instale Python 3.8 ou superior."
    exit 1
fi

echo "[1/3] Verificando ambiente Python..."
python3 --version

# Instala dependências
echo ""
echo "[2/3] Instalando dependências do Test Hub..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao instalar dependências."
    exit 1
fi

# Verifica se pytest-json-report está instalado
if ! pip3 show pytest-json-report &> /dev/null; then
    echo ""
    echo "[INFO] Instalando pytest-json-report para relatórios detalhados..."
    pip3 install pytest-json-report
fi

echo ""
echo "[3/3] Iniciando Test Hub..."
echo ""
echo "============================================================"
echo "   Acesse: http://localhost:5000"
echo "   Pressione Ctrl+C para encerrar"
echo "============================================================"
echo ""

python3 app.py
