# 🧪 Plano de Testes - Migração CNPJ Alfanumérico 2026

> **Objetivo**: Estratégia completa de testes para garantir migração segura
> do validador CNPJ numérico para alfanumérico.

---

## 📋 Sumário Executivo

### Escopo dos Testes

| Categoria | Descrição | Quantidade |
|-----------|-----------|------------|
| **Caracterização** | Documentar comportamento legado | 50+ testes |
| **Golden Master** | Captura de resultados | 10.000+ casos |
| **Unitários** | Novo validador | 100+ testes |
| **Integração** | Facade de migração | 30+ testes |
| **Regressão** | Suite completa | 4 níveis |
| **Performance** | Benchmark | 5 cenários |

### Critérios de Aceitação

```text
┌─────────────────────────────────────────────────────────────────┐
│                   CRITÉRIOS GO/NO-GO                            │
├─────────────────────────────────────────────────────────────────┤
│ ✅ Golden Master: 100% paridade                                 │
│ ✅ Cobertura de código: > 90%                                   │
│ ✅ Testes de regressão: 100% passando                           │
│ ✅ Performance: < 10% degradação                                │
│ ✅ Taxa de erro em shadow: < 0.01%                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Estratégia de Testes

### Pirâmide de Testes

```text
                    ╱╲
                   ╱  ╲
                  ╱ E2E╲         ← 5% (Smoke/Sanity)
                 ╱──────╲
                ╱        ╲
               ╱ INTEGRA- ╲      ← 20% (Facade, API)
              ╱   ÇÃO      ╲
             ╱──────────────╲
            ╱                ╲
           ╱    UNITÁRIOS     ╲   ← 75% (Validadores)
          ╱                    ╲
         ╱────────────────────────╲
```

### Fases de Teste

#### Fase 1: Caracterização do Legado

```python
"""
OBJETIVO: Documentar 100% do comportamento atual.

QUANDO: Antes de qualquer modificação no código.
"""

# Técnicas a utilizar:
# 1. Testes de caracterização por categoria
# 2. Boundary testing (limites)
# 3. Equivalence partitioning (classes)
# 4. Decision table testing (combinações)
```

#### Fase 2: Golden Master

```python
"""
OBJETIVO: Criar snapshot de todos os resultados possíveis.

FORMATO: JSON com 10.000+ casos de teste.
"""

# Categorias de casos:
# - CNPJs válidos (numéricos)
# - CNPJs válidos (alfanuméricos)
# - CNPJs inválidos (formato)
# - CNPJs inválidos (DV)
# - Casos de borda
# - Entradas maliciosas
```

#### Fase 3: Testes do Novo Validador

```python
"""
OBJETIVO: Garantir que nova implementação está correta.

COBERTURA: > 90% de branches.
"""

# Categorias:
# - Validação de formato
# - Cálculo de DV
# - Retrocompatibilidade
# - Performance
```

#### Fase 4: Testes de Integração

```python
"""
OBJETIVO: Validar Facade de migração.

CENÁRIOS: Rollout gradual, shadow mode, rollback.
"""

