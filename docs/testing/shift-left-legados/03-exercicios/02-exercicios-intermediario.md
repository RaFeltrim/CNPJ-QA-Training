# 🟡 Exercícios Nível Intermediário - Suporte 50%

## Objetivo

Exercícios com orientação parcial. Você recebe o contexto e os requisitos,
mas precisa implementar parte da solução sozinho. Dicas são fornecidas
quando necessário.

---

## Exercício 1: Golden Master para API

### Contexto

Você está migrando uma API de consulta de dados. Precisa criar um Golden Master
que capture as respostas da API atual para comparar após a migração.

### Código Legado

```python
# legacy/data_api.py
class DataAPI:
    """API legada de consulta de dados."""
    
    def __init__(self):
        self._data = {
            "usuarios": [
                {"id": 1, "nome": "João", "ativo": True},
                {"id": 2, "nome": "Maria", "ativo": True},
                {"id": 3, "nome": "Pedro", "ativo": False},
            ],
            "produtos": [
                {"id": 101, "nome": "Widget", "preco": 99.90},
                {"id": 102, "nome": "Gadget", "preco": 149.90},
            ]
        }
    
    def buscar(self, tipo, filtro=None):
        """
        Busca dados por tipo.
        
        Args:
            tipo: 'usuarios' ou 'produtos'
            filtro: dict com campos para filtrar
        """
        dados = self._data.get(tipo, [])
        
        if filtro:
            resultado = []
            for item in dados:
                match = True
                for k, v in filtro.items():
                    if item.get(k) != v:
                        match = False
                        break
                if match:
                    resultado.append(item)
            return resultado
        
        return dados
    
    def contar(self, tipo, filtro=None):
        """Conta registros."""
        return len(self.buscar(tipo, filtro))
    
    def existe(self, tipo, id):
        """Verifica se registro existe."""
        dados = self.buscar(tipo, {"id": id})
        return len(dados) > 0
```

### Requisitos

1. Criar classe `GoldenMasterAPI` que capture respostas
2. Gerar casos de teste para todas as operações (buscar, contar, existe)
3. Salvar Golden Master em JSON
4. Implementar comparação com relatório de diferenças

### Template Inicial

```python
# test_golden_master_api.py
"""
Golden Master para DataAPI.

TODO: Complete a implementação.
"""

import json
import pytest
from pathlib import Path
from legacy.data_api import DataAPI


class GoldenMasterAPI:
    """Classe para gerenciar Golden Master de API."""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.arquivo = Path(f"golden_masters/{nome}.json")
        self.arquivo.parent.mkdir(exist_ok=True)
    
    def gerar_casos_teste(self) -> dict:
        """
        Gera todos os casos de teste possíveis.
        
        TODO: Implementar geração de casos para:
        - buscar('usuarios')
        - buscar('usuarios', {'ativo': True})
        - buscar('usuarios', {'ativo': False})
        - buscar('produtos')
        - buscar('produtos', {'id': 101})
        - buscar('tipo_invalido')
        - contar('usuarios')
        - contar('usuarios', {'ativo': True})
        - contar('produtos')
        - existe('usuarios', 1)
        - existe('usuarios', 999)
        - existe('produtos', 101)
        
        Returns:
            Dict com chave=descrição_caso, valor=resultado
        """
        api = DataAPI()
        casos = {}
        
        # TODO: Implementar geração de casos
        # Dica: Use um padrão de chave como "operacao|args"
        
        return casos
    
    def capturar(self):
        """
        Captura Golden Master atual.
        
        TODO: Implementar salvamento em JSON
        """
        pass
    
    def comparar(self, casos_atuais: dict) -> dict:
        """
        Compara casos atuais com Golden Master.
        
        TODO: Implementar comparação com relatório
        
        Returns:
            Dict com: passed, total, differences
        """
        pass


# === Testes ===

class TestGoldenMasterAPI:
    """Testes usando Golden Master."""
    
    @pytest.fixture
    def golden_master(self):
        return GoldenMasterAPI("data_api")
    
    @pytest.mark.capture
    def test_capturar_golden_master(self, golden_master):
        """Captura novo Golden Master."""
        # TODO: Implementar captura
        pass
    
    def test_comparar_com_golden_master(self, golden_master):
        """Compara com Golden Master existente."""
        # TODO: Implementar comparação
        pass
```

### Dicas

<details>
<summary>💡 Dica 1: Estrutura de casos</summary>

Use um dicionário com chaves descritivas:

```python
casos = {
    "buscar|usuarios|sem_filtro": api.buscar("usuarios"),
    "buscar|usuarios|ativo_true": api.buscar("usuarios", {"ativo": True}),
    # ...
}
```

