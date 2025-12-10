"""
Testes de integração para CNPJ alfanumérico.

Este módulo contém testes que validam a integração entre:
- Validador alfanumérico (NewAlphanumericCNPJValidator)
- API REST (endpoints /validate/alphanumeric e /generate/alphanumeric)
- Mock da API da Receita Federal (ReceitaFederalAPIMock)
"""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.cnpj_validator.validators.new_alphanumeric_validator import (
    NewAlphanumericCNPJValidator
)
from tests.mocks import (
    ReceitaFederalAPIMock,
    MockEmpresaData,
    CNPJS_TESTE_ALFANUMERICOS,
    gerar_cnpj_alfanumerico_valido
)


# Cliente de teste para a API
client = TestClient(app)


# =============================================================================
# Testes do Mock da API Receita Federal
# =============================================================================

class TestReceitaFederalAPIMock:
    """Testes para o mock da API da Receita Federal."""

    def setup_method(self):
        """Configuração antes de cada teste."""
        self.mock = ReceitaFederalAPIMock()

    def test_consulta_cnpj_alfanumerico(self):
        """Deve consultar um CNPJ alfanumérico no mock."""
        cnpj = gerar_cnpj_alfanumerico_valido()
        empresa = self.mock.consultar(cnpj)
        
        assert empresa is not None
        assert empresa.razao_social is not None
        assert len(empresa.razao_social) > 0

    def test_consulta_cnpj_precadastrado(self):
        """Deve retornar dados de empresa pré-cadastrada."""
        empresa = self.mock.consultar("TE.STE.CNP/0001-00")
        
        assert empresa.razao_social == "TESTE CNPJ ALFANUMERICO LTDA"
        assert empresa.nome_fantasia == "TESTE ALFA"
        assert empresa.situacao_cadastral == "ATIVA"

    def test_consulta_empresa_baixada(self):
        """Deve retornar empresa com situação BAIXADA."""
        empresa = self.mock.consultar("BA.IXA.DA1/0001-00")
        
        assert empresa.situacao_cadastral == "BAIXADA"

    def test_consulta_empresa_inapta(self):
        """Deve retornar empresa com situação INAPTA."""
        empresa = self.mock.consultar("IN.APT.A12/0001-00")
        
        assert empresa.situacao_cadastral == "INAPTA"

    def test_cadastrar_empresa_customizada(self):
        """Deve permitir cadastrar empresa personalizada."""
        empresa_custom = MockEmpresaData(
            cnpj="CU.STO.M01/0001-99",
            razao_social="EMPRESA CUSTOMIZADA LTDA",
            nome_fantasia="CUSTOM CORP",
            capital_social=1000000.00
        )
        
        self.mock.cadastrar_empresa("CU.STO.M01/0001-99", empresa_custom)
        resultado = self.mock.consultar("CU.STO.M01/0001-99")
        
        assert resultado.razao_social == "EMPRESA CUSTOMIZADA LTDA"
        assert resultado.capital_social == 1000000.00

    def test_verificar_situacao_ativa(self):
        """Deve verificar situação de empresa ativa."""
        resultado = self.mock.verificar_situacao("TE.STE.CNP/0001-00")
        
        assert resultado["ativa"] is True
        assert resultado["situacao"] == "ATIVA"

    def test_verificar_situacao_baixada(self):
        """Deve verificar situação de empresa baixada."""
        resultado = self.mock.verificar_situacao("BA.IXA.DA1/0001-00")
        
        assert resultado["ativa"] is False
        assert resultado["situacao"] == "BAIXADA"

    def test_to_api_response_formato_brasilapi(self):
        """Deve converter para formato da BrasilAPI."""
        empresa = self.mock.consultar("TE.STE.CNP/0001-00")
        response = self.mock.to_api_response(empresa)
        
        assert "cnpj" in response
        assert "razao_social" in response
        assert "descricao_situacao_cadastral" in response
        assert "capital_social" in response

    def test_consulta_cnpj_invalido(self):
        """Deve rejeitar CNPJ com tamanho inválido."""
        with pytest.raises(ValueError):
            self.mock.consultar("12345")  # Muito curto

    def test_geracao_dados_consistentes(self):
        """Deve gerar dados consistentes para o mesmo CNPJ."""
        cnpj = gerar_cnpj_alfanumerico_valido(raiz="CONSIS01")
        
        empresa1 = self.mock.consultar(cnpj)
        empresa2 = self.mock.consultar(cnpj)
        
        assert empresa1.razao_social == empresa2.razao_social
        assert empresa1.porte == empresa2.porte