# Cenários:
# - 100% legado
# - Shadow mode
# - Rollout por porcentagem
# - Canary por cliente
# - Rollback de emergência
```

---

## 📊 Casos de Teste Detalhados

### 1. Testes de Caracterização

#### 1.1 CNPJs Válidos Numéricos

| ID | Entrada | Saída Esperada | Categoria |
|----|---------|----------------|-----------|
| TC-001 | `11.222.333/0001-81` | `True` | Formatado |
| TC-002 | `11222333000181` | `True` | Sem formatação |
| TC-003 | `00.000.000/0001-91` | `True` | Zeros iniciais |
| TC-004 | `99.999.999/9999-99` | `False` | Limite superior |
| TC-005 | `11.222.333/0002-62` | `True` | Filial |

#### 1.2 CNPJs Inválidos (Formato)

| ID | Entrada | Saída Esperada | Motivo |
|----|---------|----------------|--------|
| TC-010 | `11.222.333/0001` | `False` | Incompleto |
| TC-011 | `11.222.333/0001-811` | `False` | Excedente |
| TC-012 | `11.222.333/0001-8A` | `False` | Letra no DV |
| TC-013 | `null` | `False` | Nulo |
| TC-014 | `` | `False` | Vazio |

#### 1.3 CNPJs Inválidos (DV)

| ID | Entrada | Saída Esperada | Motivo |
|----|---------|----------------|--------|
| TC-020 | `11.222.333/0001-82` | `False` | DV1 errado |
| TC-021 | `11.222.333/0001-71` | `False` | DV2 errado |
| TC-022 | `11.222.333/0001-00` | `False` | Ambos errados |
| TC-023 | `11.111.111/1111-11` | `False` | Repetidos |
| TC-024 | `00.000.000/0000-00` | `False` | Zeros |

### 2. Testes do Validador Alfanumérico

#### 2.1 CNPJs Alfanuméricos Válidos

| ID | Entrada | Saída Esperada | Categoria |
|----|---------|----------------|-----------|
| TC-100 | `AB.CDE.FGH/0001-XX` | `True` | Full alfa |
| TC-101 | `A1.B2C.D34/0001-XX` | `True` | Misto |
| TC-102 | `12.ABC.DEF/0001-XX` | `True` | Início numérico |
| TC-103 | `ab.cde.fgh/0001-XX` | `True` | Minúsculas |
| TC-104 | `AB.CDE.123/0002-XX` | `True` | Filial |

> **Nota**: Os valores `XX` nos DVs devem ser calculados para cada caso.

#### 2.2 Retrocompatibilidade

| ID | Entrada | Validador Numérico | Validador Alfa | Status |
|----|---------|-------------------|----------------|--------|
| TC-110 | `11.222.333/0001-81` | `True` | `True` | ✅ |
| TC-111 | `00.000.000/0001-91` | `True` | `True` | ✅ |
| TC-112 | `11.222.333/0001-82` | `False` | `False` | ✅ |

### 3. Testes de Integração do Facade

#### 3.1 Cenários de Rollout

| ID | Cenário | Config | Comportamento |
|----|---------|--------|---------------|
| TC-200 | Legacy only | `percentage=0` | Sempre usa legado |
| TC-201 | New only | `percentage=100` | Sempre usa novo |
| TC-202 | 50/50 | `percentage=50` | Distribui 50% |
| TC-203 | Shadow | `shadow=True` | Executa ambos |
| TC-204 | Canary | `canary=['C001']` | Clientes específicos |

#### 3.2 Cenários de Rollback

| ID | Cenário | Trigger | Ação |
|----|---------|---------|------|
| TC-210 | Erro > 0.1% | Automático | Reduz para 50% |
| TC-211 | Erro > 1% | Automático | Reduz para 0% |
| TC-212 | Erro crítico | Manual | Kill switch |
| TC-213 | Divergência | Alerta | Log + continua legado |

### 4. Testes de Performance

#### 4.1 Benchmarks

| ID | Cenário | Métrica | Limite |
|----|---------|---------|--------|
| TC-300 | Validação simples | Tempo médio | < 1ms |
| TC-301 | 1000 validações | Throughput | > 10k/s |
| TC-302 | Pico de carga | p99 latência | < 10ms |
| TC-303 | Memória | Uso máximo | < 50MB |
| TC-304 | Novo vs Legado | Degradação | < 10% |

---

## 📁 Estrutura do Golden Master

### Formato do Arquivo

```json
{
  "metadata": {
    "version": "1.0.0",
    "generated_at": "2025-12-10T10:00:00Z",
    "total_cases": 10547,
    "validator_version": "2.0.0"
  },
  "cases": {
    "validate|11222333000181": {
      "input": "11222333000181",
      "output": true,
      "category": "valid_numeric"
    },
    "validate|ABCDEFGH000145": {
      "input": "ABCDEFGH000145",
      "output": true,
      "category": "valid_alphanumeric"
    },
    "validate|invalid": {
      "input": "invalid",
      "output": false,
      "category": "invalid_format"
    }
  }
}
```

### Categorias de Casos

| Categoria | Quantidade | Descrição |
|-----------|------------|-----------|
| `valid_numeric` | 1000 | CNPJs numéricos válidos |
| `valid_alphanumeric` | 2000 | CNPJs alfanuméricos válidos |
| `invalid_format` | 500 | Formato incorreto |
| `invalid_dv` | 500 | DV incorreto |
| `boundary` | 200 | Casos de borda |
| `special_chars` | 100 | Caracteres especiais |
| `edge_cases` | 247 | Outros casos de borda |
| **Total** | **10.547** | |

---

## 🔄 Suite de Regressão em 4 Níveis

### Nível 1: Smoke Tests (< 1 min)

```python
"""
QUANDO: Toda build, pré-commit, CI trigger.

OBJETIVO: Sistema está funcionando?
"""

