# Exercícios Nível Intermediário 🟡

> Exercícios 4-6: Pouco guiados, para aplicação prática

---

## Exercício 4: Critérios de Aceitação Testáveis

### 🎯 Tipo: POUCO SUPORTE

---

### Contexto

O Product Owner trouxe uma nova funcionalidade para o validador de CNPJ:

> "Precisamos validar se um CNPJ está ativo na Receita Federal antes de permitir o cadastro. Se o CNPJ estiver inativo, suspenso ou baixado, o sistema deve bloquear o cadastro e mostrar uma mensagem apropriada."

Você é o QA participando do refinamento (Three Amigos). Sua tarefa é transformar esse requisito vago em **critérios de aceitação testáveis**.

---

### Cenário

**História de Usuário (incompleta)**:

```
Como um operador do sistema
Quero validar a situação cadastral do CNPJ
Para evitar cadastrar empresas inativas
```

**Informações adicionais do PO**:
- As situações possíveis são: ATIVA, BAIXADA, SUSPENSA, INAPTA, NULA
- Apenas ATIVA deve permitir cadastro
- Precisamos mostrar mensagem diferente para cada situação

---

### Sua Tarefa

1. Escrever critérios de aceitação no formato Gherkin (Dado-Quando-Então)
2. Cobrir todos os cenários possíveis (positivos e negativos)
3. Identificar edge cases e perguntas para o PO
4. Definir os dados de teste necessários

---

### 💡 Dica Estratégica

Pense em:
- O que acontece com cada situação cadastral?
- E se a API estiver fora do ar?
- E se o CNPJ não existir na base da Receita?

---

### ✅ Critérios de Sucesso

- [ ] Pelo menos 6 cenários de aceitação escritos
- [ ] Formato Gherkin correto (Dado-Quando-Então)
- [ ] Cenários cobrem sucesso E falha
- [ ] Edge cases identificados
- [ ] Pelo menos 3 perguntas para o PO

---

### 📝 Espaço para Sua Resposta

**Critérios de Aceitação**:

```gherkin
Funcionalidade: Validação de Situação Cadastral do CNPJ

  # Cenário 1
  Cenário: _______________________________________________
    Dado ________________________________________________
    Quando ______________________________________________
    Então _______________________________________________

  # Cenário 2
  Cenário: _______________________________________________
    Dado ________________________________________________
    Quando ______________________________________________
    Então _______________________________________________

  # (Continue com mais cenários...)
```

**Edge Cases Identificados**:

```
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________
```

**Perguntas para o PO**:

```
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________
```

**Dados de Teste Necessários**:

| Situação | CNPJ de Exemplo | Comportamento Esperado |
|----------|-----------------|------------------------|
| ATIVA | | |
| BAIXADA | | |
| ... | | |

---

