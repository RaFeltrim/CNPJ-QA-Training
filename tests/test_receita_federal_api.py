"""
Testes para o cliente da API da Receita Federal
"""

import pytest
from unittest.mock import patch, MagicMock
import json

from src.cnpj_validator.receita_federal_api import (
    ReceitaFederalAPI,
    CNPJData,
    ReceitaFederalAPIError,
)


class TestCNPJData:
    """Testes para a classe CNPJData."""

    def test_cnpj_data_creation(self):
        """Testa criação de CNPJData com valores padrão."""
        data = CNPJData()
        assert data.cnpj == ""
        assert data.razao_social == ""
        assert data.situacao_cadastral == ""
        assert data.capital_social == 0.0
        assert data.mei is False

    def test_cnpj_data_with_values(self):
        """Testa criação de CNPJData com valores."""
        data = CNPJData(
            cnpj="11222333000181",
            razao_social="EMPRESA TESTE LTDA",
            situacao_cadastral="ATIVA",
            capital_social=100000.00,
        )
        assert data.cnpj == "11222333000181"
        assert data.razao_social == "EMPRESA TESTE LTDA"
        assert data.situacao_cadastral == "ATIVA"
        assert data.capital_social == 100000.00

    def test_is_ativa(self):
        """Testa método is_ativa."""
        data_ativa = CNPJData(situacao_cadastral="ATIVA")
        data_baixada = CNPJData(situacao_cadastral="BAIXADA")
        
        assert data_ativa.is_ativa() is True
        assert data_baixada.is_ativa() is False

    def test_is_matriz(self):
        """Testa método is_matriz."""
        data_matriz = CNPJData(cnpj="11222333000181")
        data_filial = CNPJData(cnpj="11222333000262")
        
        assert data_matriz.is_matriz() is True
        assert data_filial.is_matriz() is False

    def test_to_dict(self):
        """Testa conversão para dicionário."""
        data = CNPJData(
            cnpj="11222333000181",
            razao_social="EMPRESA TESTE",
        )
        result = data.to_dict()
        
        assert isinstance(result, dict)
        assert result["cnpj"] == "11222333000181"
        assert result["razao_social"] == "EMPRESA TESTE"

    def test_get_endereco_completo(self):
        """Testa formatação do endereço completo."""
        data = CNPJData(
            endereco={
                "logradouro": "Av Paulista",
                "numero": "1000",
                "complemento": "Sala 100",
                "bairro": "Bela Vista",
                "municipio": "São Paulo",
                "uf": "SP",
                "cep": "01310-100",
            }
        )
        endereco = data.get_endereco_completo()
        
        assert "Av Paulista" in endereco
        assert "1000" in endereco
        assert "São Paulo" in endereco
        assert "SP" in endereco


