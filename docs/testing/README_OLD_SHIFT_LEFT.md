# CNPJ Validator - Sistema de Validação com Shift Left Testing

## Visão Geral

Sistema completo de validação de CNPJ (Cadastro Nacional de Pessoa Jurídica) desenvolvido com **princípios de Shift Left Testing** e integração com **Zephyr Scale (Jira)**.

### Destaques

- **Shift Left Testing**: Testes desde o início do desenvolvimento
- **Cobertura > 90%**: Testes unitários e de integração abrangentes
- **CI/CD Automatizado**: Pipeline completo com GitHub Actions
- **Integração Zephyr**: Sincronização automática com Jira
- **Qualidade de Código**: Linting, formatação e análise de segurança

## Estrutura do Projeto

```
CNPJ-QA-Training/
├── cnpj_validator/              # Código principal
│   ├── validators/
│   │   ├── numeric_validator.py        # Validação numérica
│   │   └── alphanumeric_validator.py   # Validação alfanumérica
│   └── cnpj_validator.py        # Validador principal
│
├── tests/                       # Testes (Shift Left)
│   ├── test_numeric_validator.py
│   ├── test_alphanumeric_validator.py
│   └── test_integration.py
│
├── docs/                        # Documentação
│   ├── SHIFT_LEFT_TESTING.md   # Guia Shift Left
│   └── ZEPHYR_INTEGRATION.md   # Guia Zephyr/Jira
│
├── scripts/                     # Scripts CI/CD
│   ├── run_tests.bat           # Windows
│   └── run_tests.sh            # Linux/Mac
│
├── .github/workflows/          # CI/CD
│   └── ci-cd.yml              # Pipeline GitHub Actions
│
├── examples/                   # Exemplos de uso
│   ├── demo.py                # Demonstração completa
│   └── simple_example.py      # Exemplo básico
│
├── pytest.ini                 # Configuração pytest
├── .coveragerc               # Configuração cobertura
└── requirements.txt          # Dependências
```

## Funcionalidades

### Validador Numérico
- Remove formatação
- Valida tamanho (14 dígitos)
- Detecta CNPJs inválidos (todos dígitos iguais)
- Calcula e valida dígitos verificadores
- Formata CNPJ (XX.XXX.XXX/XXXX-XX)

### Validador Alfanumérico
- Valida formato padrão
- Verifica caracteres especiais
- Valida posições dos separadores
- Identifica matriz (0001) ou filial (0002+)
- Detecta espaços em branco
- Extrai partes do CNPJ

### Validador Principal (Integrado)
- Validação completa (numérica + alfanumérica)
- Métodos de conveniência (format, clean, get_info)
- Relatórios detalhados
- Tratamento de erros robusto

## Testes (Shift Left Testing)

### Estatísticas de Testes
- **Total de Testes**: 100+
- **Cobertura de Código**: >90%
- **Tempo de Execução**: <10 segundos
- **Testes Automatizados**: 100%

### Executar Testes

#### Windows
```cmd
# Pipeline completo
scripts\run_tests.bat

# Testes específicos
pytest tests/test_numeric_validator.py
pytest tests/test_integration.py -m integration
pytest -m zephyr  # Testes mapeados no Jira
```

#### Linux/Mac
```bash
# Pipeline completo
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh

# Testes específicos
pytest tests/ -v
pytest --cov=cnpj_validator --cov-report=html
```

### Tipos de Testes

| Tipo | Quantidade | Markers | Quando Executar |
|------|-----------|---------|-----------------|
| **Unit** | 80+ | `@pytest.mark.unit` | A cada commit |
| **Integration** | 15+ | `@pytest.mark.integration` | A cada PR |
| **Smoke** | 10+ | `@pytest.mark.smoke` | A cada build |
| **Regression** | 50+ | `@pytest.mark.regression` | A cada release |

## Instalação

### Pré-requisitos
- Python 3.7+
- pip

### Instalar Dependências
```bash
# Dependências básicas (produção)
pip install -r requirements.txt

# Apenas bibliotecas padrão do Python são necessárias para funcionalidade básica
```

## Uso Rápido

### Exemplo Básico
```python
from cnpj_validator import CNPJValidator

validator = CNPJValidator()

# Validação simples
result = validator.validate("11.222.333/0001-81")
print(result['valid'])  # True

# Validação rápida
is_valid = CNPJValidator.is_valid("11222333000181")
print(is_valid)  # True

# Formatar CNPJ
formatted = validator.format("11222333000181")
print(formatted)  # 11.222.333/0001-81

# Obter informações
info = validator.get_info("11.222.333/0001-81")
print(info['matriz_filial']['type'])  # matriz
```

### Executar Exemplos
```bash
# Demonstração completa
python examples/demo.py

# Exemplo básico
python examples/simple_example.py
```

## 🔄 CI/CD Pipeline (Shift Left)

### Pipeline Automático (GitHub Actions)

```
┌─────────────────────────────────────────────────────────────┐
│  FASE 1: Quality Checks (Rápido - <1 min)                  │
│  ├─ Black (formatação)                                      │
│  ├─ Flake8 (linting)                                        │
│  ├─ Pylint (análise estática)                               │
│  ├─ Bandit (segurança)                                      │
│  └─ Safety (vulnerabilidades)                               │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 2: Unit Tests (Moderado - 2-3 min)                   │
│  ├─ Python 3.8, 3.9, 3.10, 3.11                            │
│  ├─ Ubuntu + Windows                                         │
│  └─ 80+ testes unitários                                    │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 3: Integration Tests (Moderado - 1-2 min)            │
│  └─ 15+ testes de integração                                │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 4: Coverage & Reports (Rápido - <1 min)              │
│  ├─ Cobertura de código                                     │
│  ├─ Relatórios HTML                                         │
│  └─ Upload para Codecov                                     │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 5: Sync com Zephyr (Opcional)                        │
│  └─ Sincronizar resultados com Jira                        │
└─────────────────────────────────────────────────────────────┘
```

