# Arquitetura do Projeto CNPJ-QA-Training

## Visão Geral

O CNPJ-QA-Training é um sistema de validação de CNPJ desenvolvido com arquitetura modular, focado em:

1. **Separação de responsabilidades** - Cada módulo tem função específica
2. **Testabilidade** - Código facilmente testável em isolamento
3. **Extensibilidade** - Fácil adicionar novos validadores ou provedores de API
4. **Propósito pedagógico** - Estrutura clara para aprendizado

---

## Estrutura em Camadas

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFACES (Apresentação)                │
│                  examples/, scripts/, API                   │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                   CORE (Lógica de Negócio)                  │
│                src/cnpj_validator/cnpj_validator.py         │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                 VALIDATORS (Validação Especializada)        │
│          src/cnpj_validator/validators/*.py                 │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│               INFRASTRUCTURE (Serviços Externos)            │
│           src/cnpj_validator/receita_federal_api.py         │
└─────────────────────────────────────────────────────────────┘
```

---

## Mapeamento de Diretórios

| Camada | Diretório | Responsabilidade |
|--------|-----------|------------------|
| **Interfaces** | `examples/` | Exemplos de uso para desenvolvedores |
| **Interfaces** | `scripts/` | Automação de tarefas (testes, build) |
| **Interfaces** | `src/api/` | API HTTP (FastAPI) |
| **Core** | `src/cnpj_validator/cnpj_validator.py` | Orquestração da validação |
| **Validators** | `src/cnpj_validator/validators/` | Validadores especializados |
| **Infrastructure** | `src/cnpj_validator/receita_federal_api.py` | Cliente API externa |
| **Tests** | `tests/` | Testes unitários e de integração |
| **Docs** | `docs/` | Documentação técnica e pedagógica |

---

## Componentes Principais

### 1. CNPJValidator (Facade)

**Arquivo:** `src/cnpj_validator/cnpj_validator.py`

Classe principal que orquestra a validação combinando os validadores especializados.

```python
class CNPJValidator:
    """
    Validador principal de CNPJ.
    
    Combina validação numérica e alfanumérica em uma interface unificada.
    """
    
    def __init__(self):
        self.numeric_validator = NumericCNPJValidator()
        self.alphanumeric_validator = AlphanumericCNPJValidator()
    
    def validate(self, cnpj: str) -> dict:
        """Executa validação completa."""
        pass
    
    @staticmethod
    def is_valid(cnpj: str) -> bool:
        """Validação rápida (método estático)."""
        pass
```

**Padrão utilizado:** Facade Pattern - simplifica a interface para o usuário final.

### 2. NumericCNPJValidator

**Arquivo:** `src/cnpj_validator/validators/numeric_validator.py`

Responsável pela validação matemática do CNPJ:

- Remoção de formatação
- Validação de tamanho (14 dígitos)
- Detecção de CNPJs inválidos (todos iguais)
- Cálculo de dígitos verificadores (Módulo 11)

```python
class NumericCNPJValidator:
    """Validador numérico de CNPJ."""
    
    WEIGHTS_FIRST = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    WEIGHTS_SECOND = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    def validate(self, cnpj: str) -> dict:
        pass
    
    def calculate_check_digits(self, cnpj_base: str) -> tuple:
        pass
```

### 3. AlphanumericCNPJValidator

**Arquivo:** `src/cnpj_validator/validators/alphanumeric_validator.py`

Responsável pela validação de formato:

- Padrão XX.XXX.XXX/XXXX-XX
- Caracteres permitidos
- Identificação matriz/filial
- Extração de componentes

```python
class AlphanumericCNPJValidator:
    """Validador alfanumérico de CNPJ."""
    
    PATTERN = r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$'
    
    def validate(self, cnpj: str) -> dict:
        pass
    
    def get_info(self, cnpj: str) -> dict:
        pass
```

### 4. ReceitaFederalAPI

**Arquivo:** `src/cnpj_validator/receita_federal_api.py`

Cliente para consulta de dados cadastrais em APIs públicas:

```python
class ReceitaFederalAPI:
    """Cliente para API da Receita Federal."""
    
    PROVIDERS = {
        'brasilapi': 'https://brasilapi.com.br/api/cnpj/v1/',
        'receitaws': 'https://receitaws.com.br/v1/cnpj/'
    }
    
    def consultar(self, cnpj: str) -> CNPJData:
        """Consulta dados completos do CNPJ."""
        pass
    
    def verificar_situacao(self, cnpj: str) -> str:
        """Retorna apenas situação cadastral."""
        pass
```

**Características:**
- Múltiplos provedores com fallback
- Rate limiting automático
- Retry com backoff exponencial
- Cache de resultados (opcional)

---

## Fluxo de Validação

```
                    ┌─────────────────┐
                    │  Input: CNPJ    │
                    │ "11.222.333/    │
                    │   0001-81"      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ CNPJValidator   │
                    │   .validate()   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │ Alphanumer │  │  Numeric   │  │  API Call  │
     │ Validator  │  │ Validator  │  │ (opcional) │
     └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
           │               │               │
           │  Formato OK?  │  DVs OK?      │  Dados?
           │               │               │
           └───────────────┼───────────────┘
                           │
                           ▼
                    ┌─────────────────┐
                    │   Resultado     │
                    │   Consolidado   │
                    └─────────────────┘
```

---

## Decisões Arquiteturais (ADRs)

### ADR-001: Separação de Validadores

**Contexto:** Necessidade de validar CNPJ em diferentes aspectos (formato e matemática).

**Decisão:** Criar validadores especializados independentes.

**Consequências:**
- ✅ Cada validador pode ser testado isoladamente
- ✅ Fácil adicionar novo tipo de validação
- ✅ Código mais legível e manutenível
- ⚠️ Pequena duplicação na limpeza de CNPJ

### ADR-002: Múltiplos Provedores de API

**Contexto:** APIs públicas podem ficar indisponíveis ou ter rate limiting.

**Decisão:** Implementar fallback entre BrasilAPI e ReceitaWS.

**Consequências:**
- ✅ Maior disponibilidade
- ✅ Redundância em caso de falha
- ⚠️ Complexidade adicional no código
- ⚠️ Necessidade de normalizar respostas diferentes

### ADR-003: Estrutura de Retorno Padronizada

**Contexto:** Diferentes validadores retornam informações distintas.

**Decisão:** Usar dicionário padronizado com campos consistentes.

```python
{
    'valid': bool,
    'cnpj_clean': str,
    'cnpj_formatted': str,
    'errors': list[str],
    'warnings': list[str],
    'info': dict  # informações adicionais
}
```

**Consequências:**
- ✅ Interface previsível para consumidores
- ✅ Fácil de serializar para JSON
- ✅ Extensível sem quebrar compatibilidade

### ADR-004: Propósito Pedagógico

**Contexto:** Projeto usado para treinamento de QAs.

**Decisão:** Priorizar legibilidade sobre otimização prematura.

**Consequências:**
- ✅ Código mais fácil de entender
- ✅ Bom para aprendizado
- ✅ Exemplos claros de boas práticas
- ⚠️ Pode não ser ideal para alto volume

---

## Testes

### Estrutura de Testes

```
tests/
├── __init__.py
├── test_numeric_validator.py      # Testes unitários - validador numérico
├── test_alphanumeric_validator.py # Testes unitários - validador alfanumérico
├── test_new_alphanumeric_validator.py # Testes do novo validador
├── test_integration.py            # Testes de integração
└── test_receita_federal_api.py    # Testes da API (mock)
```

### Pirâmide de Testes

```
         /\
        /  \  E2E (poucos)
       /    \  Testes manuais, CI/CD
      /──────\
     /        \  Integration (médios)
    /          \  test_integration.py
   /────────────\
  /              \  Unit (muitos)
 /                \  test_*_validator.py
/──────────────────\
```

### Cobertura Alvo

| Componente | Cobertura Mínima |
|------------|------------------|
| Validators | 95% |
| CNPJValidator | 90% |
| ReceitaFederalAPI | 80% (com mocks) |
| Utils | 85% |

---

## Extensibilidade

### Adicionar Novo Validador

1. Criar arquivo em `src/cnpj_validator/validators/`
2. Implementar interface padrão:

```python
class NovoValidator:
    def validate(self, cnpj: str) -> dict:
        return {
            'valid': bool,
            'errors': list,
            # campos específicos
        }
```

3. Integrar no `CNPJValidator` principal
4. Adicionar testes em `tests/`

### Adicionar Novo Provedor de API

1. Adicionar URL em `ReceitaFederalAPI.PROVIDERS`
2. Implementar método de parsing para resposta
3. Adicionar ao fallback chain
4. Testar com mocks

---

## Referências

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Facade Pattern](https://refactoring.guru/design-patterns/facade)
- [Keep a Changelog](https://keepachangelog.com/)
