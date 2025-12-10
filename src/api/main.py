"""
API REST para Validação de CNPJ com Swagger/OpenAPI

Execute com: uvicorn src.api.main:app --reload
Acesse o Swagger em: http://localhost:8000/docs
"""

from cnpj_validator.validators.new_alphanumeric_validator import NewAlphanumericCNPJValidator
from cnpj_validator.validators.numeric_validator import NumericCNPJValidator
from cnpj_validator.validators.alphanumeric_validator import AlphanumericCNPJValidator
from cnpj_validator import CNPJValidator, ReceitaFederalAPI, ReceitaFederalAPIError
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

import sys
import os

# Adiciona o diretório src ao path para importações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# =============================================================================
# MODELOS (Schemas)
# =============================================================================

class TipoEstabelecimento(str, Enum):
    """Tipo de estabelecimento do CNPJ"""
    MATRIZ = "matriz"
    FILIAL = "filial"


class CNPJValidationResponse(BaseModel):
    """Resposta da validação de CNPJ"""
    valid: bool = Field(..., description="Se o CNPJ é válido")
    cnpj_formatted: str = Field(..., description="CNPJ formatado (XX.XXX.XXX/XXXX-XX)")
    cnpj_clean: str = Field(..., description="CNPJ sem formatação (14 dígitos)")
    tipo: Optional[TipoEstabelecimento] = Field(None, description="Matriz ou Filial")
    errors: List[str] = Field(default=[], description="Erros encontrados")

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "cnpj_formatted": "11.222.333/0001-81",
                "cnpj_clean": "11222333000181",
                "tipo": "matriz",
                "errors": []
            }
        }


class NumericValidationResponse(BaseModel):
    """Resposta da validação numérica detalhada"""
    valid: bool = Field(..., description="Se o CNPJ é válido")
    length_valid: bool = Field(..., description="Se possui 14 dígitos")
    not_all_same: bool = Field(..., description="Se os dígitos não são todos iguais")
    check_digits_valid: bool = Field(..., description="Se os DVs estão corretos")
    first_digit: Optional[int] = Field(None, description="1º DV calculado")
    second_digit: Optional[int] = Field(None, description="2º DV calculado")
    cnpj_clean: str = Field(..., description="CNPJ apenas números")
    errors: List[str] = Field(default=[], description="Erros encontrados")

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "length_valid": True,
                "not_all_same": True,
                "check_digits_valid": True,
                "first_digit": 8,
                "second_digit": 1,
                "cnpj_clean": "11222333000181",
                "errors": []
            }
        }


class FormatValidationResponse(BaseModel):
    """Resposta da validação de formato"""
    valid: bool = Field(..., description="Se o formato é válido")
    format_valid: bool = Field(..., description="Se está no formato XX.XXX.XXX/XXXX-XX")
    separators_valid: bool = Field(..., description="Se os separadores estão corretos")
    special_chars_valid: bool = Field(..., description="Se não há caracteres inválidos")
    whitespace_valid: bool = Field(..., description="Se não há espaços")
    tipo: Optional[TipoEstabelecimento] = Field(None, description="Matriz ou Filial")
    parts: Optional[dict] = Field(None, description="Partes do CNPJ")
    errors: List[str] = Field(default=[], description="Erros encontrados")

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "format_valid": True,
                "separators_valid": True,
                "special_chars_valid": True,
                "whitespace_valid": True,
                "tipo": "matriz",
                "parts": {"raiz": "11222333", "ordem": "0001", "dv": "81"},
                "errors": []
            }
        }


class NewFormatValidationResponse(BaseModel):
    """Resposta da validação do novo formato alfanumérico (2026+)"""
    valid: bool = Field(..., description="Se o CNPJ é válido")
    is_alphanumeric: bool = Field(..., description="Se contém letras na raiz")
    is_matriz: Optional[bool] = Field(None, description="Se é matriz")
    cnpj_formatted: str = Field(..., description="CNPJ formatado")
    cnpj_clean: str = Field(..., description="CNPJ sem formatação")
    root_valid: bool = Field(..., description="Se a raiz é válida")
    order_valid: bool = Field(..., description="Se a ordem é válida")
    dv_valid: bool = Field(..., description="Se os DVs estão corretos")
    parts: Optional[dict] = Field(None, description="Partes do CNPJ")
    errors: List[str] = Field(default=[], description="Erros encontrados")

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "is_alphanumeric": True,
                "is_matriz": True,
                "cnpj_formatted": "AB.CDE.123/0001-XX",
                "cnpj_clean": "ABCDE123000145",
                "root_valid": True,
                "order_valid": True,
                "dv_valid": True,
                "parts": {"raiz": "ABCDE123", "ordem": "0001", "dv": "45"},
                "errors": []
            }
        }


