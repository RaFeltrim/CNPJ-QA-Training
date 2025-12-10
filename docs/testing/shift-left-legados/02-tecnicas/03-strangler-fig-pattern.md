# 🌿 Strangler Fig Pattern

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- ✅ Entender o Strangler Fig Pattern e sua origem
- ✅ Aplicar a técnica para migrar sistemas legados gradualmente
- ✅ Implementar rotas e proxies para migração incremental
- ✅ Testar tanto o sistema legado quanto o novo simultaneamente

---

## 1. O Que é Strangler Fig Pattern?

### 1.1 Origem do Nome

> O padrão recebe o nome da **figueira-estranguladora** (Strangler Fig),
> uma planta tropical que cresce ao redor de árvores existentes,
> eventualmente substituindo-as completamente.

```text
┌─────────────────────────────────────────────────────────────────┐
│                    FIGUEIRA ESTRANGULADORA                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    FASE 1: Semente          FASE 2: Crescimento    FASE 3: Final│
│                                                                  │
│         🌱                      🌿🌲                   🌳        │
│        /│\                     /│││\                  /│\       │
│         │                      │││││                  │││       │
│        🌲                      🌲│🌲                   │││       │
│    Árvore Host             Fig ao redor           Fig domina    │
│                            da árvore              Árvore morta  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Aplicação em Software

```text
┌─────────────────────────────────────────────────────────────────┐
│                    STRANGLER FIG EM SOFTWARE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FASE 1: Sistema Legado      FASE 2: Migração      FASE 3: Novo │
│                                                                  │
│      ┌─────────┐             ┌─────────┐           ┌─────────┐  │
│      │ Legado  │             │ Proxy/  │           │  Novo   │  │
│      │ 100%    │             │ Facade  │           │  100%   │  │
│      └─────────┘             └────┬────┘           └─────────┘  │
│           │                  ┌────┴────┐                │       │
│           │                  │         │                │       │
│           │              ┌───┴───┐ ┌───┴───┐            │       │
│           ▼              │Legado │ │ Novo  │            ▼       │
│      Sistema             │ 60%   │ │ 40%   │       Sistema      │
│      Legado              └───────┘ └───────┘       Novo         │
│                                                                  │
│  Tudo passa pelo     Proxy decide qual     Legado removido      │
│  sistema antigo      sistema usar          completamente        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Implementação Básica

### 2.1 Estrutura do Padrão

```python
# strangler_facade.py
"""
Strangler Fig Facade para migração de validador CNPJ.

Este facade roteia requisições entre o sistema legado e o novo,
permitindo migração gradual e segura.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RouteStrategy(Enum):
    """Estratégias de roteamento."""
    LEGACY_ONLY = "legacy"        # 100% legado
    NEW_ONLY = "new"              # 100% novo
    PERCENTAGE = "percentage"      # % para novo
    FEATURE_FLAG = "flag"          # Baseado em flag
    CANARY = "canary"             # Usuários específicos


class StranglerFacade(ABC):
    """
    Facade base para implementar Strangler Fig Pattern.
    
    Esta classe abstrata define o contrato para facades que
    roteiam entre implementação legada e nova.
    """
    
    def __init__(self, strategy: RouteStrategy = RouteStrategy.LEGACY_ONLY):
        self.strategy = strategy
        self._new_percentage = 0
        self._feature_flags: Dict[str, bool] = {}
        self._canary_users: set = set()
    
    @abstractmethod
    def _call_legacy(self, *args, **kwargs) -> Any:
        """Executa implementação legada."""
        pass
    
    @abstractmethod
    def _call_new(self, *args, **kwargs) -> Any:
        """Executa nova implementação."""
        pass
    
    def set_new_percentage(self, percentage: int):
        """Define % de tráfego para nova implementação."""
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage deve estar entre 0 e 100")
        self._new_percentage = percentage
        logger.info(f"Tráfego para nova implementação: {percentage}%")
    
    def set_feature_flag(self, flag: str, enabled: bool):
        """Define estado de uma feature flag."""
        self._feature_flags[flag] = enabled
        logger.info(f"Feature flag '{flag}': {'enabled' if enabled else 'disabled'}")
    
    def add_canary_user(self, user_id: str):
        """Adiciona usuário ao grupo canary."""
        self._canary_users.add(user_id)
    
    def _should_use_new(self, **context) -> bool:
        """
        Decide se deve usar nova implementação.
        
        Args:
            context: Contexto adicional (user_id, feature_flag, etc)
        """
        if self.strategy == RouteStrategy.LEGACY_ONLY:
            return False
        
        if self.strategy == RouteStrategy.NEW_ONLY:
            return True
        
        if self.strategy == RouteStrategy.PERCENTAGE:
            import random
            return random.randint(1, 100) <= self._new_percentage
        
        if self.strategy == RouteStrategy.FEATURE_FLAG:
            flag = context.get("feature_flag")
            return self._feature_flags.get(flag, False)
        
        if self.strategy == RouteStrategy.CANARY:
            user_id = context.get("user_id")
            return user_id in self._canary_users
        
        return False
    
    def execute(self, *args, **kwargs) -> Any:
        """
        Executa a operação, roteando para legado ou novo.
        
        Este método é o ponto de entrada principal. Ele decide
        qual implementação usar e garante logging adequado.
        """
        context = kwargs.pop("_context", {})
        use_new = self._should_use_new(**context)
        
        implementation = "NEW" if use_new else "LEGACY"
        logger.debug(f"Routing to {implementation} implementation")
        
        try:
            if use_new:
                result = self._call_new(*args, **kwargs)
            else:
                result = self._call_legacy(*args, **kwargs)
            
            logger.debug(f"{implementation} returned: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in {implementation}: {e}")
            raise
```

