# 4. Como Aplicar em uma Organização

> Implementação passo a passo, boas práticas e ferramentas

---

## 🎯 Objetivo deste Módulo

Ao final deste módulo, você será capaz de:

- Avaliar o estado atual de testes em um projeto
- Implementar Shift Left passo a passo
- Aplicar 10+ boas práticas comprovadas
- Escolher ferramentas adequadas por categoria
- Definir métricas de sucesso

---

## 📋 Passo a Passo de Implementação

### Visão Geral dos Passos

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   PASSO 1: DIAGNÓSTICO                                             │
│   "Onde estamos hoje?"                                              │
│                │                                                    │
│                ▼                                                    │
│   PASSO 2: OBJETIVOS                                               │
│   "Onde queremos chegar?"                                           │
│                │                                                    │
│                ▼                                                    │
│   PASSO 3: ENGAJAMENTO                                             │
│   "Quem precisa estar junto?"                                       │
│                │                                                    │
│                ▼                                                    │
│   PASSO 4: QA NO REFINAMENTO                                       │
│   "Mudar como trabalhamos"                                          │
│                │                                                    │
│                ▼                                                    │
│   PASSO 5: TESTES NO DESENVOLVIMENTO                               │
│   "Dev escreve testes"                                              │
│                │                                                    │
│                ▼                                                    │
│   PASSO 6: PIPELINE CI/CD                                          │
│   "Automatizar verificações"                                        │
│                │                                                    │
│                ▼                                                    │
│   PASSO 7: PIRÂMIDE DE TESTES                                      │
│   "Reorganizar tipos de teste"                                      │
│                │                                                    │
│                ▼                                                    │
│   PASSO 8: TREINAMENTO                                             │
│   "Capacitar o time"                                                │
│                │                                                    │
│                ▼                                                    │
│   PASSO 9: MÉTRICAS                                                │
│   "Medir para melhorar"                                             │
│                │                                                    │
│                ▼                                                    │
│   PASSO 10: MELHORIA CONTÍNUA                                      │
│   "Ajustar constantemente"                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Passo 1: Diagnóstico do Estado Atual

**Perguntas para responder**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ DIAGNÓSTICO - CHECKLIST                                            │
│                                                                     │
│ □ Como são feitos testes hoje? Quando entram no ciclo?              │
│                                                                     │
│ □ Existem pipelines de CI/CD? Quais testes são automatizados?       │
│                                                                     │
│ □ Onde os defeitos são mais descobertos?                            │
│   - Em desenvolvimento (pelo dev)?                                   │
│   - Em QA (após código "pronto")?                                   │
│   - Em produção (pelo cliente)?                                     │
│                                                                     │
│ □ Qual a cobertura de testes atual?                                 │
│                                                                     │
│ □ Quanto tempo o pipeline demora?                                   │
│                                                                     │
│ □ Qual a taxa de testes "flaky" (instáveis)?                        │
│                                                                     │
│ □ QA participa de refinamentos?                                     │
│                                                                     │
│ □ Desenvolvedores escrevem testes?                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Ferramenta de diagnóstico - Matriz de Maturidade**:

| Prática | Nível 1 (Inicial) | Nível 2 (Gerenciado) | Nível 3 (Definido) | Nível 4 (Otimizado) |
|---------|-------------------|----------------------|--------------------|--------------------|
| Testes Unitários | Não existem | Alguns existem | Obrigatórios para novo código | TDD praticado |
| CI/CD | Não existe | Build manual | Build automatizado | Pipeline completo |
| QA no Refinamento | Não participa | Às vezes | Sempre participa | Co-cria requisitos |
| Métricas | Não medimos | Cobertura básica | Múltiplas métricas | Decisões baseadas em dados |

---

### Passo 2: Definir Visão e Objetivos

**Exemplos de objetivos SMART**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ OBJETIVOS BEM DEFINIDOS                                            │
│                                                                     │
│ ✅ "Reduzir defeitos encontrados em produção em 50% em 6 meses"     │
│                                                                     │
│ ✅ "Aumentar cobertura de testes unitários para 70% em 3 meses"     │
│                                                                     │
│ ✅ "Reduzir tempo de pipeline de 45min para 15min em 2 meses"       │
│                                                                     │
│ ✅ "100% das histórias com critérios de aceitação testáveis"        │
│                                                                     │
│ ❌ "Melhorar qualidade" (vago, não mensurável)                      │
│                                                                     │
│ ❌ "Testar mais" (não específico, sem prazo)                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Passo 3: Engajar Lideranças e Times

