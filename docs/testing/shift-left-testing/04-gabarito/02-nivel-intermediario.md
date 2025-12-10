# 📝 Gabarito - Nível Intermediário

> **Exercícios 4-6** | Tempo de Revisão: ~45 minutos

---

## Exercício 4: Análise de Código Legado

### 📋 Enunciado Resumido
Analisar código legado do validador CNPJ e propor melhorias testáveis seguindo princípios Shift Left.

### ✅ Resposta Esperada

#### 4.1 Problemas Identificados

```python
# CÓDIGO ORIGINAL (problemático)
def validate_cnpj(cnpj):
    # Problema 1: Sem validação de entrada
    # Problema 2: Lógica complexa em um único método
    # Problema 3: Sem tratamento de erros específicos
    # Problema 4: Sem documentação
    # Problema 5: Difícil de testar (alto acoplamento)
    
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    if len(cnpj) != 14:
        return False
    # ... mais lógica misturada
```

**Análise Detalhada**:

| # | Problema | Impacto | Princípio Shift Left Violado |
|---|----------|---------|------------------------------|
| 1 | Sem validação de entrada | Comportamento indefinido com None/tipos errados | Fail Fast |
| 2 | Função monolítica | Difícil testar partes isoladas | Testabilidade |
| 3 | Retorna apenas bool | Não informa qual problema ocorreu | Feedback Contínuo |
| 4 | Sem docstrings | Difícil entender comportamento esperado | Documentação |
| 5 | Acoplamento alto | Mudança em uma parte quebra outras | Modularidade |

#### 4.2 Código Refatorado

