#!/usr/bin/env python3
"""
CNPJ Validator CLI - Interface de Linha de Comando

Ferramenta completa para validação, geração e consulta de CNPJs
com suporte ao novo formato alfanumérico (2026).

Uso:
    cnpj-validator validate <cnpj>
    cnpj-validator generate [--alphanumeric] [--root=XXXXXXXX] [--count=N]
    cnpj-validator format <cnpj>
    cnpj-validator info <cnpj>
    cnpj-validator batch <arquivo>
"""

import argparse
import sys
import json
from typing import List, Optional

try:
    from cnpj_validator import CNPJValidator
    from cnpj_validator.validators.new_alphanumeric_validator import NewAlphanumericCNPJValidator
except ImportError:
    # Fallback para importação relativa durante desenvolvimento
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from cnpj_validator import CNPJValidator
    from cnpj_validator.validators.new_alphanumeric_validator import NewAlphanumericCNPJValidator


class CNPJValidatorCLI:
    """Interface de linha de comando para o CNPJ Validator."""
    
    def __init__(self):
        self.validator = CNPJValidator()
        self.alphanumeric_validator = NewAlphanumericCNPJValidator()
    
    def validate(self, cnpj: str, verbose: bool = False) -> dict:
        """
        Valida um CNPJ.
        
        Args:
            cnpj: CNPJ a ser validado
            verbose: Se True, retorna informações detalhadas
            
        Returns:
            Dicionário com resultado da validação
        """
        result = self.validator.validate(cnpj)
        
        if verbose:
            return result
        
        return {
            'valid': result['valid'],
            'cnpj': result.get('cnpj_formatted', cnpj),
            'errors': result.get('errors', [])
        }
    
    def generate(
        self,
        count: int = 1,
        alphanumeric: bool = False,
        root: Optional[str] = None,
        formatted: bool = True
    ) -> List[str]:
        """
        Gera CNPJs válidos para testes.
        
        Args:
            count: Quantidade de CNPJs a gerar
            alphanumeric: Se True, gera CNPJs alfanuméricos
            root: Raiz específica para o CNPJ
            formatted: Se True, retorna formatado
            
        Returns:
            Lista de CNPJs gerados
        """
        cnpjs = []
        
        for _ in range(count):
            if root:
                cnpj = self.alphanumeric_validator.generate_valid_cnpj(root)
            elif alphanumeric:
                import random
                import string
                chars = string.ascii_uppercase + string.digits
                random_root = ''.join(random.choices(chars, k=8))
                cnpj = self.alphanumeric_validator.generate_valid_cnpj(random_root)
            else:
                import random
                random_root = ''.join([str(random.randint(0, 9)) for _ in range(8)])
                cnpj = self.alphanumeric_validator.generate_valid_cnpj(random_root)
            
            if formatted:
                cnpj = self._format_cnpj(cnpj)
            
            cnpjs.append(cnpj)
        
        return cnpjs
    
    def _format_cnpj(self, cnpj: str) -> str:
        """Formata um CNPJ."""
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '').upper()
        if len(cnpj) != 14:
            return cnpj
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"
    
    def format(self, cnpj: str) -> str:
        """
        Formata um CNPJ.
        
        Args:
            cnpj: CNPJ a ser formatado
            
        Returns:
            CNPJ formatado
        """
        return self._format_cnpj(cnpj)
    
    def info(self, cnpj: str) -> dict:
        """
        Retorna informações detalhadas do CNPJ.
        
        Args:
            cnpj: CNPJ a consultar
            
        Returns:
            Dicionário com informações
        """
        return self.validator.get_cnpj_info(cnpj)
    
    def batch_validate(self, file_path: str) -> List[dict]:
        """
        Valida múltiplos CNPJs de um arquivo.
        
        Args:
            file_path: Caminho para arquivo com CNPJs (um por linha)
            
        Returns:
            Lista de resultados
        """
        results = []
        
        with open(file_path, 'r') as f:
            for line in f:
                cnpj = line.strip()
                if cnpj:
                    result = self.validate(cnpj)
                    results.append(result)
        
        return results


