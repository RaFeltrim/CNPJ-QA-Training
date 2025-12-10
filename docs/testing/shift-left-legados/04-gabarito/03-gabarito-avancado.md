# 📝 Gabarito - Exercícios Avançados

> **Nível**: 🔴 Avançado (Suporte 0%)  
> **Objetivo**: Soluções de referência para exercícios complexos de migração de sistemas legados

---

## Exercício 1: Migração Completa de Módulo de Pagamentos

### 1.1 Documento de Estratégia de Migração

```markdown
# Estratégia de Migração - Módulo de Pagamentos

## Resumo Executivo

Migração do processador de pagamentos legado para nova implementação
utilizando Strangler Fig Pattern com Feature Flags.

## Fases da Migração

### Fase 1: Caracterização (Semana 1-2)
- Documentar comportamentos existentes
- Criar Golden Master com 10.000+ casos
- Identificar regras de negócio implícitas

### Fase 2: Implementação (Semana 3-4)
- Nova implementação com mesma interface
- Testes unitários abrangentes
- Shadow mode paralelo

### Fase 3: Rollout Gradual (Semana 5-8)
- 1% → 5% → 10% → 25% → 50% → 100%
- Monitoramento contínuo
- Rollback automático em caso de divergência

### Fase 4: Cutover (Semana 9)
- Desativar sistema legado
- Remoção de feature flags
- Documentação final

## Plano de Rollback

| Cenário | Ação | Tempo |
|---------|------|-------|
| Taxa de erro > 0.1% | Rollback para 50% | 30s |
| Taxa de erro > 1% | Rollback para 0% | 30s |
| Falha crítica | Kill switch imediato | 5s |
```

### 1.2 Suite de Testes de Caracterização

