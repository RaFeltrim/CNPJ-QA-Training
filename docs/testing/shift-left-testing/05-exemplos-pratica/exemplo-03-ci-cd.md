# ⚙️ Exemplo 03: Pipeline CI/CD

> **Objetivo**: Demonstrar configuração completa de pipeline CI/CD com princípios Shift Left

## 📋 Contexto

Este exemplo apresenta o pipeline GitHub Actions do projeto CNPJ-QA-Training, explicando como cada estágio implementa princípios de Shift Left Testing.

## 🏗️ Arquitetura do Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PIPELINE SHIFT LEFT                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  TRIGGER: push/PR para master                                           │
│                                                                          │
│  ┌─────────────────┐                                                    │
│  │ quality-checks  │ ← PRIMEIRO: Verificações rápidas                   │
│  │ • lint (flake8) │   Tempo: ~30s                                      │
│  │ • format (black)│   Fail Fast: Código mal formatado para aqui       │
│  └────────┬────────┘                                                    │
│           │ needs                                                        │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │   unit-tests    │ ← SEGUNDO: Testes unitários                        │
│  │ • matrix 3.8-11 │   Tempo: ~2min                                     │
│  │ • pytest + cov  │   Fail Fast: Bug lógico para aqui                 │
│  └────────┬────────┘                                                    │
│           │ needs                                                        │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │integration-tests│ ← TERCEIRO: Testes de integração                   │
│  │ • mocks         │   Tempo: ~3min                                     │
│  │ • e2e (select)  │   Fail Fast: Problemas de integração              │
│  └────────┬────────┘                                                    │
│           │ needs                                                        │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │    security     │ ← QUARTO: Verificações de segurança                │
│  │ • bandit (SAST) │   Tempo: ~1min                                     │
│  │ • safety (deps) │   Fail Fast: Vulnerabilidades                      │
│  └─────────────────┘                                                    │
│                                                                          │
│  TOTAL: ~7min (se tudo passar)                                          │
│  FAIL FAST: Feedback em segundos se houver problema                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 📄 Arquivo de Workflow Completo