# =============================================================================
# Testes de Integração: Validador + Mock
# =============================================================================

class TestIntegracaoValidadorMock:
    """Testes de integração entre validador e mock."""

    def setup_method(self):
        """Configuração antes de cada teste."""
        self.mock = ReceitaFederalAPIMock()
        self.validator = NewAlphanumericCNPJValidator()

    def test_gerar_validar_consultar(self):
        """Fluxo completo: gerar CNPJ, validar e consultar no mock."""
        # 1. Gerar CNPJ alfanumérico válido
        cnpj = gerar_cnpj_alfanumerico_valido()
        
        # 2. Validar o CNPJ
        result = self.validator.validate(cnpj)
        assert result.get("valid") is True
        
        # 3. Consultar no mock
        empresa = self.mock.consultar(cnpj)
        assert empresa is not None
        assert empresa.situacao_cadastral == "ATIVA"

    def test_todos_cnpjs_teste_validos(self):
        """Todos os CNPJs de teste pré-definidos devem ser consultáveis."""
        for item in CNPJS_TESTE_ALFANUMERICOS:
            cnpj = item["cnpj"]
            empresa = self.mock.consultar(cnpj)
            assert empresa is not None, f"Falha ao consultar: {cnpj}"

    def test_gerar_varios_cnpjs_diferentes(self):
        """Deve gerar CNPJs únicos e válidos."""
        cnpjs_gerados = set()
        
        for _ in range(10):
            cnpj = gerar_cnpj_alfanumerico_valido()
            
            # Verificar unicidade
            assert cnpj not in cnpjs_gerados
            cnpjs_gerados.add(cnpj)
            
            # Verificar validade
            result = self.validator.validate(cnpj)
            assert result.get("valid") is True
            
            # Verificar consulta no mock
            empresa = self.mock.consultar(cnpj)
            assert empresa is not None

    def test_cnpj_apenas_letras(self):
        """CNPJ com raiz apenas de letras."""
        cnpj = gerar_cnpj_alfanumerico_valido(apenas_letras=True)
        
        # Extrair raiz (8 primeiros caracteres sem formatação)
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
        raiz = cnpj_limpo[:8]
        
        # Verificar que é só letras
        assert raiz.isalpha()
        
        # Validar e consultar
        result = self.validator.validate(cnpj)
        assert result.get("valid") is True
        empresa = self.mock.consultar(cnpj)
        assert empresa is not None

    def test_cnpj_apenas_numeros(self):
        """CNPJ com raiz apenas de números (tradicional)."""
        cnpj = gerar_cnpj_alfanumerico_valido(apenas_numeros=True)
        
        # Extrair raiz
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
        raiz = cnpj_limpo[:8]
        
        # Verificar que é só números
        assert raiz.isdigit()
        
        # Validar e consultar
        result = self.validator.validate(cnpj)
        assert result.get("valid") is True


# =============================================================================
# Testes de Integração: API REST
# =============================================================================

