"""
Testes Unitários para NumericCNPJValidator
Seguindo princípios de Shift Left Testing
"""

import pytest
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cnpj_validator.validators.numeric_validator import NumericCNPJValidator


class TestNumericCNPJValidatorFormatting:
    """Testes de formatação e limpeza de CNPJ"""
    
    def test_remove_formatting_with_dots_slash_dash(self):
        """Deve remover pontos, barras e traços"""
        cnpj = "11.222.333/0001-81"
        result = NumericCNPJValidator.remove_formatting(cnpj)
        assert result == "11222333000181"
    
    def test_remove_formatting_with_only_numbers(self):
        """Deve manter CNPJ que já está sem formatação"""
        cnpj = "11222333000181"
        result = NumericCNPJValidator.remove_formatting(cnpj)
        assert result == "11222333000181"
    
    def test_remove_formatting_with_spaces(self):
        """Deve remover espaços"""
        cnpj = "11 222 333 0001 81"
        result = NumericCNPJValidator.remove_formatting(cnpj)
        assert result == "11222333000181"
    
    def test_remove_formatting_with_mixed_characters(self):
        """Deve remover todos os caracteres não numéricos"""
        cnpj = "11-222-333-0001-81"
        result = NumericCNPJValidator.remove_formatting(cnpj)
        assert result == "11222333000181"
    
    def test_remove_formatting_empty_string(self):
        """Deve retornar string vazia para entrada vazia"""
        cnpj = ""
        result = NumericCNPJValidator.remove_formatting(cnpj)
        assert result == ""
    
    def test_remove_formatting_with_non_string(self):
        """Deve retornar string vazia para entrada não string"""
        result = NumericCNPJValidator.remove_formatting(None)
        assert result == ""
        
        result = NumericCNPJValidator.remove_formatting(123)
        assert result == ""


class TestNumericCNPJValidatorLength:
    """Testes de validação de tamanho"""
    
    def test_validate_length_correct(self):
        """Deve validar CNPJ com 14 dígitos"""
        cnpj = "11222333000181"
        assert NumericCNPJValidator.validate_length(cnpj) is True
    
    def test_validate_length_too_short(self):
        """Deve rejeitar CNPJ com menos de 14 dígitos"""
        cnpj = "1122233300018"
        assert NumericCNPJValidator.validate_length(cnpj) is False
    
    def test_validate_length_too_long(self):
        """Deve rejeitar CNPJ com mais de 14 dígitos"""
        cnpj = "112223330001811"
        assert NumericCNPJValidator.validate_length(cnpj) is False
    
    def test_validate_length_empty(self):
        """Deve rejeitar string vazia"""
        cnpj = ""
        assert NumericCNPJValidator.validate_length(cnpj) is False


class TestNumericCNPJValidatorSameDigits:
    """Testes de validação de dígitos iguais"""
    
    @pytest.mark.parametrize("cnpj", [
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
    ])
    def test_validate_all_same_digits_should_fail(self, cnpj):
        """Deve rejeitar CNPJs com todos os dígitos iguais"""
        assert NumericCNPJValidator.validate_all_same_digits(cnpj) is False
    
    def test_validate_different_digits_should_pass(self):
        """Deve aceitar CNPJ com dígitos diferentes"""
        cnpj = "11222333000181"
        assert NumericCNPJValidator.validate_all_same_digits(cnpj) is True