class TestReceitaFederalAPI:
    """Testes para o cliente da API."""

    def test_init_default(self):
        """Testa inicialização com valores padrão."""
        api = ReceitaFederalAPI()
        assert api.api_preferida == "brasilapi"
        assert api.timeout == 30
        assert api.max_retries == 3

    def test_init_custom(self):
        """Testa inicialização com valores customizados."""
        api = ReceitaFederalAPI(
            api_preferida="receitaws",
            timeout=60,
            max_retries=5,
        )
        assert api.api_preferida == "receitaws"
        assert api.timeout == 60
        assert api.max_retries == 5

    def test_limpar_cnpj(self):
        """Testa limpeza de formatação do CNPJ."""
        api = ReceitaFederalAPI()
        
        assert api._limpar_cnpj("11.222.333/0001-81") == "11222333000181"
        assert api._limpar_cnpj("11222333000181") == "11222333000181"
        assert api._limpar_cnpj("11 222 333 0001 81") == "11222333000181"

    def test_validar_cnpj_basico_valido(self):
        """Testa validação básica com CNPJ válido."""
        api = ReceitaFederalAPI()
        
        assert api._validar_cnpj_basico("11222333000181") is True
        assert api._validar_cnpj_basico("11.222.333/0001-81") is True

    def test_validar_cnpj_basico_invalido(self):
        """Testa validação básica com CNPJ inválido."""
        api = ReceitaFederalAPI()
        
        # Menos de 14 dígitos
        assert api._validar_cnpj_basico("1122233300018") is False
        # Todos dígitos iguais
        assert api._validar_cnpj_basico("00000000000000") is False
        assert api._validar_cnpj_basico("11111111111111") is False

    def test_consultar_cnpj_invalido(self):
        """Testa consulta com CNPJ inválido."""
        api = ReceitaFederalAPI()
        
        with pytest.raises(ValueError):
            api.consultar("123")
        
        with pytest.raises(ValueError):
            api.consultar("00000000000000")

    @patch("src.cnpj_validator.receita_federal_api.urlopen")
    def test_consultar_sucesso_brasilapi(self, mock_urlopen):
        """Testa consulta bem-sucedida via BrasilAPI."""
        # Mock da resposta da API
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "cnpj": "11222333000181",
            "razao_social": "EMPRESA TESTE LTDA",
            "nome_fantasia": "TESTE",
            "descricao_situacao_cadastral": "ATIVA",
            "data_situacao_cadastral": "2020-01-01",
            "data_inicio_atividade": "2010-05-15",
            "cnae_fiscal": "6201501",
            "cnae_fiscal_descricao": "Desenvolvimento de software",
            "logradouro": "Rua Teste",
            "numero": "100",
            "bairro": "Centro",
            "municipio": "São Paulo",
            "uf": "SP",
            "cep": "01000000",
            "capital_social": 100000.0,
            "qsa": [
                {"nome_socio": "João Silva", "qualificacao_socio": "Sócio-Administrador"}
            ],
        }).encode("utf-8")
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        api = ReceitaFederalAPI()
        api._min_interval = 0  # Desabilitar rate limit para testes
        
        resultado = api.consultar("11222333000181")

        assert resultado.cnpj == "11222333000181"
        assert resultado.razao_social == "EMPRESA TESTE LTDA"
        assert resultado.situacao_cadastral == "ATIVA"
        assert resultado.is_ativa() is True

    @patch("src.cnpj_validator.receita_federal_api.urlopen")
    def test_consultar_cnpj_nao_encontrado(self, mock_urlopen):
        """Testa consulta com CNPJ não encontrado."""
        from urllib.error import HTTPError
        
        mock_urlopen.side_effect = HTTPError(
            url="https://api.test",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=MagicMock(read=MagicMock(return_value=b"Not Found")),
        )

        api = ReceitaFederalAPI()
        api._min_interval = 0

        with pytest.raises(ReceitaFederalAPIError) as exc_info:
            api.consultar("11222333000181", usar_fallback=False)
        
        assert exc_info.value.status_code == 404
        assert "não encontrado" in str(exc_info.value).lower()

    def test_verificar_situacao(self):
        """Testa método verificar_situacao."""
        api = ReceitaFederalAPI()
        
        # Mock do método consultar
        with patch.object(api, "consultar") as mock_consultar:
            mock_consultar.return_value = CNPJData(
                cnpj="11222333000181",
                situacao_cadastral="ATIVA",
                data_situacao_cadastral="2020-01-01",
            )
            
            resultado = api.verificar_situacao("11222333000181")
            
            assert resultado["cnpj"] == "11222333000181"
            assert resultado["situacao"] == "ATIVA"
            assert resultado["ativa"] is True
            assert resultado["data_situacao"] == "2020-01-01"

    def test_buscar_socios(self):
        """Testa método buscar_socios."""
        api = ReceitaFederalAPI()
        
        socios_esperados = [
            {"nome": "João Silva", "qualificacao": "Sócio-Administrador"},
            {"nome": "Maria Santos", "qualificacao": "Sócio"},
        ]
        
        with patch.object(api, "consultar") as mock_consultar:
            mock_consultar.return_value = CNPJData(
                cnpj="11222333000181",
                quadro_societario=socios_esperados,
            )
            
            resultado = api.buscar_socios("11222333000181")
            
            assert len(resultado) == 2
            assert resultado[0]["nome"] == "João Silva"


class TestReceitaFederalAPIError:
    """Testes para a exceção customizada."""

    def test_error_message(self):
        """Testa criação de erro com mensagem."""
        error = ReceitaFederalAPIError("Erro de teste")
        assert str(error) == "Erro de teste"

    def test_error_with_status_code(self):
        """Testa criação de erro com status code."""
        error = ReceitaFederalAPIError("Not Found", status_code=404)
        assert error.status_code == 404

    def test_error_with_response(self):
        """Testa criação de erro com resposta."""
        error = ReceitaFederalAPIError(
            "Erro",
            status_code=500,
            response='{"error": "Internal Server Error"}',
        )
        assert error.response == '{"error": "Internal Server Error"}'


class TestIntegracaoValidadorAPI:
    """Testes de integração entre CNPJValidator e ReceitaFederalAPI."""

    def test_validar_e_consultar(self):
        """Testa fluxo de validar localmente e consultar na API."""
        from src.cnpj_validator import CNPJValidator, ReceitaFederalAPI
        
        validator = CNPJValidator()
        api = ReceitaFederalAPI()
        
        cnpj = "11.222.333/0001-81"
        
        # Primeiro valida localmente
        resultado_validacao = validator.validate(cnpj)
        
        # Se válido, preparamos para consultar na API
        if resultado_validacao["valid"]:
            cnpj_limpo = resultado_validacao["cnpj_clean"]
            assert cnpj_limpo == "11222333000181"
            
            # Mock da consulta na API
            with patch.object(api, "consultar") as mock_consultar:
                mock_consultar.return_value = CNPJData(
                    cnpj=cnpj_limpo,
                    razao_social="EMPRESA TESTE",
                    situacao_cadastral="ATIVA",
                )
                
                dados = api.consultar(cnpj_limpo)
                assert dados.cnpj == cnpj_limpo
                assert dados.is_ativa() is True
