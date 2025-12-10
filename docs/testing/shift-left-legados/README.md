# 🏛️ Shift Left Testing em Sistemas Legados

> **Material Completo de Aprendizado**: Como aplicar práticas modernas de qualidade
> em sistemas antigos, com foco na migração para CNPJ Alfanumérico 2026.

---

## 📌 O Que É Este Material?

Este é um **curso prático e progressivo** sobre como aplicar **Shift Left Testing em Sistemas Legados** - um dos maiores desafios do QA moderno.

Sistemas legados são aplicações antigas, frequentemente críticas para o negócio, que precisam ser atualizadas para suportar novas funcionalidades (como o CNPJ alfanumérico) sem quebrar o que já funciona.

### 🎯 Por Que Este Material Existe?

```
┌─────────────────────────────────────────────────────────────────┐
│  "Sistemas legados ⚠️ Requerem atualização"                     │
│                                                                  │
│  Esta frase do guia de CNPJ Alfanumérico 2026 representa um     │
│  dos maiores desafios que QAs enfrentam na vida real:           │
│                                                                  │
│  → Como testar mudanças em sistemas que têm 10+ anos?           │
│  → Como garantir que nada quebra ao adicionar nova feature?     │
│  → Como criar testes quando não existem testes?                 │
│  → Como migrar dados e validações sem downtime?                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🎯 Cenário Real: Migração CNPJ Alfanumérico

Em **julho de 2026**, todos os sistemas brasileiros precisam suportar CNPJs alfanuméricos:

| Antes (Legado) | Depois (Atualizado) |
|----------------|---------------------|
| `11.222.333/0001-81` | `AB.CDE.123/0001-45` |
| Campo: `CHAR(14)` | Campo: `VARCHAR(14)` |
| Regex: `[0-9]{14}` | Regex: `[A-Z0-9]{8}[0-9]{6}` |
| Validação: apenas números | Validação: alfanumérico |

**Este material ensina como testar essa migração com segurança.**

---

## 🗺️ Estrutura do Material

```
shift-left-legados/
│
├── README.md                          ← Você está aqui!
│
├── 01-fundamentos/                    # 📚 Base Teórica
│   ├── 01-o-que-sao-sistemas-legados.md
│   ├── 02-desafios-de-testar-legados.md
│   ├── 03-shift-left-em-contexto-legado.md
│   └── 04-estrategias-de-migracao.md
│
├── 02-tecnicas/                       # 🛠️ Técnicas Práticas
│   ├── 01-caracterization-tests.md   # Testes de caracterização
│   ├── 02-golden-master-testing.md   # Teste do mestre dourado
│   ├── 03-strangler-fig-pattern.md   # Padrão estrangulador
│   ├── 04-feature-flags.md           # Flags de funcionalidade
│   └── 05-testes-de-regressao.md     # Regressão em legados
│
├── 03-exercicios/                     # 🎯 Prática Guiada
│   ├── 01-nivel-basico.md            # Identificar e documentar
│   ├── 02-nivel-intermediario.md     # Criar testes de caracterização
│   └── 03-nivel-avancado.md          # Migração completa
│
├── 04-gabarito/                       # 🔑 Respostas
│   ├── 01-nivel-basico.md
│   ├── 02-nivel-intermediario.md
│   └── 03-nivel-avancado.md
│
└── 05-caso-pratico-cnpj/              # 💼 Caso Real
    ├── cenario-migracao.md           # Contexto do problema
    ├── plano-de-testes.md            # Estratégia completa
    ├── implementacao-testes.md       # Código dos testes
    └── checklist-go-live.md          # Lista de verificação
```

---

## 🎓 Para Quem É Este Material?

| Perfil | Foco Principal | Tempo Estimado |
|--------|----------------|----------------|
| 🟢 **Junior** | Entender conceitos e identificar legados | 3-4 semanas |
| 🟡 **Mid-Level** | Criar testes de caracterização e regressão | 2-3 semanas |
| 🔴 **Senior** | Estratégias de migração e liderança técnica | 1-2 semanas |

---

## 📋 Roteiro de Estudos

### Semana 1-2: Fundamentos

```
Dia 1-2: O que são sistemas legados
Dia 3-4: Desafios específicos de teste
Dia 5-7: Shift Left adaptado para legados
```

### Semana 3-4: Técnicas

```
Dia 1-2: Characterization Tests
Dia 3-4: Golden Master Testing
Dia 5-6: Strangler Fig Pattern
Dia 7: Feature Flags
```

### Semana 5-6: Prática

```
Dia 1-3: Exercícios básicos
Dia 4-6: Exercícios intermediários
Dia 7-10: Caso prático CNPJ
```

---

## 🔗 Pré-requisitos

Antes de iniciar, certifique-se de ter completado:

1. ✅ [Guia de Shift Left Testing](../shift-left-testing/README.md)
2. ✅ [Guia Completo CNPJ](../../guides/guia-completo-cnpj.md)
3. ✅ [CNPJ Alfanumérico 2026](../../guides/cnpj-alfanumerico-2026.md)

---

## 🚀 Comece Agora!

**Próximo passo**: [01-fundamentos/01-o-que-sao-sistemas-legados.md](01-fundamentos/01-o-que-sao-sistemas-legados.md)