class TestIntegracaoAPIRest:
    """Testes de integração com a API REST."""

    def test_endpoint_validate_alphanumeric_valido(self):
        """Endpoint de validação deve aceitar CNPJ alfanumérico válido."""
        cnpj = gerar_cnpj_alfanumerico_valido()
        
        response = client.get(f"/api/v1/validate/alphanumeric?cnpj={cnpj}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True

    def test_endpoint_validate_alphanumeric_invalido(self):
        """Endpoint de validação deve rejeitar CNPJ inválido."""
        cnpj_invalido = "AB.CDE.FGH/0001-99"  # DV incorreto
        
        response = client.get(f"/api/v1/validate/alphanumeric?cnpj={cnpj_invalido}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False

    def test_endpoint_generate_alphanumeric(self):
        """Endpoint de geração deve retornar CNPJ válido."""
        response = client.get("/api/v1/generate/alphanumeric")
        
        assert response.status_code == 200
        data = response.json()
        assert "cnpj_clean" in data
        assert "cnpj_formatted" in data
        
        # Validar o CNPJ gerado
        validator = NewAlphanumericCNPJValidator()
        result = validator.validate(data["cnpj_clean"])
        assert result.get("valid") is True

    def test_endpoint_generate_com_raiz(self):
        """Endpoint de geração deve aceitar raiz customizada."""
        response = client.get("/api/v1/generate/alphanumeric?raiz=TESTABCD")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que a raiz foi usada
        assert data["cnpj_clean"].startswith("TESTABCD")

    def test_endpoint_generate_raiz_invalida(self):
        """Endpoint de geração deve rejeitar raiz inválida."""
        response = client.get("/api/v1/generate/alphanumeric?raiz=AB@#$")
        
        assert response.status_code == 400

    def test_fluxo_gerar_e_validar(self):
        """Fluxo completo: gerar via API e validar via API."""
        # 1. Gerar
        response_gerar = client.get("/api/v1/generate/alphanumeric")
        assert response_gerar.status_code == 200
        cnpj = response_gerar.json()["cnpj_clean"]
        
        # 2. Validar
        response_validar = client.get(f"/api/v1/validate/alphanumeric?cnpj={cnpj}")
        assert response_validar.status_code == 200
        assert response_validar.json()["valid"] is True

    def test_api_health_check(self):
        """API deve responder ao health check."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


# =============================================================================
# Testes de Cenários Realistas
# =============================================================================

class TestCenariosRealistas:
    """Testes simulando cenários reais de uso."""

    def setup_method(self):
        """Configuração antes de cada teste."""
        self.mock = ReceitaFederalAPIMock()
        self.validator = NewAlphanumericCNPJValidator()

    def test_cenario_abertura_empresa_2026(self):
        """Simula abertura de empresa após julho/2026."""
        # Empresa nova com CNPJ alfanumérico
        cnpj = gerar_cnpj_alfanumerico_valido(raiz="NOVA2026")
        
        # Cadastrar empresa nova
        empresa_nova = MockEmpresaData(
            cnpj=cnpj,
            razao_social="NOVA EMPRESA 2026 LTDA",
            nome_fantasia="STARTUP 2026",
            data_abertura="2026-08-01",
            situacao_cadastral="ATIVA",
            porte="ME",
            capital_social=50000.00
        )
        self.mock.cadastrar_empresa(cnpj, empresa_nova)
        
        # Consultar
        resultado = self.mock.consultar(cnpj)
        
        assert resultado.data_abertura == "2026-08-01"
        assert resultado.situacao_cadastral == "ATIVA"

    def test_cenario_validacao_lote(self):
        """Simula validação de lote de CNPJs alfanuméricos."""
        cnpjs = [gerar_cnpj_alfanumerico_valido() for _ in range(50)]
        
        validos = 0
        for cnpj in cnpjs:
            result = self.validator.validate(cnpj)
            if result.get("valid"):
                validos += 1
        
        # Todos devem ser válidos (foram gerados com DVs corretos)
        assert validos == 50

    def test_cenario_migracao_sistema(self):
        """Simula migração de sistema para suportar alfanumérico."""
        # CNPJs alfanuméricos novos
        cnpjs_novos = [
            gerar_cnpj_alfanumerico_valido(apenas_letras=True),
            gerar_cnpj_alfanumerico_valido()
        ]
        
        # Sistema deve validar os novos formatos
        for cnpj in cnpjs_novos:
            result = self.validator.validate(cnpj)
            # NewAlphanumericCNPJValidator valida CNPJs gerados corretamente
            assert result.get("valid") is True

    def test_cenario_consulta_situacao_cadastral(self):
        """Simula verificação de situação cadastral."""
        # Configurar diferentes situações
        situacoes = {
            "ATIVA": "TE.STE.CNP/0001-00",
            "BAIXADA": "BA.IXA.DA1/0001-00",
            "INAPTA": "IN.APT.A12/0001-00"
        }
        
        for situacao_esperada, cnpj in situacoes.items():
            resultado = self.mock.verificar_situacao(cnpj)
            assert resultado["situacao"] == situacao_esperada


# =============================================================================
# Testes de Performance
# =============================================================================

class TestPerformance:
    """Testes de performance básicos."""

    def test_geracao_1000_cnpjs(self):
        """Deve gerar 1000 CNPJs em tempo razoável."""
        import time
        
        validator = NewAlphanumericCNPJValidator()
        
        inicio = time.time()
        for _ in range(1000):
            cnpj = gerar_cnpj_alfanumerico_valido()
            validator.validate(cnpj)
        fim = time.time()
        
        tempo_total = fim - inicio
        # Deve completar em menos de 5 segundos
        assert tempo_total < 5.0, f"Tempo excedido: {tempo_total:.2f}s"

    def test_consulta_mock_1000_vezes(self):
        """Deve consultar mock 1000 vezes em tempo razoável."""
        import time
        
        mock = ReceitaFederalAPIMock()
        cnpj = gerar_cnpj_alfanumerico_valido()
        
        inicio = time.time()
        for _ in range(1000):
            mock.consultar(cnpj)
        fim = time.time()
        
        tempo_total = fim - inicio
        # Deve completar em menos de 2 segundos
        assert tempo_total < 2.0, f"Tempo excedido: {tempo_total:.2f}s"
