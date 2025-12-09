# Templates e Guia de Integração Zephyr Scale (Jira)

## Template de Caso de Teste no Zephyr

### Estrutura Básica

```
Test Case ID: CNPJ-T###
Nome: [Nome descritivo do teste]
Objetivo: [O que este teste valida]
Prioridade: [Crítica/Alta/Média/Baixa]
Tipo: [Unit/Integration/Regression/Smoke]
Componente: [NumericValidator/AlphanumericValidator/CNPJValidator]
Labels: [shift-left, automated, regression]
```

---

## Casos de Teste Mapeados

### 1. Validação Numérica

#### CNPJ-T001: Validar CNPJ Válido Básico
- **Objetivo**: Verificar se CNPJ válido é aceito
- **Prioridade**: Crítica
- **Tipo**: Unit, Smoke
- **Pré-condições**: Sistema de validação disponível
- **Steps**:
  1. Inicializar NumericCNPJValidator
  2. Chamar validate() com "11.222.333/0001-81"
  3. Verificar result['valid'] == True
- **Resultado Esperado**: CNPJ validado com sucesso
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T001")`

#### CNPJ-T002: Rejeitar CNPJ com Dígito Verificador Inválido
- **Objetivo**: Garantir que dígitos verificadores incorretos sejam rejeitados
- **Prioridade**: Crítica
- **Tipo**: Unit, Regression
- **Steps**:
  1. Inicializar NumericCNPJValidator
  2. Chamar validate() com "11.222.333/0001-99"
  3. Verificar result['valid'] == False
  4. Verificar "verificadores inválidos" em errors
- **Resultado Esperado**: CNPJ rejeitado com mensagem clara
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T002")`

#### CNPJ-T003: Rejeitar CNPJ com Todos Dígitos Iguais
- **Objetivo**: Validar rejeição de CNPJs conhecidos como inválidos
- **Prioridade**: Alta
- **Tipo**: Unit, Regression
- **Dados de Teste**: 
  - 00000000000000
  - 11111111111111
  - 22222222222222
- **Steps**:
  1. Inicializar NumericCNPJValidator
  2. Para cada CNPJ de teste, chamar validate()
  3. Verificar result['valid'] == False
- **Resultado Esperado**: Todos CNPJs rejeitados
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T003")`

#### CNPJ-T004: Validar Remoção de Formatação
- **Objetivo**: Verificar limpeza de caracteres especiais
- **Prioridade**: Alta
- **Tipo**: Unit
- **Steps**:
  1. Chamar remove_formatting() com "11.222.333/0001-81"
  2. Verificar resultado == "11222333000181"
- **Resultado Esperado**: CNPJ sem formatação
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T004")`

#### CNPJ-T005: Validar Tamanho de CNPJ
- **Objetivo**: Garantir validação de 14 dígitos
- **Prioridade**: Alta
- **Tipo**: Unit
- **Dados de Teste**:
  - "123" (muito curto)
  - "1122233300018" (13 dígitos)
  - "112223330001811" (15 dígitos)
- **Steps**:
  1. Para cada CNPJ, chamar validate_length()
  2. Verificar resultado == False
- **Resultado Esperado**: Tamanhos incorretos rejeitados
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T005")`

---

### 2. Validação Alfanumérica

#### CNPJ-T010: Validar Formato Correto
- **Objetivo**: Verificar padrão XX.XXX.XXX/XXXX-XX
- **Prioridade**: Crítica
- **Tipo**: Unit, Smoke
- **Steps**:
  1. Inicializar AlphanumericCNPJValidator
  2. Chamar validate_format() com "11.222.333/0001-81"
  3. Verificar result['valid'] == True
- **Resultado Esperado**: Formato aceito
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T010")`

#### CNPJ-T011: Rejeitar Formato Incorreto
- **Objetivo**: Rejeitar separadores errados
- **Prioridade**: Alta
- **Tipo**: Unit, Regression
- **Dados de Teste**:
  - "11-222-333-0001-81"
  - "11.222.333.0001-81"
  - "11222333000181"
- **Steps**:
  1. Para cada CNPJ, chamar validate_format()
  2. Verificar result['valid'] == False
- **Resultado Esperado**: Formatos rejeitados
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T011")`

#### CNPJ-T012: Identificar Código de Matriz
- **Objetivo**: Detectar código 0001 como matriz
- **Prioridade**: Média
- **Tipo**: Unit
- **Steps**:
  1. Chamar validate_matriz_filial() com "11.222.333/0001-81"
  2. Verificar info['type'] == 'matriz'
  3. Verificar info['code'] == '0001'
