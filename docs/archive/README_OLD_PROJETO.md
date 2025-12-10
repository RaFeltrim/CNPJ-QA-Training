# Sistema de Validação de CNPJ

Sistema completo de validação de CNPJ (Cadastro Nacional de Pessoa Jurídica) em Python, desenvolvido para servir como base de testes e treinamento em QA.

## Características

Este sistema oferece validação completa de CNPJ com separação entre:

- **Validação Numérica**: Verifica estrutura, tamanho e dígitos verificadores
- **Validação Alfanumérica**: Valida formatação, caracteres especiais e padrões

## Estrutura do Projeto

```
CNPJ-QA-Training/
├── cnpj_validator/
│   ├── __init__.py
│   ├── cnpj_validator.py          # Módulo principal
│   └── validators/
│       ├── __init__.py
│       ├── numeric_validator.py    # Validador numérico
│       └── alphanumeric_validator.py  # Validador alfanumérico
├── examples/
│   └── demo.py                     # Exemplos de uso
├── tests/                          # Diretório para testes (QA)
└── README.md
```

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/RaFeltrim/CNPJ-QA-Training.git
cd CNPJ-QA-Training
```

2. Não há dependências externas necessárias (usa apenas bibliotecas padrão do Python)

## Uso Básico

### Validação Completa

```python
from cnpj_validator import CNPJValidator

validator = CNPJValidator()

# Validar CNPJ formatado
result = validator.validate("11.222.333/0001-81")
print(result['valid'])  # True ou False

# Validar CNPJ sem formatação
result = validator.validate("11222333000181")
print(result['valid'])  # True ou False
```

### Validação Rápida

```python
from cnpj_validator import CNPJValidator

# Método estático para validação rápida
is_valid = CNPJValidator.is_valid("11.222.333/0001-81")
print(is_valid)  # True ou False
```

### Validação Apenas Numérica

```python
from cnpj_validator.validators.numeric_validator import NumericCNPJValidator

validator = NumericCNPJValidator()
result = validator.validate("11222333000181")

if result['valid']:
    print(f"CNPJ válido: {result['cnpj_clean']}")
else:
    print(f"Erros: {result['errors']}")
```

### Validação Apenas Alfanumérica

```python
from cnpj_validator.validators.alphanumeric_validator import AlphanumericCNPJValidator

validator = AlphanumericCNPJValidator()
result = validator.validate("11.222.333/0001-81")

if result['valid']:
    print("Formato correto!")
    print(f"Tipo: {result['filial_info']['type']}")  # matriz ou filial
else:
    print(f"Erros: {result['errors']}")
```

### Formatação e Limpeza

```python
from cnpj_validator import CNPJValidator

validator = CNPJValidator()

# Formatar CNPJ
formatted = validator.format("11222333000181")
print(formatted)  # 11.222.333/0001-81

# Limpar formatação
clean = validator.clean("11.222.333/0001-81")
print(clean)  # 11222333000181
```

### Obter Informações Detalhadas

```python
from cnpj_validator import CNPJValidator

validator = CNPJValidator()
info = validator.get_info("11.222.333/0001-81")

