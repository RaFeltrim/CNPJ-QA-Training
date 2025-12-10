"""
Inicializador do pacote de mocks para testes.
"""

from .receita_federal_mock import (
    ReceitaFederalAPIMock,
    MockEmpresaData,
    CNPJS_TESTE_ALFANUMERICOS,
    gerar_cnpj_alfanumerico_valido,
)

__all__ = [
    "ReceitaFederalAPIMock",
    "MockEmpresaData",
    "CNPJS_TESTE_ALFANUMERICOS",
    "gerar_cnpj_alfanumerico_valido",
]
