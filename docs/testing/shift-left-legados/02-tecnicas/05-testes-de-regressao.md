# 🔄 Testes de Regressão em Sistemas Legados

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- ✅ Entender a importância de testes de regressão em migrações
- ✅ Criar suítes de regressão eficientes
- ✅ Automatizar execução de testes de regressão
- ✅ Gerenciar falsos positivos e manutenção de testes

---

## 1. O Que São Testes de Regressão?

### 1.1 Definição

> **Teste de Regressão** = Verificação de que mudanças no código não quebraram
> funcionalidades que estavam funcionando anteriormente.

```text
┌─────────────────────────────────────────────────────────────────┐
│                    TESTES DE REGRESSÃO                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  "REGRESSÃO" = Algo que funcionava e parou de funcionar         │
│                                                                  │
│  ANTES da mudança:         DEPOIS da mudança:                   │
│  ┌─────────────────┐       ┌─────────────────┐                  │
│  │  Funcionalidade │       │  Funcionalidade │                  │
│  │    ✅ OK        │  →    │    ❌ Quebrou   │                  │
│  └─────────────────┘       └─────────────────┘                  │
│                                                                  │
│  TESTE DE REGRESSÃO:                                             │
│  Detecta quando isso acontece ANTES de ir para produção         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Por Que São Críticos em Legados?

```text
┌─────────────────────────────────────────────────────────────────┐
│           POR QUE REGRESSÃO É CRÍTICO EM LEGADOS?               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. ACOPLAMENTO OCULTO                                           │
│     Sistema legado tem dependências não documentadas.           │
│     Mudar A pode quebrar B, C e D sem você saber.              │
│                                                                  │
│  2. FALTA DE TESTES EXISTENTES                                   │
│     Sem testes, qualquer mudança é "voar às cegas".            │
│     Você não sabe o que está funcionando até quebrar.          │
│                                                                  │
│  3. CONHECIMENTO PERDIDO                                         │
│     Quem escreveu não está mais na empresa.                    │
│     Documentação está desatualizada ou não existe.             │
│                                                                  │
│  4. COMPORTAMENTOS "ACIDENTAIS"                                  │
│     Bugs que viraram features.                                  │
│     Clientes dependem de comportamentos não intencionais.      │
│                                                                  │
│  5. MIGRAÇÃO GRADUAL                                             │
│     Durante migração, sistema híbrido é mais frágil.           │
│     Cada mudança pode quebrar integração legado/novo.          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Estratégias de Teste de Regressão

### 2.1 Pirâmide de Regressão

```text
                    ╱╲
                   ╱  ╲
                  ╱ E2E╲           ← Poucos (lentos, frágeis)
                 ╱──────╲
                ╱        ╲
               ╱ Integração╲       ← Médios (equilíbrio)
              ╱────────────╲
             ╱              ╲
            ╱   Unitários    ╲     ← Muitos (rápidos, estáveis)
           ╱──────────────────╲
          
          
PARA SISTEMAS LEGADOS, AJUSTE A PIRÂMIDE:

                    ╱╲
                   ╱E2E╲           ← Mais E2E no início
                  ╱────╲              (não tem unitários)
                 ╱      ╲
                ╱Integração╲       ← Foco aqui durante migração
               ╱──────────╲
              ╱            ╲
             ╱  Unitários   ╲      ← Adicionar conforme refatora
            ╱────────────────╲
           ╱                  ╲
          ╱  Caracterização    ╲   ← BASE: Caracterizar primeiro
         ╱──────────────────────╲
```

### 2.2 Níveis de Teste de Regressão

