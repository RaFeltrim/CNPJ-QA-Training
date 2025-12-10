# Exercícios Nível Avançado 🔴

> Exercícios 7-10: Independentes, para demonstrar maestria

---

## Exercício 7: Estratégia de Testes para Projeto Novo

### 🎯 Tipo: INDEPENDENTE

---

### Contexto

Você foi designado como QA Lead para um novo projeto: um **microsserviço de validação de documentos** que validará não apenas CNPJ, mas também CPF, RG, CNH e passaporte.

O projeto está na fase de planejamento e você precisa definir a estratégia completa de testes seguindo princípios de Shift Left.

---

### Cenário

**Requisitos do projeto**:
- API REST com endpoints para cada tipo de documento
- Integração com APIs governamentais para validação online
- Banco de dados para cache de consultas
- Autenticação via OAuth 2.0
- SLA de resposta: 200ms para validação offline, 2s para online
- Disponibilidade: 99.9%

**Stack planejada**:
- Python/FastAPI
- PostgreSQL
- Redis (cache)
- Docker/Kubernetes
- GitHub Actions

**Time**:
- 3 desenvolvedores
- 1 QA (você)
- 1 DevOps
- 1 Product Owner

---

### Sua Tarefa

Elabore um documento de **Estratégia de Testes** completo contendo:

1. **Visão geral da estratégia**
2. **Tipos de teste e proporção** (pirâmide)
3. **Ferramentas selecionadas** (com justificativa)
4. **Processo de QA no ciclo de desenvolvimento**
5. **Métricas de qualidade** a acompanhar
6. **Riscos e mitigações**
7. **Cronograma de implementação**

---

### ✅ Critérios de Sucesso

- [ ] Documento completo com todas as 7 seções
- [ ] Estratégia alinhada com princípios de Shift Left
- [ ] Proporção de testes justificada
- [ ] Ferramentas adequadas à stack
- [ ] Métricas mensuráveis e relevantes
- [ ] Riscos realistas com mitigações práticas

---

### 📝 Espaço para Sua Resposta

```markdown
# Estratégia de Testes - Microsserviço de Validação de Documentos

## 1. Visão Geral


## 2. Tipos de Teste e Proporção


## 3. Ferramentas Selecionadas


## 4. Processo de QA no Ciclo de Desenvolvimento


## 5. Métricas de Qualidade


## 6. Riscos e Mitigações


## 7. Cronograma de Implementação


```

---

