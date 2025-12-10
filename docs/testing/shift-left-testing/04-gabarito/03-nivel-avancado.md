# 📝 Gabarito - Nível Avançado

> **Exercícios 7-10** | Tempo de Revisão: ~60 minutos

---

## Exercício 7: Estratégia Organizacional

### 📋 Enunciado Resumido
Criar proposta executiva para implementação de Shift Left em organização com 50 desenvolvedores, 10 QAs, considerando resistência cultural.

### ✅ Resposta Esperada

#### 7.1 Documento Executivo

```markdown
# Proposta: Implementação Shift Left Testing
## [Nome da Empresa] - Transformação de Qualidade

### Sumário Executivo

**Problema**: 60% dos defeitos são encontrados após deploy, custando 
R$ 500K/ano em correções e retrabalho.

**Solução**: Implementar Shift Left Testing em 3 fases ao longo de 6 meses.

**ROI Esperado**: Redução de 40% em custos de defeitos (R$ 200K/ano).

### Análise Situacional

| Indicador Atual | Valor | Meta 6 meses |
|-----------------|-------|--------------|
| Bugs em produção | 25/mês | 10/mês |
| Cobertura de código | 35% | 75% |
| Tempo de deploy | 2 semanas | 2 dias |
| Custo por defeito | R$ 8K | R$ 2K |

### Plano de Implementação

**Fase 1: Fundação (Mês 1-2)**
- Treinar 10 desenvolvedores piloto
- Implementar CI/CD básico
- Estabelecer métricas baseline

**Fase 2: Expansão (Mês 3-4)**
- Expandir para todos os times
- Automação de testes críticos
- Code review obrigatório

**Fase 3: Otimização (Mês 5-6)**
- Testes de integração automatizados
- Dashboard de métricas
- Processo de melhoria contínua

### Gestão de Resistência

| Resistência | Estratégia |
|-------------|------------|
| "Não temos tempo" | Mostrar que bugs custam mais tempo |
| "QA testa, não dev" | Pair programming QA + Dev |
| "Funciona na minha máquina" | Ambientes idênticos via containers |

### Investimento

| Item | Custo |
|------|-------|
| Treinamento | R$ 50K |
| Ferramentas | R$ 30K/ano |
| Consultoria | R$ 40K |
| **Total Ano 1** | **R$ 120K** |

### Riscos e Mitigação

1. **Queda de produtividade inicial**
   - Mitigação: Fase piloto pequena, métricas de learning curve

2. **Resistência de desenvolvedores sênior**
   - Mitigação: Envolver como mentores e champions

3. **Ferramentas inadequadas**
   - Mitigação: POC de 30 dias antes de comprar

### Conclusão

Investimento de R$ 120K com retorno de R$ 200K/ano a partir do segundo ano.
Aprovação solicitada para início imediato da Fase 1.

---
**Próximos Passos**: Reunião de kickoff em [data]
**Sponsor**: [Nome do executivo]
**Responsável**: [Nome do líder técnico]
```

#### 7.2 Framework de Gestão de Mudança

