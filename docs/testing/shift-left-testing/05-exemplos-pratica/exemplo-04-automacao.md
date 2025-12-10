# 🚀 Exemplo 04: Automação Completa

> **Objetivo**: Demonstrar automação end-to-end integrando todos os conceitos Shift Left

## 📋 Contexto

Este exemplo final integra todos os conceitos apresentados em um sistema completo de automação para o projeto CNPJ-QA-Training.

## 🏗️ Arquitetura Completa

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SHIFT LEFT AUTOMATION ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   DEVELOPER                    CI/CD                    MONITORING      │
│   WORKSTATION                  PIPELINE                 & FEEDBACK      │
│                                                                          │
│   ┌─────────────┐             ┌─────────────┐         ┌─────────────┐  │
│   │ Pre-commit  │             │   GitHub    │         │  Dashboard  │  │
│   │ Hooks       │────────────▶│  Actions    │────────▶│  Metrics    │  │
│   │ • lint      │             │  Pipeline   │         │  & Alerts   │  │
│   │ • format    │             │             │         │             │  │
│   │ • secrets   │             │             │         │             │  │
│   └─────────────┘             └─────────────┘         └─────────────┘  │
│                                     │                       │          │
│   ┌─────────────┐                   │                       │          │
│   │ IDE         │                   ▼                       ▼          │
│   │ Extensions  │             ┌─────────────┐         ┌─────────────┐  │
│   │ • Pylance   │             │   Test      │         │  Reports    │  │
│   │ • pytest    │             │   Results   │────────▶│  Badges     │  │
│   │ • coverage  │             │             │         │  Trends     │  │
│   └─────────────┘             └─────────────┘         └─────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Configuração Completa

### 1. Pre-commit Hooks

```yaml
# .pre-commit-config.yaml

# Configuração de pre-commit hooks para Shift Left
# Instalação: pip install pre-commit && pre-commit install

default_stages: [commit]
fail_fast: true

repos:
  # ===== FORMATAÇÃO =====
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
        args: ['--line-length=127']
  
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile=black', '--line-length=127']
  
  # ===== LINTING =====
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=127', '--max-complexity=10']
        additional_dependencies:
          - flake8-docstrings
          - flake8-bugbear
  
  # ===== TYPE CHECKING =====
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        args: ['--ignore-missing-imports']
  
  # ===== SEGURANÇA =====
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
        additional_dependencies: ['bandit[toml]']
  
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
  
  # ===== TESTES RÁPIDOS =====
  - repo: local
    hooks:
      - id: pytest-smoke
        name: Pytest Smoke Tests
        entry: pytest
        args: ['-m', 'smoke', '-x', '-q', '--tb=no']
        language: system
        types: [python]
        pass_filenames: false
        always_run: true
  
  # ===== VALIDAÇÕES GERAIS =====
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
      - id: debug-statements
```

### 2. Makefile para Automação Local