SMOKE_TESTS = [
    "test_sistema_responde",
    "test_cnpj_valido_aceito",
    "test_cnpj_invalido_rejeitado",
    "test_formato_correto",
]
```

**Comando:**
```bash
pytest tests/ -m smoke --timeout=60
```

### Nível 2: Sanity Tests (< 5 min)

```python
"""
QUANDO: Após merge, antes de staging.

OBJETIVO: Funcionalidades principais ok?
"""

SANITY_TESTS = [
    "test_todas_validacoes_principais",
    "test_calculo_dv_numerico",
    "test_calculo_dv_alfanumerico",
    "test_formatacao",
    "test_limpeza_entrada",
]
```

**Comando:**
```bash
pytest tests/ -m sanity --timeout=300
```

### Nível 3: Core Regression (< 30 min)

```python
"""
QUANDO: Antes de deploy para staging/produção.

OBJETIVO: Cobertura completa de cenários.
"""

CORE_TESTS = [
    "test_todas_faixas_cnpj",
    "test_todos_tipos_entrada",
    "test_integracao_facade",
    "test_rollout_gradual",
    "test_rollback",
]
```

**Comando:**
```bash
pytest tests/ -m core --timeout=1800
```

### Nível 4: Full Regression (> 1 hora)

```python
"""
QUANDO: Release major, antes de Go-Live.

OBJETIVO: 100% de paridade com Golden Master.
"""

FULL_TESTS = [
    "test_golden_master_completo",
    "test_todas_combinacoes",
    "test_performance_benchmark",
    "test_carga_stress",
]
```

**Comando:**
```bash
pytest tests/ -m full --timeout=7200
```

---

## 📈 Métricas e KPIs

### Dashboard de Testes

| Métrica | Alvo | Atual | Status |
|---------|------|-------|--------|
| Cobertura de código | > 90% | - | 🔄 |
| Testes passando | 100% | - | 🔄 |
| Golden Master paridade | 100% | - | 🔄 |
| Tempo smoke tests | < 1 min | - | 🔄 |
| Tempo full regression | < 2h | - | 🔄 |

### Critérios de Saída por Fase

#### Fase 1 → Fase 2 (Caracterização → Implementação)

- [ ] 100% dos comportamentos documentados
- [ ] Golden Master capturado
- [ ] Nenhuma regra de negócio desconhecida

#### Fase 2 → Fase 3 (Implementação → Rollout)

- [ ] Novo validador implementado
- [ ] 100% dos testes unitários passando
- [ ] Performance dentro do limite

#### Fase 3 → Fase 4 (Rollout → Go-Live)

- [ ] Shadow mode com 0% divergência por 1 semana
- [ ] Rollout 50% estável por 2 semanas
- [ ] Nenhum incidente P1/P2

---

## 🛠️ Ferramentas e Ambiente

### Stack de Testes

| Ferramenta | Uso | Versão |
|------------|-----|--------|
| pytest | Framework de testes | 7.x |
| pytest-cov | Cobertura | 4.x |
| pytest-benchmark | Performance | 4.x |
| hypothesis | Property-based | 6.x |
| faker | Geração de dados | 18.x |

### Configuração CI/CD

```yaml
# .github/workflows/tests.yml

name: Test Suite

on: [push, pull_request]

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Smoke Tests
        run: pytest -m smoke

  sanity:
    needs: smoke
    runs-on: ubuntu-latest
    steps:
      - name: Run Sanity Tests
        run: pytest -m sanity

  core:
    needs: sanity
    runs-on: ubuntu-latest
    steps:
      - name: Run Core Regression
        run: pytest -m core

  full:
    if: github.ref == 'refs/heads/main'
    needs: core
    runs-on: ubuntu-latest
    steps:
      - name: Run Full Regression
        run: pytest -m full
```

---

## 🔗 Próximos Passos

1. **[Implementação dos Testes](implementacao-testes.md)** - Código completo
2. **[Checklist Go-Live](checklist-go-live.md)** - Validação final

---

## 📚 Referências

- [Shift Left Testing - Guia Teórico](../01-fundamentos/)
- [Técnicas de Teste em Legados](../02-tecnicas/)
- [CNPJ Alfanumérico 2026](../../../guides/cnpj-alfanumerico-2026.md)
