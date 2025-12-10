# Guia de Contribuição

Obrigado por considerar contribuir para o **CNPJ-QA-Training**! Este documento fornece diretrizes para contribuir com código, documentação e melhorias.

## Índice

1. [Código de Conduta](#código-de-conduta)
2. [Como Contribuir](#como-contribuir)
3. [Configuração do Ambiente](#configuração-do-ambiente)
4. [Padrões de Código](#padrões-de-código)
5. [Processo de Pull Request](#processo-de-pull-request)
6. [Convenções de Commit](#convenções-de-commit)

---

## Código de Conduta

### Nossa Responsabilidade

Mantemos um ambiente inclusivo e respeitoso. Esperamos que todos os participantes:

- Sejam respeitosos com diferentes opiniões e experiências
- Aceitem críticas construtivas
- Foquem no que é melhor para a comunidade
- Mostrem empatia com outros membros

### Comportamentos Inaceitáveis

- Linguagem ou imagens ofensivas
- Trolling ou comentários depreciativos
- Assédio público ou privado
- Compartilhar informações privadas de outros

---

## Como Contribuir

### Reportando Bugs

Antes de criar um relatório de bug:

1. Verifique a [lista de issues](https://github.com/RaFeltrim/CNPJ-QA-Training/issues) existentes
2. Se o bug já foi reportado, adicione um comentário ao invés de abrir novo issue

**Ao reportar um bug, inclua:**

- Título descritivo
- Passos para reproduzir o problema
- Comportamento esperado vs. observado
- Versão do Python utilizada
- Sistema operacional
- Logs ou screenshots relevantes

### Sugerindo Melhorias

1. Use um título claro e descritivo
2. Descreva a melhoria em detalhes
3. Explique por que seria útil para o projeto
4. Liste exemplos de uso, se aplicável

### Contribuindo com Código

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente a mudança
4. Adicione/atualize testes
5. Atualize documentação se necessário
6. Abra um Pull Request

---

## Configuração do Ambiente

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)
- Git

### Setup Local

```bash
# 1. Clone seu fork
git clone https://github.com/SEU-USUARIO/CNPJ-QA-Training.git
cd CNPJ-QA-Training

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Instale dependências de desenvolvimento
pip install pytest pytest-cov black flake8

# 5. Instale o pacote em modo desenvolvimento
pip install -e .

# 6. Execute os testes para verificar o setup
pytest tests/ -v
```

---

## Padrões de Código

### Python

Seguimos as convenções PEP 8 com algumas adaptações:

```python
# Classes: PascalCase
class CNPJValidator:
    pass

class NumericCNPJValidator:
    pass

# Funções e métodos: snake_case
def validate_cnpj(cnpj: str) -> bool:
    pass

def calculate_check_digit(numbers: list) -> int:
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Variáveis: snake_case
cnpj_clean = "11222333000181"
is_valid = True
```

### Docstrings

Use docstrings em todas as funções públicas:

```python
def validate(self, cnpj: str) -> dict:
    """
    Valida um CNPJ completo.

    Args:
        cnpj: CNPJ a ser validado (com ou sem formatação)

    Returns:
        dict: Resultado da validação contendo:
            - valid (bool): Se o CNPJ é válido
            - cnpj_clean (str): CNPJ sem formatação
            - errors (list): Lista de erros encontrados

    Raises:
        ValueError: Se o CNPJ estiver vazio

    Example:
        >>> validator = CNPJValidator()
        >>> result = validator.validate("11.222.333/0001-81")
        >>> print(result['valid'])
        True
    """
```

### Estrutura de Arquivos

```
src/cnpj_validator/
├── __init__.py           # Exports públicos
├── cnpj_validator.py     # Validador principal
├── receita_federal_api.py # Cliente API
└── validators/
    ├── __init__.py
    ├── numeric_validator.py      # snake_case
    └── alphanumeric_validator.py # snake_case
```

### Nomenclatura de Arquivos

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Módulos Python | `snake_case.py` | `numeric_validator.py` |
| Testes | `test_*.py` | `test_numeric_validator.py` |
| Documentação | `kebab-case.md` | `guia-completo-cnpj.md` |
| Scripts | `kebab-case` | `run-tests.sh` |

---

## Processo de Pull Request

### 1. Criar Branch

```bash
# Atualize a master
git checkout master
git pull origin master

# Crie uma branch descritiva
git checkout -b feat/nova-funcionalidade
# ou
git checkout -b fix/corrigir-bug
# ou
git checkout -b docs/atualizar-readme
```

**Convenção de branches:**

| Prefixo | Uso |
|---------|-----|
| `feat/` | Nova funcionalidade |
| `fix/` | Correção de bug |
| `docs/` | Documentação |
| `refactor/` | Refatoração |
| `test/` | Adição/modificação de testes |

### 2. Desenvolver

```bash
# Implemente sua mudança
# Escreva/atualize testes
# Atualize documentação

# Verifique qualidade
flake8 src/ tests/
pytest tests/ -v --cov=src/cnpj_validator
```

### 3. Commit

```bash
git add .
git commit -m "feat: adicionar validação de CNPJ alfanumérico"
```

### 4. Push e PR

```bash
git push origin feat/nova-funcionalidade
```

Depois, abra um Pull Request no GitHub.

### 5. Checklist do PR

Antes de submeter, verifique:

- [ ] Código segue os padrões do projeto
- [ ] Testes passam: `pytest tests/ -v`
- [ ] Cobertura de testes adequada
- [ ] Documentação atualizada (se aplicável)
- [ ] Commits têm mensagens claras
- [ ] Sem conflitos com a branch master

---

## Convenções de Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

### Tipos

| Tipo | Descrição |
|------|-----------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação (sem mudança de código) |
| `refactor` | Refatoração |
| `test` | Adição/modificação de testes |
| `ci` | Mudanças em CI/CD |
| `chore` | Tarefas de manutenção |

### Exemplos

```bash
# Simples
git commit -m "feat: adicionar validação de CNPJ alfanumérico"

# Com escopo
git commit -m "fix(api): corrigir timeout na consulta Receita Federal"

# Com corpo explicativo
git commit -m "refactor: reorganizar estrutura de validadores

Separar validação numérica e alfanumérica em módulos distintos
para melhor manutenibilidade e testabilidade.

Closes #42"
```

---

## Testes

### Executar Testes

```bash
# Todos os testes
pytest tests/ -v

# Com cobertura
pytest tests/ -v --cov=src/cnpj_validator --cov-report=html

# Testes específicos
pytest tests/test_numeric_validator.py -v

# Testes por marcador
pytest -m "unit" -v
pytest -m "integration" -v
```

### Escrever Testes

```python
import pytest
from src.cnpj_validator import CNPJValidator

class TestCNPJValidator:
    """Testes para o validador principal de CNPJ."""

    def test_validate_valid_cnpj(self):
        """Deve validar CNPJ com formato correto."""
        validator = CNPJValidator()
        result = validator.validate("11.222.333/0001-81")
        
        assert result['valid'] is True
        assert result['cnpj_clean'] == "11222333000181"

    def test_validate_invalid_cnpj(self):
        """Deve rejeitar CNPJ com dígitos verificadores incorretos."""
        validator = CNPJValidator()
        result = validator.validate("11.222.333/0001-99")
        
        assert result['valid'] is False
        assert len(result['errors']) > 0
```

---

## Dúvidas?

- Abra uma [Discussion](https://github.com/RaFeltrim/CNPJ-QA-Training/discussions)
- Consulte a [documentação](./docs/README.md)
- Verifique os [issues existentes](https://github.com/RaFeltrim/CNPJ-QA-Training/issues)

---

Obrigado por contribuir! 🎯
