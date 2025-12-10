# 🔄 Shift Left em Contexto de Sistema Legado

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- ✅ Adaptar os princípios de Shift Left para legados
- ✅ Entender a diferença entre Shift Left tradicional e em legados
- ✅ Aplicar a estratégia "Test First, Change Later"
- ✅ Criar um plano de testes progressivo

---

## 1. O Paradoxo do Shift Left em Legados

### 1.1 O Problema

**Shift Left tradicional** diz: *"Teste cedo, teste desde o início"*

**Mas em legados**: *O início já passou há 10 anos!*

```text
┌─────────────────────────────────────────────────────────────────┐
│          LINHA DO TEMPO - SHIFT LEFT TRADICIONAL                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Requisitos → Design → Código → Testes → Deploy → Produção      │
│      ▲                                                           │
│      │                                                           │
│      └── "Comece os testes AQUI" (Shift Left)                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│          LINHA DO TEMPO - SISTEMA LEGADO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [2005: Sistema criado sem testes]                              │
│           │                                                      │
│           ▼                                                      │
│  [2010: Cresceu, mais código sem testes]                        │
│           │                                                      │
│           ▼                                                      │
│  [2015: Devs originais saíram]                                  │
│           │                                                      │
│           ▼                                                      │
│  [2025: Você entra no projeto] ◄── VOCÊ ESTÁ AQUI               │
│           │                                                      │
│           ▼                                                      │
│  [2026: Precisa suportar CNPJ alfanumérico]                     │
│                                                                  │
│  Como aplicar "Shift Left" se o "Left" foi há 20 anos?         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 A Solução: Shift Left Adaptado

> **Em sistemas legados, Shift Left significa:**
> 
> *"Antes de fazer QUALQUER mudança, crie testes que documentem
> o comportamento atual. Depois, e só depois, mude o código."*

---

## 2. O Princípio: Test First, Change Later

### 2.1 A Regra de Ouro

```text
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   🥇 REGRA DE OURO PARA LEGADOS:                                │
│                                                                  │
│   "Nunca mude código legado sem antes ter testes que            │
│    provem que o comportamento atual está documentado."          │
│                                                                  │
│   Em outras palavras:                                            │
│   PRIMEIRO: Teste o que existe                                   │
│   DEPOIS:   Mude o código                                        │
│   POR FIM:  Verifique que os testes ainda passam                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Por Que Essa Ordem?

| Ordem | Ação | Risco |
|-------|------|-------|
| ❌ Errado | Mudar código → Criar testes | Você não sabe o que quebrou |
| ✅ Certo | Criar testes → Mudar código | Você sabe exatamente o que mudou |

**Exemplo com CNPJ**:

```python
# ❌ ERRADO: Mudar primeiro
def validar_cnpj(cnpj):
    cnpj = ''.join(c for c in cnpj if c.isalnum())  # Mudou de isdigit para isalnum
    # ... resto do código
    
# Se quebrar algo, como você sabe? Não tinha teste!


# ✅ CERTO: Testar primeiro
def test_validar_cnpj_numerico_atual():
    """Documenta comportamento ATUAL antes de mudar."""
    assert validar_cnpj("11222333000181") == True
    assert validar_cnpj("11.222.333/0001-81") == True
    assert validar_cnpj("00000000000000") == False
    assert validar_cnpj("ABCDE123000145") == False  # ← Atual: rejeita letras

# Agora você tem uma baseline!
# Se mudar e o teste quebrar, você sabe exatamente o que mudou.
```

---

## 3. Os 4 Passos do Shift Left em Legados

### Passo 1: Caracterizar (Entender o que existe)

```text
┌────────────────────────────────────────┐
│ 📋 CARACTERIZAR                         │
├────────────────────────────────────────┤
│                                         │
│ • Ler o código existente               │
│ • Identificar inputs e outputs         │
│ • Mapear dependências                  │
│ • Documentar comportamentos            │
│ • Criar testes de caracterização       │
│                                         │
│ Tempo: 40% do esforço total            │
│                                         │
└────────────────────────────────────────┘
```

### Passo 2: Cobrir (Criar rede de segurança)