print(f"CNPJ Formatado: {info['cnpj_formatted']}")
print(f"Tipo: {info['matriz_filial']['type']}")  # matriz ou filial
print(f"Raiz: {info['parts']['raiz']}")
print(f"Ordem: {info['parts']['ordem']}")
print(f"DV: {info['parts']['dv']}")
```

## Executar Exemplos

Execute o arquivo de demonstração para ver todos os recursos em ação:

```bash
cd examples
python demo.py
```

O script de demonstração inclui:
1. Validação completa (numérica + alfanumérica)
2. Validação numérica isolada
3. Validação alfanumérica isolada
4. Formatação de CNPJ
5. Limpeza de CNPJ
6. Informações detalhadas
7. Validação rápida
8. Cálculo de dígitos verificadores
9. Validação de matriz/filial
10. Modo interativo

## Funcionalidades dos Validadores

### Validador Numérico (`NumericCNPJValidator`)

- Remove formatação (pontos, traços, barras)
- Valida tamanho (14 dígitos)
- Detecta CNPJs com todos dígitos iguais
- Calcula e valida dígitos verificadores
- Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX

### Validador Alfanumérico (`AlphanumericCNPJValidator`)

- Valida formato XX.XXX.XXX/XXXX-XX
- Verifica caracteres especiais válidos
- Valida posições dos separadores (. / -)
- Identifica matriz (0001) ou filial (0002+)
- Detecta espaços em branco indesejados
- Extrai partes do CNPJ (raiz, ordem, DV)

### Validador Principal (`CNPJValidator`)

- Integra validações numéricas e alfanuméricas
- Fornece relatórios detalhados de validação
- Oferece métodos de conveniência (format, clean, get_info)
- Suporte para validação parcial (apenas numérica ou alfanumérica)

## Uso para QA e Testes

Este projeto foi desenvolvido especificamente para treinamento de QA. Você pode:

1. **Criar casos de teste** baseados nas funcionalidades
2. **Testar cenários válidos e inválidos**
3. **Verificar tratamento de erros**
4. **Validar mensagens de erro**
5. **Testar edge cases** (valores limites, entradas inesperadas)

### Exemplos de Casos de Teste

```python
# Caso de teste: CNPJ válido
assert CNPJValidator.is_valid("11.222.333/0001-81") == True

# Caso de teste: CNPJ com todos dígitos iguais
assert CNPJValidator.is_valid("11111111111111") == False

# Caso de teste: CNPJ com tamanho incorreto
result = NumericCNPJValidator().validate("123456")
assert result['valid'] == False
assert "14 dígitos" in result['errors'][0]

# Caso de teste: Formato incorreto
result = AlphanumericCNPJValidator().validate("11-222-333-0001-81")
assert result['valid'] == False
```

## Estrutura de Resposta

Todas as validações retornam um dicionário estruturado:

```python
{
    'valid': bool,              # True se válido
    'cnpj_clean': str,          # CNPJ sem formatação
    'cnpj_formatted': str,      # CNPJ formatado
    'errors': list,             # Lista de erros
    'warnings': list,           # Lista de avisos
    'numeric_validation': dict, # Detalhes da validação numérica
    'alphanumeric_validation': dict  # Detalhes da validação alfanumérica
}
```

## Regras de Validação

### CNPJ Válido:
- Deve ter exatamente 14 dígitos
- Não pode ter todos os dígitos iguais
- Dígitos verificadores devem ser válidos
- Formato: XX.XXX.XXX/XXXX-XX (quando formatado)
- Código de matriz/filial não pode ser 0000

### Dígitos Verificadores:
O CNPJ possui 2 dígitos verificadores calculados com base nos 12 primeiros dígitos:
- **Primeiro DV**: Calculado com pesos 5,4,3,2,9,8,7,6,5,4,3,2
- **Segundo DV**: Calculado com pesos 6,5,4,3,2,9,8,7,6,5,4,3,2

## Contribuindo

Este é um projeto educacional para treinamento de QA. Contribuições são bem-vindas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## Documentação Adicional

Consulte os arquivos no repositório para mais informações:
- `01.Guia_cnpj_qa.md` - Guia completo de QA para CNPJ
- `02.Exercicios_cnpj.md` - Exercícios práticos
- `05.Casos_de_Teste_Realistas.md` - Casos de teste detalhados

## Licença

Este projeto é de código aberto e está disponível para fins educacionais.

## Autor

Rafael Feltrim - [@RaFeltrim](https://github.com/RaFeltrim)

## Objetivo Educacional

Este projeto serve como base para:
- Treinamento de QA Manual
- Prática de testes automatizados
- Aprendizado de validação de dados
- Estudo de padrões de teste
- Desenvolvimento de casos de teste

---

**Nota**: Este é um sistema educacional. Para uso em produção, considere adicionar mais validações e integrações com bases de dados oficiais da Receita Federal.
