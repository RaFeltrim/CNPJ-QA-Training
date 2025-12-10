# 🔬 Characterization Tests (Testes de Caracterização)

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- ✅ Entender o que são testes de caracterização
- ✅ Criar testes que documentam comportamento existente
- ✅ Aplicar a técnica em código legado real
- ✅ Usar testes de caracterização como rede de segurança

---

## 1. O Que São Testes de Caracterização?

### 1.1 Definição

> **Characterization Test** = Um teste que documenta o comportamento **atual** do sistema,
> não o comportamento **esperado** ou **desejado**.

```text
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  TESTE TRADICIONAL:                                              │
│  "O sistema DEVE fazer X" (requisito)                           │
│                                                                  │
│  TESTE DE CARACTERIZAÇÃO:                                        │
│  "O sistema FAZ X" (documentação do comportamento atual)        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Por Que Criar?

| Situação | Solução |
|----------|---------|
| "Não sei o que esse código faz" | Teste de caracterização descobre |
| "Tenho medo de quebrar algo" | Teste de caracterização protege |
| "Não existe documentação" | Teste de caracterização documenta |
| "Preciso refatorar código" | Teste de caracterização valida |

### 1.3 Analogia: O Detetive

Imagine que você é um detetive investigando um sistema legado:

```text
DETETIVE (QA):
├── Pista 1: O que essa função recebe? (inputs)
├── Pista 2: O que ela retorna? (outputs)
├── Pista 3: O que ela faz de "estranho"? (efeitos colaterais)
└── Conclusão: Documentar em forma de teste
```

---

## 2. Como Criar Testes de Caracterização

### 2.1 O Processo em 5 Passos

```text
┌────────────────────────────────────────────────────────────────┐
│              PROCESSO DE CARACTERIZAÇÃO                         │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. IDENTIFICAR                                                  │
│     └── Qual função/módulo precisa ser caracterizado?           │
│                                                                  │
│  2. EXPLORAR                                                     │
│     └── Quais inputs são possíveis?                             │
│     └── Quais são os casos de borda?                            │
│                                                                  │
│  3. EXECUTAR                                                     │
│     └── Rodar o código com diferentes inputs                    │
│     └── Observar os outputs                                     │
│                                                                  │
│  4. DOCUMENTAR                                                   │
│     └── Transformar observações em asserts                      │
│     └── Criar teste que captura o comportamento                 │
│                                                                  │
│  5. VALIDAR                                                      │
│     └── Rodar o teste (deve passar!)                            │
│     └── Se falhar: seu teste está errado, não o código          │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 Exemplo Prático: Validador de CNPJ Legado

**Código legado** (sem documentação):

```python
# arquivo: legacy/cnpj_utils.py
# Última modificação: 2010
# Autor: desconhecido

def proc_cnpj(c, f=True):
    """Processa CNPJ."""
    if not c:
        return None
    c = ''.join(x for x in str(c) if x.isdigit())
    if len(c) != 14:
        return False if f else c
    if c == c[0] * 14:
        return False if f else c
    s = 0
    for i, p in enumerate([5,4,3,2,9,8,7,6,5,4,3,2]):
        s += int(c[i]) * p
    d1 = 0 if s % 11 < 2 else 11 - s % 11
    if int(c[12]) != d1:
        return False if f else c
    s = 0
    for i, p in enumerate([6,5,4,3,2,9,8,7,6,5,4,3,2]):
        s += int(c[i]) * p
    d2 = 0 if s % 11 < 2 else 11 - s % 11
    return (int(c[13]) == d2) if f else c if int(c[13]) == d2 else False
```

**Perguntas que surgem**:
- O que é `c`? (provavelmente CNPJ)
- O que é `f`? (flag... de quê?)
- O que retorna quando `f=True` vs `f=False`?
- Por que às vezes retorna `None`, `False`, ou o próprio CNPJ?

### 2.3 Passo 1: Identificar

```python
# O que sabemos:
# - Função: proc_cnpj(c, f=True)
# - Parece validar CNPJ
# - Tem comportamento diferente baseado em 'f'
```

### 2.4 Passo 2: Explorar

```python
# Categorias de input para testar:
inputs_explorar = {
    "valores_nulos": [None, "", 0],
    "tamanhos_errados": ["123", "12345678901234567890"],
    "cnpjs_validos": ["11222333000181", "11.222.333/0001-81"],
    "cnpjs_invalidos": ["11222333000182", "00000000000000"],
    "todos_iguais": ["11111111111111", "00000000000000"],
    "com_letras": ["1122233300AB81", "ABCDEFGHIJKLMN"],
}
```

### 2.5 Passo 3: Executar