```yaml
# .github/workflows/ci-cd.yml

name: CI/CD Pipeline

# ============================================================
# TRIGGERS
# ============================================================
on:
  push:
    branches: [master, main]
    paths-ignore:
      - '**.md'
      - 'docs/**'
  pull_request:
    branches: [master, main]
  schedule:
    # Roda diariamente às 6h UTC para verificar dependências
    - cron: '0 6 * * *'

# ============================================================
# VARIÁVEIS DE AMBIENTE GLOBAIS
# ============================================================
env:
  PYTHON_DEFAULT_VERSION: '3.11'
  COVERAGE_THRESHOLD: 80

# ============================================================
# JOBS
# ============================================================
jobs:
  # ----------------------------------------------------------
  # JOB 1: QUALITY CHECKS
  # Executa primeiro para feedback rápido
  # ----------------------------------------------------------
  quality-checks:
    name: 🔍 Quality Checks
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout código
        uses: actions/checkout@v4
      
      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_DEFAULT_VERSION }}
          cache: 'pip'
      
      - name: 📦 Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install flake8 black isort
      
      - name: 🔎 Lint com flake8
        run: |
          # Erros críticos que quebram o build
          flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
          # Warnings que geram alerta mas não quebram
          flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      
      - name: 🎨 Verificar formatação com black
        run: black --check --diff src/ tests/
      
      - name: 📋 Verificar imports com isort
        run: isort --check-only --diff src/ tests/

  # ----------------------------------------------------------
  # JOB 2: UNIT TESTS
  # Roda após quality-checks passar
  # ----------------------------------------------------------
  unit-tests:
    name: 🧪 Unit Tests (Python ${{ matrix.python-version }})
    needs: quality-checks
    runs-on: ubuntu-latest
    
    strategy:
      fail-fast: true  # Para imediatamente se um falhar
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
      - name: 📥 Checkout código
        uses: actions/checkout@v4
      
      - name: 🐍 Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: 📦 Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist
      
      - name: 🧪 Executar testes unitários
        run: |
          pytest tests/ \
            --ignore=tests/test_integration.py \
            -v \
            --tb=short \
            --cov=src \
            --cov-report=xml \
            --cov-report=term-missing \
            --cov-fail-under=${{ env.COVERAGE_THRESHOLD }} \
            -n auto  # Paralelo
      
      - name: 📊 Upload cobertura para Codecov
        if: matrix.python-version == env.PYTHON_DEFAULT_VERSION
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          flags: unittests
          fail_ci_if_error: true
          token: ${{ secrets.CODECOV_TOKEN }}

  # ----------------------------------------------------------
  # JOB 3: INTEGRATION TESTS
  # Roda após unit-tests passar
  # ----------------------------------------------------------
  integration-tests:
    name: 🔗 Integration Tests
    needs: unit-tests
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout código
        uses: actions/checkout@v4
      
      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_DEFAULT_VERSION }}
          cache: 'pip'
      
      - name: 📦 Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest responses
      
      - name: 🔗 Executar testes de integração
        run: |
          pytest tests/test_integration.py \
            -v \
            --tb=long \
            -m "not e2e"  # Exclui E2E em PRs

  # ----------------------------------------------------------
  # JOB 4: SECURITY CHECKS
  # Roda após integration-tests passar
  # ----------------------------------------------------------
  security:
    name: 🔒 Security Checks
    needs: integration-tests
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout código
        uses: actions/checkout@v4
      
      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_DEFAULT_VERSION }}
          cache: 'pip'
      
      - name: 📦 Instalar ferramentas de segurança
        run: |
          python -m pip install --upgrade pip
          pip install bandit safety pip-audit
      
      - name: 🔍 SAST com Bandit
        run: |
          bandit -r src/ \
            -f json \
            -o bandit-report.json \
            --severity-level medium \
            --confidence-level medium \
            || true  # Não falha, apenas reporta
      
      - name: 📋 Safety Check (dependências)
        run: |
          pip install -r requirements.txt
          safety check --full-report
        continue-on-error: true
      
      - name: 🔎 pip-audit
        run: pip-audit
        continue-on-error: true
      
      - name: 📤 Upload relatório de segurança
        uses: actions/upload-artifact@v4
        with:
          name: security-reports
          path: |
            bandit-report.json

  # ----------------------------------------------------------
  # JOB 5: BUILD & PUBLISH (apenas em push para master)
  # ----------------------------------------------------------
  build:
    name: 📦 Build Package
    needs: security
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/master'
    
    steps:
      - name: 📥 Checkout código
        uses: actions/checkout@v4
      
      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_DEFAULT_VERSION }}
      
      - name: 📦 Build package
        run: |
          pip install build
          python -m build
      
      - name: 📤 Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  # ----------------------------------------------------------
  # JOB 6: E2E TESTS (Apenas em schedule)
  # ----------------------------------------------------------
  e2e-tests:
    name: 🌐 E2E Tests
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule'
    
    steps:
      - name: 📥 Checkout código
        uses: actions/checkout@v4
      
      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_DEFAULT_VERSION }}
      
      - name: 📦 Instalar dependências
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: 🌐 Executar testes E2E
        env:
          RECEITA_API_KEY: ${{ secrets.RECEITA_API_KEY }}
        run: |
          pytest tests/ -m "e2e" -v --tb=long
        continue-on-error: true  # Não bloqueia schedule
```

## 🎯 Princípios Shift Left Aplicados

### 1. Fail Fast - Ordem dos Jobs

```yaml
jobs:
  quality-checks:    # ~30s - Mais rápido
    ...
  unit-tests:        # ~2min - Segundo
    needs: quality-checks
  integration-tests: # ~3min - Terceiro
    needs: unit-tests
  security:          # ~1min - Quarto
    needs: integration-tests
```

**Por quê?** Problemas de lint são detectados em 30 segundos, não em 7 minutos.

### 2. Matrix Testing - Múltiplas Versões

```yaml
strategy:
  fail-fast: true
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11']
```

**Por quê?** Encontra incompatibilidades antes de chegar nos usuários.

### 3. Cobertura com Threshold

```yaml
--cov-fail-under=${{ env.COVERAGE_THRESHOLD }}
```

**Por quê?** Impede merge de código sem testes adequados.

### 4. Segurança Integrada

