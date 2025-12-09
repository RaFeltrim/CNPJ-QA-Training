"""
Exemplo de uso da API da Receita Federal
Demonstra como consultar dados cadastrais de empresas
"""

import sys
import os

# Adicionar o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cnpj_validator import CNPJValidator, ReceitaFederalAPI, ReceitaFederalAPIError


def print_section(title: str):
    """Imprime um cabeçalho de seção."""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def exemplo_validacao_e_consulta():
    """
    Demonstra o fluxo completo: validar CNPJ localmente e consultar na API.
    """
    print_section("1. VALIDAÇÃO LOCAL + CONSULTA NA API")
    
    # Inicializar validador e cliente da API
    validator = CNPJValidator()
    api = ReceitaFederalAPI()
    
    # CNPJ para testar (substitua por um CNPJ válido real para testar)
    cnpj = "00.000.000/0001-91"  # CNPJ da Receita Federal (exemplo)
    
    print(f"CNPJ a validar: {cnpj}")
    print("-" * 40)
    
    # Passo 1: Validar localmente
    print("\n📋 Passo 1: Validação Local")
    resultado = validator.validate(cnpj)
    
    if not resultado['valid']:
        print(f"❌ CNPJ inválido: {', '.join(resultado['errors'])}")
        print("   Não é necessário consultar a API.")
        return
    
    print(f"✅ CNPJ válido localmente")
    print(f"   CNPJ limpo: {resultado['cnpj_clean']}")
    print(f"   CNPJ formatado: {resultado['cnpj_formatted']}")
    
    # Passo 2: Consultar na API
    print("\n🌐 Passo 2: Consulta na API da Receita Federal")
    print("   (Aguarde, respeitando rate limit da API...)")
    
    try:
        dados = api.consultar(resultado['cnpj_clean'])
        
        print(f"\n✅ Dados obtidos com sucesso!")
        print("-" * 40)
        print(f"📌 Razão Social: {dados.razao_social}")
        print(f"📌 Nome Fantasia: {dados.nome_fantasia or '(não informado)'}")
        print(f"📌 Situação: {dados.situacao_cadastral}")
        print(f"📌 Data Abertura: {dados.data_abertura}")
        print(f"📌 CNAE Principal: {dados.cnae_principal.get('descricao', 'N/A')}")
        print(f"📌 Capital Social: R$ {dados.capital_social:,.2f}")
        print(f"📌 É Matriz: {'Sim' if dados.is_matriz() else 'Não (Filial)'}")
        print(f"📌 Simples Nacional: {'Sim' if dados.simples_nacional.get('optante') else 'Não'}")
        print(f"📌 MEI: {'Sim' if dados.mei else 'Não'}")
        
        if dados.endereco:
            print(f"\n📍 Endereço:")
            print(f"   {dados.get_endereco_completo()}")
        
        if dados.quadro_societario:
            print(f"\n👥 Quadro Societário ({len(dados.quadro_societario)} sócio(s)):")
            for socio in dados.quadro_societario[:5]:  # Mostrar até 5 sócios
                print(f"   - {socio.get('nome', 'N/A')} ({socio.get('qualificacao', 'N/A')})")
        
    except ReceitaFederalAPIError as e:
        print(f"\n❌ Erro na consulta: {e}")
        if e.status_code == 404:
            print("   O CNPJ não foi encontrado na base da Receita Federal.")
        elif e.status_code == 429:
            print("   Rate limit excedido. Aguarde alguns segundos e tente novamente.")


def exemplo_verificar_situacao():
    """
    Demonstra como verificar apenas a situação cadastral.
    """
    print_section("2. VERIFICAR SITUAÇÃO CADASTRAL")
    
    api = ReceitaFederalAPI()
    
    # CNPJ para verificar
    cnpj = "00.000.000/0001-91"
    
    print(f"Verificando situação do CNPJ: {cnpj}")
    
    try:
        situacao = api.verificar_situacao(cnpj)
        
        print(f"\n📋 Resultado:")
        print(f"   CNPJ: {situacao['cnpj']}")
        print(f"   Situação: {situacao['situacao']}")
        print(f"   Ativa: {'✅ Sim' if situacao['ativa'] else '❌ Não'}")
        print(f"   Data da Situação: {situacao['data_situacao']}")
        
    except ReceitaFederalAPIError as e:
        print(f"\n❌ Erro: {e}")