```python
# Script de exploração (rodar manualmente)
from legacy.cnpj_utils import proc_cnpj

# Explorar com f=True (default)
print("=== f=True (default) ===")
print(f"None        -> {proc_cnpj(None)}")
print(f"''          -> {proc_cnpj('')}")
print(f"'123'       -> {proc_cnpj('123')}")
print(f"'11222333000181' -> {proc_cnpj('11222333000181')}")
print(f"'11.222.333/0001-81' -> {proc_cnpj('11.222.333/0001-81')}")
print(f"'11222333000182' -> {proc_cnpj('11222333000182')}")
print(f"'11111111111111' -> {proc_cnpj('11111111111111')}")

# Explorar com f=False
print("\n=== f=False ===")
print(f"None        -> {proc_cnpj(None, f=False)}")
print(f"'123'       -> {proc_cnpj('123', f=False)}")
print(f"'11222333000181' -> {proc_cnpj('11222333000181', f=False)}")
print(f"'11222333000182' -> {proc_cnpj('11222333000182', f=False)}")

# Output observado:
# === f=True (default) ===
# None        -> None
# ''          -> None
# '123'       -> False
# '11222333000181' -> True
# '11.222.333/0001-81' -> True
# '11222333000182' -> False
# '11111111111111' -> False
#
# === f=False ===
# None        -> None
# '123'       -> 123  (retorna o próprio valor limpo!)
# '11222333000181' -> 11222333000181
# '11222333000182' -> False
```

### 2.6 Passo 4: Documentar

```python
# test_characterization_proc_cnpj.py
"""
Testes de Caracterização para proc_cnpj()

⚠️ IMPORTANTE: Estes testes documentam o comportamento ATUAL,
   não o comportamento desejado. Se um teste falhar após uma
   mudança, significa que o comportamento foi alterado.

Descobertas:
- 'c' = CNPJ a processar
- 'f' = flag de modo (True=validação, False=limpeza+validação)
- f=True: retorna bool (True/False) ou None
- f=False: retorna CNPJ limpo se válido, False se inválido, valor limpo se tamanho errado
"""

import pytest
from legacy.cnpj_utils import proc_cnpj


class TestCharacterizationProcCnpj:
    """Documentação via testes do comportamento de proc_cnpj()."""
    
    # ===== MODO VALIDAÇÃO (f=True, default) =====
    
    class TestModoValidacao:
        """Comportamento quando f=True (modo de validação)."""
        
        def test_none_retorna_none(self):
            """Caracterização: None como input retorna None."""
            assert proc_cnpj(None) is None
        
        def test_string_vazia_retorna_none(self):
            """Caracterização: String vazia retorna None."""
            assert proc_cnpj("") is None
        
        def test_cnpj_curto_retorna_false(self):
            """Caracterização: CNPJ com menos de 14 dígitos retorna False."""
            assert proc_cnpj("123") == False
            assert proc_cnpj("1234567890123") == False
        
        def test_cnpj_longo_retorna_false(self):
            """Caracterização: CNPJ com mais de 14 dígitos retorna False."""
            assert proc_cnpj("123456789012345") == False
        
        def test_cnpj_valido_retorna_true(self):
            """Caracterização: CNPJ válido retorna True."""
            assert proc_cnpj("11222333000181") == True
        
        def test_cnpj_formatado_retorna_true(self):
            """Caracterização: Remove formatação antes de validar."""
            assert proc_cnpj("11.222.333/0001-81") == True
        
        def test_cnpj_dv_errado_retorna_false(self):
            """Caracterização: CNPJ com DV incorreto retorna False."""
            assert proc_cnpj("11222333000182") == False
        
        def test_cnpj_todos_iguais_retorna_false(self):
            """Caracterização: CNPJ com todos dígitos iguais retorna False."""
            assert proc_cnpj("11111111111111") == False
            assert proc_cnpj("00000000000000") == False
        
        def test_cnpj_com_letras_retorna_false(self):
            """
            Caracterização: CNPJ com letras retorna False.
            
            ⚠️ NOTA: Este comportamento precisará mudar em 2026
            quando CNPJs alfanuméricos forem permitidos.
            """
            assert proc_cnpj("1122233300AB81") == False
            assert proc_cnpj("ABCDEFGHIJKLMN") == False
    
    # ===== MODO LIMPEZA (f=False) =====
    
    class TestModoLimpeza:
        """
        Comportamento quando f=False (modo de limpeza).
        
        Descoberta: Este modo retorna o CNPJ limpo se válido,
        ou o valor limpo mesmo se tamanho errado (comportamento estranho).
        """
        
        def test_none_retorna_none(self):
            """Caracterização: None retorna None mesmo com f=False."""
            assert proc_cnpj(None, f=False) is None
        
        def test_cnpj_curto_retorna_valor_limpo(self):
            """
            Caracterização: CNPJ curto retorna o valor limpo!
            
            ⚠️ COMPORTAMENTO ESTRANHO: Diferente de f=True que retorna False.
            Isso pode ser um bug ou feature intencional.
            """
            assert proc_cnpj("123", f=False) == "123"
        
        def test_cnpj_valido_retorna_cnpj_limpo(self):
            """Caracterização: CNPJ válido retorna string limpa."""
            assert proc_cnpj("11222333000181", f=False) == "11222333000181"
        
        def test_cnpj_formatado_retorna_limpo(self):
            """Caracterização: Remove formatação e retorna limpo."""
            assert proc_cnpj("11.222.333/0001-81", f=False) == "11222333000181"
        
        def test_cnpj_dv_errado_retorna_false(self):
            """Caracterização: DV errado retorna False mesmo com f=False."""
            assert proc_cnpj("11222333000182", f=False) == False
```