</details>

<details>
<summary>💡 Dica 2: Serialização JSON</summary>

Lembre que JSON não aceita todos os tipos Python:

```python
import json

# Para salvar
with open(self.arquivo, 'w') as f:
    json.dump(casos, f, indent=2, default=str)

# Para carregar
with open(self.arquivo, 'r') as f:
    return json.load(f)
```

</details>

<details>
<summary>💡 Dica 3: Comparação detalhada</summary>

Use `deepdiff` para comparações complexas:

```python
from deepdiff import DeepDiff

diff = DeepDiff(esperado, atual, ignore_order=True)
if diff:
    print(f"Diferenças: {diff}")
```

Ou compare manualmente item a item.

</details>

---

## Exercício 2: Strangler Facade com Rollout Percentual

### Contexto

Você precisa migrar um serviço de cálculo de frete. A nova implementação
tem algumas diferenças e você quer fazer rollout gradual.

### Implementações

```python
# Serviço legado
def calcular_frete_legado(cep_origem, cep_destino, peso):
    """
    Cálculo legado - usa tabela simples.
    
    - Mesmo estado: R$ 10 + peso * 0.5
    - Estados vizinhos: R$ 20 + peso * 1.0
    - Outros: R$ 30 + peso * 1.5
    """
    if not all([cep_origem, cep_destino, peso]):
        return None
    
    # Simular lógica de estados pelo CEP
    estado_origem = cep_origem[:2]
    estado_destino = cep_destino[:2]
    
    if estado_origem == estado_destino:
        return round(10 + peso * 0.5, 2)
    elif abs(int(estado_origem) - int(estado_destino)) <= 10:
        return round(20 + peso * 1.0, 2)
    else:
        return round(30 + peso * 1.5, 2)


# Serviço novo
def calcular_frete_novo(cep_origem, cep_destino, peso, tipo='normal'):
    """
    Cálculo novo - mais opções e precisão.
    
    - Mesmo estado: R$ 12 + peso * 0.45
    - Estados vizinhos: R$ 22 + peso * 0.95
    - Outros: R$ 32 + peso * 1.45
    - Tipo 'expresso': +50%
    """
    if not all([cep_origem, cep_destino, peso]):
        return {"valor": None, "erro": "Parâmetros inválidos"}
    
    estado_origem = cep_origem[:2]
    estado_destino = cep_destino[:2]
    
    if estado_origem == estado_destino:
        valor = 12 + peso * 0.45
    elif abs(int(estado_origem) - int(estado_destino)) <= 10:
        valor = 22 + peso * 0.95
    else:
        valor = 32 + peso * 1.45
    
    if tipo == 'expresso':
        valor *= 1.5
    
    return {
        "valor": round(valor, 2),
        "tipo": tipo,
        "prazo_dias": 3 if tipo == 'expresso' else 7
    }
```

### Requisitos

1. Criar facade com suporte a rollout percentual
2. Normalizar resposta do novo para formato do legado (compatibilidade)
3. Implementar logging de divergências
4. Criar testes para diferentes cenários de rollout

### Template Inicial