### 2.2 Aplicação no CNPJ

```python
# cnpj_strangler_facade.py
"""
Strangler Facade específico para migração do validador de CNPJ.

Permite migrar gradualmente de validação somente numérica
para validação alfanumérica (2026).
"""

from strangler_facade import StranglerFacade, RouteStrategy
from typing import Optional
import logging

# Importar implementações
from legacy.cnpj_utils import proc_cnpj as legacy_validate
from src.cnpj_validator.alphanumeric_validator import AlphanumericValidator

logger = logging.getLogger(__name__)


class CNPJStranglerFacade(StranglerFacade):
    """
    Facade para migração do validador de CNPJ.
    
    Exemplo de uso:
        # Iniciar com 100% legado
        facade = CNPJStranglerFacade()
        
        # Migrar para 10% nova implementação
        facade.set_strategy(RouteStrategy.PERCENTAGE)
        facade.set_new_percentage(10)
        
        # Eventualmente, 100% nova
        facade.set_strategy(RouteStrategy.NEW_ONLY)
    """
    
    def __init__(self, strategy: RouteStrategy = RouteStrategy.LEGACY_ONLY):
        super().__init__(strategy)
        self._new_validator = AlphanumericValidator()
    
    def _call_legacy(self, cnpj: str, **kwargs) -> bool:
        """
        Chama validador legado.
        
        O legado usa a função proc_cnpj com f=True para modo validação.
        """
        logger.debug(f"Validando com LEGADO: {cnpj}")
        return legacy_validate(cnpj, f=True)
    
    def _call_new(self, cnpj: str, **kwargs) -> bool:
        """
        Chama novo validador alfanumérico.
        
        O novo validador suporta CNPJs alfanuméricos.
        """
        logger.debug(f"Validando com NOVO: {cnpj}")
        return self._new_validator.validate(cnpj)
    
    def validate(self, cnpj: str, **context) -> bool:
        """
        Valida um CNPJ, roteando para implementação apropriada.
        
        Args:
            cnpj: CNPJ a validar (numérico ou alfanumérico)
            **context: Contexto para decisão de roteamento
                - user_id: ID do usuário (para canary)
                - feature_flag: Nome da flag (para feature flags)
        
        Returns:
            True se CNPJ válido, False caso contrário
        """
        return self.execute(cnpj, _context=context)
    
    def validate_with_comparison(self, cnpj: str) -> dict:
        """
        Valida CNPJ com AMBAS implementações e compara.
        
        Útil para fase de testes em paralelo (shadow mode).
        
        Returns:
            Dict com resultados de ambas implementações
        """
        legacy_result = self._call_legacy(cnpj)
        new_result = self._call_new(cnpj)
        
        match = legacy_result == new_result
        
        if not match:
            logger.warning(
                f"DIVERGÊNCIA DETECTADA para CNPJ {cnpj}:\n"
                f"  Legado: {legacy_result}\n"
                f"  Novo: {new_result}"
            )
        
        return {
            "cnpj": cnpj,
            "legacy_result": legacy_result,
            "new_result": new_result,
            "match": match
        }
```

