# 🔗 Exemplo 02: Testes de Integração

> **Objetivo**: Demonstrar estratégias de testes de integração com mocks e API real

## 📋 Contexto

Este exemplo utiliza o `ReceitaFederalAPI` do projeto CNPJ-QA-Training para demonstrar como testar integrações com serviços externos seguindo princípios Shift Left.

## 🔍 Código Sob Teste

```python
# src/cnpj_validator/receita_federal_api.py

import requests
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class SituacaoCadastral(Enum):
    """Situação cadastral do CNPJ na Receita Federal."""
    ATIVA = "ATIVA"
    SUSPENSA = "SUSPENSA"
    INAPTA = "INAPTA"
    BAIXADA = "BAIXADA"
    NULA = "NULA"


@dataclass
class EmpresaInfo:
    """Informações da empresa retornadas pela API."""
    cnpj: str
    razao_social: str
    nome_fantasia: str
    situacao: SituacaoCadastral
    tipo: str  # MATRIZ ou FILIAL
    atividade_principal: str
    endereco: dict
    
    @classmethod
    def from_api_response(cls, data: dict) -> 'EmpresaInfo':
        """Cria instância a partir da resposta da API."""
        return cls(
            cnpj=data.get('cnpj', ''),
            razao_social=data.get('nome', ''),
            nome_fantasia=data.get('fantasia', ''),
            situacao=SituacaoCadastral(data.get('situacao', 'ATIVA')),
            tipo=data.get('tipo', 'MATRIZ'),
            atividade_principal=data.get('atividade_principal', [{}])[0].get('text', ''),
            endereco={
                'logradouro': data.get('logradouro', ''),
                'numero': data.get('numero', ''),
                'complemento': data.get('complemento', ''),
                'bairro': data.get('bairro', ''),
                'municipio': data.get('municipio', ''),
                'uf': data.get('uf', ''),
                'cep': data.get('cep', '')
            }
        )


class APIError(Exception):
    """Erro genérico da API."""
    pass


class CNPJNotFoundError(APIError):
    """CNPJ não encontrado na base da Receita."""
    pass


class RateLimitError(APIError):
    """Limite de requisições excedido."""
    pass


class ReceitaFederalAPI:
    """
    Cliente para consulta de CNPJ na API da Receita Federal.
    
    Implementa:
    - Retry com backoff exponencial
    - Timeout configurável
    - Cache de resultados
    - Tratamento de erros específicos
    """
    
    BASE_URL = "https://receitaws.com.br/v1/cnpj"
    DEFAULT_TIMEOUT = 10
    MAX_RETRIES = 3
    
    def __init__(self, timeout: int = DEFAULT_TIMEOUT, cache_enabled: bool = True):
        self.timeout = timeout
        self.cache_enabled = cache_enabled
        self._cache: dict = {}
    
    def consultar(self, cnpj: str) -> EmpresaInfo:
        """
        Consulta informações de um CNPJ na Receita Federal.
        
        Args:
            cnpj: CNPJ a consultar (com ou sem formatação)
            
        Returns:
            EmpresaInfo com dados da empresa
            
        Raises:
            CNPJNotFoundError: CNPJ não existe na base
            RateLimitError: Limite de requisições excedido
            APIError: Outros erros de API
        """
        # Sanitiza CNPJ
        cnpj_limpo = self._sanitize(cnpj)
        
        # Verifica cache
        if self.cache_enabled and cnpj_limpo in self._cache:
            return self._cache[cnpj_limpo]
        
        # Faz requisição com retry
        response = self._make_request(cnpj_limpo)
        
        # Processa resposta
        empresa = EmpresaInfo.from_api_response(response)
        
        # Armazena em cache
        if self.cache_enabled:
            self._cache[cnpj_limpo] = empresa
        
        return empresa
    
    def _sanitize(self, cnpj: str) -> str:
        """Remove formatação do CNPJ."""
        return ''.join(c for c in cnpj if c.isdigit())
    
    def _make_request(self, cnpj: str) -> dict:
        """Faz requisição HTTP com retry."""
        url = f"{self.BASE_URL}/{cnpj}"
        
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, timeout=self.timeout)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    raise CNPJNotFoundError(f"CNPJ {cnpj} não encontrado")
                elif response.status_code == 429:
                    if attempt < self.MAX_RETRIES - 1:
                        self._wait_backoff(attempt)
                        continue
                    raise RateLimitError("Limite de requisições excedido")
                else:
                    raise APIError(f"Erro HTTP {response.status_code}")
                    
            except requests.exceptions.Timeout:
                if attempt < self.MAX_RETRIES - 1:
                    continue
                raise APIError(f"Timeout após {self.MAX_RETRIES} tentativas")
            except requests.exceptions.RequestException as e:
                raise APIError(f"Erro de conexão: {e}")
        
        raise APIError("Máximo de tentativas excedido")
    
    def _wait_backoff(self, attempt: int) -> None:
        """Aguarda tempo exponencial entre retries."""
        import time
        wait_time = 2 ** attempt  # 1s, 2s, 4s
        time.sleep(wait_time)
    
    def limpar_cache(self) -> None:
        """Limpa o cache de consultas."""
        self._cache.clear()
```

