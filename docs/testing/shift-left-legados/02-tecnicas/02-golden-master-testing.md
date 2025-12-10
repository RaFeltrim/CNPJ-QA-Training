# 🏆 Golden Master Testing

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- ✅ Entender o conceito de Golden Master Testing
- ✅ Criar snapshots do comportamento atual do sistema
- ✅ Usar Golden Master para detectar regressões
- ✅ Implementar comparação automatizada de outputs

---

## 1. O Que é Golden Master Testing?

### 1.1 Definição

> **Golden Master** = Um snapshot do output de um sistema que serve como
> referência "dourada" (golden) para comparar outputs futuros.

```text
┌─────────────────────────────────────────────────────────────────┐
│                     GOLDEN MASTER TESTING                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CAPTURA (Uma vez)                                            │
│     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     │
│     │   Sistema   │ --> │   Output    │ --> │   Golden    │     │
│     │   Legado    │     │   Atual     │     │   Master    │     │
│     └─────────────┘     └─────────────┘     │  (Arquivo)  │     │
│                                              └─────────────┘     │
│                                                                  │
│  2. COMPARAÇÃO (Toda execução)                                   │
│     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     │
│     │   Sistema   │ --> │   Output    │ --> │  Comparar   │     │
│     │   Modificado│     │   Novo      │     │  com Golden │     │
│     └─────────────┘     └─────────────┘     └─────────────┘     │
│                                                   │              │
│                                    ┌──────────────┼──────────┐   │
│                                    │              │          │   │
│                                    ▼              ▼          │   │
│                              ✅ IGUAL       ❌ DIFERENTE     │   │
│                              (Passou!)      (Regressão!)     │   │
│                                                              │   │
└──────────────────────────────────────────────────────────────┘   │
```

### 1.2 Analogia: A Foto de Referência

Imagine que você é um restaurador de arte:

```text
RESTAURAÇÃO DE QUADRO:
1. Antes de restaurar, tire uma foto de alta resolução (Golden Master)
2. Faça as restaurações necessárias
3. Compare o resultado com a foto original
4. Se algo ficou diferente sem querer → regressão

REFATORAÇÃO DE CÓDIGO:
1. Antes de refatorar, capture o output completo (Golden Master)
2. Faça as modificações necessárias
3. Compare o output atual com o capturado
4. Se algo ficou diferente sem querer → regressão
```

### 1.3 Diferença para Characterization Tests

| Aspecto | Characterization Tests | Golden Master |
|---------|----------------------|---------------|
| **Granularidade** | Uma função/método | Sistema completo |
| **Output** | Valores específicos | Arquivo/snapshot completo |
| **Quando usar** | Entender comportamento | Detectar regressões em massa |
| **Manutenção** | Média | Baixa |
| **Cobertura** | Casos específicos | Todos os casos de uma vez |

---

## 2. Implementando Golden Master

### 2.1 Estrutura Básica

