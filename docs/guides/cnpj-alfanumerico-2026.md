# CNPJ Alfanumérico 2026 - Guia Técnico Completo

## Visão Geral

A partir de **julho de 2026**, a Receita Federal do Brasil implementará uma mudança significativa no formato do CNPJ: a possibilidade de incluir **letras (A-Z)** nos 8 primeiros caracteres (raiz), além dos números tradicionais.

Este documento fornece especificações técnicas para implementação e validação do novo formato.

---

## 1. Contexto da Mudança

### 1.1 Por que a mudança?

O formato numérico atual (14 dígitos) possui capacidade limitada:
- **Combinações possíveis na raiz**: 10⁸ = 100 milhões
- **CNPJs já atribuídos**: ~55 milhões (dados de 2024)
- **Projeção de esgotamento**: Entre 2026-2030

Com a inclusão de letras:
- **Novas combinações**: 36⁸ ≈ 2,8 trilhões
- **Capacidade expandida**: Suficiente para séculos

### 1.2 Base Legal

| Documento | Descrição |
|-----------|-----------|
| IN RFB nº 2.119/2022 | Norma atual do CNPJ |
| Nota Técnica RFB 2024 | Especificação do formato alfanumérico |
| Portaria RFB (prevista) | Regulamentação final |

### 1.3 Cronograma

| Data | Evento |
|------|--------|
| 2024 | Anúncio oficial da Receita Federal |
| Jan/2026 | Início do período de adaptação |
| **Jul/2026** | **Entrada em vigor oficial** |
| 2027+ | Migração gradual de sistemas legados |

---

## 2. Estrutura do Novo Formato

### 2.1 Composição

```
AA.AAA.AAA/NNNN-DD
```

| Parte | Posição | Caracteres Permitidos | Descrição |
|-------|---------|----------------------|-----------|
| **Raiz** | 1-8 | A-Z, 0-9 (36 chars) | Identificação da empresa |
| **Ordem** | 9-12 | 0-9 (10 chars) | Matriz (0001) ou filial |
| **DV** | 13-14 | 0-9 (10 chars) | Dígitos verificadores |

### 2.2 Regras de Formatação

```
Posição dos separadores:
- Ponto (.) após posição 2: XX.
- Ponto (.) após posição 5: XX.XXX.
- Barra (/) após posição 8: XX.XXX.XXX/
- Hífen (-) após posição 12: XX.XXX.XXX/XXXX-
```

### 2.3 Exemplos Válidos

| CNPJ | Tipo | Descrição |
|------|------|-----------|
| `AB.CDE.123/0001-45` | Alfanumérico | Raiz mista (letras + números) |
| `XY.ZAB.CDE/0001-78` | Alfanumérico | Raiz apenas letras |
| `11.222.333/0001-81` | Numérico | Formato tradicional (continua válido) |
| `A1.B2C.3D4/0002-99` | Alfanumérico | Filial (ordem > 0001) |

### 2.4 Exemplos Inválidos

| CNPJ | Erro |
|------|------|
| `AB.CDE.123/ABCD-45` | Ordem deve ser numérica |
| `AB.CDE.123/0001-AB` | DV deve ser numérico |
| `ab.cde.123/0001-45` | Letras devem ser maiúsculas* |
| `AB.CDE.12@/0001-45` | Caractere especial inválido |

> *Nota: Nossa implementação aceita minúsculas e converte automaticamente para maiúsculas.

---

## 3. Tabela de Conversão ASCII

### 3.1 Mapeamento de Caracteres para Cálculo do DV

Para calcular os dígitos verificadores, cada caractere é convertido para um valor numérico:

#### Números (0-9)
| Char | ASCII | Valor DV |
|------|-------|----------|
| 0 | 48 | 0 |
| 1 | 49 | 1 |
| 2 | 50 | 2 |
| 3 | 51 | 3 |
| 4 | 52 | 4 |
| 5 | 53 | 5 |
| 6 | 54 | 6 |
| 7 | 55 | 7 |
| 8 | 56 | 8 |
| 9 | 57 | 9 |