```python
# regression_test_levels.py
"""
Definição dos níveis de teste de regressão.
"""

from enum import Enum
from typing import List, Dict
from dataclasses import dataclass


class RegressionLevel(Enum):
    """Níveis de teste de regressão."""
    
    # Nível 1: Smoke Tests (5 min)
    SMOKE = "smoke"
    
    # Nível 2: Sanity Tests (15 min)
    SANITY = "sanity"
    
    # Nível 3: Core Regression (1 hora)
    CORE = "core"
    
    # Nível 4: Full Regression (4+ horas)
    FULL = "full"


@dataclass
class RegressionSuite:
    """Define uma suíte de regressão."""
    level: RegressionLevel
    name: str
    description: str
    estimated_time: str
    when_to_run: str
    test_markers: List[str]


# Configuração das suítes
REGRESSION_SUITES: Dict[RegressionLevel, RegressionSuite] = {
    
    RegressionLevel.SMOKE: RegressionSuite(
        level=RegressionLevel.SMOKE,
        name="Smoke Tests",
        description="Verificação rápida de que o sistema está 'vivo'",
        estimated_time="5 minutos",
        when_to_run="A cada commit, deploy",
        test_markers=["smoke"]
    ),
    
    RegressionLevel.SANITY: RegressionSuite(
        level=RegressionLevel.SANITY,
        name="Sanity Tests",
        description="Verificação de funcionalidades críticas",
        estimated_time="15 minutos",
        when_to_run="A cada PR, antes de merge",
        test_markers=["sanity", "critical"]
    ),
    
    RegressionLevel.CORE: RegressionSuite(
        level=RegressionLevel.CORE,
        name="Core Regression",
        description="Testes das funcionalidades principais",
        estimated_time="1 hora",
        when_to_run="Diariamente, nightly build",
        test_markers=["core", "regression"]
    ),
    
    RegressionLevel.FULL: RegressionSuite(
        level=RegressionLevel.FULL,
        name="Full Regression",
        description="Suíte completa de regressão",
        estimated_time="4+ horas",
        when_to_run="Antes de release, semanalmente",
        test_markers=["regression"]
    ),
}


def get_pytest_command(level: RegressionLevel) -> str:
    """Retorna comando pytest para executar suíte."""
    suite = REGRESSION_SUITES[level]
    markers = " or ".join(suite.test_markers)
    return f'pytest -m "{markers}" --tb=short'
```

---

## 3. Implementação Prática

### 3.1 Estrutura de Testes de Regressão

```python
# tests/regression/conftest.py
"""
Configuração para testes de regressão.
"""

import pytest
from typing import Generator
from datetime import datetime


# === Markers ===

def pytest_configure(config):
    """Registrar markers de regressão."""
    config.addinivalue_line(
        "markers", "smoke: Smoke tests - execução rápida (5 min)"
    )
    config.addinivalue_line(
        "markers", "sanity: Sanity tests - funcionalidades críticas (15 min)"
    )
    config.addinivalue_line(
        "markers", "core: Core regression - funcionalidades principais (1 hora)"
    )
    config.addinivalue_line(
        "markers", "regression: Full regression suite (4+ horas)"
    )
    config.addinivalue_line(
        "markers", "slow: Testes lentos - excluir em execuções rápidas"
    )


# === Fixtures ===

@pytest.fixture(scope="session")
def regression_start_time() -> datetime:
    """Timestamp de início da execução."""
    return datetime.now()


@pytest.fixture(scope="session")
def regression_report(regression_start_time) -> Generator:
    """Fixture para gerar relatório de regressão."""
    results = {
        "start_time": regression_start_time.isoformat(),
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "failures": []
    }
    
    yield results
    
    # Ao final, salvar relatório
    results["end_time"] = datetime.now().isoformat()
    duration = datetime.now() - regression_start_time
    results["duration_seconds"] = duration.total_seconds()
    
    print(f"\n{'='*60}")
    print("RELATÓRIO DE REGRESSÃO")
    print(f"{'='*60}")
    print(f"Início: {results['start_time']}")
    print(f"Duração: {duration}")
    print(f"Passou: {results['passed']}")
    print(f"Falhou: {results['failed']}")
    print(f"Pulou: {results['skipped']}")
    
    if results['failures']:
        print(f"\nFALHAS:")
        for failure in results['failures']:
            print(f"  - {failure}")
```

### 3.2 Smoke Tests

