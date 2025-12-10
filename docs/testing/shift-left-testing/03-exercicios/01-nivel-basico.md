# Exercícios Nível Básico 🟢

> Exercícios 1-3: Muito guiados, para construir fundamentos

---

## Exercício 1: Análise de PR com Shift Left

### 🎯 Tipo: EXEMPLO RESOLVIDO COMPLETO

Este exercício demonstra como um QA aplica Shift Left Testing ao revisar um Pull Request. **Leia, entenda e aprenda** - não precisa resolver, apenas acompanhar.

---

### Contexto

Você é QA em uma equipe que desenvolve o validador de CNPJ. Um desenvolvedor abriu um Pull Request com uma nova funcionalidade: **validação de CNPJ alfanumérico** (novo formato da Receita Federal que permite letras).

A equipe ainda não pratica Shift Left consistentemente. Sua missão é aplicar os princípios de Shift Left nesta revisão.

---

### Cenário

**Pull Request #42**: Adicionar validação de CNPJ alfanumérico

**Descrição do Dev**:
> "Implementei a validação para o novo formato de CNPJ que aceita letras nas posições do identificador. Funciona nos meus testes manuais."

**Arquivos alterados**:
- `src/cnpj_validator/validators/alphanumeric_validator.py` (novo)
- `src/cnpj_validator/cnpj_validator.py` (modificado)

**Código do novo validador** (simplificado):

```python
# src/cnpj_validator/validators/alphanumeric_validator.py

class AlphanumericCNPJValidator:
    """Validador para CNPJ alfanumérico"""
    
    CNPJ_PATTERN = re.compile(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')
    
    @staticmethod
    def validate_format(cnpj: str) -> dict:
        """Valida formato do CNPJ"""
        if AlphanumericCNPJValidator.CNPJ_PATTERN.match(cnpj):
            return {'valid': True, 'errors': []}
        return {'valid': False, 'errors': ['Formato inválido']}
```

---

### 🔍 SOLUÇÃO PASSO A PASSO

#### Passo 1: Verificar se houve refinamento prévio (Shift Left no planejamento)

**Pergunta**: Essa história foi refinada com QA antes do desenvolvimento?

**Análise**:
```
┌─────────────────────────────────────────────────────────────────────┐
│ CHECKLIST DE REFINAMENTO                                           │
│                                                                     │
│ □ História de usuário documentada?                                  │
│   → Não encontrada. PR tem apenas descrição vaga.                  │
│                                                                     │
│ □ Critérios de aceitação definidos?                                │
│   → Não definidos antes do desenvolvimento.                        │
│                                                                     │
│ □ QA participou da discussão?                                      │
│   → Aparentemente não. Não há menção a cenários de teste.          │
│                                                                     │
│ □ Riscos identificados?                                            │
│   → Não documentados.                                               │
│                                                                     │
│ CONCLUSÃO: Refinamento não seguiu Shift Left                       │
└─────────────────────────────────────────────────────────────────────┘
```

**Ação**: Comentar no PR sugerindo que futuras funcionalidades passem por refinamento com QA.

---

#### Passo 2: Definir critérios de aceitação retroativamente

**O que deveria ter sido definido ANTES**:

```gherkin
Funcionalidade: Validação de CNPJ Alfanumérico

  Cenário: CNPJ numérico no formato correto
    Dado que tenho o CNPJ "11.222.333/0001-81"
    Quando eu validar o formato
    Então deve retornar válido

  Cenário: CNPJ alfanumérico no formato correto
    Dado que tenho o CNPJ "11.222.33A/0001-81"
    Quando eu validar o formato
    Então deve retornar válido
    
  Cenário: CNPJ sem formatação
    Dado que tenho o CNPJ "11222333000181"
    Quando eu validar o formato
    Então deve retornar inválido com mensagem "CNPJ sem formatação"

  Cenário: CNPJ com caracteres especiais inválidos
    Dado que tenho o CNPJ "11.222.333/0001-8!"
    Quando eu validar o formato
    Então deve retornar inválido com mensagem "Caracteres inválidos"

  Cenário: CNPJ com letras minúsculas
    Dado que tenho o CNPJ "11.222.33a/0001-81"
    Quando eu validar o formato
    Então deve retornar válido (conversão automática para maiúscula)
    OU deve retornar inválido (dependendo da regra de negócio)
```

