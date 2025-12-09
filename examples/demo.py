"""
Exemplos de Uso do Sistema de Validação de CNPJ
Demonstra as funcionalidades dos validadores numérico e alfanumérico
"""

import sys
import os

# Adicionar o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cnpj_validator import CNPJValidator
from src.cnpj_validator.validators.numeric_validator import NumericCNPJValidator
from src.cnpj_validator.validators.alphanumeric_validator import AlphanumericCNPJValidator


def print_section(title: str):
    """Imprime um cabeçalho de seção."""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def print_result(cnpj: str, result: dict):
    """Imprime o resultado da validação de forma formatada."""
    print(f"CNPJ: {cnpj}")
    print(f"Válido: {'✓ SIM' if result['valid'] else '✗ NÃO'}")
    
    if result.get('errors'):
        print(f"Erros: {', '.join(result['errors'])}")
    
    if result.get('warnings'):
        print(f"Avisos: {', '.join(result['warnings'])}")
    
    if result.get('cnpj_clean'):
        print(f"CNPJ Limpo: {result['cnpj_clean']}")
    
    if result.get('cnpj_formatted'):
        print(f"CNPJ Formatado: {result['cnpj_formatted']}")
    
    print("-" * 80)


def exemplo_validacao_completa():
    """Demonstra validação completa usando CNPJValidator."""
    print_section("1. VALIDAÇÃO COMPLETA (Numérica + Alfanumérica)")
    
    validator = CNPJValidator()
    
    # CNPJs de teste
    cnpjs_teste = [
        "11.222.333/0001-81",  # Válido e formatado
        "11222333000181",      # Válido sem formatação
        "00.000.000/0000-00",  # Inválido - todos zeros
        "11.222.333/0001-82",  # Inválido - DV errado
        "11.222.333/0000-81",  # Inválido - código matriz/filial 0000
        "  11.222.333/0001-81  ",  # Com espaços
    ]
    
    for cnpj in cnpjs_teste:
        result = validator.validate(cnpj, validate_format=True)
        print_result(cnpj, result)


def exemplo_validacao_numerica():
    """Demonstra validação apenas numérica."""
    print_section("2. VALIDAÇÃO NUMÉRICA ISOLADA")
    
    validator = NumericCNPJValidator()
    
    cnpjs_teste = [
        "11.222.333/0001-81",
        "11222333000181",
        "1122233300018",      # Tamanho incorreto
        "11111111111111",     # Todos dígitos iguais
        "11.222.333/0001-99", # Dígitos verificadores incorretos
    ]
    
    for cnpj in cnpjs_teste:
        result = validator.validate(cnpj)
        print_result(cnpj, result)


def exemplo_validacao_alfanumerica():
    """Demonstra validação apenas alfanumérica."""
    print_section("3. VALIDAÇÃO ALFANUMÉRICA ISOLADA")
    
    validator = AlphanumericCNPJValidator()
    
    cnpjs_teste = [
        "11.222.333/0001-81",  # Formato correto
        "11222333000181",      # Sem formatação
        "11.222.333-0001/81",  # Separadores na ordem errada
        "11.222.333/0001.81",  # Separador incorreto
        "11.222.333/0001-8A",  # Caractere inválido
        "11 222 333/0001-81",  # Espaços em vez de pontos
    ]
    
    for cnpj in cnpjs_teste:
        result = validator.validate(cnpj)
        print_result(cnpj, result)


def exemplo_formatacao():
    """Demonstra formatação de CNPJ."""
    print_section("4. FORMATAÇÃO DE CNPJ")
    
    validator = CNPJValidator()
    
    cnpjs_teste = [
        "11222333000181",
        "11.222.333/0001-81",
        "11-222-333-0001-81",
    ]
    
    print("Formatando CNPJs:\n")
    for cnpj in cnpjs_teste:
        formatted = validator.format(cnpj)
        print(f"Input:  {cnpj}")
        print(f"Output: {formatted}")
        print("-" * 80)


def exemplo_limpeza():
    """Demonstra remoção de formatação."""
    print_section("5. LIMPEZA DE CNPJ (Remoção de Formatação)")
    
    validator = CNPJValidator()
    
    cnpjs_teste = [
        "11.222.333/0001-81",
        "11-222-333-0001-81",
        "11 222 333 0001 81",
        "11222333000181",
    ]
    
    print("Removendo formatação:\n")
    for cnpj in cnpjs_teste:
        clean = validator.clean(cnpj)
        print(f"Input:  {cnpj}")
        print(f"Output: {clean}")
        print("-" * 80)


def exemplo_informacoes_detalhadas():
    """Demonstra extração de informações detalhadas."""
    print_section("6. INFORMAÇÕES DETALHADAS DO CNPJ")
    
    validator = CNPJValidator()
    
    cnpjs_teste = [
        "11.222.333/0001-81",  # Matriz
        "11.222.333/0002-62",  # Filial
    ]
    
    for cnpj in cnpjs_teste:
        info = validator.get_info(cnpj)
        print(f"CNPJ: {cnpj}\n")
        
        if info['valid']:
            print(f"✓ CNPJ Válido")
            print(f"Formatado: {info['cnpj_formatted']}")
            print(f"Limpo: {info['cnpj_clean']}")
            
            if 'matriz_filial' in info:
                mf_info = info['matriz_filial']
                print(f"Tipo: {mf_info['type'].upper()}")
                if 'code' in mf_info:
                    print(f"Código: {mf_info['code']}")
            
            if 'parts' in info:
                parts = info['parts']
                print(f"\nPartes do CNPJ:")
                print(f"  - Raiz: {parts['raiz']}")
                print(f"  - Ordem: {parts['ordem']}")
                print(f"  - DV: {parts['dv']}")
        else:
            print(f"✗ CNPJ Inválido")
            print(f"Erros: {', '.join(info['errors'])}")
        
        print("-" * 80)