```text
┌────────────────────────────────────────┐
│ 🛡️ COBRIR                               │
├────────────────────────────────────────┤
│                                         │
│ • Escrever testes unitários            │
│ • Criar testes de integração           │
│ • Definir golden masters               │
│ • Alcançar cobertura mínima (60-80%)   │
│ • Validar em ambiente isolado          │
│                                         │
│ Tempo: 30% do esforço total            │
│                                         │
└────────────────────────────────────────┘
```

### Passo 3: Mudar (Implementar a funcionalidade)

```text
┌────────────────────────────────────────┐
│ 🔧 MUDAR                                │
├────────────────────────────────────────┤
│                                         │
│ • Fazer mudanças incrementais          │
│ • Rodar testes após cada mudança       │
│ • Usar feature flags se possível       │
│ • Manter backward compatibility        │
│ • Code review rigoroso                 │
│                                         │
│ Tempo: 20% do esforço total            │
│                                         │
└────────────────────────────────────────┘
```

### Passo 4: Verificar (Garantir que nada quebrou)

```text
┌────────────────────────────────────────┐
│ ✅ VERIFICAR                            │
├────────────────────────────────────────┤
│                                         │
│ • Rodar todos os testes                │
│ • Comparar com golden masters          │
│ • Testar em staging                    │
│ • Smoke tests em produção              │
│ • Monitorar métricas de negócio        │
│                                         │
│ Tempo: 10% do esforço total            │
│                                         │
└────────────────────────────────────────┘
```

---

## 4. Exemplo Prático: Migração CNPJ

### 4.1 Situação Inicial

```python
# Sistema legado: validador_cnpj_2005.py
# Última alteração: 2012
# Testes: 0
# Linhas: 150
# Documentação: "Valida CNPJ"

def validar_cnpj(cnpj):
    """Valida CNPJ."""
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    
    if len(cnpj) != 14:
        return False
    
    if not cnpj.isdigit():
        return False
    
    if cnpj == cnpj[0] * 14:
        return False
    
    # Cálculo do primeiro DV
    soma = 0
    peso = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12):
        soma += int(cnpj[i]) * peso[i]
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj[12]) != dv1:
        return False
    
    # Cálculo do segundo DV
    soma = 0
    peso = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(13):
        soma += int(cnpj[i]) * peso[i]
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    return int(cnpj[13]) == dv2
```

### 4.2 Passo 1: Caracterizar

```python
# test_caracterizacao_cnpj.py
"""
Testes de Caracterização para validar_cnpj()

OBJETIVO: Documentar o comportamento ATUAL do sistema,
          NÃO o comportamento DESEJADO.

Se o teste falhar, significa que o código mudou!
"""

import pytest
from validador_cnpj_2005 import validar_cnpj


class TestCaracterizacaoCNPJ:
    """Documenta comportamento atual do validador."""
    
    # === CNPJs que o sistema ACEITA hoje ===
    
    def test_aceita_cnpj_numerico_valido(self):
        """Comportamento atual: aceita CNPJ numérico válido."""
        assert validar_cnpj("11222333000181") == True
    
    def test_aceita_cnpj_formatado(self):
        """Comportamento atual: aceita CNPJ com formatação."""
        assert validar_cnpj("11.222.333/0001-81") == True
    
    # === CNPJs que o sistema REJEITA hoje ===
    
    def test_rejeita_cnpj_curto(self):
        """Comportamento atual: rejeita CNPJ com menos de 14 dígitos."""
        assert validar_cnpj("1122233300018") == False
    
    def test_rejeita_cnpj_longo(self):
        """Comportamento atual: rejeita CNPJ com mais de 14 dígitos."""
        assert validar_cnpj("112223330001811") == False
    
    def test_rejeita_todos_iguais(self):
        """Comportamento atual: rejeita CNPJ com todos dígitos iguais."""
        assert validar_cnpj("11111111111111") == False
    
    def test_rejeita_dv_invalido(self):
        """Comportamento atual: rejeita CNPJ com DV errado."""
        assert validar_cnpj("11222333000182") == False  # DV correto é 81
    
    # === 🚨 COMPORTAMENTO CRÍTICO: Alfanuméricos ===
    
    def test_rejeita_cnpj_alfanumerico(self):
        """
        ⚠️ COMPORTAMENTO ATUAL: Rejeita CNPJs com letras!
        
        Este teste documenta que o sistema ATUAL não suporta
        o novo formato alfanumérico que entra em vigor em 2026.
        
        Quando adicionarmos suporte, este teste precisará mudar.
        """
        assert validar_cnpj("ABCDE123000145") == False
        assert validar_cnpj("AB.CDE.123/0001-45") == False
    
    def test_rejeita_cnpj_misto(self):
        """Comportamento atual: rejeita CNPJ com letras misturadas."""
        assert validar_cnpj("A1B2C3D4000199") == False
```