```
┌─────────────────────────────────────────────────────────────────┐
│                 MODELO ADKAR APLICADO A SHIFT LEFT              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  A - AWARENESS (Conscientização)                                │
│      ├── Workshop "Custo de Defeitos"                           │
│      ├── Cases de sucesso da indústria                          │
│      └── Métricas atuais vs benchmark                           │
│                                                                  │
│  D - DESIRE (Desejo)                                            │
│      ├── WIIFM - "O que eu ganho com isso?"                     │
│      ├── Menos noites corrigindo bugs                           │
│      └── Reconhecimento por qualidade                           │
│                                                                  │
│  K - KNOWLEDGE (Conhecimento)                                   │
│      ├── Treinamentos hands-on                                  │
│      ├── Documentação acessível                                 │
│      └── Mentoria 1:1                                           │
│                                                                  │
│  A - ABILITY (Habilidade)                                       │
│      ├── Tempo protegido para prática                           │
│      ├── Ambiente de experimentação                             │
│      └── Ferramentas adequadas                                  │
│                                                                  │
│  R - REINFORCEMENT (Reforço)                                    │
│      ├── Métricas visíveis                                      │
│      ├── Celebração de vitórias                                 │
│      └── Feedback contínuo                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 💡 Por Que Funciona

**1. ROI Quantificado**
- Executivos entendem dinheiro
- Números concretos > promessas vagas
- Baseline permite medir progresso

**2. Fases Incrementais**
- Menos risco que big bang
- Aprendizado entre fases
- Permite ajustes

**3. Gestão de Resistência Proativa**
- Antecipar objeções
- Ter resposta pronta
- Transformar resistentes em aliados

**4. Framework ADKAR**
- Modelo comprovado de change management
- Aborda aspectos humanos
- Sequência lógica

### ⚠️ Erros Comuns

1. **Focar só em tecnologia**
   - 70% de transformações falham por cultura
   - Pessoas > Processos > Ferramentas

2. **Subestimar resistência**
   - Nem todos querem mudar
   - Influenciadores são chave

3. **Métricas irrealistas**
   - 100% cobertura em 3 meses é fantasia
   - Metas achievable mantêm motivação

4. **Sem sponsor executivo**
   - Sem poder, mudança morre
   - Precisa de alguém que remove bloqueios

---

## Exercício 8: Shift Left Security

### 📋 Enunciado Resumido
Implementar verificações de segurança no pipeline do projeto CNPJ.

### ✅ Resposta Esperada

#### 8.1 Arquitetura de Segurança

```
┌─────────────────────────────────────────────────────────────────┐
│                  SECURITY SHIFT LEFT PIPELINE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   PRE-COMMIT                LOCAL DEV              CI/CD         │
│   ┌──────────┐             ┌──────────┐         ┌──────────┐    │
│   │ Secrets  │             │  IDE     │         │  SAST    │    │
│   │ Detection│────────────▶│ Security │────────▶│  DAST    │    │
│   │ (detect- │             │ Plugins  │         │  SCA     │    │
│   │  secrets)│             │          │         │  Secrets │    │
│   └──────────┘             └──────────┘         └──────────┘    │
│                                                                  │
│   SAST = Static Application Security Testing                    │
│   DAST = Dynamic Application Security Testing                   │
│   SCA = Software Composition Analysis                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 8.2 Implementação Pre-Commit

```yaml
# .pre-commit-config.yaml

repos:
  # Detecta secrets no código
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package.lock.json
  
  # Análise de segurança Python (Bandit)
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
        additional_dependencies: ['bandit[toml]']
  
  # Verifica dependências vulneráveis
  - repo: https://github.com/pyupio/safety
    rev: 2.3.5
    hooks:
      - id: safety
        args: ['check', '--full-report']
```

#### 8.3 Pipeline CI/CD Completo

```yaml
# .github/workflows/security.yml

name: Security Pipeline

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  schedule:
    # Roda diariamente para pegar novas vulnerabilidades
    - cron: '0 6 * * *'

jobs:
  # ===== SAST - Análise Estática =====
  sast-bandit:
    name: SAST - Bandit
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Bandit
        uses: PyCQA/bandit-action@v1
        with:
          configfile: pyproject.toml
          targets: src/
          severity: medium
          confidence: medium
          exit-zero: false
      
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: bandit-output.sarif
  
  # ===== SCA - Dependências =====
  dependency-check:
    name: SCA - Dependency Check
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install Dependencies
        run: pip install -r requirements.txt
      
      - name: Run Safety Check
        run: |
          pip install safety
          safety check --full-report --output json > safety-report.json
        continue-on-error: true
      
      - name: Run pip-audit
        run: |
          pip install pip-audit
          pip-audit --format json > pip-audit-report.json
        continue-on-error: true
      
      - name: Process Results
        run: |
          python scripts/process_security_results.py \
            --safety safety-report.json \
            --pip-audit pip-audit-report.json
  
  # ===== Secrets Detection =====
  secrets-scan:
    name: Secrets Detection
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Histórico completo
      
      - name: TruffleHog Scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.pull_request.base.sha }}
          head: ${{ github.event.pull_request.head.sha }}
          extra_args: --only-verified
      
      - name: Gitleaks Scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  
  # ===== CodeQL Analysis =====
  codeql:
    name: CodeQL Analysis
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: python
          queries: security-extended
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
  
  # ===== Security Report =====
  security-report:
    name: Generate Security Report
    needs: [sast-bandit, dependency-check, secrets-scan, codeql]
    runs-on: ubuntu-latest
    if: always()
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Download All Reports
        uses: actions/download-artifact@v4
      
      - name: Generate Summary Report
        run: |
          python scripts/generate_security_report.py \
            --output security-report.md
      
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('security-report.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: report
            });
```