## ✅ Suíte de Testes de Integração

```python
# tests/test_receita_federal_api.py

import pytest
import responses
import requests
from unittest.mock import patch, MagicMock

from cnpj_validator.receita_federal_api import (
    ReceitaFederalAPI,
    EmpresaInfo,
    SituacaoCadastral,
    CNPJNotFoundError,
    RateLimitError,
    APIError
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def api():
    """API client sem cache para testes isolados."""
    return ReceitaFederalAPI(timeout=5, cache_enabled=False)

@pytest.fixture
def api_com_cache():
    """API client com cache habilitado."""
    return ReceitaFederalAPI(timeout=5, cache_enabled=True)

@pytest.fixture
def resposta_empresa_valida():
    """Resposta mock de empresa válida."""
    return {
        "cnpj": "11.222.333/0001-81",
        "nome": "EMPRESA EXEMPLO LTDA",
        "fantasia": "EXEMPLO",
        "situacao": "ATIVA",
        "tipo": "MATRIZ",
        "atividade_principal": [
            {"code": "62.01-5-01", "text": "Desenvolvimento de software"}
        ],
        "logradouro": "Rua Exemplo",
        "numero": "123",
        "complemento": "Sala 1",
        "bairro": "Centro",
        "municipio": "São Paulo",
        "uf": "SP",
        "cep": "01234-567"
    }


# ============================================================
# TESTES COM MOCK (Rápidos, Isolados)
# ============================================================

class TestReceitaFederalAPIWithMock:
    """
    Testes usando mock de respostas HTTP.
    
    Princípio Shift Left: Testes rápidos e determinísticos
    que rodam em qualquer ambiente sem dependências externas.
    """
    
    BASE_URL = "https://receitaws.com.br/v1/cnpj"
    
    @responses.activate
    def test_consulta_cnpj_valido_retorna_empresa(self, api, resposta_empresa_valida):
        """
        GIVEN uma API mockada retornando dados válidos
        WHEN consulto um CNPJ
        THEN recebo objeto EmpresaInfo com dados corretos
        """
        # Arrange
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json=resposta_empresa_valida,
            status=200
        )
        
        # Act
        empresa = api.consultar("11.222.333/0001-81")
        
        # Assert
        assert isinstance(empresa, EmpresaInfo)
        assert empresa.cnpj == "11.222.333/0001-81"
        assert empresa.razao_social == "EMPRESA EXEMPLO LTDA"
        assert empresa.nome_fantasia == "EXEMPLO"
        assert empresa.situacao == SituacaoCadastral.ATIVA
        assert empresa.tipo == "MATRIZ"
    
    @responses.activate
    def test_consulta_cnpj_sem_formatacao(self, api, resposta_empresa_valida):
        """
        GIVEN CNPJ sem formatação
        WHEN consulto na API
        THEN a sanitização funciona corretamente
        """
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json=resposta_empresa_valida,
            status=200
        )
        
        empresa = api.consultar("11222333000181")
        
        assert empresa.cnpj == "11.222.333/0001-81"
    
    @responses.activate
    def test_cnpj_nao_encontrado_levanta_excecao(self, api):
        """
        GIVEN CNPJ inexistente na base
        WHEN consulto
        THEN recebo CNPJNotFoundError
        """
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/99999999999999",
            json={"message": "CNPJ não encontrado"},
            status=404
        )
        
        with pytest.raises(CNPJNotFoundError) as exc_info:
            api.consultar("99999999999999")
        
        assert "99999999999999" in str(exc_info.value)
    
    @responses.activate
    def test_rate_limit_levanta_excecao_apos_retries(self, api):
        """
        GIVEN API retornando 429 consistentemente
        WHEN consulto com retries
        THEN recebo RateLimitError após máximo de tentativas
        """
        # Mock retorna 429 em todas as tentativas
        for _ in range(api.MAX_RETRIES):
            responses.add(
                responses.GET,
                f"{self.BASE_URL}/11222333000181",
                json={"message": "Rate limit exceeded"},
                status=429
            )
        
        with pytest.raises(RateLimitError):
            api.consultar("11222333000181")
        
        # Verifica que tentou MAX_RETRIES vezes
        assert len(responses.calls) == api.MAX_RETRIES
    
    @responses.activate
    def test_timeout_faz_retry(self, api):
        """
        GIVEN primeira requisição com timeout
        WHEN consulto
        THEN faz retry e sucede na segunda
        """
        # Primeira chamada: timeout
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            body=requests.exceptions.Timeout()
        )
        # Segunda chamada: sucesso
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json={"cnpj": "11.222.333/0001-81", "nome": "EMPRESA", 
                  "situacao": "ATIVA", "tipo": "MATRIZ"},
            status=200
        )
        
        empresa = api.consultar("11222333000181")
        
        assert empresa.cnpj == "11.222.333/0001-81"
        assert len(responses.calls) == 2
    
    @responses.activate
    def test_erro_servidor_levanta_api_error(self, api):
        """
        GIVEN API retornando erro 500
        WHEN consulto
        THEN recebo APIError genérico
        """
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json={"message": "Internal server error"},
            status=500
        )
        
        with pytest.raises(APIError) as exc_info:
            api.consultar("11222333000181")
        
        assert "500" in str(exc_info.value)


class TestReceitaFederalAPICache:
    """
    Testes do sistema de cache.
    
    Princípio Shift Left: Cache reduz dependência de serviços externos
    e melhora performance, mas precisa ser testado isoladamente.
    """
    
    BASE_URL = "https://receitaws.com.br/v1/cnpj"
    
    @responses.activate
    def test_cache_evita_segunda_requisicao(self, api_com_cache, resposta_empresa_valida):
        """
        GIVEN cache habilitado e primeira consulta feita
        WHEN consulto mesmo CNPJ novamente
        THEN não faz nova requisição HTTP
        """
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json=resposta_empresa_valida,
            status=200
        )
        
        # Primeira consulta
        empresa1 = api_com_cache.consultar("11222333000181")
        
        # Segunda consulta (deve usar cache)
        empresa2 = api_com_cache.consultar("11222333000181")
        
        # Apenas uma requisição foi feita
        assert len(responses.calls) == 1
        
        # Resultados são iguais
        assert empresa1.cnpj == empresa2.cnpj
    
    @responses.activate
    def test_cache_diferencia_cnpjs(self, api_com_cache):
        """
        GIVEN cache com um CNPJ
        WHEN consulto CNPJ diferente
        THEN faz nova requisição
        """
        # Mock para dois CNPJs diferentes
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json={"cnpj": "11.222.333/0001-81", "nome": "EMPRESA 1",
                  "situacao": "ATIVA", "tipo": "MATRIZ"},
            status=200
        )
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/22333444000192",
            json={"cnpj": "22.333.444/0001-92", "nome": "EMPRESA 2",
                  "situacao": "ATIVA", "tipo": "MATRIZ"},
            status=200
        )
        
        empresa1 = api_com_cache.consultar("11222333000181")
        empresa2 = api_com_cache.consultar("22333444000192")
        
        # Duas requisições diferentes
        assert len(responses.calls) == 2
        assert empresa1.razao_social == "EMPRESA 1"
        assert empresa2.razao_social == "EMPRESA 2"
    
    @responses.activate
    def test_limpar_cache(self, api_com_cache, resposta_empresa_valida):
        """
        GIVEN cache com dados
        WHEN limpo o cache e consulto novamente
        THEN faz nova requisição
        """
        # Setup: duas respostas iguais
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json=resposta_empresa_valida,
            status=200
        )
        responses.add(
            responses.GET,
            f"{self.BASE_URL}/11222333000181",
            json=resposta_empresa_valida,
            status=200
        )
        
        # Primeira consulta
        api_com_cache.consultar("11222333000181")
        
        # Limpa cache
        api_com_cache.limpar_cache()
        
        # Segunda consulta (deve fazer nova requisição)
        api_com_cache.consultar("11222333000181")
        
        assert len(responses.calls) == 2


class TestEmpresaInfoParsing:
    """
    Testes de parsing da resposta da API.
    
    Princípio Shift Left: Testar parsing isoladamente
    facilita identificar problemas de integração.
    """
    
    def test_parsing_completo(self, resposta_empresa_valida):
        """Parse de resposta completa."""
        empresa = EmpresaInfo.from_api_response(resposta_empresa_valida)
        
        assert empresa.cnpj == "11.222.333/0001-81"
        assert empresa.razao_social == "EMPRESA EXEMPLO LTDA"
        assert empresa.nome_fantasia == "EXEMPLO"
        assert empresa.situacao == SituacaoCadastral.ATIVA
        assert empresa.atividade_principal == "Desenvolvimento de software"
        assert empresa.endereco['municipio'] == "São Paulo"
    
    def test_parsing_campos_ausentes(self):
        """Parse de resposta com campos ausentes."""
        resposta_minima = {
            "cnpj": "11.222.333/0001-81",
            "situacao": "ATIVA"
        }
        
        empresa = EmpresaInfo.from_api_response(resposta_minima)
        
        assert empresa.cnpj == "11.222.333/0001-81"
        assert empresa.razao_social == ""  # Default
        assert empresa.nome_fantasia == ""
        assert empresa.tipo == "MATRIZ"  # Default
    
    def test_parsing_situacoes(self):
        """Parse de diferentes situações cadastrais."""
        situacoes = ["ATIVA", "SUSPENSA", "INAPTA", "BAIXADA", "NULA"]
        
        for situacao in situacoes:
            resposta = {"cnpj": "11222333000181", "situacao": situacao}
            empresa = EmpresaInfo.from_api_response(resposta)
            assert empresa.situacao == SituacaoCadastral(situacao)


# ============================================================
# TESTES E2E (Lentos, Requerem API Real)
# ============================================================

@pytest.mark.e2e
@pytest.mark.skip(reason="Requer API real - executar manualmente")
class TestReceitaFederalAPIE2E:
    """
    Testes end-to-end com API real.
    
    Princípio Shift Left: Testes E2E são caros, então
    executamos menos frequentemente e em ambiente controlado.
    
    Para executar: pytest -m e2e --run-e2e
    """
    
    def test_consulta_cnpj_real(self):
        """
        Consulta CNPJ real na API da Receita.
        
        ATENÇÃO: Este teste faz requisição real!
        - Respeite rate limits
        - Use CNPJ de teste válido
        """
        api = ReceitaFederalAPI()
        
        # CNPJ da Receita Federal (público)
        empresa = api.consultar("00.394.460/0058-87")
        
        assert empresa.situacao == SituacaoCadastral.ATIVA
        assert "RECEITA" in empresa.razao_social.upper()


# ============================================================
# TESTES DE CONTRATO
# ============================================================

class TestReceitaFederalAPIContract:
    """
    Testes de contrato - validam estrutura esperada da API.
    
    Princípio Shift Left: Testes de contrato detectam
    mudanças na API antes que quebrem em produção.
    """
    
    def test_resposta_contem_campos_obrigatorios(self, resposta_empresa_valida):
        """Resposta deve conter todos os campos que usamos."""
        campos_obrigatorios = ['cnpj', 'nome', 'situacao', 'tipo']
        
        for campo in campos_obrigatorios:
            assert campo in resposta_empresa_valida, f"Campo {campo} ausente"
    
    def test_situacao_e_valor_conhecido(self, resposta_empresa_valida):
        """Situação deve ser um valor conhecido."""
        situacoes_validas = ['ATIVA', 'SUSPENSA', 'INAPTA', 'BAIXADA', 'NULA']
        
        assert resposta_empresa_valida['situacao'] in situacoes_validas


# ============================================================
# CONFIGURAÇÃO PYTEST
# ============================================================

def pytest_configure(config):
    """Registra markers customizados."""
    config.addinivalue_line(
        "markers", "e2e: testes end-to-end que requerem API real"
    )
```