**Quem precisa estar engajado**:

| Stakeholder | Por que engajar | Como engajar |
|-------------|-----------------|--------------|
| Gestão/Liderança | Apoio para mudanças e tempo | ROI, redução de custos com bugs |
| Desenvolvedores | Executarão as mudanças | Menos retrabalho, código mais limpo |
| QAs | Mudarão forma de trabalhar | Papel mais estratégico |
| POs/PMs | Participarão de refinamentos | Entregas mais previsíveis |

**Argumentos para a liderança**:

```
CUSTO DE NÃO FAZER SHIFT LEFT
─────────────────────────────
• Bug em produção custa 100x mais que em desenvolvimento
• Retrabalho consome 30-40% do tempo de desenvolvimento
• Bugs críticos em produção = dano à reputação + perda de clientes

BENEFÍCIOS DO SHIFT LEFT
────────────────────────
• Redução de 40-50% em defeitos escapados
• Aumento de 20-30% em velocidade de entrega
• Melhoria na satisfação do cliente
• Equipes mais colaborativas e menos estressadas
```

---

### Passo 4: Introduzir QA na Fase de Refinamento

**Mudança de processo**:

```
ANTES                                    DEPOIS
──────                                   ──────

PO escreve história                      PO, Dev e QA refinam juntos
       │                                        │
       ▼                                        ▼
Dev implementa                           Three Amigos define:
       │                                 • Critérios de aceitação
       ▼                                 • Cenários de teste
QA testa (e encontra problemas)          • Riscos e edge cases
       │                                        │
       ▼                                        ▼
Volta para Dev corrigir                  Dev implementa COM testes
       │                                        │
       ▼                                        ▼
QA testa novamente...                    QA valida e explora
```

**Template de História com Critérios Testáveis**:

```markdown
## História de Usuário

**Como** usuário do sistema
**Quero** validar um CNPJ
**Para** garantir que o número é válido antes de cadastrar

## Critérios de Aceitação

### Cenário 1: CNPJ válido formatado
- **Dado** que informo "11.222.333/0001-81"
- **Quando** submeto para validação
- **Então** o sistema indica CNPJ válido

### Cenário 2: CNPJ com dígitos verificadores errados
- **Dado** que informo "11.222.333/0001-99"
- **Quando** submeto para validação
- **Então** o sistema indica CNPJ inválido
- **E** mostra mensagem "Dígitos verificadores inválidos"

### Cenário 3: CNPJ com caracteres inválidos
- **Dado** que informo "11.222.333/0001-8A"
- **Quando** submeto para validação
- **Então** o sistema indica formato inválido

## Notas Técnicas
- Aceitar CNPJ com ou sem formatação
- Validar dígitos verificadores conforme algoritmo da Receita
- Retornar CNPJ formatado quando válido
```

---

### Passo 5: Estabelecer Testes no Desenvolvimento

**Práticas a implementar**:

1. **Testes unitários obrigatórios** para novas funcionalidades
2. **Code review** inclui revisão de testes
3. **Cobertura mínima** para PRs (ex: 80% no código novo)

**Template de Teste Unitário**:

```python
"""
Template de teste unitário seguindo padrões do projeto
"""
import pytest
from src.cnpj_validator.validators.numeric_validator import NumericCNPJValidator


class TestNomeDaFuncionalidade:
    """Descrição do que está sendo testado"""
    
    # Arrange: Configuração de fixtures se necessário
    @pytest.fixture
    def validator(self):
        return NumericCNPJValidator()
    
    # Testes positivos (happy path)
    def test_should_return_valid_when_cnpj_is_correct(self, validator):
        """Deve retornar válido quando CNPJ está correto"""
        # Arrange
        cnpj = "11222333000181"
        
        # Act
        result = validator.validate(cnpj)
        
        # Assert
        assert result['valid'] is True
    
    # Testes negativos (casos de erro)
    def test_should_return_invalid_when_cnpj_is_too_short(self, validator):
        """Deve retornar inválido quando CNPJ tem menos de 14 dígitos"""
        # Arrange
        cnpj = "1122233300018"
        
        # Act
        result = validator.validate(cnpj)
        
        # Assert
        assert result['valid'] is False
        assert "tamanho" in result['errors'][0].lower()
    
    # Testes de edge cases
    @pytest.mark.parametrize("cnpj", [
        "00000000000000",
        "11111111111111",
        "99999999999999",
    ])
    def test_should_reject_cnpj_with_all_same_digits(self, validator, cnpj):
        """Deve rejeitar CNPJ com todos os dígitos iguais"""
        result = validator.validate(cnpj)
        assert result['valid'] is False
```