```python
# test_characterization_payments.py
"""
Testes de Caracterização para PaymentProcessor.

OBJETIVO: Documentar 100% do comportamento do sistema legado.
"""

import pytest
from dataclasses import dataclass
from typing import Dict, Any, Optional
from decimal import Decimal
import json
from pathlib import Path


# === Sistema Legado (Original) ===

class PaymentProcessor:
    """Processador de pagamentos legado."""
    
    def process(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        # Validações
        if not transaction.get('amount') or transaction['amount'] <= 0:
            return {
                'status': 'error',
                'code': 'E001',
                'message': 'Invalid amount'
            }
        
        if transaction['amount'] > 50000:
            return {
                'status': 'declined',
                'code': 'D001',
                'message': 'Amount exceeds limit'
            }
        
        # Processamento
        approved = transaction['amount'] < 10000
        
        return {
            'transaction_id': f"TXN-{transaction['id']}",
            'status': 'approved' if approved else 'declined',
            'code': 'A001' if approved else 'D002',
            'message': 'Transaction approved' if approved else 'Risk analysis declined'
        }
    
    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        return {
            'refund_id': f"REF-{transaction_id}",
            'status': 'approved',
            'amount': amount
        }
    
    def get_status(self, transaction_id: str) -> Dict[str, Any]:
        return {
            'transaction_id': transaction_id,
            'status': 'completed',
            'amount': 100.00
        }


class TestCharacterizationPayments:
    """Documentação completa do comportamento do PaymentProcessor."""
    
    @pytest.fixture
    def processor(self):
        return PaymentProcessor()
    
    class TestProcessValidacoes:
        """Testes de validação de entrada."""
        
        @pytest.fixture
        def processor(self):
            return PaymentProcessor()
        
        def test_amount_none_retorna_erro(self, processor):
            """
            DESCOBERTA: amount=None retorna erro E001.
            """
            result = processor.process({'id': '1', 'amount': None})
            assert result['status'] == 'error'
            assert result['code'] == 'E001'
        
        def test_amount_zero_retorna_erro(self, processor):
            """
            DESCOBERTA: amount=0 retorna erro E001.
            """
            result = processor.process({'id': '1', 'amount': 0})
            assert result['status'] == 'error'
            assert result['code'] == 'E001'
        
        def test_amount_negativo_retorna_erro(self, processor):
            """
            DESCOBERTA: Valores negativos retornam erro E001.
            """
            result = processor.process({'id': '1', 'amount': -100})
            assert result['status'] == 'error'
            assert result['code'] == 'E001'
        
        def test_amount_acima_limite_declined(self, processor):
            """
            DESCOBERTA: Valores > 50000 retornam declined D001.
            
            ⚠️ REGRA DE NEGÓCIO: Limite de transação = R$ 50.000,00
            """
            result = processor.process({'id': '1', 'amount': 50001})
            assert result['status'] == 'declined'
            assert result['code'] == 'D001'
        
        def test_amount_igual_limite_declined(self, processor):
            """
            DESCOBERTA: Valor exatamente 50000 também é declined.
            
            ⚠️ A comparação é > (estritamente maior), então 50000 passa.
            """
            result = processor.process({'id': '1', 'amount': 50000})
            # Este vai para processamento (não é > 50000)
            assert result['status'] in ['approved', 'declined']
    
    class TestProcessRegrasNegocio:
        """Testes de regras de negócio do processamento."""
        
        @pytest.fixture
        def processor(self):
            return PaymentProcessor()
        
        def test_amount_baixo_aprovado(self, processor):
            """
            DESCOBERTA: Valores < 10000 são aprovados.
            
            ⚠️ REGRA DE NEGÓCIO IMPLÍCITA: Análise de risco automática.
            """
            result = processor.process({'id': '1', 'amount': 9999.99})
            assert result['status'] == 'approved'
            assert result['code'] == 'A001'
        
        def test_amount_alto_declined_risco(self, processor):
            """
            DESCOBERTA: Valores >= 10000 são declined por risco.
            
            ⚠️ REGRA DE NEGÓCIO: Valores altos vão para análise manual.
            """
            result = processor.process({'id': '1', 'amount': 10000})
            assert result['status'] == 'declined'
            assert result['code'] == 'D002'
        
        def test_transaction_id_formato(self, processor):
            """
            DESCOBERTA: transaction_id usa prefixo TXN-.
            """
            result = processor.process({'id': 'ABC123', 'amount': 100})
            assert result['transaction_id'] == 'TXN-ABC123'
    
    class TestRefund:
        """Testes de estorno."""
        
        @pytest.fixture
        def processor(self):
            return PaymentProcessor()
        
        def test_refund_sempre_aprovado(self, processor):
            """
            DESCOBERTA: Refunds são sempre aprovados.
            
            ⚠️ PROBLEMA POTENCIAL: Não há validação de estorno.
            """
            result = processor.refund('TXN-123', 100)
            assert result['status'] == 'approved'
        
        def test_refund_id_formato(self, processor):
            """
            DESCOBERTA: refund_id usa prefixo REF-.
            """
            result = processor.refund('TXN-123', 100)
            assert result['refund_id'] == 'REF-TXN-123'


# === Resumo das Descobertas ===
"""
REGRAS DE NEGÓCIO DOCUMENTADAS:

1. VALIDAÇÃO DE ENTRADA:
   - amount obrigatório e > 0
   - Limite máximo: R$ 50.000,00

2. ANÁLISE DE RISCO:
   - < R$ 10.000: aprovação automática
   - >= R$ 10.000 até R$ 50.000: declined para análise manual

3. ESTORNOS:
   - Sempre aprovados (sem validação)

4. FORMATOS:
   - Transaction ID: TXN-{id}
   - Refund ID: REF-{transaction_id}

⚠️ PROBLEMAS IDENTIFICADOS:
   - Estornos não são validados
   - Não há verificação de tipo de pagamento
   - Sem logging de auditoria
"""
```

### 1.3 Golden Master com 1000+ Casos

