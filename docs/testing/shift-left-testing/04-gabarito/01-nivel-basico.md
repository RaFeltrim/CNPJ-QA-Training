# 📝 Gabarito - Nível Básico

> **Exercícios 1-3** | Tempo de Revisão: ~30 minutos

---

## Exercício 1: Identificação de Problemas

### 📋 Enunciado Resumido
Analisar os cenários A-D e identificar qual princípio Shift Left está sendo violado.

### ✅ Resposta Esperada

| Cenário | Princípio Violado | Justificativa |
|---------|-------------------|---------------|
| A | Fail Fast | Testes só em produção - problemas descobertos tarde demais |
| B | Automação | Testes manuais criam gargalo e inconsistência |
| C | Colaboração | QA isolado não recebe requisitos - retrabalho garantido |
| D | Continuous Feedback | Sem métricas = decisões sem base em dados |

### 💡 Por Que Funciona

**Cenário A - Fail Fast**:
O princípio "Fail Fast" diz que devemos descobrir problemas o mais cedo possível. Quando testes só rodam em produção, o ciclo de feedback é longo demais, e correções são 10-100x mais caras.

**Cenário B - Automação**:
Testes manuais não escalam. Uma equipe que dobra de tamanho não consegue dobrar testes manuais na mesma proporção. Automação permite crescimento sustentável.

**Cenário C - Colaboração**:
Se QA não participa desde os requisitos, testa contra entendimento errado. "Shift Left" significa mover QA para o início, não apenas automação.

**Cenário D - Continuous Feedback**:
Sem métricas, não sabemos se estamos melhorando ou piorando. "O que não é medido não pode ser melhorado" (Peter Drucker).

### ⚠️ Erros Comuns

1. **Confundir Fail Fast com "testar tudo rápido"**
   - Fail Fast é sobre descobrir problemas cedo, não velocidade de execução

2. **Achar que Automação resolve tudo**
   - Automação de processo ruim = processo ruim automatizado

3. **Pensar que Colaboração = mais reuniões**
   - Colaboração efetiva reduz reuniões, não aumenta

4. **Métricas sem contexto**
   - Medir "bugs encontrados" pode criar incentivo errado

### 🔄 Alternativas Aceitáveis

- **Cenário A**: Também aceitar "Continuous Testing" ou "Test Early"
- **Cenário B**: "Test Early" também é válido se justificado
- **Cenário C**: "Comunicação Efetiva" é termo alternativo aceitável
- **Cenário D**: "Métricas de Qualidade" ou "Data-Driven Testing"

### 📚 Conexão com a Teoria

Este exercício conecta com:
- [02-fundamentacao-teorica.md](../02-guia-teorico/02-fundamentacao-teorica.md) - 8 Princípios
- Regra 1-10-100 de custo de defeitos

### 🎯 Pontos de Discussão

1. "Por que empresas ainda resistem a Shift Left?"
2. "Qual princípio é mais difícil de implementar na sua experiência?"
3. "Como convencer gestão sobre investimento em automação?"

---

## Exercício 2: Teste Unitário Real

### 📋 Enunciado Resumido
Criar teste para a função `format_cnpj()` que formata CNPJ numérico para formato com pontuação.

### ✅ Resposta Esperada

