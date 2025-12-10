# 📚 O Que São Sistemas Legados?

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- ✅ Definir o que caracteriza um sistema legado
- ✅ Identificar sistemas legados em seu ambiente de trabalho
- ✅ Entender por que sistemas legados são críticos para os negócios
- ✅ Reconhecer os sinais de alerta de um sistema legado

---

## 1. Definição

### 1.1 O Que É Um Sistema Legado?

> **Sistema Legado** (do inglês *Legacy System*) é qualquer sistema de software
> que continua em uso, mas foi desenvolvido com tecnologias, padrões ou práticas
> que são consideradas ultrapassadas.

**Importante**: Legado não significa necessariamente "ruim" ou "quebrado". Significa que o sistema:

- Foi criado em uma época diferente
- Usa tecnologias que não são mais as preferidas
- Tem dívida técnica acumulada
- É difícil de modificar com segurança

### 1.2 Analogia: A Casa Antiga

Imagine uma casa construída em 1950:

| Característica | Casa Antiga | Sistema Legado |
|----------------|-------------|----------------|
| **Funciona?** | Sim, pessoas moram lá | Sim, negócio depende dele |
| **É segura?** | Em geral, sim | Em geral, sim |
| **Fácil de modificar?** | Não, estrutura antiga | Não, código antigo |
| **Documentação?** | Plantas perdidas | Documentação desatualizada |
| **Quem construiu?** | Engenheiros que não trabalham mais | Desenvolvedores que saíram |
| **Atualização necessária?** | Sim, fiação elétrica | Sim, novas funcionalidades |

---

## 2. Características de Sistemas Legados

### 2.1 Sinais Técnicos

```text
┌─────────────────────────────────────────────────────────────────┐
│ ⚠️ CHECKLIST: É UM SISTEMA LEGADO?                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ [ ] Linguagem/framework descontinuado ou obsoleto               │
│ [ ] Documentação inexistente ou desatualizada                   │
│ [ ] Poucos ou nenhum teste automatizado                         │
│ [ ] Desenvolvedores originais não trabalham mais na empresa     │
│ [ ] Medo de fazer alterações ("não mexe que está funcionando")  │
│ [ ] Arquitetura monolítica e fortemente acoplada                │
│ [ ] Código espaguete ou difícil de entender                     │
│ [ ] Dependências de bibliotecas antigas sem manutenção          │
│ [ ] Banco de dados com schema rígido e sem migrations           │
│ [ ] Deploy manual ou processo complexo                          │
│                                                                  │
│ Se marcou 3+ itens: provavelmente é um legado!                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Sinais de Negócio

- **Alta criticidade**: O sistema é essencial para operações diárias
- **Muitos usuários**: Centenas ou milhares dependem dele
- **Integrações**: Outros sistemas se conectam a ele
- **Conhecimento tribal**: Só algumas pessoas sabem como funciona
- **Custo de substituição**: Muito caro para reescrever do zero

---

## 3. Exemplo Prático: Sistema de CNPJ Legado

### 3.1 Cenário

Imagine um sistema bancário desenvolvido em 2005 que valida CNPJs:

```python
# Código legado típico (Python 2.5, ano 2005)
# Arquivo: validador_cnpj.py

def valida_cnpj(cnpj):
    """Valida CNPJ - Apenas números permitidos"""
    # Remove formatação
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    
    # Verifica se tem 14 dígitos numéricos
    if len(cnpj) != 14:
        return False
    
    if not cnpj.isdigit():  # ← PROBLEMA: Não aceita letras!
        return False
    
    # Calcula DVs...
    # (código de validação omitido)
    
    return True
```

### 3.2 O Problema em 2026

Com o CNPJ alfanumérico:

```python
# Tentando validar CNPJ novo no sistema legado
cnpj_novo = "AB.CDE.123/0001-45"

resultado = valida_cnpj(cnpj_novo)
print(resultado)  # False - REJEITADO!

