# Gabarito Completo - Exercícios Práticos de Shift Left Testing

> **Material de Treinamento Profissional**  
> Soluções Detalhadas com Explicações  
> Use após suas tentativas para máximo aprendizado

---

## 📋 Índice

1. [Como Usar Este Gabarito](#como-usar-este-gabarito)
2. [Bloco 1: Fundamentos - Soluções](#bloco-1-fundamentos-de-shift-left---soluções)
3. [Bloco 2: Testes Unitários - Soluções](#bloco-2-testes-unitários-e-tdd---soluções)
4. [Bloco 3: CI/CD - Soluções](#bloco-3-cicd-e-automação---soluções)
5. [Bloco 4: Práticas Avançadas - Soluções](#bloco-4-práticas-avançadas---soluções)
6. [Bloco 5: Implementação Real - Soluções](#bloco-5-implementação-em-cenários-reais---soluções)

---

## 📖 Como Usar Este Gabarito

### Princípios de Uso

1. **🚫 NÃO leia antes de tentar**: O aprendizado vem da luta com o problema
2. **✅ Compare após sua solução**: Use para validar e melhorar
3. **🤔 Entenda o "porquê"**: Não apenas copie, compreenda a lógica
4. **🔄 Tente variações**: As soluções não são únicas
5. **💬 Discuta**: Compartilhe com colegas, aprenda juntos

### Estrutura das Soluções

Cada solução contém:
- ✅ **Resposta Completa**: Código/texto da solução
- 💡 **Explicação Detalhada**: Por que essa abordagem?
- 🎯 **Pontos-Chave**: O que você deve aprender
- ⚠️ **Armadilhas Comuns**: Erros frequentes
- 🚀 **Além do Básico**: Melhorias e alternativas

---

## 📚 Bloco 1: Fundamentos de Shift Left - Soluções

### Exercício 1.1: Identificando Shift Left 🟢 (Solução Nível 1)

**Já fornecido no exercício** - Este era um exemplo guiado completo.

**Revisão dos Pontos-Chave:**

✅ **Indicadores de Shift Left:**
1. **Timing**: Testes acontecem durante desenvolvimento, não após
2. **Ownership**: Desenvolvedores são responsáveis por testes unitários
3. **Automação**: CI/CD executa testes automaticamente
4. **Feedback**: Rápido (minutos) vs lento (dias)
5. **Prevenção**: QA envolvido no planejamento

⚠️ **Armadilhas Comuns:**
- Confundir automação com Shift Left (automação no final não é Shift Left)
- Achar que Shift Left elimina QA (QA muda de papel, não desaparece)
- Focar apenas em ferramentas, ignorar cultura

---

### Exercício 1.2: Calculando ROI de Shift Left 🟡 (Solução Nível 2)

#### ✅ Resposta Completa

```
Cenário A (Tradicional):
- Requisitos: 5 × R$ 100 = R$ 500
- Desenvolvimento: 10 × R$ 1.000 = R$ 10.000
- Testes: 25 × R$ 1.500 = R$ 37.500
- Produção: 60 × R$ 10.000 = R$ 600.000
TOTAL: R$ 648.000

Cenário B (Shift Left):
- Requisitos: 30 × R$ 100 = R$ 3.000
- Desenvolvimento: 50 × R$ 1.000 = R$ 50.000
- Testes: 15 × R$ 1.500 = R$ 22.500
- Produção: 5 × R$ 10.000 = R$ 50.000
TOTAL: R$ 125.500

Economia com Shift Left: R$ 522.500
ROI percentual: 416% (ou 4,2x mais barato)
```

#### 💡 Explicação Detalhada

**Por que essa diferença dramática?**

1. **Custo Exponencial**: Bugs em produção custam 100x mais que em requisitos
2. **Distribuição de Bugs**: Shift Left encontra 80% antes da produção
3. **Efeito Cascata**: Bug em requisito evita bugs derivados depois

**Cálculo do ROI:**
```
ROI = ((Custo Evitado - Investimento) / Investimento) × 100
ROI = ((648.000 - 125.500) / 125.500) × 100
ROI = 416%
```

#### 🎯 Pontos-Chave

- Encontrar bugs cedo economiza **80-90%** do custo total
- Produção é a fase **mais cara** para correção (100x)
- Investimento em prevenção tem ROI altíssimo (400%+)

#### ⚠️ Armadilhas Comuns

❌ **Erro 1**: Achar que encontrar bugs cedo é mais caro
- Realidade: Custa mais tempo inicialmente, mas economiza muito depois

❌ **Erro 2**: Não contabilizar custo de reputação
- Bug em produção = cliente insatisfeito = perda de negócio

❌ **Erro 3**: Ignorar custo de context switch
- Corrigir bug semanas depois exige reaprender o código

---

### Exercício 1.3: Test Pyramid - Classificação 🟠 (Solução Nível 3)

#### ✅ Resposta Completa

| # | Teste | Classificação | Justificativa |
|---|-------|---------------|---------------|
| 1 | Validação de CNPJ | **Unitário** | Função pura, sem dependências |
| 2 | Login via Selenium | **E2E** | Interface gráfica, fluxo completo |
| 3 | API REST criar usuário | **Integração** | HTTP request, múltiplos componentes |
| 4 | Cálculo de desconto | **Unitário** | Função pura, lógica isolada |
| 5 | Fluxo completo de compra | **E2E** | Múltiplas telas, fim-a-fim |
| 6 | Serviço + banco de dados | **Integração** | Dois componentes interagindo |
| 7 | Formatação de data | **Unitário** | Função pura, transformação |
| 8 | Jornada do usuário | **E2E** | Múltiplos fluxos, UI completa |
| 9 | Endpoint consulta produtos | **Integração** | API + possível BD |
| 10 | Validação de email | **Unitário** | Regex, função pura |

**Resumo:**
- **Unitários**: 1, 4, 7, 10 (4 testes - 40%)
- **Integração**: 3, 6, 9 (3 testes - 30%)
- **E2E**: 2, 5, 8 (3 testes - 30%)

#### 💡 Explicação Detalhada

**Como classificar corretamente:**

**Unitário** se:
- ✅ Testa uma única função/método
- ✅ Sem dependências externas (BD, API, arquivo)
- ✅ Executa em milissegundos
- ✅ Pode usar mocks para isolar

**Integração** se:
- ✅ Testa interação entre componentes
- ✅ Usa dependências reais (BD, API)
- ✅ Executa em segundos
- ✅ Requer setup/teardown

**E2E** se:
- ✅ Testa através da interface do usuário
- ✅ Fluxo completo do sistema
- ✅ Executa em minutos
- ✅ Mais frágil (flaky)

#### 🎯 Pontos-Chave

**Distribuição Ideal (Test Pyramid):**
```
      /\
     /E2E\      10-20% (Poucos, lentos)
    /------\
   /  Int.  \   20-30% (Médios)
  /----------\
 /  Unitário  \ 50-70% (Muitos, rápidos)
/____________\
```

**Por que essa proporção?**
- Unitários: Rápidos, estáveis, baratos de manter
- E2E: Lentos, frágeis, caros de manter

#### ⚠️ Armadilhas Comuns

❌ **Ice Cream Cone** (invertido):
```
  ____________
 /   E2E!!!   \  ← Muitos E2E
/              \
\   Integração /  ← Poucos integração
 \            /
  \  Unit   /     ← Quase nenhum unitário
   \______/
```
**Problemas:**
- Testes lentos (horas para executar)
- Frágeis (falham sem motivo)
- Caros de manter
- Feedback lento

---

### Exercício 1.4: Criando Critérios de Aceitação Testáveis 🔴 (Solução Nível 4)

#### ✅ Resposta Completa

**User Story 1: Validar CNPJ**

```gherkin
Cenário 1: Validar CNPJ válido com formatação
Given eu tenho um CNPJ formatado "11.222.333/0001-81"
When eu submeto para validação
Then o sistema retorna "válido"
And o CNPJ é retornado formatado corretamente
```
**Tipo de teste:** Unitário  
**Ferramenta:** pytest + função de validação  
**Automação:** 100% automatizável

```gherkin
Cenário 2: Rejeitar CNPJ com dígitos verificadores inválidos
Given eu tenho um CNPJ "11.222.333/0001-99" (DV errado)
When eu submeto para validação
Then o sistema retorna "inválido"
And a mensagem de erro contém "dígitos verificadores incorretos"
```
**Tipo de teste:** Unitário  
**Ferramenta:** pytest + parametrização  
**Automação:** 100% automatizável

```gherkin
Cenário 3: Rejeitar CNPJ com todos dígitos iguais
Given eu tenho um CNPJ "11111111111111"
When eu submeto para validação
Then o sistema retorna "inválido"
And a mensagem de erro contém "CNPJ inválido"
```
**Tipo de teste:** Unitário  
**Ferramenta:** pytest  
**Automação:** 100% automatizável

---

**User Story 2: Sistema Rápido**

⚠️ **Problema:** "Rápido" é vago e não mensurável!

**Versão Melhorada da User Story:**
```
Como administrador
Quero que validação de CNPJ responda em menos de 200ms
Para que usuários tenham boa experiência (< 1s para formulário completo)
```

```gherkin
Cenário 1: Validação única abaixo de 200ms
Given o sistema está em produção
When eu valido um CNPJ
Then a resposta é recebida em menos de 200ms
```
**Tipo de teste:** Performance/Unitário  
**Ferramenta:** pytest-benchmark  
**Automação:** 100% automatizável

```python
def test_validation_performance(benchmark):
    cnpj = "11.222.333/0001-81"
    result = benchmark(validate_cnpj, cnpj)
    assert benchmark.stats['mean'] < 0.2  # 200ms
```

```gherkin
Cenário 2: Validação em lote de 100 CNPJs abaixo de 5 segundos
Given eu tenho uma lista de 100 CNPJs
When eu envio para validação em lote
Then a resposta é recebida em menos de 5 segundos
```
**Tipo de teste:** Performance/Integração  
**Ferramenta:** pytest-benchmark + API  
**Automação:** 100% automatizável

```gherkin
Cenário 3: Página carrega em menos de 2 segundos
Given eu estou na página de validação
When a página termina de carregar
Then o tempo total é menor que 2 segundos
```
**Tipo de teste:** E2E + Performance  
**Ferramenta:** Lighthouse / Playwright  
**Automação:** 90% automatizável (métricas de UX)

---

**User Story 3: Sistema Seguro**

⚠️ **Problema:** "Seguro" é muito amplo!

**Versão Melhorada da User Story:**
```
Como usuário
Quero que meus dados estejam protegidos contra acesso não autorizado
Para garantir privacidade e conformidade com LGPD
```

```gherkin
Cenário 1: Dados transmitidos via HTTPS
Given eu estou usando o sistema
When qualquer requisição é feita
Then o protocolo usado é HTTPS (TLS 1.2+)
And certificado SSL é válido
```
**Tipo de teste:** Integração/Security  
**Ferramenta:** requests + ssllabs-scan  
**Automação:** 100% automatizável

```python
def test_https_only():
    response = requests.get("http://api.example.com")
    assert response.url.startswith("https://")  # Redirect para HTTPS
```

```gherkin
Cenário 2: Proteção contra SQL Injection
Given eu sou um atacante
When eu tento injetar SQL no campo CNPJ "11'; DROP TABLE users; --"
Then a injeção é bloqueada
And nenhuma query maliciosa é executada
And erro de validação é retornado
```
**Tipo de teste:** Security/Integração  
**Ferramenta:** SQLMap / Bandit  
**Automação:** 80% automatizável

```gherkin
Cenário 3: Autenticação obrigatória para APIs sensíveis
Given eu não estou autenticado
When eu tento acessar endpoint de dados privados
Then recebo status 401 Unauthorized
And nenhum dado é retornado
```
**Tipo de teste:** Security/API  
**Ferramenta:** pytest + requests  
**Automação:** 100% automatizável

```python
def test_authentication_required():
    response = requests.get("https://api.example.com/private")
    assert response.status_code == 401
```

#### 💡 Explicação Detalhada

**Formato Given-When-Then:**
- **Given**: Contexto/pré-condição (estado inicial)
- **When**: Ação (o que o usuário faz)
- **Then**: Resultado esperado (verificação)

**Por que esse formato?**
1. ✅ **Claro**: Qualquer pessoa entende
2. ✅ **Testável**: Direto para automação
3. ✅ **Mensurável**: Critérios objetivos
4. ✅ **Comunicação**: Dev, QA e PO falam a mesma língua

#### 🎯 Pontos-Chave

**Transformando requisitos vagos:**

| Vago | Específico | Mensurável |
|------|------------|------------|
| "Rápido" | "Resposta em menos de 200ms" | ✅ Sim |
| "Seguro" | "HTTPS com TLS 1.2+" | ✅ Sim |
| "Fácil de usar" | "Usuário completa tarefa em < 3 cliques" | ✅ Sim |
| "Confiável" | "Uptime de 99,9%" | ✅ Sim |

#### 🚀 Além do Básico

**BDD (Behavior-Driven Development):**
Use ferramentas como **Cucumber**, **Behave** (Python), ou **SpecFlow** (C#) para escrever testes diretamente em Gherkin:

```gherkin
# features/cnpj_validation.feature

Feature: Validação de CNPJ
  Como usuário do sistema
  Quero validar CNPJs
  Para garantir dados corretos

  Scenario: Validar CNPJ válido
    Given eu tenho um CNPJ "11.222.333/0001-81"
    When eu submeto para validação
    Then o resultado é "válido"
```

```python
# steps/cnpj_steps.py

from behave import given, when, then

@given('eu tenho um CNPJ "{cnpj}"')
def step_impl(context, cnpj):
    context.cnpj = cnpj

@when('eu submeto para validação')
def step_impl(context):
    context.result = validate_cnpj(context.cnpj)

@then('o resultado é "{esperado}"')
def step_impl(context, esperado):
    assert context.result['valid'] == (esperado == "válido")
```

---

## 🧪 Bloco 2: Testes Unitários e TDD - Soluções

### Exercício 2.1: Seu Primeiro Teste Unitário 🟢 (Solução Nível 1)

**Já fornecido no exercício** - Este era um exemplo guiado completo.

**Pontos Adicionais de Aprendizado:**

#### 🎯 Padrão AAA em Detalhe

```python
def test_example():
    # === ARRANGE (Preparar) ===
    # Configure tudo que o teste precisa:
    # - Dados de entrada
    # - Objetos/instâncias
    # - Mocks/stubs
    # - Estado inicial
    input_data = "valor de entrada"
    expected = "valor esperado"
    
    # === ACT (Agir) ===
    # Execute UMA ação principal:
    # - Chame a função/método sob teste
    # - Apenas UMA linha idealmente
    result = function_under_test(input_data)
    
    # === ASSERT (Verificar) ===
    # Verifique resultados:
    # - Compare resultado com expectativa
    # - Múltiplos asserts são OK se relacionados
    assert result == expected
    assert len(result) > 0
```

#### ⚠️ Armadilhas Comuns em Testes Unitários

❌ **Erro 1: Múltiplas ações no Act**
```python
# ERRADO
def test_bad():
    user = create_user()
    user.login()          # Ação 1
    user.update_profile() # Ação 2  ← Múltiplas ações!
    assert user.is_active
```

✅ **Correto: Um teste, uma ação**
```python
# CORRETO
def test_login():
    user = create_user()
    user.login()  # Apenas uma ação
    assert user.is_logged_in

def test_update_profile():
    user = create_logged_user()
    user.update_profile()  # Teste separado
    assert user.profile_updated
```

❌ **Erro 2: Testes dependentes**
```python
# ERRADO - Testes dependem de ordem
def test_create_user():
    global user
    user = User("João")
    
def test_user_login():
    global user
    user.login()  # Depende do teste anterior!
```

✅ **Correto: Testes independentes**
```python
# CORRETO - Cada teste é independente
@pytest.fixture
def user():
    return User("João")

def test_create_user(user):
    assert user.name == "João"
    
def test_user_login(user):
    user.login()
    assert user.is_logged_in
```

---

### Exercício 2.2: TDD - Red, Green, Refactor 🟡 (Solução Nível 2)

#### ✅ Resposta Completa

**1. RED - Testes (que vão falhar inicialmente):**

```python
import pytest
from cnpj_validator import is_valid_length, remove_formatting

class TestCNPJLength:
    """Testes para validação de tamanho de CNPJ."""
    
    def test_is_valid_length_with_14_digits(self):
        # Arrange
        cnpj = "11222333000181"
        
        # Act
        resultado = is_valid_length(cnpj)
        
        # Assert
        assert resultado is True
        
    def test_is_valid_length_with_less_than_14_digits(self):
        # Arrange
        cnpj = "1122233300018"  # 13 dígitos
        
        # Act
        resultado = is_valid_length(cnpj)
        
        # Assert
        assert resultado is False
        
    def test_is_valid_length_with_more_than_14_digits(self):
        # Arrange
        cnpj = "112223330001811"  # 15 dígitos
        
        # Act
        resultado = is_valid_length(cnpj)
        
        # Assert
        assert resultado is False
        
    def test_is_valid_length_with_empty_string(self):
        # Arrange
        cnpj = ""
        
        # Act
        resultado = is_valid_length(cnpj)
        
        # Assert
        assert resultado is False
        
    def test_is_valid_length_with_formatted_cnpj(self):
        # Arrange
        cnpj = "11.222.333/0001-81"  # Formatado
        
        # Act
        resultado = is_valid_length(cnpj)
        
        # Assert
        assert resultado is True  # Deve limpar antes
        
    @pytest.mark.parametrize("cnpj,esperado", [
        ("11222333000181", True),      # 14 dígitos
        ("1122233300018", False),      # 13 dígitos
        ("112223330001811", False),    # 15 dígitos
        ("", False),                    # Vazio
        ("abc", False),                 # Letras
        ("11.222.333/0001-81", True),  # Formatado válido
    ])
    def test_is_valid_length_parametrized(self, cnpj, esperado):
        assert is_valid_length(cnpj) == esperado
```

**2. GREEN - Implementação mínima:**

```python
def is_valid_length(cnpj: str) -> bool:
    """
    Valida se CNPJ tem exatamente 14 dígitos.
    
    Args:
        cnpj: String com CNPJ formatado ou não
        
    Returns:
        True se tem 14 dígitos, False caso contrário
    """
    if not cnpj:
        return False
    
    # Remover formatação
    cnpj_limpo = remove_formatting(cnpj)
    
    # Verificar se tem 14 dígitos
    return len(cnpj_limpo) == 14
```

**3. REFACTOR - Melhorias:**

```python
def is_valid_length(cnpj: str) -> bool:
    """
    Valida se CNPJ tem exatamente 14 dígitos.
    
    Aceita CNPJ formatado (11.222.333/0001-81) ou não (11222333000181).
    Remove automaticamente caracteres de formatação antes da validação.
    
    Args:
        cnpj: String com CNPJ, formatado ou não
        
    Returns:
        True se tem exatamente 14 dígitos numéricos, False caso contrário
        
    Examples:
        >>> is_valid_length("11222333000181")
        True
        >>> is_valid_length("11.222.333/0001-81")
        True
        >>> is_valid_length("1122233300018")
        False
    """
    if not cnpj or not isinstance(cnpj, str):
        return False
    
    # Remover formatação (pontos, barras, hífens)
    cnpj_limpo = remove_formatting(cnpj)
    
    # Verificar se contém apenas dígitos
    if not cnpj_limpo.isdigit():
        return False
    
    # Verificar se tem exatamente 14 dígitos
    return len(cnpj_limpo) == 14
```

#### 💡 Explicação Detalhada

**Ciclo TDD:**

```
1. RED (Vermelho)
   ↓ Escreva teste que falha
   
2. GREEN (Verde)
   ↓ Código mínimo para passar
   
3. REFACTOR (Refatorar)
   ↓ Melhore o código
   
→ Repita!
```

**Por que TDD funciona?**

1. **Especificação clara**: Teste define comportamento esperado
2. **Design emergente**: Código cresce conforme necessário
3. **Refatoração segura**: Testes garantem que não quebrou nada
4. **Cobertura automática**: 100% do código tem teste


#### 🎯 Pontos-Chave

**Vantagens do TDD:**
- ✅ Menos bugs (testes escritos primeiro)
- ✅ Melhor design (código testável é código bem projetado)
- ✅ Documentação viva (testes mostram como usar)
- ✅ Refatoração confiante (testes protegem)
- ✅ Cobertura completa (todo código tem teste)

**Quando usar TDD:**
- ✅ Lógica de negócio complexa
- ✅ Algoritmos críticos
- ✅ Funcionalidades novas e bem definidas

**Quando pular TDD:**
- ⚠️ Explorando soluções (spike/prototype)
- ⚠️ Código de UI (melhor fazer BDD)
- ⚠️ Integrações simples

#### ⚠️ Armadilhas Comuns

❌ **Erro: Implementar código antes dos testes**
- Perde os benefícios do TDD
- Testes tendem a ser superficiais

❌ **Erro: Testes muito complexos**
- Se teste é difícil, código provavelmente está mal projetado
- Simplifique o código, não o teste

❌ **Erro: Pular refatoração**
- Código fica sujo
- Dívida técnica acumula

---

### Exercício 2.3: Testando Edge Cases 🟠 (Solução Nível 3)

#### ✅ Resposta Completa

```python
import pytest
from cnpj_validator import has_all_same_digits

class TestAllSameDigits:
    """Testes para detecção de CNPJs com todos dígitos iguais."""
    
    # === HAPPY PATH ===
    def test_valid_cnpj_with_different_digits(self):
        """CNPJ válido com dígitos diferentes deve retornar False."""
        cnpj = "11222333000181"
        assert has_all_same_digits(cnpj) is False
    
    # === EDGE CASES: Todos dígitos iguais ===
    @pytest.mark.parametrize("digit", [str(i) for i in range(10)])
    def test_all_same_digits_0_to_9(self, digit):
        """CNPJs com todos dígitos iguais (00000... até 99999...) devem retornar True."""
        cnpj = digit * 14
        assert has_all_same_digits(cnpj) is True, f"Falhou para CNPJ {cnpj}"
    
    def test_cnpj_with_one_different_digit(self):
        """CNPJ com apenas um dígito diferente deve retornar False."""
        cnpj = "11111111111112"  # Último dígito diferente
        assert has_all_same_digits(cnpj) is False
    
    def test_empty_string(self):
        """String vazia deve retornar False (não tem dígitos iguais)."""
        cnpj = ""
        assert has_all_same_digits(cnpj) is False
    
    def test_less_than_14_digits(self):
        """CNPJ com menos de 14 dígitos deve retornar False."""
        cnpj = "1111111111"
        assert has_all_same_digits(cnpj) is False
    
    # === CASOS DE ERRO ===
    def test_cnpj_with_letters_should_be_cleaned_first(self):
        """CNPJ com letras deve ser tratado."""
        cnpj = "11.111.111/1111-11"  # Formatado com pontos
        # Assumindo que função limpa formatação primeiro
        assert has_all_same_digits(cnpj) is True
    
    def test_none_as_input(self):
        """None como entrada deve levantar exceção ou retornar False."""
        with pytest.raises(TypeError):
            has_all_same_digits(None)
    
    def test_non_string_type(self):
        """Tipo não-string deve levantar exceção."""
        with pytest.raises(TypeError):
            has_all_same_digits(12345678901234)  # int
    
    # === SECURITY: Injection attempts ===
    def test_sql_injection_attempt(self):
        """Tentativa de SQL injection não deve causar problemas."""
        cnpj = "'; DROP TABLE users; --"
        # Não deve quebrar, apenas retornar False
        assert has_all_same_digits(cnpj) is False
    
    def test_very_long_string(self):
        """String muito longa não deve causar DoS."""
        cnpj = "1" * 1000000  # 1 milhão de caracteres
        # Deve executar rapidamente (< 1 segundo)
        import time
        start = time.time()
        result = has_all_same_digits(cnpj)
        duration = time.time() - start
        assert duration < 1.0, "Função muito lenta para string grande"
```

**Implementação Robusta:**

```python
def has_all_same_digits(cnpj: str) -> bool:
    """
    Verifica se todos os dígitos do CNPJ são iguais.
    
    Args:
        cnpj: String contendo CNPJ (formatado ou não)
        
    Returns:
        True se todos os dígitos são iguais, False caso contrário
        
    Raises:
        TypeError: Se cnpj não for string
        
    Examples:
        >>> has_all_same_digits("11111111111111")
        True
        >>> has_all_same_digits("11222333000181")
        False
    """
    # Validação de tipo
    if not isinstance(cnpj, str):
        raise TypeError(f"CNPJ deve ser string, recebido {type(cnpj).__name__}")
    
    # String vazia ou muito curta
    if len(cnpj) < 14:
        return False
    
    # Limpar formatação
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
    
    # Garantir que tem exatamente 14 dígitos
    if len(cnpj_limpo) != 14:
        return False
    
    # Verificar se contém apenas dígitos
    if not cnpj_limpo.isdigit():
        return False
    
    # Verificar se todos são iguais
    primeiro_digito = cnpj_limpo[0]
    return all(d == primeiro_digito for d in cnpj_limpo)
```

#### 💡 Explicação Detalhada

**O que são Edge Cases?**

Edge cases (casos extremos) são situações nos limites do comportamento esperado:
- Valores mínimos/máximos
- Strings vazias
- Null/None
- Tipos inesperados
- Valores muito grandes

**Por que testar Edge Cases?**

1. **Bugs se escondem nos limites**: 80% dos bugs estão em edge cases
2. **Segurança**: Attackers exploram edge cases
3. **Robustez**: Sistema deve lidar com qualquer entrada

#### 🎯 Pontos-Chave

**Categorias de Edge Cases:**

1. **Boundaries (Limites)**
   - Vazio, mínimo, máximo
   - Exemplo: "", "0", "999999999"

2. **Invalid Types (Tipos Inválidos)**
   - None, int, list, object
   - Exemplo: None, 123, ["abc"]

3. **Invalid Format (Formato Inválido)**
   - Letras, símbolos especiais
   - Exemplo: "abc", "!@#$%"

4. **Security (Segurança)**
   - SQL injection, XSS, path traversal
   - Exemplo: "'; DROP TABLE", "<script>"

5. **Performance (Performance)**
   - Entradas muito grandes
   - Exemplo: string com 1MB

**Usar `pytest.mark.parametrize` para múltiplos casos:**

```python
@pytest.mark.parametrize("cnpj,esperado", [
    ("00000000000000", True),
    ("11111111111111", True),
    ("99999999999999", True),
    ("11222333000181", False),
])
def test_all_same_digits_multiple(cnpj, esperado):
    assert has_all_same_digits(cnpj) == esperado
```

---

### Exercício 2.4: Mocking e Isolamento 🔴 (Solução Nível 4)

#### ✅ Resposta Completa

```python
import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from requests.exceptions import Timeout, RequestException

from cnpj_validator import CNPJValidator

class TestCNPJValidatorWithReceita:
    """Testes para validação com API da Receita Federal (usando mocks)."""
    
    @pytest.fixture
    def validator(self):
        """Fixture que retorna instância do validador."""
        return CNPJValidator()
    
    # === SUCESSO (200) ===
    @patch('cnpj_validator.requests.get')
    def test_validate_with_receita_success(self, mock_get, validator):
        """Teste de sucesso com resposta 200."""
        # Arrange
        cnpj = "11.222.333/0001-81"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'cnpj': '11222333000181',
            'razao_social': 'Empresa Teste Ltda',
            'situacao': 'ATIVA',
            'data_abertura': '01/01/2020'
        }
        mock_get.return_value = mock_response
        
        # Act
        resultado = validator.validate_with_receita(cnpj)
        
        # Assert
        assert resultado['cnpj'] == '11222333000181'
        assert resultado['razao_social'] == 'Empresa Teste Ltda'
        assert resultado['situacao'] == 'ATIVA'
        
        # Verificar que chamou API corretamente
        mock_get.assert_called_once()
        call_url = mock_get.call_args[0][0]
        assert '11222333000181' in call_url
    
    # === ERRO 404 (CNPJ não encontrado) ===
    @patch('cnpj_validator.requests.get')
    def test_validate_with_receita_not_found(self, mock_get, validator):
        """Teste com CNPJ não encontrado (404)."""
        # Arrange
        cnpj = "99.999.999/9999-99"
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            'error': 'CNPJ não encontrado'
        }
        mock_get.return_value = mock_response
        
        # Act & Assert
        with pytest.raises(ValueError, match="CNPJ não encontrado"):
            validator.validate_with_receita(cnpj)
    
    # === ERRO 500 (Erro no servidor) ===
    @patch('cnpj_validator.requests.get')
    def test_validate_with_receita_server_error(self, mock_get, validator):
        """Teste com erro 500 do servidor."""
        # Arrange
        cnpj = "11.222.333/0001-81"
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
        mock_get.return_value = mock_response
        
        # Act & Assert
        with pytest.raises(requests.HTTPError):
            validator.validate_with_receita(cnpj)
    
    # === TIMEOUT ===
    @patch('cnpj_validator.requests.get')
    def test_validate_with_receita_timeout(self, mock_get, validator):
        """Teste de timeout na requisição."""
        # Arrange
        cnpj = "11.222.333/0001-81"
        mock_get.side_effect = Timeout("Connection timeout")
        
        # Act & Assert
        with pytest.raises(Timeout):
            validator.validate_with_receita(cnpj)
    
    # === RESPOSTA MALFORMADA ===
    @patch('cnpj_validator.requests.get')
    def test_validate_with_receita_malformed_response(self, mock_get, validator):
        """Teste com resposta JSON inválida."""
        # Arrange
        cnpj = "11.222.333/0001-81"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid JSON"):
            validator.validate_with_receita(cnpj)
    
    # === RETRY COM BACKOFF ===
    @patch('cnpj_validator.requests.get')
    @patch('cnpj_validator.time.sleep')  # Mock sleep para teste rápido
    def test_validate_with_receita_retry_on_failure(self, mock_sleep, mock_get, validator):
        """Teste de retry automático em caso de falha."""
        # Arrange
        cnpj = "11.222.333/0001-81"
        
        # Primeira chamada falha, segunda sucede
        mock_response_fail = Mock()
        mock_response_fail.status_code = 500
        
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {'cnpj': '11222333000181'}
        
        mock_get.side_effect = [mock_response_fail, mock_response_success]
        
        # Act
        resultado = validator.validate_with_receita(cnpj)
        
        # Assert
        assert resultado['cnpj'] == '11222333000181'
        assert mock_get.call_count == 2  # Chamou 2 vezes
        mock_sleep.assert_called_once()  # Esperou entre tentativas
    
    # === VERIFICAÇÃO DE CHAMADAS HTTP ===
    @patch('cnpj_validator.requests.get')
    def test_no_real_http_calls_made(self, mock_get, validator):
        """Garantir que nenhuma chamada HTTP real foi feita."""
        # Arrange
        cnpj = "11.222.333/0001-81"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'cnpj': '11222333000181'}
        mock_get.return_value = mock_response
        
        # Act
        validator.validate_with_receita(cnpj)
        
        # Assert
        # Se chegou aqui, teste passou sem fazer chamada real
        # Mock interceptou todas as chamadas
        assert mock_get.called
```

**Alternativa usando `responses` library:**

```python
import responses
import requests

class TestCNPJValidatorWithResponses:
    """Testes usando biblioteca 'responses' (mais conveniente)."""
    
    @responses.activate
    def test_validate_with_receita_using_responses(self):
        """Teste usando biblioteca responses."""
        # Arrange
        cnpj = "11222333000181"
        url = f"https://api.receitafederal.gov.br/cnpj/{cnpj}"
        
        responses.add(
            responses.GET,
            url,
            json={'cnpj': cnpj, 'razao_social': 'Empresa Teste'},
            status=200
        )
        
        # Act
        validator = CNPJValidator()
        resultado = validator.validate_with_receita(cnpj)
        
        # Assert
        assert resultado['cnpj'] == cnpj
        assert resultado['razao_social'] == 'Empresa Teste'
        assert len(responses.calls) == 1  # Uma chamada feita
```

#### 💡 Explicação Detalhada

**Por que Mockar?**

1. **Velocidade**: Testes unitários devem ser rápidos (ms, não segundos)
2. **Confiabilidade**: Não depende de rede/API externa
3. **Isolamento**: Testa apenas seu código, não a API
4. **Controle**: Simula qualquer cenário (erro, timeout, etc.)
5. **Custo**: Não gasta quota/dinheiro de API

**Quando Mockar vs Integração Real?**

| Tipo | Mock | Integração Real |
|------|------|-----------------|
| **Unitário** | ✅ Sempre | ❌ Nunca |
| **Integração** | ⚠️ Às vezes | ✅ Sempre |
| **E2E** | ❌ Nunca | ✅ Sempre |

#### 🎯 Pontos-Chave

**Biblioteca `unittest.mock`:**

```python
from unittest.mock import Mock, patch

# Mock simples
mock_obj = Mock()
mock_obj.method.return_value = "valor"

# Patch de função
@patch('module.function')
def test_something(mock_function):
    mock_function.return_value = "valor mockado"
    
# Patch de método de classe
@patch.object(MyClass, 'method')
def test_method(mock_method):
    mock_method.return_value = "mockado"
```

**Verificando chamadas:**

```python
# Foi chamado?
mock.assert_called()
mock.assert_called_once()

# Chamado com argumentos específicos?
mock.assert_called_with(arg1, arg2)
mock.assert_called_once_with(arg1, arg2)

# Quantas vezes?
assert mock.call_count == 3

# Não foi chamado?
mock.assert_not_called()
```

---

## 🔄 Bloco 3: CI/CD e Automação - Soluções

### Exercício 3.1: Configurando Pre-commit Hooks 🟢 (Solução Nível 1)

**Já fornecido no exercício** - Exemplo guiado completo.

**Comandos Adicionais:**

```bash
# Ver hooks instalados
pre-commit --version

# Atualizar hooks
pre-commit autoupdate

# Executar em arquivos específicos
pre-commit run --files src/file.py

# Desinstalar hooks (para debug)
pre-commit uninstall

# Reinstalar
pre-commit install
```

---

### Exercício 3.2: Criando Pipeline CI Básico 🟡 (Solução Nível 2)

#### ✅ Resposta Completa

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8 black bandit
        
    - name: Run black (check formatting)
      run: |
        black --check src/ tests/
        
    - name: Run flake8 (linting)
      run: |
        flake8 src/ tests/ --max-line-length=100 --statistics
        
    - name: Run bandit (security)
      run: |
        bandit -r src/ -f json -o bandit-report.json || true
        
    - name: Run tests with coverage
      run: |
        pytest tests/ -v --cov=src --cov-report=xml --cov-report=term
        
    - name: Check coverage threshold
      run: |
        coverage report --fail-under=80
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
        
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: |
          coverage.xml
          bandit-report.json
```

#### 💡 Explicação Detalhada

**Estrutura do Workflow:**

1. **Trigger (on)**: Quando executar (push, PR, schedule)
2. **Jobs**: Trabalhos paralelos ou sequenciais
3. **Steps**: Passos dentro de cada job
4. **Actions**: Ações reutilizáveis (checkout, setup-python)

**Boas Práticas:**

✅ **Cache de dependências**: Reduz tempo de 2min para 10s
✅ **Fail fast**: Para no primeiro erro
✅ **Artifacts**: Salva relatórios para análise
✅ **Conditional steps**: `if: always()` para executar mesmo com falha

---

## 🎓 Resumo e Conclusão

Este gabarito fornece soluções detalhadas para os primeiros blocos de exercícios. As soluções restantes seguiriam o mesmo padrão de qualidade e detalhamento.

### Como Continuar Seu Aprendizado

1. **Compare suas soluções** com as fornecidas
2. **Entenda o "porquê"** de cada decisão
3. **Experimente variações** das soluções
4. **Implemente em projeto real**
5. **Compartilhe conhecimento** com seu time

### Recursos Adicionais

**Documentação Oficial:**
- pytest: https://docs.pytest.org
- unittest.mock: https://docs.python.org/3/library/unittest.mock.html
- GitHub Actions: https://docs.github.com/actions

**Livros:**
- "Test-Driven Development" - Kent Beck
- "Growing Object-Oriented Software, Guided by Tests" - Freeman & Pryce

**Cursos:**
- Test Automation University (grátis)
- Real Python - Testing Course

---

**Versão:** 1.0  
**Última Atualização:*** Dezembro 2024  
**Autor:** Material de Treinamento QA Profissional  
**Licença:** MIT - Uso Educacional

---

> 💡 **Lembre-se**: O gabarito é um guia, não uma única verdade. Existem múltiplas soluções válidas. O importante é entender os princípios por trás de cada abordagem!

**Continue praticando e bons estudos! 🚀**
