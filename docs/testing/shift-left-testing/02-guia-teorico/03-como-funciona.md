# 3. Como Funciona na Prática

> Arquitetura, fluxo, papéis e integração com CI/CD

---

## 🎯 Objetivo deste Módulo

Ao final deste módulo, você será capaz de:

- Desenhar um fluxo de Shift Left Testing
- Entender a pirâmide de testes em profundidade
- Conhecer os papéis e responsabilidades de cada membro
- Compreender a integração com pipelines CI/CD
- Aplicar os conceitos ao projeto de validação de CNPJ

---

## 🏗️ Arquitetura de um Processo Shift Left

### Visão Geral do Fluxo

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   DESCOBERTA        REFINAMENTO        DESENVOLVIMENTO        VALIDAÇÃO   │
│       │                  │                    │                   │        │
│       ▼                  ▼                    ▼                   ▼        │
│  ┌─────────┐       ┌─────────────┐      ┌──────────┐       ┌─────────┐    │
│  │ Ideação │──────►│Three Amigos │─────►│Dev+Testes│──────►│QA+Explo │    │
│  │ Riscos  │       │Critérios AC │      │ Pipeline │       │Produção │    │
│  └─────────┘       └─────────────┘      └──────────┘       └─────────┘    │
│       │                  │                    │                   │        │
│       └──────────────────┴────────────────────┴───────────────────┘        │
│                          QUALIDADE EM TODAS AS FASES                       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Detalhamento de Cada Fase

#### Fase 1: Descoberta / Ideação

**O que acontece**:
- Definição do problema de negócio
- Identificação de riscos iniciais
- Discussão de dependências e impactos

**Participação de QA**:
- Trazer perguntas de risco
- Questionar cenários de uso
- Identificar dependências técnicas

**Entregável**: Visão clara do que será construído e principais riscos.

---

#### Fase 2: Refinamento / Análise

**O que acontece**:
- Histórias de usuário detalhadas
- Critérios de aceitação definidos
- Cenários de teste principais identificados

**Prática Chave: Three Amigos**

```
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │     PRODUCT OWNER          DEVELOPER          QA            │
    │          │                     │               │            │
    │          │   "O que precisa    │               │            │
    │          │    ser feito?"      │               │            │
    │          │                     │               │            │
    │          │                "Como vou     "Como vou testar?"  │
    │          │                 construir?"         │            │
    │          │                     │               │            │
    │          └─────────────────────┴───────────────┘            │
    │                         │                                   │
    │                         ▼                                   │
    │          ┌─────────────────────────────────┐                │
    │          │  CRITÉRIOS DE ACEITAÇÃO         │                │
    │          │  TESTÁVEIS E CLAROS             │                │
    │          └─────────────────────────────────┘                │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

**Formato de Critério de Aceitação (Gherkin)**:

```gherkin
Funcionalidade: Validação de CNPJ

  Cenário: CNPJ válido com formatação correta
    Dado que tenho um CNPJ "11.222.333/0001-81"
    Quando eu submeter para validação
    Então o resultado deve indicar CNPJ válido
    E o CNPJ formatado deve ser retornado

  Cenário: CNPJ com dígitos verificadores inválidos
    Dado que tenho um CNPJ "11.222.333/0001-99"
    Quando eu submeter para validação
    Então o resultado deve indicar CNPJ inválido
    E uma mensagem de erro sobre dígitos verificadores deve aparecer
```

**Entregável**: Histórias prontas com critérios de aceitação testáveis.

---

#### Fase 3: Design / Arquitetura

**O que acontece**:
- Decisão de componentes e interfaces
- Definição de contratos de API
- Estratégia de dados

**Foco em Testabilidade**:

```python
# Perguntas que QA faz no design:

# 1. É possível isolar este componente para teste?
# 2. As dependências podem ser mockadas/substituídas?
# 3. Existem logs adequados para debugging?
# 4. Como vamos testar integração com X?
# 5. Quais dados de teste precisamos?
```

**Entregável**: Arquitetura que permite testes em todos os níveis.

---

#### Fase 4: Implementação

**O que acontece**:
- Dev escreve código COM testes
- Testes unitários em paralelo (ou antes, em TDD)
- Code review inclui revisão de testes

**Fluxo de Desenvolvimento com Testes**:

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   1. Escrever teste unitário (pode falhar)                      │
│      │                                                           │
│      ▼                                                           │
│   2. Escrever código mínimo para passar                         │
│      │                                                           │
│      ▼                                                           │
│   3. Rodar testes localmente (pytest)                           │
│      │                                                           │
│      ▼                                                           │
│   4. Refatorar se necessário                                    │
│      │                                                           │
│      ▼                                                           │
│   5. Commit e push                                              │
│      │                                                           │
│      ▼                                                           │
│   6. Pipeline CI executa testes automaticamente                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Entregável**: Código com testes unitários e de integração passando.

---

#### Fase 5: Integração Contínua

**O que acontece em cada commit**:

```yaml
# Pipeline típico de Shift Left