```python
# golden_master_test.py
"""
Framework de Golden Master Testing para sistemas legados.
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime


class GoldenMasterTest:
    """
    Classe base para testes de Golden Master.
    
    Uso:
        1. Execute em modo CAPTURE para criar o golden master
        2. Execute em modo COMPARE para validar contra o golden master
    """
    
    def __init__(self, name: str, golden_dir: str = "golden_masters"):
        self.name = name
        self.golden_dir = Path(golden_dir)
        self.golden_dir.mkdir(exist_ok=True)
        self.golden_file = self.golden_dir / f"{name}.json"
        self.metadata_file = self.golden_dir / f"{name}.meta.json"
    
    def capture(self, results: Dict[str, Any]) -> Path:
        """
        Captura os resultados como novo Golden Master.
        
        Args:
            results: Dicionário com inputs e outputs do sistema
            
        Returns:
            Caminho do arquivo golden master criado
        """
        # Salvar golden master
        with open(self.golden_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        # Salvar metadata
        metadata = {
            "captured_at": datetime.now().isoformat(),
            "total_cases": len(results),
            "checksum": self._calculate_checksum(results)
        }
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Golden Master capturado: {self.golden_file}")
        print(f"   Total de casos: {len(results)}")
        return self.golden_file
    
    def compare(self, current_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compara resultados atuais com o Golden Master.
        
        Args:
            current_results: Resultados da execução atual
            
        Returns:
            Relatório de diferenças
        """
        if not self.golden_file.exists():
            raise FileNotFoundError(
                f"Golden Master não encontrado: {self.golden_file}\n"
                "Execute em modo CAPTURE primeiro."
            )
        
        # Carregar golden master
        with open(self.golden_file, 'r', encoding='utf-8') as f:
            golden_results = json.load(f)
        
        # Comparar
        differences = []
        matches = 0
        
        for key, golden_value in golden_results.items():
            current_value = current_results.get(key)
            
            if current_value != golden_value:
                differences.append({
                    "input": key,
                    "expected": golden_value,
                    "actual": current_value
                })
            else:
                matches += 1
        
        # Verificar novos casos
        new_cases = []
        for key in current_results:
            if key not in golden_results:
                new_cases.append(key)
        
        return {
            "passed": len(differences) == 0,
            "total_golden": len(golden_results),
            "total_current": len(current_results),
            "matches": matches,
            "differences": differences,
            "new_cases": new_cases
        }
    
    def _calculate_checksum(self, data: Dict) -> str:
        """Calcula checksum MD5 dos dados."""
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(json_str.encode()).hexdigest()
```

### 2.2 Aplicação no CNPJ Validator

```python
# test_golden_master_cnpj.py
"""
Golden Master Test para o validador de CNPJ.

Este teste captura o comportamento de TODOS os inputs possíveis
para garantir que refatorações não quebrem funcionalidade.
"""

import pytest
from pathlib import Path
import json

# Importar sistema legado
from legacy.cnpj_utils import proc_cnpj

# Importar framework Golden Master
from golden_master_test import GoldenMasterTest


class TestGoldenMasterCNPJ:
    """Testes Golden Master para validação de CNPJ."""
    
    @pytest.fixture
    def golden_master(self):
        """Instância do Golden Master para CNPJ."""
        return GoldenMasterTest("cnpj_validator")
    
    @pytest.fixture
    def cnpj_test_cases(self) -> dict:
        """
        Dataset completo de casos de teste.
        Quanto mais casos, melhor a cobertura.
        """
        cases = {}
        
        # CNPJs válidos conhecidos
        cnpjs_validos = [
            "11222333000181",
            "11.222.333/0001-81",
            "12345678000195",
            "00000000000191",  # CNPJ válido especial
        ]
        
        # CNPJs inválidos
        cnpjs_invalidos = [
            "11222333000182",  # DV errado
            "11222333000100",  # DV zerado inválido
            "12345678901234",  # Aleatório
        ]
        
        # CNPJs com todos dígitos iguais
        cnpjs_repetidos = [
            "00000000000000",
            "11111111111111",
            "99999999999999",
        ]
        
        # Tamanhos incorretos
        tamanhos_errados = [
            "",
            "123",
            "12345678901234567890",
        ]
        
        # Valores especiais
        valores_especiais = [
            None,
            "abc",
            "ABCDEFGHIJKLMN",
            "1122233300AB81",  # Futuro alfanumérico
        ]
        
        # Gerar casos para f=True
        for cnpj in (cnpjs_validos + cnpjs_invalidos + cnpjs_repetidos + 
                     tamanhos_errados + valores_especiais):
            key = f"f_true|{repr(cnpj)}"
            try:
                cases[key] = proc_cnpj(cnpj, f=True)
            except Exception as e:
                cases[key] = f"EXCEPTION: {type(e).__name__}: {str(e)}"
        
        # Gerar casos para f=False
        for cnpj in (cnpjs_validos + cnpjs_invalidos + cnpjs_repetidos + 
                     tamanhos_errados + valores_especiais):
            key = f"f_false|{repr(cnpj)}"
            try:
                cases[key] = proc_cnpj(cnpj, f=False)
            except Exception as e:
                cases[key] = f"EXCEPTION: {type(e).__name__}: {str(e)}"
        
        return cases
    
    @pytest.mark.capture
    def test_capture_golden_master(self, golden_master, cnpj_test_cases):
        """
        MODO CAPTURA: Executa para criar/atualizar o Golden Master.
        
        Rodar com: pytest -m capture test_golden_master_cnpj.py
        
        ⚠️ SÓ EXECUTE QUANDO SOUBER QUE O COMPORTAMENTO ATUAL ESTÁ CORRETO!
        """
        golden_master.capture(cnpj_test_cases)
        
        # Sempre passa - só captura
        assert True
    
    def test_compare_with_golden_master(self, golden_master, cnpj_test_cases):
        """
        MODO COMPARAÇÃO: Valida output atual contra Golden Master.
        
        Este teste FALHA se qualquer comportamento mudou.
        """
        report = golden_master.compare(cnpj_test_cases)
        
        if not report["passed"]:
            # Formatar mensagem de erro detalhada
            msg = f"\n❌ Golden Master Test FALHOU!\n"
            msg += f"   Matches: {report['matches']}/{report['total_golden']}\n"
            msg += f"\n   DIFERENÇAS ENCONTRADAS:\n"
            
            for diff in report["differences"][:10]:  # Mostrar até 10
                msg += f"\n   Input: {diff['input']}\n"
                msg += f"   Esperado: {diff['expected']}\n"
                msg += f"   Atual:    {diff['actual']}\n"
            
            if len(report["differences"]) > 10:
                msg += f"\n   ... e mais {len(report['differences']) - 10} diferenças"
            
            pytest.fail(msg)
        
        print(f"\n✅ Golden Master Test PASSOU!")
        print(f"   Total de casos verificados: {report['matches']}")
```