**Ação**: Criar issue para definir critérios pendentes com PO.

---

#### Passo 3: Analisar os testes unitários do PR

**Verificando se o Dev escreveu testes**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ANÁLISE DE TESTES NO PR                                            │
│                                                                     │
│ Arquivos de teste alterados: NENHUM ⚠️                             │
│                                                                     │
│ PROBLEMA:                                                           │
│ - Nova funcionalidade sem nenhum teste automatizado                │
│ - Viola princípio "Dev escreve testes junto com código"            │
│ - Como sabemos que funciona? Apenas "testes manuais" mencionados   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Ação**: Solicitar testes unitários antes de aprovar o PR.

---

#### Passo 4: Identificar cenários de teste necessários

**Testes que deveriam existir**:

```python
# tests/test_alphanumeric_validator.py

import pytest
from src.cnpj_validator.validators.alphanumeric_validator import AlphanumericCNPJValidator


class TestAlphanumericValidatorFormat:
    """Testes de validação de formato"""
    
    # Casos positivos (happy path)
    def test_validate_format_numeric_cnpj_correct(self):
        """CNPJ numérico com formato correto deve ser válido"""
        result = AlphanumericCNPJValidator.validate_format("11.222.333/0001-81")
        assert result['valid'] is True
    
    def test_validate_format_alphanumeric_cnpj_correct(self):
        """CNPJ alfanumérico com formato correto deve ser válido"""
        result = AlphanumericCNPJValidator.validate_format("11.222.33A/0001-81")
        assert result['valid'] is True
    
    # Casos negativos
    def test_validate_format_without_formatting(self):
        """CNPJ sem formatação deve retornar erro específico"""
        result = AlphanumericCNPJValidator.validate_format("11222333000181")
        assert result['valid'] is False
        assert "formatação" in result['errors'][0].lower()
    
    def test_validate_format_with_invalid_chars(self):
        """CNPJ com caracteres especiais inválidos deve retornar erro"""
        result = AlphanumericCNPJValidator.validate_format("11.222.333/0001-8!")
        assert result['valid'] is False
    
    # Edge cases
    @pytest.mark.parametrize("cnpj", [
        "",
        None,
        "   ",
        "11.222.333/0001-811",  # muito longo
        "11.222.333/0001-8",    # muito curto
    ])
    def test_validate_format_edge_cases(self, cnpj):
        """Edge cases devem ser tratados sem exceção"""
        # Não deve lançar exceção
        result = AlphanumericCNPJValidator.validate_format(cnpj)
        assert result['valid'] is False
```

---

#### Passo 5: Verificar integração com pipeline CI/CD

**Checklist de CI/CD**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ VERIFICAÇÃO DE PIPELINE                                            │
│                                                                     │
│ ✅ Pipeline existe e está configurado                              │
│ ✅ Testes rodam automaticamente no PR                              │
│ ⚠️ Cobertura atual: PR não adiciona novos testes                   │
│ ✅ Linting passa                                                    │
│ ✅ Análise estática passa                                           │
│                                                                     │
│ OBSERVAÇÃO:                                                         │
│ Se o PR fosse mergeado assim, a cobertura de código diminuiria     │
│ (novo código sem testes = menos cobertura)                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

#### Passo 6: Documentar feedback no PR

**Comentário de revisão (exemplo)**:

```markdown
## Revisão de QA - Aplicando Shift Left

### ✅ Pontos Positivos
- Código bem estruturado
- Segue padrão do projeto

### ⚠️ Pontos de Atenção

#### 1. Falta de Refinamento Prévio
Esta funcionalidade não passou por refinamento com QA. 
Para próximas features, sugiro sessão de Three Amigos antes do desenvolvimento.

#### 2. Testes Unitários Ausentes
O PR não inclui testes automatizados. Por favor, adicione:
- Teste para CNPJ numérico válido
- Teste para CNPJ alfanumérico válido
- Teste para CNPJ sem formatação
- Teste para caracteres inválidos
- Testes de edge cases (null, vazio, etc.)

#### 3. Critérios de Aceitação
Precisamos definir com PO:
- Letras minúsculas são aceitas?
- Quais posições podem ter letras?
- Mensagens de erro esperadas?

### 📋 Próximos Passos
1. [ ] Definir critérios de aceitação com PO
2. [ ] Adicionar testes unitários
3. [ ] Atualizar PR para nova revisão

Obs: Não estou bloqueando o PR, mas sugiro fortemente atender 
estes pontos antes do merge.
```

