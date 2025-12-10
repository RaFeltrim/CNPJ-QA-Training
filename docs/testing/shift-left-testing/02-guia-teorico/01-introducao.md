# 1. Introdução ao Shift Left Testing

> O que é, por que importa e como começar a pensar diferente sobre qualidade

---

## 🎯 Objetivo deste Módulo

Ao final deste módulo, você será capaz de:
- Explicar o que é Shift Left Testing em linguagem simples
- Entender por que essa abordagem surgiu
- Identificar os benefícios principais
- Reconhecer situações onde Shift Left se aplica

---

## 📝 O Que É Shift Left Testing?

### A Explicação Mais Simples Possível

Imagine uma linha do tempo de um projeto de software:

```
INÍCIO ──────────────────────────────────────────────────► FIM
   │                                                        │
   │  Planejamento → Design → Código → Testes → Deploy      │
   │                                                        │
   └────────────────────────────────────────────────────────┘
```

**Testes Tradicionais**: Os testes acontecem no final, após o código estar "pronto".

**Shift Left**: "Deslocar para a esquerda" - mover os testes e atividades de qualidade para o **início** da linha do tempo.

```
INÍCIO ──────────────────────────────────────────────────► FIM
   │                                                        │
   │  Testes começam AQUI ───────────────────────────►      │
   │  desde o planejamento!                                 │
   └────────────────────────────────────────────────────────┘
```

### 💡 Definição Formal

> **Shift Left Testing** é uma abordagem de qualidade de software onde testes, feedback e atividades de QA são trazidos o mais cedo possível no ciclo de desenvolvimento.

Em vez de testar **somente no fim** (antes da entrega), a equipe começa a **prevenir e detectar problemas** já na concepção, no refinamento e no desenvolvimento inicial.

---

## ❓ Por Que "Shift Left"?

O nome vem de uma metáfora visual:

Se você imaginar as fases do desenvolvimento em uma linha horizontal (da esquerda para a direita), os testes tradicionalmente ficam **à direita** (no final).

"Shift Left" significa literalmente **mover para a esquerda** - ou seja, para o início.

```
         TRADICIONAL                          SHIFT LEFT
         
    ◄─── Esquerda    Direita ───►        ◄─── Esquerda    Direita ───►
    
    ┌────────────────────────────┐        ┌────────────────────────────┐
    │ Plan │ Dev │ Build │ TEST │        │ TEST │ Plan │ Dev │ Build  │
    └────────────────────────────┘        │ TEST │ TEST │ TEST│ TEST  │
                           ▲              └────────────────────────────┘
                           │              ▲
                    Testes aqui           │
                                   Testes em TODAS as fases
```

---

## 🤔 Por Que Isso Importa?

### O Problema do Teste Tardio

Quando testes acontecem apenas no final:

1. **Defeitos são descobertos tarde** → Código já está "pronto"
2. **Correções são caras** → Requer refazer trabalho
3. **Prazos são comprometidos** → "Descobrimos bugs na véspera"
4. **Conflitos surgem** → Dev "termina", QA "bloqueia"
5. **Qualidade é sacrificada** → "Não dá tempo de testar tudo"

### 💡 A Ideia Central

> **Quanto mais cedo um defeito é encontrado, mais barato e rápido ele é de corrigir.**

Esta não é apenas intuição - é um fato comprovado por décadas de pesquisa em engenharia de software.

### O Custo de Correção por Fase

```
                        CUSTO RELATIVO DE CORREÇÃO
                        
    Produção        ████████████████████████████████████████  100x
    
    Testes          ████████████████████                       40x
    
    Desenvolvimento ████████████                               15x
    
    Design          ██████                                      5x
    
    Requisitos      ██                                          1x
    
                    └────────────────────────────────────────────►
                                        Custo
```

**Traduzindo**: Corrigir um bug em produção pode custar **100 vezes mais** do que corrigi-lo durante a fase de requisitos.

---

## 📊 Benefícios do Shift Left Testing

### 1. Redução de Custos

- Defeitos encontrados cedo = correções baratas
- Menos retrabalho = mais produtividade
- Menos bugs em produção = menos suporte

### 2. Maior Qualidade

- Problemas prevenidos antes de existirem
- Código mais testável (design orientado a testes)
- Menos defeitos escapam para produção

### 3. Entregas Mais Rápidas

- Pipeline mais confiável
- Menos bloqueios de última hora
- Feedback rápido permite iterações ágeis

### 4. Melhor Colaboração

- QA envolvido desde o início
- Responsabilidade compartilhada
- Menos "jogo de culpa"

### 5. Documentação Viva

- Testes servem como especificação
- Critérios de aceitação claros
- Comportamento documentado em código

---

## 🔄 Shift Left na Prática: O Que Muda?

### Antes (Tradicional)

| Fase | Quem Faz | O Que Faz |
|------|----------|-----------|
| Requisitos | PO/PM | Define o que construir |
| Design | Dev | Projeta a solução |
| Código | Dev | Implementa |
| Testes | QA | Testa depois de "pronto" |
| Deploy | DevOps | Coloca em produção |

**Problema**: QA só entra no final, quando já é tarde para prevenir.

### Depois (Shift Left)