```python
# tests/regression/test_smoke.py
"""
Smoke Tests - Verificação rápida de sanidade do sistema.

Executar: pytest -m smoke
Tempo estimado: 5 minutos

Estes testes verificam:
- Sistema está "vivo"
- Endpoints principais respondem
- Banco de dados conecta
- Dependências externas acessíveis
"""

import pytest


@pytest.mark.smoke
class TestSmokeCNPJValidator:
    """Smoke tests para validador de CNPJ."""
    
    def test_modulo_importa(self):
        """SMOKE: Módulo principal importa sem erro."""
        from src.cnpj_validator import CNPJValidator
        assert CNPJValidator is not None
    
    def test_instancia_cria(self):
        """SMOKE: Classe instancia sem erro."""
        from src.cnpj_validator import CNPJValidator
        validator = CNPJValidator()
        assert validator is not None
    
    def test_validacao_basica_funciona(self):
        """SMOKE: Validação básica retorna resultado."""
        from src.cnpj_validator import CNPJValidator
        validator = CNPJValidator()
        
        # Não importa se True ou False, só que não dê erro
        result = validator.validate("11222333000181")
        assert isinstance(result, bool)
    
    def test_cnpj_valido_retorna_true(self):
        """SMOKE: CNPJ válido conhecido retorna True."""
        from src.cnpj_validator import CNPJValidator
        validator = CNPJValidator()
        
        # CNPJ que DEVE ser válido
        assert validator.validate("11222333000181") == True


@pytest.mark.smoke
class TestSmokeAPI:
    """Smoke tests para API."""
    
    def test_api_importa(self):
        """SMOKE: Módulo de API importa."""
        from src.api import main
        assert main is not None
    
    def test_health_endpoint(self, client):
        """SMOKE: Endpoint de health responde."""
        response = client.get("/health")
        assert response.status_code == 200


@pytest.mark.smoke
class TestSmokeDatabase:
    """Smoke tests para banco de dados."""
    
    def test_conexao_estabelece(self, db_connection):
        """SMOKE: Conexão com banco estabelece."""
        assert db_connection is not None
        assert db_connection.is_connected()
```

### 3.3 Sanity Tests

```python
# tests/regression/test_sanity.py
"""
Sanity Tests - Verificação de funcionalidades críticas.

Executar: pytest -m sanity
Tempo estimado: 15 minutos

Estes testes verificam funcionalidades que NUNCA podem falhar:
- Validação de CNPJ válido
- Rejeição de CNPJ inválido
- Formatação correta
- Fluxos críticos de negócio
"""

import pytest


@pytest.mark.sanity
class TestSanityCNPJValidation:
    """Sanity tests para validação de CNPJ."""
    
    @pytest.fixture
    def validator(self):
        from src.cnpj_validator import CNPJValidator
        return CNPJValidator()
    
    # === CRÍTICO: CNPJs Válidos Devem Passar ===
    
    @pytest.mark.parametrize("cnpj", [
        "11222333000181",           # Formato básico
        "11.222.333/0001-81",       # Com pontuação
        "00000000000191",           # CNPJ especial válido
    ])
    def test_cnpjs_validos_aceitos(self, validator, cnpj):
        """SANITY: CNPJs válidos DEVEM ser aceitos."""
        assert validator.validate(cnpj) == True, f"CNPJ válido rejeitado: {cnpj}"
    
    # === CRÍTICO: CNPJs Inválidos Devem Ser Rejeitados ===
    
    @pytest.mark.parametrize("cnpj,motivo", [
        ("11222333000182", "DV incorreto"),
        ("00000000000000", "Todos zeros"),
        ("11111111111111", "Todos iguais"),
        ("123", "Tamanho incorreto"),
        ("", "Vazio"),
    ])
    def test_cnpjs_invalidos_rejeitados(self, validator, cnpj, motivo):
        """SANITY: CNPJs inválidos DEVEM ser rejeitados."""
        assert validator.validate(cnpj) == False, \
            f"CNPJ inválido aceito ({motivo}): {cnpj}"
    
    # === CRÍTICO: Formatação ===
    
    def test_formatacao_cnpj(self, validator):
        """SANITY: Formatação deve produzir resultado correto."""
        result = validator.format("11222333000181")
        assert result == "11.222.333/0001-81"
    
    def test_formatacao_remove_caracteres_extras(self, validator):
        """SANITY: Formatação deve limpar input sujo."""
        result = validator.format("11.222.333/0001-81")
        # Deve normalizar e reformatar
        assert result == "11.222.333/0001-81"


@pytest.mark.sanity
class TestSanityMigration:
    """Sanity tests específicos para migração CNPJ 2026."""
    
    def test_sistema_legado_ainda_funciona(self):
        """SANITY: Sistema legado deve continuar funcionando."""
        from legacy.cnpj_utils import proc_cnpj
        
        # Validação numérica deve funcionar
        assert proc_cnpj("11222333000181") == True
        assert proc_cnpj("11222333000182") == False
    
    def test_novo_sistema_funciona(self):
        """SANITY: Novo sistema deve funcionar."""
        from src.cnpj_validator.alphanumeric_validator import AlphanumericValidator
        
        validator = AlphanumericValidator()
        
        # Deve aceitar numérico
        assert validator.validate("11222333000181") == True
        
        # Deve aceitar alfanumérico (2026)
        # Nota: ajustar quando implementação estiver pronta
    
    def test_paridade_sistemas(self):
        """SANITY: Legado e novo devem ter mesmos resultados para CNPJs numéricos."""
        from legacy.cnpj_utils import proc_cnpj
        from src.cnpj_validator.alphanumeric_validator import AlphanumericValidator
        
        validator = AlphanumericValidator()
        
        cnpjs_teste = [
            "11222333000181",
            "11222333000182",
            "00000000000000",
        ]
        
        for cnpj in cnpjs_teste:
            legacy_result = proc_cnpj(cnpj)
            new_result = validator.validate(cnpj)
            
            assert legacy_result == new_result, \
                f"Divergência para {cnpj}: legado={legacy_result}, novo={new_result}"
```