#### 8.4 Configuração Bandit

```toml
# pyproject.toml

[tool.bandit]
targets = ["src"]
exclude_dirs = ["tests", "docs"]
skips = ["B101"]  # Permite assert em código de produção (se necessário)

# Severidade mínima para falhar
severity = "MEDIUM"
confidence = "MEDIUM"

# Testes específicos para habilitar
tests = [
    "B102",  # exec_used
    "B103",  # set_bad_file_permissions
    "B104",  # hardcoded_bind_all_interfaces
    "B105",  # hardcoded_password_string
    "B106",  # hardcoded_password_funcarg
    "B107",  # hardcoded_password_default
    "B108",  # hardcoded_tmp_directory
    "B110",  # try_except_pass
    "B112",  # try_except_continue
    "B201",  # flask_debug_true
    "B301",  # pickle
    "B302",  # marshal
    "B303",  # md5
    "B304",  # des
    "B305",  # cipher
    "B306",  # mktemp_q
    "B307",  # eval
    "B308",  # mark_safe
    "B310",  # urllib_urlopen
    "B311",  # random
    "B312",  # telnetlib
    "B313",  # xml_bad_cElementTree
    "B314",  # xml_bad_ElementTree
    "B315",  # xml_bad_expatreader
    "B316",  # xml_bad_expatbuilder
    "B317",  # xml_bad_sax
    "B318",  # xml_bad_minidom
    "B319",  # xml_bad_pulldom
    "B320",  # xml_bad_etree
    "B321",  # ftplib
    "B323",  # unverified_context
    "B324",  # hashlib_new_insecure_functions
    "B501",  # request_with_no_cert_validation
    "B502",  # ssl_with_bad_version
    "B503",  # ssl_with_bad_defaults
    "B504",  # ssl_with_no_version
    "B505",  # weak_cryptographic_key
    "B506",  # yaml_load
    "B507",  # ssh_no_host_key_verification
    "B601",  # paramiko_calls
    "B602",  # subprocess_popen_with_shell_equals_true
    "B603",  # subprocess_without_shell_equals_true
    "B604",  # any_other_function_with_shell_equals_true
    "B605",  # start_process_with_a_shell
    "B606",  # start_process_with_no_shell
    "B607",  # start_process_with_partial_path
    "B608",  # hardcoded_sql_expressions
    "B609",  # linux_commands_wildcard_injection
    "B610",  # django_extra_used
    "B611",  # django_rawsql_used
    "B701",  # jinja2_autoescape_false
    "B702",  # use_of_mako_templates
    "B703",  # django_mark_safe
]
```

#### 8.5 Script de Processamento

```python
"""
Script para processar resultados de segurança e gerar relatório.
"""
import json
import sys
from pathlib import Path
from typing import List, Dict


def process_safety_report(report_path: str) -> List[Dict]:
    """Processa relatório do Safety."""
    if not Path(report_path).exists():
        return []
    
    with open(report_path) as f:
        data = json.load(f)
    
    vulnerabilities = []
    for vuln in data.get('vulnerabilities', []):
        vulnerabilities.append({
            'tool': 'safety',
            'package': vuln['package_name'],
            'version': vuln['analyzed_version'],
            'severity': vuln.get('severity', 'unknown'),
            'description': vuln['vulnerability_id'],
            'fix': vuln.get('more_info_path', '')
        })
    
    return vulnerabilities


def generate_report(vulnerabilities: List[Dict]) -> str:
    """Gera relatório markdown."""
    if not vulnerabilities:
        return "## ✅ Security Report\n\nNo vulnerabilities found!"
    
    critical = [v for v in vulnerabilities if v['severity'] == 'critical']
    high = [v for v in vulnerabilities if v['severity'] == 'high']
    medium = [v for v in vulnerabilities if v['severity'] == 'medium']
    low = [v for v in vulnerabilities if v['severity'] == 'low']
    
    report = f"""## 🔒 Security Report

### Summary
- 🔴 Critical: {len(critical)}
- 🟠 High: {len(high)}
- 🟡 Medium: {len(medium)}
- 🟢 Low: {len(low)}

### Vulnerabilities

| Severity | Package | Version | Description |
|----------|---------|---------|-------------|
"""
    
    for vuln in sorted(vulnerabilities, key=lambda x: x['severity']):
        icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(vuln['severity'], '⚪')
        report += f"| {icon} {vuln['severity']} | {vuln['package']} | {vuln['version']} | {vuln['description']} |\n"
    
    return report


if __name__ == '__main__':
    # Processar argumentos e gerar relatório
    vulnerabilities = process_safety_report('safety-report.json')
    report = generate_report(vulnerabilities)
    print(report)
    
    # Falhar se houver vulnerabilidades críticas ou altas
    critical_high = [v for v in vulnerabilities 
                     if v['severity'] in ['critical', 'high']]
    sys.exit(1 if critical_high else 0)
```