---

## 3. Fases da Migração

### 3.1 Diagrama de Fases

```text
┌─────────────────────────────────────────────────────────────────┐
│                    FASES DA MIGRAÇÃO                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FASE 0: Preparação (Semanas 1-4)                               │
│  ├── Criar facade/proxy                                         │
│  ├── Implementar logging detalhado                              │
│  ├── Criar testes de caracterização                             │
│  └── Estratégia: LEGACY_ONLY                                    │
│                                                                  │
│  FASE 1: Shadow Mode (Semanas 5-8)                              │
│  ├── Executar AMBAS implementações                              │
│  ├── Comparar resultados (não usar novo em produção)            │
│  ├── Coletar divergências                                       │
│  └── Estratégia: LEGACY_ONLY + logging de comparação            │
│                                                                  │
│  FASE 2: Canary Release (Semanas 9-12)                          │
│  ├── Direcionar usuários de teste para novo                     │
│  ├── Monitorar métricas e erros                                 │
│  ├── Rollback rápido se problemas                               │
│  └── Estratégia: CANARY (5% dos usuários)                       │
│                                                                  │
│  FASE 3: Gradual Rollout (Semanas 13-20)                        │
│  ├── Aumentar % gradualmente (10% → 25% → 50% → 75%)            │
│  ├── Monitorar em cada aumento                                  │
│  ├── Ajustar baseado em feedback                                │
│  └── Estratégia: PERCENTAGE (crescente)                         │
│                                                                  │
│  FASE 4: Full Migration (Semanas 21-24)                         │
│  ├── 100% para nova implementação                               │
│  ├── Manter legado como fallback                                │
│  ├── Monitorar intensivamente                                   │
│  └── Estratégia: NEW_ONLY                                       │
│                                                                  │
│  FASE 5: Cleanup (Após estabilização)                           │
│  ├── Remover código legado                                      │
│  ├── Remover facade                                             │
│  ├── Simplificar arquitetura                                    │
│  └── Documentar lições aprendidas                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Implementação das Fases

```python
# migration_controller.py
"""
Controlador de migração com suporte a diferentes fases.
"""

from enum import Enum
from datetime import datetime
from typing import Dict, List
import logging

from cnpj_strangler_facade import CNPJStranglerFacade
from strangler_facade import RouteStrategy

logger = logging.getLogger(__name__)


class MigrationPhase(Enum):
    """Fases da migração."""
    PREPARATION = "preparation"
    SHADOW_MODE = "shadow_mode"
    CANARY = "canary"
    GRADUAL_ROLLOUT = "gradual_rollout"
    FULL_MIGRATION = "full_migration"
    CLEANUP = "cleanup"