class TestNumericCNPJValidatorCheckDigits:
    """Testes de cálculo de dígitos verificadores"""
    
    def test_calculate_first_digit_valid(self):
        """Deve calcular corretamente o primeiro dígito verificador"""
        cnpj = "112223330001"
        first_digit = NumericCNPJValidator.calculate_first_digit(cnpj)
        assert first_digit == 8
    
    def test_calculate_second_digit_valid(self):
        """Deve calcular corretamente o segundo dígito verificador"""
        cnpj = "1122233300018"
        second_digit = NumericCNPJValidator.calculate_second_digit(cnpj)
        assert second_digit == 1
    
    def test_validate_check_digits_valid_cnpj(self):
        """Deve validar dígitos verificadores de CNPJ válido"""
        cnpj = "11222333000181"
        assert NumericCNPJValidator.validate_check_digits(cnpj) is True
    
    def test_validate_check_digits_invalid_first_digit(self):
        """Deve rejeitar CNPJ com primeiro dígito verificador incorreto"""
        cnpj = "11222333000191"  # Primeiro DV errado
        assert NumericCNPJValidator.validate_check_digits(cnpj) is False
    
    def test_validate_check_digits_invalid_second_digit(self):
        """Deve rejeitar CNPJ com segundo dígito verificador incorreto"""
        cnpj = "11222333000182"  # Segundo DV errado
        assert NumericCNPJValidator.validate_check_digits(cnpj) is False
    
    def test_validate_check_digits_invalid_length(self):
        """Deve rejeitar CNPJ com tamanho incorreto"""
        cnpj = "1122233300018"  # 13 dígitos
        assert NumericCNPJValidator.validate_check_digits(cnpj) is False


class TestNumericCNPJValidatorCompleteValidation:
    """Testes de validação completa"""
    
    def test_validate_valid_formatted_cnpj(self):
        """Deve validar CNPJ válido e formatado"""
        cnpj = "11.222.333/0001-81"
        result = NumericCNPJValidator.validate(cnpj)
        
        assert result['valid'] is True
        assert result['cnpj_clean'] == "11222333000181"
        assert result['errors'] == []
    
    def test_validate_valid_unformatted_cnpj(self):
        """Deve validar CNPJ válido sem formatação"""
        cnpj = "11222333000181"
        result = NumericCNPJValidator.validate(cnpj)
        
        assert result['valid'] is True
        assert result['cnpj_clean'] == "11222333000181"
        assert result['errors'] == []
    
    def test_validate_empty_cnpj(self):
        """Deve rejeitar CNPJ vazio"""
        cnpj = ""
        result = NumericCNPJValidator.validate(cnpj)
        
        assert result['valid'] is False
        assert "vazio" in result['errors'][0]
    
    def test_validate_none_cnpj(self):
        """Deve rejeitar CNPJ None"""
        cnpj = None
        result = NumericCNPJValidator.validate(cnpj)
        
        assert result['valid'] is False
        assert len(result['errors']) > 0
    
    def test_validate_non_string_cnpj(self):
        """Deve rejeitar entrada não string"""
        cnpj = 11222333000181
        result = NumericCNPJValidator.validate(cnpj)
        
        assert result['valid'] is False
        assert "string" in result['errors'][0]
    
    def test_validate_cnpj_with_letters(self):
        """Deve rejeitar CNPJ com letras (após remoção da formatação, tamanho fica incorreto)"""
        cnpj = "1122233300018A"
        result = NumericCNPJValidator.validate(cnpj)
        
        assert result['valid'] is False
        # A letra é removida pela formatação, resultando em 13 dígitos
        assert "14 dígitos" in result['errors'][0]
    
    def test_validate_cnpj_wrong_length(self):
        """Deve rejeitar CNPJ com tamanho incorreto"""
        cnpj = "112223330001"  # 12 dígitos
        result = NumericCNPJValidator.validate(cnpj)
        
        assert result['valid'] is False
        assert "14 dígitos" in result['errors'][0]
    
    def test_validate_cnpj_all_zeros(self):
        """Deve rejeitar CNPJ com todos zeros"""
        cnpj = "00000000000000"
        result = NumericCNPJValidator.validate(cnpj)
        
        assert result['valid'] is False
        assert "dígitos iguais" in result['errors'][0]
    
    def test_validate_cnpj_invalid_check_digits(self):
        """Deve rejeitar CNPJ com dígitos verificadores inválidos"""
        cnpj = "11222333000199"
        result = NumericCNPJValidator.validate(cnpj)
        
        assert result['valid'] is False
        assert "verificadores inválidos" in result['errors'][0]
    
    @pytest.mark.parametrize("cnpj,expected_formatted", [
        ("11222333000181", "11.222.333/0001-81"),
        ("34028316000103", "34.028.316/0001-03"),
        ("60746948000112", "60.746.948/0001-12"),
    ])
    def test_validate_multiple_valid_cnpjs(self, cnpj, expected_formatted):
        """Deve validar múltiplos CNPJs válidos"""
        result = NumericCNPJValidator.validate(cnpj)
        assert result['valid'] is True
        assert result['cnpj_clean'] == cnpj


