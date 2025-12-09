"""
CNPJ Validator - Sistema de Validação de CNPJ
Módulo principal para validação de números de CNPJ (Cadastro Nacional de Pessoa Jurídica)
"""

from .validators.numeric_validator import NumericCNPJValidator
from .validators.alphanumeric_validator import AlphanumericCNPJValidator
from .cnpj_validator import CNPJValidator

__version__ = "1.0.0"
__all__ = ["CNPJValidator", "NumericCNPJValidator", "AlphanumericCNPJValidator"]
