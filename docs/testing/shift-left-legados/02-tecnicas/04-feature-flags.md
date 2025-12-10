# 🚩 Feature Flags para Migrações

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- ✅ Entender o que são Feature Flags e seus tipos
- ✅ Implementar sistema de Feature Flags para migrações
- ✅ Criar estratégias de rollout controlado
- ✅ Testar código com Feature Flags

---

## 1. O Que São Feature Flags?

### 1.1 Definição

> **Feature Flag** (também chamada Feature Toggle) = Um mecanismo que permite
> habilitar ou desabilitar funcionalidades sem fazer deploy de novo código.

```text
┌─────────────────────────────────────────────────────────────────┐
│                      FEATURE FLAGS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SEM Feature Flags:                                              │
│                                                                  │
│    Deploy → Funcionalidade SEMPRE ativa                         │
│    Problema? → Novo deploy para desativar                       │
│                                                                  │
│  COM Feature Flags:                                              │
│                                                                  │
│    Deploy → Funcionalidade controlada por flag                  │
│                                                                  │
│    if feature_flag("nova_validacao"):                           │
│        usar_nova_validacao()                                    │
│    else:                                                         │
│        usar_validacao_antiga()                                  │
│                                                                  │
│    Problema? → Desativa flag (sem deploy!)                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Tipos de Feature Flags

```text
┌─────────────────────────────────────────────────────────────────┐
│                    TIPOS DE FEATURE FLAGS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. RELEASE FLAGS (Lançamento)                                   │
│     Propósito: Controlar lançamento de novas features           │
│     Duração: Temporária (remover após estabilizar)              │
│     Exemplo: "cnpj_alfanumerico_enabled"                        │
│                                                                  │
│  2. OPS FLAGS (Operacionais)                                     │
│     Propósito: Controlar comportamento operacional              │
│     Duração: Permanente ou longa                                │
│     Exemplo: "modo_manutencao", "cache_enabled"                 │
│                                                                  │
│  3. EXPERIMENT FLAGS (Experimentos)                              │
│     Propósito: Testes A/B e experimentos                        │
│     Duração: Temporária (duração do experimento)                │
│     Exemplo: "novo_ui_checkout_v2"                              │
│                                                                  │
│  4. PERMISSION FLAGS (Permissões)                                │
│     Propósito: Controlar acesso por usuário/grupo               │
│     Duração: Permanente                                          │
│     Exemplo: "beta_users", "premium_features"                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Implementação Básica

### 2.1 Sistema de Feature Flags

