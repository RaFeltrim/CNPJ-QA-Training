# 📋 Planejamento de Aprendizado: Shift Left Testing

> Roadmap completo de 6 semanas para dominar Shift Left Testing

---

## 🎯 Visão Geral do Plano

Este plano de aprendizado foi desenhado para levar você do **zero ao domínio** em Shift Left Testing. Cada semana tem objetivos claros, leituras obrigatórias e exercícios práticos.

### Estrutura Geral

| Semana | Tema | Nível | Carga Horária |
|--------|------|-------|---------------|
| 1 | Conceitos Fundamentais | Junior | 6-8h |
| 2 | Como Funciona na Prática | Junior/Mid | 6-8h |
| 3 | Implementação Passo a Passo | Mid | 8-10h |
| 4 | Boas Práticas e Padrões | Mid | 6-8h |
| 5 | Exercícios Práticos | Mid/Senior | 8-10h |
| 6 | Projeto Integrador | Senior | 10-12h |

**Total**: 44-56 horas de estudo

---

## 📅 Semana 1: Conceitos Fundamentais

### Objetivo
Entender o que é Shift Left Testing, por que existe e quais são seus benefícios.

### O Que Você Vai Aprender
- Definição clara de Shift Left Testing
- Contexto histórico: como chegamos aqui
- Diferenças entre testes tradicionais e Shift Left
- Benefícios mensuráveis da abordagem

### Leituras Obrigatórias
1. [`02-guia-teorico/01-introducao.md`](../02-guia-teorico/01-introducao.md)
2. [`02-guia-teorico/02-fundamentacao-teorica.md`](../02-guia-teorico/02-fundamentacao-teorica.md) (Seções 1-3)

### Atividades Práticas
- [ ] Leia os materiais obrigatórios
- [ ] Faça anotações dos conceitos-chave
- [ ] Responda o quiz de autoavaliação (final da seção)
- [ ] Identifique no seu contexto atual onde testes acontecem "tarde demais"

### Autoavaliação - Semana 1
Responda mentalmente:
1. O que significa "Shift Left" literalmente?
2. Por que descobrir defeitos cedo é mais barato?
3. Qual a principal diferença cultural entre testes tradicionais e Shift Left?
4. Cite 3 benefícios de Shift Left Testing.

### Critérios de Sucesso
✅ Consegue explicar Shift Left em 2 minutos para um colega  
✅ Entende a diferença entre "testar no fim" vs "testar desde o início"  
✅ Reconhece situações onde Shift Left traria valor  

---

## 📅 Semana 2: Como Funciona na Prática

### Objetivo
Compreender a arquitetura, o fluxo e os processos de Shift Left em um ciclo de desenvolvimento.

### O Que Você Vai Aprender
- Fluxo de testes em cada fase do desenvolvimento
- Papéis e responsabilidades (Dev, QA, PM, DevOps)
- Pirâmide de testes e sua importância
- Integração com CI/CD
- Como QA atua desde o refinamento

### Leituras Obrigatórias
1. [`02-guia-teorico/02-fundamentacao-teorica.md`](../02-guia-teorico/02-fundamentacao-teorica.md) (Seções 4-6)
2. [`02-guia-teorico/03-como-funciona.md`](../02-guia-teorico/03-como-funciona.md)

### Atividades Práticas
- [ ] Desenhe o fluxo atual do seu projeto/empresa
- [ ] Identifique onde QA entra no processo
- [ ] Compare com o fluxo ideal de Shift Left
- [ ] Liste 3 mudanças que poderiam ser feitas

### Autoavaliação - Semana 2
Responda mentalmente:
1. Em qual fase do desenvolvimento um QA deve começar a atuar em Shift Left?
2. O que é a "Pirâmide de Testes"? Desenhe-a.
3. Qual o papel do Dev em Shift Left?
4. Como CI/CD se relaciona com Shift Left?

### Critérios de Sucesso
✅ Consegue desenhar um fluxo de Shift Left  
✅ Entende a pirâmide de testes e suas camadas  
✅ Sabe qual é a responsabilidade de cada papel  
✅ Compreende o papel do CI/CD no processo  

---

## 📅 Semana 3: Implementação Passo a Passo

### Objetivo
Aprender como implementar Shift Left Testing em um projeto real, do zero.

### O Que Você Vai Aprender
- Como avaliar o estado atual de um projeto
- Passos para começar a implementação
- Escolha de ferramentas adequadas
- Como treinar a equipe
- Estratégias de adoção incremental