```python
# frete_facade.py
"""
Strangler Facade para serviço de frete.

TODO: Complete a implementação.
"""

import hashlib
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class FreteFacade:
    """
    Facade para migração do serviço de frete.
    
    Suporta:
    - Rollout por porcentagem
    - Modo shadow (compara ambos)
    - Normalização de resposta
    """
    
    def __init__(self, percentual_novo: int = 0):
        """
        Args:
            percentual_novo: 0-100, porcentagem de requests para nova implementação
        """
        self.percentual_novo = percentual_novo
        self._divergencias = []
    
    def _calcular_legado(self, cep_origem, cep_destino, peso) -> Optional[float]:
        """Chama implementação legada."""
        # TODO: Implementar chamada ao serviço legado
        pass
    
    def _calcular_novo(self, cep_origem, cep_destino, peso, **kwargs) -> Dict:
        """Chama nova implementação."""
        # TODO: Implementar chamada ao serviço novo
        pass
    
    def _normalizar_resposta_novo(self, resposta_novo: Dict) -> Optional[float]:
        """
        Normaliza resposta do novo para formato do legado.
        
        TODO: Extrair apenas o valor para manter compatibilidade
        """
        pass
    
    def _deve_usar_novo(self, user_id: str = None) -> bool:
        """
        Decide se deve usar nova implementação.
        
        TODO: Implementar lógica de rollout percentual
        Dica: Use hash do user_id para consistência
        """
        pass
    
    def calcular(
        self, 
        cep_origem: str, 
        cep_destino: str, 
        peso: float,
        user_id: str = None,
        **kwargs
    ) -> Optional[float]:
        """
        Calcula frete usando a implementação apropriada.
        
        TODO: Implementar roteamento baseado em percentual
        """
        pass
    
    def calcular_shadow(
        self,
        cep_origem: str,
        cep_destino: str,
        peso: float
    ) -> Dict[str, Any]:
        """
        Executa ambas implementações e compara.
        
        TODO: Implementar modo shadow
        
        Returns:
            Dict com resultados de ambas e flag de divergência
        """
        pass
    
    def get_divergencias(self):
        """Retorna lista de divergências encontradas."""
        return self._divergencias


# === Testes ===

class TestFreteFacade:
    """Testes do facade de frete."""
    
    @pytest.fixture
    def facade_legado(self):
        """Facade 100% legado."""
        return FreteFacade(percentual_novo=0)
    
    @pytest.fixture
    def facade_novo(self):
        """Facade 100% novo."""
        return FreteFacade(percentual_novo=100)
    
    @pytest.fixture
    def facade_misto(self):
        """Facade 50% cada."""
        return FreteFacade(percentual_novo=50)
    
    def test_0_porcento_sempre_usa_legado(self, facade_legado):
        """
        Com 0%, deve sempre usar legado.
        
        TODO: Implementar teste
        """
        pass
    
    def test_100_porcento_sempre_usa_novo(self, facade_novo):
        """
        Com 100%, deve sempre usar novo.
        
        TODO: Implementar teste
        """
        pass
    
    def test_50_porcento_distribui(self, facade_misto):
        """
        Com 50%, deve distribuir aproximadamente igual.
        
        TODO: Implementar teste
        Dica: Testar com 100 user_ids diferentes
        """
        pass
    
    def test_shadow_mode_detecta_divergencia(self, facade_legado):
        """
        Shadow mode deve detectar quando resultados diferem.
        
        TODO: Implementar teste
        """
        pass
```

### Dicas

<details>
<summary>💡 Dica 1: Hash consistente</summary>

Para rollout consistente por usuário:

```python
def _deve_usar_novo(self, user_id: str = None) -> bool:
    if not user_id:
        return False
    
    # Hash gera número consistente para mesmo user
    hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    bucket = hash_val % 100
    
    return bucket < self.percentual_novo
```

</details>

<details>
<summary>💡 Dica 2: Normalização de resposta</summary>

Para manter compatibilidade:

```python
def _normalizar_resposta_novo(self, resposta_novo: Dict) -> Optional[float]:
    if resposta_novo and "valor" in resposta_novo:
        return resposta_novo["valor"]
    return None
```

</details>

---

## Exercício 3: Feature Flags com Contexto

### Contexto

Você precisa implementar feature flags que consideram múltiplos contextos:
usuário, grupo, ambiente, data, etc.

### Requisitos

1. Criar sistema de feature flags com regras compostas
2. Suportar: usuários específicos, grupos, porcentagem, datas
3. Implementar logging de avaliações
4. Criar testes para cada tipo de regra

### Template Inicial