---

### Passo 6: Construir Pipeline CI/CD

**Estrutura recomendada**:

```yaml
# .github/workflows/shift-left-pipeline.yml

name: Shift Left Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  # Estágio 1: Verificações de código (mais rápido)
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install linters
        run: pip install flake8 black pylint
      
      - name: Check formatting
        run: black --check src/
      
      - name: Lint code
        run: flake8 src/
      
      - name: Static analysis
        run: pylint src/ --fail-under=8.0

  # Estágio 2: Testes unitários (rápido)
  unit-tests:
    needs: code-quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run unit tests
        run: pytest tests/ -v -m "not integration" --cov=src --cov-fail-under=70

  # Estágio 3: Testes de integração (mais lento)
  integration-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run integration tests
        run: pytest tests/ -v -m "integration"

  # Estágio 4: Segurança (Shift Left Security)
  security-scan:
    needs: code-quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security scan
        run: |
          pip install bandit safety
          bandit -r src/
          safety check
```

---

### Passo 7: Reorganizar a Pirâmide de Testes

**Análise e reorganização**:

```
SITUAÇÃO TÍPICA (ANTES)              SITUAÇÃO IDEAL (DEPOIS)
────────────────────────              ─────────────────────────

      /████████████\                          /\
     /██████████████\                        /  \
    / MUITOS TESTES  \                      / 10%\
   /    MANUAIS E2E   \                    / E2E  \
  /────────────────────\                  /────────\
 /        POUCOS        \                /   20%    \
/    TESTES UNITÁRIOS    \              / Integração \
/────────────────────────-\            /──────────────\
                                      /      70%       \
                                     /    Unitários     \
                                    /────────────────────\
```

**Ações para reorganizar**:

1. **Identificar** testes E2E que podem ser API/unitários
2. **Converter** testes de UI para testes de API quando possível
3. **Aumentar** cobertura de testes unitários em código crítico
4. **Eliminar** testes redundantes e flaky
5. **Manter** apenas E2E para fluxos críticos de negócio

---

### Passo 8: Treinar o Time

**Tópicos de treinamento**:

| Audiência | Tópicos | Formato |
|-----------|---------|---------|
| Todos | Conceitos de Shift Left, por que importa | Workshop 2h |
| Devs | Escrita de testes unitários, TDD básico | Hands-on 4h |
| QAs | Estratégia de testes, automação | Workshop 4h |
| POs | Critérios de aceitação testáveis | Workshop 2h |

**Recursos internos a criar**:

- Guia de estilo de testes (convenções de nome, estrutura)
- Templates de teste por tipo
- Exemplos de bons critérios de aceitação
- FAQ de dúvidas comuns

---

### Passo 9: Definir Métricas e Dashboards

**Métricas essenciais**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ DASHBOARD DE QUALIDADE - SHIFT LEFT                                │
│                                                                     │
│ ┌─────────────────────┐  ┌─────────────────────┐                    │
│ │ Defeitos por Fase   │  │ Cobertura de Código │                    │
│ │                     │  │                     │                    │
│ │ Requisitos: 5%  ────│  │ Total: 75%     ─────│                    │
│ │ Dev: 45%        ████│  │ Crítico: 90%   █████│                    │
│ │ QA: 40%         ████│  │ Novo: 85%      █████│                    │
│ │ Produção: 10%   ─── │  │                     │                    │
│ └─────────────────────┘  └─────────────────────┘                    │
│                                                                     │
│ ┌─────────────────────┐  ┌─────────────────────┐                    │
│ │ Tempo de Pipeline   │  │ Taxa de Build Verde │                    │
│ │                     │  │                     │                    │
│ │ Atual: 12 min       │  │ Atual: 92%          │                    │
│ │ Meta: 15 min    ✅  │  │ Meta: 95%       ⚠️  │                    │
│ └─────────────────────┘  └─────────────────────┘                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Passo 10: Ciclo de Melhoria Contínua