def exemplo_validacao_rapida():
    """Demonstra método de validação rápida."""
    print_section("7. VALIDAÇÃO RÁPIDA (Método Estático)")
    
    cnpjs_teste = [
        "11.222.333/0001-81",
        "11222333000181",
        "00.000.000/0000-00",
        "11111111111111",
    ]
    
    print("Validação rápida (retorna apenas True/False):\n")
    for cnpj in cnpjs_teste:
        is_valid = CNPJValidator.is_valid(cnpj)
        status = "✓ VÁLIDO" if is_valid else "✗ INVÁLIDO"
        print(f"{cnpj:25} → {status}")
    
    print("-" * 80)


def exemplo_calculo_digitos():
    """Demonstra cálculo de dígitos verificadores."""
    print_section("8. CÁLCULO DE DÍGITOS VERIFICADORES")
    
    validator = NumericCNPJValidator()
    
    # CNPJ base sem dígitos verificadores
    cnpj_base = "11222333000181"
    
    print(f"CNPJ Base (12 dígitos): {cnpj_base[:12]}\n")
    
    primeiro_digito = validator.calculate_first_digit(cnpj_base[:12])
    print(f"Primeiro Dígito Verificador: {primeiro_digito}")
    
    segundo_digito = validator.calculate_second_digit(cnpj_base[:13])
    print(f"Segundo Dígito Verificador: {segundo_digito}")
    
    print(f"\nCNPJ Completo: {cnpj_base[:12]}{primeiro_digito}{segundo_digito}")
    print(f"CNPJ Formatado: {validator.format_cnpj(cnpj_base[:12] + str(primeiro_digito) + str(segundo_digito))}")
    print("-" * 80)


def exemplo_matriz_filial():
    """Demonstra validação de códigos matriz/filial."""
    print_section("9. VALIDAÇÃO DE MATRIZ E FILIAL")
    
    validator = AlphanumericCNPJValidator()
    
    cnpjs_teste = [
        "11.222.333/0001-81",  # Matriz
        "11.222.333/0002-62",  # Filial 2
        "11.222.333/0010-24",  # Filial 10
        "11.222.333/0000-00",  # Código inválido (0000)
    ]
    
    for cnpj in cnpjs_teste:
        result = validator.validate_matriz_filial(cnpj)
        print(f"CNPJ: {cnpj}")
        
        if result['valid']:
            info = result['info']
            print(f"✓ Código válido")
            print(f"Tipo: {info['type'].upper()}")
            if 'code' in info:
                print(f"Código: {info['code']}")
            if 'number' in info:
                print(f"Número da Filial: {info['number']}")
        else:
            print(f"✗ Código inválido")
            print(f"Erros: {', '.join(result['errors'])}")
        
        print("-" * 80)


def menu_interativo():
    """Menu interativo para testar validações."""
    print_section("10. MODO INTERATIVO - TESTE SEU CNPJ")
    
    validator = CNPJValidator()
    
    while True:
        print("\nDigite um CNPJ para validar (ou 'sair' para encerrar):")
        cnpj = input("CNPJ: ").strip()
        
        if cnpj.lower() in ['sair', 'exit', 'quit', 'q']:
            print("\nEncerrando modo interativo...\n")
            break
        
        if not cnpj:
            print("⚠ Por favor, digite um CNPJ válido.\n")
            continue
        
        print("\n" + "-" * 80)
        result = validator.validate(cnpj, validate_format=True)
        print_result(cnpj, result)
        
        if result['valid']:
            info = validator.get_info(cnpj)
            if 'matriz_filial' in info:
                mf_info = info['matriz_filial']
                print(f"📊 Tipo: {mf_info['type'].upper()}")


def main():
    """Função principal que executa todos os exemplos."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "SISTEMA DE VALIDAÇÃO DE CNPJ" + " " * 30 + "║")
    print("║" + " " * 25 + "Exemplos de Uso" + " " * 38 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        # Executar exemplos
        exemplo_validacao_completa()
        exemplo_validacao_numerica()
        exemplo_validacao_alfanumerica()
        exemplo_formatacao()
        exemplo_limpeza()
        exemplo_informacoes_detalhadas()
        exemplo_validacao_rapida()
        exemplo_calculo_digitos()
        exemplo_matriz_filial()
        
        # Menu interativo
        resposta = input("\nDeseja testar CNPJs no modo interativo? (s/n): ").strip().lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            menu_interativo()
        
        print_section("FIM DOS EXEMPLOS")
        print("✓ Todos os exemplos foram executados com sucesso!")
        print("\nPara usar o sistema em seu código:")
        print("  from cnpj_validator import CNPJValidator")
        print("  validator = CNPJValidator()")
        print("  result = validator.validate('11.222.333/0001-81')")
        print()
        
    except Exception as e:
        print(f"\n❌ Erro durante a execução dos exemplos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