---

### 📊 Análise do Resultado

**O que aprendemos com este exercício**:

| Princípio de Shift Left | Como foi aplicado |
|------------------------|-------------------|
| QA cedo | Feedback no PR, mesmo que tardio |
| Critérios testáveis | Definidos retroativamente |
| Dev escreve testes | Solicitado como requisito para merge |
| Automação | Verificado status do pipeline |
| Prevenção | Sugestão de processo para futuro |

**Conceitos aplicados**:
- Revisão de código com foco em qualidade
- Definição de cenários de teste
- Feedback construtivo
- Identificação de gaps no processo

---

### 💡 Lições para Levar

```
┌─────────────────────────────────────────────────────────────────────┐
│ LIÇÕES DESTE EXERCÍCIO                                             │
│                                                                     │
│ 1. Shift Left não é só "testar antes" - é envolver QA em TODO      │
│    o processo, desde requisitos até revisão de código.             │
│                                                                     │
│ 2. Se o processo não foi seguido, ainda podemos agregar valor      │
│    aplicando princípios retroativamente.                           │
│                                                                     │
│ 3. Feedback deve ser construtivo e educativo, não apenas           │
│    "está errado".                                                   │
│                                                                     │
│ 4. Testes unitários são responsabilidade do Dev, mas QA pode       │
│    guiar o que testar.                                              │
│                                                                     │
│ 5. Cada PR é oportunidade de melhorar o processo.                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Exercício 2: Refatoração com Testes

### 🎯 Tipo: PRÁTICA GUIADA

Agora é sua vez! Use as dicas para resolver.

---

### Contexto

Você precisa refatorar o método `validate_check_digits` do validador numérico. A refatoração vai melhorar a legibilidade, mas não deve mudar o comportamento.

**Princípio de Shift Left**: Antes de refatorar, garanta que existem testes que protegem contra regressões.

---

### Cenário

O código atual:

```python
# src/cnpj_validator/validators/numeric_validator.py

@staticmethod
def validate_check_digits(cnpj: str) -> bool:
    """Valida os dígitos verificadores do CNPJ."""
    if len(cnpj) != 14:
        return False
    
    first_digit = NumericCNPJValidator.calculate_first_digit(cnpj)
    if int(cnpj[12]) != first_digit:
        return False
    
    second_digit = NumericCNPJValidator.calculate_second_digit(cnpj)
    if int(cnpj[13]) != second_digit:
        return False
    
    return True
```

**Sua missão**: Garantir que existem testes adequados ANTES de fazer qualquer refatoração.

---

### Sua Tarefa

1. Identificar cenários de teste necessários
2. Escrever testes que cubram esses cenários
3. Executar os testes para garantir que passam
4. (Bônus) Sugerir a refatoração

---

### 💡 Dica 1: Identificando Cenários

Pense em:
- O que acontece com CNPJ de tamanho errado?
- O que acontece com primeiro dígito correto e segundo errado?
- O que acontece com primeiro errado e segundo correto?
- O que acontece com ambos corretos?
- E com ambos errados?

---

### 💡 Dica 2: Estrutura do Teste

Use esta estrutura como base:

```python
class TestValidateCheckDigits:
    """Testes para validação de dígitos verificadores"""
    
    def test_should_return_true_when_both_digits_are_correct(self):
        """Cenário: ambos os dígitos verificadores estão corretos"""
        # Arrange
        cnpj = "11222333000181"  # CNPJ válido conhecido
        
        # Act
        result = NumericCNPJValidator.validate_check_digits(cnpj)
        
        # Assert
        assert result is True
    
    def test_should_return_false_when_first_digit_is_wrong(self):
        # Seu código aqui...
        pass