```python
# feature_flags.py
"""
Sistema de Feature Flags para controle de funcionalidades.

Suporta:
- Flags simples (on/off)
- Rollout gradual por porcentagem
- Segmentação por usuário/grupo
- Regras baseadas em contexto
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class FlagType(Enum):
    """Tipos de feature flags."""
    RELEASE = "release"
    OPS = "ops"
    EXPERIMENT = "experiment"
    PERMISSION = "permission"


@dataclass
class FeatureFlag:
    """
    Representa uma feature flag.
    
    Attributes:
        name: Nome único da flag
        enabled: Se está habilitada globalmente
        flag_type: Tipo da flag (release, ops, etc)
        percentage: % de usuários que verão a feature (0-100)
        allowed_users: Lista de user_ids que sempre veem a feature
        allowed_groups: Lista de grupos que sempre veem a feature
        start_date: Data de início (None = imediato)
        end_date: Data de fim (None = sem fim)
        metadata: Dados adicionais
    """
    name: str
    enabled: bool = False
    flag_type: FlagType = FlagType.RELEASE
    percentage: int = 0
    allowed_users: List[str] = field(default_factory=list)
    allowed_groups: List[str] = field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class FeatureFlagService:
    """
    Serviço para gerenciar e avaliar feature flags.
    
    Exemplo de uso:
        service = FeatureFlagService()
        
        # Criar flag
        service.create_flag(
            name="cnpj_alfanumerico",
            enabled=True,
            percentage=10,  # 10% dos usuários
        )
        
        # Verificar flag
        if service.is_enabled("cnpj_alfanumerico", user_id="user123"):
            usar_cnpj_alfanumerico()
    """
    
    def __init__(self, storage_file: str = None):
        self._flags: Dict[str, FeatureFlag] = {}
        self._storage_file = storage_file
        
        if storage_file:
            self._load_from_file()
    
    def create_flag(
        self,
        name: str,
        enabled: bool = False,
        flag_type: FlagType = FlagType.RELEASE,
        percentage: int = 0,
        allowed_users: List[str] = None,
        allowed_groups: List[str] = None,
        **kwargs
    ) -> FeatureFlag:
        """Cria uma nova feature flag."""
        flag = FeatureFlag(
            name=name,
            enabled=enabled,
            flag_type=flag_type,
            percentage=percentage,
            allowed_users=allowed_users or [],
            allowed_groups=allowed_groups or [],
            **kwargs
        )
        self._flags[name] = flag
        self._save_to_file()
        
        logger.info(f"Feature flag criada: {name} (enabled={enabled})")
        return flag
    
    def get_flag(self, name: str) -> Optional[FeatureFlag]:
        """Retorna uma flag pelo nome."""
        return self._flags.get(name)
    
    def update_flag(self, name: str, **updates) -> FeatureFlag:
        """Atualiza uma flag existente."""
        flag = self._flags.get(name)
        if not flag:
            raise KeyError(f"Flag não encontrada: {name}")
        
        for key, value in updates.items():
            if hasattr(flag, key):
                setattr(flag, key, value)
        
        self._save_to_file()
        logger.info(f"Feature flag atualizada: {name} -> {updates}")
        return flag
    
    def delete_flag(self, name: str):
        """Remove uma flag."""
        if name in self._flags:
            del self._flags[name]
            self._save_to_file()
            logger.info(f"Feature flag removida: {name}")
    
    def is_enabled(
        self,
        name: str,
        user_id: str = None,
        groups: List[str] = None,
        context: Dict = None
    ) -> bool:
        """
        Verifica se uma flag está habilitada para um contexto específico.
        
        Ordem de avaliação:
        1. Flag existe?
        2. Flag habilitada globalmente?
        3. Dentro do período de validade?
        4. Usuário na lista de permitidos?
        5. Grupo na lista de permitidos?
        6. Percentual de rollout?
        
        Args:
            name: Nome da flag
            user_id: ID do usuário
            groups: Lista de grupos do usuário
            context: Contexto adicional
        
        Returns:
            True se feature habilitada, False caso contrário
        """
        flag = self._flags.get(name)
        
        # 1. Flag não existe
        if not flag:
            logger.debug(f"Flag '{name}' não existe -> False")
            return False
        
        # 2. Flag desabilitada globalmente
        if not flag.enabled:
            logger.debug(f"Flag '{name}' desabilitada -> False")
            return False
        
        # 3. Verificar período de validade
        now = datetime.now()
        if flag.start_date and now < flag.start_date:
            logger.debug(f"Flag '{name}' ainda não iniciou -> False")
            return False
        if flag.end_date and now > flag.end_date:
            logger.debug(f"Flag '{name}' expirou -> False")
            return False
        
        # 4. Usuário na lista de permitidos
        if user_id and user_id in flag.allowed_users:
            logger.debug(f"Flag '{name}' usuário permitido -> True")
            return True
        
        # 5. Grupo na lista de permitidos
        if groups:
            for group in groups:
                if group in flag.allowed_groups:
                    logger.debug(f"Flag '{name}' grupo permitido -> True")
                    return True
        
        # 6. Rollout por porcentagem
        if flag.percentage > 0 and user_id:
            # Usar hash consistente para mesmo usuário sempre ter mesmo resultado
            user_bucket = self._get_user_bucket(user_id, name)
            if user_bucket <= flag.percentage:
                logger.debug(f"Flag '{name}' usuário no bucket {user_bucket}% -> True")
                return True
            else:
                logger.debug(f"Flag '{name}' usuário no bucket {user_bucket}% > {flag.percentage}% -> False")
                return False
        
        # Se percentage = 100, habilitar para todos
        if flag.percentage >= 100:
            return True
        
        # Default: habilitado (flag.enabled = True mas sem regras específicas)
        return flag.percentage >= 100
    
    def _get_user_bucket(self, user_id: str, flag_name: str) -> int:
        """
        Calcula bucket consistente para usuário.
        
        Mesmo usuário + mesma flag = mesmo bucket (0-100)
        Isso garante experiência consistente.
        """
        key = f"{user_id}:{flag_name}"
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return hash_value % 100 + 1  # 1-100
    
    def _save_to_file(self):
        """Salva flags em arquivo."""
        if not self._storage_file:
            return
        
        data = {}
        for name, flag in self._flags.items():
            data[name] = {
                "enabled": flag.enabled,
                "flag_type": flag.flag_type.value,
                "percentage": flag.percentage,
                "allowed_users": flag.allowed_users,
                "allowed_groups": flag.allowed_groups,
                "start_date": flag.start_date.isoformat() if flag.start_date else None,
                "end_date": flag.end_date.isoformat() if flag.end_date else None,
                "metadata": flag.metadata,
            }
        
        with open(self._storage_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_from_file(self):
        """Carrega flags de arquivo."""
        import os
        if not os.path.exists(self._storage_file):
            return
        
        with open(self._storage_file, 'r') as f:
            data = json.load(f)
        
        for name, config in data.items():
            self._flags[name] = FeatureFlag(
                name=name,
                enabled=config["enabled"],
                flag_type=FlagType(config["flag_type"]),
                percentage=config["percentage"],
                allowed_users=config.get("allowed_users", []),
                allowed_groups=config.get("allowed_groups", []),
                start_date=datetime.fromisoformat(config["start_date"]) if config.get("start_date") else None,
                end_date=datetime.fromisoformat(config["end_date"]) if config.get("end_date") else None,
                metadata=config.get("metadata", {}),
            )


# Instância global (singleton)
_feature_flag_service: FeatureFlagService = None


def get_feature_flag_service() -> FeatureFlagService:
    """Retorna instância singleton do serviço."""
    global _feature_flag_service
    if _feature_flag_service is None:
        _feature_flag_service = FeatureFlagService()
    return _feature_flag_service


def feature_flag(name: str, user_id: str = None, **kwargs) -> bool:
    """
    Função helper para verificar feature flag.
    
    Uso:
        if feature_flag("nova_feature", user_id="123"):
            fazer_coisa_nova()
    """
    return get_feature_flag_service().is_enabled(name, user_id=user_id, **kwargs)
```