### Leituras Obrigatórias
1. [`02-guia-teorico/04-como-aplicar.md`](../02-guia-teorico/04-como-aplicar.md) (Seções 1-5)
2. [`05-exemplos-pratica/exemplo-01-unit-tests.md`](../05-exemplos-pratica/exemplo-01-unit-tests.md)

### Atividades Práticas
- [ ] Analise o projeto CNPJ-QA-Training
- [ ] Identifique os tipos de testes existentes
- [ ] Execute a suite de testes: `pytest tests/ -v`
- [ ] Leia e entenda 3 testes unitários do projeto

### Exercício Prático
```bash
# Clone e configure o projeto
git clone https://github.com/RaFeltrim/CNPJ-QA-Training.git
cd CNPJ-QA-Training
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt

# Execute os testes
pytest tests/ -v

# Veja a cobertura
pytest tests/ --cov=src --cov-report=html
```

### Autoavaliação - Semana 3
Responda mentalmente:
1. Qual o primeiro passo para implementar Shift Left?
2. Por que começar com um projeto piloto?
3. Quais ferramentas são essenciais para começar?
4. Como medir se a implementação está funcionando?

### Critérios de Sucesso
✅ Consegue executar testes do projeto de exemplo  
✅ Entende a estrutura de testes unitários  
✅ Sabe os passos para iniciar em um projeto novo  
✅ Conhece as ferramentas básicas necessárias  

---

## 📅 Semana 4: Boas Práticas e Padrões

### Objetivo
Aprender as melhores práticas, padrões de mercado e como evitar erros comuns.

### O Que Você Vai Aprender
- 10+ boas práticas de Shift Left
- Padrões de escrita de testes
- Integração com metodologias ágeis
- Métricas de qualidade relevantes
- Armadilhas comuns e como evitá-las

### Leituras Obrigatórias
1. [`02-guia-teorico/04-como-aplicar.md`](../02-guia-teorico/04-como-aplicar.md) (Seções 6-8)
2. [`02-guia-teorico/05-lembrar-sempre.md`](../02-guia-teorico/05-lembrar-sempre.md)
3. [`05-exemplos-pratica/exemplo-03-ci-cd.md`](../05-exemplos-pratica/exemplo-03-ci-cd.md)

### Atividades Práticas
- [ ] Analise o pipeline CI/CD do projeto: `.github/workflows/ci-cd.yml`
- [ ] Identifique quais fases de Shift Left estão implementadas
- [ ] Liste 5 boas práticas que você observa no projeto
- [ ] Identifique 2 melhorias potenciais

### Autoavaliação - Semana 4
Responda mentalmente:
1. Cite 5 boas práticas de Shift Left Testing
2. Qual a armadilha mais comum na implementação?
3. Quais métricas indicam sucesso de Shift Left?
4. Por que "cobertura de código" sozinha não é suficiente?

### Critérios de Sucesso
✅ Conhece pelo menos 10 boas práticas  
✅ Sabe identificar armadilhas comuns  
✅ Entende quais métricas acompanhar  
✅ Consegue analisar um pipeline CI/CD  

---

## 📅 Semana 5: Exercícios Práticos

### Objetivo
Aplicar todo o conhecimento adquirido em exercícios progressivos.

### O Que Você Vai Fazer
- Resolver exercícios do nível básico ao avançado
- Praticar escrita de testes
- Analisar e melhorar código existente
- Aplicar conceitos em cenários realistas

### Materiais
1. [`03-exercicios/00-introducao-metodologia.md`](../03-exercicios/00-introducao-metodologia.md)
2. [`03-exercicios/01-nivel-basico.md`](../03-exercicios/01-nivel-basico.md)
3. [`03-exercicios/02-nivel-intermediario.md`](../03-exercicios/02-nivel-intermediario.md)
4. [`04-gabarito/`](../04-gabarito/) (consultar após tentar)

### Cronograma da Semana
| Dia | Atividade |
|-----|-----------|
| 1-2 | Exercícios nível básico (1-3) |
| 3-4 | Exercícios nível intermediário (4-6) |
| 5 | Revisão e consolidação |

### Dicas para os Exercícios
- Tente resolver ANTES de olhar o gabarito
- Anote suas dúvidas
- Compare sua solução com a do gabarito
- Entenda POR QUE a solução funciona

### Critérios de Sucesso
✅ Completou exercícios 1-3 sem olhar gabarito  
✅ Completou exercícios 4-6 com poucas consultas  
✅ Entendeu os conceitos aplicados em cada exercício  
✅ Consegue explicar suas soluções  

---

## 📅 Semana 6: Projeto Integrador