```python
# golden_master_payments.py
"""
Golden Master para PaymentProcessor.
"""

import json
import itertools
from pathlib import Path
from typing import Dict, Any, List


class GoldenMasterPayments:
    """Gerador de Golden Master para pagamentos."""
    
    def __init__(self):
        self.processor = PaymentProcessor()
        self.arquivo = Path("golden_masters/payments.json")
    
    def gerar_transacoes_teste(self) -> List[Dict[str, Any]]:
        """Gera combinações de transações para teste."""
        
        ids = ['1', 'ABC', '123-456', '', None]
        
        amounts = [
            None, -1000, -0.01, 0, 0.01, 1, 
            100, 999.99, 1000, 5000, 
            9999.99, 10000, 10000.01,
            25000, 49999.99, 50000, 50000.01,
            100000, 1000000
        ]
        
        currencies = ['BRL', 'USD', 'EUR', None]
        
        types = ['credit', 'debit', 'pix', 'invalid', None]
        
        customer_ids = ['C001', 'C002', None]
        
        merchant_ids = ['M001', None]
        
        transacoes = []
        
        for id_, amount, currency, tipo, customer, merchant in itertools.product(
            ids, amounts, currencies, types, customer_ids, merchant_ids
        ):
            transacoes.append({
                'id': id_,
                'amount': amount,
                'currency': currency,
                'type': tipo,
                'customer_id': customer,
                'merchant_id': merchant
            })
        
        return transacoes
    
    def capturar(self) -> Dict[str, Any]:
        """Captura Golden Master completo."""
        
        casos = {}
        transacoes = self.gerar_transacoes_teste()
        
        print(f"🔄 Gerando {len(transacoes)} casos de teste...")
        
        for i, txn in enumerate(transacoes):
            # Process
            chave_process = f"process|{json.dumps(txn, sort_keys=True)}"
            try:
                resultado = self.processor.process(txn)
                casos[chave_process] = resultado
            except Exception as e:
                casos[chave_process] = {
                    'exception': type(e).__name__,
                    'message': str(e)
                }
            
            if (i + 1) % 1000 == 0:
                print(f"   Processados: {i + 1}/{len(transacoes)}")
        
        # Testes de Refund
        refund_amounts = [0, 50, 100, 1000, 10000]
        txn_ids = ['TXN-1', 'TXN-ABC', 'INVALID', None]
        
        for txn_id, amount in itertools.product(txn_ids, refund_amounts):
            chave = f"refund|{txn_id}|{amount}"
            try:
                resultado = self.processor.refund(txn_id, amount)
                casos[chave] = resultado
            except Exception as e:
                casos[chave] = {
                    'exception': type(e).__name__,
                    'message': str(e)
                }
        
        # Salvar
        self.arquivo.parent.mkdir(exist_ok=True)
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(casos, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Golden Master capturado: {self.arquivo}")
        print(f"   Total de casos: {len(casos)}")
        
        return casos
    
    def comparar(self) -> Dict[str, Any]:
        """Compara implementação atual com Golden Master."""
        
        with open(self.arquivo, 'r') as f:
            golden = json.load(f)
        
        diferencas = []
        matches = 0
        
        for chave, esperado in golden.items():
            partes = chave.split('|')
            metodo = partes[0]
            
            try:
                if metodo == 'process':
                    txn = json.loads(partes[1])
                    atual = self.processor.process(txn)
                elif metodo == 'refund':
                    txn_id = partes[1]
                    amount = float(partes[2])
                    atual = self.processor.refund(txn_id, amount)
                else:
                    continue
                
                if atual != esperado:
                    diferencas.append({
                        'caso': chave,
                        'esperado': esperado,
                        'atual': atual
                    })
                else:
                    matches += 1
                    
            except Exception as e:
                atual = {'exception': type(e).__name__, 'message': str(e)}
                if atual != esperado:
                    diferencas.append({
                        'caso': chave,
                        'esperado': esperado,
                        'atual': atual
                    })
        
        return {
            'passed': len(diferencas) == 0,
            'total': len(golden),
            'matches': matches,
            'diferencas': diferencas[:10]  # Primeiras 10
        }
```