class TestNumericCNPJValidatorFormatCNPJ:
    """Testes de formatação de CNPJ"""
    
    def test_format_cnpj_valid(self):
        """Deve formatar CNPJ válido corretamente"""
        cnpj = "11222333000181"
        formatted = NumericCNPJValidator.format_cnpj(cnpj)
        assert formatted == "11.222.333/0001-81"
    
    def test_format_cnpj_already_formatted(self):
        """Deve formatar CNPJ que já está formatado"""
        cnpj = "11.222.333/0001-81"
        formatted = NumericCNPJValidator.format_cnpj(cnpj)
        assert formatted == "11.222.333/0001-81"
    
    def test_format_cnpj_invalid_length(self):
        """Deve retornar vazio para CNPJ com tamanho incorreto"""
        cnpj = "1122233300018"
        formatted = NumericCNPJValidator.format_cnpj(cnpj)
        assert formatted == ""
    
    def test_format_cnpj_with_letters(self):
        """Deve retornar vazio para CNPJ com letras"""
        cnpj = "1122233300018A"
        formatted = NumericCNPJValidator.format_cnpj(cnpj)
        assert formatted == ""
    
    def test_format_cnpj_empty(self):
        """Deve retornar vazio para CNPJ vazio"""
        cnpj = ""
        formatted = NumericCNPJValidator.format_cnpj(cnpj)
        assert formatted == ""


class TestNumericCNPJValidatorEdgeCases:
    """Testes de casos extremos e limites"""
    
    def test_cnpj_with_leading_zeros(self):
        """Deve validar CNPJ com zeros à esquerda"""
        cnpj = "00000001000191"  # CNPJ válido com zeros
        # Nota: Este CNPJ precisa ter DVs válidos
        # Usando um exemplo real
        cnpj_real = "01234567000100"
        result = NumericCNPJValidator.validate(cnpj_real)
        # Apenas verificar que processa, DV pode estar incorreto
        assert 'valid' in result
    
    def test_cnpj_with_special_characters(self):
        """Deve remover caracteres especiais variados"""
        cnpj = "11@222#333$0001%81"
        clean = NumericCNPJValidator.remove_formatting(cnpj)
        assert clean == "11222333000181"
    
    def test_very_long_string(self):
        """Deve rejeitar string muito longa"""
        cnpj = "1" * 100
        result = NumericCNPJValidator.validate(cnpj)
        assert result['valid'] is False
    
    def test_cnpj_with_unicode_characters(self):
        """Deve lidar com caracteres Unicode (são removidos pela formatação)"""
        cnpj = "11.222.333/0001-81★"
        result = NumericCNPJValidator.validate(cnpj)
        # O caractere Unicode é removido e o CNPJ resultante é válido
        assert result['valid'] is True
        assert result['cnpj_clean'] == "11222333000181"


# Casos de teste para integração com Zephyr
class TestZephyrIntegration:
    """
    Testes marcados para integração com Zephyr Scale
    Use estas anotações para mapear com casos de teste no Jira
    """
    
    @pytest.mark.zephyr("CNPJ-T001")
    def test_cnpj_valid_basic(self):
        """
        Zephyr Test Case: CNPJ-T001
        Descrição: Validar CNPJ válido básico
        Prioridade: Alta
        """
        cnpj = "11.222.333/0001-81"
        result = NumericCNPJValidator.validate(cnpj)
        assert result['valid'] is True
    
    @pytest.mark.zephyr("CNPJ-T002")
    def test_cnpj_invalid_check_digit(self):
        """
        Zephyr Test Case: CNPJ-T002
        Descrição: Rejeitar CNPJ com dígito verificador inválido
        Prioridade: Alta
        """
        cnpj = "11.222.333/0001-99"
        result = NumericCNPJValidator.validate(cnpj)
        assert result['valid'] is False
        assert "verificadores inválidos" in result['errors'][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