class GenerateCNPJResponse(BaseModel):
    """Resposta da geração de CNPJ"""
    cnpj_formatted: str = Field(..., description="CNPJ formatado")
    cnpj_clean: str = Field(..., description="CNPJ sem formatação")
    raiz: str = Field(..., description="Raiz utilizada")
    is_alphanumeric: bool = Field(..., description="Se contém letras")


class BatchValidationResponse(BaseModel):
    """Resposta da validação em lote"""
    total: int = Field(..., description="Total de CNPJs")
    valid_count: int = Field(..., description="Quantidade de válidos")
    invalid_count: int = Field(..., description="Quantidade de inválidos")
    results: List[dict] = Field(..., description="Resultados individuais")


class CNPJInfoResponse(BaseModel):
    """Dados cadastrais do CNPJ"""
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    situacao_cadastral: str
    tipo_estabelecimento: str
    data_abertura: Optional[str] = None
    endereco: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    atividade_principal: Optional[str] = None


class HealthResponse(BaseModel):
    """Resposta do health check"""
    status: str
    version: str
    service: str


# =============================================================================
# CONFIGURAÇÃO DA API
# =============================================================================

API_VERSION = "2.1.0"

app = FastAPI(
    title="API de Validação de CNPJ",
    description="""
## API para Validação e Consulta de CNPJ

### Funcionalidades

| Recurso | Descrição |
|---------|-----------|
| **Validação** | Verifica dígitos verificadores e formato |
| **Formatação** | Converte CNPJ para formato padrão |
| **Consulta** | Busca dados na Receita Federal |
| **Novo Formato** | Suporte ao CNPJ alfanumérico (2026+) |

### Tipos de Validação

1. **Básica** - Valida dígitos verificadores
2. **Numérica** - Detalhes do cálculo dos DVs
3. **Formato** - Verifica pontuação e separadores
4. **Novo Formato** - CNPJs com letras (A-Z) na raiz

### CNPJs para Teste

| CNPJ | Válido | Observação |
|------|--------|------------|
| `11222333000181` | Sim | CNPJ válido (matriz) |
| `11222333000262` | Sim | CNPJ válido (filial) |
| `11111111111111` | Não | Dígitos repetidos |
| `12345678901234` | Não | DVs incorretos |

---
*Projeto de treinamento em QA*
    """,
    version=API_VERSION,
    contact={
        "name": "Rafael Feltrim",
        "url": "https://github.com/RaFeltrim/CNPJ-QA-Training",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Status",
            "description": "Verificação de saúde da API",
        },
        {
            "name": "Validação Básica",
            "description": "Validação simples de CNPJ",
        },
        {
            "name": "Validação Detalhada",
            "description": "Validação com detalhes (numérica e formato)",
        },
        {
            "name": "Novo Formato (2026+)",
            "description": "CNPJ alfanumérico com letras na raiz",
        },
        {
            "name": "Consulta Receita Federal",
            "description": "Busca dados cadastrais",
        },
        {
            "name": "Utilitários",
            "description": "Formatação e ferramentas auxiliares",
        },
    ]
)


# =============================================================================
# 🏥 STATUS
# =============================================================================

@app.get("/", tags=["Status"], summary="Informações da API")
async def root():
    """Retorna informações básicas da API."""
    return {
        "api": "CNPJ Validator",
        "version": API_VERSION,
        "docs": "/docs",
        "status": "online"
    }


@app.get("/health", tags=["Status"], summary="Health Check", response_model=HealthResponse)
async def health_check():
    """Verifica se a API está funcionando. Útil para monitoramento."""
    return HealthResponse(status="healthy", version=API_VERSION, service="cnpj-validator-api")


# =============================================================================
# VALIDAÇÃO BÁSICA
# =============================================================================

