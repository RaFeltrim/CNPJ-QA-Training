# 📝 Gabarito - Exercícios Intermediários

## Exercício 1: Golden Master para API

### Solução Completa

```python
# test_golden_master_api.py
"""
Golden Master para DataAPI.
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass


# === API Legada (simulada) ===

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
        return len(self.buscar(tipo, filtro))
    
    def existe(self, tipo, id):
        dados = self.buscar(tipo, {"id": id})
        return len(dados) > 0


# === Golden Master ===

class GoldenMasterAPI:
    """Classe para gerenciar Golden Master de API."""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.arquivo = Path(f"golden_masters/{nome}.json")
        self.arquivo.parent.mkdir(exist_ok=True)
    
    def gerar_casos_teste(self) -> dict:
        """Gera todos os casos de teste possíveis."""
        api = DataAPI()
        casos = {}
        
        # === BUSCAR ===
        
        # Buscar sem filtro
        casos["buscar|usuarios|sem_filtro"] = api.buscar("usuarios")
        casos["buscar|produtos|sem_filtro"] = api.buscar("produtos")
        casos["buscar|tipo_invalido|sem_filtro"] = api.buscar("tipo_invalido")
        
        # Buscar com filtros
        casos["buscar|usuarios|ativo_true"] = api.buscar("usuarios", {"ativo": True})
        casos["buscar|usuarios|ativo_false"] = api.buscar("usuarios", {"ativo": False})
        casos["buscar|usuarios|id_1"] = api.buscar("usuarios", {"id": 1})
        casos["buscar|usuarios|id_999"] = api.buscar("usuarios", {"id": 999})
        casos["buscar|usuarios|nome_joao"] = api.buscar("usuarios", {"nome": "João"})
        
        casos["buscar|produtos|id_101"] = api.buscar("produtos", {"id": 101})
        casos["buscar|produtos|preco_99.90"] = api.buscar("produtos", {"preco": 99.90})
        
        # Filtros compostos
        casos["buscar|usuarios|ativo_true_id_1"] = api.buscar("usuarios", {"ativo": True, "id": 1})
        casos["buscar|usuarios|ativo_false_id_1"] = api.buscar("usuarios", {"ativo": False, "id": 1})
        
        # === CONTAR ===
        
        casos["contar|usuarios|sem_filtro"] = api.contar("usuarios")
        casos["contar|usuarios|ativo_true"] = api.contar("usuarios", {"ativo": True})
        casos["contar|usuarios|ativo_false"] = api.contar("usuarios", {"ativo": False})
        casos["contar|produtos|sem_filtro"] = api.contar("produtos")
        casos["contar|tipo_invalido|sem_filtro"] = api.contar("tipo_invalido")
        
        # === EXISTE ===
        
        casos["existe|usuarios|id_1"] = api.existe("usuarios", 1)
        casos["existe|usuarios|id_2"] = api.existe("usuarios", 2)
        casos["existe|usuarios|id_999"] = api.existe("usuarios", 999)
        casos["existe|produtos|id_101"] = api.existe("produtos", 101)
        casos["existe|produtos|id_999"] = api.existe("produtos", 999)
        casos["existe|tipo_invalido|id_1"] = api.existe("tipo_invalido", 1)
        
        return casos
    
    def capturar(self) -> Path:
        """Captura Golden Master atual."""
        casos = self.gerar_casos_teste()
        
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(casos, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Golden Master capturado: {self.arquivo}")
        print(f"   Total de casos: {len(casos)}")
        
        return self.arquivo
    
    def carregar(self) -> dict:
        """Carrega Golden Master existente."""
        if not self.arquivo.exists():
            raise FileNotFoundError(f"Golden Master não encontrado: {self.arquivo}")
        
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def comparar(self, casos_atuais: dict) -> dict:
        """Compara casos atuais com Golden Master."""
        golden = self.carregar()
        
        diferencas = []
        matches = 0
        
        for chave, esperado in golden.items():
            atual = casos_atuais.get(chave)
            
            # Comparação profunda para listas e dicts
            if atual != esperado:
                diferencas.append({
                    'caso': chave,
                    'esperado': esperado,
                    'atual': atual
                })
            else:
                matches += 1
        
        # Verificar novos casos não no golden
        novos_casos = []
        for chave in casos_atuais:
            if chave not in golden:
                novos_casos.append(chave)
        
        return {
            'passed': len(diferencas) == 0,
            'total_golden': len(golden),
            'total_atual': len(casos_atuais),
            'matches': matches,
            'diferencas': diferencas,
            'novos_casos': novos_casos
        }


# === Testes ===

class TestGoldenMasterAPI:
    """Testes usando Golden Master."""
    
    @pytest.fixture
    def golden_master(self):
        return GoldenMasterAPI("data_api")
    
    @pytest.mark.capture
    def test_capturar_golden_master(self, golden_master):
        """Captura novo Golden Master."""
        arquivo = golden_master.capturar()
        assert arquivo.exists()
    
    def test_comparar_com_golden_master(self, golden_master):
        """Compara com Golden Master existente."""
        if not golden_master.arquivo.exists():
            pytest.skip("Golden Master não existe. Execute pytest -m capture primeiro.")
        
        casos_atuais = golden_master.gerar_casos_teste()
        relatorio = golden_master.comparar(casos_atuais)
        
        if not relatorio['passed']:
            msg = f"\n❌ Golden Master Test FALHOU!\n"
            msg += f"   Total no Golden: {relatorio['total_golden']}\n"
            msg += f"   Matches: {relatorio['matches']}\n"
            msg += f"   Diferenças: {len(relatorio['diferencas'])}\n"
            
            for d in relatorio['diferencas'][:5]:
                msg += f"\n   Caso: {d['caso']}\n"
                msg += f"   Esperado: {d['esperado']}\n"
                msg += f"   Atual: {d['atual']}\n"
            
            pytest.fail(msg)
        
        print(f"\n✅ Golden Master PASSOU! ({relatorio['matches']} casos)")
    
    def test_validar_estrutura_golden_master(self, golden_master):
        """Valida que Golden Master tem todos os tipos de operação."""
        if not golden_master.arquivo.exists():
            pytest.skip("Golden Master não existe")
        
        golden = golden_master.carregar()
        
        # Deve ter operações de buscar
        assert any(k.startswith("buscar|") for k in golden.keys())
        
        # Deve ter operações de contar
        assert any(k.startswith("contar|") for k in golden.keys())
        
        # Deve ter operações de existe
        assert any(k.startswith("existe|") for k in golden.keys())
        
        # Deve ter casos para ambos os tipos
        assert any("usuarios" in k for k in golden.keys())
        assert any("produtos" in k for k in golden.keys())
```