---

## 3. Golden Master para Outputs Complexos

### 3.1 APIs e Respostas JSON

```python
# test_golden_master_api.py
"""
Golden Master para respostas de API.
"""

import pytest
import json
import requests
from deepdiff import DeepDiff  # pip install deepdiff

from golden_master_test import GoldenMasterTest


class TestGoldenMasterAPI:
    """Golden Master para API de consulta CNPJ."""
    
    @pytest.fixture
    def api_golden_master(self):
        return GoldenMasterTest("api_cnpj_responses")
    
    @pytest.fixture
    def api_test_cases(self) -> dict:
        """
        Captura respostas da API para diferentes CNPJs.
        
        ⚠️ CUIDADO: APIs externas podem mudar independentemente.
        Use mock em produção ou aceite mudanças específicas.
        """
        from src.cnpj_validator import CNPJValidator
        validator = CNPJValidator()
        
        cases = {}
        cnpjs = [
            "11222333000181",
            "00000000000191",
            # Adicione mais CNPJs para cobertura
        ]
        
        for cnpj in cnpjs:
            try:
                result = validator.consultar_receita(cnpj)
                # Remover campos que mudam (timestamps, etc)
                if result:
                    result = self._normalize_response(result)
                cases[cnpj] = result
            except Exception as e:
                cases[cnpj] = {"error": str(e)}
        
        return cases
    
    def _normalize_response(self, response: dict) -> dict:
        """
        Remove campos que variam entre execuções.
        
        Campos como 'ultima_atualizacao', 'data_consulta' mudam
        e não devem causar falha no Golden Master.
        """
        ignorar = [
            "ultima_atualizacao",
            "data_consulta",
            "timestamp",
        ]
        
        normalized = {k: v for k, v in response.items() if k not in ignorar}
        return normalized
    
    def test_compare_api_responses(self, api_golden_master, api_test_cases):
        """Valida respostas da API contra Golden Master."""
        golden_file = api_golden_master.golden_file
        
        if not golden_file.exists():
            pytest.skip("Golden Master não existe. Execute em modo capture primeiro.")
        
        with open(golden_file, 'r') as f:
            golden = json.load(f)
        
        for cnpj, current in api_test_cases.items():
            if cnpj not in golden:
                continue
            
            diff = DeepDiff(golden[cnpj], current, ignore_order=True)
            
            if diff:
                pytest.fail(
                    f"Diferença na resposta para CNPJ {cnpj}:\n{diff}"
                )
```