```python
# feature_flags_advanced.py
"""
Sistema avançado de Feature Flags.

TODO: Complete a implementação.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum


class RuleType(Enum):
    """Tipos de regras."""
    USER_LIST = "user_list"        # Usuários específicos
    GROUP_LIST = "group_list"      # Grupos específicos
    PERCENTAGE = "percentage"       # Porcentagem de usuários
    DATE_RANGE = "date_range"       # Range de datas
    ENVIRONMENT = "environment"     # Ambiente (dev, staging, prod)


@dataclass
class Rule:
    """Uma regra de avaliação."""
    type: RuleType
    config: Dict[str, Any]


@dataclass
class FeatureFlag:
    """Feature flag com múltiplas regras."""
    name: str
    enabled: bool = True
    rules: List[Rule] = field(default_factory=list)
    default: bool = False


class FeatureFlagEvaluator:
    """
    Avaliador de feature flags com regras compostas.
    
    As regras são avaliadas em ordem:
    1. Se flag desabilitada globalmente -> False
    2. Se alguma regra permitir -> True
    3. Se nenhuma regra aplicar -> default
    """
    
    def __init__(self):
        self._flags: Dict[str, FeatureFlag] = {}
        self._evaluations: List[Dict] = []
    
    def register(self, flag: FeatureFlag):
        """Registra uma feature flag."""
        self._flags[flag.name] = flag
    
    def evaluate(
        self,
        flag_name: str,
        context: Dict[str, Any]
    ) -> bool:
        """
        Avalia feature flag dado um contexto.
        
        Args:
            flag_name: Nome da flag
            context: Dict com user_id, groups, environment, etc
        
        TODO: Implementar avaliação de todas as regras
        """
        pass
    
    def _evaluate_rule(self, rule: Rule, context: Dict) -> Optional[bool]:
        """
        Avalia uma regra específica.
        
        TODO: Implementar avaliação de cada tipo de regra
        
        Returns:
            True se regra permite
            False se regra nega
            None se regra não se aplica
        """
        pass
    
    def _evaluate_user_list(self, config: Dict, context: Dict) -> Optional[bool]:
        """
        Regra USER_LIST: verifica se usuário está na lista.
        
        config: {"users": ["user1", "user2"]}
        context: {"user_id": "user1"}
        
        TODO: Implementar
        """
        pass
    
    def _evaluate_group_list(self, config: Dict, context: Dict) -> Optional[bool]:
        """
        Regra GROUP_LIST: verifica se algum grupo está na lista.
        
        config: {"groups": ["beta", "admin"]}
        context: {"groups": ["beta", "users"]}
        
        TODO: Implementar
        """
        pass
    
    def _evaluate_percentage(self, config: Dict, context: Dict) -> Optional[bool]:
        """
        Regra PERCENTAGE: verifica se usuário está no bucket.
        
        config: {"percentage": 30}
        context: {"user_id": "user123"}
        
        TODO: Implementar
        """
        pass
    
    def _evaluate_date_range(self, config: Dict, context: Dict) -> Optional[bool]:
        """
        Regra DATE_RANGE: verifica se está dentro do período.
        
        config: {"start": "2025-01-01", "end": "2025-12-31"}
        context: {} (usa data atual)
        
        TODO: Implementar
        """
        pass
    
    def _evaluate_environment(self, config: Dict, context: Dict) -> Optional[bool]:
        """
        Regra ENVIRONMENT: verifica se ambiente está na lista.
        
        config: {"environments": ["dev", "staging"]}
        context: {"environment": "dev"}
        
        TODO: Implementar
        """
        pass
    
    def get_evaluation_log(self) -> List[Dict]:
        """Retorna log de avaliações."""
        return self._evaluations


# === Testes ===

class TestFeatureFlagEvaluator:
    """Testes do avaliador de feature flags."""
    
    @pytest.fixture
    def evaluator(self):
        return FeatureFlagEvaluator()
    
    def test_flag_desabilitada_retorna_false(self, evaluator):
        """Flag desabilitada deve sempre retornar False."""
        flag = FeatureFlag(name="test", enabled=False)
        evaluator.register(flag)
        
        result = evaluator.evaluate("test", {"user_id": "any"})
        assert result == False
    
    def test_user_list_permite_usuario(self, evaluator):
        """
        Usuário na lista deve ser permitido.
        
        TODO: Implementar
        """
        pass
    
    def test_group_list_permite_grupo(self, evaluator):
        """
        Grupo na lista deve ser permitido.
        
        TODO: Implementar
        """
        pass
    
    def test_percentage_distribuicao(self, evaluator):
        """
        Porcentagem deve aproximar valor configurado.
        
        TODO: Implementar
        """
        pass
    
    def test_date_range_dentro(self, evaluator):
        """
        Data dentro do range deve ser permitida.
        
        TODO: Implementar
        """
        pass
    
    def test_regras_compostas(self, evaluator):
        """
        Múltiplas regras devem funcionar juntas.
        
        Cenário: Permitir se (usuário beta) OU (grupo admin) OU (10% usuários)
        
        TODO: Implementar
        """
        pass
```

### Dicas

<details>
<summary>💡 Dica 1: Estrutura de avaliação</summary>

```python
def evaluate(self, flag_name: str, context: Dict) -> bool:
    flag = self._flags.get(flag_name)
    
    if not flag:
        return False
    
    if not flag.enabled:
        return False
    
    # Avaliar cada regra
    for rule in flag.rules:
        result = self._evaluate_rule(rule, context)
        if result is True:
            return True
    
    return flag.default
```

</details>

<details>
<summary>💡 Dica 2: Date range com datetime</summary>

```python
def _evaluate_date_range(self, config: Dict, context: Dict) -> Optional[bool]:
    start = datetime.fromisoformat(config.get("start", "1970-01-01"))
    end = datetime.fromisoformat(config.get("end", "2099-12-31"))
    now = datetime.now()
    
    if start <= now <= end:
        return True
    return None  # Não se aplica fora do range
```

</details>

---

## Checklist de Conclusão

- [ ] Implementei Golden Master para API com casos completos
- [ ] Criei Strangler Facade com rollout percentual
- [ ] Implementei Feature Flags com regras compostas
- [ ] Todos os testes passam
- [ ] Código está documentado

**Próximo**: [03-exercicios-avancado.md](03-exercicios-avancado.md)