### 1.4 Facade de Migração com Rollout Gradual

```python
# payment_facade.py
"""
Facade para migração gradual de PaymentProcessor.

Implementa Strangler Fig Pattern com Feature Flags.
"""

import random
import time
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Callable
from enum import Enum
from datetime import datetime


class RolloutMode(Enum):
    """Modos de rollout."""
    LEGACY_ONLY = "legacy"
    NEW_ONLY = "new"
    PERCENTAGE = "percentage"
    SHADOW = "shadow"
    CANARY = "canary"


@dataclass
class RolloutConfig:
    """Configuração de rollout."""
    mode: RolloutMode = RolloutMode.LEGACY_ONLY
    percentage: float = 0.0
    shadow_enabled: bool = False
    canary_customers: list = field(default_factory=list)


@dataclass
class MigrationMetrics:
    """Métricas de migração."""
    legacy_calls: int = 0
    new_calls: int = 0
    shadow_calls: int = 0
    divergences: int = 0
    errors_legacy: int = 0
    errors_new: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'legacy_calls': self.legacy_calls,
            'new_calls': self.new_calls,
            'shadow_calls': self.shadow_calls,
            'divergences': self.divergences,
            'error_rate_legacy': self.errors_legacy / max(self.legacy_calls, 1),
            'error_rate_new': self.errors_new / max(self.new_calls, 1)
        }


class PaymentMigrationFacade:
    """
    Facade para migração gradual.
    
    Suporta:
    - Rollout por porcentagem
    - Shadow mode (executa ambos, compara)
    - Canary (clientes específicos)
    - Métricas e logging
    """
    
    def __init__(
        self,
        legacy_processor,
        new_processor,
        config: Optional[RolloutConfig] = None
    ):
        self.legacy = legacy_processor
        self.new = new_processor
        self.config = config or RolloutConfig()
        self.metrics = MigrationMetrics()
        self.logger = logging.getLogger(__name__)
    
    def process(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Processa transação usando a estratégia configurada."""
        
        mode = self._determine_mode(transaction)
        
        if mode == RolloutMode.LEGACY_ONLY:
            return self._process_legacy(transaction)
        
        elif mode == RolloutMode.NEW_ONLY:
            return self._process_new(transaction)
        
        elif mode == RolloutMode.SHADOW:
            return self._process_shadow(transaction)
        
        elif mode == RolloutMode.PERCENTAGE:
            if random.random() < self.config.percentage:
                return self._process_new(transaction)
            return self._process_legacy(transaction)
        
        elif mode == RolloutMode.CANARY:
            if transaction.get('customer_id') in self.config.canary_customers:
                return self._process_new(transaction)
            return self._process_legacy(transaction)
        
        return self._process_legacy(transaction)
    
    def _determine_mode(self, transaction: Dict[str, Any]) -> RolloutMode:
        """Determina modo baseado na transação."""
        
        # Shadow mode sempre executa ambos
        if self.config.shadow_enabled:
            return RolloutMode.SHADOW
        
        return self.config.mode
    
    def _process_legacy(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Processa usando sistema legado."""
        
        self.metrics.legacy_calls += 1
        start = time.time()
        
        try:
            result = self.legacy.process(transaction)
            self._log_call('legacy', transaction, result, time.time() - start)
            return result
        except Exception as e:
            self.metrics.errors_legacy += 1
            self._log_error('legacy', transaction, e)
            raise
    
    def _process_new(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Processa usando novo sistema."""
        
        self.metrics.new_calls += 1
        start = time.time()
        
        try:
            result = self.new.process(transaction)
            self._log_call('new', transaction, result, time.time() - start)
            return result
        except Exception as e:
            self.metrics.errors_new += 1
            self._log_error('new', transaction, e)
            raise
    
    def _process_shadow(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Shadow mode: executa ambos, compara, retorna legado.
        
        Útil para validar nova implementação em produção
        sem afetar usuários.
        """
        
        self.metrics.shadow_calls += 1
        
        # Executa legado primeiro (é o que retorna)
        legacy_result = self._process_legacy(transaction)
        
        # Executa novo em paralelo (async em produção)
        try:
            new_result = self.new.process(transaction)
            self.metrics.new_calls += 1
            
            # Compara resultados
            if not self._compare_results(legacy_result, new_result):
                self.metrics.divergences += 1
                self._log_divergence(transaction, legacy_result, new_result)
        
        except Exception as e:
            self.metrics.errors_new += 1
            self._log_error('new_shadow', transaction, e)
        
        # Sempre retorna legado no shadow mode
        return legacy_result
    
    def _compare_results(
        self,
        legacy: Dict[str, Any],
        new: Dict[str, Any]
    ) -> bool:
        """Compara resultados normalizando diferenças aceitáveis."""
        
        # Campos críticos que devem ser iguais
        critical_fields = ['status', 'code']
        
        for field in critical_fields:
            if legacy.get(field) != new.get(field):
                return False
        
        return True
    
    def _log_call(
        self,
        system: str,
        transaction: Dict[str, Any],
        result: Dict[str, Any],
        duration: float
    ):
        """Log estruturado de chamada."""
        
        self.logger.info(
            f"Payment processed",
            extra={
                'system': system,
                'transaction_id': transaction.get('id'),
                'amount': transaction.get('amount'),
                'status': result.get('status'),
                'duration_ms': duration * 1000
            }
        )
    
    def _log_divergence(
        self,
        transaction: Dict[str, Any],
        legacy: Dict[str, Any],
        new: Dict[str, Any]
    ):
        """Log de divergência entre sistemas."""
        
        self.logger.warning(
            f"Divergence detected",
            extra={
                'transaction': transaction,
                'legacy_result': legacy,
                'new_result': new
            }
        )
    
    def _log_error(
        self,
        system: str,
        transaction: Dict[str, Any],
        error: Exception
    ):
        """Log de erro."""
        
        self.logger.error(
            f"Error in {system}",
            extra={
                'transaction': transaction,
                'error': str(error)
            }
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas atuais."""
        return self.metrics.to_dict()
    
    def set_rollout_percentage(self, percentage: float):
        """Atualiza porcentagem de rollout."""
        
        if not 0 <= percentage <= 1:
            raise ValueError("Percentage must be between 0 and 1")
        
        self.config.percentage = percentage
        self.config.mode = RolloutMode.PERCENTAGE
        
        self.logger.info(f"Rollout updated to {percentage * 100}%")
    
    def emergency_rollback(self):
        """Rollback de emergência para 100% legado."""
        
        self.config.mode = RolloutMode.LEGACY_ONLY
        self.config.percentage = 0
        self.config.shadow_enabled = False
        
        self.logger.critical("EMERGENCY ROLLBACK executed")
```