### 3.2 Relatórios e Arquivos

```python
# test_golden_master_relatorios.py
"""
Golden Master para relatórios gerados pelo sistema.
"""

import pytest
import hashlib
from pathlib import Path


class TestGoldenMasterRelatorios:
    """Golden Master para arquivos de relatório."""
    
    GOLDEN_DIR = Path("golden_masters/relatorios")
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    
    def _file_hash(self, filepath: Path) -> str:
        """Calcula hash SHA256 do arquivo."""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def _capture_golden(self, report_path: Path):
        """Captura arquivo como Golden Master."""
        golden_path = self.GOLDEN_DIR / f"{report_path.stem}.golden{report_path.suffix}"
        golden_path.write_bytes(report_path.read_bytes())
        
        # Salvar hash para comparação rápida
        hash_path = self.GOLDEN_DIR / f"{report_path.stem}.hash"
        hash_path.write_text(self._file_hash(report_path))
        
        return golden_path
    
    def _compare_with_golden(self, report_path: Path) -> bool:
        """Compara arquivo com Golden Master."""
        golden_hash_path = self.GOLDEN_DIR / f"{report_path.stem}.hash"
        
        if not golden_hash_path.exists():
            pytest.skip(f"Golden Master não existe para {report_path.stem}")
        
        expected_hash = golden_hash_path.read_text()
        actual_hash = self._file_hash(report_path)
        
        return expected_hash == actual_hash
    
    @pytest.mark.capture
    def test_capture_relatorio_cnpj(self):
        """Captura relatório de CNPJ como Golden Master."""
        from src.reports import generate_cnpj_report
        
        report_path = Path("output/relatorio_cnpj.csv")
        generate_cnpj_report(output=report_path)
        
        self._capture_golden(report_path)
        assert True
    
    def test_compare_relatorio_cnpj(self):
        """Compara relatório atual com Golden Master."""
        from src.reports import generate_cnpj_report
        
        report_path = Path("output/relatorio_cnpj.csv")
        generate_cnpj_report(output=report_path)
        
        assert self._compare_with_golden(report_path), \
            f"Relatório diferente do Golden Master!\n" \
            f"Compare manualmente: {report_path} vs golden_masters/relatorios/"
```

---

## 4. Quando Atualizar o Golden Master

### 4.1 Fluxo de Decisão

```text
┌───────────────────────────────────────────────────────────────┐
│                GOLDEN MASTER TEST FALHOU!                      │
│                                                                │
│                    O que fazer?                                │
│                         │                                      │
│            ┌────────────┴────────────┐                         │
│            │                         │                         │
│    A mudança foi               A mudança foi                   │
│    INTENCIONAL?                ACIDENTAL?                      │
│            │                         │                         │
│            ▼                         ▼                         │
│    ┌───────────────┐        ┌───────────────┐                  │
│    │  ATUALIZAR    │        │  INVESTIGAR   │                  │
│    │  Golden Master│        │  E CORRIGIR   │                  │
│    └───────┬───────┘        └───────┬───────┘                  │
│            │                        │                          │
│            ▼                        ▼                          │
│    pytest -m capture         Encontrar causa                   │
│    test_golden_master.py     Reverter mudança                  │
│                              Corrigir bug                      │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

### 4.2 Checklist para Atualização

```text
ANTES de atualizar o Golden Master, verifique:

☐ A mudança está documentada (PR, ticket, changelog)?
☐ Product Owner/Stakeholders aprovaram a mudança de comportamento?
☐ A mudança foi testada manualmente?
☐ Outros testes (unitários, integração) passam?
☐ Não há regressões colaterais?
☐ O novo comportamento está correto em todos os casos?

SE TUDO SIM:
  → Executar: pytest -m capture test_golden_master.py
  → Commitar novo Golden Master com mensagem explicativa

SE ALGUM NÃO:
  → NÃO atualizar!
  → Investigar e corrigir o código
