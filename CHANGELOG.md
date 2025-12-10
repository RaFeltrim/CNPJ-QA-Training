# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added

#### CNPJ Alfanumérico 2026
- **Documentação Técnica Completa** (`docs/guides/cnpj-alfanumerico-2026.md`)
  - Especificação do novo formato AA.AAA.AAA/NNNN-DD
  - Tabela ASCII completa (A=10...Z=35)
  - Algoritmo de cálculo do DV adaptado
  - Cronograma de implementação (jul/2026)
  - Exemplos de código e casos de teste

- **Endpoints REST para CNPJ Alfanumérico**
  - `GET /api/v1/validate/alphanumeric` - Validação completa
  - `GET /api/v1/generate/alphanumeric` - Geração de CNPJs válidos
  - `POST /api/v1/new-format/generate` - Geração com opções
  - `GET /api/v1/new-format/calculate-dv` - Cálculo de DVs
  - Suporte a parâmetros: `raiz`, `only_letters`, `only_numbers`, `filial`

- **Mock da API da Receita Federal** (`tests/mocks/`)
  - Classe `ReceitaFederalAPIMock` para testes isolados
  - Dados de empresas pré-cadastradas (ativa, baixada, inapta)
  - Geração consistente de dados fictícios
  - Conversão para formato BrasilAPI

- **Testes de Integração Alfanuméricos** (`tests/test_integration_alphanumeric.py`)
  - 28 novos testes de integração
  - Cobertura de Mock, Validador, API REST
  - Testes de cenários realistas (abertura empresa, validação lote)
  - Testes de performance (1000 CNPJs)

### Changed
- `ReceitaFederalAPI._limpar_cnpj()` - Agora preserva letras para CNPJs alfanuméricos
- `ReceitaFederalAPI._validar_cnpj_basico()` - Usa ambos validadores (numérico e alfanumérico)
- Adicionado método `_is_cnpj_alfanumerico()` para detecção automática do tipo
- Reorganizado imports em `src/api/main.py` (sys.path antes dos imports locais)

### Dependencies
- Adicionado `httpx` para testes com FastAPI TestClient

---

## [2.0.0] - 2025-12-09

### Added
- **Integração com API da Receita Federal**
  - Classe `ReceitaFederalAPI` para consulta de dados cadastrais
  - Classe `CNPJData` (dataclass) com todos os campos retornados
  - Suporte a BrasilAPI e ReceitaWS como provedores
  - Rate limiting automático e retry com backoff exponencial
  - Métodos: `consultar()`, `verificar_situacao()`, `buscar_socios()`

- **Material de Shift Left Testing**
  - Curso completo estruturado em `docs/testing/shift-left-testing/`
  - 5 módulos: planejamento, guia teórico, exercícios, gabarito, exemplos
  - Progressão pedagógica do Junior ao Senior
  - Integração com exemplos do validador CNPJ

- **Pipeline CI/CD Completo**
  - GitHub Actions com 5 fases (Quality, Unit, Integration, Coverage, Deploy)
  - Testes em múltiplas versões Python (3.8, 3.9, 3.10, 3.11)
  - Testes em múltiplos sistemas (Ubuntu, Windows)
  - Análise de segurança com Bandit e Safety
  - Cobertura de código automatizada

- **Integração Zephyr Scale**
  - Templates para mapeamento de casos de teste no Jira
  - Markers pytest para sincronização (`@pytest.mark.zephyr`)
  - Documentação em `docs/testing/zephyr-integration.md`

### Changed
- Reestruturação completa do repositório
- Migração de `cnpj_validator/` para `src/cnpj_validator/`
- Padronização de nomenclatura para `kebab-case` (docs) e `snake_case` (Python)
- Atualização do README.md com nova estrutura e exemplos da API

### Fixed
- Imports nos testes atualizados para nova estrutura `src.cnpj_validator`
- Scripts de teste atualizados para nova localização

---

## [1.0.0] - 2025-11-15

### Added
- **Validador Numérico de CNPJ**
  - Remoção automática de formatação
  - Validação de tamanho (14 dígitos)
  - Detecção de CNPJs inválidos (todos dígitos iguais)
  - Cálculo e validação de dígitos verificadores (Módulo 11)
  - Formatação no padrão XX.XXX.XXX/XXXX-XX

- **Validador Alfanumérico de CNPJ**
  - Validação de formato padrão
  - Verificação de caracteres especiais
  - Identificação de matriz (0001) ou filial
  - Extração de partes do CNPJ (raiz, ordem, DV)

- **Validador Principal Integrado**
  - Classe `CNPJValidator` com validação completa
  - Métodos de conveniência: `format()`, `clean()`, `get_info()`
  - Método estático `is_valid()` para validação rápida

- **Material de Treinamento QA**
  - Guia completo sobre CNPJ (`docs/guides/guia-completo-cnpj.md`)
  - 21 exercícios práticos com metodologia Scaffolding
  - Gabarito detalhado com explicações
  - Plano de estudo de 6 semanas
  - 33 casos de teste realistas

- **Documentação Técnica**
  - Guia de implementação em 4 linguagens (TypeScript, Python, Java, C#)
  - Glossário técnico completo
  - Referências à legislação brasileira

- **Infraestrutura**
  - Configuração como pacote pip (`setup.py`)
  - Arquivo `requirements.txt` com dependências
  - Scripts de teste para Windows e Linux
  - Exemplos de uso em `examples/`

### Security
- Validação de entrada para evitar injection
- Sanitização de dados antes do processamento

---

## Guia de Versionamento

### Tipos de Mudança

- **Added**: Novas funcionalidades
- **Changed**: Mudanças em funcionalidades existentes
- **Deprecated**: Funcionalidades que serão removidas em breve
- **Removed**: Funcionalidades removidas
- **Fixed**: Correções de bugs
- **Security**: Correções de vulnerabilidades

### Versionamento Semântico

- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (0.X.0): Novas funcionalidades compatíveis
- **PATCH** (0.0.X): Correções de bugs compatíveis

---

[Unreleased]: https://github.com/RaFeltrim/CNPJ-QA-Training/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/RaFeltrim/CNPJ-QA-Training/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/RaFeltrim/CNPJ-QA-Training/releases/tag/v1.0.0
