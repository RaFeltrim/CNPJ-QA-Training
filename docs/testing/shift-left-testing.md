# Guia de Shift Left Testing - Projeto CNPJ Validator

## O que é Shift Left Testing?

**Shift Left Testing** é uma abordagem de teste que move as atividades de qualidade para as fases iniciais do ciclo de desenvolvimento de software (SDLC - Software Development Life Cycle). Em vez de testar apenas no final, testamos desde o início.

### Princípios Fundamentais

1. **Testar Cedo** - Quanto mais cedo identificamos defeitos, mais barato é corrigi-los
2. **Testar Frequentemente** - Testes contínuos e automatizados
3. **Prevenção sobre Detecção** - Evitar que defeitos sejam criados
4. **Feedback Rápido** - Desenvolvedores recebem feedback imediato
5. **Qualidade é Responsabilidade de Todos** - Não apenas do time de QA

## Implementação no Projeto CNPJ Validator

### 1. Estrutura de Testes

```
tests/
├── test_numeric_validator.py      # Testes unitários - Validador numérico
├── test_alphanumeric_validator.py # Testes unitários - Validador alfanumérico
└── test_integration.py             # Testes de integração
```

### 2. Níveis de Teste (Test Pyramid)

```
         /\
        /  \  E2E (Poucas)
       /----\
      /      \  Integration (Médias)
     /--------\
    /          \  Unit Tests (Muitas)
   /____________\
```

#### Testes Unitários (Base da Pirâmide)
- **Rápidos**: Executam em milissegundos
- **Isolados**: Testam uma única função/método
- **Muitos**: Cobrem todos os casos de uso
- **Exemplos**:
  - `test_remove_formatting()`
  - `test_calculate_first_digit()`
  - `test_validate_length()`

#### Testes de Integração (Meio da Pirâmide)
- **Moderados**: Executam em segundos
- **Conectados**: Testam interação entre componentes
- **Médio número**: Cobrem fluxos principais
- **Exemplos**:
  - `test_validate_with_both_validations()`
  - `test_format_and_clean_roundtrip()`

## Ciclo de Desenvolvimento com Shift Left

### Fase 1: Planejamento
- Definir critérios de aceitação
- Criar casos de teste antes do código (TDD)
- Revisar requisitos de qualidade

### Fase 2: Desenvolvimento
- Escrever testes unitários
- Implementar código
- Executar testes localmente
- Code review com foco em testabilidade

### Fase 3: Integração Contínua (CI)
- Testes automatizados em cada commit
- Análise de cobertura de código
- Verificação de qualidade (linting)
- Testes de segurança

### Fase 4: Feedback e Melhoria
- Revisar métricas de qualidade
- Adicionar testes para bugs encontrados
- Refatorar código e testes

## Executando os Testes

### Executar Todos os Testes
```bash
pytest
```

### Executar com Cobertura
```bash
pytest --cov=cnpj_validator --cov-report=html
```

### Executar Testes Específicos
```bash
# Apenas testes unitários
pytest tests/test_numeric_validator.py

# Apenas testes de integração
pytest tests/test_integration.py -m integration

# Apenas testes marcados para Zephyr
pytest -m zephyr

# Testes críticos
pytest -m critical
```

### Executar em Paralelo (Mais Rápido)
```bash
pytest -n auto
```

### Gerar Relatório HTML
```bash
pytest --html=reports/test_report.html
```

## Métricas de Qualidade

### Cobertura de Código
- **Meta**: Mínimo 80%
- **Verificar**: `pytest --cov=cnpj_validator --cov-report=term-missing`
- **Relatório**: `reports/coverage/index.html`

### Indicadores de Sucesso
- Cobertura de código > 80%
- Todos os testes passando
- Tempo de execução < 5 segundos
- Zero erros de linting
- Zero vulnerabilidades de segurança

## Markers do Pytest

Use markers para organizar e filtrar testes:

```python
@pytest.mark.unit
def test_basic_validation():
    pass

@pytest.mark.integration
def test_full_flow():
    pass

@pytest.mark.zephyr("CNPJ-T001")
def test_case_for_jira():
    pass

@pytest.mark.critical
def test_must_not_fail():
    pass

@pytest.mark.slow
def test_performance():
    pass
```

## Integração com Zephyr Scale (Jira)

### Configuração de Markers

Cada teste pode ser marcado com ID do Zephyr:

```python
@pytest.mark.zephyr("CNPJ-T001")
def test_validate_correct_cnpj():
    """
    Zephyr Test Case: CNPJ-T001
    Descrição: Validar CNPJ válido
    Prioridade: Alta
    """
    assert CNPJValidator.is_valid("11.222.333/0001-81")
```

### Mapeamento de Testes

| Marker | Tipo de Teste | Prioridade | Executar em |
|--------|---------------|------------|-------------|
| `@pytest.mark.smoke` | Smoke Test | Crítica | Todos os builds |
| `@pytest.mark.regression` | Regressão | Alta | Release |
| `@pytest.mark.integration` | Integração | Média | CI/CD |
| `@pytest.mark.unit` | Unitário | Todas | Sempre |