- **Resultado Esperado**: Identificado como matriz
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T012")`

#### CNPJ-T013: Identificar Código de Filial
- **Objetivo**: Detectar código 0002+ como filial
- **Prioridade**: Média
- **Tipo**: Unit
- **Steps**:
  1. Chamar validate_matriz_filial() com "11.222.333/0002-62"
  2. Verificar info['type'] == 'filial'
  3. Verificar info['number'] == 2
- **Resultado Esperado**: Identificado como filial
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T013")`

#### CNPJ-T014: Rejeitar Código 0000
- **Objetivo**: Validar rejeição de código inválido
- **Prioridade**: Alta
- **Tipo**: Unit, Regression
- **Steps**:
  1. Chamar validate_matriz_filial() com "11.222.333/0000-00"
  2. Verificar result['valid'] == False
- **Resultado Esperado**: Código rejeitado
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T014")`

#### CNPJ-T015: Detectar Espaços em Branco
- **Objetivo**: Identificar espaços indesejados
- **Prioridade**: Média
- **Tipo**: Unit
- **Dados de Teste**:
  - " 11.222.333/0001-81" (início)
  - "11.222.333/0001-81 " (fim)
  - "11.222.333 /0001-81" (meio)
- **Steps**:
  1. Para cada CNPJ, chamar validate_whitespace()
  2. Verificar detecção apropriada
- **Resultado Esperado**: Espaços detectados
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T015")`

---

### 3. Integração

#### CNPJ-T100: Fluxo Completo de Validação
- **Objetivo**: Validar integração numérica + alfanumérica
- **Prioridade**: Crítica
- **Tipo**: Integration, Smoke
- **Steps**:
  1. Inicializar CNPJValidator
  2. Chamar validate() com "11.222.333/0001-81" e validate_format=True
  3. Verificar numeric_validation['valid'] == True
  4. Verificar alphanumeric_validation['valid'] == True
  5. Verificar result['valid'] == True
- **Resultado Esperado**: Validação completa bem-sucedida
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T100")`

#### CNPJ-T101: Roundtrip Format/Clean
- **Objetivo**: Testar formatação e limpeza em sequência
- **Prioridade**: Alta
- **Tipo**: Integration
- **Steps**:
  1. Inicializar CNPJValidator
  2. clean = clean("11.222.333/0001-81")
  3. formatted = format(clean)
  4. Verificar formatted == "11.222.333/0001-81"
- **Resultado Esperado**: Roundtrip bem-sucedido
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T101")`

#### CNPJ-T102: Validação com Extração de Info
- **Objetivo**: Testar get_info() completo
- **Prioridade**: Alta
- **Tipo**: Integration
- **Steps**:
  1. Inicializar CNPJValidator
  2. info = get_info("11.222.333/0001-81")
  3. Verificar info['valid'] == True
  4. Verificar info['matriz_filial']['type'] == 'matriz'
  5. Verificar info['parts'] contém raiz, ordem, dv
- **Resultado Esperado**: Informações extraídas corretamente
- **Pytest Marker**: `@pytest.mark.zephyr("CNPJ-T102")`

---

## Mapeamento Pytest para Zephyr

### Estrutura de Código

```python
import pytest

@pytest.mark.zephyr("CNPJ-T001")
@pytest.mark.critical
@pytest.mark.smoke
def test_cnpj_valido_basico():
    """
    Zephyr Test Case: CNPJ-T001
    Descrição: Validar CNPJ válido básico
    Prioridade: Crítica
    Tipo: Unit, Smoke
    Componente: NumericValidator
    """
    validator = NumericCNPJValidator()
    result = validator.validate("11.222.333/0001-81")
    assert result['valid'] is True
```

### Executar Testes por Caso Zephyr

```bash
# Executar teste específico
pytest -m "zephyr" -k "CNPJ-T001"

# Executar todos testes mapeados
pytest -m zephyr

# Executar por prioridade
pytest -m critical
pytest -m smoke
```

---

## Relatório de Resultados

### Formato de Saída para Zephyr

```json
{
  "testCaseKey": "CNPJ-T001",
  "status": "PASS",
  "executionTime": "0.023s",
  "environment": "Development",
  "executedBy": "Automation",
  "executionDate": "2025-12-09T10:30:00Z",
  "attachments": [
    {
      "name": "test_report.html",
      "type": "text/html"
    }
  ]
}
```