# O sistema legado não reconhece CNPJs com letras
# Resultado: Clientes não conseguem se cadastrar!
```

### 3.3 Por Que Não "Apenas Mudar"?

| Risco | Descrição |
|-------|-----------|
| **Sem testes** | Ninguém sabe o que pode quebrar |
| **Muitas dependências** | 50+ sistemas usam essa função |
| **Dados históricos** | 10 anos de CNPJs numéricos no banco |
| **Regulamentação** | Banco Central exige auditoria de mudanças |
| **Conhecimento perdido** | Dev original saiu em 2015 |

---

## 4. Tipos de Sistemas Legados

### 4.1 Classificação por Idade

| Tipo | Idade | Características | Estratégia |
|------|-------|-----------------|------------|
| **Brownfield** | 2-5 anos | Código recente mas já com dívida técnica | Refatorar |
| **Legacy** | 5-15 anos | Tecnologia datada, pouca documentação | Estrangular |
| **Ancient** | 15+ anos | Linguagens mortas, hardware específico | Substituir |

### 4.2 Classificação por Criticidade

```text
         Alta Criticidade
              ▲
              │
    ┌─────────┼─────────┐
    │ CRÍTICO │ NUCLEAR │
    │ Migrar  │ Cuidado │
    │ com     │ extremo │
    │ cautela │         │
    ├─────────┼─────────┤
    │ ROTINA  │ LEGADO  │
    │ Pode    │ Pode    │
    │ esperar │ evoluir │
    │         │ gradual │
    └─────────┼─────────┘
              │
              ▼
        Baixa Criticidade
    
    ◄─────────┼─────────►
    Baixo     │    Alto
    Valor     │    Valor
    de        │    de
    Negócio   │    Negócio
```

---

## 5. O Paradoxo do Legado

### 5.1 Por Que Legados Persistem?

```text
┌──────────────────────────────────────────────────────────┐
│                  O CICLO VICIOSO                          │
│                                                           │
│   ┌─────────┐         ┌─────────────┐                    │
│   │ Sistema │────────►│ Funciona    │                    │
│   │ Legado  │         │ (de alguma  │                    │
│   │         │         │  forma)     │                    │
│   └────▲────┘         └──────┬──────┘                    │
│        │                     │                            │
│        │                     ▼                            │
│   ┌────┴────┐         ┌─────────────┐                    │
│   │ Ninguém │◄────────│ Ninguém     │                    │
│   │ quer    │         │ entende o   │                    │
│   │ mexer   │         │ código      │                    │
│   └─────────┘         └─────────────┘                    │
│                                                           │
│   "Se está funcionando, não mexe!"                       │
└──────────────────────────────────────────────────────────┘
```

### 5.2 O Custo Real

| Métrica | Sistema Moderno | Sistema Legado |
|---------|-----------------|----------------|
| Tempo para nova feature | 1-2 semanas | 2-3 meses |
| Bugs em produção | 1-2/mês | 5-10/mês |
| Tempo de correção | Horas | Dias/Semanas |
| Onboarding de dev | 1-2 semanas | 2-3 meses |
| Custo de manutenção | Baixo | Alto (60-80% do budget) |

---

## 6. Exercício de Reflexão

### 6.1 Identifique Legados no Seu Trabalho

Pense em sistemas que você conhece:

1. **Qual é o sistema mais antigo** que você já trabalhou?
2. **Quantos dos sinais** da checklist ele apresentava?
3. **O que aconteceria** se precisasse fazer uma mudança grande?
4. **Existem testes automatizados** para esse sistema?

### 6.2 Auto-Avaliação

```text
Responda mentalmente:

1. Você já teve medo de alterar um código por não 
   saber o que poderia quebrar?
   
2. Você já ouviu "só fulano sabe como isso funciona"?

3. Você já encontrou código sem comentários ou 
   documentação explicando o porquê?

4. Você já viu um sistema "funcionando por milagre"?

Se respondeu SIM para qualquer uma: você já trabalhou
com sistemas legados!
```

---

## 7. Resumo

### 7.1 Pontos-Chave

| Conceito | Definição |
|----------|-----------|
| **Sistema Legado** | Software antigo ainda em uso, difícil de modificar |
| **Dívida Técnica** | Custo acumulado de atalhos e decisões passadas |
| **Conhecimento Tribal** | Informação que só existe na cabeça de algumas pessoas |
| **Código Espaguete** | Código confuso, sem estrutura clara |

### 7.2 O Que Vem a Seguir?

No próximo módulo, vamos explorar os **desafios específicos de testar sistemas legados** e por que as abordagens tradicionais de QA frequentemente falham.

---

## 📚 Referências

- Feathers, Michael. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- Fowler, Martin. *Refactoring: Improving the Design of Existing Code*. Addison-Wesley, 2018.

---

**Próximo**: [02-desafios-de-testar-legados.md](02-desafios-de-testar-legados.md)