### 1.5 Suite de Regressão em 4 Níveis

```python
# test_regression_payments.py
"""
Suite de Regressão em 4 níveis para PaymentProcessor.
"""

import pytest
import time


# === Nível 1: Smoke Tests (< 1 min) ===

class TestSmokePayments:
    """
    Smoke Tests - Validação rápida de sanidade.
    
    Execução: < 1 minuto
    Quando: Toda build, pré-commit
    """
    
    @pytest.fixture
    def processor(self):
        return PaymentProcessor()
    
    def test_sistema_responde(self, processor):
        """Sistema está funcionando."""
        result = processor.process({'id': '1', 'amount': 100})
        assert result is not None
    
    def test_transacao_simples_aprovada(self, processor):
        """Transação simples é aprovada."""
        result = processor.process({'id': '1', 'amount': 100})
        assert result['status'] == 'approved'
    
    def test_transacao_invalida_erro(self, processor):
        """Transação inválida retorna erro."""
        result = processor.process({'id': '1', 'amount': -100})
        assert result['status'] == 'error'
    
    def test_refund_funciona(self, processor):
        """Estorno básico funciona."""
        result = processor.refund('TXN-1', 100)
        assert result['status'] == 'approved'


# === Nível 2: Sanity Tests (< 5 min) ===

class TestSanityPayments:
    """
    Sanity Tests - Validação de funcionalidades principais.
    
    Execução: < 5 minutos
    Quando: Após merge, staging
    """
    
    @pytest.fixture
    def processor(self):
        return PaymentProcessor()
    
    class TestValidacoes:
        
        @pytest.fixture
        def processor(self):
            return PaymentProcessor()
        
        @pytest.mark.parametrize("amount,expected_status", [
            (None, 'error'),
            (0, 'error'),
            (-100, 'error'),
            (100, 'approved'),
            (10000, 'declined'),
            (50001, 'declined'),
        ])
        def test_validacao_amount(self, processor, amount, expected_status):
            result = processor.process({'id': '1', 'amount': amount})
            assert result['status'] == expected_status
    
    class TestRegrasNegocio:
        
        @pytest.fixture
        def processor(self):
            return PaymentProcessor()
        
        def test_limite_aprovacao_automatica(self, processor):
            """Valores < 10000 são aprovados automaticamente."""
            result = processor.process({'id': '1', 'amount': 9999.99})
            assert result['status'] == 'approved'
        
        def test_limite_analise_manual(self, processor):
            """Valores >= 10000 vão para análise."""
            result = processor.process({'id': '1', 'amount': 10000})
            assert result['status'] == 'declined'
            assert result['code'] == 'D002'
        
        def test_limite_maximo(self, processor):
            """Valores > 50000 são recusados."""
            result = processor.process({'id': '1', 'amount': 50001})
            assert result['status'] == 'declined'
            assert result['code'] == 'D001'


# === Nível 3: Core Regression (< 30 min) ===

class TestCoreRegressionPayments:
    """
    Core Regression - Cobertura completa de cenários.
    
    Execução: < 30 minutos
    Quando: Deploy para produção
    """
    
    @pytest.fixture
    def processor(self):
        return PaymentProcessor()
    
    @pytest.mark.parametrize("amount", [
        0.01, 0.99, 1, 10, 100, 500, 1000, 2500, 5000,
        7500, 9000, 9999, 9999.99, 10000, 10000.01,
        15000, 25000, 40000, 49999.99, 50000, 50000.01
    ])
    def test_faixa_valores(self, processor, amount):
        """Testa todas as faixas de valores."""
        result = processor.process({'id': '1', 'amount': amount})
        assert 'status' in result
    
    @pytest.mark.parametrize("tipo", [
        'credit', 'debit', 'pix', 'boleto', 'invalid', None
    ])
    def test_tipos_transacao(self, processor, tipo):
        """Testa todos os tipos de transação."""
        result = processor.process({
            'id': '1',
            'amount': 100,
            'type': tipo
        })
        # Sistema atual ignora tipo, deve funcionar
        assert result['status'] == 'approved'
    
    class TestCasosBorda:
        
        @pytest.fixture
        def processor(self):
            return PaymentProcessor()
        
        def test_id_vazio(self, processor):
            result = processor.process({'id': '', 'amount': 100})
            assert result['transaction_id'] == 'TXN-'
        
        def test_amount_decimal_longo(self, processor):
            result = processor.process({'id': '1', 'amount': 99.999999})
            assert result['status'] == 'approved'


# === Nível 4: Full Regression ===

class TestFullRegressionPayments:
    """
    Full Regression - Todas as combinações.
    
    Execução: > 1 hora
    Quando: Release major, fim de semana
    """
    
    @pytest.fixture
    def processor(self):
        return PaymentProcessor()
    
    @pytest.fixture
    def golden_master(self):
        return GoldenMasterPayments()
    
    def test_golden_master_compliance(self, processor, golden_master):
        """Verifica 100% de paridade com Golden Master."""
        result = golden_master.comparar()
        
        assert result['passed'], (
            f"Golden Master falhou: {result['diferencas']}"
        )
```