### 3.4 Core Regression

```python
# tests/regression/test_core.py
"""
Core Regression - Testes das funcionalidades principais.

Executar: pytest -m core
Tempo estimado: 1 hora

Cobertura:
- Todas as funcionalidades principais
- Casos de borda comuns
- Integrações críticas
- Fluxos de negócio importantes
"""

import pytest
from typing import List


@pytest.mark.core
@pytest.mark.regression
class TestCoreCNPJValidation:
    """Core regression para validação de CNPJ."""
    
    @pytest.fixture
    def validator(self):
        from src.cnpj_validator import CNPJValidator
        return CNPJValidator()
    
    # === Validação Completa ===
    
    @pytest.mark.parametrize("cnpj", [
        # CNPJs válidos de diferentes faixas
        "11222333000181",
        "12345678000195",
        "00000000000191",
        "99999999000100",  # Se for válido
    ])
    def test_cnpjs_validos_completo(self, validator, cnpj):
        """CORE: Validação completa de CNPJs válidos."""
        result = validator.validate(cnpj)
        assert result == True, f"CNPJ válido rejeitado: {cnpj}"
    
    @pytest.mark.parametrize("cnpj,motivo", [
        ("11222333000180", "DV1 errado"),
        ("11222333000191", "DV2 errado"),
        ("11222333000182", "Ambos DVs errados"),
        ("00000000000000", "Sequência repetida"),
        ("11111111111111", "Sequência repetida"),
        ("22222222222222", "Sequência repetida"),
        ("123456789012", "12 dígitos"),
        ("12345678901234567", "17 dígitos"),
        ("1234567890123a", "Com letra no meio"),
    ])
    def test_cnpjs_invalidos_completo(self, validator, cnpj, motivo):
        """CORE: Validação completa de CNPJs inválidos."""
        result = validator.validate(cnpj)
        assert result == False, f"CNPJ inválido aceito ({motivo}): {cnpj}"
    
    # === Formatação Completa ===
    
    @pytest.mark.parametrize("input_cnpj,expected", [
        ("11222333000181", "11.222.333/0001-81"),
        ("11.222.333/0001-81", "11.222.333/0001-81"),
        ("11 222 333 0001 81", "11.222.333/0001-81"),
        ("11222333000181   ", "11.222.333/0001-81"),
        ("   11222333000181", "11.222.333/0001-81"),
    ])
    def test_formatacao_completa(self, validator, input_cnpj, expected):
        """CORE: Formatação lida com diferentes inputs."""
        result = validator.format(input_cnpj)
        assert result == expected
    
    # === Integração com API Receita ===
    
    @pytest.mark.slow
    def test_consulta_receita_cnpj_valido(self, validator):
        """CORE: Consulta à Receita retorna dados para CNPJ válido."""
        # Usar CNPJ público conhecido
        result = validator.consultar_receita("11222333000181")
        
        assert result is not None
        assert "razao_social" in result or "situacao" in result
    
    @pytest.mark.slow
    def test_consulta_receita_cnpj_inexistente(self, validator):
        """CORE: Consulta à Receita lida com CNPJ inexistente."""
        # CNPJ válido mas inexistente
        result = validator.consultar_receita("11222333000181")
        
        # Deve retornar None ou indicação de não encontrado
        # (depende da implementação)


@pytest.mark.core
@pytest.mark.regression
class TestCoreMigration:
    """Core regression para migração de sistema."""
    
    def test_facade_roteia_corretamente(self):
        """CORE: Facade roteia para implementação correta."""
        from cnpj_strangler_facade import CNPJStranglerFacade
        from strangler_facade import RouteStrategy
        
        facade = CNPJStranglerFacade(RouteStrategy.LEGACY_ONLY)
        
        # Deve usar legado
        with pytest.MonkeyPatch.context() as mp:
            legacy_called = []
            new_called = []
            
            mp.setattr(facade, '_call_legacy', 
                      lambda x: legacy_called.append(x) or True)
            mp.setattr(facade, '_call_new',
                      lambda x: new_called.append(x) or True)
            
            facade.validate("11222333000181")
            
            assert len(legacy_called) == 1
            assert len(new_called) == 0
    
    def test_feature_flag_controla_rollout(self):
        """CORE: Feature flag controla qual implementação usar."""
        from feature_flags import FeatureFlagService
        
        service = FeatureFlagService()
        service.create_flag(
            "cnpj_alfanumerico",
            enabled=True,
            percentage=50
        )
        
        # Deve haver distribuição aproximada
        enabled_count = sum(
            1 for i in range(100)
            if service.is_enabled("cnpj_alfanumerico", user_id=f"user_{i}")
        )
        
        assert 30 < enabled_count < 70, f"Distribuição incorreta: {enabled_count}%"
```