```python
"""
Módulo de validação de CNPJ com design testável.
Segue princípios Shift Left para facilitar testes automatizados.
"""
from dataclasses import dataclass
from typing import Union
from enum import Enum


class CNPJValidationError(Exception):
    """Exceção base para erros de validação de CNPJ."""
    pass


class ValidationResult(Enum):
    """Resultados possíveis da validação."""
    VALID = "valid"
    INVALID_FORMAT = "invalid_format"
    INVALID_LENGTH = "invalid_length"
    INVALID_DIGITS = "invalid_digits"
    INVALID_CHECKSUM = "invalid_checksum"


@dataclass
class CNPJValidationReport:
    """Relatório detalhado de validação."""
    is_valid: bool
    result: ValidationResult
    message: str
    original_input: str
    sanitized_input: str = ""
    
    def __bool__(self):
        return self.is_valid


class CNPJValidator:
    """
    Validador de CNPJ com design orientado a testes.
    
    Princípios aplicados:
    - Single Responsibility: cada método faz uma coisa
    - Fail Fast: validações na entrada
    - Feedback Rico: relatórios detalhados
    
    Exemplo:
        >>> validator = CNPJValidator()
        >>> result = validator.validate("11.222.333/0001-81")
        >>> print(result.is_valid)
        True
    """
    
    # Constantes para facilitar testes
    CNPJ_LENGTH = 14
    FIRST_MULTIPLIERS = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    SECOND_MULTIPLIERS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    def validate(self, cnpj: Union[str, None]) -> CNPJValidationReport:
        """
        Valida um CNPJ e retorna relatório detalhado.
        
        Args:
            cnpj: String contendo CNPJ (com ou sem formatação)
            
        Returns:
            CNPJValidationReport com resultado detalhado
            
        Raises:
            CNPJValidationError: Se input for None ou tipo inválido
        """
        # Fail Fast: validação de entrada
        if cnpj is None:
            raise CNPJValidationError("CNPJ não pode ser None")
        
        if not isinstance(cnpj, str):
            raise CNPJValidationError(f"CNPJ deve ser string, recebido {type(cnpj)}")
        
        original = cnpj
        
        # Etapa 1: Sanitização
        sanitized = self._sanitize(cnpj)
        
        # Etapa 2: Validação de formato
        format_result = self._validate_format(sanitized)
        if format_result:
            return CNPJValidationReport(
                is_valid=False,
                result=format_result,
                message=self._get_message(format_result),
                original_input=original,
                sanitized_input=sanitized
            )
        
        # Etapa 3: Validação de dígitos verificadores
        if not self._validate_check_digits(sanitized):
            return CNPJValidationReport(
                is_valid=False,
                result=ValidationResult.INVALID_CHECKSUM,
                message="Dígitos verificadores inválidos",
                original_input=original,
                sanitized_input=sanitized
            )
        
        # Sucesso
        return CNPJValidationReport(
            is_valid=True,
            result=ValidationResult.VALID,
            message="CNPJ válido",
            original_input=original,
            sanitized_input=sanitized
        )
    
    def _sanitize(self, cnpj: str) -> str:
        """Remove caracteres não numéricos."""
        return ''.join(c for c in cnpj if c.isdigit())
    
    def _validate_format(self, cnpj: str) -> Union[ValidationResult, None]:
        """Valida formato do CNPJ sanitizado."""
        if len(cnpj) != self.CNPJ_LENGTH:
            return ValidationResult.INVALID_LENGTH
        
        if not cnpj.isdigit():
            return ValidationResult.INVALID_DIGITS
        
        # CNPJs com todos dígitos iguais são inválidos
        if len(set(cnpj)) == 1:
            return ValidationResult.INVALID_FORMAT
        
        return None  # Formato OK
    
    def _validate_check_digits(self, cnpj: str) -> bool:
        """Valida os dois dígitos verificadores."""
        first_digit = self._calculate_digit(cnpj[:12], self.FIRST_MULTIPLIERS)
        second_digit = self._calculate_digit(cnpj[:13], self.SECOND_MULTIPLIERS)
        
        return cnpj[12] == str(first_digit) and cnpj[13] == str(second_digit)
    
    def _calculate_digit(self, base: str, multipliers: list) -> int:
        """Calcula um dígito verificador."""
        total = sum(int(d) * m for d, m in zip(base, multipliers))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    def _get_message(self, result: ValidationResult) -> str:
        """Retorna mensagem amigável para cada tipo de erro."""
        messages = {
            ValidationResult.INVALID_FORMAT: "Formato de CNPJ inválido",
            ValidationResult.INVALID_LENGTH: f"CNPJ deve ter {self.CNPJ_LENGTH} dígitos",
            ValidationResult.INVALID_DIGITS: "CNPJ deve conter apenas dígitos",
            ValidationResult.INVALID_CHECKSUM: "Dígitos verificadores inválidos",
        }
        return messages.get(result, "Erro desconhecido")
```

#### 4.3 Testes para Código Refatorado