```makefile
# Makefile

.PHONY: help install lint format test test-unit test-integration test-e2e coverage security clean

# Variáveis
PYTHON := python
PYTEST := pytest
COVERAGE_THRESHOLD := 80

# Help
help:
	@echo "CNPJ Validator - Comandos Disponíveis"
	@echo "======================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install     - Instala dependências"
	@echo "  make dev-install - Instala dependências de desenvolvimento"
	@echo ""
	@echo "Qualidade:"
	@echo "  make lint        - Executa linters"
	@echo "  make format      - Formata código"
	@echo "  make type-check  - Verifica tipos"
	@echo ""
	@echo "Testes:"
	@echo "  make test        - Executa todos os testes"
	@echo "  make test-unit   - Executa testes unitários"
	@echo "  make test-int    - Executa testes de integração"
	@echo "  make test-e2e    - Executa testes E2E"
	@echo "  make coverage    - Gera relatório de cobertura"
	@echo ""
	@echo "Segurança:"
	@echo "  make security    - Executa verificações de segurança"
	@echo ""
	@echo "CI/CD:"
	@echo "  make ci          - Executa pipeline completo"
	@echo ""

# Setup
install:
	$(PYTHON) -m pip install --upgrade pip
	pip install -r requirements.txt

dev-install: install
	pip install -r requirements-dev.txt
	pre-commit install

# Qualidade de Código
lint:
	@echo "🔍 Executando linters..."
	flake8 src/ tests/ --count --statistics
	pylint src/ --fail-under=8.0

format:
	@echo "🎨 Formatando código..."
	black src/ tests/
	isort src/ tests/

format-check:
	@echo "🎨 Verificando formatação..."
	black --check --diff src/ tests/
	isort --check-only --diff src/ tests/

type-check:
	@echo "📝 Verificando tipos..."
	mypy src/ --ignore-missing-imports

# Testes
test:
	@echo "🧪 Executando todos os testes..."
	$(PYTEST) tests/ -v --tb=short

test-unit:
	@echo "🧪 Executando testes unitários..."
	$(PYTEST) tests/ \
		--ignore=tests/test_integration.py \
		-v --tb=short \
		-m "not e2e"

test-int:
	@echo "🔗 Executando testes de integração..."
	$(PYTEST) tests/test_integration.py -v --tb=short

test-e2e:
	@echo "🌐 Executando testes E2E..."
	$(PYTEST) tests/ -m "e2e" -v --tb=long

test-smoke:
	@echo "💨 Executando smoke tests..."
	$(PYTEST) tests/ -m "smoke" -x -q

coverage:
	@echo "📊 Gerando relatório de cobertura..."
	$(PYTEST) tests/ \
		--cov=src \
		--cov-report=html \
		--cov-report=xml \
		--cov-report=term-missing \
		--cov-fail-under=$(COVERAGE_THRESHOLD)
	@echo "Relatório HTML gerado em htmlcov/index.html"

# Segurança
security:
	@echo "🔒 Executando verificações de segurança..."
	bandit -r src/ -f json -o reports/bandit.json || true
	safety check --full-report
	pip-audit

secrets-scan:
	@echo "🔑 Verificando secrets..."
	detect-secrets scan --baseline .secrets.baseline

# CI Pipeline Local
ci: format-check lint type-check test-unit test-int security coverage
	@echo ""
	@echo "✅ Pipeline CI completo executado com sucesso!"

# Limpeza
clean:
	@echo "🧹 Limpando arquivos temporários..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Desenvolvimento
run:
	$(PYTHON) -m uvicorn src.api.main:app --reload

# Build
build:
	@echo "📦 Construindo pacote..."
	$(PYTHON) -m build

# Relatórios
report-coverage:
	@echo "📊 Abrindo relatório de cobertura..."
	open htmlcov/index.html || xdg-open htmlcov/index.html

report-security:
	@echo "🔒 Gerando relatório de segurança..."
	bandit -r src/ -f html -o reports/security.html
	@echo "Relatório gerado em reports/security.html"
```

### 3. Script de Automação Completa

