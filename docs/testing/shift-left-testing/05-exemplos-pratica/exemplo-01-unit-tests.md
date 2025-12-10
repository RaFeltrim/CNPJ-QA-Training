# 🧪 Exemplo 01: Testes Unitários

> **Objetivo**: Demonstrar boas práticas de testes unitários usando código real do projeto CNPJ

## 📋 Contexto

Este exemplo utiliza o `NumericValidator` do projeto CNPJ-QA-Training para demonstrar como aplicar os princípios de Shift Left Testing em testes unitários.

## 🔍 Código Sob Teste

```python
# src/cnpj_validator/validators/numeric_validator.py

class NumericValidator:
    """
    Validador de CNPJ numérico tradicional (14 dígitos).
    
    Responsável por:
    - Validar estrutura (14 dígitos numéricos)
    - Calcular e validar dígitos verificadores
    """
    
    # Multiplicadores para cálculo dos dígitos verificadores
    FIRST_DIGIT_WEIGHTS = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    SECOND_DIGIT_WEIGHTS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    def validate(self, cnpj: str) -> bool:
        """
        Valida um CNPJ numérico.
        
        Args:
            cnpj: String contendo apenas números (14 dígitos)
            
        Returns:
            True se válido, False caso contrário
        """
        # Remove formatação se houver
        cnpj = self._sanitize(cnpj)
        
        # Validações básicas
        if not self._is_valid_format(cnpj):
            return False
        
        # Validação dos dígitos verificadores
        return self._validate_check_digits(cnpj)
    
    def _sanitize(self, cnpj: str) -> str:
        """Remove caracteres não numéricos."""
        if cnpj is None:
            return ""
        return ''.join(c for c in str(cnpj) if c.isdigit())
    
    def _is_valid_format(self, cnpj: str) -> bool:
        """Verifica se o formato é válido."""
        # Deve ter 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Não pode ter todos os dígitos iguais
        if len(set(cnpj)) == 1:
            return False
        
        return True
    
    def _validate_check_digits(self, cnpj: str) -> bool:
        """Valida os dígitos verificadores."""
        # Primeiro dígito
        first_digit = self._calculate_digit(cnpj[:12], self.FIRST_DIGIT_WEIGHTS)
        if cnpj[12] != str(first_digit):
            return False
        
        # Segundo dígito
        second_digit = self._calculate_digit(cnpj[:13], self.SECOND_DIGIT_WEIGHTS)
        if cnpj[13] != str(second_digit):
            return False
        
        return True
    
    def _calculate_digit(self, base: str, weights: list) -> int:
        """Calcula um dígito verificador."""
        total = sum(int(d) * w for d, w in zip(base, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
```

## ✅ Suíte de Testes Completa