```python
import pytest
from cnpj_validator_refactored import (
    CNPJValidator, 
    CNPJValidationError,
    ValidationResult
)


class TestCNPJValidatorSanitize:
    """Testes isolados para o método _sanitize."""
    
    @pytest.fixture
    def validator(self):
        return CNPJValidator()
    
    def test_sanitize_remove_pontuacao(self, validator):
        assert validator._sanitize("11.222.333/0001-81") == "11222333000181"
    
    def test_sanitize_mantem_numeros(self, validator):
        assert validator._sanitize("11222333000181") == "11222333000181"
    
    def test_sanitize_remove_espacos(self, validator):
        assert validator._sanitize(" 11 222 333 ") == "11222333"


class TestCNPJValidatorFormat:
    """Testes isolados para validação de formato."""
    
    @pytest.fixture
    def validator(self):
        return CNPJValidator()
    
    def test_format_tamanho_correto_retorna_none(self, validator):
        assert validator._validate_format("11222333000181") is None
    
    def test_format_tamanho_incorreto_retorna_erro(self, validator):
        result = validator._validate_format("1122233300018")  # 13 dígitos
        assert result == ValidationResult.INVALID_LENGTH
    
    def test_format_digitos_iguais_retorna_erro(self, validator):
        result = validator._validate_format("11111111111111")
        assert result == ValidationResult.INVALID_FORMAT


class TestCNPJValidatorCheckDigits:
    """Testes isolados para cálculo de dígitos verificadores."""
    
    @pytest.fixture
    def validator(self):
        return CNPJValidator()
    
    def test_calcula_primeiro_digito(self, validator):
        # CNPJ: 11.222.333/0001-81
        # Primeiro dígito verificador: 8
        digito = validator._calculate_digit("112223330001", validator.FIRST_MULTIPLIERS)
        assert digito == 8
    
    def test_calcula_segundo_digito(self, validator):
        # CNPJ: 11.222.333/0001-81
        # Segundo dígito verificador: 1
        digito = validator._calculate_digit("1122233300018", validator.SECOND_MULTIPLIERS)
        assert digito == 1
    
    def test_validate_check_digits_valido(self, validator):
        assert validator._validate_check_digits("11222333000181") is True
    
    def test_validate_check_digits_invalido(self, validator):
        assert validator._validate_check_digits("11222333000182") is False


class TestCNPJValidatorIntegration:
    """Testes de integração do validador completo."""
    
    @pytest.fixture
    def validator(self):
        return CNPJValidator()
    
    def test_cnpj_valido_retorna_report_positivo(self, validator):
        result = validator.validate("11.222.333/0001-81")
        
        assert result.is_valid is True
        assert result.result == ValidationResult.VALID
        assert bool(result) is True
    
    def test_cnpj_invalido_retorna_report_negativo(self, validator):
        result = validator.validate("11.222.333/0001-82")
        
        assert result.is_valid is False
        assert result.result == ValidationResult.INVALID_CHECKSUM
        assert bool(result) is False
    
    def test_cnpj_none_levanta_excecao(self, validator):
        with pytest.raises(CNPJValidationError) as exc:
            validator.validate(None)
        assert "None" in str(exc.value)
    
    def test_cnpj_tipo_errado_levanta_excecao(self, validator):
        with pytest.raises(CNPJValidationError) as exc:
            validator.validate(12345)
        assert "string" in str(exc.value)
    
    @pytest.mark.parametrize("cnpj,expected_valid", [
        ("11.222.333/0001-81", True),
        ("11222333000181", True),
        ("00.000.000/0001-91", True),
        ("11.222.333/0001-82", False),  # Dígito errado
        ("11111111111111", False),       # Dígitos iguais
        ("1234567890123", False),        # Tamanho errado
    ])
    def test_diversos_cnpjs(self, validator, cnpj, expected_valid):
        result = validator.validate(cnpj)
        assert result.is_valid == expected_valid
```

### 💡 Por Que Funciona

**1. Separação de Responsabilidades**
- Cada método privado faz UMA coisa
- Facilita testar cada parte isoladamente
- Mudança em uma parte não quebra outras

**2. Fail Fast**
- Exceções explícitas para entradas inválidas
- Não tenta processar dados ruins
- Feedback imediato

**3. Rich Feedback**
- `ValidationResult` enum com todos os casos
- `CNPJValidationReport` com contexto completo
- Mensagens amigáveis para debug

**4. Testabilidade**
- Métodos públicos e privados testáveis
- Fixtures simplificam setup
- Parametrização cobre muitos casos

### ⚠️ Erros Comuns

1. **Refatorar sem testes primeiro**
   - Sempre escreva testes ANTES de refatorar
   - Garante que comportamento é preservado

2. **Over-engineering**
   - Não precisa de 10 classes para um validador simples
   - Balance entre testabilidade e complexidade

3. **Ignorar casos de borda**
   - None, string vazia, tipos errados
   - CNPJs com todos dígitos iguais

