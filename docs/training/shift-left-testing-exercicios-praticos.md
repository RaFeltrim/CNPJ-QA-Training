# Exercícios Práticos de Shift Left Testing

> **Material de Treinamento Profissional**  
> Metodologia: Scaffolding Pedagógico (Andaimes Educacionais)  
> Níveis: 1 (Guiado) → 4 (Autônomo)  
> Total: 18 Exercícios Progressivos

---

## 📋 Índice

1. [Como Usar Este Material](#como-usar-este-material)
2. [Metodologia Scaffolding](#metodologia-scaffolding)
3. [Exercícios - Bloco 1: Fundamentos](#bloco-1-fundamentos-de-shift-left)
4. [Exercícios - Bloco 2: Testes Unitários](#bloco-2-testes-unitários-e-tdd)
5. [Exercícios - Bloco 3: CI/CD](#bloco-3-cicd-e-automação)
6. [Exercícios - Bloco 4: Práticas Avançadas](#bloco-4-práticas-avançadas)
7. [Exercícios - Bloco 5: Implementação Real](#bloco-5-implementação-em-cenários-reais)

---

## 📖 Como Usar Este Material

### Estrutura dos Exercícios

Cada exercício segue a metodologia de **Scaffolding** (andaimes educacionais), reduzindo gradualmente o suporte conforme você desenvolve autonomia:

```
🟢 Nível 1 (Guiado Completo)      → Exemplo resolvido passo a passo
🟡 Nível 2 (Estrutura Guiada)     → Estrutura fornecida, você preenche
🟠 Nível 3 (Modelo Simplificado)  → Dicas e direção geral
🔴 Nível 4 (Totalmente Autônomo)  → Apenas enunciado, você resolve
```

### Como Progredir

1. **Comece pelo Nível 1**: Mesmo que pareça fácil, observe os padrões
2. **Não pule níveis**: Cada nível constrói sobre o anterior
3. **Faça hands-on**: Digite o código, não copie/cole
4. **Compare com gabarito**: Após sua tentativa, veja a solução
5. **Experimente variações**: Tente resolver de formas diferentes

### Pré-requisitos

- Conhecimento básico de programação (Python preferencial)
- Git básico
- Terminal/linha de comando
- IDE instalada (VSCode, PyCharm, etc.)
- Python 3.8+ instalado

### Tempo Estimado

- **Bloco 1**: 2-3 horas
- **Bloco 2**: 4-5 horas
- **Bloco 3**: 3-4 horas
- **Bloco 4**: 4-5 horas
- **Bloco 5**: 5-6 horas
- **Total**: ~20 horas (2-3 semanas part-time)

---

## 🎯 Metodologia Scaffolding

### O Que É Scaffolding?

**Scaffolding** (andaimes educacionais) é uma técnica pedagógica onde o instrutor fornece suporte estruturado que é gradualmente removido conforme o aluno desenvolve competência.

### Analogia da Construção

Imagine aprender a andar de bicicleta:

- **Nível 1**: Bicicleta com rodinhas + adulto segurando
- **Nível 2**: Apenas rodinhas
- **Nível 3**: Sem rodinhas, adulto ao lado
- **Nível 4**: Sozinho, sem suporte

### Aplicação nos Exercícios

| Nível | Suporte | O Que Você Faz | Aprendizado |
|-------|---------|----------------|-------------|
| 🟢 **Nível 1** | 90% | Observa e replica | Padrões e estrutura |
| 🟡 **Nível 2** | 60% | Preenche lacunas | Lógica e sintaxe |
| 🟠 **Nível 3** | 30% | Constrói com dicas | Resolução de problemas |
| 🔴 **Nível 4** | 0% | Resolve completamente | Autonomia total |

---

## 📚 Bloco 1: Fundamentos de Shift Left

### Exercício 1.1: Identificando Shift Left 🟢 (Nível 1)

**Objetivo:** Reconhecer características de Shift Left em cenários reais.

**Contexto:**  
Você é QA em uma empresa e está avaliando duas equipes diferentes. Identifique qual equipe pratica Shift Left Testing.

**Equipe A:**
- Desenvolvedores escrevem código completo
- QA testa tudo no final da sprint
- Bugs encontrados são logados no Jira
- Correções acontecem na próxima sprint
- Deploy manual após aprovação de QA

**Equipe B:**
- Requisitos incluem critérios de aceitação testáveis
- Desenvolvedores escrevem testes unitários junto com código
- Pipeline CI/CD executa testes automaticamente
- QA revisa estratégia de testes no refinamento
- Deploy automático após testes passarem

**Solução Guiada:**

**Resposta:** Equipe B pratica Shift Left Testing.

**Análise detalhada:**

| Característica | Equipe A (Tradicional) | Equipe B (Shift Left) |
|----------------|------------------------|----------------------|
| **Quando testa** | Final da sprint | Durante desenvolvimento |
| **Quem testa** | Apenas QA | Dev + QA |
| **Automação** | Nenhuma/limitada | Extensiva |
| **Feedback** | Dias/semana | Minutos |
| **Custo de correção** | Alto (sprint seguinte) | Baixo (imediato) |

**Indicadores de Shift Left na Equipe B:**
1. ✅ Critérios de aceitação definidos cedo (planejamento)
2. ✅ Desenvolvedores escrevem testes (responsabilidade compartilhada)
3. ✅ Automação em CI/CD (feedback rápido)
4. ✅ QA envolvido no refinamento (prevenção)
5. ✅ Deploy automático (confiança na qualidade)

**Aprendizado:** Shift Left é sobre **quando**, **quem** e **como** testamos, não apenas **o que** testamos.

---

### Exercício 1.2: Calculando ROI de Shift Left 🟡 (Nível 2)

**Objetivo:** Entender o impacto financeiro de encontrar bugs cedo.

**Contexto:**  
Sua empresa encontrou 100 bugs no último trimestre. Calcule o custo total em cada cenário:

**Dados:**
- Custo de correção na fase de Requisitos: R$ 100
- Custo de correção na fase de Desenvolvimento: R$ 1.000
- Custo de correção na fase de Testes: R$ 1.500
- Custo de correção em Produção: R$ 10.000

**Cenário A (Tradicional):**
- 5 bugs encontrados em Requisitos
- 10 bugs encontrados em Desenvolvimento
- 25 bugs encontrados em Testes
- 60 bugs encontrados em Produção

**Cenário B (Shift Left):**
- 30 bugs encontrados em Requisitos
- 50 bugs encontrados em Desenvolvimento
- 15 bugs encontrados em Testes
- 5 bugs encontrados em Produção

**Template para Solução:**

```
Cenário A (Tradicional):
- Requisitos: 5 × R$ 100 = R$ ______
- Desenvolvimento: 10 × R$ 1.000 = R$ ______
- Testes: 25 × R$ 1.500 = R$ ______
- Produção: 60 × R$ 10.000 = R$ ______
TOTAL: R$ ______

Cenário B (Shift Left):
- Requisitos: 30 × R$ 100 = R$ ______
- Desenvolvimento: 50 × R$ 1.000 = R$ ______
- Testes: 15 × R$ 1.500 = R$ ______
- Produção: 5 × R$ 10.000 = R$ ______
TOTAL: R$ ______

Economia com Shift Left: R$ ______
ROI percentual: ______%
```

**Tarefa:** Preencha os valores e calcule a economia.

---

### Exercício 1.3: Test Pyramid - Classificação 🟠 (Nível 3)

**Objetivo:** Classificar testes na pirâmide correta.

**Contexto:**  
Você herdou uma suíte de testes com 50 testes. Classifique cada tipo de teste na Test Pyramid:

**Lista de Testes:**
1. Teste de validação de CNPJ (função pura, sem dependências)
2. Teste de login via interface gráfica (Selenium)
3. Teste de API REST de criação de usuário
4. Teste de cálculo de desconto (função pura)
5. Teste de fluxo completo de compra (do carrinho ao pagamento)
6. Teste de integração entre serviço de pedidos e banco de dados
7. Teste de formatação de data (função pura)
8. Teste de toda jornada do usuário (cadastro → compra → logout)
9. Teste de endpoint de consulta de produtos
10. Teste de validação de email (regex, função pura)

**Dicas:**
- **Unitários**: Funções puras, sem dependências externas
- **Integração**: Múltiplos componentes, banco de dados, APIs internas
- **E2E**: Interface gráfica, fluxos completos do usuário

**Tarefa:** Crie uma tabela classificando cada teste e justifique.

---

### Exercício 1.4: Criando Critérios de Aceitação Testáveis 🔴 (Nível 4)

**Objetivo:** Transformar requisitos vagos em critérios testáveis.

**Contexto:**  
Product Owner escreveu as seguintes user stories. Sua tarefa é adicionar critérios de aceitação testáveis no formato **Given-When-Then**.

**User Story 1:**
```
Como usuário
Quero validar um CNPJ
Para garantir que é válido antes de cadastrar
```

**User Story 2:**
```
Como administrador
Quero que o sistema seja rápido
Para que usuários tenham boa experiência
```

**User Story 3:**
```
Como usuário
Quero que o sistema seja seguro
Para proteger meus dados
```

**Tarefa:** Para cada user story, escreva:
- Pelo menos 3 critérios de aceitação no formato Given-When-Then
- Identifique como cada critério pode ser testado (unitário, integração, E2E)
- Sugira ferramentas/técnicas para cada tipo de teste

---

## 🧪 Bloco 2: Testes Unitários e TDD

### Exercício 2.1: Seu Primeiro Teste Unitário 🟢 (Nível 1)

**Objetivo:** Escrever um teste unitário básico.

**Contexto:**  
Você precisa implementar uma função que remove formatação de CNPJ.

**Função a testar:**
```python
def remove_formatting(cnpj: str) -> str:
    """Remove pontos, barras e hífens de um CNPJ."""
    return cnpj.replace(".", "").replace("/", "").replace("-", "")
```

**Teste Completo (Exemplo):**

```python
import pytest
from cnpj_validator import remove_formatting

class TestRemoveFormatting:
    """Testes para função remove_formatting."""
    
    def test_remove_formatting_from_valid_cnpj(self):
        # Arrange (Preparar)
        cnpj_formatado = "11.222.333/0001-81"
        esperado = "11222333000181"
        
        # Act (Agir)
        resultado = remove_formatting(cnpj_formatado)
        
        # Assert (Verificar)
        assert resultado == esperado
        
    def test_remove_formatting_already_clean(self):
        # Arrange
        cnpj_limpo = "11222333000181"
        esperado = "11222333000181"
        
        # Act
        resultado = remove_formatting(cnpj_limpo)
        
        # Assert
        assert resultado == esperado
        
    def test_remove_formatting_empty_string(self):
        # Arrange
        cnpj_vazio = ""
        esperado = ""
        
        # Act
        resultado = remove_formatting(cnpj_vazio)
        
        # Assert
        assert resultado == esperado
```

**Executar o teste:**
```bash
pytest test_cnpj.py -v
```

**Análise do padrão AAA (Arrange-Act-Assert):**

1. **Arrange (Preparar):** Configure dados de entrada e expectativa
2. **Act (Agir):** Execute a função sob teste
3. **Assert (Verificar):** Compare resultado com expectativa

**Seu Exercício:**  
Digite o código acima, execute e observe os resultados.

---

### Exercício 2.2: TDD - Red, Green, Refactor 🟡 (Nível 2)

**Objetivo:** Praticar o ciclo TDD.

**Contexto:**  
Implemente uma função `is_valid_length(cnpj: str) -> bool` que retorna `True` se o CNPJ tem exatamente 14 dígitos (após limpeza).

**Ciclo TDD:**

**1. RED - Escreva o teste (que vai falhar):**

```python
def test_is_valid_length_with_14_digits():
    # Arrange
    cnpj = "11222333000181"
    
    # Act
    resultado = is_valid_length(cnpj)
    
    # Assert
    assert resultado is True
```

**Tarefa:** Execute o teste e veja ele falhar (RED).

**2. GREEN - Implemente o mínimo para passar:**

```python
def is_valid_length(cnpj: str) -> bool:
    # Sua implementação aqui
    pass
```

**Tarefa:** Implemente a função para o teste passar (GREEN).

**3. REFACTOR - Melhore o código:**

Adicione mais casos de teste:
- CNPJ com menos de 14 dígitos (deve retornar False)
- CNPJ com mais de 14 dígitos (deve retornar False)
- CNPJ com formatação (deve limpar antes de validar)
- String vazia (deve retornar False)

**Tarefa:** Escreva pelo menos 4 testes adicionais e refatore a função se necessário.

---

### Exercício 2.3: Testando Edge Cases 🟠 (Nível 3)

**Objetivo:** Identificar e testar casos extremos.

**Contexto:**  
Você tem uma função que valida se todos os dígitos de um CNPJ são diferentes (CNPJs como "11111111111111" são inválidos).

```python
def has_all_same_digits(cnpj: str) -> bool:
    """Retorna True se todos os dígitos são iguais."""
    # Implementação já existe
    pass
```

**Tarefa:**  
Crie uma suíte completa de testes cobrindo:

1. **Happy Path (Caminho Feliz):**
   - CNPJ válido com dígitos diferentes

2. **Edge Cases (Casos Extremos):**
   - Todos os dígitos iguais (00000000000000 até 99999999999999)
   - CNPJ com um dígito diferente
   - String vazia
   - CNPJ com menos de 14 dígitos
   - CNPJ com letras (deve tratar ou falhar?)

3. **Casos de Erro:**
   - None como entrada
   - Tipos não string

**Dicas:**
- Use `pytest.mark.parametrize` para testar múltiplos valores
- Pense em segurança: o que pode dar errado?
- Teste comportamento com entradas inesperadas

---

### Exercício 2.4: Mocking e Isolamento 🔴 (Nível 4)

**Objetivo:** Isolar testes usando mocks.

**Contexto:**  
Você tem uma função que consulta a API da Receita Federal para validar CNPJ:

```python
import requests

class CNPJValidator:
    def validate_with_receita(self, cnpj: str) -> dict:
        """Valida CNPJ consultando API da Receita Federal."""
        url = f"https://api.receitafederal.gov.br/cnpj/{cnpj}"
        response = requests.get(url)
        return response.json()
```

**Desafio:**  
Crie testes unitários **sem fazer chamadas reais à API**. Você deve:

1. Mockar a chamada `requests.get()`
2. Testar comportamento com sucesso (status 200)
3. Testar comportamento com erro (status 404, 500)
4. Testar timeout de rede
5. Testar resposta malformada

**Ferramentas sugeridas:**
- `unittest.mock` (built-in do Python)
- `pytest-mock` (plugin do pytest)
- `responses` (biblioteca de mocking)

**Tarefa:** Implemente os testes usando mocks, garantindo que nenhuma chamada HTTP real seja feita.

---

## 🔄 Bloco 3: CI/CD e Automação

### Exercício 3.1: Configurando Pre-commit Hooks 🟢 (Nível 1)

**Objetivo:** Implementar verificações automáticas antes de commit.

**Contexto:**  
Você quer garantir que código mal formatado ou com erros de linting não entre no repositório.

**Passo a Passo:**

**1. Instalar pre-commit:**
```bash
pip install pre-commit
```

**2. Criar arquivo `.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
      
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']
```

**3. Instalar hooks:**
```bash
pre-commit install
```

**4. Testar:**
```bash
pre-commit run --all-files
```

**Seu Exercício:**
1. Configure pre-commit no projeto CNPJ-QA-Training
2. Crie um arquivo Python com erros intencionais:
   - Linhas muito longas
   - Espaços em branco no final
   - Falta de linha em branco no final do arquivo
3. Tente fazer commit e observe os erros
4. Corrija e faça commit com sucesso

---

### Exercício 3.2: Criando Pipeline CI Básico 🟡 (Nível 2)

**Objetivo:** Configurar GitHub Actions para executar testes.

**Contexto:**  
Você quer que os testes executem automaticamente em cada push.

**Template Fornecido:**

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
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        # [TAREFA 1] Instalar dependências
        
    - name: Run linting
      run: |
        # [TAREFA 2] Executar flake8
        
    - name: Run tests
      run: |
        # [TAREFA 3] Executar pytest com coverage
        
    - name: Check coverage
      run: |
        # [TAREFA 4] Verificar cobertura mínima de 80%
```

**Suas Tarefas:**
1. Preencha as seções marcadas com [TAREFA]
2. Adicione step para executar black (verificação de formatação)
3. Adicione step para executar testes de segurança (bandit)
4. Configure para falhar se cobertura < 80%

**Dica:** Procure no repositório CNPJ-QA-Training por exemplos existentes.

---

### Exercício 3.3: Paralelização de Testes 🟠 (Nível 3)

**Objetivo:** Otimizar tempo de execução dos testes.

**Contexto:**  
Sua suíte de testes está demorando 10 minutos. Você precisa reduzir para menos de 3 minutos.

**Cenário:**
- 500 testes unitários (5 minutos)
- 100 testes de integração (4 minutos)
- 20 testes E2E (1 minuto)
- Total: 10 minutos

**Estratégias Disponíveis:**
1. Executar testes em paralelo (pytest-xdist)
2. Separar em jobs diferentes no CI
3. Cachear dependências
4. Executar apenas testes afetados

**Tarefa:**  
Projete uma estratégia de paralelização:
1. Calcule tempo esperado com cada estratégia
2. Identifique dependências entre testes
3. Configure pytest-xdist para testes unitários
4. Configure CI com matriz de jobs
5. Implemente caching de dependências

**Estrutura sugerida:**
```yaml
jobs:
  unit-tests:
    # Testes unitários em paralelo (4 workers)
    
  integration-tests:
    # Testes de integração (precisa de unit-tests)
    
  e2e-tests:
    # Testes E2E (precisa de integration-tests)
```

---

### Exercício 3.4: Rollback Automático em Falhas 🔴 (Nível 4)

**Objetivo:** Implementar estratégia de rollback automático.

**Contexto:**  
Você quer deploy automático, mas com segurança: se testes em staging falharem, deve fazer rollback.

**Requisitos:**
1. Deploy em staging após merge na branch main
2. Executar smoke tests em staging
3. Se smoke tests passarem → deploy em produção
4. Se smoke tests falharem → rollback staging + notificar time
5. Executar health checks pós-deploy em produção
6. Se health checks falharem → rollback produção + pager duty

**Desafio:**  
Desenhe e implemente o workflow completo de CI/CD com rollback:
- Use GitHub Actions ou GitLab CI
- Implemente smoke tests realistas
- Configure notificações (Slack/email)
- Documente processo de rollback manual
- Adicione métricas de tempo de deploy

---

## 🚀 Bloco 4: Práticas Avançadas

### Exercício 4.1: Security Testing (SAST) 🟢 (Nível 1)

**Objetivo:** Identificar vulnerabilidades de segurança no código.

**Contexto:**  
Você precisa adicionar scanning de segurança ao pipeline.

**Código com Vulnerabilidades:**

```python
import os
import pickle

def save_data(data, filename):
    """Salva dados em arquivo."""
    # Vulnerabilidade 1: Path traversal
    with open(filename, 'wb') as f:
        # Vulnerabilidade 2: Pickle inseguro
        pickle.dump(data, f)

def execute_command(user_input):
    """Executa comando do sistema."""
    # Vulnerabilidade 3: Command injection
    os.system(f"echo {user_input}")
    
def query_database(cnpj):
    """Consulta CNPJ no banco."""
    # Vulnerabilidade 4: SQL Injection
    query = f"SELECT * FROM empresas WHERE cnpj = '{cnpj}'"
    return execute_query(query)
```

**Ferramentas:**

**1. Bandit (Python):**
```bash
pip install bandit
bandit -r src/ -f json -o bandit-report.json
```

**2. Semgrep (Múltiplas linguagens):**
```bash
pip install semgrep
semgrep --config=auto src/
```

**Seu Exercício:**
1. Execute bandit no código acima
2. Identifique as 4 vulnerabilidades
3. Classifique severidade de cada uma
4. Corrija todas as vulnerabilidades
5. Re-execute bandit para confirmar correções

**Exemplo de correção para Vulnerabilidade 1:**
```python
import os
from pathlib import Path

def save_data_secure(data, filename):
    """Salva dados em arquivo de forma segura."""
    # Validar e sanitizar path
    safe_path = Path('/var/data') / Path(filename).name
    if not str(safe_path).startswith('/var/data'):
        raise ValueError("Path inválido")
    
    # Usar JSON em vez de pickle
    import json
    with open(safe_path, 'w') as f:
        json.dump(data, f)
```

---

### Exercício 4.2: Test Data Management 🟡 (Nível 2)

**Objetivo:** Gerenciar dados de teste de forma eficiente e segura.

**Contexto:**  
Você tem dados de produção que precisa usar em testes, mas contém informações sensíveis.

**Dados de Produção (Exemplo):**
```json
{
  "cnpj": "11.222.333/0001-81",
  "razao_social": "Empresa XYZ Ltda",
  "email": "contato@empresaxyz.com.br",
  "telefone": "+55 11 98765-4321",
  "cpf_socios": ["111.222.333-44", "555.666.777-88"],
  "faturamento": 5000000.00
}
```

**Requisitos:**
1. Anonimizar dados sensíveis (CPF, telefone, email)
2. Manter formato válido (CNPJ real, email válido)
3. Dados devem ser reproduzíveis (mesma seed = mesmos dados)
4. Versionar dados de teste no git

**Template:**

```python
from faker import Faker
import json

class TestDataGenerator:
    def __init__(self, seed=42):
        self.fake = Faker('pt_BR')
        Faker.seed(seed)
    
    def anonymize_company(self, company_data):
        """Anonimiza dados de empresa."""
        return {
            'cnpj': # [TAREFA 1] Manter CNPJ real ou gerar válido?
            'razao_social': # [TAREFA 2] Gerar nome fake
            'email': # [TAREFA 3] Gerar email fake
            'telefone': # [TAREFA 4] Gerar telefone fake
            'cpf_socios': # [TAREFA 5] Gerar CPFs válidos
            'faturamento': # [TAREFA 6] Manter, alterar ou anonimizar?
        }
```

**Suas Tarefas:**
1. Complete o código acima
2. Gere 10 empresas anonimizadas
3. Salve em `tests/data/empresas_test.json`
4. Crie fixtures do pytest usando esses dados
5. Use nos testes de integração

---

### Exercício 4.3: Performance Testing 🟠 (Nível 3)

**Objetivo:** Adicionar testes de performance ao Shift Left.

**Contexto:**  
Requisito: A validação de CNPJ deve processar 1000 CNPJs em menos de 1 segundo.

**Função a testar:**
```python
def validate_batch(cnpjs: list[str]) -> list[dict]:
    """Valida lista de CNPJs."""
    return [CNPJValidator().validate(cnpj) for cnpj in cnpjs]
```

**Requisitos do teste:**
1. Gerar 1000 CNPJs válidos
2. Executar validação em lote
3. Medir tempo de execução
4. Falhar se tempo > 1 segundo
5. Identificar gargalos (profiling)

**Ferramentas:**
- `pytest-benchmark` (integração com pytest)
- `cProfile` (profiling built-in)
- `memory_profiler` (uso de memória)

**Exemplo inicial:**
```python
import pytest
from cnpj_validator import validate_batch

def test_batch_validation_performance(benchmark):
    # Arrange
    cnpjs = generate_valid_cnpjs(1000)
    
    # Act & Assert
    result = benchmark(validate_batch, cnpjs)
    
    # Verificar que completou em < 1 segundo
    assert benchmark.stats['mean'] < 1.0
```

**Suas Tarefas:**
1. Implemente geração de 1000 CNPJs válidos
2. Configure pytest-benchmark
3. Execute e meça performance baseline
4. Se falhar, identifique gargalo com cProfile
5. Otimize código (dica: usar vectorização ou paralelização)
6. Re-execute e confirme melhoria

---

### Exercício 4.4: Chaos Engineering em Testes 🔴 (Nível 4)

**Objetivo:** Testar resiliência do sistema a falhas.

**Contexto:**  
Seu sistema consulta API externa da Receita Federal. Você quer garantir que lida bem com falhas:
- Timeout
- Rate limiting (429)
- Servidor indisponível (503)
- Resposta malformada
- Latência alta

**Requisitos:**
Implemente testes que:
1. Simulam falhas de rede (timeout)
2. Simulam rate limiting (retry com backoff)
3. Simulam resposta malformada (validação)
4. Simulam latência alta (timeout configurável)
5. Verificam fallback para cache local
6. Verificam logging adequado de erros
7. Verificam métricas de resiliência

**Desafio Avançado:**
Use biblioteca de chaos engineering (chaos-monkey, toxiproxy) para:
- Injetar latência variável
- Simular perda de pacotes
- Simular quedas intermitentes
- Testar circuit breaker pattern

**Estrutura sugerida:**
```python
import pytest
import requests
from unittest.mock import patch, Mock

class TestAPIResilience:
    
    def test_handles_timeout(self):
        # Simular timeout
        pass
    
    def test_retries_on_rate_limit(self):
        # Simular 429 + retry
        pass
    
    def test_falls_back_to_cache(self):
        # API falha → usa cache
        pass
    
    def test_circuit_breaker_opens(self):
        # Múltiplas falhas → circuit breaker abre
        pass
```

---

## 🌍 Bloco 5: Implementação em Cenários Reais

### Exercício 5.1: Projeto Piloto - Planejamento 🟢 (Nível 1)

**Objetivo:** Planejar implementação de Shift Left em um projeto real.

**Contexto:**  
Você foi designado para liderar a implantação de Shift Left em um projeto. O projeto é:
- **Sistema:** API REST de gerenciamento de clientes
- **Time:** 5 desenvolvedores, 2 QAs, 1 PO
- **Duração:** 3 meses (6 sprints de 2 semanas)
- **Estado Atual:** 
  - Cobertura de testes: 30%
  - Testes manuais apenas
  - Deploy manual semanal
  - ~20 bugs/mês em produção

**Template de Planejamento:**

```markdown
# Projeto Piloto: Shift Left Testing

## 1. Objetivos SMART

- [ ] Específico: _______________________________
- [ ] Mensurável: _______________________________
- [ ] Atingível: _______________________________
- [ ] Relevante: _______________________________
- [ ] Temporal: _______________________________

## 2. Métricas Baseline

- Cobertura de código: 30%
- Taxa de defeitos: 20/mês
- Tempo de deploy: _______
- Tempo de feedback: _______

## 3. Metas (3 meses)

- Cobertura de código: _______ (meta: 80%)
- Taxa de defeitos: _______ (meta: 5/mês)
- Tempo de deploy: _______
- Tempo de feedback: _______

## 4. Plano de 6 Sprints

### Sprint 1-2: Fundação
- [ ] _______________________________
- [ ] _______________________________

### Sprint 3-4: Implementação
- [ ] _______________________________
- [ ] _______________________________

### Sprint 5-6: Consolidação
- [ ] _______________________________
- [ ] _______________________________

## 5. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Resistência do time | Alta | Alto | ____________ |
| Falta de tempo | Média | Médio | ____________ |
| Ferramentas inadequadas | Baixa | Baixo | ____________ |

## 6. Recursos Necessários

- Orçamento: R$ _______
- Ferramentas: _______
- Treinamento: _______ horas
- Consultoria: _______
```

**Sua Tarefa:** Preencha o template completo com um plano realista.

---

### Exercício 5.2: Code Review Checklist 🟡 (Nível 2)

**Objetivo:** Criar checklist de code review focada em qualidade.

**Contexto:**  
Você quer padronizar code reviews para garantir qualidade consistente.

**Categorias:**
1. Testes
2. Cobertura
3. Qualidade de Código
4. Segurança
5. Performance
6. Documentação

**Template Inicial:**

```markdown
# Code Review Checklist - Shift Left

## ✅ Testes

- [ ] Testes unitários incluídos para código novo?
- [ ] [TAREFA 1] Adicione 3 itens sobre testes
- [ ] _______________________________
- [ ] _______________________________

## 📊 Cobertura

- [ ] Cobertura mantida ou melhorada?
- [ ] [TAREFA 2] Adicione 2 itens sobre cobertura
- [ ] _______________________________

## 🎯 Qualidade de Código

- [ ] [TAREFA 3] Adicione 5 itens sobre qualidade
- [ ] _______________________________
- [ ] _______________________________
- [ ] _______________________________
- [ ] _______________________________

## 🔒 Segurança

- [ ] [TAREFA 4] Adicione 4 itens sobre segurança
- [ ] _______________________________
- [ ] _______________________________
- [ ] _______________________________

## ⚡ Performance

- [ ] [TAREFA 5] Adicione 3 itens sobre performance
- [ ] _______________________________
- [ ] _______________________________

## 📝 Documentação

- [ ] [TAREFA 6] Adicione 3 itens sobre documentação
- [ ] _______________________________
- [ ] _______________________________
```

**Suas Tarefas:**
1. Complete todos os itens marcados com [TAREFA]
2. Priorize itens (crítico, importante, desejável)
3. Adicione exemplos do que constitui "bom" vs "ruim"
4. Crie versão automatizada (linter rules)

---

### Exercício 5.3: Treinamento da Equipe 🟠 (Nível 3)

**Objetivo:** Desenhar programa de treinamento de Shift Left.

**Contexto:**  
Você precisa treinar um time de 10 pessoas (7 devs, 2 QAs, 1 PO) em Shift Left Testing.

**Restrições:**
- Orçamento: R$ 20.000
- Tempo: 40 horas por pessoa (1 mês, 2h/dia)
- Formato: Misto (presencial + remoto)
- Objetivo: Time autônomo em Shift Left

**Requisitos do Programa:**
1. Conteúdo teórico e prático
2. Hands-on com projeto real
3. Avaliação de aprendizado
4. Certificação interna

**Estrutura Sugerida:**

```markdown
# Programa de Treinamento Shift Left

## Semana 1: Fundamentos (8h)
### Conteúdo
- [Tarefa] Defina tópicos

### Atividades Práticas
- [Tarefa] Defina exercícios

### Material
- [Tarefa] Liste recursos

## Semana 2: TDD e Testes Unitários (10h)
### Conteúdo
...

## Semana 3: CI/CD e Automação (10h)
### Conteúdo
...

## Semana 4: Práticas Avançadas (8h)
### Conteúdo
...

## Semana 5: Projeto Final (4h)
### Desafio
...
```

**Suas Tarefas:**
1. Detalhes completo do programa de 40 horas
2. Crie material de cada semana (slides, exercícios)
3. Defina critérios de avaliação
4. Planeje projeto final hands-on
5. Calcule ROI esperado do treinamento

---

### Exercício 5.4: Implementação Completa End-to-End 🔴 (Nível 4)

**Objetivo:** Implementar Shift Left completo em projeto real.

**Contexto:**  
Este é o exercício final e mais complexo. Você implementará Shift Left do zero em um projeto real (pode ser o CNPJ-QA-Training ou projeto próprio).

**Requisitos Completos:**

**1. Testes (70 pontos)**
- [ ] Testes unitários com cobertura > 80%
- [ ] Testes de integração
- [ ] Testes E2E para fluxos críticos
- [ ] Testes de performance
- [ ] Testes de segurança (SAST)
- [ ] Testes de contrato (API)

**2. CI/CD (100 pontos)**
- [ ] Pipeline completo (build, test, deploy)
- [ ] Múltiplos ambientes (dev, staging, prod)
- [ ] Deploy automático
- [ ] Rollback automático
- [ ] Notificações (Slack/email)
- [ ] Métricas e dashboards

**3. Qualidade de Código (50 pontos)**
- [ ] Pre-commit hooks configurados
- [ ] Linting rigoroso
- [ ] Code coverage tracking
- [ ] Dependency scanning
- [ ] Code review checklist

**4. Documentação (30 pontos)**
- [ ] README com instruções claras
- [ ] Guia de contribuição
- [ ] Architecture Decision Records (ADRs)
- [ ] Runbooks operacionais

**5. Cultura (50 pontos)**
- [ ] Definition of Done com testes
- [ ] Retrospectivas com foco em qualidade
- [ ] Pair programming sessions
- [ ] Knowledge sharing (demos, workshops)

**Entrega:**
- Repositório GitHub completo
- Vídeo demo (10 min)
- Apresentação de resultados (métricas antes/depois)
- Lições aprendidas (post-mortem)

**Critérios de Avaliação:**
- Funcionalidade: 30%
- Testes: 25%
- CI/CD: 20%
- Qualidade: 15%
- Documentação: 10%

**Tempo estimado:** 40-60 horas

---

## 📊 Checklist de Progresso

### Bloco 1: Fundamentos ✅
- [ ] Exercício 1.1: Identificando Shift Left (Nível 1)
- [ ] Exercício 1.2: Calculando ROI (Nível 2)
- [ ] Exercício 1.3: Test Pyramid (Nível 3)
- [ ] Exercício 1.4: Critérios Testáveis (Nível 4)

### Bloco 2: Testes Unitários e TDD ✅
- [ ] Exercício 2.1: Primeiro Teste (Nível 1)
- [ ] Exercício 2.2: TDD Red-Green-Refactor (Nível 2)
- [ ] Exercício 2.3: Edge Cases (Nível 3)
- [ ] Exercício 2.4: Mocking (Nível 4)

### Bloco 3: CI/CD ✅
- [ ] Exercício 3.1: Pre-commit Hooks (Nível 1)
- [ ] Exercício 3.2: Pipeline CI (Nível 2)
- [ ] Exercício 3.3: Paralelização (Nível 3)
- [ ] Exercício 3.4: Rollback Automático (Nível 4)

### Bloco 4: Práticas Avançadas ✅
- [ ] Exercício 4.1: Security Testing (Nível 1)
- [ ] Exercício 4.2: Test Data Management (Nível 2)
- [ ] Exercício 4.3: Performance Testing (Nível 3)
- [ ] Exercício 4.4: Chaos Engineering (Nível 4)

### Bloco 5: Implementação Real ✅
- [ ] Exercício 5.1: Planejamento (Nível 1)
- [ ] Exercício 5.2: Code Review Checklist (Nível 2)
- [ ] Exercício 5.3: Treinamento (Nível 3)
- [ ] Exercício 5.4: Implementação Completa (Nível 4)

---

## 🎯 Próximos Passos

Após completar estes exercícios:

1. **Revise o Gabarito** (shift-left-testing-gabarito.md)
2. **Compare suas soluções** com as respostas detalhadas
3. **Implemente em projeto real** usando conhecimento adquirido
4. **Compartilhe aprendizados** com seu time
5. **Mentore outros** na jornada de Shift Left

---

## 💡 Dicas de Estudo

**Para Iniciantes:**
- Não pule níveis, a progressão é intencional
- Faça hands-on, não apenas leia
- Use o gabarito após suas tentativas
- Peça ajuda quando travar

**Para Intermediários:**
- Tente resolver Nível 3-4 antes de ver gabarito
- Experimente abordagens diferentes
- Compare com soluções da comunidade
- Contribua com melhorias

**Para Avançados:**
- Foque em Exercício 5.4 (implementação completa)
- Mentore iniciantes
- Contribua com novos exercícios
- Compartilhe case studies

---

**Versão:** 1.0  
**Última Atualização:** 2024  
**Autor:** Material de Treinamento QA Profissional  
**Licença:** MIT - Uso Educacional

---

> 💡 **Lembre-se**: A prática leva à perfeição. Cada exercício é uma oportunidade de internalizar conceitos de Shift Left Testing. Não tenha pressa, mas seja consistente!

**Bons estudos e mãos à obra! 🚀**
