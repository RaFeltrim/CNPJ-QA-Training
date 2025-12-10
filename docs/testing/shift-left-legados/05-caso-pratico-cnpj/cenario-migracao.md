# 📋 Cenário de Migração - CNPJ Alfanumérico 2026

> **Contexto**: Este documento descreve o cenário completo de migração do
> validador de CNPJ numérico para o novo formato alfanumérico (Jul/2026).

---

## 🎯 Resumo Executivo

### O Desafio

Em **julho de 2026**, a Receita Federal do Brasil implementará o novo formato
de CNPJ alfanumérico. Todos os sistemas que validam, armazenam ou processam
CNPJs precisam ser atualizados para suportar o novo formato.

```text
┌─────────────────────────────────────────────────────────────────┐
│                    ANTES vs DEPOIS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CNPJ Numérico (Legado)        CNPJ Alfanumérico (Novo)        │
│   ─────────────────────        ────────────────────────         │
│   11.222.333/0001-81     →     AB.CDE.123/0001-45              │
│                                                                  │
│   • 14 dígitos numéricos        • 8 alfanuméricos + 6 numéricos │
│   • Validação simples           • Validação com peso ASCII      │
│   • Formato único               • Compatível com antigo         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Por Que É Crítico?

| Aspecto | Impacto |
|---------|---------|
| **Compliance** | Obrigatório por lei a partir de Jul/2026 |
| **Volume** | Milhões de CNPJs a processar diariamente |
| **Risco** | Falhas podem bloquear operações fiscais |
| **Legado** | Sistemas têm 10+ anos sem testes |

---

## 📊 Análise do Sistema Legado

### Estrutura do Código Atual

```text
src/cnpj_validator/
├── __init__.py              # Exports principais
├── cnpj_validator.py        # Validador principal (legado)
├── numeric_validator.py     # Validação numérica
├── alphanumeric_validator.py    # Nova validação (já existe)
└── new_alphanumeric_validator.py # Validador 2026
```

### Validador Numérico (Legado)

```python
# Comportamento atual do numeric_validator.py

def validar_cnpj_numerico(cnpj: str) -> bool:
    """
    Valida CNPJ no formato numérico tradicional.
    
    Características:
    - Aceita apenas dígitos
    - Calcula DV com pesos fixos
    - Remove formatação automaticamente
    """
    # Limpeza
    cnpj_limpo = ''.join(c for c in cnpj if c.isdigit())
    
    # Validação de tamanho
    if len(cnpj_limpo) != 14:
        return False
    
    # Validação de dígitos repetidos
    if cnpj_limpo == cnpj_limpo[0] * 14:
        return False
    
    # Cálculo dos dígitos verificadores
    # ... (algoritmo tradicional)
```

### Novo Validador Alfanumérico (2026)

```python
# Comportamento esperado do alphanumeric_validator.py

def validar_cnpj_alfanumerico(cnpj: str) -> bool:
    """
    Valida CNPJ no novo formato alfanumérico.
    
    Características:
    - Aceita letras (A-Z) nos 8 primeiros caracteres
    - Últimos 6 caracteres são numéricos (filial + DV)
    - Cálculo de DV usa código ASCII
    - Retrocompatível com formato numérico
    """
```

---

## 🔍 Regras de Negócio Identificadas

### Formato do CNPJ

```text
CNPJ: XX.XXX.XXX/YYYY-ZZ

Onde:
├── XX.XXX.XXX  = Raiz (8 caracteres)
│   ├── Numérico: 0-9
│   └── Alfanumérico: A-Z, 0-9
│
├── YYYY = Filial (4 dígitos numéricos)
│   └── 0001 = Matriz
│   └── 0002+ = Filiais
│
└── ZZ = Dígitos Verificadores (2 dígitos numéricos)
```

### Algoritmo de Validação

#### CNPJ Numérico (Tradicional)

```python
# Pesos para cálculo do DV
PESOS_DV1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
PESOS_DV2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

def calcular_dv_numerico(cnpj_base: str) -> tuple:
    """Calcula DVs para CNPJ numérico."""
    
    # Primeiro DV
    soma = sum(int(d) * p for d, p in zip(cnpj_base, PESOS_DV1))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    # Segundo DV
    cnpj_com_dv1 = cnpj_base + str(dv1)
    soma = sum(int(d) * p for d, p in zip(cnpj_com_dv1, PESOS_DV2))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    return (dv1, dv2)