4. **Testes muito acoplados à implementação**
   - Testar comportamento, não implementação
   - Se método interno muda, teste não deveria quebrar

### 🔄 Alternativas Aceitáveis

- Usar funções ao invés de classe (programação funcional)
- Retornar tupla (bool, mensagem) ao invés de dataclass
- Usar validação com decorators
- Implementar como pipeline de validações

### 📚 Conexão com a Teoria

- [03-como-funciona.md](../02-guia-teorico/03-como-funciona.md) - Design Testável
- [04-como-aplicar.md](../02-guia-teorico/04-como-aplicar.md) - Refatoração

### 🎯 Pontos de Discussão

1. "Como decidir quando uma função está grande demais?"
2. "Testar métodos privados é boa prática?"
3. "Exceção vs retorno de erro - quando usar cada um?"

---

## Exercício 5: Estratégia de Integração

### 📋 Enunciado Resumido
Desenhar estratégia de testes de integração para comunicação entre validador CNPJ e API da Receita Federal.

### ✅ Resposta Esperada

#### 5.1 Arquitetura de Testes

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIRÂMIDE DE TESTES - INTEGRAÇÃO              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                         ┌─────────┐                              │
│                         │   E2E   │  (Poucos, Lentos, Caros)    │
│                         │ Receita │                              │
│                       ┌─┴─────────┴─┐                            │
│                       │ Integração  │  ← FOCO DESTE EXERCÍCIO   │
│                       │   Mock API  │                            │
│                     ┌─┴─────────────┴─┐                          │
│                     │   Contrato API   │  (Validam interface)    │
│                   ┌─┴─────────────────┴─┐                        │
│                   │    Unitários CNPJ    │  (Muitos, Rápidos)    │
│                   └─────────────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.2 Níveis de Teste

| Nível | Propósito | Velocidade | Dependências |
|-------|-----------|------------|--------------|
| Unitário | Lógica de validação | < 100ms | Nenhuma |
| Contrato | Interface da API | < 500ms | Schema JSON |
| Integração (Mock) | Fluxo completo | < 2s | Mock server |
| E2E (Real) | Validação real | < 10s | API Receita |

#### 5.3 Implementação com Mocks