**Integração com cerimônias ágeis**:

| Cerimônia | Ação de Shift Left |
|-----------|-------------------|
| Planning | Discutir riscos, critérios de aceitação |
| Daily | Mencionar status de pipeline, testes falhando |
| Review | Demonstrar testes junto com funcionalidade |
| Retro | Analisar métricas de qualidade, planejar melhorias |

---

## ✅ 12 Boas Práticas Comprovadas

### 1. Incluir QA Cedo nas Discussões

```
❌ QA recebe tarefa "pronta" para testar
✅ QA participa desde a ideação e refinamento
```

**Por quê?** QA traz perspectiva de risco e cenários que Dev/PO não pensam.

---

### 2. Escrever Critérios de Aceitação Testáveis

```
❌ "O sistema deve ser rápido"
✅ "O tempo de resposta deve ser menor que 200ms para 95% das requisições"

❌ "Validar o CNPJ"
✅ "Dado CNPJ '11.222.333/0001-81', quando validar, então retornar válido"
```

---

### 3. Adotar a Pirâmide de Testes Corretamente

```
❌ 50 testes E2E, 10 testes unitários
✅ 200 testes unitários, 50 integração, 10 E2E
```

---

### 4. Rodar Testes a Cada Commit

```yaml
# Trigger em todo push e PR
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

---

### 5. Tornar Resultados Visíveis

- Dashboard de cobertura
- Status de pipeline no PR
- Notificação de falha em canal do time

---

### 6. Usar Feature Toggles

```python
# Liberar funcionalidade gradualmente
if feature_flags.is_enabled("new_cnpj_validation"):
    result = new_validator.validate(cnpj)
else:
    result = legacy_validator.validate(cnpj)
```

---

### 7. Aplicar Shift Left Security

```yaml
# Verificações de segurança no pipeline
- name: Security scan
  run: |
    bandit -r src/           # Análise estática de segurança
    safety check             # Vulnerabilidades em dependências
```

---

### 8. Projetar para Testabilidade

```python
# ❌ Difícil de testar
class Validator:
    def validate(self):
        api = ExternalAPI()  # Dependência fixa
        return api.call()

# ✅ Fácil de testar
class Validator:
    def __init__(self, api=None):
        self.api = api or ExternalAPI()  # Injeção de dependência
    
    def validate(self):
        return self.api.call()
```

---

### 9. Manter Suites de Teste Saudáveis

- Eliminar testes flaky (instáveis)
- Remover testes redundantes
- Otimizar testes lentos
- Revisar periodicamente

---

### 10. Praticar Testes Exploratórios

Automação não substitui criatividade humana:

```
┌─────────────────────────────────────────────────────────────────────┐
│ SESSÃO DE TESTE EXPLORATÓRIO                                       │
│                                                                     │
│ Missão: Encontrar problemas na validação de CNPJ alfanumérico      │
│ Tempo: 30 minutos                                                   │
│ Foco: Edge cases não cobertos por automação                        │
│                                                                     │
│ Ideias para explorar:                                               │
│ □ CNPJs com caracteres unicode                                     │
│ □ CNPJs muito longos (buffer overflow?)                            │
│ □ Múltiplas validações simultâneas                                 │
│ □ CNPJ com espaços em posições inesperadas                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 11. Criar Guias e Padrões Internos

Documentar para consistência:

- Convenções de nome de teste
- Estrutura de pastas
- Padrões de mock/stub
- Exemplos de bons testes

---

### 12. Automatizar Dados e Ambientes de Teste

```python
# Fixtures reutilizáveis
@pytest.fixture
def valid_cnpjs():
    return [
        "11.222.333/0001-81",
        "22.333.444/0001-92",
        "33.444.555/0001-03",
    ]

@pytest.fixture
def invalid_cnpjs():
    return [
        "00.000.000/0000-00",  # Todos zeros
        "11.111.111/1111-11",  # Todos iguais
        "99.999.999/9999-99",  # DV inválido
    ]
```

---

## 🛠️ Ferramentas Recomendadas por Categoria

### CI/CD