### 3.5 Gerador de Relatório

```python
# tests/regression/report_generator.py
"""
Gerador de relatório de regressão.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict


@dataclass
class TestResult:
    """Resultado de um teste."""
    name: str
    outcome: str  # passed, failed, skipped
    duration: float
    error_message: str = None


@dataclass
class RegressionReport:
    """Relatório completo de regressão."""
    timestamp: str
    suite_level: str
    total_tests: int
    passed: int
    failed: int
    skipped: int
    duration_seconds: float
    failures: List[TestResult]
    coverage_percent: float = None


class RegressionReportGenerator:
    """Gera relatórios de regressão em múltiplos formatos."""
    
    def __init__(self, output_dir: str = "reports/regression"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, report: RegressionReport) -> Dict[str, Path]:
        """
        Gera relatório em múltiplos formatos.
        
        Returns:
            Dict com caminhos dos arquivos gerados
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        outputs = {}
        
        # JSON
        json_path = self.output_dir / f"regression_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        outputs["json"] = json_path
        
        # HTML
        html_path = self.output_dir / f"regression_{timestamp}.html"
        html_content = self._generate_html(report)
        with open(html_path, 'w') as f:
            f.write(html_content)
        outputs["html"] = html_path
        
        # Markdown (para PR comments)
        md_path = self.output_dir / f"regression_{timestamp}.md"
        md_content = self._generate_markdown(report)
        with open(md_path, 'w') as f:
            f.write(md_content)
        outputs["markdown"] = md_path
        
        return outputs
    
    def _generate_html(self, report: RegressionReport) -> str:
        """Gera relatório HTML."""
        status_color = "green" if report.failed == 0 else "red"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Relatório de Regressão - {report.timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f0f0f0; padding: 20px; border-radius: 8px; }}
        .status {{ color: {status_color}; font-size: 24px; font-weight: bold; }}
        .metrics {{ display: flex; gap: 20px; margin: 20px 0; }}
        .metric {{ background: white; padding: 15px; border-radius: 4px; text-align: center; }}
        .metric-value {{ font-size: 32px; font-weight: bold; }}
        .failures {{ background: #ffe0e0; padding: 15px; border-radius: 4px; }}
        .failure-item {{ margin: 10px 0; padding: 10px; background: white; }}
    </style>
</head>
<body>
    <h1>Relatório de Regressão</h1>
    
    <div class="summary">
        <div class="status">
            {"✅ PASSOU" if report.failed == 0 else "❌ FALHOU"}
        </div>
        <p>Suite: {report.suite_level}</p>
        <p>Data: {report.timestamp}</p>
        <p>Duração: {report.duration_seconds:.1f}s</p>
    </div>
    
    <div class="metrics">
        <div class="metric">
            <div class="metric-value">{report.total_tests}</div>
            <div>Total</div>
        </div>
        <div class="metric">
            <div class="metric-value" style="color: green">{report.passed}</div>
            <div>Passou</div>
        </div>
        <div class="metric">
            <div class="metric-value" style="color: red">{report.failed}</div>
            <div>Falhou</div>
        </div>
        <div class="metric">
            <div class="metric-value" style="color: orange">{report.skipped}</div>
            <div>Pulou</div>
        </div>
    </div>
    
    {"<div class='failures'><h3>Falhas:</h3>" + "".join([
        f"<div class='failure-item'><strong>{f.name}</strong><br>{f.error_message or 'Sem mensagem'}</div>"
        for f in report.failures
    ]) + "</div>" if report.failures else ""}
    
</body>
</html>
        """
        return html
    
    def _generate_markdown(self, report: RegressionReport) -> str:
        """Gera relatório Markdown."""
        status = "✅ PASSOU" if report.failed == 0 else "❌ FALHOU"
        
        md = f"""# Relatório de Regressão

## Status: {status}

| Métrica | Valor |
|---------|-------|
| Suite | {report.suite_level} |
| Total | {report.total_tests} |
| Passou | {report.passed} |
| Falhou | {report.failed} |
| Pulou | {report.skipped} |
| Duração | {report.duration_seconds:.1f}s |
"""
        
        if report.failures:
            md += "\n## Falhas\n\n"
            for f in report.failures:
                md += f"### ❌ {f.name}\n"
                md += f"```\n{f.error_message or 'Sem mensagem'}\n```\n\n"
        
        return md
```