### 2.7 Passo 5: Validar

```bash
# Rodar os testes de caracterização
pytest test_characterization_proc_cnpj.py -v

# Esperado: TODOS devem passar!
# Se algum falhar, seu teste está errado, não o código legado.
```

---

## 3. Boas Práticas

### 3.1 Nomenclatura

```python
# ✅ BOM: Nome descritivo do comportamento observado
def test_cnpj_com_letras_retorna_false(self):
    """Caracterização: CNPJ com letras retorna False."""

# ❌ RUIM: Nome genérico
def test_validacao_1(self):
    pass
```

### 3.2 Documentação

```python
# ✅ BOM: Docstring explicando o comportamento
def test_cnpj_curto_retorna_valor_limpo(self):
    """
    Caracterização: CNPJ curto retorna o valor limpo!
    
    ⚠️ COMPORTAMENTO ESTRANHO: Diferente de f=True que retorna False.
    Isso pode ser um bug ou feature intencional.
    Manter comportamento até validar com stakeholders.
    """

# ❌ RUIM: Sem documentação
def test_cnpj_curto(self):
    assert proc_cnpj("123", f=False) == "123"
```

### 3.3 Marcar Comportamentos Estranhos

```python
# Use marcadores para destacar comportamentos que precisam de atenção

import pytest

@pytest.mark.comportamento_estranho
def test_tamanho_errado_nao_retorna_erro(self):
    """
    ⚠️ COMPORTAMENTO POTENCIALMENTE PROBLEMÁTICO
    
    O sistema aceita CNPJs de qualquer tamanho em modo f=False.
    Isso pode permitir dados inválidos no banco.
    
    TODO: Validar com PO se é intencional.
    """
    assert proc_cnpj("123", f=False) == "123"


@pytest.mark.mudanca_2026
def test_rejeita_letras_atualmente(self):
    """
    🔄 COMPORTAMENTO QUE MUDARÁ EM 2026
    
    Atualmente rejeita CNPJs com letras.
    Em julho/2026, precisará aceitar.
    """
    assert proc_cnpj("ABCDE123000145") == False
```

---

## 4. Exercício Prático

### 4.1 Desafio

Você recebeu este código legado. Crie testes de caracterização:

```python
# legacy/format_utils.py
def fmt(v, t='cpf'):
    if not v: return v
    v = ''.join(c for c in str(v) if c.isdigit())
    if t == 'cpf' and len(v) == 11:
        return f'{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}'
    elif t == 'cnpj' and len(v) == 14:
        return f'{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:]}'
    elif t == 'tel' and len(v) >= 10:
        if len(v) == 11:
            return f'({v[:2]}) {v[2:7]}-{v[7:]}'
        return f'({v[:2]}) {v[2:6]}-{v[6:]}'
    return v
```

### 4.2 Template de Resposta

```python
# test_characterization_fmt.py

import pytest
from legacy.format_utils import fmt


class TestCharacterizationFmt:
    """Testes de caracterização para fmt()."""
    
    class TestValoresNulos:
        """O que acontece com valores nulos/vazios?"""
        
        def test_none_retorna_none(self):
            # Descobrir: o que retorna para None?
            assert fmt(None) == ???  # Preencha após testar
        
        def test_string_vazia_retorna_???(self):
            assert fmt("") == ???
    
    class TestCPF:
        """Comportamento para t='cpf' (default)."""
        
        def test_cpf_11_digitos_formata(self):
            assert fmt("12345678901") == ???
        
        def test_cpf_formatado_reformata(self):
            assert fmt("123.456.789-01") == ???
        
        def test_cpf_tamanho_errado_retorna_???(self):
            assert fmt("123456789") == ???
    
    # Continue para CNPJ e telefone...
```

---

## 5. Resumo

### 5.1 Checklist de Caracterização

```text
☐ Identifiquei a função/módulo a caracterizar
☐ Listei todas as categorias de input possíveis
☐ Executei o código com cada categoria
☐ Documentei os outputs observados
☐ Criei testes que capturam o comportamento
☐ Todos os testes passam
☐ Marquei comportamentos estranhos
☐ Documentei comportamentos que precisam mudar no futuro
```

### 5.2 Quando Usar

| Situação | Use Characterization Tests? |
|----------|----------------------------|
| Antes de refatorar código legado | ✅ Sim, sempre |
| Antes de adicionar nova feature | ✅ Sim |
| Código sem documentação | ✅ Sim |
| Bug em produção para investigar | ✅ Sim |
| Código novo com TDD | ❌ Não, use testes tradicionais |

---

**Próximo**: [02-golden-master-testing.md](02-golden-master-testing.md)
