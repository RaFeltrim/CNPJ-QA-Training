# 🚀 Shift Left Testing: Material Completo de Aprendizado

> Um guia pedagógico estruturado do **Junior ao Senior** sobre Shift Left Testing,
> com exemplos práticos usando o validador de CNPJ.

---

## 📌 O Que É Este Material?

Este é um **curso completo e progressivo** sobre **Shift Left Testing**, uma abordagem moderna de qualidade de software onde testes e atividades de QA são trazidos o mais cedo possível no ciclo de desenvolvimento.

### 🎯 Diferencial

- **Sem suposições de conhecimento prévio** - Tudo é explicado do zero
- **Exemplos práticos reais** - Usando o próprio código do validador de CNPJ
- **Progressão pedagógica** - Do básico ao avançado com scaffolding
- **Exercícios com gabarito** - Prática guiada com respostas comentadas

---

## 🗺️ Como Navegar Este Material

### 🟢 Para Iniciantes (QAs Junior)

**Tempo estimado**: 4-6 semanas (1-2h por dia)

1. **Entenda a estrutura** → [`01-planejamento/estrutura-pedagogica.md`](01-planejamento/estrutura-pedagogica.md)
2. **Aprenda os conceitos** → [`02-guia-teorico/`](02-guia-teorico/index.md) (comece por `01-introducao.md`)
3. **Pratique com ajuda** → [`03-exercicios/01-nivel-basico.md`](03-exercicios/01-nivel-basico.md)
4. **Valide seu aprendizado** → [`04-gabarito/01-nivel-basico.md`](04-gabarito/01-nivel-basico.md)
5. **Veja na prática** → [`05-exemplos-pratica/`](05-exemplos-pratica/)

### 🟡 Para Profissionais Mid-Level

**Tempo estimado**: 2-3 semanas

1. **Revise conceitos-chave** → [`02-guia-teorico/04-como-aplicar.md`](02-guia-teorico/04-como-aplicar.md)
2. **Desafie-se** → [`03-exercicios/02-nivel-intermediario.md`](03-exercicios/02-nivel-intermediario.md)
3. **Implemente** → Crie testes em seu próprio projeto
4. **Compare** → [`04-gabarito/02-nivel-intermediario.md`](04-gabarito/02-nivel-intermediario.md)

### 🔴 Para Seniores

**Tempo estimado**: 1 semana

1. **Checklist estratégico** → [`02-guia-teorico/05-lembrar-sempre.md`](02-guia-teorico/05-lembrar-sempre.md)
2. **Desafios complexos** → [`03-exercicios/03-nivel-avancado.md`](03-exercicios/03-nivel-avancado.md)
3. **Projetos integradores** → Aplicar em escala organizacional

---

## 📚 Estrutura Completa do Material

```
shift-left-testing/
│
├── README.md                          ← Você está aqui!
│
├── 01-planejamento/                   # 📋 Planejamento de Estudo
│   ├── plano-aprendizado.md          # Roadmap completo de 6 semanas
│   └── estrutura-pedagogica.md       # Como o material está organizado
│
├── 02-guia-teorico/                   # 📖 Fundamentos Teóricos
│   ├── index.md                      # Índice do guia
│   ├── 01-introducao.md              # O que é Shift Left Testing
│   ├── 02-fundamentacao-teorica.md   # Princípios, história, conceitos
│   ├── 03-como-funciona.md           # Arquitetura, fluxo, processos
│   ├── 04-como-aplicar.md            # Implementação passo a passo
│   └── 05-lembrar-sempre.md          # Checklist e armadilhas
│
├── 03-exercicios/                     # 🎯 Exercícios Práticos
│   ├── index.md                      # Índice dos exercícios
│   ├── 00-introducao-metodologia.md  # Explicação do scaffolding
│   ├── 01-nivel-basico.md            # Exercícios 1-3 (muito guiados)
│   ├── 02-nivel-intermediario.md     # Exercícios 4-6 (pouco guiados)
│   └── 03-nivel-avancado.md          # Exercícios 7-10 (desafios)
│
├── 04-gabarito/                       # 🔑 Respostas Comentadas
│   ├── index.md                      # Índice do gabarito
│   ├── 01-nivel-basico.md            # Gabarito exercícios 1-3
│   ├── 02-nivel-intermediario.md     # Gabarito exercícios 4-6
│   └── 03-nivel-avancado.md          # Gabarito exercícios 7-10
│
├── 05-exemplos-pratica/               # 💻 Código Real
│   ├── exemplo-01-unit-tests.md      # Implementando testes unitários
│   ├── exemplo-02-integration.md     # Testes de integração com API
│   ├── exemplo-03-ci-cd.md           # Integração em pipeline CI/CD
│   └── exemplo-04-automacao.md       # Automação completa
│
└── assets/                            # 🖼️ Recursos
    └── diagramas/                    # Diagramas e imagens
```

---

## 🎯 O Que Você Aprenderá

| Módulo | Conceitos | Nível |
|--------|-----------|-------|
| Introdução | O que é, por que existe, benefícios | 🟢 Junior |
| Fundamentação | Princípios, história, comparações | 🟢 Junior |
| Como Funciona | Arquitetura, fluxo, papéis | 🟡 Mid |
| Como Aplicar | Implementação, boas práticas, ferramentas | 🟡 Mid |
| Checklist | Armadilhas, sustentabilidade | 🔴 Senior |