### 2.2 Decorator para Feature Flags

```python
# feature_flag_decorators.py
"""
Decorators para simplificar uso de feature flags.
"""

from functools import wraps
from typing import Callable, Any
from feature_flags import feature_flag


def with_feature_flag(
    flag_name: str,
    fallback: Callable = None,
    default_value: Any = None
):
    """
    Decorator que condiciona execução de função a uma feature flag.
    
    Args:
        flag_name: Nome da flag
        fallback: Função alternativa se flag desabilitada
        default_value: Valor a retornar se flag desabilitada (sem fallback)
    
    Exemplo:
        @with_feature_flag("nova_validacao", fallback=validacao_antiga)
        def validar_cnpj(cnpj):
            return nova_validacao(cnpj)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = kwargs.pop('_user_id', None)
            
            if feature_flag(flag_name, user_id=user_id):
                return func(*args, **kwargs)
            elif fallback:
                return fallback(*args, **kwargs)
            else:
                return default_value
        
        return wrapper
    return decorator


def feature_variant(flag_name: str, variants: dict):
    """
    Decorator para selecionar variante baseado em flag.
    
    Args:
        flag_name: Nome da flag
        variants: Dict mapeando valor da flag para função
    
    Exemplo:
        @feature_variant("algoritmo_validacao", {
            "v1": validacao_v1,
            "v2": validacao_v2,
            "v3": validacao_v3,
        })
        def validar(cnpj):
            # Implementação default
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            from feature_flags import get_feature_flag_service
            service = get_feature_flag_service()
            flag = service.get_flag(flag_name)
            
            if flag and flag.enabled:
                variant = flag.metadata.get("variant", None)
                if variant and variant in variants:
                    return variants[variant](*args, **kwargs)
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

---

## 3. Aplicação no CNPJ 2026

### 3.1 Configuração das Flags

```python
# cnpj_feature_flags.py
"""
Feature flags específicas para migração CNPJ alfanumérico 2026.
"""