### 4.3 Passo 2: Cobrir

```python
# test_cobertura_cnpj.py
"""
Testes de Cobertura para garantir rede de segurança.

OBJETIVO: Garantir que todas as linhas do código estão cobertas
          por pelo menos um teste.
"""

import pytest
from validador_cnpj_2005 import validar_cnpj


class TestCoberturaValidacao:
    """Testes para 100% de cobertura de código."""
    
    # Cobertura: linha do len()
    @pytest.mark.parametrize("cnpj", [
        "",
        "123",
        "1234567890123",
        "123456789012345",
    ])
    def test_cobertura_validacao_tamanho(self, cnpj):
        """Cobre branch de validação de tamanho."""
        assert validar_cnpj(cnpj) == False
    
    # Cobertura: linha do isdigit()
    @pytest.mark.parametrize("cnpj", [
        "AAAAAAAAAAAAAA",
        "11222333000A81",
        "!@#$%^&*()_+{}",
    ])
    def test_cobertura_validacao_digitos(self, cnpj):
        """Cobre branch de validação de dígitos."""
        assert validar_cnpj(cnpj) == False
    
    # Cobertura: linha de todos iguais
    @pytest.mark.parametrize("digito", "0123456789")
    def test_cobertura_todos_iguais(self, digito):
        """Cobre branch de validação de dígitos repetidos."""
        cnpj = digito * 14
        assert validar_cnpj(cnpj) == False
    
    # Cobertura: cálculo DV1
    def test_cobertura_calculo_dv1_resto_zero(self):
        """Cobre branch onde resto DV1 < 2."""
        # Encontrar um CNPJ onde o resto seja 0 ou 1
        # (requer análise do algoritmo)
        pass  # Implementar baseado na análise
    
    # Cobertura: cálculo DV2
    def test_cobertura_calculo_dv2_resto_zero(self):
        """Cobre branch onde resto DV2 < 2."""
        pass  # Implementar baseado na análise
```

### 4.4 Passo 3: Mudar

```python
# validador_cnpj_2026.py (NOVA VERSÃO)
"""
Validador de CNPJ com suporte a formato alfanumérico.
Retrocompatível com formato numérico tradicional.
"""

def validar_cnpj(cnpj):
    """
    Valida CNPJ numérico ou alfanumérico.
    
    Suporta:
    - Formato numérico: 11.222.333/0001-81
    - Formato alfanumérico: AB.CDE.123/0001-45 (2026+)
    """
    # Remove formatação (MUDANÇA: aceita letras agora)
    cnpj = ''.join(c for c in cnpj.upper() if c.isalnum())
    
    if len(cnpj) != 14:
        return False
    
    # Valida estrutura: 8 alfanum + 6 numéricos
    raiz = cnpj[:8]
    sufixo = cnpj[8:]
    
    if not all(c.isalnum() for c in raiz):
        return False
    
    if not sufixo.isdigit():
        return False
    
    # Rejeita todos caracteres iguais
    if len(set(cnpj)) == 1:
        return False
    
    # Cálculo do DV (MUDANÇA: usa valor ASCII para letras)
    def char_value(c):
        if c.isdigit():
            return int(c)
        return ord(c) - 55  # A=10, B=11, ..., Z=35
    
    # Primeiro DV
    peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(char_value(cnpj[i]) * peso1[i] for i in range(12))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj[12]) != dv1:
        return False
    
    # Segundo DV
    peso2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(char_value(cnpj[i]) * peso2[i] for i in range(13))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    
    return int(cnpj[13]) == dv2
```

### 4.5 Passo 4: Verificar