```python
"""
Testes de integração com mock da API da Receita Federal.
Usa responses para simular respostas HTTP sem chamar API real.
"""
import pytest
import responses
from cnpj_validator import CNPJService


class TestCNPJServiceIntegration:
    """Testes de integração do serviço CNPJ."""
    
    BASE_URL = "https://receitaws.com.br/v1/cnpj"
    
    @pytest.fixture
    def service(self):
        return CNPJService()
    
    # --- Cenário de Sucesso ---
    
    @responses.activate
    def test_consulta_cnpj_existente(self, service):
        """CNPJ válido e existente retorna dados da empresa."""
        # Arrange: Mock da API
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json={
                "cnpj": "11.222.333/0001-81",
                "nome": "EMPRESA TESTE LTDA",
                "situacao": "ATIVA",
                "tipo": "MATRIZ"
            },
            status=200
        )
        
        # Act
        result = service.consultar("11222333000181")
        
        # Assert
        assert result.cnpj == "11.222.333/0001-81"
        assert result.nome == "EMPRESA TESTE LTDA"
        assert result.situacao == "ATIVA"
    
    # --- Cenários de Erro ---
    
    @responses.activate
    def test_consulta_cnpj_inexistente(self, service):
        """CNPJ inexistente retorna erro 404."""
        # Arrange
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/99999999999999",
            json={"message": "CNPJ não encontrado"},
            status=404
        )
        
        # Act & Assert
        with pytest.raises(CNPJNotFoundError):
            service.consultar("99999999999999")
    
    @responses.activate
    def test_api_timeout(self, service):
        """Timeout da API é tratado graciosamente."""
        # Arrange: Simula timeout
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            body=requests.exceptions.Timeout()
        )
        
        # Act & Assert
        with pytest.raises(APITimeoutError) as exc:
            service.consultar("11222333000181")
        
        assert "timeout" in str(exc.value).lower()
    
    @responses.activate
    def test_api_rate_limit(self, service):
        """Rate limit (429) ativa retry com backoff."""
        # Arrange: Primeiro retorna 429, depois 200
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json={"message": "Rate limit exceeded"},
            status=429
        )
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json={"cnpj": "11.222.333/0001-81", "nome": "EMPRESA"},
            status=200
        )
        
        # Act
        result = service.consultar("11222333000181")
        
        # Assert
        assert result.cnpj == "11.222.333/0001-81"
        assert len(responses.calls) == 2  # Fez retry
    
    @responses.activate
    def test_resposta_malformada(self, service):
        """JSON inválido é tratado."""
        # Arrange
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            body="not json",
            status=200
        )
        
        # Act & Assert
        with pytest.raises(InvalidResponseError):
            service.consultar("11222333000181")


class TestCNPJServiceContract:
    """Testes de contrato - validam schema da resposta."""
    
    @responses.activate
    def test_resposta_contem_campos_obrigatorios(self, service):
        """Resposta da API deve conter campos obrigatórios."""
        # Schema esperado
        required_fields = ["cnpj", "nome", "situacao", "tipo"]
        
        responses.add(
            responses.GET,
            f"{TestCNPJServiceIntegration.BASE_URL}/11222333000181",
            json={
                "cnpj": "11.222.333/0001-81",
                "nome": "EMPRESA",
                "situacao": "ATIVA",
                "tipo": "MATRIZ",
                # Campos extras são OK
                "extra": "ignorado"
            },
            status=200
        )
        
        result = service.consultar("11222333000181")
        
        for field in required_fields:
            assert hasattr(result, field), f"Campo {field} ausente"
```

#### 5.4 Configuração do Mock Server

```python
# conftest.py - Fixtures compartilhadas

import pytest
import responses

@pytest.fixture
def mock_api():
    """Ativa mocking de respostas HTTP."""
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.fixture
def mock_api_success(mock_api):
    """Mock pré-configurado para sucesso."""
    mock_api.add(
        responses.GET,
        "https://receitaws.com.br/v1/cnpj/11222333000181",
        json={
            "cnpj": "11.222.333/0001-81",
            "nome": "EMPRESA TESTE LTDA",
            "situacao": "ATIVA",
            "tipo": "MATRIZ"
        },
        status=200
    )
    return mock_api
```

#### 5.5 Estratégia de Execução

```yaml
# .github/workflows/integration-tests.yml

integration-tests:
  runs-on: ubuntu-latest
  
  strategy:
    matrix:
      test-type: [mock, contract]
      include:
        - test-type: mock
          markers: "integration and not e2e"
        - test-type: contract  
          markers: "contract"
  
  steps:
    - name: Run Integration Tests
      run: |
        pytest tests/integration/ \
          -m "${{ matrix.markers }}" \
          --tb=short \
          -v

# Testes E2E rodam apenas em schedule (não em cada PR)
e2e-tests:
  runs-on: ubuntu-latest
  if: github.event_name == 'schedule'
  
  steps:
    - name: Run E2E Tests
      env:
        RECEITA_API_KEY: ${{ secrets.RECEITA_API_KEY }}
      run: |
        pytest tests/e2e/ -m "e2e" --tb=long
```

### 💡 Por Que Funciona

**1. Isolamento com Mocks**
- Testes não dependem de API externa
- Rodam offline e em qualquer ambiente
- Controlamos exatamente o comportamento

**2. Cobertura de Cenários**
- Sucesso, erro 404, timeout, rate limit, JSON inválido
- Impossível testar todos estes cenários com API real

**3. Velocidade**
- Mocks respondem instantaneamente
- Pipeline rápido = feedback rápido