## 🎯 Estratégias Demonstradas

### 1. Pirâmide de Testes de Integração

```
                ┌─────────┐
                │   E2E   │  ← Poucos, executados em schedule
              ┌─┴─────────┴─┐
              │  Contrato   │  ← Validam interface
            ┌─┴─────────────┴─┐
            │   Mock Tests    │  ← Maioria, rápidos
            └─────────────────┘
```

### 2. Biblioteca `responses` para Mocking

```python
@responses.activate
def test_consulta(self, api):
    responses.add(
        responses.GET,
        "https://api.example.com/endpoint",
        json={"data": "value"},
        status=200
    )
    
    result = api.call()
    
    assert result == expected
```

### 3. Testes de Cenários de Erro

```python
# Timeout
responses.add(
    responses.GET,
    url,
    body=requests.exceptions.Timeout()
)

# Rate Limit
responses.add(responses.GET, url, status=429)

# Not Found
responses.add(responses.GET, url, status=404)
```

### 4. Testes de Cache

```python
def test_cache(self, api):
    # Primeira chamada
    api.consultar("123")
    # Segunda chamada (cache)
    api.consultar("123")
    
    # Apenas 1 requisição HTTP
    assert len(responses.calls) == 1
```

## 📊 Cobertura de Cenários

| Cenário | Tipo de Teste | Frequência |
|---------|---------------|------------|
| Sucesso | Mock | Todo commit |
| 404 Not Found | Mock | Todo commit |
| 429 Rate Limit | Mock | Todo commit |
| 500 Server Error | Mock | Todo commit |
| Timeout + Retry | Mock | Todo commit |
| Cache hit | Mock | Todo commit |
| Cache miss | Mock | Todo commit |
| Parsing | Unitário | Todo commit |
| API Real | E2E | Diário/Semanal |

## 🔗 Próximos Passos

- [Exemplo 03: Pipeline CI/CD](exemplo-03-ci-cd.md)
- [Exemplo 04: Automação Completa](exemplo-04-automacao.md)

---

| Anterior | Índice | Próximo |
|----------|--------|---------|
| [← Unit Tests](exemplo-01-unit-tests.md) | [📚 Principal](../README.md) | [CI/CD →](exemplo-03-ci-cd.md) |