```python
# test_verificacao_migracao.py
"""
Testes de Verificação pós-migração.

OBJETIVO: Garantir que:
1. Comportamento antigo ainda funciona (retrocompatibilidade)
2. Comportamento novo funciona (nova funcionalidade)
"""

import pytest
from validador_cnpj_2026 import validar_cnpj


class TestRetrocompatibilidade:
    """Garante que CNPJs numéricos antigos ainda funcionam."""
    
    def test_cnpj_numerico_valido_ainda_funciona(self):
        """Não quebramos os CNPJs antigos."""
        assert validar_cnpj("11222333000181") == True
        assert validar_cnpj("11.222.333/0001-81") == True
    
    def test_cnpj_numerico_invalido_ainda_rejeita(self):
        """Ainda rejeitamos CNPJs inválidos."""
        assert validar_cnpj("11222333000182") == False
        assert validar_cnpj("11111111111111") == False


class TestNovaFuncionalidade:
    """Testa o novo suporte a CNPJs alfanuméricos."""
    
    def test_cnpj_alfanumerico_valido(self):
        """Agora aceitamos CNPJs alfanuméricos válidos."""
        # Usar CNPJ com DV calculado corretamente
        assert validar_cnpj("ABCDE123000145") == True  # Assumindo DV correto
    
    def test_cnpj_alfanumerico_formatado(self):
        """Aceitamos CNPJs alfanuméricos com formatação."""
        assert validar_cnpj("AB.CDE.123/0001-45") == True
    
    def test_cnpj_alfanumerico_invalido(self):
        """Rejeitamos CNPJs alfanuméricos com DV errado."""
        assert validar_cnpj("ABCDE123000199") == False


class TestRegressao:
    """Testes de regressão para garantir que nada quebrou."""
    
    @pytest.mark.parametrize("cnpj,esperado", [
        # CNPJs válidos
        ("11222333000181", True),
        ("11.222.333/0001-81", True),
        # CNPJs inválidos
        ("11222333000182", False),
        ("11111111111111", False),
        ("", False),
        ("123", False),
    ])
    def test_regressao_comportamento_anterior(self, cnpj, esperado):
        """Todos os casos que funcionavam antes ainda funcionam."""
        assert validar_cnpj(cnpj) == esperado
```

---

## 5. O Diagrama Completo

```text
┌─────────────────────────────────────────────────────────────────┐
│           SHIFT LEFT EM SISTEMAS LEGADOS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TRADICIONAL (sistema novo):                                     │
│                                                                  │
│  Requisitos → Testes → Código → Deploy                          │
│      ◄───── Shift Left ─────►                                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  EM LEGADOS:                                                     │
│                                                                  │
│  [Código existe há anos sem testes]                             │
│              │                                                   │
│              ▼                                                   │
│  ┌───────────────────┐                                          │
│  │ 1. CARACTERIZAR   │ ← Entender o que existe                  │
│  │    (Criar testes  │                                          │
│  │     que documentam│                                          │
│  │     comportamento)│                                          │
│  └─────────┬─────────┘                                          │
│            │                                                     │
│            ▼                                                     │
│  ┌───────────────────┐                                          │
│  │ 2. COBRIR         │ ← Criar rede de segurança                │
│  │    (Alcançar      │                                          │
│  │     cobertura     │                                          │
│  │     adequada)     │                                          │
│  └─────────┬─────────┘                                          │
│            │                                                     │
│            ▼                                                     │
│  ┌───────────────────┐                                          │
│  │ 3. MUDAR          │ ← Só agora mexer no código               │
│  │    (Implementar   │                                          │
│  │     nova          │                                          │
│  │     funcionalidade│                                          │
│  └─────────┬─────────┘                                          │
│            │                                                     │
│            ▼                                                     │
│  ┌───────────────────┐                                          │
│  │ 4. VERIFICAR      │ ← Garantir que nada quebrou              │
│  │    (Rodar todos   │                                          │
│  │     os testes)    │                                          │
│  └───────────────────┘                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Resumo

### 6.1 Pontos-Chave

| Conceito | Em Sistema Novo | Em Sistema Legado |
|----------|-----------------|-------------------|
| **Shift Left** | Testes antes do código | Testes antes da mudança |
| **Primeiro passo** | Escrever requisitos | Documentar comportamento atual |
| **Rede de segurança** | TDD desde o início | Characterization tests |
| **Objetivo** | Prevenir bugs | Não criar bugs novos |

### 6.2 A Frase Para Lembrar

> **"Em legados, não escrevemos testes para o código que queremos.**
> **Escrevemos testes para o código que temos.**
> **Só depois mudamos o código."**

---

**Próximo**: [04-estrategias-de-migracao.md](04-estrategias-de-migracao.md)