stages:
  - quality-checks    # Linting, formatação, análise estática
  - unit-tests        # Testes unitários (rápidos)
  - integration-tests # Testes de integração
  - security-scan     # Verificação de segurança
  - deploy-staging    # Deploy em ambiente de teste
  - smoke-tests       # Validação básica pós-deploy
```

**Entregável**: Build verde com todas as verificações passando.

---

#### Fase 6: Validação Final

**O que acontece**:
- Testes exploratórios focados em risco
- Validação de integrações completas
- Verificação de requisitos não-funcionais

**QA foca em**:
- Cenários que automação não cobre
- Edge cases complexos
- Experiência do usuário
- Comportamentos inesperados

**Entregável**: Validação de que o sistema atende aos requisitos.

---

#### Fase 7: Produção e Monitoramento

**O que acontece**:
- Deploy controlado (feature flags, canary)
- Monitoramento de erros e métricas
- Feedback para melhorar testes

**Shift Left não termina no deploy**:

```
PRODUÇÃO
    │
    ├── Monitorar erros/exceções
    │
    ├── Analisar métricas de uso
    │
    └── Retroalimentar testes
        │
        └── "Este bug em produção deveria ter sido pego por um teste!"
            │
            └── Criar novo teste para evitar regressão
```

---

## 🔺 A Pirâmide de Testes em Profundidade

### Estrutura da Pirâmide

```
                              PIRÂMIDE DE TESTES
                              
                                    /\
                                   /  \
                                  / UI \
                                 / E2E  \        10%
                                /────────\       Poucos, lentos
                               /          \      Alta fragilidade
                              /  API/      \
                             / Integração   \    20%
                            /────────────────\   Quantidade média
                           /                  \  Média velocidade
                          /    UNITÁRIOS       \
                         /                      \ 70%
                        /────────────────────────\ Muitos, rápidos
                                                   Baixa fragilidade
```

### Nível 1: Testes Unitários (Base - 70%)

**Características**:
- Testam uma única unidade (função, método, classe)
- Extremamente rápidos (milissegundos)
- Isolados - não dependem de banco, API, arquivo
- Determinísticos - sempre mesmo resultado

**Exemplo do Projeto CNPJ**:

```python
# tests/test_numeric_validator.py

class TestNumericCNPJValidatorLength:
    """Testes de validação de tamanho - UNITÁRIOS"""
    
    def test_validate_length_correct(self):
        """Deve validar CNPJ com 14 dígitos"""
        cnpj = "11222333000181"
        assert NumericCNPJValidator.validate_length(cnpj) is True
    
    def test_validate_length_too_short(self):
        """Deve rejeitar CNPJ com menos de 14 dígitos"""
        cnpj = "1122233300018"
        assert NumericCNPJValidator.validate_length(cnpj) is False
    
    def test_validate_length_too_long(self):
        """Deve rejeitar CNPJ com mais de 14 dígitos"""
        cnpj = "112223330001811"
        assert NumericCNPJValidator.validate_length(cnpj) is False
```

**O que testar**:
- Lógica de negócio
- Cálculos
- Validações
- Transformações de dados
- Edge cases

---

### Nível 2: Testes de Integração (Meio - 20%)

**Características**:
- Testam comunicação entre componentes
- Mais lentos que unitários (segundos)
- Podem usar banco de dados, APIs, filas
- Verificam contratos e integrações

**Exemplo do Projeto CNPJ**:

```python
# tests/test_integration.py

class TestCNPJValidatorIntegration:
    """Testes de integração entre validadores"""
    
    def test_validate_with_both_validations(self):
        """Deve executar validação numérica E alfanumérica"""
        validator = CNPJValidator()
        cnpj = "11.222.333/0001-81"
        
        result = validator.validate(cnpj, validate_format=True)
        
        # Verifica que ambas validações foram executadas
        assert result['valid'] is True
        assert 'numeric_validation' in result
        assert 'alphanumeric_validation' in result
        assert result['numeric_validation']['valid'] is True
        assert result['alphanumeric_validation']['valid'] is True
