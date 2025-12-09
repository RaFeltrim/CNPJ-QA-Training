"""
Exemplo simples de uso do validador de CNPJ
"""

import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cnpj_validator import CNPJValidator


def main():
    """Exemplo básico de validação de CNPJ."""
    
    print("=" * 60)
    print("  EXEMPLO SIMPLES - VALIDADOR DE CNPJ")
    print("=" * 60)
    
    # Criar instância do validador
    validator = CNPJValidator()
    
    # Lista de CNPJs para testar
    cnpjs = [
        "11.222.333/0001-81",  # Válido
        "11222333000181",      # Válido sem formatação
        "00.000.000/0000-00",  # Inválido
    ]
    
    print("\nTestando CNPJs:\n")
    
    for cnpj in cnpjs:
        # Validar
        result = validator.validate(cnpj)
        
        # Mostrar resultado
        status = "✓ VÁLIDO" if result['valid'] else "✗ INVÁLIDO"
        print(f"CNPJ: {cnpj:25} → {status}")
        
        if not result['valid']:
            print(f"  Erros: {', '.join(result['errors'])}")
        else:
            print(f"  Formatado: {result['cnpj_formatted']}")
        
        print()
    
    print("=" * 60)


if __name__ == "__main__":
    main()