**4. Testes de Contrato**
- Garantem que nossa expectativa da API está correta
- Falham se API mudar (cedo)

### ⚠️ Erros Comuns

1. **Mocks muito específicos**
   - Se mock é cópia exata da API, qualquer mudança quebra
   - Mock deve capturar essência, não detalhes

2. **Não testar cenários de erro**
   - 90% dos bugs estão em error handling
   - API sempre pode falhar de formas inesperadas

3. **Confundir mock com stub**
   - Mock: verifica interações (foi chamado com X?)
   - Stub: retorna valor fixo
   - Use o correto para cada caso

4. **Testes E2E demais**
   - Caros, lentos, flaky
   - Use para smoke tests apenas

### 🔄 Alternativas Aceitáveis

- Usar `httpretty` ou `vcr.py` ao invés de `responses`
- WireMock para mock server mais robusto
- Pact para testes de contrato consumer-driven

### 📚 Conexão com a Teoria

- [03-como-funciona.md](../02-guia-teorico/03-como-funciona.md) - Pirâmide de Testes
- [04-como-aplicar.md](../02-guia-teorico/04-como-aplicar.md) - Estratégias de Mocking

### 🎯 Pontos de Discussão

1. "Quando usar mock vs API real?"
2. "Como manter mocks sincronizados com API real?"
3. "Testes de contrato são responsabilidade de quem?"

---

## Exercício 6: Métricas e Monitoramento

### 📋 Enunciado Resumido
Definir métricas para medir efetividade de Shift Left no projeto CNPJ.

### ✅ Resposta Esperada

#### 6.1 Framework de Métricas