def exemplo_buscar_socios():
    """
    Demonstra como buscar o quadro societário.
    """
    print_section("3. BUSCAR QUADRO SOCIETÁRIO")
    
    api = ReceitaFederalAPI()
    
    # CNPJ para buscar sócios
    cnpj = "00.000.000/0001-91"
    
    print(f"Buscando sócios do CNPJ: {cnpj}")
    
    try:
        socios = api.buscar_socios(cnpj)
        
        if socios:
            print(f"\n👥 {len(socios)} sócio(s) encontrado(s):\n")
            for i, socio in enumerate(socios, 1):
                print(f"   {i}. {socio.get('nome', 'N/A')}")
                print(f"      Qualificação: {socio.get('qualificacao', 'N/A')}")
                if socio.get('data_entrada'):
                    print(f"      Entrada: {socio['data_entrada']}")
                print()
        else:
            print("\n   Nenhum sócio encontrado.")
        
    except ReceitaFederalAPIError as e:
        print(f"\n❌ Erro: {e}")


def exemplo_uso_basico():
    """
    Exemplo mais simples de uso.
    """
    print_section("4. EXEMPLO BÁSICO")
    
    print("Código de exemplo:")
    print("-" * 40)
    print("""
from cnpj_validator import CNPJValidator, ReceitaFederalAPI

# Validar localmente
validator = CNPJValidator()
if CNPJValidator.is_valid("11.222.333/0001-81"):
    print("CNPJ válido!")

# Consultar na Receita Federal
api = ReceitaFederalAPI()
dados = api.consultar("11222333000181")
print(f"Empresa: {dados.razao_social}")
print(f"Ativa: {dados.is_ativa()}")
""")


def exemplo_tratamento_erros():
    """
    Demonstra tratamento de erros da API.
    """
    print_section("5. TRATAMENTO DE ERROS")
    
    api = ReceitaFederalAPI()
    
    cnpjs_teste = [
        ("12345", "CNPJ com formato inválido"),
        ("00000000000000", "CNPJ com todos dígitos iguais"),
        ("99999999999999", "CNPJ provavelmente inexistente"),
    ]
    
    for cnpj, descricao in cnpjs_teste:
        print(f"\n📋 Testando: {descricao}")
        print(f"   CNPJ: {cnpj}")
        
        try:
            dados = api.consultar(cnpj)
            print(f"   ✅ Encontrado: {dados.razao_social}")
        except ValueError as e:
            print(f"   ⚠️ Erro de validação: {e}")
        except ReceitaFederalAPIError as e:
            print(f"   ❌ Erro da API: {e}")
            if e.status_code:
                print(f"      Status HTTP: {e.status_code}")


def main():
    """Executa os exemplos."""
    print("\n" + "=" * 80)
    print("   DEMONSTRAÇÃO: API DA RECEITA FEDERAL")
    print("   CNPJ Validator v2.0.0")
    print("=" * 80)
    
    print("\n⚠️  ATENÇÃO: As APIs públicas têm rate limit.")
    print("    Aguarde entre as consultas para evitar bloqueio.")
    print("    Os exemplos usam CNPJs fictícios para demonstração.")
    
    # Executar exemplos
    exemplo_uso_basico()
    
    # Para testar com consultas reais, descomente as linhas abaixo:
    # exemplo_validacao_e_consulta()
    # exemplo_verificar_situacao()
    # exemplo_buscar_socios()
    # exemplo_tratamento_erros()
    
    print("\n" + "=" * 80)
    print("   Para executar consultas reais, edite este arquivo e")
    print("   descomente as funções desejadas na função main().")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
