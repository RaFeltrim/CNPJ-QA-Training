"""
Cliente da API da Receita Federal para consulta de CNPJ
Utiliza APIs públicas para obter dados cadastrais de empresas
"""

from __future__ import annotations

import time
import logging
from dataclasses import dataclass, field
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import json
import ssl

# Configurar logging
logger = logging.getLogger(__name__)


@dataclass
class CNPJData:
    """
    Classe que representa os dados de um CNPJ consultado na Receita Federal.

    Attributes:
        cnpj: Número do CNPJ
        razao_social: Razão social da empresa
        nome_fantasia: Nome fantasia da empresa
        situacao_cadastral: Situação cadastral (ATIVA, BAIXADA, etc.)
        data_situacao_cadastral: Data da situação cadastral
        motivo_situacao_cadastral: Código do motivo da situação
        data_abertura: Data de abertura da empresa
        porte: Porte da empresa (ME, EPP, etc.)
        natureza_juridica: Código e descrição da natureza jurídica
        cnae_principal: CNAE fiscal principal
        cnaes_secundarios: Lista de CNAEs secundários
        endereco: Dados de endereço completo
        telefone: Telefone de contato
        email: Email de contato
        capital_social: Capital social da empresa
        quadro_societario: Lista de sócios
        simples_nacional: Informações do Simples Nacional
        mei: Se é MEI
        raw_data: Dados brutos da API
    """
    cnpj: str = ""
    razao_social: str = ""
    nome_fantasia: str = ""
    situacao_cadastral: str = ""
    data_situacao_cadastral: str = ""
    motivo_situacao_cadastral: str = ""
    data_abertura: str = ""
    porte: str = ""
    natureza_juridica: str = ""
    cnae_principal: dict = field(default_factory=dict)
    cnaes_secundarios: list = field(default_factory=list)
    endereco: dict = field(default_factory=dict)
    telefone: str = ""
    email: str = ""
    capital_social: float = 0.0
    quadro_societario: list = field(default_factory=list)
    simples_nacional: dict = field(default_factory=dict)
    mei: bool = False
    raw_data: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {
            "cnpj": self.cnpj,
            "razao_social": self.razao_social,
            "nome_fantasia": self.nome_fantasia,
            "situacao_cadastral": self.situacao_cadastral,
            "data_situacao_cadastral": self.data_situacao_cadastral,
            "motivo_situacao_cadastral": self.motivo_situacao_cadastral,
            "data_abertura": self.data_abertura,
            "porte": self.porte,
            "natureza_juridica": self.natureza_juridica,
            "cnae_principal": self.cnae_principal,
            "cnaes_secundarios": self.cnaes_secundarios,
            "endereco": self.endereco,
            "telefone": self.telefone,
            "email": self.email,
            "capital_social": self.capital_social,
            "quadro_societario": self.quadro_societario,
            "simples_nacional": self.simples_nacional,
            "mei": self.mei,
        }

    def is_ativa(self) -> bool:
        """Verifica se a empresa está com situação ATIVA."""
        return self.situacao_cadastral.upper() == "ATIVA"

    def is_matriz(self) -> bool:
        """Verifica se é matriz (identificador 0001)."""
        cnpj_clean = "".join(c for c in self.cnpj if c.isdigit())
        if len(cnpj_clean) >= 12:
            return cnpj_clean[8:12] == "0001"
        return False

    def get_endereco_completo(self) -> str:
        """Retorna o endereço formatado completo."""
        if not self.endereco:
            return ""

        parts = []
        if self.endereco.get("logradouro"):
            parts.append(self.endereco["logradouro"])
        if self.endereco.get("numero"):
            parts.append(self.endereco["numero"])
        if self.endereco.get("complemento"):
            parts.append(self.endereco["complemento"])
        if self.endereco.get("bairro"):
            parts.append(f"- {self.endereco['bairro']}")
        if self.endereco.get("municipio"):
            parts.append(f"- {self.endereco['municipio']}")
        if self.endereco.get("uf"):
            parts.append(f"/{self.endereco['uf']}")
        if self.endereco.get("cep"):
            parts.append(f"- CEP: {self.endereco['cep']}")

        return " ".join(parts)