### Ao Final Você Será Capaz De:

✅ Explicar o que é Shift Left Testing e por que importa  
✅ Identificar diferenças entre testes tradicionais vs. Shift Left  
✅ Projetar uma arquitetura de testes com pirâmide adequada  
✅ Implementar testes unitários e de integração desde o início  
✅ Integrar testes em pipelines CI/CD  
✅ Definir métricas de qualidade relevantes  
✅ Evitar armadilhas comuns na implementação  
✅ Liderar iniciativas de Shift Left em equipes  

---

## 🛠️ Ferramentas Usadas nos Exemplos

| Categoria | Ferramenta | Uso |
|-----------|------------|-----|
| Linguagem | Python 3.8+ | Código do projeto |
| Testes | pytest | Framework de testes |
| CI/CD | GitHub Actions | Pipeline automatizado |
| Cobertura | pytest-cov | Métricas de cobertura |
| Linting | flake8, pylint | Análise estática |
| Segurança | bandit, safety | Shift Left Security |

---

## 💡 Metodologia de Aprendizado

Este material usa **scaffolding pedagógico**:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  NÍVEL 1: EXEMPLO RESOLVIDO                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Solução completa passo a passo                      │   │
│  │ Todas as explicações detalhadas                     │   │
│  │ "Observe e aprenda"                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                  │
│  NÍVEL 2: PRÁTICA GUIADA                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Dicas e direcionamento                              │   │
│  │ Estrutura parcial fornecida                         │   │
│  │ "Tente com ajuda"                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                  │
│  NÍVEL 3: PRÁTICA SEMI-GUIADA                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Apenas contexto e poucas dicas                      │   │
│  │ "Tente sozinho, com pequena ajuda"                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                  │
│  NÍVEL 4: PRÁTICA INDEPENDENTE                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Apenas o problema - você resolve                    │   │
│  │ "Demonstre sua maestria"                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## ⏱️ Tempo Estimado por Seção

| Seção | Junior | Mid | Senior |
|-------|--------|-----|--------|
| Planejamento | 1h | 30min | 15min |
| Guia Teórico | 10-15h | 5-8h | 2-3h |
| Exercícios | 15-20h | 8-10h | 3-5h |
| Exemplos Práticos | 8-10h | 4-5h | 2h |
| **Total** | **34-46h** | **17-24h** | **7-10h** |

---

## 📋 Pré-requisitos

### Conhecimento Necessário

- **Básico**: Lógica de programação, conceitos de teste
- **Intermediário**: Python básico, Git básico
- **Avançado**: CI/CD conceitual (não precisa dominar)

### Ferramentas Necessárias

- Python 3.8 ou superior
- Git
- Editor de código (VS Code recomendado)
- Terminal/Linha de comando

### Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/RaFeltrim/CNPJ-QA-Training.git
cd CNPJ-QA-Training

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Execute os testes para verificar
pytest tests/ -v
```

---

## 🤝 Como Usar Este Material

### Estudo Individual

1. Reserve tempo diário (recomendado: 1-2h)
2. Siga a ordem dos módulos
3. Não pule exercícios - a prática é essencial
4. Use o gabarito apenas após tentar resolver
5. Anote dúvidas para pesquisar depois

### Estudo em Grupo

1. Divida o grupo por níveis de experiência
2. Discuta os conceitos teóricos em conjunto
3. Resolva exercícios individualmente, compare depois
4. Faça pair programming nos exemplos práticos

### Treinamento Corporativo

1. Use o plano de 6 semanas como base
2. Adapte exercícios ao contexto da empresa
3. Inclua código real dos projetos da equipe
4. Promova workshops com os exemplos práticos

---

## 📊 Métricas de Sucesso

### Como Saber Se Você Aprendeu?

✅ **Nível 1**: Consegue explicar Shift Left para um colega  
✅ **Nível 2**: Consegue identificar melhorias de Shift Left em um projeto  
✅ **Nível 3**: Consegue implementar testes unitários e de integração  
✅ **Nível 4**: Consegue configurar pipeline CI/CD com testes  
✅ **Nível 5**: Consegue liderar implementação de Shift Left em equipe  

---

## 🔄 Atualizações e Contribuições

### Versão Atual

- **Versão**: 1.0
- **Última atualização**: Dezembro 2025
- **Mantido por**: Rafael Feltrim

### Contribuindo

Se encontrar erros, sugerir melhorias, ou adicionar exemplos:

1. Abra uma [issue](https://github.com/RaFeltrim/CNPJ-QA-Training/issues)
2. Crie um [Pull Request](https://github.com/RaFeltrim/CNPJ-QA-Training/pulls)
3. Marque como `documentation`

---

## 📞 Suporte

- **Dúvidas**: Abra uma issue no repositório
- **Sugestões**: Pull requests são bem-vindos
- **Feedback**: Nos ajude a melhorar este material!

---

<div align="center">

**🎓 Bom aprendizado! 🎓**

*"A qualidade não é um ato, é um hábito." - Aristóteles*

</div>