---

## Exercício 2: Sistema de Regras de Negócio (Resumo)

### Parser do Formato Proprietário

```python
# rules_parser.py
"""
Parser para formato proprietário de regras.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class Condition:
    """Uma condição IF."""
    field: str
    operator: str
    value: Any


@dataclass
class Action:
    """Uma ação THEN."""
    target: str
    expression: str


@dataclass
class Rule:
    """Uma regra completa."""
    name: str
    conditions: List[Condition]
    action: Action


class RulesParser:
    """Parser para linguagem de regras proprietária."""
    
    OPERATORS = {
        '=': lambda a, b: a == b,
        '<': lambda a, b: a < b,
        '>': lambda a, b: a > b,
        '<=': lambda a, b: a <= b,
        '>=': lambda a, b: a >= b,
        'IN': lambda a, b: a in b,
    }
    
    def parse_file(self, content: str) -> List[Rule]:
        """Parse arquivo de regras."""
        
        rules = []
        current_rule = None
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Ignorar comentários e linhas vazias
            if not line or line.startswith('#'):
                continue
            
            # Início de regra
            if line.startswith('RULE '):
                name = line[5:].strip()
                current_rule = {'name': name, 'conditions': []}
            
            # Condição IF/THEN
            elif line.startswith('IF '):
                match = re.match(
                    r'IF\s+(\w+)\s*(=|<|>|<=|>=|IN)\s*(.+?)\s+THEN\s+(.+)',
                    line
                )
                if match:
                    field, op, value, action = match.groups()
                    current_rule['conditions'].append({
                        'field': field,
                        'operator': op,
                        'value': self._parse_value(value),
                        'action': action
                    })
            
            # Fim de regra
            elif line == 'END':
                if current_rule:
                    rules.append(current_rule)
                current_rule = None
        
        return rules
    
    def _parse_value(self, value: str) -> Any:
        """Parse valor string para tipo apropriado."""
        
        value = value.strip()
        
        # String
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        
        # Lista
        if value.startswith('[') and value.endswith(']'):
            items = value[1:-1].split(',')
            return [self._parse_value(i.strip()) for i in items]
        
        # Número
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return value


# === Exemplo de Uso ===

RULES_CONTENT = '''
# Arquivo: regras_auto.rules
RULE premium_base
  IF vehicle_type = "car" THEN premium = 1000
  IF vehicle_type = "motorcycle" THEN premium = 500
  IF vehicle_type = "truck" THEN premium = 2000
END

RULE age_modifier
  IF driver_age < 25 THEN premium = premium * 1.5
  IF driver_age > 65 THEN premium = premium * 1.2
END
'''

parser = RulesParser()
rules = parser.parse_file(RULES_CONTENT)
```