```

---

### 💡 Dica 3: CNPJs para Teste

| CNPJ | Situação |
|------|----------|
| 11222333000181 | Válido (use como referência) |
| 11222333000191 | Primeiro dígito errado (8→9) |
| 11222333000182 | Segundo dígito errado (1→2) |
| 11222333000199 | Ambos errados |
| 1122233300018 | Tamanho errado (13 dígitos) |

---

### ✅ Critérios de Sucesso

Você completou o exercício se:

- [ ] Identificou pelo menos 5 cenários de teste
- [ ] Escreveu testes para cada cenário
- [ ] Todos os testes passam quando executados
- [ ] Os testes protegem contra regressão na refatoração

---

### 📝 Espaço para Sua Resposta

**Cenários identificados**:

```
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________
4. _______________________________________________
5. _______________________________________________
```

**Seus testes**:

```python
# Cole seu código de teste aqui
class TestValidateCheckDigits:
    """Seus testes para validação de dígitos verificadores"""
    
    # Escreva seus testes...
    pass
```

---

**Quando terminar**, compare com o [Gabarito - Exercício 2](../04-gabarito/01-nivel-basico.md#exercício-2-refatoração-com-testes).

---

## Exercício 3: Testes de API

### 🎯 Tipo: PRÁTICA SEMI-GUIADA

Menos dicas agora - você está progredindo!

---

### Contexto

O projeto inclui integração com a API da Receita Federal para consultar dados de CNPJ. Você precisa garantir que essa integração está testada adequadamente seguindo princípios de Shift Left.

---

### Cenário

O código de integração:

```python
# src/cnpj_validator/receita_federal_api.py

class ReceitaFederalAPI:
    """Cliente para consulta de CNPJ via API pública"""
    
    BASE_URL = "https://brasilapi.com.br/api/cnpj/v1"
    
    def consultar(self, cnpj: str) -> CNPJData:
        """Consulta dados de um CNPJ na API"""
        cnpj_clean = re.sub(r'[^0-9]', '', cnpj)
        url = f"{self.BASE_URL}/{cnpj_clean}"
        
        response = urlopen(Request(url))
        data = json.loads(response.read())
        
        return self._parse_response(data)
```

**Desafio**: A API real é externa. Como testar sem depender dela?

---

### Sua Tarefa

1. Identificar os tipos de teste necessários para esta integração
2. Decidir o que testar com mock vs. o que testar com API real
3. Escrever pelo menos 3 testes diferentes
4. Justificar suas decisões de design de teste

---

### 💡 Dica Única

Pense na **pirâmide de testes** para APIs:
- **Unitário**: Testar `_parse_response` isoladamente (mock do response)
- **Integração**: Testar comunicação com API (pode usar mock HTTP)
- **E2E/Smoke**: Testar com API real (poucos, lentos)

Como você dividiria seus testes?

---

### ✅ Critérios de Sucesso

- [ ] Identificou pelo menos 3 tipos de cenário diferentes
- [ ] Usou mocks apropriadamente
- [ ] Testes são determinísticos (não dependem de rede)
- [ ] Cobriu caso de sucesso e erro
- [ ] Justificou decisões de design

---

### 📝 Espaço para Sua Resposta

**Estratégia de testes escolhida**:

```
Tipo de teste       | O que testar              | Mock ou Real?
--------------------|---------------------------|---------------
Unitário           |                           |
Integração         |                           |
Smoke              |                           |
```

**Justificativa**:

```
Por que escolhi essa divisão:
_______________________________________________
_______________________________________________
_______________________________________________
```

**Seus testes**:

```python
# Cole seu código de teste aqui
import pytest
from unittest.mock import Mock, patch

class TestReceitaFederalAPI:
    """Seus testes para a API da Receita Federal"""
    
    # Escreva seus testes...
    pass
```

---

**Quando terminar**, compare com o [Gabarito - Exercício 3](../04-gabarito/01-nivel-basico.md#exercício-3-testes-de-api).

---

## 🎉 Parabéns!

Você completou os exercícios do nível básico!

**Próximo passo**: [Exercícios Nível Intermediário](02-nivel-intermediario.md) →

---

## 📚 Recursos de Apoio

Se precisou de ajuda extra:
- [Guia Teórico - Como Funciona](../02-guia-teorico/03-como-funciona.md)
- [Exemplo Prático - Unit Tests](../05-exemplos-pratica/exemplo-01-unit-tests.md)
- [Gabarito Nível Básico](../04-gabarito/01-nivel-basico.md)