### Objetivo
Demonstrar maestria aplicando todos os conceitos em um projeto completo.

### O Projeto
Você vai implementar Shift Left Testing completo em uma nova funcionalidade do validador de CNPJ.

### Fases do Projeto

#### Fase 1: Análise e Planejamento (2h)
- Entender a funcionalidade a ser desenvolvida
- Identificar riscos e cenários de teste
- Criar critérios de aceitação testáveis

#### Fase 2: Design de Testes (2h)
- Definir estratégia de testes
- Planejar pirâmide de testes
- Especificar casos de teste

#### Fase 3: Implementação (4h)
- Criar testes unitários (TDD)
- Criar testes de integração
- Implementar a funcionalidade

#### Fase 4: Integração CI/CD (2h)
- Adicionar testes ao pipeline
- Configurar métricas de qualidade
- Validar execução automatizada

#### Fase 5: Documentação e Apresentação (2h)
- Documentar decisões
- Preparar apresentação dos resultados
- Refletir sobre o processo

### Materiais de Apoio
1. [`03-exercicios/03-nivel-avancado.md`](../03-exercicios/03-nivel-avancado.md)
2. [`04-gabarito/03-nivel-avancado.md`](../04-gabarito/03-nivel-avancado.md)
3. [`05-exemplos-pratica/exemplo-04-automacao.md`](../05-exemplos-pratica/exemplo-04-automacao.md)

### Critérios de Sucesso
✅ Projeto completo implementado  
✅ Testes passando no pipeline  
✅ Cobertura adequada em código crítico  
✅ Documentação clara das decisões  
✅ Consegue apresentar e defender suas escolhas  

---

## 📊 Progressão de Dificuldade

```
Semana 1-2: FUNDAMENTOS
├── Leitura e compreensão
├── Conceitos teóricos
└── Autoavaliação
        │
        ▼
Semana 3-4: APLICAÇÃO
├── Exemplos práticos
├── Análise de código real
└── Exercícios guiados
        │
        ▼
Semana 5: PRÁTICA
├── Exercícios progressivos
├── Menos suporte
└── Resolução autônoma
        │
        ▼
Semana 6: MAESTRIA
├── Projeto completo
├── Integração de conceitos
└── Demonstração de competência
```

---

## 🎓 Certificação de Conhecimento

Ao completar este plano, você deve ser capaz de:

### Nível Conceitual
- [ ] Explicar Shift Left Testing para qualquer audiência
- [ ] Comparar com abordagens tradicionais
- [ ] Argumentar benefícios com dados

### Nível Prático
- [ ] Escrever testes unitários e de integração
- [ ] Configurar pipeline CI/CD com testes
- [ ] Analisar e melhorar cobertura de testes

### Nível Estratégico
- [ ] Planejar implementação de Shift Left em um projeto
- [ ] Definir métricas de sucesso
- [ ] Liderar adoção em uma equipe

---

## 💡 Dicas Gerais de Estudo

### Antes de Começar
1. Reserve um horário fixo para estudar
2. Prepare seu ambiente de desenvolvimento
3. Tenha o projeto CNPJ-QA-Training clonado e funcionando

### Durante o Estudo
1. Faça anotações - escrever ajuda a fixar
2. Teste os exemplos - não apenas leia
3. Pergunte-se "por quê?" constantemente
4. Conecte com sua experiência real

### Após Cada Semana
1. Revise suas anotações
2. Identifique pontos que ficaram confusos
3. Releia materiais se necessário
4. Aplique algo no seu trabalho real

---

## ❓ FAQ - Perguntas Frequentes

### Posso fazer em menos tempo?
Sim, profissionais com experiência podem acelerar. Ajuste o ritmo ao seu nível.

### E se eu travar em algum exercício?
Consulte o gabarito parcialmente, entenda a direção, e tente novamente.

### Preciso fazer na ordem?
Recomendamos seguir a ordem, mas você pode pular seções que já domina.

### Como sei se estou pronto para avançar?
Use os critérios de sucesso de cada semana como guia.

---

## 🔗 Recursos Adicionais

### Leituras Complementares
- Google Testing Blog
- Martin Fowler - Testing Strategies
- ISTQB Syllabus

### Ferramentas para Praticar
- pytest (Python)
- Jest (JavaScript)
- JUnit (Java)

### Comunidades
- Stack Overflow - tag: shift-left
- Reddit - r/QualityAssurance
- LinkedIn - grupos de QA

---

**Próximo passo**: [Estrutura Pedagógica](estrutura-pedagogica.md) →