## Automação e CI/CD

### Pre-commit Hooks (Executar antes de commit)
```bash
# Executar testes
pytest

# Verificar cobertura
pytest --cov=cnpj_validator --cov-fail-under=80

# Linting
flake8 cnpj_validator/
pylint cnpj_validator/

# Formatação
black cnpj_validator/
```

### Pipeline CI/CD Básico

```yaml
# Exemplo de workflow
1. Commit → 2. Testes Unitários → 3. Testes Integração → 4. Deploy
```

## Checklist de Qualidade (Shift Left)

### Antes de Codificar
- [ ] Requisitos estão claros?
- [ ] Critérios de aceitação definidos?
- [ ] Casos de teste planejados?
- [ ] Dados de teste preparados?

### Durante o Desenvolvimento
- [ ] Testes unitários escritos?
- [ ] Código passa nos testes?
- [ ] Cobertura adequada?
- [ ] Code review realizado?

### Antes de Commitar
- [ ] Todos os testes passam?
- [ ] Cobertura mantida ou melhorada?
- [ ] Linting sem erros?
- [ ] Documentação atualizada?

### Antes de Mergear
- [ ] Testes de integração passam?
- [ ] Build de CI passa?
- [ ] Code review aprovado?
- [ ] Testes de regressão OK?

## Boas Práticas

### 1. TDD (Test-Driven Development)
```python
# 1. Escrever teste (RED)
def test_new_feature():
    assert new_function() == expected_result

# 2. Implementar código (GREEN)
def new_function():
    return expected_result

# 3. Refatorar (REFACTOR)
def new_function():
    # Código limpo e otimizado
    return expected_result
```

### 2. Testes Descritivos
```python
# Evitar
def test_cnpj():
    assert validate("123")

# Recomendado
def test_validate_should_reject_cnpj_shorter_than_14_digits():
    cnpj = "123"
    result = validator.validate(cnpj)
    assert result['valid'] is False
    assert "14 dígitos" in result['errors'][0]
```

### 3. Arrange-Act-Assert (AAA)
```python
def test_format_cnpj():
    # Arrange (Preparar)
    validator = CNPJValidator()
    cnpj = "11222333000181"
    
    # Act (Agir)
    formatted = validator.format(cnpj)
    
    # Assert (Verificar)
    assert formatted == "11.222.333/0001-81"
```

### 4. DRY em Testes (fixtures)
```python
@pytest.fixture
def validator():
    return CNPJValidator()

@pytest.fixture
def valid_cnpj():
    return "11.222.333/0001-81"

def test_something(validator, valid_cnpj):
    result = validator.validate(valid_cnpj)
    assert result['valid'] is True
```

## Ferramentas Utilizadas

### Testes
- **pytest**: Framework de testes
- **pytest-cov**: Cobertura de código
- **pytest-html**: Relatórios HTML
- **pytest-xdist**: Execução paralela

### Qualidade
- **flake8**: Linting (PEP 8)
- **pylint**: Análise estática
- **black**: Formatação automática
- **mypy**: Type checking

### Segurança
- **bandit**: Análise de segurança
- **safety**: Vulnerabilidades em dependências

## Monitoramento Contínuo

### Dashboards Recomendados
- **Cobertura de Código**: Tendência ao longo do tempo
- **Taxa de Sucesso**: % de testes passando
- **Tempo de Execução**: Performance dos testes
- **Defeitos Encontrados**: Por fase do ciclo

### Alertas
- Cobertura < 80%
- Testes falhando por > 1 hora
- Vulnerabilidades de segurança
- Performance degradada

## Objetivos do Shift Left

1. **Reduzir Custo**: Encontrar bugs cedo custa 10-100x menos
2. **Aumentar Qualidade**: Menos bugs em produção
3. **Acelerar Entrega**: Feedback rápido = deploys rápidos
4. **Melhorar Colaboração**: Dev e QA trabalham juntos desde o início
5. **Prevenir Problemas**: Não apenas detectá-los

## Próximos Passos

1. **Configurar CI/CD**: GitHub Actions, GitLab CI, Jenkins
2. **Integrar com Zephyr**: Automatizar sincronização de resultados
3. **Adicionar Testes E2E**: Selenium, Playwright
4. **Performance Testing**: Testes de carga e stress
5. **Security Testing**: SAST, DAST, análise de dependências

## Cultura de Qualidade

> "Qualidade não é uma atividade, é uma cultura." - Shift Left Philosophy

### Responsabilidades Compartilhadas
- **Desenvolvedores**: Escrever testes unitários, code review
- **QA**: Estratégia de testes, automação, integração
- **DevOps**: CI/CD, ambientes, monitoramento
- **Product**: Critérios de aceitação, priorização

---

**Lembre-se**: Shift Left não significa eliminar testes tardios, mas complementá-los com testes precoces e contínuos.