```python
#!/usr/bin/env python3
"""
automation.py - Script de automação Shift Left completo.

Este script orquestra todas as verificações de qualidade,
testes e relatórios do projeto CNPJ Validator.

Uso:
    python scripts/automation.py --full      # Pipeline completo
    python scripts/automation.py --quick     # Verificação rápida
    python scripts/automation.py --report    # Gera relatórios
"""

import argparse
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


@dataclass
class StepResult:
    """Resultado de um passo da automação."""
    name: str
    success: bool
    duration: float
    output: str
    error: str = ""


class AutomationRunner:
    """Executor de automação Shift Left."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[StepResult] = []
        self.start_time = time.time()
    
    def run_step(self, name: str, command: List[str], 
                 fail_fast: bool = True) -> StepResult:
        """Executa um passo da automação."""
        print(f"\n{'='*60}")
        print(f"▶ {name}")
        print(f"{'='*60}")
        
        start = time.time()
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos máximo
            )
            
            duration = time.time() - start
            success = result.returncode == 0
            
            step_result = StepResult(
                name=name,
                success=success,
                duration=duration,
                output=result.stdout,
                error=result.stderr
            )
            
            if self.verbose or not success:
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr, file=sys.stderr)
            
            status = "✅ PASSOU" if success else "❌ FALHOU"
            print(f"\n{status} em {duration:.2f}s")
            
            self.results.append(step_result)
            
            if not success and fail_fast:
                print("\n⚠️  Fail Fast: Parando execução devido a falha")
                self.generate_report()
                sys.exit(1)
            
            return step_result
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start
            step_result = StepResult(
                name=name,
                success=False,
                duration=duration,
                output="",
                error="Timeout após 5 minutos"
            )
            self.results.append(step_result)
            print(f"\n❌ TIMEOUT após {duration:.2f}s")
            return step_result
    
    def run_quality_checks(self) -> bool:
        """Executa verificações de qualidade."""
        print("\n" + "="*60)
        print("🔍 FASE 1: QUALITY CHECKS")
        print("="*60)
        
        steps = [
            ("Flake8 - Lint", ["python", "-m", "flake8", "src/", "tests/"]),
            ("Black - Format Check", ["python", "-m", "black", "--check", "src/", "tests/"]),
            ("isort - Import Check", ["python", "-m", "isort", "--check-only", "src/", "tests/"]),
        ]
        
        all_passed = True
        for name, cmd in steps:
            result = self.run_step(name, cmd, fail_fast=False)
            if not result.success:
                all_passed = False
        
        return all_passed
    
    def run_unit_tests(self) -> bool:
        """Executa testes unitários."""
        print("\n" + "="*60)
        print("🧪 FASE 2: UNIT TESTS")
        print("="*60)
        
        result = self.run_step(
            "Pytest - Unit Tests",
            [
                "python", "-m", "pytest", "tests/",
                "--ignore=tests/test_integration.py",
                "-v", "--tb=short",
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-fail-under=80"
            ]
        )
        
        return result.success
    
    def run_integration_tests(self) -> bool:
        """Executa testes de integração."""
        print("\n" + "="*60)
        print("🔗 FASE 3: INTEGRATION TESTS")
        print("="*60)
        
        result = self.run_step(
            "Pytest - Integration Tests",
            [
                "python", "-m", "pytest",
                "tests/test_integration.py",
                "-v", "--tb=short"
            ]
        )
        
        return result.success
    
    def run_security_checks(self) -> bool:
        """Executa verificações de segurança."""
        print("\n" + "="*60)
        print("🔒 FASE 4: SECURITY CHECKS")
        print("="*60)
        
        steps = [
            ("Bandit - SAST", ["python", "-m", "bandit", "-r", "src/", "-ll"]),
            ("Safety - Dependencies", ["python", "-m", "safety", "check"]),
        ]
        
        all_passed = True
        for name, cmd in steps:
            result = self.run_step(name, cmd, fail_fast=False)
            if not result.success:
                all_passed = False
        
        return all_passed
    
    def run_full_pipeline(self) -> bool:
        """Executa pipeline completo."""
        print("\n" + "#"*60)
        print("#" + " "*20 + "SHIFT LEFT PIPELINE" + " "*19 + "#")
        print("#"*60)
        print(f"\nInício: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        phases = [
            ("Quality Checks", self.run_quality_checks),
            ("Unit Tests", self.run_unit_tests),
            ("Integration Tests", self.run_integration_tests),
            ("Security Checks", self.run_security_checks),
        ]
        
        all_passed = True
        for phase_name, phase_func in phases:
            if not phase_func():
                all_passed = False
                # Continua para coletar todos os resultados
        
        self.generate_report()
        
        return all_passed
    
    def run_quick_check(self) -> bool:
        """Executa verificação rápida (smoke tests)."""
        print("\n" + "#"*60)
        print("#" + " "*20 + "QUICK CHECK" + " "*27 + "#")
        print("#"*60)
        
        # Apenas lint e smoke tests
        lint_result = self.run_step(
            "Quick Lint",
            ["python", "-m", "flake8", "src/", "--select=E9,F63,F7,F82"]
        )
        
        test_result = self.run_step(
            "Smoke Tests",
            ["python", "-m", "pytest", "tests/", "-m", "smoke", "-x", "-q"]
        )
        
        return lint_result.success and test_result.success
    
    def generate_report(self) -> None:
        """Gera relatório final."""
        total_time = time.time() - self.start_time
        passed = sum(1 for r in self.results if r.success)
        failed = len(self.results) - passed
        
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL")
        print("="*60)
        
        print(f"\n{'Passo':<40} {'Status':<10} {'Tempo':<10}")
        print("-" * 60)
        
        for result in self.results:
            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"{result.name:<40} {status:<10} {result.duration:.2f}s")
        
        print("-" * 60)
        print(f"\n📈 Resumo:")
        print(f"   Total de passos: {len(self.results)}")
        print(f"   Passou: {passed}")
        print(f"   Falhou: {failed}")
        print(f"   Tempo total: {total_time:.2f}s")
        
        if failed == 0:
            print("\n" + "="*60)
            print("✅ PIPELINE COMPLETO - TODOS OS CHECKS PASSARAM!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print(f"❌ PIPELINE FALHOU - {failed} CHECK(S) COM PROBLEMA")
            print("="*60)
        
        # Salva relatório em JSON
        self._save_json_report()
    
    def _save_json_report(self) -> None:
        """Salva relatório em formato JSON."""
        import json
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_duration": time.time() - self.start_time,
            "results": [
                {
                    "name": r.name,
                    "success": r.success,
                    "duration": r.duration
                }
                for r in self.results
            ],
            "summary": {
                "total": len(self.results),
                "passed": sum(1 for r in self.results if r.success),
                "failed": sum(1 for r in self.results if not r.success)
            }
        }
        
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / f"pipeline-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Relatório salvo em: {report_file}")


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Automação Shift Left para CNPJ Validator"
    )
    parser.add_argument(
        "--full", 
        action="store_true",
        help="Executa pipeline completo"
    )
    parser.add_argument(
        "--quick",
        action="store_true", 
        help="Executa verificação rápida"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostra output detalhado"
    )
    
    args = parser.parse_args()
    
    runner = AutomationRunner(verbose=args.verbose)
    
    if args.quick:
        success = runner.run_quick_check()
    else:
        success = runner.run_full_pipeline()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

### 4. requirements-dev.txt

```text
# requirements-dev.txt
# Dependências de desenvolvimento e CI/CD