class MigrationController:
    """
    Controla a migração do sistema legado para o novo.
    
    Exemplo:
        controller = MigrationController()
        controller.set_phase(MigrationPhase.CANARY)
        
        # Validar usando fase atual
        result = controller.validate("11222333000181")
    """
    
    def __init__(self):
        self.facade = CNPJStranglerFacade()
        self.current_phase = MigrationPhase.PREPARATION
        self._divergences: List[Dict] = []
        self._metrics: Dict = {
            "legacy_calls": 0,
            "new_calls": 0,
            "divergences": 0,
            "errors_legacy": 0,
            "errors_new": 0,
        }
    
    def set_phase(self, phase: MigrationPhase):
        """
        Configura a fase de migração.
        
        Automaticamente ajusta estratégia e parâmetros do facade.
        """
        self.current_phase = phase
        logger.info(f"Migração: entrando na fase {phase.value}")
        
        if phase == MigrationPhase.PREPARATION:
            self.facade.strategy = RouteStrategy.LEGACY_ONLY
        
        elif phase == MigrationPhase.SHADOW_MODE:
            self.facade.strategy = RouteStrategy.LEGACY_ONLY
            # Shadow mode: compara mas usa legado
        
        elif phase == MigrationPhase.CANARY:
            self.facade.strategy = RouteStrategy.CANARY
            # Adicionar usuários de teste
            self.facade.add_canary_user("test_user_1")
            self.facade.add_canary_user("qa_team")
        
        elif phase == MigrationPhase.GRADUAL_ROLLOUT:
            self.facade.strategy = RouteStrategy.PERCENTAGE
            self.facade.set_new_percentage(10)  # Começar com 10%
        
        elif phase == MigrationPhase.FULL_MIGRATION:
            self.facade.strategy = RouteStrategy.NEW_ONLY
        
        elif phase == MigrationPhase.CLEANUP:
            self.facade.strategy = RouteStrategy.NEW_ONLY
            logger.info("CLEANUP: Preparar para remover código legado")
    
    def validate(self, cnpj: str, user_id: str = None) -> bool:
        """
        Valida CNPJ usando estratégia da fase atual.
        
        Em shadow mode, executa comparação mas retorna legado.
        """
        if self.current_phase == MigrationPhase.SHADOW_MODE:
            # Shadow mode: comparar ambos
            comparison = self.facade.validate_with_comparison(cnpj)
            
            if not comparison["match"]:
                self._divergences.append({
                    "cnpj": cnpj,
                    "timestamp": datetime.now().isoformat(),
                    **comparison
                })
                self._metrics["divergences"] += 1
            
            self._metrics["legacy_calls"] += 1
            return comparison["legacy_result"]
        
        else:
            # Outras fases: usar facade normalmente
            context = {"user_id": user_id} if user_id else {}
            return self.facade.validate(cnpj, **context)
    
    def increase_rollout(self, new_percentage: int):
        """Aumenta % do gradual rollout."""
        if self.current_phase != MigrationPhase.GRADUAL_ROLLOUT:
            raise ValueError("Só pode aumentar rollout na fase GRADUAL_ROLLOUT")
        
        current = self.facade._new_percentage
        if new_percentage <= current:
            raise ValueError(f"Novo % ({new_percentage}) deve ser maior que atual ({current})")
        
        self.facade.set_new_percentage(new_percentage)
        logger.info(f"Rollout aumentado: {current}% → {new_percentage}%")
    
    def get_metrics(self) -> Dict:
        """Retorna métricas da migração."""
        return {
            **self._metrics,
            "current_phase": self.current_phase.value,
            "divergences_list": self._divergences[-10:]  # Últimas 10
        }
    
    def get_divergence_report(self) -> str:
        """Gera relatório de divergências."""
        if not self._divergences:
            return "Nenhuma divergência encontrada."
        
        report = f"RELATÓRIO DE DIVERGÊNCIAS\n"
        report += f"Total: {len(self._divergences)}\n\n"
        
        for div in self._divergences[:20]:
            report += f"CNPJ: {div['cnpj']}\n"
            report += f"  Legado: {div['legacy_result']}\n"
            report += f"  Novo: {div['new_result']}\n"
            report += f"  Timestamp: {div['timestamp']}\n\n"
        
        return report
```

---

## 4. Testando o Strangler Fig

### 4.1 Testes de Paridade

```python
# test_strangler_facade.py
"""
Testes para garantir que o Strangler Facade funciona corretamente.
"""

import pytest
from unittest.mock import Mock, patch

from cnpj_strangler_facade import CNPJStranglerFacade
from strangler_facade import RouteStrategy