```
┌─────────────────────────────────────────────────────────────────┐
│                    MÉTRICAS SHIFT LEFT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   LEADING (Preditivas)          LAGGING (Resultados)            │
│   ┌─────────────────────┐       ┌─────────────────────┐         │
│   │ • Cobertura código  │       │ • Bugs em produção  │         │
│   │ • Testes por commit │  ──▶  │ • MTTR (tempo fix)  │         │
│   │ • Tempo de build    │       │ • Custo de defeitos │         │
│   │ • Review coverage   │       │ • Satisfação user   │         │
│   └─────────────────────┘       └─────────────────────┘         │
│                                                                  │
│   PROCESSO                      QUALIDADE                        │
│   ┌─────────────────────┐       ┌─────────────────────┐         │
│   │ • Lead time         │       │ • Taxa de defeitos  │         │
│   │ • Cycle time        │       │ • Escape rate       │         │
│   │ • Deploy frequency  │       │ • Test pass rate    │         │
│   │ • Automation %      │       │ • Tech debt ratio   │         │
│   └─────────────────────┘       └─────────────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 6.2 Métricas Específicas

| Métrica | Fórmula | Meta | Frequência |
|---------|---------|------|------------|
| **Code Coverage** | Linhas testadas / Total linhas | ≥ 80% | Por commit |
| **Test Pass Rate** | Testes passando / Total testes | ≥ 95% | Por build |
| **Build Time** | Tempo total do pipeline | < 10 min | Por build |
| **Defect Escape Rate** | Bugs produção / Total bugs | < 10% | Semanal |
| **MTTR** | Tempo médio para corrigir | < 4h | Por incidente |
| **Lead Time** | Commit até produção | < 1 dia | Por deploy |

#### 6.3 Dashboard de Métricas

```python
"""
Coletor de métricas Shift Left para o projeto CNPJ.
Integra com GitHub Actions e gera relatórios.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict
import json


@dataclass
class ShiftLeftMetrics:
    """Container para métricas Shift Left."""
    
    # Cobertura
    line_coverage: float = 0.0
    branch_coverage: float = 0.0
    
    # Velocidade
    build_time_seconds: int = 0
    test_execution_time: int = 0
    
    # Qualidade
    tests_total: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    tests_skipped: int = 0
    
    # Defeitos
    bugs_found_dev: int = 0
    bugs_found_qa: int = 0
    bugs_found_prod: int = 0
    
    # Timestamps
    collected_at: datetime = field(default_factory=datetime.now)
    
    @property
    def test_pass_rate(self) -> float:
        """Taxa de testes passando."""
        if self.tests_total == 0:
            return 0.0
        return (self.tests_passed / self.tests_total) * 100
    
    @property
    def defect_escape_rate(self) -> float:
        """Taxa de defeitos que escaparam para produção."""
        total_bugs = self.bugs_found_dev + self.bugs_found_qa + self.bugs_found_prod
        if total_bugs == 0:
            return 0.0
        return (self.bugs_found_prod / total_bugs) * 100
    
    @property
    def shift_left_score(self) -> float:
        """
        Score composto de efetividade Shift Left (0-100).
        
        Componentes:
        - Cobertura (30%): 80%+ = máximo
        - Pass Rate (25%): 95%+ = máximo
        - Build Time (20%): <10min = máximo
        - Escape Rate (25%): <10% = máximo
        """
        coverage_score = min(self.line_coverage / 80, 1.0) * 30
        pass_rate_score = min(self.test_pass_rate / 95, 1.0) * 25
        
        # Build time: 10 min = 600s
        build_score = max(0, (600 - self.build_time_seconds) / 600) * 20
        
        # Escape rate: quanto menor, melhor
        escape_score = max(0, (100 - self.defect_escape_rate) / 90) * 25
        
        return coverage_score + pass_rate_score + build_score + escape_score
    
    def to_dict(self) -> Dict:
        """Converte para dicionário para exportação."""
        return {
            "coverage": {
                "line": self.line_coverage,
                "branch": self.branch_coverage
            },
            "tests": {
                "total": self.tests_total,
                "passed": self.tests_passed,
                "failed": self.tests_failed,
                "skipped": self.tests_skipped,
                "pass_rate": self.test_pass_rate
            },
            "performance": {
                "build_time_seconds": self.build_time_seconds,
                "test_time_seconds": self.test_execution_time
            },
            "quality": {
                "bugs_dev": self.bugs_found_dev,
                "bugs_qa": self.bugs_found_qa,
                "bugs_prod": self.bugs_found_prod,
                "escape_rate": self.defect_escape_rate
            },
            "score": {
                "shift_left_score": self.shift_left_score,
                "grade": self._get_grade()
            },
            "collected_at": self.collected_at.isoformat()
        }
    
    def _get_grade(self) -> str:
        """Retorna nota baseada no score."""
        score = self.shift_left_score
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        return "F"


class MetricsCollector:
    """Coleta métricas de várias fontes."""
    
    def __init__(self):
        self.metrics = ShiftLeftMetrics()
    
    def collect_from_pytest(self, report_path: str) -> None:
        """Coleta métricas do relatório pytest."""
        # Implementação lê coverage.xml e pytest report
        pass
    
    def collect_from_github(self, repo: str) -> None:
        """Coleta métricas do GitHub Actions."""
        # Implementação usa GitHub API
        pass
    
    def generate_report(self) -> str:
        """Gera relatório em formato markdown."""
        m = self.metrics
        
        report = f"""
# 📊 Relatório Shift Left - {m.collected_at.strftime('%Y-%m-%d')}

## Score Geral: {m.shift_left_score:.1f}/100 ({m._get_grade()})

### Cobertura de Código
| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Linhas | {m.line_coverage:.1f}% | 80% | {'✅' if m.line_coverage >= 80 else '⚠️'} |
| Branches | {m.branch_coverage:.1f}% | 70% | {'✅' if m.branch_coverage >= 70 else '⚠️'} |

### Execução de Testes
| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Total | {m.tests_total} | - | - |
| Passando | {m.tests_passed} ({m.test_pass_rate:.1f}%) | 95% | {'✅' if m.test_pass_rate >= 95 else '⚠️'} |
| Falhando | {m.tests_failed} | 0 | {'✅' if m.tests_failed == 0 else '❌'} |