### 💡 Por Que Funciona

**1. Defesa em Profundidade**
- Múltiplas camadas (pre-commit, CI, scheduled)
- Se uma falha, outra pega

**2. Shift Left Real**
- Pre-commit: antes do push
- Developer tools: durante desenvolvimento
- CI: última linha de defesa

**3. Automação**
- Zero esforço manual
- Consistente em todo commit
- Histórico de segurança

**4. Feedback Rico**
- Relatório em PR
- SARIF para GitHub Security
- Métricas de tendência

### ⚠️ Erros Comuns

1. **Muitos falsos positivos**
   - Desabilita verificações = perda de confiança
   - Configure thresholds adequados

2. **Ignorar findings**
   - Criar baseline não é resolver
   - Processo para triagem é essencial

3. **Só scanner, sem processo**
   - Ferramenta sem processo = relatório ignorado
   - Defina SLA para correção por severidade

---

## Exercício 9: Dashboard de Métricas

### 📋 Enunciado Resumido
Criar dashboard interativo para visualizar métricas Shift Left do projeto CNPJ.

### ✅ Resposta Esperada

#### 9.1 Arquitetura do Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    DASHBOARD ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   DATA SOURCES              PROCESSING            VISUALIZATION  │
│   ┌──────────┐             ┌──────────┐         ┌──────────┐    │
│   │ GitHub   │             │          │         │          │    │
│   │ Actions  │────────────▶│  Python  │────────▶│ Markdown │    │
│   │          │             │  Script  │         │  Report  │    │
│   ├──────────┤             │          │         │          │    │
│   │ Pytest   │────────────▶│  JSON    │────────▶│ GitHub   │    │
│   │ Coverage │             │  Storage │         │  Pages   │    │
│   ├──────────┤             │          │         │          │    │
│   │ Git      │────────────▶│          │────────▶│ Badges   │    │
│   │ History  │             │          │         │          │    │
│   └──────────┘             └──────────┘         └──────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 9.2 Gerador de Dashboard