```

#### CNPJ Alfanumérico (2026)

```python
# Tabela ASCII para conversão
ASCII_MAP = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 17, 'B': 18, 'C': 19, 'D': 20, 'E': 21,
    'F': 22, 'G': 23, 'H': 24, 'I': 25, 'J': 26,
    'K': 27, 'L': 28, 'M': 29, 'N': 30, 'O': 31,
    'P': 32, 'Q': 33, 'R': 34, 'S': 35, 'T': 36,
    'U': 37, 'V': 38, 'W': 39, 'X': 40, 'Y': 41,
    'Z': 42
}

def calcular_dv_alfanumerico(cnpj_base: str) -> tuple:
    """
    Calcula DVs para CNPJ alfanumérico.
    
    Diferença: usa valor ASCII mapeado ao invés de int().
    """
    valores = [ASCII_MAP[c.upper()] for c in cnpj_base]
    
    # Primeiro DV (mesma lógica, valores diferentes)
    soma = sum(v * p for v, p in zip(valores, PESOS_DV1))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    # Segundo DV
    valores_com_dv1 = valores + [dv1]
    soma = sum(v * p for v, p in zip(valores_com_dv1, PESOS_DV2))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    return (dv1, dv2)
```

---

## ⚠️ Riscos Identificados

### Técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Falha na validação | Média | Alto | Golden Master + Shadow Mode |
| Performance degradada | Baixa | Médio | Benchmark antes/depois |
| Incompatibilidade | Alta | Alto | Testes de regressão extensivos |
| Perda de dados | Baixa | Crítico | Backup + validação dual |

### De Negócio

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Deadline Jul/2026 | Fixa | Crítico | Plano de contingência |
| Resistência à mudança | Média | Médio | Treinamento + documentação |
| Dependências externas | Alta | Alto | Mapeamento de integrações |

---

## 📅 Cronograma de Migração

### Visão Geral

```text
2025 Q4          2026 Q1          2026 Q2          2026 Q3
   │                │                │                │
   ▼                ▼                ▼                ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ FASE 1  │────│ FASE 2  │────│ FASE 3  │────│ FASE 4  │
│ Análise │    │ Testes  │    │ Rollout │    │ Cutover │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### Detalhamento por Fase

#### Fase 1: Análise e Caracterização (8 semanas)

| Semana | Atividade | Entregável |
|--------|-----------|------------|
| 1-2 | Análise do código legado | Documentação técnica |
| 3-4 | Testes de caracterização | Suite de 100+ testes |
| 5-6 | Golden Master | Arquivo com 10.000+ casos |
| 7-8 | Documentação de regras | Especificação completa |

#### Fase 2: Implementação e Testes (8 semanas)

| Semana | Atividade | Entregável |
|--------|-----------|------------|
| 9-10 | Implementar Facade | Código + testes |
| 11-12 | Suite de regressão | 4 níveis de testes |
| 13-14 | Shadow mode | Métricas de paridade |
| 15-16 | Ajustes e correções | Bugs corrigidos |

#### Fase 3: Rollout Gradual (8 semanas)

| Semana | Porcentagem | Critério de Avanço |
|--------|-------------|-------------------|
| 17-18 | 1% | Taxa de erro < 0.01% |
| 19-20 | 5% | Taxa de erro < 0.01% |
| 21-22 | 25% | Taxa de erro < 0.01% |
| 23-24 | 50% | Taxa de erro < 0.01% |

#### Fase 4: Cutover (4 semanas)

| Semana | Atividade | Entregável |
|--------|-----------|------------|
| 25-26 | 100% novo sistema | Legado desativado |
| 27-28 | Monitoramento | Relatório final |

---

## 🎓 Objetivos de Aprendizado

Ao completar este caso prático, você será capaz de:

1. **Analisar** sistemas legados e documentar comportamentos
2. **Criar** testes de caracterização e Golden Masters
3. **Implementar** Strangler Fig Pattern com Feature Flags
4. **Planejar** rollout gradual com métricas
5. **Executar** migração com zero downtime

---

## 🔗 Próximos Passos

1. **[Plano de Testes](plano-de-testes.md)** - Estratégia detalhada de testes
2. **[Implementação dos Testes](implementacao-testes.md)** - Código completo
3. **[Checklist Go-Live](checklist-go-live.md)** - Validação final