@app.get(
    "/api/v1/validate",
    tags=["Validação Básica"],
    summary="Validar CNPJ",
    response_model=CNPJValidationResponse
)
async def validate_cnpj(
    cnpj: str = Query(..., description="CNPJ a validar", example="11222333000181")
):
    """
    Valida um CNPJ verificando os dígitos verificadores.

    **Aceita com ou sem formatação.**

    Exemplo: `?cnpj=11222333000181` ou `?cnpj=11.222.333/0001-81`
    """
    validator = CNPJValidator()
    result = validator.validate(cnpj)

    tipo = None
    if result.get('valid'):
        info = validator.get_info(cnpj)
        tipo = TipoEstabelecimento.MATRIZ if info.get('is_matriz') else TipoEstabelecimento.FILIAL

    return CNPJValidationResponse(
        valid=result.get('valid', False),
        cnpj_formatted=result.get('cnpj_formatted', ''),
        cnpj_clean=result.get('cnpj_clean', ''),
        tipo=tipo,
        errors=result.get('errors', [])
    )


@app.get(
    "/api/v1/validate/batch",
    tags=["Validação Básica"],
    summary="Validar múltiplos CNPJs",
    response_model=BatchValidationResponse
)
async def validate_batch(
    cnpjs: str = Query(..., description="CNPJs separados por vírgula (máx. 50)",
                       example="11222333000181,11111111111111")
):
    """
    Valida múltiplos CNPJs em uma única requisição.

    **Limite**: 50 CNPJs por requisição.
    """
    cnpj_list = [c.strip() for c in cnpjs.split(",")]

    if len(cnpj_list) > 50:
        raise HTTPException(status_code=400, detail="Máximo de 50 CNPJs por requisição")

    validator = CNPJValidator()
    results = []

    for cnpj in cnpj_list:
        result = validator.validate(cnpj)
        results.append({
            "cnpj": cnpj,
            "valid": result.get('valid', False),
            "cnpj_formatted": result.get('cnpj_formatted', ''),
            "errors": result.get('errors', [])
        })

    valid_count = sum(1 for r in results if r['valid'])

    return BatchValidationResponse(
        total=len(results),
        valid_count=valid_count,
        invalid_count=len(results) - valid_count,
        results=results
    )


# =============================================================================
# VALIDAÇÃO DETALHADA
# =============================================================================

@app.get(
    "/api/v1/validate/numeric",
    tags=["Validação Detalhada"],
    summary="Validação Numérica",
    response_model=NumericValidationResponse
)
async def validate_numeric(
    cnpj: str = Query(..., description="CNPJ (apenas números)", example="11222333000181")
):
    """
    Validação numérica detalhada com cálculo dos dígitos verificadores.

    Retorna:
    - Se o tamanho está correto (14 dígitos)
    - Se os dígitos não são todos iguais
    - Os DVs calculados vs informados
    """
    errors = []
    cnpj_clean = NumericCNPJValidator.remove_formatting(cnpj)

    length_valid = NumericCNPJValidator.validate_length(cnpj_clean)
    not_all_same = NumericCNPJValidator.validate_all_same_digits(cnpj_clean)

    first_digit = None
    second_digit = None
    check_digits_valid = False

    if length_valid and cnpj_clean.isdigit():
        first_digit = NumericCNPJValidator.calculate_first_digit(cnpj_clean[:12])
        second_digit = NumericCNPJValidator.calculate_second_digit(cnpj_clean[:13])
        check_digits_valid = NumericCNPJValidator.validate_check_digits(cnpj_clean)

    if not length_valid:
        errors.append(f"CNPJ deve ter 14 dígitos (possui {len(cnpj_clean)})")
    if not not_all_same:
        errors.append("Dígitos não podem ser todos iguais")
    if length_valid and not check_digits_valid:
        errors.append(
            f"DV inválido: esperado {first_digit}{second_digit}, recebido {cnpj_clean[12:14]}")

    return NumericValidationResponse(
        valid=length_valid and not_all_same and check_digits_valid,
        length_valid=length_valid,
        not_all_same=not_all_same,
        check_digits_valid=check_digits_valid,
        first_digit=first_digit,
        second_digit=second_digit,
        cnpj_clean=cnpj_clean,
        errors=errors
    )