```python
# tests/test_numeric_validator.py

import pytest
from cnpj_validator.validators.numeric_validator import NumericValidator


class TestNumericValidatorSanitize:
    """
    Testes para o método _sanitize.
    
    Princípio Shift Left: Testar cada componente isoladamente
    permite encontrar bugs mais cedo e facilita debug.
    """
    
    @pytest.fixture
    def validator(self):
        """Fixture que fornece instância do validador."""
        return NumericValidator()
    
    def test_sanitize_remove_pontos(self, validator):
        """Remove pontos da formatação CNPJ."""
        resultado = validator._sanitize("11.222.333.0001.81")
        assert resultado == "11222333000181"
    
    def test_sanitize_remove_barras(self, validator):
        """Remove barras da formatação CNPJ."""
        resultado = validator._sanitize("11222333/000181")
        assert resultado == "11222333000181"
    
    def test_sanitize_remove_hifens(self, validator):
        """Remove hífens da formatação CNPJ."""
        resultado = validator._sanitize("11222333000181-")
        assert resultado == "11222333000181"
    
    def test_sanitize_formatacao_completa(self, validator):
        """Remove toda formatação padrão do CNPJ."""
        resultado = validator._sanitize("11.222.333/0001-81")
        assert resultado == "11222333000181"
    
    def test_sanitize_numeros_puros(self, validator):
        """Mantém números sem alteração."""
        resultado = validator._sanitize("11222333000181")
        assert resultado == "11222333000181"
    
    def test_sanitize_espacos(self, validator):
        """Remove espaços em branco."""
        resultado = validator._sanitize(" 11 222 333 ")
        assert resultado == "11222333"
    
    def test_sanitize_none_retorna_vazio(self, validator):
        """None retorna string vazia."""
        resultado = validator._sanitize(None)
        assert resultado == ""
    
    def test_sanitize_string_vazia(self, validator):
        """String vazia permanece vazia."""
        resultado = validator._sanitize("")
        assert resultado == ""


class TestNumericValidatorFormat:
    """
    Testes para validação de formato.
    
    Princípio Shift Left: Fail Fast - detectar problemas
    de formato antes de processar.
    """
    
    @pytest.fixture
    def validator(self):
        return NumericValidator()
    
    def test_format_valido_14_digitos(self, validator):
        """14 dígitos numéricos é formato válido."""
        assert validator._is_valid_format("11222333000181") is True
    
    def test_format_invalido_13_digitos(self, validator):
        """13 dígitos é inválido (falta 1)."""
        assert validator._is_valid_format("1122233300018") is False
    
    def test_format_invalido_15_digitos(self, validator):
        """15 dígitos é inválido (sobra 1)."""
        assert validator._is_valid_format("112223330001811") is False
    
    def test_format_invalido_digitos_iguais(self, validator):
        """Todos os dígitos iguais é inválido."""
        assert validator._is_valid_format("11111111111111") is False
        assert validator._is_valid_format("00000000000000") is False
        assert validator._is_valid_format("99999999999999") is False
    
    def test_format_valido_alguns_zeros(self, validator):
        """CNPJ com muitos zeros mas não todos é válido."""
        # CNPJ 00.000.000/0001-91 é válido (primeiro CNPJ possível)
        assert validator._is_valid_format("00000000000191") is True
    
    def test_format_vazio_invalido(self, validator):
        """String vazia é inválida."""
        assert validator._is_valid_format("") is False


class TestNumericValidatorCheckDigits:
    """
    Testes para cálculo dos dígitos verificadores.
    
    Princípio Shift Left: Testes de unidade verificam
    algoritmo matemático isoladamente.
    """
    
    @pytest.fixture
    def validator(self):
        return NumericValidator()
    
    # Testes do primeiro dígito verificador
    
    def test_calcula_primeiro_digito_exemplo_1(self, validator):
        """Calcula primeiro dígito para CNPJ 11.222.333/0001-81."""
        # Base: 112223330001, Primeiro dígito esperado: 8
        digito = validator._calculate_digit(
            "112223330001", 
            validator.FIRST_DIGIT_WEIGHTS
        )
        assert digito == 8
    
    def test_calcula_primeiro_digito_exemplo_2(self, validator):
        """Calcula primeiro dígito para CNPJ 00.000.000/0001-91."""
        digito = validator._calculate_digit(
            "000000000001", 
            validator.FIRST_DIGIT_WEIGHTS
        )
        assert digito == 9
    
    # Testes do segundo dígito verificador
    
    def test_calcula_segundo_digito_exemplo_1(self, validator):
        """Calcula segundo dígito para CNPJ 11.222.333/0001-81."""
        # Base: 1122233300018, Segundo dígito esperado: 1
        digito = validator._calculate_digit(
            "1122233300018", 
            validator.SECOND_DIGIT_WEIGHTS
        )
        assert digito == 1
    
    def test_calcula_segundo_digito_exemplo_2(self, validator):
        """Calcula segundo dígito para CNPJ 00.000.000/0001-91."""
        digito = validator._calculate_digit(
            "0000000000019", 
            validator.SECOND_DIGIT_WEIGHTS
        )
        assert digito == 1
    
    # Testes de validação completa dos dígitos
    
    def test_digitos_verificadores_validos(self, validator):
        """Dígitos verificadores corretos passam na validação."""
        assert validator._validate_check_digits("11222333000181") is True
        assert validator._validate_check_digits("00000000000191") is True
    
    def test_primeiro_digito_incorreto(self, validator):
        """Primeiro dígito incorreto falha na validação."""
        # CNPJ correto: 11222333000181
        # Alterando primeiro dígito verificador (8 -> 7)
        assert validator._validate_check_digits("11222333000171") is False
    
    def test_segundo_digito_incorreto(self, validator):
        """Segundo dígito incorreto falha na validação."""
        # CNPJ correto: 11222333000181
        # Alterando segundo dígito verificador (1 -> 2)
        assert validator._validate_check_digits("11222333000182") is False
    
    def test_ambos_digitos_incorretos(self, validator):
        """Ambos dígitos incorretos falha na validação."""
        assert validator._validate_check_digits("11222333000199") is False


class TestNumericValidatorIntegration:
    """
    Testes de integração do método validate().
    
    Princípio Shift Left: Testes de integração verificam
    que os componentes funcionam juntos corretamente.
    """
    
    @pytest.fixture
    def validator(self):
        return NumericValidator()
    
    # --- Casos de Sucesso ---
    
    def test_cnpj_valido_sem_formatacao(self, validator):
        """CNPJ válido sem formatação."""
        assert validator.validate("11222333000181") is True
    
    def test_cnpj_valido_com_formatacao(self, validator):
        """CNPJ válido com formatação padrão."""
        assert validator.validate("11.222.333/0001-81") is True
    
    def test_cnpj_valido_com_espacos(self, validator):
        """CNPJ válido com espaços extras."""
        assert validator.validate(" 11222333000181 ") is True
    
    # --- Casos de Falha: Formato ---
    
    def test_cnpj_muito_curto(self, validator):
        """CNPJ com menos de 14 dígitos."""
        assert validator.validate("1122233300018") is False
    
    def test_cnpj_muito_longo(self, validator):
        """CNPJ com mais de 14 dígitos."""
        assert validator.validate("112223330001811") is False
    
    def test_cnpj_vazio(self, validator):
        """String vazia é inválida."""
        assert validator.validate("") is False
    
    def test_cnpj_none(self, validator):
        """None é tratado como inválido."""
        assert validator.validate(None) is False
    
    def test_cnpj_apenas_formatacao(self, validator):
        """Apenas caracteres de formatação é inválido."""
        assert validator.validate("...///-") is False
    
    # --- Casos de Falha: Dígitos Verificadores ---
    
    def test_cnpj_digito_verificador_errado(self, validator):
        """CNPJ com dígito verificador incorreto."""
        assert validator.validate("11222333000182") is False
        assert validator.validate("11222333000191") is False
    
    # --- Casos Especiais ---
    
    def test_cnpj_todos_zeros_exceto_verificadores(self, validator):
        """CNPJ 00.000.000/0001-91 é válido (primeiro CNPJ)."""
        assert validator.validate("00000000000191") is True
    
    def test_cnpj_digitos_iguais(self, validator):
        """CNPJ com todos dígitos iguais é sempre inválido."""
        cnpjs_invalidos = [
            "00000000000000",
            "11111111111111",
            "22222222222222",
            "33333333333333",
            "44444444444444",
            "55555555555555",
            "66666666666666",
            "77777777777777",
            "88888888888888",
            "99999999999999",
        ]
        for cnpj in cnpjs_invalidos:
            assert validator.validate(cnpj) is False, f"CNPJ {cnpj} deveria ser inválido"
    
    # --- Testes Parametrizados ---
    
    @pytest.mark.parametrize("cnpj,esperado", [
        # CNPJs válidos conhecidos
        ("11222333000181", True),
        ("11.222.333/0001-81", True),
        ("00000000000191", True),
        
        # CNPJs inválidos
        ("11222333000182", False),  # Dígito errado
        ("1122233300018", False),   # Muito curto
        ("11111111111111", False),  # Dígitos iguais
        ("", False),                 # Vazio
    ])
    def test_validacao_parametrizada(self, validator, cnpj, esperado):
        """Testa múltiplos casos com parametrização."""
        assert validator.validate(cnpj) == esperado


class TestNumericValidatorEdgeCases:
    """
    Testes de casos de borda.
    
    Princípio Shift Left: Identificar e testar edge cases
    previne bugs em produção.
    """
    
    @pytest.fixture
    def validator(self):
        return NumericValidator()
    
    def test_entrada_tipo_inteiro(self, validator):
        """Entrada como inteiro é convertida para string."""
        # O método _sanitize converte para string
        resultado = validator.validate(11222333000181)
        # Pode passar ou falhar dependendo da implementação
        # O importante é não lançar exceção
        assert isinstance(resultado, bool)
    
    def test_entrada_com_letras(self, validator):
        """Entrada com letras misturadas."""
        assert validator.validate("11a22b33c00018d") is False
    
    def test_entrada_unicode(self, validator):
        """Entrada com caracteres unicode."""
        assert validator.validate("１１２２２３３３０００１８１") is False  # Full-width
    
    def test_cnpj_com_quebra_linha(self, validator):
        """CNPJ com quebra de linha."""
        assert validator.validate("11222333\n000181") is True


# --- Markers para categorização ---

class TestNumericValidatorSmoke:
    """
    Testes de fumaça - verificação rápida de sanidade.
    
    Executados primeiro no pipeline para feedback rápido.
    """
    
    @pytest.fixture
    def validator(self):
        return NumericValidator()
    
    @pytest.mark.smoke
    def test_smoke_valido(self, validator):
        """Verifica que um CNPJ válido passa."""
        assert validator.validate("11222333000181") is True
    
    @pytest.mark.smoke
    def test_smoke_invalido(self, validator):
        """Verifica que um CNPJ inválido falha."""
        assert validator.validate("00000000000000") is False
```