class ReceitaFederalAPIError(Exception):
    """Exceção para erros na API da Receita Federal."""

    def __init__(
        self, message: str, status_code: Optional[int] = None,
        response: Optional[str] = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ReceitaFederalAPI:
    """
    Cliente para consulta de CNPJ via APIs públicas.

    Utiliza a API pública BrasilAPI como fonte de dados.
    A BrasilAPI agrega dados de múltiplas fontes oficiais.

    Limites:
        - Rate limit: 3 requisições por minuto (API pública)
        - Timeout: 30 segundos por requisição

    Example:
        >>> api = ReceitaFederalAPI()
        >>> dados = api.consultar("11222333000181")
        >>> print(dados.razao_social)
        'EMPRESA EXEMPLO LTDA'
    """

    # APIs disponíveis (em ordem de preferência)
    APIS = {
        "brasilapi": "https://brasilapi.com.br/api/cnpj/v1/{cnpj}",
        "receitaws": "https://www.receitaws.com.br/v1/cnpj/{cnpj}",
    }

    def __init__(
        self,
        api_preferida: str = "brasilapi",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Inicializa o cliente da API.

        Args:
            api_preferida: Nome da API preferida ('brasilapi' ou 'receitaws')
            timeout: Timeout em segundos para requisições
            max_retries: Número máximo de tentativas em caso de erro
            retry_delay: Delay entre tentativas em segundos
        """
        self.api_preferida = api_preferida
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._last_request_time: float = 0.0
        self._min_interval: float = 20.0  # 3 req/min = 1 req a cada 20s

    def _limpar_cnpj(self, cnpj: str) -> str:
        """
        Remove formatação do CNPJ, mantendo letras e números.

        Compatível com o novo formato alfanumérico (2026+).
        Converte letras para maiúsculas.
        """
        return "".join(c for c in cnpj if c.isalnum()).upper()

    def _limpar_cnpj_numerico(self, cnpj: str) -> str:
        """
        Remove formatação do CNPJ, mantendo apenas números.

        Para uso com APIs que ainda não suportam formato alfanumérico.
        """
        return "".join(c for c in cnpj if c.isdigit())

    def _is_alphanumeric_cnpj(self, cnpj: str) -> bool:
        """Verifica se o CNPJ contém letras (formato alfanumérico)."""
        cnpj_limpo = self._limpar_cnpj(cnpj)
        return any(c.isalpha() for c in cnpj_limpo[:8])

    def _validar_cnpj_basico(self, cnpj: str) -> bool:
        """
        Validação básica do CNPJ antes da consulta.

        Compatível com formato numérico e alfanumérico.
        """
        cnpj_limpo = self._limpar_cnpj(cnpj)
        if len(cnpj_limpo) != 14:
            return False
        if len(set(cnpj_limpo)) == 1:
            return False

        # Validar estrutura: raiz (8 alfanum) + ordem (4 num) + dv (2 num)
        raiz = cnpj_limpo[:8]
        ordem = cnpj_limpo[8:12]
        dv = cnpj_limpo[12:14]

        # Raiz: A-Z e 0-9
        if not all(c.isalnum() for c in raiz):
            return False

        # Ordem e DV: apenas números
        if not ordem.isdigit() or not dv.isdigit():
            return False

        return True

    def _respeitar_rate_limit(self) -> None:
        """Garante que o rate limit seja respeitado."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            wait_time = self._min_interval - elapsed
            logger.debug(f"Rate limit: aguardando {wait_time:.1f}s")
            time.sleep(wait_time)
        self._last_request_time = time.time()

    def _fazer_requisicao(self, url: str) -> dict:
        """
        Faz requisição HTTP para a API.

        Args:
            url: URL completa da API

        Returns:
            Dados JSON da resposta

        Raises:
            ReceitaFederalAPIError: Em caso de erro na requisição
        """
        # Criar contexto SSL que ignora verificação (algumas APIs têm certificados problemáticos)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        headers = {
            "User-Agent": "CNPJ-Validator/1.0 (Python)",
            "Accept": "application/json",
        }

        request = Request(url, headers=headers)

        try:
            with urlopen(request, timeout=self.timeout, context=ctx) as response:
                data = response.read().decode("utf-8")
                return json.loads(data)
        except HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode("utf-8")
            except Exception:
                pass

            if e.code == 404:
                raise ReceitaFederalAPIError(
                    "CNPJ não encontrado na base da Receita Federal",
                    status_code=404,
                    response=error_body,
                )
            elif e.code == 429:
                raise ReceitaFederalAPIError(
                    "Rate limit excedido. Aguarde antes de fazer nova consulta.",
                    status_code=429,
                    response=error_body,
                )
            else:
                raise ReceitaFederalAPIError(
                    f"Erro HTTP {e.code}: {e.reason}",
                    status_code=e.code,
                    response=error_body,
                )
        except URLError as e:
            raise ReceitaFederalAPIError(f"Erro de conexão: {e.reason}")
        except json.JSONDecodeError as e:
            raise ReceitaFederalAPIError(f"Erro ao decodificar resposta JSON: {e}")
        except TimeoutError:
            raise ReceitaFederalAPIError(f"Timeout após {self.timeout} segundos")

    def _parse_brasilapi(self, data: dict) -> CNPJData:
        """Parse dos dados da BrasilAPI."""
        # Extrair CNAEs secundários
        cnaes_secundarios = []
        for cnae in data.get("cnaes_secundarios", []) or []:
            if isinstance(cnae, dict):
                cnaes_secundarios.append({
                    "codigo": cnae.get("codigo", ""),
                    "descricao": cnae.get("descricao", ""),
                })

        # Extrair quadro societário
        socios = []
        for socio in data.get("qsa", []) or []:
            if isinstance(socio, dict):
                socios.append({
                    "nome": socio.get("nome_socio", ""),
                    "qualificacao": socio.get("qualificacao_socio", ""),
                    "data_entrada": socio.get("data_entrada_sociedade", ""),
                })

        return CNPJData(
            cnpj=data.get("cnpj", ""),
            razao_social=data.get("razao_social", ""),
            nome_fantasia=data.get("nome_fantasia", "") or "",
            situacao_cadastral=data.get("descricao_situacao_cadastral", ""),
            data_situacao_cadastral=data.get("data_situacao_cadastral", ""),
            motivo_situacao_cadastral=str(data.get("motivo_situacao_cadastral", "")),
            data_abertura=data.get("data_inicio_atividade", ""),
            porte=data.get("porte", ""),
            natureza_juridica=data.get("natureza_juridica", ""),
            cnae_principal={
                "codigo": data.get("cnae_fiscal", ""),
                "descricao": data.get("cnae_fiscal_descricao", ""),
            },
            cnaes_secundarios=cnaes_secundarios,
            endereco={
                "logradouro": data.get("logradouro", ""),
                "numero": data.get("numero", ""),
                "complemento": data.get("complemento", ""),
                "bairro": data.get("bairro", ""),
                "municipio": data.get("municipio", ""),
                "uf": data.get("uf", ""),
                "cep": data.get("cep", ""),
            },
            telefone=data.get("ddd_telefone_1", ""),
            email=data.get("email", "") or "",
            capital_social=float(data.get("capital_social", 0) or 0),
            quadro_societario=socios,
            simples_nacional={
                "optante": data.get("opcao_pelo_simples", False),
                "data_opcao": data.get("data_opcao_pelo_simples", ""),
                "data_exclusao": data.get("data_exclusao_do_simples", ""),
            },
            mei=data.get("opcao_pelo_mei", False),
            raw_data=data,
        )

    def _parse_receitaws(self, data: dict) -> CNPJData:
        """Parse dos dados da ReceitaWS."""
        # Extrair CNAEs secundários
        cnaes_secundarios = []
        for cnae in data.get("atividades_secundarias", []) or []:
            if isinstance(cnae, dict):
                cnaes_secundarios.append({
                    "codigo": cnae.get("code", ""),
                    "descricao": cnae.get("text", ""),
                })

        # Extrair quadro societário
        socios = []
        for socio in data.get("qsa", []) or []:
            if isinstance(socio, dict):
                socios.append({
                    "nome": socio.get("nome", ""),
                    "qualificacao": socio.get("qual", ""),
                })

        # CNAE principal
        atividade_principal = data.get("atividade_principal", [{}])
        if atividade_principal and isinstance(atividade_principal, list):
            cnae_principal = {
                "codigo": atividade_principal[0].get("code", ""),
                "descricao": atividade_principal[0].get("text", ""),
            }
        else:
            cnae_principal = {}

        return CNPJData(
            cnpj=data.get("cnpj", ""),
            razao_social=data.get("nome", ""),
            nome_fantasia=data.get("fantasia", "") or "",
            situacao_cadastral=data.get("situacao", ""),
            data_situacao_cadastral=data.get("data_situacao", ""),
            motivo_situacao_cadastral=data.get("motivo_situacao", ""),
            data_abertura=data.get("abertura", ""),
            porte=data.get("porte", ""),
            natureza_juridica=data.get("natureza_juridica", ""),
            cnae_principal=cnae_principal,
            cnaes_secundarios=cnaes_secundarios,
            endereco={
                "logradouro": data.get("logradouro", ""),
                "numero": data.get("numero", ""),
                "complemento": data.get("complemento", ""),
                "bairro": data.get("bairro", ""),
                "municipio": data.get("municipio", ""),
                "uf": data.get("uf", ""),
                "cep": data.get("cep", ""),
            },
            telefone=data.get("telefone", ""),
            email=data.get("email", "") or "",
            capital_social=float(
                str(data.get("capital_social", "0")).replace(".", "").replace(",", ".")
                or 0
            ),
            quadro_societario=socios,
            simples_nacional={
                "optante": (
                    data.get("simples", {}).get("optante", False)
                    if data.get("simples") else False
                ),
            },
            mei=data.get("simei", {}).get("optante", False) if data.get("simei") else False,
            raw_data=data,
        )

    def consultar(self, cnpj: str, usar_fallback: bool = True) -> CNPJData:
        """
        Consulta dados de um CNPJ na Receita Federal.

        Args:
            cnpj: Número do CNPJ (com ou sem formatação)
            usar_fallback: Se True, tenta outras APIs em caso de erro

        Returns:
            CNPJData com os dados da empresa

        Raises:
            ReceitaFederalAPIError: Em caso de erro na consulta
            ValueError: Se o CNPJ for inválido

        Example:
            >>> api = ReceitaFederalAPI()
            >>> dados = api.consultar("11.222.333/0001-81")
            >>> print(dados.razao_social)
        """
        cnpj_limpo = self._limpar_cnpj(cnpj)

        if not self._validar_cnpj_basico(cnpj_limpo):
            raise ValueError(f"CNPJ inválido: {cnpj}")

        # Verificar se é alfanumérico
        is_alphanumeric = self._is_alphanumeric_cnpj(cnpj_limpo)
        if is_alphanumeric:
            raise ReceitaFederalAPIError(
                "CNPJs alfanuméricos ainda não são suportados pelas APIs externas. "
                "A Receita Federal implementará suporte a partir de julho/2026. "
                "Use o endpoint /api/v1/validate/alphanumeric para validação local.",
                status_code=501  # Not Implemented
            )

        # Para consulta, usar apenas a parte numérica
        cnpj_numerico = self._limpar_cnpj_numerico(cnpj)

        # Lista de APIs para tentar
        apis_para_tentar = [self.api_preferida]
        if usar_fallback:
            apis_para_tentar.extend(
                api for api in self.APIS.keys() if api != self.api_preferida
            )

        last_error: Optional[Exception] = None

        for api_name in apis_para_tentar:
            if api_name not in self.APIS:
                continue

            url = self.APIS[api_name].format(cnpj=cnpj_numerico)

            for attempt in range(self.max_retries):
                try:
                    self._respeitar_rate_limit()
                    logger.info(
                        f"Consultando CNPJ {cnpj_limpo} via {api_name} (tentativa {attempt + 1})")

                    data = self._fazer_requisicao(url)

                    # Verificar se a API retornou erro
                    if data.get("status") == "ERROR" or data.get("message"):
                        raise ReceitaFederalAPIError(
                            data.get("message", "Erro desconhecido na API")
                        )

                    # Parse baseado na API
                    if api_name == "brasilapi":
                        return self._parse_brasilapi(data)
                    elif api_name == "receitaws":
                        return self._parse_receitaws(data)
                    else:
                        # Parser genérico
                        return self._parse_brasilapi(data)

                except ReceitaFederalAPIError as e:
                    last_error = e
                    if e.status_code == 404:
                        # CNPJ não encontrado - não adianta tentar novamente
                        raise
                    elif e.status_code == 429:
                        # Rate limit - esperar mais
                        wait_time = self.retry_delay * (attempt + 1) * 5
                        logger.warning(f"Rate limit atingido, aguardando {wait_time}s")
                        time.sleep(wait_time)
                    else:
                        # Outros erros - tentar novamente após delay
                        if attempt < self.max_retries - 1:
                            time.sleep(self.retry_delay * (attempt + 1))
                except Exception as e:
                    last_error = e
                    logger.warning(f"Erro na tentativa {attempt + 1} com {api_name}: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))

            logger.warning(f"Todas as tentativas com {api_name} falharam")

        # Se chegou aqui, todas as APIs falharam
        if last_error:
            raise last_error
        raise ReceitaFederalAPIError("Não foi possível consultar o CNPJ em nenhuma API")

    def verificar_situacao(self, cnpj: str) -> dict:
        """
        Verifica apenas a situação cadastral do CNPJ.

        Args:
            cnpj: Número do CNPJ

        Returns:
            Dicionário com situação cadastral:
            {
                'cnpj': str,
                'situacao': str,
                'ativa': bool,
                'data_situacao': str
            }
        """
        dados = self.consultar(cnpj)
        return {
            "cnpj": dados.cnpj,
            "situacao": dados.situacao_cadastral,
            "ativa": dados.is_ativa(),
            "data_situacao": dados.data_situacao_cadastral,
        }

    def buscar_socios(self, cnpj: str) -> list:
        """
        Busca o quadro societário de um CNPJ.

        Args:
            cnpj: Número do CNPJ

        Returns:
            Lista de sócios
        """
        dados = self.consultar(cnpj)
        return dados.quadro_societario