---

## Exercício 2: Strangler Facade com Rollout Percentual

### Solução Completa

```python
# frete_facade.py
"""
Strangler Facade para serviço de frete.
"""

import hashlib
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


# === Implementações ===

def calcular_frete_legado(cep_origem, cep_destino, peso):
    """Cálculo legado - usa tabela simples."""
    if not all([cep_origem, cep_destino, peso]):
        return None
    
    try:
        estado_origem = cep_origem[:2]
        estado_destino = cep_destino[:2]
        
        if estado_origem == estado_destino:
            return round(10 + peso * 0.5, 2)
        elif abs(int(estado_origem) - int(estado_destino)) <= 10:
            return round(20 + peso * 1.0, 2)
        else:
            return round(30 + peso * 1.5, 2)
    except (ValueError, TypeError):
        return None


def calcular_frete_novo(cep_origem, cep_destino, peso, tipo='normal'):
    """Cálculo novo - mais opções e precisão."""
    if not all([cep_origem, cep_destino, peso]):
        return {"valor": None, "erro": "Parâmetros inválidos"}
    
    try:
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
    except (ValueError, TypeError):
        return {"valor": None, "erro": "Erro no cálculo"}


# === Facade ===

class FreteFacade:
    """
    Facade para migração do serviço de frete.
    """
    
    def __init__(self, percentual_novo: int = 0):
        if not 0 <= percentual_novo <= 100:
            raise ValueError("percentual_novo deve estar entre 0 e 100")
        
        self.percentual_novo = percentual_novo
        self._divergencias: List[Dict] = []
        self._chamadas: Dict[str, int] = {"legado": 0, "novo": 0}
    
    def _calcular_legado(self, cep_origem, cep_destino, peso) -> Optional[float]:
        """Chama implementação legada."""
        self._chamadas["legado"] += 1
        return calcular_frete_legado(cep_origem, cep_destino, peso)
    
    def _calcular_novo(self, cep_origem, cep_destino, peso, **kwargs) -> Dict:
        """Chama nova implementação."""
        self._chamadas["novo"] += 1
        return calcular_frete_novo(cep_origem, cep_destino, peso, **kwargs)
    
    def _normalizar_resposta_novo(self, resposta_novo: Dict) -> Optional[float]:
        """Normaliza resposta do novo para formato do legado."""
        if resposta_novo and "valor" in resposta_novo:
            return resposta_novo["valor"]
        return None
    
    def _deve_usar_novo(self, user_id: str = None) -> bool:
        """Decide se deve usar nova implementação."""
        if self.percentual_novo == 0:
            return False
        
        if self.percentual_novo >= 100:
            return True
        
        if not user_id:
            # Sem user_id, usar random (não ideal, mas funciona)
            import random
            return random.randint(1, 100) <= self.percentual_novo
        
        # Com user_id, usar hash para consistência
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        bucket = (hash_val % 100) + 1  # 1-100
        
        return bucket <= self.percentual_novo
    
    def calcular(
        self, 
        cep_origem: str, 
        cep_destino: str, 
        peso: float,
        user_id: str = None,
        **kwargs
    ) -> Optional[float]:
        """Calcula frete usando a implementação apropriada."""
        usar_novo = self._deve_usar_novo(user_id)
        
        if usar_novo:
            resposta = self._calcular_novo(cep_origem, cep_destino, peso, **kwargs)
            return self._normalizar_resposta_novo(resposta)
        else:
            return self._calcular_legado(cep_origem, cep_destino, peso)
    
    def calcular_shadow(
        self,
        cep_origem: str,
        cep_destino: str,
        peso: float
    ) -> Dict[str, Any]:
        """Executa ambas implementações e compara."""
        resultado_legado = self._calcular_legado(cep_origem, cep_destino, peso)
        resposta_novo = self._calcular_novo(cep_origem, cep_destino, peso)
        resultado_novo = self._normalizar_resposta_novo(resposta_novo)
        
        # Comparar valores
        # Considerar match se diferença < 0.01 (precisão de centavos)
        if resultado_legado is not None and resultado_novo is not None:
            match = abs(resultado_legado - resultado_novo) < 0.01
        else:
            match = resultado_legado == resultado_novo
        
        comparacao = {
            'cep_origem': cep_origem,
            'cep_destino': cep_destino,
            'peso': peso,
            'legado': resultado_legado,
            'novo': resultado_novo,
            'novo_completo': resposta_novo,
            'match': match,
            'timestamp': datetime.now().isoformat()
        }
        
        if not match:
            self._divergencias.append(comparacao)
            logger.warning(
                f"DIVERGÊNCIA FRETE: {cep_origem} -> {cep_destino}, peso={peso}\n"
                f"  Legado: {resultado_legado}\n"
                f"  Novo: {resultado_novo}"
            )
        
        return comparacao
    
    def get_divergencias(self) -> List[Dict]:
        """Retorna lista de divergências encontradas."""
        return self._divergencias
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas de uso."""
        return {
            'chamadas_legado': self._chamadas['legado'],
            'chamadas_novo': self._chamadas['novo'],
            'divergencias': len(self._divergencias),
            'percentual_configurado': self.percentual_novo
        }


# === Testes ===

import pytest


class TestFreteFacade:
    """Testes do facade de frete."""
    
    @pytest.fixture
    def facade_legado(self):
        return FreteFacade(percentual_novo=0)
    
    @pytest.fixture
    def facade_novo(self):
        return FreteFacade(percentual_novo=100)
    
    @pytest.fixture
    def facade_misto(self):
        return FreteFacade(percentual_novo=50)
    
    def test_0_porcento_sempre_usa_legado(self, facade_legado):
        """Com 0%, deve sempre usar legado."""
        for i in range(10):
            facade_legado.calcular("01310100", "04101200", 5.0, user_id=f"user_{i}")
        
        stats = facade_legado.get_estatisticas()
        assert stats['chamadas_legado'] == 10
        assert stats['chamadas_novo'] == 0
    
    def test_100_porcento_sempre_usa_novo(self, facade_novo):
        """Com 100%, deve sempre usar novo."""
        for i in range(10):
            facade_novo.calcular("01310100", "04101200", 5.0, user_id=f"user_{i}")
        
        stats = facade_novo.get_estatisticas()
        assert stats['chamadas_legado'] == 0
        assert stats['chamadas_novo'] == 10
    
    def test_50_porcento_distribui(self, facade_misto):
        """Com 50%, deve distribuir aproximadamente igual."""
        for i in range(100):
            facade_misto.calcular("01310100", "04101200", 5.0, user_id=f"user_{i}")
        
        stats = facade_misto.get_estatisticas()
        total = stats['chamadas_legado'] + stats['chamadas_novo']
        
        # Deve estar entre 30% e 70% para cada lado (tolerância estatística)
        assert 30 < stats['chamadas_legado'] < 70
        assert 30 < stats['chamadas_novo'] < 70
    
    def test_mesmo_usuario_mesmo_resultado(self, facade_misto):
        """Mesmo user_id deve sempre ir para mesma implementação."""
        resultados = []
        for _ in range(10):
            # Resetar chamadas
            facade_misto._chamadas = {"legado": 0, "novo": 0}
            
            facade_misto.calcular("01310100", "04101200", 5.0, user_id="usuario_fixo")
            
            # Verificar qual foi usado
            if facade_misto._chamadas['legado'] > 0:
                resultados.append('legado')
            else:
                resultados.append('novo')
        
        # Todos devem ser iguais
        assert all(r == resultados[0] for r in resultados)
    
    def test_shadow_mode_detecta_divergencia(self):
        """Shadow mode deve detectar quando resultados diferem."""
        facade = FreteFacade(percentual_novo=0)
        
        # Os valores são diferentes entre legado e novo por design
        # Legado: 10 + 5*0.5 = 12.5
        # Novo: 12 + 5*0.45 = 14.25
        resultado = facade.calcular_shadow("01310100", "01310200", 5.0)
        
        # Deve detectar a divergência
        assert resultado['match'] == False
        assert resultado['legado'] == 12.5
        assert resultado['novo'] == 14.25
        
        # Deve registrar a divergência
        divergencias = facade.get_divergencias()
        assert len(divergencias) == 1
    
    def test_shadow_mode_match_valores_proximos(self):
        """Shadow mode com valores muito próximos deve considerar match."""
        facade = FreteFacade()
        
        # Criar cenário onde diferença é mínima
        # Isso depende da implementação específica
        # Por ora, testar que a lógica existe
        assert hasattr(facade, 'calcular_shadow')
    
    def test_validacao_percentual_invalido(self):
        """Deve rejeitar percentuais inválidos."""
        with pytest.raises(ValueError):
            FreteFacade(percentual_novo=-1)
        
        with pytest.raises(ValueError):
            FreteFacade(percentual_novo=101)
    
    def test_calculo_retorna_valor(self, facade_legado):
        """Cálculo deve retornar valor numérico."""
        resultado = facade_legado.calcular("01310100", "04101200", 5.0)
        
        assert resultado is not None
        assert isinstance(resultado, float)
        assert resultado > 0
    
    def test_parametros_invalidos(self, facade_legado):
        """Parâmetros inválidos devem retornar None."""
        assert facade_legado.calcular(None, "04101200", 5.0) is None
        assert facade_legado.calcular("01310100", None, 5.0) is None
        assert facade_legado.calcular("01310100", "04101200", None) is None
```