@app.get(
    "/api/v1/validate/format",
    tags=["Validação Detalhada"],
    summary="Validação de Formato",
    response_model=FormatValidationResponse
)
async def validate_format(
    cnpj: str = Query(..., description="CNPJ formatado", example="11.222.333/0001-81")
):
    """
    Validação de formato detalhada.

    Verifica:
    - Formato XX.XXX.XXX/XXXX-XX
    - Separadores nas posições corretas
    - Ausência de caracteres especiais inválidos
    - Ausência de espaços em branco
    """
    errors = []

    format_result = AlphanumericCNPJValidator.validate_format(cnpj)
    separators_result = AlphanumericCNPJValidator.validate_separator_positions(cnpj)
    special_chars_result = AlphanumericCNPJValidator.validate_special_characters(cnpj)
    whitespace_result = AlphanumericCNPJValidator.validate_whitespace(cnpj)
    matriz_filial_result = AlphanumericCNPJValidator.validate_matriz_filial(cnpj)

    format_valid = format_result.get('valid', False)
    separators_valid = separators_result.get('valid', False)
    special_chars_valid = special_chars_result.get('valid', False)
    whitespace_valid = whitespace_result.get('valid', False)

    all_results = [
        format_result, separators_result, special_chars_result,
        whitespace_result, matriz_filial_result
    ]
    for result in all_results:
        errors.extend(result.get('errors', []))

    tipo = None
    if matriz_filial_result.get('valid'):
        tipo = TipoEstabelecimento.MATRIZ if matriz_filial_result.get(
            'is_matriz') else TipoEstabelecimento.FILIAL

    parts = AlphanumericCNPJValidator.extract_parts(cnpj)
    all_valid = all([format_valid, separators_valid, special_chars_valid, whitespace_valid])

    return FormatValidationResponse(
        valid=all_valid,
        format_valid=format_valid,
        separators_valid=separators_valid,
        special_chars_valid=special_chars_valid,
        whitespace_valid=whitespace_valid,
        tipo=tipo,
        parts=parts,
        errors=errors
    )


# =============================================================================
# NOVO FORMATO (2026+)
# =============================================================================

@app.get(
    "/api/v1/new-format/info",
    tags=["Novo Formato (2026+)"],
    summary="Sobre o Novo Formato"
)
async def get_new_format_info():
    """
    Informações sobre o novo formato de CNPJ alfanumérico.

    A Receita Federal definiu que a partir de 2026, CNPJs poderão
    conter letras (A-Z) nos 8 primeiros caracteres (raiz).
    """
    return {
        "titulo": "Novo Formato de CNPJ Alfanumérico",
        "previsao": "2026",
        "motivo": "Esgotamento da capacidade de CNPJs numéricos",
        "formato": {
            "padrao": "AA.AAA.AAA/NNNN-DD",
            "raiz": "8 caracteres (A-Z e 0-9)",
            "ordem": "4 dígitos numéricos",
            "dv": "2 dígitos verificadores"
        },
        "conversao_letras": {
            "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16,
            "H": 17, "I": 18, "J": 19, "K": 20, "L": 21, "M": 22, "N": 23,
            "O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29, "U": 30,
            "V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35
        }
    }


@app.get(
    "/api/v1/new-format/validate",
    tags=["Novo Formato (2026+)"],
    summary="Validar CNPJ Alfanumérico",
    response_model=NewFormatValidationResponse
)
async def validate_new_format(
    cnpj: str = Query(..., description="CNPJ alfanumérico", example="ABCDE123000145")
):
    """
    Valida um CNPJ no novo formato alfanumérico.

    **Formato**: `AA.AAA.AAA/NNNN-DD` ou `AAAAAAAANNNNDD`

    - Raiz (8 chars): Letras A-Z e/ou números 0-9
    - Ordem (4 dígitos): Apenas números
    - DV (2 dígitos): Calculados com letras convertidas (A=10...Z=35)
    """
    result = NewAlphanumericCNPJValidator.validate(cnpj)
    cnpj_clean = NewAlphanumericCNPJValidator.remove_formatting(cnpj)

    root_valid = NewAlphanumericCNPJValidator.validate_root_chars(
        cnpj_clean).get('valid', False) if len(cnpj_clean) >= 8 else False
    order_valid = NewAlphanumericCNPJValidator.validate_order_digits(
        cnpj_clean).get('valid', False) if len(cnpj_clean) >= 12 else False

    dv_valid = False
    if root_valid and order_valid and len(cnpj_clean) == 14:
        dv_valid = NewAlphanumericCNPJValidator.validate_check_digits(
            cnpj_clean).get('valid', False)

    return NewFormatValidationResponse(
        valid=result.get('valid', False),
        is_alphanumeric=result.get('is_alphanumeric', False),
        is_matriz=result.get('is_matriz'),
        cnpj_formatted=result.get('cnpj_formatted', ''),
        cnpj_clean=result.get('cnpj_clean', ''),
        root_valid=root_valid,
        order_valid=order_valid,
        dv_valid=dv_valid,
        parts=result.get('parts'),
        errors=result.get('errors', [])
    )