# Testes
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-xdist>=3.5.0
pytest-mock>=3.12.0
responses>=0.24.0

# Linting e Formatação
flake8>=7.0.0
flake8-docstrings>=1.7.0
flake8-bugbear>=24.1.17
black>=23.12.0
isort>=5.13.0
pylint>=3.0.0

# Type Checking
mypy>=1.8.0
types-requests>=2.31.0

# Segurança
bandit>=1.7.7
safety>=2.3.0
pip-audit>=2.6.0
detect-secrets>=1.4.0

# Pre-commit
pre-commit>=3.6.0

# Build
build>=1.0.0
twine>=4.0.0

# Documentação
mkdocs>=1.5.0
mkdocs-material>=9.5.0
```

## 📊 Dashboard de Métricas

```markdown
<!-- docs/METRICS.md -->

# 📊 Shift Left Metrics Dashboard

![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Security](https://img.shields.io/badge/security-A-brightgreen)

## Métricas Atuais

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Cobertura de Código | 85% | 80% | ✅ |
| Testes Passando | 100% | 100% | ✅ |
| Tempo de Build | 6min | <10min | ✅ |
| Vulnerabilidades | 0 | 0 | ✅ |
| Complexidade Média | 8 | <10 | ✅ |

## Tendência (Últimos 30 dias)

```
Cobertura: ▁▂▃▄▅▅▆▆▇▇█ (75% → 85%)
Build Time: █▇▆▆▅▅▄▄▃▃▂ (8min → 6min)
```

## Shift Left Score: 87/100

```
[████████████████████░░░░] 87%
```
```

## 🎯 Resumo: O Que Foi Demonstrado

| Componente | Arquivo | Princípio Shift Left |
|------------|---------|----------------------|
| Pre-commit hooks | `.pre-commit-config.yaml` | Fail Fast no commit |
| Makefile | `Makefile` | Automação local |
| Script Python | `automation.py` | Pipeline programático |
| Dev dependencies | `requirements-dev.txt` | Ferramentas integradas |
| Dashboard | `METRICS.md` | Feedback contínuo |

## 🔗 Conclusão

Este exemplo demonstrou como integrar todos os conceitos de Shift Left Testing em um sistema de automação completo:

1. **Pre-commit**: Verificações antes do commit
2. **Makefile**: Comandos padronizados
3. **Script Python**: Automação flexível
4. **CI/CD**: Pipeline no GitHub Actions
5. **Dashboard**: Visibilidade de métricas

Com esta infraestrutura, bugs são encontrados em segundos (no pre-commit), não em dias (em produção).

---

| Anterior | Índice |
|----------|--------|
| [← CI/CD](exemplo-03-ci-cd.md) | [📚 Principal](../README.md) |

---

## 🎓 Parabéns!

Você completou todos os exemplos práticos do material de Shift Left Testing. Agora você tem:

- ✅ Fundamentos teóricos sólidos
- ✅ Exercícios práticos realizados
- ✅ Exemplos de código real
- ✅ Infraestrutura de automação

**Próximo passo**: Aplicar estes conhecimentos em seus próprios projetos!