```python
import pytest
from cnpj_validator import format_cnpj

class TestFormatCNPJ:
    """Testes para a função de formatação de CNPJ."""
    
    # --- Casos de Sucesso ---
    
    def test_format_cnpj_numerico_valido(self):
        """CNPJ numérico válido deve ser formatado corretamente."""
        # Arrange
        cnpj = "11222333000181"
        
        # Act
        resultado = format_cnpj(cnpj)
        
        # Assert
        assert resultado == "11.222.333/0001-81"
    
    def test_format_cnpj_ja_formatado(self):
        """CNPJ já formatado deve permanecer igual."""
        # Arrange
        cnpj = "11.222.333/0001-81"
        
        # Act
        resultado = format_cnpj(cnpj)
        
        # Assert
        assert resultado == "11.222.333/0001-81"
    
    # --- Casos de Borda ---
    
    def test_format_cnpj_com_espacos(self):
        """CNPJ com espaços deve ser limpo e formatado."""
        # Arrange
        cnpj = " 11222333000181 "
        
        # Act
        resultado = format_cnpj(cnpj)
        
        # Assert
        assert resultado == "11.222.333/0001-81"
    
    # --- Casos de Erro ---
    
    def test_format_cnpj_tamanho_incorreto(self):
        """CNPJ com tamanho incorreto deve lançar ValueError."""
        # Arrange
        cnpj = "1122233300018"  # 13 dígitos
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            format_cnpj(cnpj)
        
        assert "14 dígitos" in str(exc_info.value)
    
    def test_format_cnpj_vazio(self):
        """CNPJ vazio deve lançar ValueError."""
        # Arrange
        cnpj = ""
        
        # Act & Assert
        with pytest.raises(ValueError):
            format_cnpj(cnpj)
    
    def test_format_cnpj_none(self):
        """CNPJ None deve lançar TypeError."""
        # Act & Assert
        with pytest.raises(TypeError):
            format_cnpj(None)
    
    # --- Parametrização para múltiplos casos ---
    
    @pytest.mark.parametrize("entrada,esperado", [
        ("11222333000181", "11.222.333/0001-81"),
        ("00000000000191", "00.000.000/0001-91"),
        ("99999999999999", "99.999.999/9999-99"),
    ])
    def test_format_cnpj_diversos_validos(self, entrada, esperado):
        """Teste parametrizado para diversos CNPJs válidos."""
        assert format_cnpj(entrada) == esperado
```

### 💡 Por Que Funciona

**Estrutura AAA (Arrange-Act-Assert)**:
- Separa claramente preparação, execução e verificação
- Facilita leitura e manutenção
- Padrão da indústria

**Cobertura de Cenários**:
- ✅ Caso feliz (happy path)
- ✅ Casos de borda (espaços, já formatado)
- ✅ Casos de erro (tamanho, vazio, None)

**Boas Práticas Aplicadas**:
- Docstrings explicativas
- Nomes descritivos (`test_format_cnpj_numerico_valido`)
- Uso de `pytest.raises` para exceções
- Parametrização para reduzir duplicação

### ⚠️ Erros Comuns

1. **Testar apenas o caso feliz**
   ```python
   # ❌ Incompleto
   def test_format():
       assert format_cnpj("11222333000181") == "11.222.333/0001-81"
   ```

2. **Não usar AAA**
   ```python
   # ❌ Difícil de ler
   def test_format():
       assert format_cnpj(" 11222333000181 ") == "11.222.333/0001-81" and format_cnpj("") raises ValueError
   ```

3. **Assert sem mensagem útil**
   ```python
   # ❌ Mensagem de erro genérica
   assert resultado == esperado
   
   # ✅ Melhor
   assert resultado == esperado, f"Esperado {esperado}, obtido {resultado}"
   ```

4. **Não testar exceções corretamente**
   ```python
   # ❌ Não verifica mensagem
   with pytest.raises(ValueError):
       format_cnpj("")
   
   # ✅ Verifica mensagem
   with pytest.raises(ValueError) as exc:
       format_cnpj("")
   assert "específica" in str(exc.value)
   ```

### 🔄 Alternativas Aceitáveis

- Usar `unittest` ao invés de `pytest`
- Separar em múltiplos arquivos por tipo de teste
- Usar fixtures para setup comum
- Adicionar testes de performance

### 📚 Conexão com a Teoria

- [03-como-funciona.md](../02-guia-teorico/03-como-funciona.md) - Pirâmide de Testes (base são unitários)
- [04-como-aplicar.md](../02-guia-teorico/04-como-aplicar.md) - Ferramentas e práticas

### 🎯 Pontos de Discussão

1. "Quantos testes são suficientes para uma função simples?"
2. "Como decidir quais casos de borda testar?"
3. "Testes parametrizados vs testes individuais - quando usar cada um?"

---

## Exercício 3: Pipeline CI/CD Básico

### 📋 Enunciado Resumido
Analisar o pipeline GitHub Actions do projeto CNPJ e responder perguntas sobre sua estrutura.

### ✅ Resposta Esperada

#### 3.1 Estágios do Pipeline