@app.post(
    "/api/v1/new-format/generate",
    tags=["Novo Formato (2026+)"],
    summary="Gerar CNPJ Alfanumérico",
    response_model=GenerateCNPJResponse
)
async def generate_new_format(
    raiz: Optional[str] = Query(
        None, description="Raiz personalizada (8 chars)", example="ABCD1234", max_length=8)
):
    """
    Gera um CNPJ alfanumérico válido.

    - **Sem raiz**: Gera aleatoriamente com letras e números
    - **Com raiz**: Usa a raiz informada e calcula os DVs

    **Atenção**: CNPJs gerados são fictícios, apenas para testes.
    """
    if raiz:
        raiz_clean = raiz.upper().replace('.', '').replace('-', '').replace('/', '')
        if len(raiz_clean) > 8:
            raise HTTPException(status_code=400, detail="Raiz deve ter no máximo 8 caracteres")

        invalid = [c for c in raiz_clean if c not in NewAlphanumericCNPJValidator.VALID_ROOT_CHARS]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Caracteres inválidos: {invalid}")

    cnpj_formatted = NewAlphanumericCNPJValidator.generate_valid_cnpj(raiz)
    cnpj_clean = NewAlphanumericCNPJValidator.remove_formatting(cnpj_formatted)
    validation = NewAlphanumericCNPJValidator.validate(cnpj_formatted)

    return GenerateCNPJResponse(
        cnpj_formatted=cnpj_formatted,
        cnpj_clean=cnpj_clean,
        raiz=cnpj_clean[:8],
        is_alphanumeric=validation.get('is_alphanumeric', False)
    )


@app.get(
    "/api/v1/new-format/calculate-dv",
    tags=["Novo Formato (2026+)"],
    summary="Calcular DVs"
)
async def calculate_dv(
    base: str = Query(..., description="12 caracteres (raiz + ordem)", example="ABCD12340001")
):
    """
    Calcula os dígitos verificadores para uma base de CNPJ alfanumérico.

    **Entrada**: 8 caracteres da raiz + 4 dígitos da ordem

    **Saída**: Os 2 dígitos verificadores calculados
    """
    base_clean = NewAlphanumericCNPJValidator.remove_formatting(base)

    if len(base_clean) < 12:
        detail_msg = f"Forneça 12 caracteres (raiz + ordem). Recebido: {len(base_clean)}"
        raise HTTPException(status_code=400, detail=detail_msg)

    base_clean = base_clean[:12]

    root_result = NewAlphanumericCNPJValidator.validate_root_chars(base_clean)
    if not root_result.get('valid', False):
        raise HTTPException(
            status_code=400, detail=f"Raiz inválida: {root_result.get('errors', [])}")

    if not base_clean[8:12].isdigit():
        raise HTTPException(status_code=400, detail="Ordem (posições 9-12) deve ser numérica")

    dv1 = NewAlphanumericCNPJValidator.calculate_first_digit(base_clean)
    dv2 = NewAlphanumericCNPJValidator.calculate_second_digit(base_clean + str(dv1))

    cnpj_complete = base_clean + str(dv1) + str(dv2)

    return {
        "base": base_clean,
        "dv1": dv1,
        "dv2": dv2,
        "dv": f"{dv1}{dv2}",
        "cnpj_complete": cnpj_complete,
        "cnpj_formatted": NewAlphanumericCNPJValidator.format_cnpj(cnpj_complete)
    }


# =============================================================================
# CONSULTA RECEITA FEDERAL
# =============================================================================