**Quando terminar**, compare com o [Gabarito - Exercício 7](../04-gabarito/03-nivel-avancado.md#exercício-7-estratégia-de-testes-para-projeto-novo).

---

## Exercício 8: Shift Left Security

### 🎯 Tipo: INDEPENDENTE

---

### Contexto

A equipe de segurança identificou que o projeto CNPJ-QA-Training precisa melhorar suas práticas de segurança. Você foi encarregado de implementar **Shift Left Security** no projeto.

---

### Cenário

**Problemas identificados**:
1. Não há verificação de vulnerabilidades em dependências
2. Não há análise estática de segurança (SAST)
3. Segredos (API keys) já foram commitados no passado
4. Não há validação de input sanitization
5. Logs podem expor dados sensíveis

**Requisitos**:
- Integrar verificações de segurança no pipeline
- Não aumentar tempo de pipeline em mais de 5 minutos
- Gerar relatórios de vulnerabilidades
- Bloquear PRs com vulnerabilidades críticas

---

### Sua Tarefa

1. Projetar a integração de segurança no pipeline CI/CD
2. Selecionar e configurar ferramentas de segurança
3. Definir políticas de bloqueio (o que bloqueia PR?)
4. Criar testes de segurança específicos para o projeto
5. Documentar processo de resposta a vulnerabilidades

---

### ✅ Critérios de Sucesso

- [ ] Pipeline modificado com estágios de segurança
- [ ] Ferramentas de SAST e dependency check configuradas
- [ ] Políticas de bloqueio definidas
- [ ] Pelo menos 3 testes de segurança escritos
- [ ] Processo de resposta documentado

---

### 📝 Espaço para Sua Resposta

**Pipeline de Segurança (YAML)**:

```yaml
# Adicione os jobs de segurança

```

**Ferramentas Selecionadas**:

| Ferramenta | Propósito | Configuração |
|------------|-----------|--------------|
| | | |

**Políticas de Bloqueio**:

```
BLOQUEIA PR quando:
- 
- 
- 

NÃO BLOQUEIA (apenas alerta) quando:
- 
- 
```

**Testes de Segurança**:

```python
# tests/test_security.py



```

**Processo de Resposta a Vulnerabilidades**:

```
1. Vulnerabilidade identificada
   ↓
2. 
   ↓
3. 
   ↓
4. 
```

---

**Quando terminar**, compare com o [Gabarito - Exercício 8](../04-gabarito/03-nivel-avancado.md#exercício-8-shift-left-security).

---

## Exercício 9: Métricas e Dashboard de Qualidade

### 🎯 Tipo: INDEPENDENTE

---

### Contexto

A liderança quer visibilidade sobre a qualidade do projeto. Você precisa definir métricas de qualidade relevantes e propor um dashboard para acompanhamento.

---

### Cenário

**Perguntas da liderança**:
- "Como está a qualidade do nosso código?"
- "Estamos melhorando ou piorando?"
- "O Shift Left está funcionando?"
- "Onde devemos investir mais esforço?"

**Dados disponíveis**:
- Histórico de bugs (Jira)
- Cobertura de código (pytest-cov)
- Resultados de pipeline (GitHub Actions)
- Tempo de builds
- PRs mergeados

---

### Sua Tarefa

1. Definir 8-10 métricas de qualidade relevantes
2. Para cada métrica: fórmula, fonte de dados, meta
3. Projetar layout do dashboard
4. Definir frequência de atualização
5. Criar alertas para métricas fora do esperado

---

### ✅ Critérios de Sucesso

- [ ] 8-10 métricas definidas com clareza
- [ ] Métricas são mensuráveis e acionáveis
- [ ] Dashboard tem layout lógico
- [ ] Alertas definidos para situações críticas
- [ ] Métricas respondem às perguntas da liderança

---

### 📝 Espaço para Sua Resposta

**Métricas Definidas**:

| # | Métrica | Fórmula | Fonte | Meta | Frequência |
|---|---------|---------|-------|------|------------|
| 1 | | | | | |
| 2 | | | | | |
| ... | | | | | |

**Layout do Dashboard**:

```
┌─────────────────────────────────────────────────────────────┐
│                     DASHBOARD DE QUALIDADE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Desenhe ou descreva o layout]                            │
│                                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Alertas Configurados**:

| Métrica | Condição de Alerta | Ação |
|---------|-------------------|------|
| | | |

---

**Quando terminar**, compare com o [Gabarito - Exercício 9](../04-gabarito/03-nivel-avancado.md#exercício-9-métricas-e-dashboard-de-qualidade).

---

## Exercício 10: Projeto Integrador

### 🎯 Tipo: PROJETO COMPLETO

---

### Contexto

Este é o exercício final. Você vai aplicar **todos os conceitos** de Shift Left Testing em um cenário realista e completo.

---

### Cenário

A empresa decidiu adicionar uma nova funcionalidade ao validador de CNPJ:

**Funcionalidade**: Validação de CNPJ de Filiais

> "Como usuário, quero validar se um CNPJ é de matriz ou filial, e listar todas as filiais de uma matriz, para gerenciar melhor meu cadastro de fornecedores."

**Requisitos funcionais**:
- Identificar se CNPJ é matriz (0001) ou filial (0002+)
- Dado um CNPJ de matriz, listar todas as filiais ativas
- Retornar dados básicos de cada filial (razão social, situação)

**Requisitos não-funcionais**:
- Tempo de resposta < 3s para listagem
- Cache de resultados por 24h
- Rate limit: 10 requisições/minuto por usuário

---

### Sua Tarefa

Implemente Shift Left Testing **completo** para esta funcionalidade:

### Fase 1: Planejamento (Shift Left no Requisito)
- Critérios de aceitação detalhados
- Cenários de teste identificados
- Riscos mapeados
- Perguntas para stakeholders

### Fase 2: Design (Shift Left na Arquitetura)
- Proposta de arquitetura testável
- Decisões de design documentadas
- Contratos de API definidos

### Fase 3: Implementação (Shift Left no Código)
- Testes unitários (TDD)
- Código da funcionalidade
- Testes de integração

### Fase 4: Pipeline (Shift Left no Deploy)
- Modificações no CI/CD
- Gates de qualidade

### Fase 5: Documentação
- Documentação da funcionalidade
- Documentação dos testes

---

### ✅ Critérios de Sucesso

- [ ] Critérios de aceitação completos (min. 8 cenários)
- [ ] Arquitetura testável documentada
- [ ] Pelo menos 10 testes unitários
- [ ] Pelo menos 3 testes de integração
- [ ] Pipeline atualizado
- [ ] Código funcionando
- [ ] Documentação completa

---

### 📝 Espaço para Sua Resposta

### Fase 1: Planejamento

**Critérios de Aceitação**:

```gherkin
Funcionalidade: Validação de CNPJ Matriz/Filial

  Cenário: 
    Dado 
    Quando 
    Então 

  # Continue...
```

**Riscos Identificados**:

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| | | | |

---

### Fase 2: Design

**Arquitetura Proposta**:

```
[Desenhe ou descreva a arquitetura]
```

**Contrato de API**:

```yaml
# OpenAPI/Swagger
paths:
  /cnpj/{cnpj}/tipo:
    get:
      # ...
  
  /cnpj/{cnpj}/filiais:
    get:
      # ...
```

---

### Fase 3: Implementação

**Testes Unitários**:

```python
# tests/test_matriz_filial.py



```

**Código da Funcionalidade**:

```python
# src/cnpj_validator/matriz_filial.py



```

**Testes de Integração**:

```python
# tests/test_matriz_filial_integration.py



```

---

### Fase 4: Pipeline

```yaml
# Modificações no CI/CD



```

---

### Fase 5: Documentação

```markdown
# Funcionalidade: Validação Matriz/Filial

## Visão Geral


## Como Usar


## Testes


```

---

**Quando terminar**, compare com o [Gabarito - Exercício 10](../04-gabarito/03-nivel-avancado.md#exercício-10-projeto-integrador).

---

## 🏆 Parabéns!

Você completou **todos os exercícios** de Shift Left Testing!

**O que você demonstrou**:
- ✅ Compreensão profunda dos conceitos
- ✅ Capacidade de aplicar em cenários reais
- ✅ Habilidade de planejar e implementar
- ✅ Visão estratégica de qualidade

---

## 🎓 Próximos Passos

1. **Revise** os gabaritos e compare com suas soluções
2. **Aplique** o que aprendeu em projetos reais
3. **Compartilhe** conhecimento com seu time
4. **Continue** aprendendo e evoluindo

---

## 📚 Recursos Finais

- [Gabarito Nível Avançado](../04-gabarito/03-nivel-avancado.md)
- [Exemplos Práticos Completos](../05-exemplos-pratica/)
- [Guia Teórico - Referência](../02-guia-teorico/)

---

**Voltar para**: [Índice dos Exercícios](index.md) | [README Principal](../README.md)