```python
"""
Dashboard Generator para métricas Shift Left.
Gera relatório markdown e badges para GitHub Pages.
"""
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import subprocess


@dataclass
class MetricsSnapshot:
    """Snapshot de métricas em um ponto no tempo."""
    timestamp: datetime
    coverage: float
    tests_total: int
    tests_passed: int
    build_time: int
    bugs_prod: int
    commit_sha: str


class DashboardGenerator:
    """Gera dashboard de métricas Shift Left."""
    
    def __init__(self, data_dir: str = "metrics/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_current_metrics(self) -> MetricsSnapshot:
        """Coleta métricas do estado atual."""
        # Coverage do pytest
        coverage = self._get_coverage()
        
        # Resultados dos testes
        tests = self._get_test_results()
        
        # Build time do último workflow
        build_time = self._get_build_time()
        
        # Commit atual
        commit = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True, text=True
        ).stdout.strip()
        
        return MetricsSnapshot(
            timestamp=datetime.now(),
            coverage=coverage,
            tests_total=tests['total'],
            tests_passed=tests['passed'],
            build_time=build_time,
            bugs_prod=0,  # Integrar com issue tracker
            commit_sha=commit
        )
    
    def _get_coverage(self) -> float:
        """Extrai cobertura do coverage.xml."""
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse('coverage.xml')
            root = tree.getroot()
            return float(root.attrib.get('line-rate', 0)) * 100
        except Exception:
            return 0.0
    
    def _get_test_results(self) -> Dict:
        """Extrai resultados do pytest."""
        try:
            with open('.pytest_cache/v/cache/lastfailed', 'r') as f:
                failed = len(json.load(f))
        except Exception:
            failed = 0
        
        # Total de testes (exemplo simplificado)
        result = subprocess.run(
            ['pytest', '--collect-only', '-q'],
            capture_output=True, text=True
        )
        total = len([l for l in result.stdout.split('\n') if '::test_' in l])
        
        return {
            'total': total,
            'passed': total - failed,
            'failed': failed
        }
    
    def _get_build_time(self) -> int:
        """Obtém tempo do último build (em segundos)."""
        # Simplificado - integrar com GitHub API
        return 300
    
    def load_history(self) -> List[MetricsSnapshot]:
        """Carrega histórico de métricas."""
        history_file = self.data_dir / "history.json"
        if not history_file.exists():
            return []
        
        with open(history_file) as f:
            data = json.load(f)
        
        return [
            MetricsSnapshot(
                timestamp=datetime.fromisoformat(m['timestamp']),
                coverage=m['coverage'],
                tests_total=m['tests_total'],
                tests_passed=m['tests_passed'],
                build_time=m['build_time'],
                bugs_prod=m['bugs_prod'],
                commit_sha=m['commit_sha']
            )
            for m in data
        ]
    
    def save_snapshot(self, snapshot: MetricsSnapshot) -> None:
        """Salva snapshot no histórico."""
        history = self.load_history()
        history.append(snapshot)
        
        # Manter últimos 90 dias
        cutoff = datetime.now().timestamp() - (90 * 24 * 60 * 60)
        history = [h for h in history if h.timestamp.timestamp() > cutoff]
        
        history_file = self.data_dir / "history.json"
        with open(history_file, 'w') as f:
            json.dump([
                {
                    'timestamp': h.timestamp.isoformat(),
                    'coverage': h.coverage,
                    'tests_total': h.tests_total,
                    'tests_passed': h.tests_passed,
                    'build_time': h.build_time,
                    'bugs_prod': h.bugs_prod,
                    'commit_sha': h.commit_sha
                }
                for h in history
            ], f, indent=2)
    
    def generate_dashboard(self) -> str:
        """Gera dashboard em markdown."""
        current = self.collect_current_metrics()
        history = self.load_history()
        
        # Calcular tendências
        if len(history) >= 7:
            week_ago = history[-7]
            coverage_trend = current.coverage - week_ago.coverage
            build_trend = current.build_time - week_ago.build_time
        else:
            coverage_trend = 0
            build_trend = 0
        
        # Determinar status
        coverage_status = "✅" if current.coverage >= 80 else "⚠️" if current.coverage >= 60 else "❌"
        test_status = "✅" if current.tests_passed == current.tests_total else "⚠️"
        build_status = "✅" if current.build_time < 600 else "⚠️"
        
        dashboard = f"""# 📊 Shift Left Dashboard

> Última atualização: {current.timestamp.strftime('%Y-%m-%d %H:%M')} | Commit: `{current.commit_sha}`

## 🎯 Métricas Principais

| Métrica | Valor | Meta | Status | Tendência 7d |
|---------|-------|------|--------|--------------|
| **Cobertura** | {current.coverage:.1f}% | 80% | {coverage_status} | {'+' if coverage_trend > 0 else ''}{coverage_trend:.1f}% |
| **Testes Passando** | {current.tests_passed}/{current.tests_total} | 100% | {test_status} | - |
| **Build Time** | {current.build_time}s | <600s | {build_status} | {'+' if build_trend > 0 else ''}{build_trend}s |

## 📈 Shift Left Score

```
Score Atual: {self._calculate_score(current):.0f}/100

[{'█' * int(self._calculate_score(current) / 5)}{'░' * (20 - int(self._calculate_score(current) / 5))}]
```

### Composição do Score

| Componente | Peso | Valor | Contribuição |
|------------|------|-------|--------------|
| Cobertura | 30% | {current.coverage:.1f}% | {min(current.coverage / 80, 1.0) * 30:.1f} |
| Testes | 25% | {(current.tests_passed / current.tests_total * 100) if current.tests_total > 0 else 0:.1f}% | {min((current.tests_passed / current.tests_total) / 0.95, 1.0) * 25 if current.tests_total > 0 else 0:.1f} |
| Build | 20% | {current.build_time}s | {max(0, (600 - current.build_time) / 600) * 20:.1f} |
| Qualidade | 25% | {100 - current.bugs_prod}% | {max(0, (100 - current.bugs_prod) / 90) * 25:.1f} |

## 📉 Histórico (Últimos 30 dias)

```
Cobertura:
{self._generate_sparkline([h.coverage for h in history[-30:]])}