def create_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos."""
    
    parser = argparse.ArgumentParser(
        prog='cnpj-validator',
        description='Validador de CNPJ brasileiro com suporte ao formato alfanumérico 2026',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos:
  cnpj-validator validate 11.222.333/0001-81
  cnpj-validator generate --count 5
  cnpj-validator generate --alphanumeric
  cnpj-validator format 11222333000181
  cnpj-validator info 11.222.333/0001-81
  cnpj-validator batch cnpjs.txt

Mais informações: https://github.com/RaFeltrim/CNPJ-QA-Training
        '''
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 2.0.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando: validate
    validate_parser = subparsers.add_parser('validate', help='Valida um CNPJ')
    validate_parser.add_argument('cnpj', help='CNPJ a ser validado')
    validate_parser.add_argument(
        '--verbose', '-V',
        action='store_true',
        help='Mostra informações detalhadas'
    )
    validate_parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Saída em formato JSON'
    )
    
    # Comando: generate
    generate_parser = subparsers.add_parser('generate', help='Gera CNPJs válidos para testes')
    generate_parser.add_argument(
        '--count', '-n',
        type=int,
        default=1,
        help='Quantidade de CNPJs a gerar (padrão: 1)'
    )
    generate_parser.add_argument(
        '--alphanumeric', '-a',
        action='store_true',
        help='Gera CNPJs alfanuméricos (formato 2026)'
    )
    generate_parser.add_argument(
        '--root', '-r',
        type=str,
        help='Raiz específica para o CNPJ (8 caracteres)'
    )
    generate_parser.add_argument(
        '--no-format',
        action='store_true',
        help='Retorna sem formatação'
    )
    generate_parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Saída em formato JSON'
    )
    
    # Comando: format
    format_parser = subparsers.add_parser('format', help='Formata um CNPJ')
    format_parser.add_argument('cnpj', help='CNPJ a ser formatado')
    
    # Comando: info
    info_parser = subparsers.add_parser('info', help='Mostra informações do CNPJ')
    info_parser.add_argument('cnpj', help='CNPJ a consultar')
    info_parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Saída em formato JSON'
    )
    
    # Comando: batch
    batch_parser = subparsers.add_parser('batch', help='Valida CNPJs em lote')
    batch_parser.add_argument('file', help='Arquivo com CNPJs (um por linha)')
    batch_parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Saída em formato JSON'
    )
    batch_parser.add_argument(
        '--summary', '-s',
        action='store_true',
        help='Mostra apenas resumo'
    )
    
    return parser


def main():
    """Função principal do CLI."""
    
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    cli = CNPJValidatorCLI()
    
    try:
        if args.command == 'validate':
            result = cli.validate(args.cnpj, verbose=args.verbose)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                if result['valid']:
                    print(f"✅ CNPJ válido: {result['cnpj']}")
                else:
                    print(f"❌ CNPJ inválido: {args.cnpj}")
                    for error in result.get('errors', []):
                        print(f"   └─ {error}")
                sys.exit(0 if result['valid'] else 1)
        
        elif args.command == 'generate':
            cnpjs = cli.generate(
                count=args.count,
                alphanumeric=args.alphanumeric,
                root=args.root,
                formatted=not args.no_format
            )
            
            if args.json:
                print(json.dumps(cnpjs, indent=2))
            else:
                for cnpj in cnpjs:
                    print(cnpj)
        
        elif args.command == 'format':
            formatted = cli.format(args.cnpj)
            print(formatted)
        
        elif args.command == 'info':
            info = cli.info(args.cnpj)
            
            if args.json:
                print(json.dumps(info, indent=2, ensure_ascii=False))
            else:
                if info.get('valid'):
                    print(f"📋 Informações do CNPJ: {info.get('cnpj_formatted', args.cnpj)}")
                    print(f"   ├─ Raiz: {info.get('parts', {}).get('raiz', 'N/A')}")
                    print(f"   ├─ Filial: {info.get('parts', {}).get('filial', 'N/A')}")
                    print(f"   ├─ DV: {info.get('parts', {}).get('dv', 'N/A')}")
                    matriz_info = info.get('matriz_filial', {})
                    tipo = 'Matriz' if matriz_info.get('is_matriz') else f"Filial #{matriz_info.get('numero_filial', 'N/A')}"
                    print(f"   └─ Tipo: {tipo}")
                else:
                    print(f"❌ CNPJ inválido: {args.cnpj}")
                    for error in info.get('errors', []):
                        print(f"   └─ {error}")
                    sys.exit(1)
        
        elif args.command == 'batch':
            results = cli.batch_validate(args.file)
            
            if args.summary:
                total = len(results)
                valid = sum(1 for r in results if r['valid'])
                invalid = total - valid
                print(f"📊 Resumo da validação em lote:")
                print(f"   ├─ Total: {total}")
                print(f"   ├─ Válidos: {valid} ({valid/total*100:.1f}%)")
                print(f"   └─ Inválidos: {invalid} ({invalid/total*100:.1f}%)")
            elif args.json:
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                for result in results:
                    status = "✅" if result['valid'] else "❌"
                    print(f"{status} {result['cnpj']}")
                
                # Resumo no final
                total = len(results)
                valid = sum(1 for r in results if r['valid'])
                print(f"\n📊 {valid}/{total} CNPJs válidos")
    
    except FileNotFoundError as e:
        print(f"❌ Erro: Arquivo não encontrado - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