---

## Exercício 3: Migração de Banco de Dados (Resumo)

### Wrapper Python para Oracle

```python
# oracle_wrapper.py
"""
Wrapper Python para procedure Oracle.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from decimal import Decimal


@dataclass
class ComissaoResult:
    """Resultado do cálculo de comissão."""
    comissao: Decimal
    detalhes: List[Dict[str, Any]]


class ComissaoOracleWrapper:
    """Wrapper para procedure Oracle de comissão."""
    
    def __init__(self, connection):
        self.conn = connection
    
    def calcular(
        self,
        vendedor_id: int,
        mes: int,
        ano: int
    ) -> ComissaoResult:
        """
        Chama procedure Oracle e retorna resultado estruturado.
        """
        
        cursor = self.conn.cursor()
        
        # Output parameters
        comissao_var = cursor.var(float)
        detalhes_cursor = cursor.var(cursor)
        
        # Chamar procedure
        cursor.callproc(
            'calcular_comissao',
            [vendedor_id, mes, ano, comissao_var, detalhes_cursor]
        )
        
        # Extrair resultados
        comissao = Decimal(str(comissao_var.getvalue() or 0))
        
        detalhes = []
        for row in detalhes_cursor.getvalue():
            detalhes.append({
                'id': row[0],
                'valor': Decimal(str(row[1])),
                'comissao_item': Decimal(str(row[2]))
            })
        
        return ComissaoResult(
            comissao=comissao,
            detalhes=detalhes
        )


# === Implementação PostgreSQL ===

class ComissaoPostgres:
    """
    Reimplementação em Python/PostgreSQL.
    
    Mantém mesma lógica de negócio.
    """
    
    FAIXAS = [
        (1.5, 0.15, 500),   # >= 150% meta: 15% + R$500
        (1.0, 0.10, 0),     # >= 100% meta: 10%
        (0.8, 0.05, 0),     # >= 80% meta: 5%
        (0.0, 0.02, 0),     # < 80% meta: 2%
    ]
    
    def __init__(self, session):
        self.session = session
    
    def calcular(
        self,
        vendedor_id: int,
        mes: int,
        ano: int
    ) -> ComissaoResult:
        """Calcula comissão usando mesma lógica."""
        
        # Total de vendas
        total_vendas = self._get_total_vendas(vendedor_id, mes, ano)
        
        # Meta
        meta = self._get_meta(vendedor_id, mes, ano)
        
        # Determinar faixa
        percentual, bonus = self._determinar_faixa(total_vendas, meta)
        
        # Calcular comissão
        comissao = (total_vendas * percentual) + bonus
        
        # Detalhes
        detalhes = self._get_detalhes(vendedor_id, mes, ano, percentual)
        
        return ComissaoResult(
            comissao=Decimal(str(round(comissao, 2))),
            detalhes=detalhes
        )
    
    def _determinar_faixa(
        self,
        total: Decimal,
        meta: Decimal
    ) -> tuple:
        """Determina percentual e bonus baseado na faixa."""
        
        if meta == 0:
            return (Decimal('0.02'), Decimal('0'))
        
        ratio = total / meta
        
        for threshold, percent, bonus in self.FAIXAS:
            if ratio >= threshold:
                return (Decimal(str(percent)), Decimal(str(bonus)))
        
        return (Decimal('0.02'), Decimal('0'))
```