from datetime import datetime
from feature_flags import (
    FeatureFlagService, 
    FeatureFlag, 
    FlagType,
    get_feature_flag_service
)


def setup_cnpj_2026_flags():
    """
    Configura feature flags para migração CNPJ 2026.
    
    Flags criadas:
    1. cnpj_alfanumerico_validation - Validação de CNPJs alfanuméricos
    2. cnpj_alfanumerico_format - Formatação de CNPJs alfanuméricos
    3. cnpj_alfanumerico_api - API aceitar CNPJs alfanuméricos
    4. cnpj_migration_shadow - Modo shadow (comparar legado vs novo)
    """
    service = get_feature_flag_service()
    
    # Flag 1: Validação de CNPJ Alfanumérico
    service.create_flag(
        name="cnpj_alfanumerico_validation",
        enabled=True,
        flag_type=FlagType.RELEASE,
        percentage=0,  # Começar desabilitado
        allowed_groups=["qa_team", "developers"],  # Time de QA e devs primeiro
        start_date=datetime(2025, 1, 1),  # Começar testes em 2025
        metadata={
            "description": "Habilita validação de CNPJs com letras",
            "jira": "CNPJ-2026",
            "owner": "time-cadastro",
        }
    )
    
    # Flag 2: Formatação de CNPJ Alfanumérico
    service.create_flag(
        name="cnpj_alfanumerico_format",
        enabled=True,
        flag_type=FlagType.RELEASE,
        percentage=0,
        allowed_groups=["qa_team"],
        metadata={
            "description": "Formata CNPJs mantendo letras",
            "depends_on": "cnpj_alfanumerico_validation",  # Depende da validação
        }
    )
    
    # Flag 3: API aceitar CNPJ Alfanumérico
    service.create_flag(
        name="cnpj_alfanumerico_api",
        enabled=False,  # Inicialmente desabilitado
        flag_type=FlagType.RELEASE,
        percentage=0,
        metadata={
            "description": "API de cadastro aceita CNPJs alfanuméricos",
            "breaking_change": True,
            "depends_on": ["cnpj_alfanumerico_validation", "cnpj_alfanumerico_format"],
        }
    )
    
    # Flag 4: Modo Shadow (comparação legado vs novo)
    service.create_flag(
        name="cnpj_migration_shadow",
        enabled=True,
        flag_type=FlagType.OPS,
        percentage=100,  # Todos os requests
        metadata={
            "description": "Executa validação nova em paralelo e compara",
            "log_divergences": True,
        }
    )
    
    print("✅ Feature flags CNPJ 2026 configuradas")
    return service


