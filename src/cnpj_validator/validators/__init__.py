"""
Módulo de validadores de CNPJ
"""

from .numeric_validator import NumericCNPJValidator
from .alphanumeric_validator import AlphanumericCNPJValidator

__all__ = ["NumericCNPJValidator", "AlphanumericCNPJValidator"]