| Fase | Quem Faz | O Que Faz |
|------|----------|-----------|
| Requisitos | PO/PM + QA + Dev | Define O QUE e COMO testar |
| Design | Dev + QA | Projeta solução TESTÁVEL |
| Código | Dev | Escreve código COM testes |
| Validação | QA + Dev | Valida e faz testes exploratórios |
| Deploy | DevOps + QA | Deploy com testes automatizados |

**Diferença**: QA participa de TODAS as fases.

---

## 💻 Exemplo Prático: Validador de CNPJ

Vamos ver como Shift Left se aplica ao nosso projeto de validação de CNPJ.

### Cenário: Nova Funcionalidade

**Requisito**: Adicionar validação de CNPJ alfanumérico (novo formato da Receita Federal).

### Abordagem Tradicional

```
1. PO escreve história: "Como usuário, quero validar CNPJ alfanumérico"
2. Dev implementa a validação
3. Dev "termina" e passa para QA
4. QA descobre: "E se o CNPJ tiver caracteres especiais?"
5. Dev volta para corrigir
6. QA descobre: "E CNPJs com letras minúsculas?"
7. Dev volta para corrigir novamente
8. (Repete várias vezes...)
```

**Resultado**: Atraso, frustração, bugs que "escapam".

### Abordagem Shift Left

```
1. PO escreve história inicial
2. Three Amigos (PO + Dev + QA) refinam juntos:
   - QA pergunta: "Quais caracteres são válidos?"
   - QA pergunta: "Case sensitive ou não?"
   - QA pergunta: "O que acontece com CNPJ inválido?"
3. Definem critérios de aceitação TESTÁVEIS:
   ✓ CNPJ com letras maiúsculas deve ser válido
   ✓ CNPJ com letras minúsculas deve ser convertido
   ✓ Caracteres especiais (exceto . / -) devem gerar erro
4. Dev implementa COM testes unitários desde o início
5. CI/CD roda testes automaticamente
6. QA valida e faz testes exploratórios focados
```

**Resultado**: Menos surpresas, código testado, entrega confiável.

### Código Real do Projeto

Veja como os testes unitários já existem no projeto:

```python
# tests/test_alphanumeric_validator.py

class TestAlphanumericValidatorFormat:
    """Testes de validação de formato alfanumérico"""
    
    def test_validate_format_correct_pattern(self):
        """Deve validar CNPJ no formato correto: XX.XXX.XXX/XXXX-XX"""
        result = AlphanumericCNPJValidator.validate_format("11.222.333/0001-81")
        assert result['valid'] is True
        assert result['errors'] == []
    
    def test_validate_format_without_formatting(self):
        """Deve identificar CNPJ sem formatação"""
        result = AlphanumericCNPJValidator.validate_format("11222333000181")
        assert result['valid'] is False
        assert "sem formatação" in result['errors'][0].lower()
```

Estes testes foram escritos **junto com o código**, não depois. Isso é Shift Left.

---

## ❓ Perguntas para Reflexão

Antes de continuar, pense:

1. No seu projeto atual, quando os testes acontecem?
2. Quantos bugs são descobertos em produção vs. durante desenvolvimento?
3. QA participa do planejamento/refinamento?
4. Desenvolvedores escrevem testes unitários?
5. Existe pipeline de CI/CD com testes automatizados?

Se a maioria das respostas indicar que testes/QA vêm "no final", há oportunidade para Shift Left.

---

## 📋 Resumo do Módulo

| Conceito | Definição |
|----------|-----------|
| **Shift Left** | Mover testes e QA para o início do ciclo |
| **Por que importa** | Bugs encontrados cedo são mais baratos de corrigir |
| **Benefício principal** | Prevenção em vez de detecção tardia |
| **Mudança cultural** | QA participa de todas as fases |
| **Na prática** | Testes escritos junto com código, não depois |

---

## ✅ Autoavaliação

Responda para verificar seu entendimento:

1. O que significa literalmente "Shift Left"?
   <details>
   <summary>Ver resposta</summary>
   Mover para a esquerda - ou seja, trazer testes e atividades de QA para o início do ciclo de desenvolvimento.
   </details>

2. Por que descobrir defeitos cedo é mais barato?
   <details>
   <summary>Ver resposta</summary>
   Porque o código ainda não foi integrado, testado, documentado e implantado. Quanto mais avançado no ciclo, mais trabalho precisa ser refeito.
   </details>

3. Qual a principal mudança no papel do QA em Shift Left?
   <details>
   <summary>Ver resposta</summary>
   QA deixa de ser apenas "testador no final" e passa a ser parceiro desde o planejamento, ajudando a prevenir defeitos em vez de apenas detectá-los.
   </details>

---

## 🔗 Próximos Passos

Agora que você entende **o que é** Shift Left Testing, vamos aprofundar nos **fundamentos teóricos**: por que funciona, de onde veio, e quais são os princípios que sustentam essa abordagem.

**Próximo módulo**: [2. Fundamentação Teórica](02-fundamentacao-teorica.md) →

---

## 📚 Referências para Aprofundamento

- Crispin, L. & Gregory, J. (2009). Agile Testing
- Humble, J. & Farley, D. (2010). Continuous Delivery
- Kim, G. et al. (2016). The DevOps Handbook