```yaml
security:
  needs: integration-tests
  steps:
    - bandit   # SAST
    - safety   # Dependências
    - pip-audit
```

**Por quê?** Vulnerabilidades são encontradas antes do deploy.

### 5. Testes E2E Separados

```yaml
e2e-tests:
  if: github.event_name == 'schedule'
```

**Por quê?** Testes lentos/flaky não bloqueiam PRs mas ainda são executados.

## 📊 Configuração Adicional: pytest.ini

```ini
# pytest.ini

[pytest]
# Diretórios de teste
testpaths = tests

# Padrões de arquivo
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers customizados
markers =
    smoke: Testes de sanidade rápidos
    unit: Testes unitários
    integration: Testes de integração
    e2e: Testes end-to-end
    slow: Testes lentos

# Opções padrão
addopts = 
    -v
    --tb=short
    --strict-markers
    -ra

# Cobertura
cov-report = term-missing
cov-fail-under = 80

# Warnings
filterwarnings =
    error
    ignore::DeprecationWarning
```

## 📊 Configuração: pyproject.toml

```toml
# pyproject.toml

[tool.black]
line-length = 127
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 127
known_first_party = ["cnpj_validator"]

[tool.bandit]
exclude_dirs = ["tests", "docs"]
skips = ["B101"]  # assert ok em testes

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## 🔧 Scripts de Suporte

### run-tests.bat (Windows)

```batch
@echo off
REM scripts/run-tests.bat

echo ====================================
echo    CNPJ Validator - Test Runner
echo ====================================

REM Ativa ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo.
echo [1/4] Quality Checks...
echo --------------------------------
python -m flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Lint falhou!
    exit /b 1
)

python -m black --check src/ tests/
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Formatacao incorreta! Execute: black src/ tests/
    exit /b 1
)

echo.
echo [2/4] Unit Tests...
echo --------------------------------
python -m pytest tests/ --ignore=tests/test_integration.py -v --tb=short --cov=src --cov-report=term-missing
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Testes unitarios falharam!
    exit /b 1
)

echo.
echo [3/4] Integration Tests...
echo --------------------------------
python -m pytest tests/test_integration.py -v --tb=short
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Testes de integracao falharam!
    exit /b 1
)

echo.
echo [4/4] Security Checks...
echo --------------------------------
python -m bandit -r src/ -ll
python -m safety check

echo.
echo ====================================
echo    TODOS OS TESTES PASSARAM!
echo ====================================
```

### run-tests.sh (Linux/Mac)

```bash
#!/bin/bash
# scripts/run-tests.sh

set -e  # Exit on error

echo "===================================="
echo "   CNPJ Validator - Test Runner"
echo "===================================="

# Ativa ambiente virtual se existir
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo ""
echo "[1/4] Quality Checks..."
echo "--------------------------------"
python -m flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source
python -m black --check src/ tests/

echo ""
echo "[2/4] Unit Tests..."
echo "--------------------------------"
python -m pytest tests/ \
    --ignore=tests/test_integration.py \
    -v \
    --tb=short \
    --cov=src \
    --cov-report=term-missing \
    --cov-fail-under=80

echo ""
echo "[3/4] Integration Tests..."
echo "--------------------------------"
python -m pytest tests/test_integration.py -v --tb=short

echo ""
echo "[4/4] Security Checks..."
echo "--------------------------------"
python -m bandit -r src/ -ll
python -m safety check || true

echo ""
echo "===================================="
echo "   TODOS OS TESTES PASSARAM!"
echo "===================================="
```

## 📈 Métricas do Pipeline

| Estágio | Tempo Médio | Objetivo |
|---------|-------------|----------|
| quality-checks | 30s | < 1min |
| unit-tests | 2min | < 5min |
| integration-tests | 3min | < 5min |
| security | 1min | < 2min |
| **Total** | **~7min** | **< 15min** |

## 🔗 Próximos Passos

- [Exemplo 04: Automação Completa](exemplo-04-automacao.md)
- [Exercícios Práticos](../03-exercicios/index.md)

---

| Anterior | Índice | Próximo |
|----------|--------|---------|
| [← Integration](exemplo-02-integration.md) | [📚 Principal](../README.md) | [Automação →](exemplo-04-automacao.md) |