class TestStranglerFacadeRouting:
    """Testes de roteamento do facade."""
    
    @pytest.fixture
    def facade(self):
        return CNPJStranglerFacade()
    
    def test_legacy_only_sempre_usa_legado(self, facade):
        """LEGACY_ONLY deve sempre rotear para legado."""
        facade.strategy = RouteStrategy.LEGACY_ONLY
        
        with patch.object(facade, '_call_legacy', return_value=True) as mock_legacy:
            with patch.object(facade, '_call_new') as mock_new:
                result = facade.validate("11222333000181")
                
                mock_legacy.assert_called_once()
                mock_new.assert_not_called()
    
    def test_new_only_sempre_usa_novo(self, facade):
        """NEW_ONLY deve sempre rotear para novo."""
        facade.strategy = RouteStrategy.NEW_ONLY
        
        with patch.object(facade, '_call_legacy') as mock_legacy:
            with patch.object(facade, '_call_new', return_value=True) as mock_new:
                result = facade.validate("11222333000181")
                
                mock_legacy.assert_not_called()
                mock_new.assert_called_once()
    
    def test_canary_roteia_usuarios_especificos(self, facade):
        """CANARY deve rotear usuários do grupo para novo."""
        facade.strategy = RouteStrategy.CANARY
        facade.add_canary_user("user_teste")
        
        with patch.object(facade, '_call_legacy') as mock_legacy:
            with patch.object(facade, '_call_new', return_value=True) as mock_new:
                # Usuário canary vai para novo
                facade.validate("11222333000181", user_id="user_teste")
                mock_new.assert_called_once()
                mock_legacy.assert_not_called()
                
                mock_new.reset_mock()
                
                # Usuário normal vai para legado
                with patch.object(facade, '_call_legacy', return_value=True):
                    facade.validate("11222333000181", user_id="user_normal")


class TestStranglerFacadeParidade:
    """
    Testes de paridade entre implementações.
    
    Estes testes garantem que o novo sistema se comporta
    EXATAMENTE como o legado para todos os casos conhecidos.
    """
    
    @pytest.fixture
    def facade(self):
        return CNPJStranglerFacade()
    
    @pytest.fixture
    def cnpj_test_cases(self):
        """Casos de teste para verificar paridade."""
        return [
            # (CNPJ, resultado_esperado)
            ("11222333000181", True),
            ("11.222.333/0001-81", True),
            ("11222333000182", False),  # DV errado
            ("11111111111111", False),  # Todos iguais
            ("123", False),              # Curto
            ("", False),                 # Vazio (pode ser None)
        ]
    
    def test_paridade_legado_novo(self, facade, cnpj_test_cases):
        """
        Novo sistema deve ter mesmos resultados que legado.
        
        ⚠️ Este teste é CRÍTICO durante a migração.
        Qualquer divergência deve ser investigada.
        """
        divergencias = []
        
        for cnpj, _ in cnpj_test_cases:
            comparison = facade.validate_with_comparison(cnpj)
            
            if not comparison["match"]:
                divergencias.append(comparison)
        
        if divergencias:
            report = "\n".join([
                f"CNPJ: {d['cnpj']}, Legado: {d['legacy_result']}, Novo: {d['new_result']}"
                for d in divergencias
            ])
            pytest.fail(f"Divergências encontradas:\n{report}")
    
    @pytest.mark.parametrize("cnpj,esperado", [
        ("11222333000181", True),
        ("11.222.333/0001-81", True),
        ("11222333000182", False),
        ("00000000000000", False),
    ])
    def test_paridade_parametrizada(self, facade, cnpj, esperado):
        """Teste parametrizado de paridade."""
        comparison = facade.validate_with_comparison(cnpj)
        
        assert comparison["match"], \
            f"Divergência para {cnpj}: legado={comparison['legacy_result']}, novo={comparison['new_result']}"
```

### 4.2 Testes de Performance

```python
# test_strangler_performance.py
"""
Testes de performance para comparar legado vs novo.
"""

import pytest
import time
from statistics import mean, stdev

from cnpj_strangler_facade import CNPJStranglerFacade


class TestStranglerPerformance:
    """Comparar performance entre implementações."""
    
    @pytest.fixture
    def facade(self):
        return CNPJStranglerFacade()
    
    @pytest.fixture
    def sample_cnpjs(self):
        """Amostra de CNPJs para teste de performance."""
        return [
            "11222333000181",
            "11.222.333/0001-81",
            "12345678000195",
            "00000000000191",
            "11222333000182",  # Inválido
        ] * 100  # 500 validações
    
    def test_performance_comparison(self, facade, sample_cnpjs):
        """
        Compara tempo de execução legado vs novo.
        
        Novo não deve ser significativamente mais lento.
        """
        # Medir legado
        legacy_times = []
        for cnpj in sample_cnpjs:
            start = time.perf_counter()
            facade._call_legacy(cnpj)
            legacy_times.append(time.perf_counter() - start)
        
        # Medir novo
        new_times = []
        for cnpj in sample_cnpjs:
            start = time.perf_counter()
            facade._call_new(cnpj)
            new_times.append(time.perf_counter() - start)
        
        legacy_mean = mean(legacy_times) * 1000  # ms
        new_mean = mean(new_times) * 1000
        
        print(f"\nPerformance (média em ms):")
        print(f"  Legado: {legacy_mean:.3f}ms")
        print(f"  Novo:   {new_mean:.3f}ms")
        print(f"  Diferença: {((new_mean/legacy_mean)-1)*100:.1f}%")
        
        # Novo não deve ser mais que 50% mais lento
        assert new_mean < legacy_mean * 1.5, \
            f"Novo ({new_mean:.3f}ms) é muito mais lento que legado ({legacy_mean:.3f}ms)"