---

## 4. Automação e CI/CD

### 4.1 GitHub Actions

```yaml
# .github/workflows/regression-tests.yml
name: Regression Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    # Full regression diariamente às 2:00
    - cron: '0 2 * * *'

jobs:
  smoke-tests:
    name: Smoke Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Smoke Tests
        run: pytest -m smoke --tb=short -v
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: smoke-results
          path: reports/

  sanity-tests:
    name: Sanity Tests
    needs: smoke-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Sanity Tests
        run: pytest -m sanity --tb=short -v
  
  core-regression:
    name: Core Regression (Nightly)
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Core Regression
        run: pytest -m core --tb=short -v --html=reports/core_regression.html
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: core-regression-report
          path: reports/
```

### 4.2 Script de Execução Local

```bash
#!/bin/bash
# scripts/run-regression.sh

set -e

LEVEL=${1:-smoke}

echo "╔══════════════════════════════════════════╗"
echo "║     REGRESSION TESTS - CNPJ Validator    ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Level: $LEVEL"
echo "╚══════════════════════════════════════════╝"

case $LEVEL in
  smoke)
    pytest -m smoke --tb=short -v
    ;;
  sanity)
    pytest -m sanity --tb=short -v
    ;;
  core)
    pytest -m core --tb=short -v --html=reports/core_regression.html
    ;;
  full)
    pytest -m regression --tb=short -v --html=reports/full_regression.html --cov=src --cov-report=html
    ;;
  *)
    echo "Uso: $0 [smoke|sanity|core|full]"
    exit 1
    ;;
esac

echo ""
echo "✅ Regression tests completed!"
```

---

## 5. Resumo

### 5.1 Checklist de Regressão

```text
PRÉ-DEPLOY:
☐ Smoke tests passando (5 min)
☐ Sanity tests passando (15 min)

PRÉ-MERGE (PR):
☐ Core regression passando (1 hora)
☐ Code review aprovado
☐ Coverage não diminuiu

PRÉ-RELEASE:
☐ Full regression passando (4+ horas)
☐ Performance baseline OK
☐ Testes de carga OK (se aplicável)
```

### 5.2 Quando Executar Cada Nível

| Nível | Quando | Tempo | Bloqueante? |
|-------|--------|-------|-------------|
| Smoke | Todo commit | 5 min | ✅ Sim |
| Sanity | Todo PR | 15 min | ✅ Sim |
| Core | Nightly / Pre-merge | 1 hora | ✅ Sim |
| Full | Semanal / Pre-release | 4+ horas | ✅ Para release |

---

**Próximo**: [../03-exercicios/](../03-exercicios/) - Exercícios práticos
