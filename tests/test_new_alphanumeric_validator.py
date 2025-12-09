"""
Testes para o validador de CNPJ Alfanumérico (Novo Formato)

Testa a validação de CNPJs com letras na raiz, conforme previsto
pela Receita Federal para implementação a partir de 2026.
"""

import pytest
from src.cnpj_validator.validators.new_alphanumeric_validator import NewAlphanumericCNPJValidator


class TestNewAlphanumericCNPJValidator:
    """Testes para o validador de CNPJ alfanumérico"""

    # =========================================================================
    # Testes de Remoção de Formatação
    # =========================================================================
    
    def test_remove_formatting_with_dots_and_slash(self):
        """Deve remover pontos, barra e hífen"""
        result = NewAlphanumericCNPJValidator.remove_formatting("AB.CDE.123/0001-45")
        assert result == "ABCDE123000145"
    
    def test_remove_formatting_preserves_letters(self):
        """Deve preservar letras e converter para maiúsculo"""
        result = NewAlphanumericCNPJValidator.remove_formatting("ab.cde.xyz/0001-00")
        assert result == "ABCDEXYZ000100"
    
    def test_remove_formatting_with_numbers_only(self):
        """Deve funcionar com CNPJ numérico tradicional"""
        result = NewAlphanumericCNPJValidator.remove_formatting("11.222.333/0001-81")
        assert result == "11222333000181"
    
    def test_remove_formatting_with_none(self):
        """Deve retornar string vazia para None"""
        result = NewAlphanumericCNPJValidator.remove_formatting(None)
        assert result == ""
    
    def test_remove_formatting_with_empty_string(self):
        """Deve retornar string vazia para string vazia"""
        result = NewAlphanumericCNPJValidator.remove_formatting("")
        assert result == ""

    # =========================================================================
    # Testes de Validação de Tamanho
    # =========================================================================
    
    def test_validate_length_valid(self):
        """Deve aceitar CNPJ com 14 caracteres"""
        result = NewAlphanumericCNPJValidator.validate_length("ABCDE123000145")
        assert result['valid'] is True
        assert result['length'] == 14
    
    def test_validate_length_too_short(self):
        """Deve rejeitar CNPJ com menos de 14 caracteres"""
        result = NewAlphanumericCNPJValidator.validate_length("ABCDE12300014")
        assert result['valid'] is False
        assert result['length'] == 13
        assert len(result['errors']) > 0
    
    def test_validate_length_too_long(self):
        """Deve rejeitar CNPJ com mais de 14 caracteres"""
        result = NewAlphanumericCNPJValidator.validate_length("ABCDE1230001456")
        assert result['valid'] is False
        assert result['length'] == 15

    # =========================================================================
    # Testes de Validação da Raiz
    # =========================================================================
    
    def test_validate_root_with_letters_only(self):
        """Deve aceitar raiz com apenas letras"""
        result = NewAlphanumericCNPJValidator.validate_root_chars("ABCDEFGH000100")
        assert result['valid'] is True
        assert result['has_letters'] is True
        assert result['has_numbers'] is False
    
    def test_validate_root_with_numbers_only(self):
        """Deve aceitar raiz com apenas números"""
        result = NewAlphanumericCNPJValidator.validate_root_chars("12345678000100")
        assert result['valid'] is True
        assert result['has_letters'] is False
        assert result['has_numbers'] is True
    
    def test_validate_root_with_mixed(self):
        """Deve aceitar raiz mista (letras e números)"""
        result = NewAlphanumericCNPJValidator.validate_root_chars("AB12CD34000100")
        assert result['valid'] is True
        assert result['has_letters'] is True
        assert result['has_numbers'] is True
    
    def test_validate_root_with_invalid_chars(self):
        """Deve rejeitar raiz com caracteres inválidos"""
        result = NewAlphanumericCNPJValidator.validate_root_chars("AB@DE!23000100")
        assert result['valid'] is False
        assert '@' in result['invalid_chars'] or '!' in result['invalid_chars']

    # =========================================================================
    # Testes de Validação da Ordem
    # =========================================================================
    
    def test_validate_order_matriz(self):
        """Deve identificar matriz (ordem = 0001)"""
        result = NewAlphanumericCNPJValidator.validate_order_digits("ABCDE123000100")
        assert result['valid'] is True
        assert result['order'] == "0001"
        assert result['is_matriz'] is True
    
    def test_validate_order_filial(self):
        """Deve identificar filial (ordem > 0001)"""
        result = NewAlphanumericCNPJValidator.validate_order_digits("ABCDE123000200")
        assert result['valid'] is True
        assert result['order'] == "0002"
        assert result['is_matriz'] is False
    
    def test_validate_order_with_letters(self):
        """Deve rejeitar ordem com letras"""
        result = NewAlphanumericCNPJValidator.validate_order_digits("ABCDE123ABC100")
        assert result['valid'] is False

    # =========================================================================
    # Testes de Cálculo de Dígitos Verificadores
    # =========================================================================
    
    def test_char_value_for_numbers(self):
        """Deve retornar valores corretos para números"""
        assert NewAlphanumericCNPJValidator.get_char_value('0') == 0
        assert NewAlphanumericCNPJValidator.get_char_value('5') == 5
        assert NewAlphanumericCNPJValidator.get_char_value('9') == 9
    
    def test_char_value_for_letters(self):
        """Deve retornar valores corretos para letras (A=10, B=11, ..., Z=35)"""
        assert NewAlphanumericCNPJValidator.get_char_value('A') == 10
        assert NewAlphanumericCNPJValidator.get_char_value('B') == 11
        assert NewAlphanumericCNPJValidator.get_char_value('Z') == 35
    
    def test_char_value_lowercase(self):
        """Deve funcionar com letras minúsculas"""
        assert NewAlphanumericCNPJValidator.get_char_value('a') == 10
        assert NewAlphanumericCNPJValidator.get_char_value('z') == 35
    
    def test_calculate_first_digit(self):
        """Deve calcular corretamente o primeiro dígito verificador"""
        # Para CNPJ numérico tradicional: 112223330001 -> DV = 81
        first = NewAlphanumericCNPJValidator.calculate_first_digit("112223330001")
        assert first == 8
    
    def test_calculate_second_digit(self):
        """Deve calcular corretamente o segundo dígito verificador"""
        second = NewAlphanumericCNPJValidator.calculate_second_digit("1122233300018")
        assert second == 1
    
    def test_validate_check_digits_traditional_cnpj(self):
        """Deve validar DVs de CNPJ tradicional"""
        result = NewAlphanumericCNPJValidator.validate_check_digits("11222333000181")
        assert result['valid'] is True
        assert result['expected_dv'] == "81"

    # =========================================================================
    # Testes de Validação Completa
    # =========================================================================
    
    def test_validate_traditional_cnpj(self):
        """Deve validar CNPJ numérico tradicional"""
        result = NewAlphanumericCNPJValidator.validate("11.222.333/0001-81")
        assert result['valid'] is True
        assert result['is_alphanumeric'] is False
        assert result['is_matriz'] is True
    
    def test_validate_empty_string(self):
        """Deve rejeitar string vazia"""
        result = NewAlphanumericCNPJValidator.validate("")
        assert result['valid'] is False
        assert "vazio" in result['errors'][0].lower()
    
    def test_validate_none(self):
        """Deve rejeitar None"""
        result = NewAlphanumericCNPJValidator.validate(None)
        assert result['valid'] is False
    
    def test_validate_wrong_length(self):
        """Deve rejeitar CNPJ com tamanho incorreto"""
        result = NewAlphanumericCNPJValidator.validate("ABCDE123")
        assert result['valid'] is False
        assert any("14" in e for e in result['errors'])
    
    def test_validate_all_same_chars(self):
        """Deve rejeitar CNPJ com todos caracteres iguais"""
        result = NewAlphanumericCNPJValidator.validate("AAAAAAAAAAAAAA")
        assert result['valid'] is False

    # =========================================================================
    # Testes de Formatação
    # =========================================================================
    
    def test_format_cnpj_alphanumeric(self):
        """Deve formatar CNPJ alfanumérico corretamente"""
        result = NewAlphanumericCNPJValidator.format_cnpj("ABCDE123000145")
        assert result == "AB.CDE.123/0001-45"
    
    def test_format_cnpj_traditional(self):
        """Deve formatar CNPJ tradicional corretamente"""
        result = NewAlphanumericCNPJValidator.format_cnpj("11222333000181")
        assert result == "11.222.333/0001-81"
    
    def test_format_cnpj_invalid_length(self):
        """Deve retornar string vazia para tamanho inválido"""
        result = NewAlphanumericCNPJValidator.format_cnpj("ABCDE")
        assert result == ""

    # =========================================================================
    # Testes de Extração de Partes
    # =========================================================================
    
    def test_extract_parts_alphanumeric(self):
        """Deve extrair partes de CNPJ alfanumérico"""
        result = NewAlphanumericCNPJValidator.extract_parts("AB.CDE.123/0001-45")
        assert result is not None
        assert result['raiz'] == "ABCDE123"
        assert result['ordem'] == "0001"
        assert result['dv'] == "45"
        assert result['is_matriz'] is True
        assert result['has_letters'] is True
    
    def test_extract_parts_filial(self):
        """Deve identificar filial corretamente"""
        result = NewAlphanumericCNPJValidator.extract_parts("ABCDE123000245")
        assert result is not None
        assert result['ordem'] == "0002"
        assert result['is_matriz'] is False
    
    def test_extract_parts_invalid(self):
        """Deve retornar None para CNPJ inválido"""
        result = NewAlphanumericCNPJValidator.extract_parts("ABC")
        assert result is None

    # =========================================================================
    # Testes de Geração de CNPJ
    # =========================================================================
    
    def test_generate_random_cnpj(self):
        """Deve gerar CNPJ válido aleatório"""
        cnpj = NewAlphanumericCNPJValidator.generate_valid_cnpj()
        result = NewAlphanumericCNPJValidator.validate(cnpj)
        assert result['valid'] is True
    
    def test_generate_cnpj_with_custom_root(self):
        """Deve gerar CNPJ válido com raiz personalizada"""
        cnpj = NewAlphanumericCNPJValidator.generate_valid_cnpj("TESTECNP")
        result = NewAlphanumericCNPJValidator.validate(cnpj)
        assert result['valid'] is True
        assert result['parts']['raiz'] == "TESTECNP"
    
    def test_generate_cnpj_with_short_root(self):
        """Deve preencher raiz curta com zeros"""
        cnpj = NewAlphanumericCNPJValidator.generate_valid_cnpj("ABC")
        result = NewAlphanumericCNPJValidator.validate(cnpj)
        assert result['valid'] is True
        assert result['parts']['raiz'].startswith("ABC")
    
    def test_generate_multiple_unique_cnpjs(self):
        """Deve gerar CNPJs únicos em chamadas múltiplas"""
        cnpjs = set()
        for _ in range(10):
            cnpj = NewAlphanumericCNPJValidator.generate_valid_cnpj()
            cnpjs.add(cnpj)
        # Deve ter gerado pelo menos alguns CNPJs diferentes
        assert len(cnpjs) >= 5

    # =========================================================================
    # Testes de Validação de Formato
    # =========================================================================
    
    def test_validate_format_correct(self):
        """Deve aceitar formato correto"""
        result = NewAlphanumericCNPJValidator.validate_format("AB.CDE.123/0001-45")
        assert result['valid'] is True
    
    def test_validate_format_without_separators(self):
        """Deve rejeitar formato sem separadores"""
        result = NewAlphanumericCNPJValidator.validate_format("ABCDE123000145")
        assert result['valid'] is False
    
    def test_validate_format_wrong_separators(self):
        """Deve rejeitar formato com separadores errados"""
        result = NewAlphanumericCNPJValidator.validate_format("AB-CDE-123.0001/45")
        assert result['valid'] is False

    # =========================================================================
    # Testes de Casos Especiais
    # =========================================================================
    
    def test_validate_with_lowercase_letters(self):
        """Deve aceitar letras minúsculas e converter para maiúsculas"""
        # Gera um CNPJ válido e testa com minúsculas
        cnpj_upper = NewAlphanumericCNPJValidator.generate_valid_cnpj("ABCD1234")
        cnpj_lower = cnpj_upper.lower()
        
        result = NewAlphanumericCNPJValidator.validate(cnpj_lower)
        assert result['valid'] is True
    
    def test_cnpj_numeric_compatibilidade(self):
        """Deve validar CNPJs numéricos tradicionais (retrocompatibilidade)"""
        # CNPJ válido numérico tradicional
        result = NewAlphanumericCNPJValidator.validate("34.028.316/0001-03")
        assert result['valid'] is True
        assert result['is_alphanumeric'] is False