```

**O que testar**:
- Integração entre módulos
- Comunicação com banco de dados
- Chamadas a APIs externas (com mocks ou reais)
- Fluxos que atravessam múltiplos componentes

---

### Nível 3: Testes E2E / UI (Topo - 10%)

**Características**:
- Testam o sistema completo
- Muito lentos (minutos)
- Frágeis - quebram com mudanças de UI
- Caros para manter

**Quando usar**:
- Fluxos críticos de negócio
- Happy paths principais
- Cenários que só podem ser validados end-to-end

**Por que poucos?**

```
PROBLEMA DOS TESTES E2E EXCESSIVOS:

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   100 testes E2E × 2 minutos cada = 200 minutos            │
│                                                             │
│   Pipeline demora 3+ horas                                  │
│   │                                                         │
│   ├── Desenvolvedores não esperam                          │
│   ├── Feedback muito lento                                  │
│   ├── Testes quebram por motivos aleatórios                │
│   └── Time ignora falhas                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Anti-padrão: Pirâmide Invertida (Cone de Sorvete)

```
              ANTI-PADRÃO: CONE DE SORVETE
              
                 ┌────────────────────────────────┐
                 │         MUITOS E2E             │
                 │    (lentos, frágeis, caros)    │
                 └───────────────┬────────────────┘
                                 │
                      ┌──────────┴──────────┐
                      │    Alguns Integração │
                      └──────────┬──────────┘
                                 │
                           ┌─────┴─────┐
                           │Poucos Unit│
                           └───────────┘
                           
              RESULTADO: Suite lenta, frágil, cara de manter
```

**Se você tem mais testes E2E do que unitários, há um problema.**

---

## 👥 Papéis e Responsabilidades

### Desenvolvedores (Dev)

| Responsabilidade | Descrição |
|------------------|-----------|
| Participar de refinamentos | Questionar requisitos, discutir viabilidade |
| Escrever testes unitários | Parte obrigatória do desenvolvimento |
| Manter cobertura | Código crítico deve ter testes |
| Design testável | Injeção de dependência, interfaces claras |
| Corrigir falhas rapidamente | Priorizar builds quebrados |
| Code review | Revisar testes junto com código |

---

### QA / Engenheiro de Qualidade

| Responsabilidade | Descrição |
|------------------|-----------|
| Facilitador de qualidade | Não apenas executor de testes |
| Co-criar critérios | Participar de refinamentos ativamente |
| Definir estratégia | Quais testes, onde, quando, como |
| Guiar pirâmide | Mais unitários, menos E2E |
| Automação funcional | Criar suites de regressão automatizadas |
| Testes exploratórios | Encontrar o que automação não encontra |
| Monitorar métricas | Acompanhar e reportar qualidade |

---

### Product Owner / Product Manager (PO/PM)

| Responsabilidade | Descrição |
|------------------|-----------|
| Requisitos claros | Histórias bem escritas e priorizadas |
| Critérios testáveis | Envolver QA/Dev na definição |
| Decisões informadas | Usar métricas de qualidade |
| Apoiar releases incrementais | Feature flags, experimentos |
| Priorizar qualidade | Não sacrificar por velocidade |

---

### DevOps / SRE

| Responsabilidade | Descrição |
|------------------|-----------|
| Pipeline CI/CD | Criar e manter infraestrutura de testes |
| Ambientes | Disponibilizar ambientes para testes |
| Observabilidade | Logs, métricas, tracing |
| Colaborar com QA | Inserir checks de qualidade no deploy |
| Automação de infra | Ambientes efêmeros, containers |

---

## 🔄 Integração com Pipeline CI/CD

### Pipeline Completo de Shift Left

O projeto CNPJ-QA-Training já tem um pipeline implementado. Vamos analisá-lo:

```yaml
# .github/workflows/ci-cd.yml

name: CNPJ Validator CI/CD - Shift Left Testing

on:
  push:
    branches: [ master, develop ]
  pull_request:
    branches: [ master, develop ]

jobs:
  # FASE 1: Verificações de Qualidade (Mais à Esquerda)
  quality-checks:
    name: Code Quality & Linting
    steps:
      - name: Verificar formatação (Black)
        run: black --check src/
      
      - name: Linting (Flake8)
        run: flake8 src/ --max-line-length=100
      
      - name: Análise estática (Pylint)
        run: pylint src/ --fail-under=8.0
      
      - name: Security scan (Bandit)
        run: bandit -r src/

  # FASE 2: Testes Unitários (Rápidos)
  unit-tests:
    needs: quality-checks
    steps:
      - name: Executar testes unitários
        run: pytest tests/ -v -m "unit or not integration"

  # FASE 3: Testes de Integração
  integration-tests:
    needs: unit-tests
    steps:
      - name: Executar testes de integração
        run: pytest tests/ -v -m "integration"
```

### Estágios do Pipeline Explicados

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   COMMIT                                                                │
│     │                                                                   │
│     ▼                                                                   │
│   ┌─────────────────┐                                                   │
│   │ Quality Checks  │  ← Linting, formatação, análise estática          │
│   │ (~1-2 min)      │    FALHA RÁPIDA se código não segue padrões       │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │ Unit Tests      │  ← Testes unitários isolados                      │
│   │ (~2-5 min)      │    MAIORIA dos testes aqui                        │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │Integration Tests│  ← Testes entre componentes                       │
│   │ (~5-10 min)     │    Validam integrações                            │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │ Security Scan   │  ← Verificação de vulnerabilidades                │
│   │ (~2-3 min)      │    Shift Left Security                            │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │ Deploy Staging  │  ← Deploy em ambiente de teste                    │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│   ┌─────────────────┐                                                   │
│   │ Smoke Tests     │  ← Validação básica pós-deploy                    │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            ▼                                                            │
│        ✅ PRONTO                                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Princípios do Pipeline

**1. Fail Fast (Falhar Rápido)**:
- Verificações mais rápidas primeiro
- Se linting falha, não roda testes
- Feedback em minutos, não horas

**2. Paralelização**:
- Testes em múltiplas versões Python simultaneamente
- Testes em múltiplos sistemas operacionais

**3. Bloqueio de Merge**:
- PR só pode ser mergeado se pipeline passa
- Qualidade é gate obrigatório

---

## 💻 Exemplo Completo: Projeto CNPJ

### Estrutura de Testes do Projeto

```
tests/
├── __init__.py
├── test_numeric_validator.py      # Testes unitários - validador numérico
├── test_alphanumeric_validator.py # Testes unitários - validador alfanumérico
├── test_new_alphanumeric_validator.py
├── test_integration.py            # Testes de integração
└── test_receita_federal_api.py    # Testes da API (com mocks)
```

### Markers para Categorização

```ini
# pytest.ini

markers =
    unit: Testes unitários
    integration: Testes de integração
    smoke: Testes de smoke (validação básica)
    api: Testes que dependem da API da Receita Federal
    slow: Testes que demoram mais tempo
```

### Executando por Categoria

```bash
# Apenas testes unitários (rápidos)
pytest tests/ -v -m "unit"

# Apenas testes de integração
pytest tests/ -v -m "integration"

# Tudo exceto testes lentos
pytest tests/ -v -m "not slow"

# Testes de smoke (para validação rápida)
pytest tests/ -v -m "smoke"
```

---

## 📋 Resumo do Módulo

| Aspecto | Descrição |
|---------|-----------|
| **Fluxo** | Descoberta → Refinamento → Design → Implementação → CI → Validação → Produção |
| **Three Amigos** | PO + Dev + QA refinam juntos |
| **Pirâmide** | 70% unit, 20% integration, 10% E2E |
| **Pipeline** | Quality → Unit → Integration → Security → Deploy → Smoke |
| **Dev** | Escreve testes, participa de refinamentos |
| **QA** | Facilita qualidade, define estratégia, testa exploratoriamente |

---

## ✅ Autoavaliação

1. Desenhe um fluxo de Shift Left com 5 fases principais
2. O que acontece em uma sessão de Three Amigos?
3. Por que a pirâmide de testes tem mais unitários na base?
4. Qual o papel de QA no Shift Left (diferente do tradicional)?
5. O que significa "Fail Fast" em um pipeline?

---

## 🔗 Próximos Passos

Agora que você entende **como Shift Left funciona**, vamos aprender **como aplicar** em uma organização: passo a passo de implementação, boas práticas e ferramentas.

**Próximo módulo**: [4. Como Aplicar em uma Organização](04-como-aplicar.md) →
