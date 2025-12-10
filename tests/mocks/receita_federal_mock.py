"""
Mock da API da Receita Federal para testes com CNPJs alfanuméricos.

Este mock simula respostas da API para CNPJs alfanuméricos,
permitindo testar o fluxo completo antes da implementação oficial
pela Receita Federal (prevista para julho/2026).
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
import random
import string


@dataclass
class MockEmpresaData:
    """Dados fictícios de uma empresa para testes."""
    cnpj: str
    razao_social: str
    nome_fantasia: str = ""
    situacao_cadastral: str = "ATIVA"
    data_situacao_cadastral: str = "2025-01-01"
    data_abertura: str = "2026-07-01"
    porte: str = "MEDIO"
    natureza_juridica: str = "206-2 - Sociedade Empresária Limitada"
    cnae_principal: dict = field(default_factory=lambda: {
        "codigo": "6201-5/01",
        "descricao": "Desenvolvimento de programas de computador sob encomenda"
    })
    endereco: dict = field(default_factory=lambda: {
        "logradouro": "Avenida Tecnologia",
        "numero": "1000",
        "complemento": "Sala 100",
        "bairro": "Centro",
        "municipio": "São Paulo",
        "uf": "SP",
        "cep": "01310-100"
    })
    telefone: str = "(11) 3000-0000"
    email: str = "contato@empresa.com.br"
    capital_social: float = 100000.00


class ReceitaFederalAPIMock:
    """
    Mock da API da Receita Federal para CNPJs alfanuméricos.
    
    Simula consultas para testes, gerando dados fictícios consistentes
    baseados no CNPJ fornecido.
    
    Example:
        >>> mock = ReceitaFederalAPIMock()
        >>> dados = mock.consultar("AB.CDE.123/0001-45")
        >>> print(dados.razao_social)
        'EMPRESA ABCDE123 LTDA'
    """
    
    # Empresas pré-cadastradas para testes específicos
    EMPRESAS_MOCK: Dict[str, MockEmpresaData] = {}
    
    # Situações possíveis
    SITUACOES = ["ATIVA", "BAIXADA", "INAPTA", "SUSPENSA"]
    
    # Portes possíveis
    PORTES = ["MEI", "ME", "EPP", "MEDIO", "GRANDE"]
    
    # Naturezas jurídicas comuns
    NATUREZAS = [
        "206-2 - Sociedade Empresária Limitada",
        "224-0 - Sociedade Anônima Aberta",
        "223-2 - Sociedade Anônima Fechada",
        "213-5 - Empresário Individual",
        "230-5 - Empresa Individual de Responsabilidade Limitada",
    ]

    def __init__(self, default_situacao: str = "ATIVA"):
        """
        Inicializa o mock.
        
        Args:
            default_situacao: Situação padrão para empresas geradas
        """
        self.default_situacao = default_situacao
        self._setup_empresas_padrao()
    
    def _setup_empresas_padrao(self):
        """Configura empresas padrão para testes específicos."""
        # Empresa alfanumérica ativa
        self.EMPRESAS_MOCK["TESTECNP000100"] = MockEmpresaData(
            cnpj="TE.STE.CNP/0001-00",
            razao_social="TESTE CNPJ ALFANUMERICO LTDA",
            nome_fantasia="TESTE ALFA",
            situacao_cadastral="ATIVA",
            capital_social=500000.00
        )
        
        # Empresa alfanumérica baixada
        self.EMPRESAS_MOCK["BAIXADA1000100"] = MockEmpresaData(
            cnpj="BA.IXA.DA1/0001-00",
            razao_social="EMPRESA BAIXADA EXEMPLO LTDA",
            situacao_cadastral="BAIXADA",
            data_situacao_cadastral="2026-12-01"
        )
        
        # Empresa alfanumérica inapta
        self.EMPRESAS_MOCK["INAPTA12000100"] = MockEmpresaData(
            cnpj="IN.APT.A12/0001-00",
            razao_social="EMPRESA INAPTA TESTE LTDA",
            situacao_cadastral="INAPTA"
        )
    
    def _limpar_cnpj(self, cnpj: str) -> str:
        """Remove formatação do CNPJ."""
        return "".join(c for c in cnpj if c.isalnum()).upper()
    
    def _gerar_razao_social(self, cnpj_limpo: str) -> str:
        """Gera razão social baseada no CNPJ."""
        raiz = cnpj_limpo[:8]
        sufixos = ["LTDA", "S.A.", "EIRELI", "ME", "EPP"]
        return f"EMPRESA {raiz} {random.choice(sufixos)}"
    
    def _gerar_nome_fantasia(self, cnpj_limpo: str) -> str:
        """Gera nome fantasia baseado no CNPJ."""
        raiz = cnpj_limpo[:8]
        return f"{raiz[:4]} CORP"
    
    def _gerar_empresa(self, cnpj: str) -> MockEmpresaData:
        """
        Gera dados fictícios para uma empresa.
        
        Args:
            cnpj: CNPJ formatado ou não
            
        Returns:
            MockEmpresaData com dados gerados
        """
        cnpj_limpo = self._limpar_cnpj(cnpj)
        
        # Formatar CNPJ
        cnpj_formatado = (
            f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/"
            f"{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        )
        
        # Usar seed baseada no CNPJ para dados consistentes
        seed = sum(ord(c) for c in cnpj_limpo)
        random.seed(seed)
        
        empresa = MockEmpresaData(
            cnpj=cnpj_formatado,
            razao_social=self._gerar_razao_social(cnpj_limpo),
            nome_fantasia=self._gerar_nome_fantasia(cnpj_limpo),
            situacao_cadastral=self.default_situacao,
            porte=random.choice(self.PORTES),
            natureza_juridica=random.choice(self.NATUREZAS),
            capital_social=random.randint(10000, 10000000) / 100
        )
        
        # Resetar seed para não afetar outros randoms
        random.seed()
        
        return empresa
    
    def cadastrar_empresa(self, cnpj: str, dados: MockEmpresaData) -> None:
        """
        Cadastra uma empresa específica no mock.
        
        Args:
            cnpj: CNPJ da empresa
            dados: Dados da empresa
        """
        cnpj_limpo = self._limpar_cnpj(cnpj)
        self.EMPRESAS_MOCK[cnpj_limpo] = dados
    
    def consultar(self, cnpj: str) -> MockEmpresaData:
        """
        Consulta dados de um CNPJ no mock.
        
        Args:
            cnpj: CNPJ a consultar
            
        Returns:
            MockEmpresaData com dados da empresa
            
        Raises:
            ValueError: Se CNPJ for inválido
            KeyError: Se empresa não encontrada (opcional)
        """
        cnpj_limpo = self._limpar_cnpj(cnpj)
        
        if len(cnpj_limpo) != 14:
            raise ValueError(f"CNPJ inválido: {cnpj}")
        
        # Verificar se existe no cadastro
        if cnpj_limpo in self.EMPRESAS_MOCK:
            return self.EMPRESAS_MOCK[cnpj_limpo]
        
        # Gerar empresa fictícia
        return self._gerar_empresa(cnpj)
    
    def verificar_situacao(self, cnpj: str) -> dict:
        """
        Verifica situação cadastral de um CNPJ.
        
        Args:
            cnpj: CNPJ a verificar
            
        Returns:
            Dict com situação e se está ativa
        """
        empresa = self.consultar(cnpj)
        return {
            "cnpj": empresa.cnpj,
            "situacao": empresa.situacao_cadastral,
            "ativa": empresa.situacao_cadastral == "ATIVA"
        }
    
    def to_api_response(self, empresa: MockEmpresaData) -> dict:
        """
        Converte MockEmpresaData para formato de resposta de API.
        
        Args:
            empresa: Dados da empresa
            
        Returns:
            Dict no formato da BrasilAPI
        """
        return {
            "cnpj": empresa.cnpj.replace(".", "").replace("/", "").replace("-", ""),
            "razao_social": empresa.razao_social,
            "nome_fantasia": empresa.nome_fantasia,
            "descricao_situacao_cadastral": empresa.situacao_cadastral,
            "data_situacao_cadastral": empresa.data_situacao_cadastral,
            "data_inicio_atividade": empresa.data_abertura,
            "porte": empresa.porte,
            "natureza_juridica": empresa.natureza_juridica,
            "cnae_fiscal": int(empresa.cnae_principal["codigo"].replace("-", "").replace("/", "")),
            "cnae_fiscal_descricao": empresa.cnae_principal["descricao"],
            "logradouro": empresa.endereco["logradouro"],
            "numero": empresa.endereco["numero"],
            "complemento": empresa.endereco["complemento"],
            "bairro": empresa.endereco["bairro"],
            "municipio": empresa.endereco["municipio"],
            "uf": empresa.endereco["uf"],
            "cep": empresa.endereco["cep"],
            "ddd_telefone_1": empresa.telefone,
            "email": empresa.email,
            "capital_social": empresa.capital_social
        }


# Dados de teste pré-definidos
CNPJS_TESTE_ALFANUMERICOS = [
    {
        "cnpj": "AB.CDE.123/0001-45",
        "descricao": "CNPJ alfanumérico misto",
        "esperado_valido": True
    },
    {
        "cnpj": "XY.ZAB.CDE/0001-78",
        "descricao": "CNPJ apenas letras na raiz",
        "esperado_valido": True
    },
    {
        "cnpj": "A1.B2C.3D4/0002-99",
        "descricao": "CNPJ alfanumérico filial",
        "esperado_valido": True
    },
    {
        "cnpj": "TE.STE.CNP/0001-00",
        "descricao": "CNPJ de teste padrão",
        "esperado_valido": True
    }
]


def gerar_cnpj_alfanumerico_valido(
    raiz: Optional[str] = None,
    apenas_letras: bool = False,
    apenas_numeros: bool = False
) -> str:
    """
    Gera um CNPJ alfanumérico válido para testes.
    
    Args:
        raiz: Raiz personalizada (8 caracteres)
        apenas_letras: Se True, raiz apenas com letras
        apenas_numeros: Se True, raiz apenas com números
        
    Returns:
        CNPJ formatado válido
    """
    from src.cnpj_validator.validators.new_alphanumeric_validator import (
        NewAlphanumericCNPJValidator
    )
    
    if raiz:
        return NewAlphanumericCNPJValidator.generate_valid_cnpj(raiz)
    elif apenas_letras:
        raiz = ''.join(random.choices(string.ascii_uppercase, k=8))
    elif apenas_numeros:
        raiz = ''.join(random.choices(string.digits, k=8))
    else:
        # Misto
        chars = string.ascii_uppercase + string.digits
        raiz = ''.join(random.choices(chars, k=8))
    
    return NewAlphanumericCNPJValidator.generate_valid_cnpj(raiz)