#### Letras (A-Z)
| Char | ASCII | Valor DV |
|------|-------|----------|
| A | 65 | 10 |
| B | 66 | 11 |
| C | 67 | 12 |
| D | 68 | 13 |
| E | 69 | 14 |
| F | 70 | 15 |
| G | 71 | 16 |
| H | 72 | 17 |
| I | 73 | 18 |
| J | 74 | 19 |
| K | 75 | 20 |
| L | 76 | 21 |
| M | 77 | 22 |
| N | 78 | 23 |
| O | 79 | 24 |
| P | 80 | 25 |
| Q | 81 | 26 |
| R | 82 | 27 |
| S | 83 | 28 |
| T | 84 | 29 |
| U | 85 | 30 |
| V | 86 | 31 |
| W | 87 | 32 |
| X | 88 | 33 |
| Y | 89 | 34 |
| Z | 90 | 35 |

### 3.2 Fórmula de Conversão

```python
def get_char_value(char: str) -> int:
    """Converte caractere para valor numérico."""
    char = char.upper()
    if char.isdigit():
        return int(char)  # 0-9
    else:
        return ord(char) - 55  # A=10, B=11, ..., Z=35
```

---

## 4. Algoritmo de Cálculo do DV

### 4.1 Pesos (Módulo 11)

O algoritmo continua usando Módulo 11, com os mesmos pesos do CNPJ tradicional:

```
Primeiro DV: [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
Segundo DV:  [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
```

### 4.2 Exemplo de Cálculo

**CNPJ**: `AB12CD340001` (sem formatação, 12 caracteres para calcular 1º DV)

**Passo 1**: Converter cada caractere para valor numérico

```
A  B  1  2  C  D  3  4  0  0  0  1
10 11 1  2  12 13 3  4  0  0  0  1
```

**Passo 2**: Multiplicar pelos pesos

```
Char:  A   B   1   2   C   D   3   4   0   0   0   1
Valor: 10  11  1   2   12  13  3   4   0   0   0   1
Peso:  5   4   3   2   9   8   7   6   5   4   3   2
─────────────────────────────────────────────────────
       50  44  3   4   108 104 21  24  0   0   0   2
```

**Passo 3**: Somar os resultados

```
50 + 44 + 3 + 4 + 108 + 104 + 21 + 24 + 0 + 0 + 0 + 2 = 360
```

**Passo 4**: Calcular módulo 11

```
360 % 11 = 8
```

**Passo 5**: Aplicar regra

```
Se resto < 2: DV = 0
Senão: DV = 11 - resto

11 - 8 = 3  →  Primeiro DV = 3
```

**Passo 6**: Repetir para segundo DV (incluindo o primeiro)

```
AB12CD3400013 → Segundo DV = X
```

### 4.3 Implementação em Python

```python
class NewAlphanumericCNPJValidator:
    WEIGHTS_FIRST = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    WEIGHTS_SECOND = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    @staticmethod
    def get_char_value(char: str) -> int:
        char = char.upper()
        if char.isdigit():
            return int(char)
        return ord(char) - 55  # A=10, ..., Z=35
    
    @staticmethod
    def calculate_digit(cnpj: str, weights: list) -> int:
        total = sum(
            NewAlphanumericCNPJValidator.get_char_value(c) * w 
            for c, w in zip(cnpj, weights)
        )
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
```

---

## 5. Validações Necessárias

### 5.1 Checklist de Validação

| # | Validação | Regra |
|---|-----------|-------|
| 1 | Tamanho | Exatamente 14 caracteres (sem formatação) |
| 2 | Raiz (1-8) | Apenas A-Z e 0-9 |
| 3 | Ordem (9-12) | Apenas 0-9, não pode ser 0000 |
| 4 | DV (13-14) | Apenas 0-9 |
| 5 | Não repetido | Não pode ter todos caracteres iguais |
| 6 | DV válido | Dígitos verificadores corretos |

### 5.2 Regex de Validação

```python
# CNPJ sem formatação (14 caracteres)
pattern_clean = r'^[A-Z0-9]{8}[0-9]{6}$'

# CNPJ formatado (XX.XXX.XXX/XXXX-XX)
pattern_formatted = r'^[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}/[0-9]{4}-[0-9]{2}$'
```