```

---

## 5. Exercício Prático

### 5.1 Cenário

Você precisa migrar um sistema de formatação de CNPJ usando Strangler Fig.

**Sistema legado:**
```python
def format_cnpj_legacy(cnpj):
    """Formatador legado - só aceita numérico."""
    cnpj = ''.join(c for c in str(cnpj) if c.isdigit())
    if len(cnpj) != 14:
        return cnpj
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
```

**Sistema novo:**
```python
def format_cnpj_new(cnpj):
    """Formatador novo - aceita alfanumérico."""
    cnpj = ''.join(c for c in str(cnpj).upper() if c.isalnum())
    if len(cnpj) != 14:
        return cnpj
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
```

### 5.2 Tarefa

Complete o facade abaixo:

```python
# exercicio_strangler_facade.py

from strangler_facade import StranglerFacade, RouteStrategy


class CNPJFormatterStranglerFacade(StranglerFacade):
    """
    TODO: Implementar facade para migração do formatador.
    
    Requisitos:
    1. _call_legacy deve usar format_cnpj_legacy
    2. _call_new deve usar format_cnpj_new
    3. Método format() deve rotear baseado na estratégia
    4. Método format_with_comparison() deve retornar ambos resultados
    """
    
    def _call_legacy(self, cnpj: str) -> str:
        # TODO: Implementar
        pass
    
    def _call_new(self, cnpj: str) -> str:
        # TODO: Implementar
        pass
    
    def format(self, cnpj: str, **context) -> str:
        # TODO: Implementar
        pass
    
    def format_with_comparison(self, cnpj: str) -> dict:
        # TODO: Implementar
        pass


# Testes para validar sua implementação
def test_facade_legacy_only():
    facade = CNPJFormatterStranglerFacade(RouteStrategy.LEGACY_ONLY)
    result = facade.format("11222333000181")
    assert result == "11.222.333/0001-81"


def test_facade_paridade_numerico():
    facade = CNPJFormatterStranglerFacade()
    comparison = facade.format_with_comparison("11222333000181")
    assert comparison["match"], "CNPJs numéricos devem ter mesmo resultado"


def test_facade_diferenca_alfanumerico():
    facade = CNPJFormatterStranglerFacade()
    comparison = facade.format_with_comparison("AB222333000181")
    # Legado vai remover letras, novo vai manter
    assert not comparison["match"], "CNPJs alfanuméricos devem ter resultados diferentes"
```

---

## 6. Resumo

### 6.1 Quando Usar Strangler Fig

| Situação | Use Strangler Fig? |
|----------|-------------------|
| Migração de sistema grande | ✅ Sim |
| Precisa de rollback rápido | ✅ Sim |
| Equipe pequena, risco alto | ✅ Sim |
| Sistema crítico em produção | ✅ Sim |
| Mudança pequena e isolada | ❌ Não, muito overhead |
| Sistema novo (greenfield) | ❌ Não necessário |

### 6.2 Checklist de Implementação

```text
☐ Facade/proxy criado
☐ Logging de todas as chamadas
☐ Métricas de comparação implementadas
☐ Testes de paridade criados
☐ Shadow mode funcionando
☐ Canary release configurado
☐ Rollout gradual planejado
☐ Processo de rollback documentado
☐ Monitoramento configurado
☐ Plano de cleanup definido
```

---

**Próximo**: [04-feature-flags.md](04-feature-flags.md)
