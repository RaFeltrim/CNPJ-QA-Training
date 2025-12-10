"""
CNPJ Validator - Módulo Principal
Integra validações numéricas e alfanuméricas de CNPJ
"""

from .validators.numeric_validator import NumericCNPJValidator
from .validators.alphanumeric_validator import AlphanumericCNPJValidator


class CNPJValidator:
    """
    Classe principal para validação completa de CNPJ.
    Integra validações numéricas e alfanuméricas.
    """

    def __init__(self):
        """Inicializa o validador de CNPJ."""
        self.numeric_validator = NumericCNPJValidator()
        self.alphanumeric_validator = AlphanumericCNPJValidator()

    def validate(self, cnpj: str, validate_format: bool = True) -> dict:
        """
        Realiza validação completa do CNPJ (numérica e alfanumérica).

        Args:
            cnpj: String com CNPJ formatado ou não
            validate_format: Se True, valida também o formato alfanumérico

        Returns:
            Dicionário com resultado completo da validação:
            {
                'valid': bool,
                'cnpj_input': str,
                'cnpj_clean': str,
                'cnpj_formatted': str,
                'numeric_validation': dict,
                'alphanumeric_validation': dict (se validate_format=True),
                'errors': list,
                'warnings': list
            }
        """
        result = {
            'valid': False,
            'cnpj_input': cnpj,
            'cnpj_clean': '',
            'cnpj_formatted': '',
            'numeric_validation': {},
            'alphanumeric_validation': {},
            'errors': [],
            'warnings': []
        }

        # Validação numérica
        numeric_result = self.numeric_validator.validate(cnpj)
        result['numeric_validation'] = numeric_result
        result['cnpj_clean'] = numeric_result.get('cnpj_clean', '')

        if not numeric_result['valid']:
            result['errors'].extend(numeric_result['errors'])
            return result

        # Formatar CNPJ
        result['cnpj_formatted'] = self.numeric_validator.format_cnpj(result['cnpj_clean'])

        # Validação alfanumérica (se solicitada)
        if validate_format:
            # Se o CNPJ de entrada já está formatado, valida o formato original
            if '.' in cnpj or '/' in cnpj or '-' in cnpj:
                alphanumeric_result = self.alphanumeric_validator.validate(cnpj)
            else:
                # Se não está formatado, valida o formato gerado
                alphanumeric_result = self.alphanumeric_validator.validate(result['cnpj_formatted'])
                result['warnings'].append("CNPJ fornecido sem formatação")

            result['alphanumeric_validation'] = alphanumeric_result

            if not alphanumeric_result['valid']:
                result['errors'].extend(alphanumeric_result['errors'])

            if alphanumeric_result.get('warnings'):
                result['warnings'].extend(alphanumeric_result['warnings'])

        # Definir se é válido
        if validate_format:
            result['valid'] = numeric_result['valid'] and result['alphanumeric_validation'].get(
                'valid', False)
        else:
            result['valid'] = numeric_result['valid']

        return result

    def validate_numeric_only(self, cnpj: str) -> dict:
        """
        Realiza apenas validação numérica do CNPJ.

        Args:
            cnpj: String com CNPJ

        Returns:
            Dicionário com resultado da validação numérica
        """
        return self.numeric_validator.validate(cnpj)

    def validate_alphanumeric_only(self, cnpj: str) -> dict:
        """
        Realiza apenas validação alfanumérica do CNPJ.

        Args:
            cnpj: String com CNPJ

        Returns:
            Dicionário com resultado da validação alfanumérica
        """
        return self.alphanumeric_validator.validate(cnpj)

    def format(self, cnpj: str) -> str:
        """
        Formata o CNPJ no padrão XX.XXX.XXX/XXXX-XX.

        Args:
            cnpj: String com CNPJ

        Returns:
            String com CNPJ formatado ou mensagem de erro
        """
        validation = self.numeric_validator.validate(cnpj)

        if not validation['valid']:
            return f"Erro: {', '.join(validation['errors'])}"

        return self.numeric_validator.format_cnpj(validation['cnpj_clean'])

    def clean(self, cnpj: str) -> str:
        """
        Remove formatação do CNPJ, retornando apenas os números.

        Args:
            cnpj: String com CNPJ

        Returns:
            String com apenas os números do CNPJ
        """
        return self.numeric_validator.remove_formatting(cnpj)

    def get_info(self, cnpj: str) -> dict:
        """
        Obtém informações detalhadas sobre o CNPJ.

        Args:
            cnpj: String com CNPJ

        Returns:
            Dicionário com informações do CNPJ
        """
        validation = self.validate(cnpj, validate_format=True)

        if not validation['valid']:
            return {
                'valid': False,
                'errors': validation['errors']
            }

        info = {
            'valid': True,
            'cnpj_formatted': validation['cnpj_formatted'],
            'cnpj_clean': validation['cnpj_clean']
        }

        # Adicionar informações de matriz/filial
        alphanumeric = validation.get('alphanumeric_validation', {})
        if alphanumeric.get('filial_info'):
            info['matriz_filial'] = alphanumeric['filial_info']

        # Adicionar partes do CNPJ
        if alphanumeric.get('parts'):
            info['parts'] = alphanumeric['parts']

        return info

    @staticmethod
    def is_valid(cnpj: str) -> bool:
        """
        Método de conveniência para validação rápida.

        Args:
            cnpj: String com CNPJ

        Returns:
            True se o CNPJ é válido, False caso contrário
        """
        validator = CNPJValidator()
        result = validator.validate(cnpj, validate_format=False)
        return result['valid']