```yaml
Pipeline CNPJ-QA-Training:

┌─────────────────────────────────────────────────────────────┐
│ TRIGGER: push (master) / pull_request (master)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. quality-checks (Verificações de Qualidade)               │
│    ├── Checkout código                                       │
│    ├── Setup Python 3.11                                     │
│    ├── Instalar dependências                                │
│    ├── Lint com flake8                                       │
│    └── Formatação com black --check                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. unit-tests (Testes Unitários)                            │
│    ├── needs: quality-checks                                 │
│    ├── Matrix: Python 3.8, 3.9, 3.10, 3.11                  │
│    ├── pytest com cobertura                                  │
│    └── Upload coverage para Codecov                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. integration-tests (Testes de Integração)                 │
│    ├── needs: unit-tests                                     │
│    ├── Testes com API mock                                   │
│    └── Validação end-to-end                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. security (Verificações de Segurança)                     │
│    ├── needs: integration-tests                              │
│    ├── Bandit (SAST)                                         │
│    └── Safety check dependências                             │
└─────────────────────────────────────────────────────────────┘
```

#### 3.2 O que é `needs:`?

**Definição**: A palavra-chave `needs:` define **dependências entre jobs** no GitHub Actions.

**Comportamento**:
- Job só inicia quando jobs listados em `needs:` terminam com sucesso
- Se job dependente falha, jobs subsequentes são cancelados
- Permite execução paralela de jobs independentes

**Exemplo do projeto**:
```yaml
unit-tests:
  needs: quality-checks  # Só roda se quality-checks passar
```

#### 3.3 Por que Matrix de Versões?

**Razões**:
1. **Compatibilidade**: Garante que código funciona em todas versões suportadas
2. **Detecção precoce**: Encontra problemas de sintaxe/APIs deprecadas
3. **Confiança**: Usuários podem usar qualquer versão listada
4. **Best Practice**: Padrão em projetos open source

**Trade-offs**:
- ✅ Mais cobertura
- ⚠️ Mais tempo de execução
- ⚠️ Mais uso de recursos CI

#### 3.4 Fail Fast em Ação

**Identificação no pipeline**:
```yaml
strategy:
  fail-fast: true  # Implícito ou explícito
```

**Como funciona**:
1. Primeiro estágio (quality-checks) roda primeiro
2. Se falhar, pipeline para imediatamente
3. Não gasta recursos com testes se código tem problemas de lint

**Benefícios**:
- Feedback mais rápido (< 1 min vs 10+ min)
- Economia de recursos de CI
- Incentiva código limpo

### 💡 Por Que Funciona

**Pipeline em estágios** segue a pirâmide de testes:
1. Checks rápidos primeiro (lint, format)
2. Testes unitários (muitos, rápidos)
3. Testes integração (menos, mais lentos)
4. Segurança (análise estática)

**Ordem otimiza para Fail Fast**:
- Problemas mais comuns (lint) detectados em segundos
- Só investe tempo em testes se código está "limpo"

### ⚠️ Erros Comuns

1. **Não entender dependências**
   - Achar que jobs rodam em sequência por padrão (rodam em paralelo)

2. **Confundir Matrix com duplicação**
   - Matrix é DRY (Don't Repeat Yourself) para múltiplas configs

3. **Ignorar Fail Fast**
   - Não perceber que ordem dos estágios importa

4. **Subestimar checks de qualidade**
   - "Lint é só estética" - não, previne bugs reais

### 🔄 Alternativas Aceitáveis

- Desenhar diagrama diferente mas correto
- Mencionar outros benefícios de matrix (cache, artifacts)
- Relacionar com outros sistemas CI (Jenkins, GitLab)

### 📚 Conexão com a Teoria

- [03-como-funciona.md](../02-guia-teorico/03-como-funciona.md) - Arquitetura de Pipeline
- [04-como-aplicar.md](../02-guia-teorico/04-como-aplicar.md) - Ferramentas CI/CD

### 🎯 Pontos de Discussão

1. "Como você melhoraria este pipeline?"
2. "Qual o tempo ideal para um pipeline?"
3. "Quando adicionar mais estágios?"

---

## 📊 Resumo da Avaliação - Nível Básico

| Exercício | Pontos Possíveis | Critérios Principais |
|-----------|------------------|----------------------|
| 1 | 25 | Identificação correta + justificativas |
| 2 | 40 | Código funcional + cobertura + boas práticas |
| 3 | 35 | Compreensão de CI/CD + análise crítica |
| **Total** | **100** | |

### Escala de Desempenho

- **90-100**: Pronto para nível intermediário
- **75-89**: Revisão rápida, então avançar
- **60-74**: Revisar teoria antes de avançar
- **< 60**: Refazer exercícios com suporte

---

| Anterior | Índice | Próximo |
|----------|--------|---------|
| [← Índice Gabarito](index.md) | [📚 Principal](../README.md) | [Intermediário →](02-nivel-intermediario.md) |
