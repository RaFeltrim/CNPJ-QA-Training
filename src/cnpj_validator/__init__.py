"""CNPJ Validator - Sistema de Validação de CNPJ

Módulo principal para validação de números de CNPJ (Cadastro Nacional de Pessoa Jurídica)

Compatível com Python 3.8+
"""

from .validators.numeric_validator import NumericCNPJValidator
from .validators.alphanumeric_validator import AlphanumericCNPJValidator
from .cnpj_validator import CNPJValidator
from .receita_federal_api import ReceitaFederalAPI, CNPJData, ReceitaFederalAPIError

__version__ = "2.0.0"
__all__ = [
    "CNPJValidator",
    "NumericCNPJValidator",
    "AlphanumericCNPJValidator",
    "ReceitaFederalAPI",
    "CNPJData",
    "ReceitaFederalAPIError",
]