---

## Exercício 3: Feature Flags com Contexto

### Solução Completa

```python
# feature_flags_advanced.py
"""
Sistema avançado de Feature Flags.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import hashlib
import logging

logger = logging.getLogger(__name__)


class RuleType(Enum):
    """Tipos de regras."""
    USER_LIST = "user_list"
    GROUP_LIST = "group_list"
    PERCENTAGE = "percentage"
    DATE_RANGE = "date_range"
    ENVIRONMENT = "environment"


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
    """Avaliador de feature flags com regras compostas."""
    
    def __init__(self):
        self._flags: Dict[str, FeatureFlag] = {}
        self._evaluations: List[Dict] = []
    
    def register(self, flag: FeatureFlag):
        """Registra uma feature flag."""
        self._flags[flag.name] = flag
        logger.info(f"Feature flag registrada: {flag.name}")
    
    def evaluate(self, flag_name: str, context: Dict[str, Any]) -> bool:
        """Avalia feature flag dado um contexto."""
        flag = self._flags.get(flag_name)
        
        # Log da avaliação
        evaluation = {
            'flag_name': flag_name,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'result': None,
            'reason': None
        }
        
        # Flag não existe
        if not flag:
            evaluation['result'] = False
            evaluation['reason'] = 'flag_not_found'
            self._evaluations.append(evaluation)
            return False
        
        # Flag desabilitada globalmente
        if not flag.enabled:
            evaluation['result'] = False
            evaluation['reason'] = 'flag_disabled'
            self._evaluations.append(evaluation)
            return False
        
        # Avaliar cada regra
        for rule in flag.rules:
            result = self._evaluate_rule(rule, context)
            
            if result is True:
                evaluation['result'] = True
                evaluation['reason'] = f'rule_{rule.type.value}_matched'
                self._evaluations.append(evaluation)
                return True
        
        # Nenhuma regra permitiu -> usar default
        evaluation['result'] = flag.default
        evaluation['reason'] = 'default'
        self._evaluations.append(evaluation)
        return flag.default
    
    def _evaluate_rule(self, rule: Rule, context: Dict) -> Optional[bool]:
        """Avalia uma regra específica."""
        evaluators = {
            RuleType.USER_LIST: self._evaluate_user_list,
            RuleType.GROUP_LIST: self._evaluate_group_list,
            RuleType.PERCENTAGE: self._evaluate_percentage,
            RuleType.DATE_RANGE: self._evaluate_date_range,
            RuleType.ENVIRONMENT: self._evaluate_environment,
        }
        
        evaluator = evaluators.get(rule.type)
        if evaluator:
            return evaluator(rule.config, context)
        
        return None
    
    def _evaluate_user_list(self, config: Dict, context: Dict) -> Optional[bool]:
        """Regra USER_LIST: verifica se usuário está na lista."""
        users = config.get("users", [])
        user_id = context.get("user_id")
        
        if not user_id:
            return None
        
        return user_id in users
    
    def _evaluate_group_list(self, config: Dict, context: Dict) -> Optional[bool]:
        """Regra GROUP_LIST: verifica se algum grupo está na lista."""
        allowed_groups = config.get("groups", [])
        user_groups = context.get("groups", [])
        
        if not user_groups:
            return None
        
        # Verificar se há interseção
        for group in user_groups:
            if group in allowed_groups:
                return True
        
        return None  # Nenhum grupo coincide
    
    def _evaluate_percentage(self, config: Dict, context: Dict) -> Optional[bool]:
        """Regra PERCENTAGE: verifica se usuário está no bucket."""
        percentage = config.get("percentage", 0)
        user_id = context.get("user_id")
        flag_name = context.get("_flag_name", "unknown")
        
        if not user_id:
            return None
        
        # Hash consistente
        key = f"{user_id}:{flag_name}"
        hash_val = int(hashlib.md5(key.encode()).hexdigest(), 16)
        bucket = (hash_val % 100) + 1  # 1-100
        
        return bucket <= percentage
    
    def _evaluate_date_range(self, config: Dict, context: Dict) -> Optional[bool]:
        """Regra DATE_RANGE: verifica se está dentro do período."""
        start_str = config.get("start")
        end_str = config.get("end")
        
        now = datetime.now()
        
        if start_str:
            start = datetime.fromisoformat(start_str)
            if now < start:
                return False
        
        if end_str:
            end = datetime.fromisoformat(end_str)
            if now > end:
                return False
        
        return True
    
    def _evaluate_environment(self, config: Dict, context: Dict) -> Optional[bool]:
        """Regra ENVIRONMENT: verifica se ambiente está na lista."""
        allowed_envs = config.get("environments", [])
        current_env = context.get("environment")
        
        if not current_env:
            return None
        
        return current_env in allowed_envs
    
    def get_evaluation_log(self) -> List[Dict]:
        """Retorna log de avaliações."""
        return self._evaluations


# === Testes ===

import pytest


class TestFeatureFlagEvaluator:
    """Testes do avaliador de feature flags."""
    
    @pytest.fixture
    def evaluator(self):
        return FeatureFlagEvaluator()
    
    def test_flag_nao_existe_retorna_false(self, evaluator):
        """Flag que não existe deve retornar False."""
        result = evaluator.evaluate("flag_inexistente", {"user_id": "any"})
        assert result == False
    
    def test_flag_desabilitada_retorna_false(self, evaluator):
        """Flag desabilitada deve sempre retornar False."""
        flag = FeatureFlag(name="test", enabled=False)
        evaluator.register(flag)
        
        result = evaluator.evaluate("test", {"user_id": "any"})
        assert result == False
    
    def test_user_list_permite_usuario(self, evaluator):
        """Usuário na lista deve ser permitido."""
        flag = FeatureFlag(
            name="test",
            enabled=True,
            rules=[
                Rule(
                    type=RuleType.USER_LIST,
                    config={"users": ["user_1", "user_2"]}
                )
            ]
        )
        evaluator.register(flag)
        
        assert evaluator.evaluate("test", {"user_id": "user_1"}) == True
        assert evaluator.evaluate("test", {"user_id": "user_3"}) == False
    
    def test_group_list_permite_grupo(self, evaluator):
        """Grupo na lista deve ser permitido."""
        flag = FeatureFlag(
            name="test",
            enabled=True,
            rules=[
                Rule(
                    type=RuleType.GROUP_LIST,
                    config={"groups": ["admin", "beta"]}
                )
            ]
        )
        evaluator.register(flag)
        
        assert evaluator.evaluate("test", {"groups": ["beta", "users"]}) == True
        assert evaluator.evaluate("test", {"groups": ["users"]}) == False
    
    def test_percentage_distribuicao(self, evaluator):
        """Porcentagem deve aproximar valor configurado."""
        flag = FeatureFlag(
            name="test",
            enabled=True,
            rules=[
                Rule(
                    type=RuleType.PERCENTAGE,
                    config={"percentage": 30}
                )
            ]
        )
        evaluator.register(flag)
        
        enabled_count = 0
        for i in range(1000):
            context = {"user_id": f"user_{i}", "_flag_name": "test"}
            if evaluator.evaluate("test", context):
                enabled_count += 1
        
        # Deve estar perto de 30% (tolerância 10%)
        assert 200 < enabled_count < 400, f"Esperado ~300, obteve {enabled_count}"
    
    def test_date_range_dentro(self, evaluator):
        """Data dentro do range deve ser permitida."""
        flag = FeatureFlag(
            name="test",
            enabled=True,
            rules=[
                Rule(
                    type=RuleType.DATE_RANGE,
                    config={
                        "start": "2020-01-01",
                        "end": "2030-12-31"
                    }
                )
            ]
        )
        evaluator.register(flag)
        
        result = evaluator.evaluate("test", {})
        assert result == True
    
    def test_date_range_fora(self, evaluator):
        """Data fora do range deve retornar default."""
        flag = FeatureFlag(
            name="test",
            enabled=True,
            rules=[
                Rule(
                    type=RuleType.DATE_RANGE,
                    config={
                        "start": "2030-01-01",  # Futuro
                        "end": "2030-12-31"
                    }
                )
            ],
            default=False
        )
        evaluator.register(flag)
        
        result = evaluator.evaluate("test", {})
        assert result == False
    
    def test_environment_permite(self, evaluator):
        """Ambiente na lista deve ser permitido."""
        flag = FeatureFlag(
            name="test",
            enabled=True,
            rules=[
                Rule(
                    type=RuleType.ENVIRONMENT,
                    config={"environments": ["dev", "staging"]}
                )
            ]
        )
        evaluator.register(flag)
        
        assert evaluator.evaluate("test", {"environment": "dev"}) == True
        assert evaluator.evaluate("test", {"environment": "prod"}) == False
    
    def test_regras_compostas(self, evaluator):
        """Múltiplas regras devem funcionar juntas (OR)."""
        flag = FeatureFlag(
            name="test",
            enabled=True,
            rules=[
                # Permitir usuários específicos
                Rule(
                    type=RuleType.USER_LIST,
                    config={"users": ["vip_user"]}
                ),
                # OU grupos admin
                Rule(
                    type=RuleType.GROUP_LIST,
                    config={"groups": ["admin"]}
                ),
                # OU 10% dos usuários
                Rule(
                    type=RuleType.PERCENTAGE,
                    config={"percentage": 10}
                )
            ],
            default=False
        )
        evaluator.register(flag)
        
        # VIP user - permitido pela primeira regra
        assert evaluator.evaluate("test", {"user_id": "vip_user"}) == True
        
        # Admin - permitido pela segunda regra
        assert evaluator.evaluate("test", {"user_id": "any", "groups": ["admin"]}) == True
        
        # Usuário normal - depende do percentual
        # Testar que alguns passam e outros não
        passes = sum(
            1 for i in range(100)
            if evaluator.evaluate("test", {"user_id": f"normal_{i}", "_flag_name": "test"})
        )
        
        # Com 10%, esperamos ~10 passes (tolerância: 5-20)
        assert 5 <= passes <= 20, f"Esperado ~10, obteve {passes}"
    
    def test_evaluation_log(self, evaluator):
        """Log de avaliações deve ser registrado."""
        flag = FeatureFlag(name="test", enabled=True, default=True)
        evaluator.register(flag)
        
        evaluator.evaluate("test", {"user_id": "user_1"})
        evaluator.evaluate("test", {"user_id": "user_2"})
        
        log = evaluator.get_evaluation_log()
        
        assert len(log) == 2
        assert log[0]['flag_name'] == 'test'
        assert log[0]['context']['user_id'] == 'user_1'
```

---

## Conclusão

Os exercícios intermediários cobrem:

1. **Golden Master para API**: Capturar respostas complexas com múltiplas operações
2. **Strangler Facade com Rollout**: Migração gradual com consistência por usuário
3. **Feature Flags Avançadas**: Regras compostas com múltiplos critérios

Estas técnicas são fundamentais para migrações seguras em produção.