@app.get(
    "/api/v1/consulta",
    tags=["Consulta Receita Federal"],
    summary="Consultar Dados Cadastrais",
    response_model=CNPJInfoResponse
)
async def consultar_cnpj(
    cnpj: str = Query(..., description="CNPJ a consultar", example="11222333000181")
):
    """
    Consulta dados cadastrais de um CNPJ na Receita Federal.

    **Atenção**: Depende de API externa (BrasilAPI). Pode haver indisponibilidade.
    """
    if not CNPJValidator.is_valid(cnpj):
        raise HTTPException(status_code=400, detail="CNPJ inválido")

    try:
        api = ReceitaFederalAPI()
        dados = api.consultar(cnpj)

        return CNPJInfoResponse(
            cnpj=dados.cnpj,
            razao_social=dados.razao_social,
            nome_fantasia=dados.nome_fantasia,
            situacao_cadastral=dados.situacao_cadastral,
            tipo_estabelecimento="Matriz" if dados.is_matriz() else "Filial",
            data_abertura=dados.data_abertura,
            endereco=dados.get_endereco_completo(),
            municipio=dados.municipio,
            uf=dados.uf,
            telefone=dados.telefone,
            email=dados.email,
            atividade_principal=dados.atividade_principal
        )
    except ReceitaFederalAPIError as e:
        if "não encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail="CNPJ não encontrado")
        raise HTTPException(status_code=503, detail=f"Serviço indisponível: {e}")


@app.get(
    "/api/v1/consulta/situacao",
    tags=["Consulta Receita Federal"],
    summary="Verificar Situação Cadastral"
)
async def verificar_situacao(
    cnpj: str = Query(..., description="CNPJ a verificar", example="11222333000181")
):
    """
    Verifica rapidamente a situação cadastral de um CNPJ.

    Situações possíveis: ATIVA, BAIXADA, INAPTA, SUSPENSA
    """
    if not CNPJValidator.is_valid(cnpj):
        raise HTTPException(status_code=400, detail="CNPJ inválido")

    try:
        api = ReceitaFederalAPI()
        situacao = api.verificar_situacao(cnpj)

        return {
            "cnpj": CNPJValidator.format(cnpj),
            "situacao": situacao.get("situacao", "Desconhecida"),
            "ativa": situacao.get("ativa", False)
        }
    except ReceitaFederalAPIError as e:
        if "não encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail="CNPJ não encontrado")
        raise HTTPException(status_code=503, detail=str(e))


# =============================================================================
# UTILITÁRIOS
# =============================================================================

@app.get(
    "/api/v1/format",
    tags=["Utilitários"],
    summary="Formatar CNPJ"
)
async def format_cnpj(
    cnpj: str = Query(..., description="CNPJ a formatar (14 dígitos)", example="11222333000181")
):
    """
    Formata um CNPJ no padrão XX.XXX.XXX/XXXX-XX.
    """
    formatted = CNPJValidator.format(cnpj)

    if not formatted:
        raise HTTPException(
            status_code=400, detail="Não foi possível formatar. Verifique se possui 14 dígitos.")

    return {
        "original": cnpj,
        "formatted": formatted
    }


@app.get(
    "/api/v1/generate",
    tags=["Utilitários"],
    summary="Gerar CNPJ Válido (Tradicional)"
)
async def generate_cnpj(
    tipo: str = Query("matriz", description="Tipo: matriz ou filial", enum=["matriz", "filial"])
):
    """
    Gera um CNPJ numérico tradicional válido.

    **Atenção**: CNPJs gerados são fictícios, apenas para testes.
    """
    import random

    # Gera 8 dígitos da raiz
    raiz = ''.join([str(random.randint(0, 9)) for _ in range(8)])

    # Define ordem (0001 para matriz, aleatório para filial)
    ordem = "0001" if tipo == "matriz" else f"{random.randint(2, 9999):04d}"

    base = raiz + ordem

    # Calcula DVs
    dv1 = NumericCNPJValidator.calculate_first_digit(base)
    dv2 = NumericCNPJValidator.calculate_second_digit(base + str(dv1))

    cnpj = base + str(dv1) + str(dv2)

    return {
        "cnpj": cnpj,
        "cnpj_formatted": CNPJValidator.format(cnpj),
        "tipo": tipo
    }


# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