Build Time:
{self._generate_sparkline([h.build_time for h in history[-30:]], inverse=True)}
```

## 🏆 Achievements

{self._generate_achievements(current, history)}

## 📋 Próximas Ações

{self._generate_recommendations(current)}

---

*Dashboard gerado automaticamente por [Shift Left Metrics](../README.md)*
"""
        return dashboard
    
    def _calculate_score(self, m: MetricsSnapshot) -> float:
        """Calcula score Shift Left."""
        coverage_score = min(m.coverage / 80, 1.0) * 30
        test_rate = m.tests_passed / m.tests_total if m.tests_total > 0 else 0
        pass_rate_score = min(test_rate / 0.95, 1.0) * 25
        build_score = max(0, (600 - m.build_time) / 600) * 20
        quality_score = max(0, (100 - m.bugs_prod) / 90) * 25
        return coverage_score + pass_rate_score + build_score + quality_score
    
    def _generate_sparkline(self, values: List[float], inverse: bool = False) -> str:
        """Gera sparkline ASCII."""
        if not values:
            return "No data"
        
        chars = "▁▂▃▄▅▆▇█"
        min_val, max_val = min(values), max(values)
        
        if max_val == min_val:
            return chars[4] * len(values)
        
        normalized = [(v - min_val) / (max_val - min_val) for v in values]
        if inverse:
            normalized = [1 - n for n in normalized]
        
        return ''.join(chars[int(n * 7)] for n in normalized)
    
    def _generate_achievements(self, current: MetricsSnapshot, history: List[MetricsSnapshot]) -> str:
        """Gera lista de achievements."""
        achievements = []
        
        if current.coverage >= 80:
            achievements.append("🏅 **Coverage Champion** - Cobertura acima de 80%")
        if current.tests_passed == current.tests_total:
            achievements.append("🏅 **Zero Failures** - Todos os testes passando")
        if current.build_time < 300:
            achievements.append("🏅 **Speed Demon** - Build abaixo de 5 minutos")
        if len(history) >= 30:
            achievements.append("🏅 **Consistency** - 30 dias de métricas")
        
        if not achievements:
            return "- Nenhum achievement ainda. Continue melhorando!"
        
        return '\n'.join(f"- {a}" for a in achievements)
    
    def _generate_recommendations(self, m: MetricsSnapshot) -> str:
        """Gera recomendações baseadas nas métricas."""
        recs = []
        
        if m.coverage < 80:
            recs.append(f"1. 📈 **Aumentar cobertura**: Faltam {80 - m.coverage:.1f}% para a meta")
        if m.tests_passed < m.tests_total:
            recs.append(f"2. 🔧 **Corrigir testes**: {m.tests_total - m.tests_passed} teste(s) falhando")
        if m.build_time > 600:
            recs.append(f"3. ⚡ **Otimizar build**: {m.build_time - 600}s acima da meta")
        
        if not recs:
            return "- ✅ Todas as métricas dentro da meta! Mantenha o bom trabalho."
        
        return '\n'.join(recs)
    
    def generate_badges(self) -> Dict[str, str]:
        """Gera URLs de badges para README."""
        current = self.collect_current_metrics()
        
        # Usando shields.io
        base = "https://img.shields.io/badge"
        
        # Coverage badge
        cov = current.coverage
        cov_color = "brightgreen" if cov >= 80 else "yellow" if cov >= 60 else "red"
        coverage_badge = f"{base}/coverage-{cov:.0f}%25-{cov_color}"
        
        # Tests badge
        test_rate = current.tests_passed / current.tests_total * 100 if current.tests_total > 0 else 0
        test_color = "brightgreen" if test_rate == 100 else "yellow" if test_rate >= 90 else "red"
        tests_badge = f"{base}/tests-{current.tests_passed}%2F{current.tests_total}-{test_color}"
        
        # Build badge
        build_color = "brightgreen" if current.build_time < 600 else "yellow"
        build_badge = f"{base}/build-{current.build_time}s-{build_color}"
        
        # Score badge
        score = self._calculate_score(current)
        score_color = "brightgreen" if score >= 80 else "yellow" if score >= 60 else "red"
        score_badge = f"{base}/shift--left--score-{score:.0f}-{score_color}"
        
        return {
            'coverage': coverage_badge,
            'tests': tests_badge,
            'build': build_badge,
            'score': score_badge
        }


if __name__ == '__main__':
    generator = DashboardGenerator()
    
    # Coletar e salvar métricas
    snapshot = generator.collect_current_metrics()
    generator.save_snapshot(snapshot)
    
    # Gerar dashboard
    dashboard = generator.generate_dashboard()
    
    # Salvar
    Path('docs/metrics').mkdir(parents=True, exist_ok=True)
    with open('docs/metrics/dashboard.md', 'w') as f:
        f.write(dashboard)
    
    # Gerar badges
    badges = generator.generate_badges()
    print("Badges gerados:")
    for name, url in badges.items():
        print(f"  {name}: ![{name}]({url})")
```