---

## Exercício 4: Projeto Final - CNPJ 2026

> **📝 Nota**: Este exercício é o projeto final e deve ser realizado
> consultando o material em `05-caso-pratico-cnpj/`.
>
> O gabarito completo está documentado nos arquivos:
> - `05-caso-pratico-cnpj/cenario-migracao.md`
> - `05-caso-pratico-cnpj/plano-de-testes.md`
> - `05-caso-pratico-cnpj/implementacao-testes.md`
> - `05-caso-pratico-cnpj/checklist-go-live.md`

---

## Critérios de Avaliação

### Rubrica de Avaliação

| Nível | Pontuação | Características |
|-------|-----------|-----------------|
| 🔴 Insuficiente | 0-40% | Solução incompleta, erros críticos |
| 🟠 Regular | 41-60% | Funciona parcialmente, falta cobertura |
| 🟡 Bom | 61-80% | Solução completa, boa cobertura |
| 🟢 Excelente | 81-100% | Solução robusta, documentação exemplar |

### Checklist de Autoavaliação

- [ ] Todos os comportamentos do legado foram documentados?
- [ ] O Golden Master cobre casos de borda?
- [ ] O Facade suporta rollback em < 30 segundos?
- [ ] Os testes de regressão passam em 100%?
- [ ] Há logging suficiente para auditoria?
- [ ] O plano de rollback foi testado?

---

## 🔗 Próximos Passos

Após completar os exercícios avançados:

1. **Aplique no caso prático CNPJ 2026**
   - [05-caso-pratico-cnpj/](../05-caso-pratico-cnpj/)

2. **Revise o material teórico**
   - [01-fundamentos/](../01-fundamentos/)
   - [02-tecnicas/](../02-tecnicas/)

3. **Pratique em projetos reais**
   - Use o validador em `src/cnpj_validator/`
   - Crie seus próprios Golden Masters