| Ferramenta | Melhor para | Integração |
|------------|-------------|------------|
| GitHub Actions | Projetos GitHub | Nativa |
| GitLab CI | Projetos GitLab | Nativa |
| Jenkins | Auto-hospedado, flexível | Plugins |
| Azure DevOps | Ecossistema Microsoft | Nativa |
| CircleCI | Performance, paralelismo | Via config |

### Testes Unitários

| Linguagem | Framework | Características |
|-----------|-----------|-----------------|
| Python | pytest | Simples, fixtures, parametrize |
| JavaScript | Jest | Rápido, mocks integrados |
| Java | JUnit 5 | Extensível, assertions |
| C# | xUnit | Moderno, paralelo |
| Go | testing | Built-in, benchmarks |

### Testes de Integração/API

| Ferramenta | Tipo | Uso |
|------------|------|-----|
| pytest + requests | Python | APIs REST |
| REST Assured | Java | APIs REST |
| Postman/Newman | Agnóstico | APIs REST, coleções |
| Pact | Múltiplas | Contract testing |
| Testcontainers | Múltiplas | DBs, serviços em containers |

### Testes E2E/UI

| Ferramenta | Melhor para |
|------------|-------------|
| Playwright | Multi-browser, moderno |
| Cypress | JavaScript/TypeScript |
| Selenium | Ampla compatibilidade |

### Análise Estática

| Ferramenta | Tipo |
|------------|------|
| SonarQube | Qualidade geral |
| ESLint | JavaScript/TypeScript |
| Pylint/flake8 | Python |
| Bandit | Segurança Python |

### Segurança

| Ferramenta | Tipo |
|------------|------|
| Snyk | Vulnerabilidades em deps |
| OWASP Dependency-Check | Vulnerabilidades |
| Bandit | SAST para Python |
| Safety | Python dependencies |

---

## 📊 Métricas de Sucesso

### Métricas Essenciais

| Métrica | O que mede | Meta típica |
|---------|------------|-------------|
| Defeitos por Fase | Onde bugs são encontrados | 80%+ em dev/QA |
| Cobertura de Código | % de código testado | 70-80% geral, 90%+ crítico |
| Tempo de Pipeline | Velocidade de feedback | < 15 minutos |
| Taxa de Build Verde | Estabilidade | > 90% |
| MTTR | Tempo para corrigir | < 1 hora |
| Taxa de Escape | Bugs em produção | Tendência de queda |

### Como Interpretar

```
┌─────────────────────────────────────────────────────────────────────┐
│ SINAIS DE SUCESSO                                                  │
│                                                                     │
│ ✅ Defeitos em produção diminuindo mês a mês                       │
│ ✅ Tempo de pipeline estável e rápido                               │
│ ✅ Cobertura em código crítico > 90%                               │
│ ✅ Builds vermelhos são corrigidos em < 1 hora                     │
│ ✅ QA participa de 100% dos refinamentos                           │
│                                                                     │
│ SINAIS DE ALERTA                                                   │
│                                                                     │
│ ⚠️ Muitos testes flaky (instáveis)                                 │
│ ⚠️ Pipeline demora > 30 minutos                                    │
│ ⚠️ Cobertura alta mas bugs escapam (testes de baixa qualidade)     │
│ ⚠️ Time ignora builds quebrados                                    │
│ ⚠️ Regressões frequentes                                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Resumo do Módulo

| Passo | Ação Principal |
|-------|----------------|
| 1 | Diagnosticar estado atual |
| 2 | Definir objetivos SMART |
| 3 | Engajar stakeholders |
| 4 | QA em refinamentos |
| 5 | Testes no desenvolvimento |
| 6 | Pipeline CI/CD |
| 7 | Reorganizar pirâmide |
| 8 | Treinar time |
| 9 | Métricas e dashboards |
| 10 | Melhoria contínua |

---

## ✅ Autoavaliação

1. Quais são os 3 primeiros passos para implementar Shift Left?
2. Cite 5 boas práticas de Shift Left
3. Quais métricas indicam sucesso de Shift Left?
4. Por que feature toggles ajudam em Shift Left?
5. O que deve estar em um pipeline CI/CD de Shift Left?

---

## 🔗 Próximos Passos

Agora que você sabe **como implementar**, vamos ao checklist final: **o que não esquecer** e as **armadilhas comuns** a evitar.

**Próximo módulo**: [5. O Que Lembrar Sempre](05-lembrar-sempre.md) →