### Performance
| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Build Time | {m.build_time_seconds}s | <600s | {'✅' if m.build_time_seconds < 600 else '⚠️'} |
| Test Time | {m.test_execution_time}s | <300s | {'✅' if m.test_execution_time < 300 else '⚠️'} |

### Qualidade
| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Escape Rate | {m.defect_escape_rate:.1f}% | <10% | {'✅' if m.defect_escape_rate < 10 else '❌'} |
| Bugs Dev | {m.bugs_found_dev} | - | ✅ (encontrados cedo) |
| Bugs Prod | {m.bugs_found_prod} | 0 | {'✅' if m.bugs_found_prod == 0 else '❌'} |

---
*Relatório gerado automaticamente pelo Shift Left Metrics Collector*
"""
        return report
```

#### 6.4 Integração com CI/CD

```yaml
# .github/workflows/metrics.yml

name: Collect Shift Left Metrics

on:
  workflow_run:
    workflows: ["CI/CD Pipeline"]
    types: [completed]

jobs:
  collect-metrics:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Download Artifacts
        uses: actions/download-artifact@v4
        with:
          name: coverage-report
          
      - name: Collect Metrics
        run: |
          python scripts/collect_metrics.py \
            --coverage coverage.xml \
            --output metrics.json
            
      - name: Update Dashboard
        run: |
          python scripts/update_dashboard.py \
            --metrics metrics.json \
            --output docs/metrics/latest.md
            
      - name: Check Thresholds
        run: |
          python scripts/check_thresholds.py \
            --metrics metrics.json \
            --fail-on-regression
```

### 💡 Por Que Funciona

**1. Métricas Balanceadas**
- Leading indicators preveem problemas
- Lagging indicators confirmam resultados
- Processo + Qualidade = visão completa

**2. Automação**
- Coleta automática = dados consistentes
- Sem trabalho manual = sustentável
- Integrado no pipeline = sempre atualizado

**3. Score Composto**
- Uma métrica não conta a história toda
- Score balanceado evita gaming
- Fácil de comunicar para gestão

**4. Thresholds Claros**
- Metas definidas = expectativas claras
- Alertas automáticos = ação rápida
- Tendências = melhoria contínua

### ⚠️ Erros Comuns

1. **Métricas demais**
   - Escolha 5-7 métricas principais
   - Mais que isso = paralisia por análise

2. **Otimizar métrica em vez de resultado**
   - 100% cobertura com testes ruins = inútil
   - Métricas são proxies, não objetivos

3. **Não agir nos dados**
   - Coletar métricas e ignorar = desperdício
   - Defina ações para cada threshold violado

4. **Comparar equipes diretamente**
   - Contextos diferentes = métricas diferentes
   - Compare evolução, não valores absolutos

### 📚 Conexão com a Teoria

- [05-lembrar-sempre.md](../02-guia-teorico/05-lembrar-sempre.md) - Métricas e Sustentabilidade

---

## 📊 Resumo da Avaliação - Nível Intermediário

| Exercício | Pontos | Critérios |
|-----------|--------|-----------|
| 4 | 35 | Análise crítica + Refatoração + Testes |
| 5 | 35 | Estratégia mock + Cobertura cenários |
| 6 | 30 | Framework métricas + Implementação |
| **Total** | **100** | |

### Próximos Passos

- **90-100**: Pronto para nível avançado
- **75-89**: Revisão focada em gaps
- **60-74**: Praticar mais exercícios similares
- **< 60**: Revisar teoria e básico

---

| Anterior | Índice | Próximo |
|----------|--------|---------|
| [← Básico](01-nivel-basico.md) | [📚 Principal](../README.md) | [Avançado →](03-nivel-avancado.md) |