# Plano de rollout
CNPJ_2026_ROLLOUT_PLAN = """
╔══════════════════════════════════════════════════════════════════╗
║              PLANO DE ROLLOUT - CNPJ ALFANUMÉRICO                ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  FASE 1: Shadow Mode (Jan-Mar 2025)                              ║
║  ├── cnpj_migration_shadow = 100%                                ║
║  ├── Coletar divergências legado vs novo                         ║
║  └── Zero impacto em produção                                    ║
║                                                                   ║
║  FASE 2: Internal Testing (Abr-Jun 2025)                         ║
║  ├── cnpj_alfanumerico_validation = qa_team + developers         ║
║  ├── Testar em ambientes internos                                ║
║  └── Corrigir bugs encontrados                                   ║
║                                                                   ║
║  FASE 3: Beta Users (Jul-Set 2025)                               ║
║  ├── cnpj_alfanumerico_validation = 10% usuários                 ║
║  ├── Coletar feedback de usuários reais                          ║
║  └── Monitorar métricas de erro                                  ║
║                                                                   ║
║  FASE 4: Gradual Rollout (Out-Dez 2025)                          ║
║  ├── cnpj_alfanumerico_validation = 10% → 25% → 50% → 75%        ║
║  ├── Monitorar em cada incremento                                ║
║  └── Preparar para 100%                                          ║
║                                                                   ║
║  FASE 5: Full Release (Jan 2026)                                 ║
║  ├── cnpj_alfanumerico_validation = 100%                         ║
║  ├── cnpj_alfanumerico_api = 100%                                ║
║  └── Anunciar suporte oficial                                    ║
║                                                                   ║
║  FASE 6: Cleanup (Jul 2026)                                      ║
║  ├── Remover flags                                               ║
║  ├── Remover código legado                                       ║
║  └── Simplificar arquitetura                                     ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""
```

### 3.2 Uso no Código

```python
# cnpj_validator_with_flags.py
"""
Validador de CNPJ usando Feature Flags.
"""

from feature_flags import feature_flag
from feature_flag_decorators import with_feature_flag
from typing import Optional
import logging

logger = logging.getLogger(__name__)


# === Implementações ===

def validate_cnpj_legacy(cnpj: str) -> bool:
    """Validação legada - apenas numérico."""
    digits = ''.join(c for c in cnpj if c.isdigit())
    if len(digits) != 14:
        return False
    # ... lógica de validação DV
    return True


def validate_cnpj_alphanumeric(cnpj: str) -> bool:
    """Nova validação - suporta alfanumérico."""
    chars = ''.join(c for c in cnpj.upper() if c.isalnum())
    if len(chars) != 14:
        return False
    # ... lógica de validação DV com suporte a letras
    return True


# === Função Principal com Feature Flag ===

def validate_cnpj(cnpj: str, user_id: str = None) -> bool:
    """
    Valida CNPJ, usando feature flag para decidir implementação.
    
    Args:
        cnpj: CNPJ a validar
        user_id: ID do usuário (para rollout percentual)
    
    Returns:
        True se válido, False caso contrário
    """
    # Modo shadow: executar ambos e comparar
    if feature_flag("cnpj_migration_shadow", user_id=user_id):
        legacy_result = validate_cnpj_legacy(cnpj)
        new_result = validate_cnpj_alphanumeric(cnpj)
        
        if legacy_result != new_result:
            logger.warning(
                f"DIVERGÊNCIA CNPJ: {cnpj} "
                f"(legado={legacy_result}, novo={new_result})"
            )
        
        # Ainda retorna legado durante shadow mode
        if not feature_flag("cnpj_alfanumerico_validation", user_id=user_id):
            return legacy_result
    
    # Verificar se deve usar nova validação
    if feature_flag("cnpj_alfanumerico_validation", user_id=user_id):
        return validate_cnpj_alphanumeric(cnpj)
    
    return validate_cnpj_legacy(cnpj)


# === Alternativa: Usando Decorator ===

@with_feature_flag(
    "cnpj_alfanumerico_validation",
    fallback=validate_cnpj_legacy
)
def validate_cnpj_decorated(cnpj: str) -> bool:
    """Validação usando decorator de feature flag."""
    return validate_cnpj_alphanumeric(cnpj)


# === API Endpoint ===

def api_validate_cnpj(request_data: dict) -> dict:
    """
    Endpoint de API para validação de CNPJ.
    
    Usa feature flags para:
    1. Decidir se aceita CNPJ alfanumérico
    2. Escolher implementação de validação
    """
    cnpj = request_data.get("cnpj")
    user_id = request_data.get("user_id")
    
    # Verificar se API aceita alfanumérico
    if not feature_flag("cnpj_alfanumerico_api", user_id=user_id):
        # API não aceita alfanumérico ainda
        if any(c.isalpha() for c in cnpj):
            return {
                "valid": False,
                "error": "CNPJ alfanumérico não suportado ainda",
                "code": "ALPHA_NOT_SUPPORTED"
            }
    
    # Validar
    is_valid = validate_cnpj(cnpj, user_id=user_id)
    
    return {
        "cnpj": cnpj,
        "valid": is_valid,
        "validation_method": "alphanumeric" if feature_flag("cnpj_alfanumerico_validation", user_id=user_id) else "numeric"
    }
```

---

## 4. Testando com Feature Flags

### 4.1 Testes Unitários

```python
# test_feature_flags.py
"""
Testes para sistema de feature flags.
"""

import pytest
from unittest.mock import patch
from feature_flags import (
    FeatureFlagService, 
    FeatureFlag, 
    FlagType,
    feature_flag
)


class TestFeatureFlagService:
    """Testes do serviço de feature flags."""
    
    @pytest.fixture
    def service(self):
        """Serviço limpo para cada teste."""
        return FeatureFlagService()
    
    def test_create_flag(self, service):
        """Deve criar flag corretamente."""
        flag = service.create_flag(
            name="test_flag",
            enabled=True,
            percentage=50
        )
        
        assert flag.name == "test_flag"
        assert flag.enabled == True
        assert flag.percentage == 50
    
    def test_flag_disabled_returns_false(self, service):
        """Flag desabilitada deve retornar False."""
        service.create_flag("test_flag", enabled=False)
        
        assert service.is_enabled("test_flag") == False
    
    def test_flag_enabled_100_percent_returns_true(self, service):
        """Flag habilitada com 100% deve retornar True."""
        service.create_flag("test_flag", enabled=True, percentage=100)
        
        assert service.is_enabled("test_flag") == True
    
    def test_allowed_user_always_enabled(self, service):
        """Usuário na lista de permitidos deve sempre ver feature."""
        service.create_flag(
            "test_flag",
            enabled=True,
            percentage=0,  # 0% normal
            allowed_users=["vip_user"]
        )
        
        assert service.is_enabled("test_flag", user_id="vip_user") == True
        assert service.is_enabled("test_flag", user_id="normal_user") == False
    
    def test_allowed_group_always_enabled(self, service):
        """Grupo na lista de permitidos deve sempre ver feature."""
        service.create_flag(
            "test_flag",
            enabled=True,
            percentage=0,
            allowed_groups=["beta_testers"]
        )
        
        assert service.is_enabled("test_flag", groups=["beta_testers"]) == True
        assert service.is_enabled("test_flag", groups=["regular"]) == False
    
    def test_percentage_rollout_consistent(self, service):
        """Rollout percentual deve ser consistente para mesmo usuário."""
        service.create_flag(
            "test_flag",
            enabled=True,
            percentage=50
        )
        
        # Mesmo usuário deve ter mesmo resultado sempre
        results = [
            service.is_enabled("test_flag", user_id="user_123")
            for _ in range(10)
        ]
        
        assert all(r == results[0] for r in results), \
            "Resultado deve ser consistente para mesmo usuário"
    
    def test_percentage_rollout_distribution(self, service):
        """Rollout percentual deve aproximar porcentagem configurada."""
        service.create_flag(
            "test_flag",
            enabled=True,
            percentage=30
        )
        
        # Testar com muitos usuários
        enabled_count = sum(
            1 for i in range(1000)
            if service.is_enabled("test_flag", user_id=f"user_{i}")
        )
        
        # Deve estar perto de 30% (com margem de 10%)
        assert 200 < enabled_count < 400, \
            f"Esperado ~300 habilitados, obteve {enabled_count}"


class TestCNPJFeatureFlags:
    """Testes específicos para flags de CNPJ."""
    
    @pytest.fixture
    def service(self):
        service = FeatureFlagService()
        # Configurar flags de CNPJ
        service.create_flag(
            "cnpj_alfanumerico_validation",
            enabled=True,
            percentage=0,
            allowed_groups=["qa_team"]
        )
        return service
    
    def test_qa_team_sees_new_validation(self, service):
        """Time de QA deve ver nova validação."""
        assert service.is_enabled(
            "cnpj_alfanumerico_validation",
            groups=["qa_team"]
        ) == True
    
    def test_regular_user_sees_legacy(self, service):
        """Usuário regular deve ver validação legada."""
        assert service.is_enabled(
            "cnpj_alfanumerico_validation",
            user_id="user_normal"
        ) == False
    
    def test_gradual_rollout_increase(self, service):
        """Deve aumentar rollout gradualmente."""
        # Começar com 0%
        assert service.is_enabled("cnpj_alfanumerico_validation", user_id="user_1") == False
        
        # Aumentar para 50%
        service.update_flag("cnpj_alfanumerico_validation", percentage=50)
        
        # Alguns usuários devem ver agora
        enabled_count = sum(
            1 for i in range(100)
            if service.is_enabled("cnpj_alfanumerico_validation", user_id=f"user_{i}")
        )
        
        assert 30 < enabled_count < 70, f"Esperado ~50, obteve {enabled_count}"
```

### 4.2 Testes de Integração

```python
# test_cnpj_with_flags.py
"""
Testes de integração do validador CNPJ com feature flags.
"""

import pytest
from unittest.mock import patch, MagicMock

from cnpj_validator_with_flags import (
    validate_cnpj,
    api_validate_cnpj,
    validate_cnpj_legacy,
    validate_cnpj_alphanumeric
)


class TestValidateCNPJWithFlags:
    """Testes do validador com feature flags."""
    
    def test_legacy_when_flag_disabled(self):
        """Deve usar legado quando flag desabilitada."""
        with patch('cnpj_validator_with_flags.feature_flag') as mock_flag:
            mock_flag.return_value = False
            
            # CNPJ numérico válido
            result = validate_cnpj("11222333000181")
            
            # Deve funcionar (legado aceita)
            assert result == True
    
    def test_alphanumeric_when_flag_enabled(self):
        """Deve aceitar alfanumérico quando flag habilitada."""
        with patch('cnpj_validator_with_flags.feature_flag') as mock_flag:
            # Simular: shadow=False, alfanumerico=True
            def flag_side_effect(name, **kwargs):
                return name == "cnpj_alfanumerico_validation"
            
            mock_flag.side_effect = flag_side_effect
            
            with patch('cnpj_validator_with_flags.validate_cnpj_alphanumeric') as mock_alpha:
                mock_alpha.return_value = True
                result = validate_cnpj("AB222333000145")
                
                mock_alpha.assert_called_once()
    
    def test_shadow_mode_logs_divergence(self):
        """Shadow mode deve logar divergências."""
        with patch('cnpj_validator_with_flags.feature_flag') as mock_flag:
            # Shadow habilitado, alfanumérico desabilitado
            def flag_side_effect(name, **kwargs):
                return name == "cnpj_migration_shadow"
            
            mock_flag.side_effect = flag_side_effect
            
            with patch('cnpj_validator_with_flags.logger') as mock_logger:
                # CNPJ que pode ter resultado diferente entre legado e novo
                validate_cnpj("AB222333000145")
                
                # Verificar se houve log de warning para divergência
                # (depende da implementação real)


class TestAPIWithFlags:
    """Testes da API com feature flags."""
    
    def test_api_rejects_alpha_when_flag_disabled(self):
        """API deve rejeitar alfanumérico quando flag desabilitada."""
        with patch('cnpj_validator_with_flags.feature_flag') as mock_flag:
            mock_flag.return_value = False
            
            result = api_validate_cnpj({
                "cnpj": "AB222333000145",
                "user_id": "user_1"
            })
            
            assert result["valid"] == False
            assert result["code"] == "ALPHA_NOT_SUPPORTED"
    
    def test_api_accepts_alpha_when_flag_enabled(self):
        """API deve aceitar alfanumérico quando flag habilitada."""
        with patch('cnpj_validator_with_flags.feature_flag') as mock_flag:
            mock_flag.return_value = True
            
            with patch('cnpj_validator_with_flags.validate_cnpj') as mock_validate:
                mock_validate.return_value = True
                
                result = api_validate_cnpj({
                    "cnpj": "AB222333000145",
                    "user_id": "user_1"
                })
                
                assert result["valid"] == True
```

---

## 5. Boas Práticas

### 5.1 Nomenclatura de Flags

```text
PADRÃO DE NOMENCLATURA:
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  {dominio}_{feature}_{acao}                                    │
│                                                                 │
│  Exemplos:                                                      │
│  ├── cnpj_alfanumerico_validation                              │
│  ├── checkout_new_ui_enabled                                   │
│  ├── payment_pix_instant_enabled                               │
│  └── search_elastic_v2_enabled                                 │
│                                                                 │
│  EVITE:                                                         │
│  ├── flag1, test_flag (não descritivo)                         │
│  ├── nova_feature (muito vago)                                 │
│  └── enableNewValidationForCNPJAlphanumeric (muito longo)      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 5.2 Ciclo de Vida das Flags

```text
CICLO DE VIDA DE FEATURE FLAGS:
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. CRIAÇÃO                                                     │
│     ├── Documentar propósito                                   │
│     ├── Definir owner responsável                              │
│     └── Estimar data de remoção                                │
│                                                                 │
│  2. TESTING                                                     │
│     ├── Testar com flag ON e OFF                               │
│     ├── Validar rollback funciona                              │
│     └── Performance aceitável                                  │
│                                                                 │
│  3. ROLLOUT                                                     │
│     ├── Começar com grupo pequeno                              │
│     ├── Aumentar gradualmente                                  │
│     └── Monitorar métricas                                     │
│                                                                 │
│  4. ESTABILIZAÇÃO                                               │
│     ├── 100% habilitado por 2+ semanas                         │
│     ├── Sem rollbacks necessários                              │
│     └── Métricas estáveis                                      │
│                                                                 │
│  5. REMOÇÃO (⚠️ NÃO ESQUEÇA!)                                   │
│     ├── Criar ticket de cleanup                                │
│     ├── Remover código da flag                                 │
│     ├── Remover código legado                                  │
│     └── Atualizar documentação                                 │
│                                                                 │
│  ⚠️ DÍVIDA TÉCNICA: Flags não removidas acumulam complexidade  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 6. Resumo

### 6.1 Quando Usar Feature Flags

| Situação | Use Feature Flag? |
|----------|------------------|
| Nova feature arriscada | ✅ Sim |
| Migração de sistema | ✅ Sim |
| Experimentos A/B | ✅ Sim |
| Lançamento coordenado | ✅ Sim |
| Refatoração simples | ❌ Não, overhead |
| Bug fix urgente | ❌ Não, deploy direto |

### 6.2 Checklist

```text
☐ Flag tem nome descritivo
☐ Propósito documentado
☐ Owner definido
☐ Data de remoção estimada
☐ Testes cobrem ON e OFF
☐ Rollback testado
☐ Métricas de monitoramento
☐ Ticket de cleanup criado
```

---

**Próximo**: [05-testes-de-regressao.md](05-testes-de-regressao.md)