---

## Matriz de Rastreabilidade

| Test ID | Requisito | Componente | Prioridade | Status | Automação |
|---------|-----------|------------|------------|--------|-----------|
| CNPJ-T001 | REQ-001 | NumericValidator | Crítica | Pass | Sim |
| CNPJ-T002 | REQ-001 | NumericValidator | Crítica | Pass | Sim |
| CNPJ-T003 | REQ-002 | NumericValidator | Alta | Pass | Sim |
| CNPJ-T010 | REQ-003 | AlphanumericValidator | Crítica | Pass | Sim |
| CNPJ-T011 | REQ-003 | AlphanumericValidator | Alta | Pass | Sim |
| CNPJ-T100 | REQ-004 | CNPJValidator | Crítica | Pass | Sim |

---

## Configuração do Pytest para Zephyr

### conftest.py

```python
import pytest

def pytest_configure(config):
    """Configuração customizada para integração Zephyr"""
    config.addinivalue_line(
        "markers", "zephyr(id): marca teste com ID do Zephyr Scale"
    )

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Gerar relatório customizado para Zephyr"""
    if call.when == "call":
        # Extrair marker zephyr
        zephyr_marker = item.get_closest_marker("zephyr")
        if zephyr_marker:
            test_id = zephyr_marker.args[0]
            # Aqui você pode enviar resultados para Zephyr API
            pass
```

---

## Dashboards Sugeridos no Jira

### 1. Dashboard de Cobertura
- Total de casos de teste: 100
- Casos automatizados: 85 (85%)
- Casos manuais: 15 (15%)
- Cobertura de código: 92%

### 2. Dashboard de Execução
- Última execução: 2025-12-09 10:30
- Testes executados: 85
- Passou: 83 (97.6%)
- Falhou: 2 (2.4%)
- Tempo total: 12.5s

### 3. Dashboard de Qualidade
- Bugs encontrados: 3
- Bugs críticos: 0
- Bugs por componente: NumericValidator (2), AlphanumericValidator (1)
- Taxa de regressão: 0%

---

## Automação de Sincronização

### Script de Integração (Exemplo)

```python
"""
Script para sincronizar resultados do pytest com Zephyr Scale
"""

import requests
import json

def send_results_to_zephyr(test_results):
    """Envia resultados para Zephyr Scale API"""
    
    zephyr_api = "https://api.zephyrscale.smartbear.com/v2"
    project_key = "CNPJ"
    api_token = "YOUR_API_TOKEN"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    for result in test_results:
        payload = {
            "projectKey": project_key,
            "testCaseKey": result['test_id'],
            "statusName": "Pass" if result['passed'] else "Fail",
            "executionTime": result['duration'],
            "environment": "Development"
        }
        
        response = requests.post(
            f"{zephyr_api}/testexecutions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 201:
            print(f"[OK] {result['test_id']} sincronizado")
        else:
            print(f"[ERRO] Erro ao sincronizar {result['test_id']}")
```

---

## Checklist de Integração

### Antes de Começar
- [ ] Conta Zephyr Scale configurada
- [ ] API Token gerado
- [ ] Projeto criado no Jira (CNPJ)
- [ ] Casos de teste criados no Zephyr

### Durante o Desenvolvimento
- [ ] Testes marcados com @pytest.mark.zephyr
- [ ] IDs de teste mapeados
- [ ] Testes executando localmente
- [ ] Relatórios sendo gerados

### Após Implementação
- [ ] CI/CD configurado
- [ ] Resultados sincronizando automaticamente
- [ ] Dashboards criados
- [ ] Time treinado

---

## Dicas Importantes

1. **Nomenclatura Consistente**: Use sempre o padrão CNPJ-T### para IDs
2. **Descrições Claras**: Docstrings devem explicar o objetivo do teste
3. **Priorização**: Marque testes críticos adequadamente
4. **Manutenção**: Revise e atualize casos de teste regularmente
5. **Automação**: Priorize automação de testes de regressão

---

## Recursos Adicionais

- [Documentação Zephyr Scale API](https://support.smartbear.com/zephyr-scale-cloud/api-docs/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Guia de Shift Left Testing](./SHIFT_LEFT_TESTING.md)

---

**Última Atualização**: 2025-12-09
**Versão**: 1.0