### 5.3 Casos de Teste Recomendados

```python
# CNPJs alfanuméricos válidos para teste
VALID_ALPHANUMERIC = [
    "AB.CDE.123/0001-XX",  # Calcular DV correto
    "XY.ZAB.CDE/0001-XX",  # Apenas letras na raiz
    "A1.B2C.3D4/0001-XX",  # Alternado
]

# CNPJs inválidos para teste
INVALID_CASES = [
    ("AB.CDE.123/ABCD-45", "Ordem com letras"),
    ("AB.CDE.12!/0001-45", "Caractere especial"),
    ("AA.AAA.AAA/0000-00", "Ordem zerada"),
    ("AA.AAA.AAA/AAAA-AA", "Todos campos com letras"),
]
```

---

## 6. Compatibilidade

### 6.1 Retrocompatibilidade

| Cenário | Suporte |
|---------|---------|
| CNPJ numérico tradicional | ✅ Continua válido |
| Sistemas legados | ⚠️ Requerem atualização |
| APIs da Receita Federal | 🔄 Atualização em Jul/2026 |

### 6.2 Estratégia de Migração

```
1. Validação local      → Implementar NewAlphanumericCNPJValidator
2. Banco de dados       → Alterar campos de CHAR(14) para VARCHAR(14)
3. Formulários          → Aceitar entrada alfanumérica
4. Integrações          → Aguardar APIs oficiais
5. Relatórios           → Adaptar máscaras de exibição
```

---

## 7. API de Validação

### 7.1 Endpoints Disponíveis

```
POST /api/v1/validate/alphanumeric
GET  /api/v1/validate/alphanumeric/{cnpj}
GET  /api/v1/generate/alphanumeric
```

### 7.2 Exemplo de Uso

```bash
# Validar CNPJ alfanumérico
curl -X GET "http://localhost:8000/api/v1/validate/alphanumeric/AB.CDE.123/0001-45"

# Gerar CNPJ alfanumérico válido
curl -X GET "http://localhost:8000/api/v1/generate/alphanumeric?raiz=TESTECNP"
```

### 7.3 Resposta de Validação

```json
{
  "valid": true,
  "cnpj_formatted": "AB.CDE.123/0001-45",
  "cnpj_clean": "ABCDE123000145",
  "is_alphanumeric": true,
  "is_matriz": true,
  "parts": {
    "raiz": "ABCDE123",
    "ordem": "0001",
    "dv": "45"
  },
  "validation_details": {
    "root_valid": true,
    "order_valid": true,
    "dv_valid": true,
    "has_letters": true
  },
  "errors": []
}
```

---

## 8. Limitações Atuais

### 8.1 APIs Externas

| API | Suporte Alfanumérico | Status |
|-----|---------------------|--------|
| BrasilAPI | ❌ Não | Aguardando atualização |
| ReceitaWS | ❌ Não | Aguardando atualização |
| API Oficial RFB | 🔄 Previsto Jul/2026 | Em desenvolvimento |

### 8.2 Consulta de Dados Cadastrais

Até julho de 2026, a consulta de dados cadastrais na Receita Federal só funciona para CNPJs **numéricos**. 

Para CNPJs **alfanuméricos**, apenas a validação local está disponível.

```python
# FUNCIONA: Validação local
result = NewAlphanumericCNPJValidator.validate("AB.CDE.123/0001-45")

# NÃO FUNCIONA (ainda): Consulta externa
api = ReceitaFederalAPI()
dados = api.consultar("AB.CDE.123/0001-45")  # Erro!
```

---

## 9. Referências

- [Receita Federal - CNPJ](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/cnpj)
- [IN RFB nº 2.119/2022](http://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=127371)
- [Código fonte: NewAlphanumericCNPJValidator](../src/cnpj_validator/validators/new_alphanumeric_validator.py)
- [Testes: test_new_alphanumeric_validator.py](../tests/test_new_alphanumeric_validator.py)

---

## 10. Histórico do Documento

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 10/12/2025 | CNPJ-QA-Training | Versão inicial |

---

> **Nota**: Este documento será atualizado conforme a Receita Federal publicar novas especificações oficiais.