```

---

## 5. Integração com CI/CD

### 5.1 GitHub Actions

```yaml
# .github/workflows/golden-master.yml
name: Golden Master Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  golden-master:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install deepdiff pytest
      
      - name: Run Golden Master Tests
        run: |
          pytest tests/golden_master/ -v --tb=short
      
      - name: Check for Golden Master Changes
        if: failure()
        run: |
          echo "⚠️ Golden Master Test falhou!"
          echo "Se a mudança foi intencional, atualize o Golden Master localmente:"
          echo "  pytest -m capture tests/golden_master/"
          echo "Então commite os arquivos em golden_masters/"
```

### 5.2 Proteção de Branch

```yaml
# Configuração recomendada no GitHub:
# Settings > Branches > Branch protection rules

# Require status checks to pass before merging:
# ✅ golden-master (Golden Master Tests)
# ✅ unit-tests
# ✅ integration-tests
```

---

## 6. Exercício Prático

### 6.1 Desafio

Crie um Golden Master Test para o formatador de documentos:

```python
# src/document_formatter.py
class DocumentFormatter:
    """Formata diferentes tipos de documentos brasileiros."""
    
    @staticmethod
    def format_cpf(cpf: str) -> str:
        digits = ''.join(c for c in cpf if c.isdigit())
        if len(digits) != 11:
            return cpf  # Retorna original se inválido
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
    
    @staticmethod
    def format_cnpj(cnpj: str) -> str:
        digits = ''.join(c for c in cnpj if c.isdigit())
        if len(digits) != 14:
            return cnpj
        return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
    
    @staticmethod
    def format_telefone(tel: str) -> str:
        digits = ''.join(c for c in tel if c.isdigit())
        if len(digits) == 11:  # Celular
            return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
        elif len(digits) == 10:  # Fixo
            return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        return tel
```

### 6.2 Template

```python
# test_golden_master_document_formatter.py
import pytest
from golden_master_test import GoldenMasterTest
from src.document_formatter import DocumentFormatter


class TestGoldenMasterDocumentFormatter:
    """Golden Master para DocumentFormatter."""
    
    @pytest.fixture
    def golden_master(self):
        return GoldenMasterTest("document_formatter")
    
    @pytest.fixture
    def test_cases(self) -> dict:
        """
        TODO: Criar casos de teste abrangentes.
        
        Inclua:
        - CPFs válidos e inválidos
        - CNPJs válidos e inválidos
        - Telefones fixos e celulares
        - Casos de borda (vazios, tamanhos errados, com letras)
        """
        formatter = DocumentFormatter()
        cases = {}
        
        # Adicione seus casos aqui...
        
        return cases
    
    @pytest.mark.capture
    def test_capture(self, golden_master, test_cases):
        golden_master.capture(test_cases)
    
    def test_compare(self, golden_master, test_cases):
        report = golden_master.compare(test_cases)
        assert report["passed"], f"Diferenças: {report['differences']}"
```

---

## 7. Resumo

### 7.1 Vantagens do Golden Master

| Vantagem | Descrição |
|----------|-----------|
| **Cobertura ampla** | Testa centenas de casos de uma vez |
| **Baixa manutenção** | Um arquivo captura todo comportamento |
| **Detecção de regressões** | Qualquer mudança é detectada |
| **Documentação viva** | Golden Master documenta o comportamento |

### 7.2 Desvantagens

| Desvantagem | Mitigação |
|-------------|-----------|
| Não testa "comportamento correto" | Combine com testes unitários |
| Falsos positivos se output varia | Normalize outputs (remover timestamps, etc) |
| Arquivo grande | Comprima ou use hashes |

### 7.3 Checklist

```text
☐ Golden Master criado a partir de código "bom conhecido"
☐ Casos de teste cobrem todas as funcionalidades
☐ Outputs normalizados (sem timestamps, ids aleatórios)
☐ Integrado ao CI/CD
☐ Processo de atualização documentado
☐ Time sabe quando atualizar vs investigar
```

---

**Próximo**: [03-strangler-fig-pattern.md](03-strangler-fig-pattern.md)