class TestNewAlphanumericCNPJValidatorIntegration:
    """Testes de integração para validação alfanumérica"""
    
    def test_full_workflow_generate_and_validate(self):
        """Testa o fluxo completo: gerar, formatar, extrair e validar"""
        # Gera um CNPJ
        cnpj = NewAlphanumericCNPJValidator.generate_valid_cnpj("RAFAE123")
        
        # Valida
        validation = NewAlphanumericCNPJValidator.validate(cnpj)
        assert validation['valid'] is True
        
        # Remove formatação
        cnpj_clean = NewAlphanumericCNPJValidator.remove_formatting(cnpj)
        assert len(cnpj_clean) == 14
        
        # Formata novamente
        cnpj_formatted = NewAlphanumericCNPJValidator.format_cnpj(cnpj_clean)
        assert cnpj_formatted == cnpj
        
        # Extrai partes
        parts = NewAlphanumericCNPJValidator.extract_parts(cnpj)
        assert parts['raiz'] == "RAFAE123"
        assert parts['ordem'] == "0001"
    
    def test_dv_calculation_consistency(self):
        """Testa consistência do cálculo de DV"""
        base = "ABCD1234" + "0001"  # raiz + ordem
        
        # Calcula DVs
        dv1 = NewAlphanumericCNPJValidator.calculate_first_digit(base)
        dv2 = NewAlphanumericCNPJValidator.calculate_second_digit(base + str(dv1))
        
        # Monta CNPJ completo
        cnpj = base + str(dv1) + str(dv2)
        
        # Valida
        result = NewAlphanumericCNPJValidator.validate(cnpj)
        assert result['valid'] is True
        assert result['parts']['dv'] == f"{dv1}{dv2}"