**Quando terminar**, compare com o [Gabarito - Exercício 4](../04-gabarito/02-nivel-intermediario.md#exercício-4-critérios-de-aceitação-testáveis).

---

## Exercício 5: Pipeline CI/CD

### 🎯 Tipo: POUCO SUPORTE

---

### Contexto

Sua equipe está migrando para GitHub Actions e você foi designado para projetar o pipeline de CI/CD seguindo princípios de Shift Left.

O pipeline atual roda apenas testes no final, após o deploy em staging. Você precisa redesenhá-lo.

---

### Cenário

**Requisitos do novo pipeline**:
- Deve rodar em todo push e PR para branches main e develop
- Deve ter múltiplos estágios de verificação
- Deve falhar rápido (fast fail)
- Deve incluir testes em diferentes níveis
- Deve incluir verificação de segurança

**Stack do projeto**:
- Python 3.11
- pytest para testes
- flake8 para linting
- bandit para segurança

---

### Sua Tarefa

1. Definir os estágios do pipeline (ordem e conteúdo)
2. Escrever o arquivo YAML do GitHub Actions
3. Justificar a ordem dos estágios
4. Definir critérios de falha para cada estágio

---

### 💡 Dica Estratégica

Lembre-se: **Shift Left no pipeline** significa que verificações mais rápidas e básicas vêm primeiro. Se linting falha, por que rodar testes pesados?

---

### ✅ Critérios de Sucesso

- [ ] Pipeline com pelo menos 4 estágios distintos
- [ ] Ordem dos estágios segue princípio de fail fast
- [ ] Dependências entre jobs estão corretas
- [ ] YAML é válido e executável
- [ ] Inclui verificação de segurança

---

### 📝 Espaço para Sua Resposta

**Estágios planejados** (em ordem):

```
1. _________________ (tempo estimado: ___ min)
   - O que faz: _________________________________
   - Por que nesta posição: _____________________

2. _________________ (tempo estimado: ___ min)
   - O que faz: _________________________________
   - Por que nesta posição: _____________________

3. _________________ (tempo estimado: ___ min)
   - O que faz: _________________________________
   - Por que nesta posição: _____________________

4. _________________ (tempo estimado: ___ min)
   - O que faz: _________________________________
   - Por que nesta posição: _____________________
```

**Arquivo YAML**:

```yaml
# .github/workflows/shift-left-pipeline.yml

name: Shift Left Pipeline

# Seu código aqui...
```

---

**Quando terminar**, compare com o [Gabarito - Exercício 5](../04-gabarito/02-nivel-intermediario.md#exercício-5-pipeline-cicd).

---

## Exercício 6: Reorganizando a Pirâmide de Testes

### 🎯 Tipo: POUCO SUPORTE

---

### Contexto

Você entrou em um projeto legado que tem a seguinte distribuição de testes:

```
SITUAÇÃO ATUAL (Pirâmide Invertida)

        ████████████████████████████████████   80 testes E2E (Selenium)
        ████████████████                       30 testes de integração
        ████████                               15 testes unitários

TEMPO DE EXECUÇÃO: 45 minutos
TAXA DE FLAKINESS: 30% dos testes E2E falham aleatoriamente
```

O time está frustrado: o pipeline demora muito e os testes são instáveis.

---

### Cenário

**Exemplos de testes E2E atuais**:

```python
# test_e2e_validation.py (Selenium)

def test_validate_cnpj_via_ui():
    """Testa validação de CNPJ pela interface"""
    driver.get("http://localhost:8000/validate")
    input_field = driver.find_element(By.ID, "cnpj-input")
    input_field.send_keys("11.222.333/0001-81")
    button = driver.find_element(By.ID, "validate-button")
    button.click()
    result = driver.find_element(By.ID, "result")
    assert "Válido" in result.text

def test_validate_invalid_cnpj_via_ui():
    """Testa CNPJ inválido pela interface"""
    driver.get("http://localhost:8000/validate")
    input_field = driver.find_element(By.ID, "cnpj-input")
    input_field.send_keys("00.000.000/0000-00")
    button = driver.find_element(By.ID, "validate-button")
    button.click()
    result = driver.find_element(By.ID, "result")
    assert "Inválido" in result.text
```

**Muitos desses testes E2E estão testando lógica que poderia ser testada em níveis mais baixos.**

---

### Sua Tarefa

1. Analisar os testes E2E e identificar quais podem ser movidos
2. Propor nova distribuição da pirâmide
3. Reescrever 2 testes E2E como testes unitários ou de API
4. Definir critérios para decidir quando usar cada nível

---

### 💡 Dica Estratégica

Pergunte-se: "O que exatamente este teste E2E está validando?"
- Se é lógica de negócio → pode ser unitário
- Se é integração entre componentes → pode ser teste de API
- Se é experiência do usuário na UI → mantém como E2E

---

### ✅ Critérios de Sucesso

- [ ] Identificou pelo menos 5 testes E2E que podem ser movidos
- [ ] Propôs nova distribuição seguindo proporção 70/20/10
- [ ] Reescreveu 2 testes em níveis mais baixos
- [ ] Definiu critérios claros para cada nível
- [ ] Estimou redução no tempo de pipeline

---

### 📝 Espaço para Sua Resposta

**Análise dos testes E2E**:

| Teste E2E | O que testa realmente | Pode mover para | Justificativa |
|-----------|----------------------|-----------------|---------------|
| test_validate_cnpj_via_ui | | | |
| test_validate_invalid_cnpj_via_ui | | | |
| ... | | | |

**Nova distribuição proposta**:

```
ANTES                              DEPOIS
─────                              ──────
E2E: 80                            E2E: ___
Integração: 30                     Integração: ___
Unitário: 15                       Unitário: ___

Tempo estimado: 45 min             Tempo estimado: ___ min
```

**Teste reescrito #1**:

```python
# Antes: test_e2e_validation.py (E2E)
# Depois: test_cnpj_validator.py (_____)

# Seu código aqui...
```

**Teste reescrito #2**:

```python
# Antes: (qual teste E2E)
# Depois: (qual nível)

# Seu código aqui...
```

**Critérios de decisão**:

```
Usar UNITÁRIO quando:
- _______________________________________________
- _______________________________________________

Usar INTEGRAÇÃO quando:
- _______________________________________________
- _______________________________________________

Usar E2E quando:
- _______________________________________________
- _______________________________________________
```

---

**Quando terminar**, compare com o [Gabarito - Exercício 6](../04-gabarito/02-nivel-intermediario.md#exercício-6-reorganizando-a-pirâmide-de-testes).

---

## 🎉 Excelente Progresso!

Você completou os exercícios intermediários! Agora você está pronto para os desafios avançados.

**O que você praticou**:
- ✅ Escrever critérios de aceitação testáveis
- ✅ Projetar pipeline CI/CD com Shift Left
- ✅ Reorganizar pirâmide de testes

**Próximo passo**: [Exercícios Nível Avançado](03-nivel-avancado.md) →

---

## 📚 Recursos de Apoio

- [Guia Teórico - Como Aplicar](../02-guia-teorico/04-como-aplicar.md)
- [Exemplo Prático - CI/CD](../05-exemplos-pratica/exemplo-03-ci-cd.md)
- [Gabarito Nível Intermediário](../04-gabarito/02-nivel-intermediario.md)