### 💡 Por Que Funciona

**1. Dados Históricos**
- Tendências > snapshots
- Permite ver progresso
- Identifica regressões

**2. Score Composto**
- Simplifica comunicação
- Gamifica melhoria
- Balanceia múltiplos aspectos

**3. Automação**
- Gerado em cada build
- Zero esforço manual
- Sempre atualizado

**4. Badges**
- Visibilidade no README
- Status at-a-glance
- Motivação visual

---

## Exercício 10: Projeto Integrador

### 📋 Enunciado Resumido
Criar plano completo de implementação Shift Left para o projeto CNPJ, integrando todos os conceitos aprendidos.

### ✅ Resposta Esperada

Este exercício é aberto e avaliado por completude, coerência e aplicação dos conceitos. Uma resposta exemplar deve incluir:

#### 10.1 Componentes Obrigatórios

1. **Análise do Estado Atual**
   - Métricas baseline documentadas
   - Gaps identificados
   - Quick wins mapeados

2. **Arquitetura de Testes**
   - Pirâmide de testes definida
   - Proporções justificadas
   - Ferramentas selecionadas

3. **Pipeline CI/CD**
   - Estágios definidos
   - Gates de qualidade
   - Feedback loops

4. **Segurança Integrada**
   - SAST configurado
   - Dependências verificadas
   - Secrets protegidos

5. **Métricas e Dashboard**
   - KPIs definidos
   - Coleta automatizada
   - Visualização clara

6. **Plano de Implementação**
   - Fases com timeline
   - Responsáveis definidos
   - Critérios de sucesso

7. **Gestão de Mudança**
   - Stakeholders mapeados
   - Resistências antecipadas
   - Plano de comunicação

### 💡 Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| Completude | 25% | Todos os componentes presentes |
| Coerência | 25% | Partes se integram logicamente |
| Aplicabilidade | 25% | Pode ser implementado no projeto real |
| Inovação | 15% | Ideias além do básico |
| Apresentação | 10% | Clareza e organização |

### ⚠️ Respostas Parciais

Soluções que cobrem apenas parte dos requisitos recebem pontuação proporcional. Foco em qualidade sobre quantidade.

---

## 📊 Resumo da Avaliação - Nível Avançado

| Exercício | Pontos | Foco Principal |
|-----------|--------|----------------|
| 7 | 25 | Visão organizacional + Change Management |
| 8 | 25 | Segurança técnica + Automação |
| 9 | 25 | Métricas + Visualização |
| 10 | 25 | Integração + Aplicação prática |
| **Total** | **100** | |

### Níveis de Desempenho

- **90-100**: Pronto para liderar iniciativas Shift Left
- **75-89**: Pronto para implementar com supervisão
- **60-74**: Revisar áreas específicas
- **< 60**: Revisar níveis anteriores

---

## 🎓 Conclusão do Curso

Parabéns por completar todos os exercícios! Você agora possui:

- ✅ Fundamentos teóricos sólidos
- ✅ Habilidades práticas de implementação
- ✅ Capacidade de análise e design
- ✅ Visão organizacional

### Próximos Passos Recomendados

1. **Aplicar** os conceitos em um projeto real
2. **Compartilhar** conhecimento com a equipe
3. **Iterar** e melhorar continuamente
4. **Contribuir** com a comunidade

---

| Anterior | Índice |
|----------|--------|
| [← Intermediário](02-nivel-intermediario.md) | [📚 Principal](../README.md) |