### Triggers
- ✅ Push para `master` ou `develop`
- ✅ Pull Requests
- ✅ Execução agendada (diária às 2h)

## 📊 Integração Zephyr Scale (Jira)

### Casos de Teste Mapeados

| Test ID | Componente | Prioridade | Status |
|---------|-----------|------------|--------|
| CNPJ-T001 | NumericValidator | Crítica | ✅ Automatizado |
| CNPJ-T002 | NumericValidator | Crítica | ✅ Automatizado |
| CNPJ-T010 | AlphanumericValidator | Crítica | ✅ Automatizado |
| CNPJ-T100 | CNPJValidator | Crítica | ✅ Automatizado |

### Executar Testes Zephyr
```bash
# Todos os testes mapeados
pytest -m zephyr -v

# Teste específico
pytest -m zephyr -k "CNPJ-T001"

# Por prioridade
pytest -m critical
```

## 📚 Documentação

### Guias Disponíveis
- 📖 [Guia de Shift Left Testing](docs/SHIFT_LEFT_TESTING.md)
- 📖 [Integração com Zephyr/Jira](docs/ZEPHYR_INTEGRATION.md)
- 📖 [Guia de CNPJ QA](01.Guia_cnpj_qa.md)
- 📖 [Casos de Teste Realistas](05.Casos_de_Teste_Realistas.md)

## 🎓 Conceitos de Shift Left Testing

### O que é Shift Left?
Mover testes para **fases iniciais** do desenvolvimento:
- ✅ Testar durante o desenvolvimento (não apenas no final)
- ✅ Automação desde o primeiro commit
- ✅ Feedback rápido para desenvolvedores
- ✅ Prevenir bugs em vez de apenas detectá-los
- ✅ Qualidade é responsabilidade de todos

### Benefícios
- 💰 **Redução de Custos**: Bugs encontrados cedo custam 10-100x menos
- 🚀 **Entrega Rápida**: Feedback imediato = deploys mais rápidos
- 🎯 **Maior Qualidade**: Menos bugs em produção
- 🤝 **Colaboração**: Dev e QA trabalham juntos desde o início

## 🔧 Ferramentas Utilizadas

### Testes
- `pytest` - Framework de testes
- `pytest-cov` - Cobertura de código
- `pytest-html` - Relatórios HTML

### Qualidade
- `black` - Formatação automática
- `flake8` - Linting (PEP 8)
- `pylint` - Análise estática

### Segurança
- `bandit` - Análise de segurança
- `safety` - Vulnerabilidades

### CI/CD
- GitHub Actions - Pipeline automatizado
- Codecov - Análise de cobertura

## 📈 Métricas de Qualidade

### Metas do Projeto
- ✅ Cobertura de código: >80% (atual: ~92%)
- ✅ Testes passando: 100%
- ✅ Tempo de build: <10 minutos
- ✅ Zero bugs críticos em produção

### Monitoramento
```bash
# Verificar cobertura
pytest --cov=cnpj_validator --cov-report=term-missing

# Gerar relatório HTML
pytest --cov=cnpj_validator --cov-report=html
# Abrir: reports/coverage/index.html

# Verificar qualidade
flake8 cnpj_validator/
pylint cnpj_validator/
```

## 🤝 Contribuindo

### Workflow de Contribuição
1. **Fork** o repositório
2. **Crie** uma branch (`git checkout -b feature/nova-funcionalidade`)
3. **Escreva testes** antes do código (TDD)
4. **Implemente** a funcionalidade
5. **Execute** testes localmente (`scripts/run_tests.bat`)
6. **Commit** (`git commit -m 'Adiciona nova funcionalidade'`)
7. **Push** (`git push origin feature/nova-funcionalidade`)
8. **Abra** um Pull Request

### Checklist antes de Commitar
- [ ] Todos os testes passam?
- [ ] Cobertura mantida ou melhorada?
- [ ] Código formatado (black)?
- [ ] Sem erros de linting?
- [ ] Testes adicionados para nova funcionalidade?
- [ ] Documentação atualizada?

## 🐛 Reportar Bugs

Ao reportar bugs, inclua:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Versão do Python
- Sistema operacional

## 📝 Licença

Este projeto é de código aberto e está disponível para fins educacionais.

## 👨‍💻 Autor

**Rafael Feltrim** - [@RaFeltrim](https://github.com/RaFeltrim)

## 🎓 Objetivo Educacional

Este projeto serve como:
- ✅ **Treinamento de QA Manual e Automatizado**
- ✅ **Prática de Shift Left Testing**
- ✅ **Exemplo de integração com Zephyr/Jira**
- ✅ **Referência de CI/CD**
- ✅ **Estudo de validação de dados**

## 📞 Suporte

- 📧 Issues: Use a aba Issues do GitHub
- 📖 Documentação: Consulte a pasta `docs/`
- 💬 Discussões: Use a aba Discussions

---

## 🚀 Quick Start

```bash
# 1. Clonar repositório
git clone https://github.com/RaFeltrim/CNPJ-QA-Training.git
cd CNPJ-QA-Training

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar testes
pytest

# 4. Ver relatório de cobertura
pytest --cov=cnpj_validator --cov-report=html

# 5. Testar o sistema
python examples/demo.py
```

---

**Desenvolvido com ❤️ para a comunidade de QA e Testes de Software**

**Última Atualização**: 2025-12-09