## 🎯 Práticas Demonstradas

### 1. Organização por Responsabilidade

```
TestNumericValidatorSanitize    → Testa limpeza de entrada
TestNumericValidatorFormat      → Testa validação de formato
TestNumericValidatorCheckDigits → Testa cálculo matemático
TestNumericValidatorIntegration → Testa fluxo completo
TestNumericValidatorEdgeCases   → Testa casos de borda
TestNumericValidatorSmoke       → Testes rápidos de sanidade
```

### 2. Padrão AAA (Arrange-Act-Assert)

```python
def test_sanitize_formatacao_completa(self, validator):
    # Arrange (implícito via fixture)
    # Act
    resultado = validator._sanitize("11.222.333/0001-81")
    # Assert
    assert resultado == "11222333000181"
```

### 3. Fixtures para Reutilização

```python
@pytest.fixture
def validator(self):
    """Fixture que fornece instância do validador."""
    return NumericValidator()
```

### 4. Testes Parametrizados

```python
@pytest.mark.parametrize("cnpj,esperado", [
    ("11222333000181", True),
    ("11222333000182", False),
])
def test_validacao_parametrizada(self, validator, cnpj, esperado):
    assert validator.validate(cnpj) == esperado
```

### 5. Markers para Categorização

```python
@pytest.mark.smoke
def test_smoke_valido(self, validator):
    """Executado primeiro no pipeline."""
    assert validator.validate("11222333000181") is True
```

## 📊 Métricas Esperadas

| Métrica | Valor Esperado |
|---------|----------------|
| Cobertura de linhas | > 95% |
| Cobertura de branches | > 90% |
| Tempo de execução | < 1 segundo |
| Número de testes | ~35-40 |

## 🔗 Próximos Passos

- [Exemplo 02: Testes de Integração](exemplo-02-integration.md)
- [Exemplo 03: Pipeline CI/CD](exemplo-03-ci-cd.md)

---

| Anterior | Índice | Próximo |
|----------|--------|---------|
| [← Gabarito](../04-gabarito/index.md) | [📚 Principal](../README.md) | [Integração →](exemplo-02-integration.md) |
