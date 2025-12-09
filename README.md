# CNPJ Validator - Sistema de Validação e Treinamento para QA

[![Python](https://img.shields.io/badge/Python-3.8%2B%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Sistema completo de validação de CNPJ (Cadastro Nacional da Pessoa Jurídica) desenvolvido especificamente para **treinamento de profissionais de Quality Assurance**, combinando implementação funcional com material didático estruturado.

---

## Visão Geral

Este repositório oferece:

- **Biblioteca Python** para validação de CNPJ (numérico e alfanumérico)
- **Integração com API da Receita Federal** para consulta de dados cadastrais
- **Material de treinamento completo** com metodologia pedagógica Scaffolding
- **33 casos de teste realistas** com massa de dados
- **Guias técnicos detalhados** sobre legislação e algoritmo de validação
- **Integração CI/CD** com testes automatizados e Shift Left Testing

---

## Início Rápido

### Instalação

```bash
# Clone o repositório
git clone https://github.com/RaFeltrim/CNPJ-QA-Training.git
cd CNPJ-QA-Training

# Instale como pacote (opcional)
pip install -e .

# Ou use diretamente
python examples/quick-start.py
```

### Uso Básico

```python
from src.cnpj_validator import CNPJValidator, ReceitaFederalAPI

# Validação rápida
is_valid = CNPJValidator.is_valid("11.222.333/0001-81")
print(is_valid)  # True

# Validação completa com detalhes
validator = CNPJValidator()
result = validator.validate("11.222.333/0001-81")

if result['valid']:
    print(f"CNPJ válido: {result['cnpj_formatted']}")
else:
    print(f"Erros encontrados: {result['errors']}")
```

### Consulta na Receita Federal

```python
from src.cnpj_validator import ReceitaFederalAPI, ReceitaFederalAPIError

# Consultar dados cadastrais
api = ReceitaFederalAPI()

try:
    dados = api.consultar("11.222.333/0001-81")
    print(f"Empresa: {dados.razao_social}")
    print(f"Situação: {dados.situacao_cadastral}")
    print(f"Ativa: {dados.is_ativa()}")
    print(f"Capital Social: R$ {dados.capital_social:,.2f}")
except ReceitaFederalAPIError as e:
    print(f"Erro: {e}")
```

---

## Estrutura do Projeto

```text
CNPJ-QA-Training/
│
├── src/                              # Código fonte principal
│   └── cnpj_validator/               # Módulo de validação (pacote instalável)
│       ├── __init__.py               # Exports do módulo
│       ├── cnpj_validator.py         # Validador principal
│       ├── receita_federal_api.py    # Cliente API Receita Federal
│       └── validators/               # Validadores específicos
│           ├── numeric_validator.py
│           └── alphanumeric_validator.py
│
├── docs/                             # Documentação completa
│   ├── guides/                       # Guias técnicos
│   │   ├── guia-completo-cnpj.md
│   │   ├── guia-implementacao.md
│   │   └── glossario-referencias.md
│   ├── training/                     # Material de treinamento
│   │   ├── exercicios-praticos.md
│   │   ├── gabarito-exercicios.md
│   │   └── plano-estudo-6-semanas.md
│   └── testing/                      # Casos de teste e QA
│       ├── casos-teste-realistas.md
│       ├── shift-left-testing.md
│       └── zephyr-integration.md
│
├── tests/                            # Testes automatizados (151+ testes)
│   ├── test_numeric_validator.py     # Testes do validador numérico
│   ├── test_alphanumeric_validator.py # Testes do validador alfanumérico
│   ├── test_integration.py           # Testes de integração
│   └── test_receita_federal_api.py   # Testes da API
│
├── examples/                         # Exemplos de uso
│   ├── demo.py                       # Demonstração completa
│   ├── demo_api_receita.py           # Exemplos da API
│   └── quick-start.py                # Exemplo rápido
│
├── scripts/                          # Scripts auxiliares
│   ├── run-tests.bat
│   └── run-tests.sh
│
├── reports/                          # Relatórios de teste
│   └── test_report.html              # Relatório HTML dos testes
│
├── setup.py                          # Configuração do pacote
├── pytest.ini                        # Configuração do pytest
└── requirements.txt                  # Dependências
```

---

## Documentação

### Para Iniciantes

1. **[Guia Completo CNPJ](docs/guides/guia-completo-cnpj.md)** - História, estrutura e legislação
2. **[Exercícios Práticos](docs/training/exercicios-praticos.md)** - 21 exercícios com metodologia Scaffolding
3. **[Gabarito](docs/training/gabarito-exercicios.md)** - Respostas detalhadas

### Para QA Profissionais

1. **[Casos de Teste Realistas](docs/testing/casos-teste-realistas.md)** - 33 casos de teste detalhados
2. **[Shift Left Testing](docs/testing/shift-left-testing.md)** - Metodologia aplicada
3. **[Plano de Estudo 6 Semanas](docs/training/plano-estudo-6-semanas.md)** - Roteiro completo

### Para Desenvolvedores

1. **[Guia de Implementação](docs/guides/guia-implementacao.md)** - Código em TypeScript, Python, Java, C#
2. **[Glossário Técnico](docs/guides/glossario-referencias.md)** - Terminologia e referências
3. **[API Reference](docs/README.md)** - Documentação completa

---

## Executar Testes

```bash
# Windows
scripts\run-tests.bat

# Linux/Mac
chmod +x scripts/run-tests.sh
./scripts/run-tests.sh

# Ou via pytest diretamente
pytest tests/ -v --cov=src/cnpj_validator
```

---

## Metodologia de Ensino

Este projeto utiliza **Scaffolding** (Andaimes Educacionais), técnica pedagógica que reduz gradualmente o suporte conforme o aluno desenvolve autonomia:

| Nível | Descrição | Apoio |
|-------|-----------|-------|
| 🟢 Nível 1 | Exemplo completo com todos os passos | 100% |
| 🟡 Nível 2 | Estrutura guiada | 70% |
| 🟠 Nível 3 | Modelo simplificado | 40% |
| 🔴 Nível 4 | Resolução totalmente independente | 0% |

**Resultado**: 32 exercícios progressivos que garantem aprendizado sólido e autonomia.

---

## Funcionalidades

### Validador Numérico

- Remove formatação automaticamente
- Valida tamanho (14 dígitos)
- Detecta CNPJs inválidos (todos dígitos iguais)
- Calcula e valida dígitos verificadores
- Formata CNPJ no padrão oficial

### Validador Alfanumérico

- Valida formato XX.XXX.XXX/XXXX-XX
- Verifica caracteres especiais
- Identifica matriz (0001) ou filial (0002+)
- Extrai partes do CNPJ (raiz, ordem, DV)

### Validador Integrado

- Validação completa (numérica + alfanumérica)
- Relatórios detalhados de erros
- Métodos de conveniência (format, clean, get_info)
- Tratamento robusto de erros

### API da Receita Federal

- Consulta de dados cadastrais completos
- Verificação de situação cadastral (ATIVA, BAIXADA, etc.)
- Busca de quadro societário
- Informações de CNAE, capital social, endereço
- Suporte a BrasilAPI e ReceitaWS
- Rate limiting automático e retry com backoff

---

## Casos de Teste

33 casos de teste organizados por categoria:

| Categoria | Quantidade | Prioridade |
|-----------|------------|------------|
| Happy Path | 5 | Alta |
| Formato Inválido | 8 | Alta |
| Dígitos Verificadores | 7 | Alta |
| Edge Cases | 6 | Média |
| Alfanumérico | 4 | Média |
| Performance | 3 | Baixa |

---

## Tecnologias

- **Python 3.8 - 3.12** (linguagem principal)
- **requests** (requisições HTTP para API)
- **pytest** (framework de testes)
- **pytest-cov** (cobertura de código)
- **GitHub Actions** (CI/CD)
- **Markdown** (documentação)

---

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## Plano de Desenvolvimento

- [x] Validador numérico completo
- [x] Validador alfanumérico
- [x] Material de treinamento estruturado
- [x] 33 casos de teste realistas
- [x] CI/CD com GitHub Actions
- [x] Integração com API da Receita Federal
- [ ] Validador JavaScript/TypeScript
- [ ] CLI (Command Line Interface)
- [ ] Publicação no PyPI

---

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Autor

### Rafael Feltrim

- GitHub: [@RaFeltrim](https://github.com/RaFeltrim)
- LinkedIn: [Rafael Feltrim](https://www.linkedin.com/in/rafael-feltrim)

---

## Agradecimentos

- Receita Federal do Brasil (documentação oficial)
- Comunidade de QA brasileira
- Contribuidores do projeto

---

## Suporte

- **Issues**: [GitHub Issues](https://github.com/RaFeltrim/CNPJ-QA-Training/issues)
- **Discussões**: [GitHub Discussions](https://github.com/RaFeltrim/CNPJ-QA-Training/discussions)
- **Documentação**: [docs/README.md](docs/README.md)

---

Se este projeto foi útil, considere dar uma estrela no GitHub.

Desenvolvido para a comunidade de QA brasileira.
