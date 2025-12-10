# 🗺️ Estratégias de Migração em Sistemas Legados

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- ✅ Escolher a estratégia de migração adequada para cada cenário
- ✅ Entender os trade-offs de cada abordagem
- ✅ Planejar uma migração com risco controlado
- ✅ Aplicar a estratégia correta para migração de CNPJ

---

## 1. As 4 Estratégias Principais

### Visão Geral

```text
┌─────────────────────────────────────────────────────────────────┐
│           ESTRATÉGIAS DE MIGRAÇÃO EM LEGADOS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│   │ BIG BANG    │   │ STRANGLER   │   │ PARALLEL    │          │
│   │             │   │ FIG         │   │ RUN         │          │
│   │ Tudo de uma │   │ Gradual     │   │ Dois        │          │
│   │ vez         │   │ estrangula  │   │ sistemas    │          │
│   └─────────────┘   └─────────────┘   └─────────────┘          │
│          ▲                 ▲                 ▲                  │
│          │                 │                 │                  │
│       Rápido            Seguro           Mais seguro           │
│       Arriscado         Lento            Caro                  │
│                                                                  │
│                    ┌─────────────┐                              │
│                    │ FEATURE     │                              │
│                    │ FLAGS       │                              │
│                    │             │                              │
│                    │ Liga/       │                              │
│                    │ desliga     │                              │
│                    └─────────────┘                              │
│                          ▲                                      │
│                          │                                      │
│                      Flexível                                   │
│                      Complexo                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Estratégia #1: Big Bang

### 2.1 O Que É

**Big Bang** = Substituir tudo de uma vez em um único deploy.

```text
┌──────────────────────────────────────────────────────────────┐
│                     BIG BANG                                  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ANTES:                                                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              SISTEMA LEGADO v1.0                        │ │
│  │              (Apenas CNPJ numérico)                     │ │
│  └─────────────────────────────────────────────────────────┘ │
│                           │                                   │
│                           │ DEPLOY (um único momento)        │
│                           ▼                                   │
│  DEPOIS:                                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              SISTEMA NOVO v2.0                          │ │
│  │              (CNPJ numérico + alfanumérico)             │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 Quando Usar

| Situação | Big Bang é adequado? |
|----------|----------------------|
| Sistema pequeno (< 10k linhas) | ✅ Sim |
| Mudança isolada e bem definida | ✅ Sim |
| Time experiente e confiante | ✅ Sim |
| Sistema crítico 24/7 | ❌ Não |
| Muitas integrações externas | ❌ Não |
| Pouca cobertura de testes | ❌ Não |

### 2.3 Exemplo com CNPJ

```python
# Big Bang: Trocar o validador de uma vez

# ANTES (sexta à noite)
from validador_cnpj_legado import validar_cnpj

# DEPOIS (segunda de manhã)
from validador_cnpj_2026 import validar_cnpj

# Riscos:
# - Se quebrar, afeta todos os usuários
# - Rollback pode ser complicado
# - Precisa de muita confiança nos testes
```

### 2.4 Checklist Big Bang

```text
☐ Todos os testes passando (100%)
☐ Testes de caracterização completos
☐ Ambiente de staging validado
☐ Plano de rollback documentado
☐ Janela de manutenção agendada
☐ Time de plantão disponível
☐ Monitoramento intensivo preparado
☐ Comunicação aos stakeholders feita
```

---

## 3. Estratégia #2: Strangler Fig Pattern

### 3.1 O Que É

**Strangler Fig** (Figueira Estranguladora) = Substituir gradualmente partes do sistema legado, até que ele desapareça.

Nome vem da figueira que cresce ao redor de uma árvore até substituí-la completamente.

```text
┌──────────────────────────────────────────────────────────────┐
│                   STRANGLER FIG PATTERN                       │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  FASE 1: Sistema legado completo                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ████████████████████████████████████████████████████████│ │
│  │                    LEGADO (100%)                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  FASE 2: Novo sistema começa a crescer                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ████████████████████████████████████████░░░░░░░░░░░░░░░│ │
│  │           LEGADO (70%)           │    NOVO (30%)        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  FASE 3: Novo sistema domina                                 │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ │
│  │  LEGADO(20%)│              NOVO (80%)                   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  FASE 4: Legado eliminado                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ │
│  │                      NOVO (100%)                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Implementação com Facade

```python
# Strangler Fig com Facade (Fachada)

class ValidadorCNPJFacade:
    """
    Fachada que decide qual validador usar.
    Permite migração gradual do legado para o novo.
    """
    
    def __init__(self):
        self.validador_legado = ValidadorCNPJLegado()
        self.validador_novo = ValidadorCNPJ2026()
        
        # Configuração de migração
        self.percentual_novo = 0  # Começa em 0%
    
    def validar(self, cnpj):
        """
        Roteia para validador correto baseado na configuração.
        """
        # Se CNPJ tem letras, força usar o novo
        if any(c.isalpha() for c in cnpj):
            return self.validador_novo.validar(cnpj)
        
        # Para CNPJs numéricos, usa migração gradual
        if self._usar_novo_validador():
            return self.validador_novo.validar(cnpj)
        else:
            return self.validador_legado.validar(cnpj)
    
    def _usar_novo_validador(self):
        """Decide se usa novo validador baseado em percentual."""
        import random
        return random.randint(1, 100) <= self.percentual_novo


# Plano de migração:
# Semana 1: percentual_novo = 10%  (10% dos requests usam novo)
# Semana 2: percentual_novo = 25%
# Semana 3: percentual_novo = 50%
# Semana 4: percentual_novo = 75%
# Semana 5: percentual_novo = 100%
# Semana 6: Remover código legado
```

### 3.3 Quando Usar

| Situação | Strangler Fig é adequado? |
|----------|---------------------------|
| Sistema grande e complexo | ✅ Sim |
| Migração de longo prazo | ✅ Sim |
| Precisa de rollback rápido | ✅ Sim |
| Time pequeno | ✅ Sim |
| Mudança urgente (dias) | ❌ Não |
| Orçamento muito limitado | ❌ Não |

---

## 4. Estratégia #3: Parallel Run

### 4.1 O Que É

**Parallel Run** = Executar os dois sistemas simultaneamente e comparar resultados.

```text
┌──────────────────────────────────────────────────────────────┐
│                    PARALLEL RUN                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│              ┌──────────────────────┐                        │
│              │    REQUEST CNPJ      │                        │
│              │  "11.222.333/0001-81"│                        │
│              └──────────┬───────────┘                        │
│                         │                                     │
│           ┌─────────────┴─────────────┐                      │
│           │                           │                       │
│           ▼                           ▼                       │
│  ┌─────────────────┐       ┌─────────────────┐              │
│  │    LEGADO       │       │      NOVO       │              │
│  │  validar_cnpj() │       │  validar_cnpj() │              │
│  └────────┬────────┘       └────────┬────────┘              │
│           │                         │                        │
│           ▼                         ▼                        │
│       resultado_1               resultado_2                  │
│        (True)                    (True)                      │
│           │                         │                        │
│           └─────────┬───────────────┘                        │
│                     │                                         │
│                     ▼                                         │
│           ┌─────────────────────┐                            │
│           │     COMPARADOR      │                            │
│           │                     │                            │
│           │  resultado_1 ==     │                            │
│           │  resultado_2 ?      │                            │
│           │                     │                            │
│           │  ✅ Iguais: OK      │                            │
│           │  ❌ Diferentes: LOG │                            │
│           └─────────────────────┘                            │
│                     │                                         │
│                     ▼                                         │
│           ┌─────────────────────┐                            │
│           │   RETORNA LEGADO    │ ← Segurança: usa o legado │
│           │   (por segurança)   │                            │
│           └─────────────────────┘                            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 Implementação

```python
# Parallel Run: Executa os dois e compara

import logging

class ValidadorCNPJParalelo:
    """
    Executa ambos validadores e compara resultados.
    Sempre retorna resultado do legado (segurança).
    Loga divergências para análise.
    """
    
    def __init__(self):
        self.legado = ValidadorCNPJLegado()
        self.novo = ValidadorCNPJ2026()
        self.logger = logging.getLogger("parallel_run")
    
    def validar(self, cnpj):
        # Executa ambos
        resultado_legado = self.legado.validar(cnpj)
        resultado_novo = self.novo.validar(cnpj)
        
        # Compara
        if resultado_legado != resultado_novo:
            self.logger.warning(
                f"DIVERGÊNCIA! CNPJ={cnpj} "
                f"Legado={resultado_legado} "
                f"Novo={resultado_novo}"
            )
            
            # Salva para análise posterior
            self._salvar_divergencia(cnpj, resultado_legado, resultado_novo)
        
        # Por segurança, retorna resultado do legado
        return resultado_legado
    
    def _salvar_divergencia(self, cnpj, res_legado, res_novo):
        """Salva divergência para análise."""
        with open("divergencias.log", "a") as f:
            f.write(f"{cnpj},{res_legado},{res_novo}\n")


# Após período de parallel run (ex: 2 semanas):
# 1. Analisar divergencias.log
# 2. Investigar cada caso
# 3. Decidir qual está certo
# 4. Ajustar validador novo se necessário
# 5. Quando divergências = 0, migrar para novo
```

### 4.3 Golden Master Testing

Uma variação do Parallel Run é o **Golden Master**:

```python
# Golden Master: Captura saídas do legado como "verdade"

class GoldenMasterTest:
    """
    Captura outputs do sistema legado como referência.
    Compara sistema novo contra essa referência.
    """
    
    @staticmethod
    def gerar_golden_master():
        """Executa uma vez para criar a referência."""
        legado = ValidadorCNPJLegado()
        
        casos_teste = [
            "11222333000181",
            "11.222.333/0001-81",
            "00000000000000",
            "11111111111111",
            "12345678901234",
            # ... centenas de casos
        ]
        
        golden = {}
        for cnpj in casos_teste:
            golden[cnpj] = legado.validar(cnpj)
        
        # Salvar como arquivo JSON
        import json
        with open("golden_master_cnpj.json", "w") as f:
            json.dump(golden, f)
    
    @staticmethod
    def comparar_com_golden_master():
        """Testa sistema novo contra golden master."""
        import json
        
        with open("golden_master_cnpj.json") as f:
            golden = json.load(f)
        
        novo = ValidadorCNPJ2026()
        divergencias = []
        
        for cnpj, esperado in golden.items():
            resultado = novo.validar(cnpj)
            if resultado != esperado:
                divergencias.append({
                    "cnpj": cnpj,
                    "esperado": esperado,
                    "obtido": resultado
                })
        
        return divergencias
```

---

## 5. Estratégia #4: Feature Flags

### 5.1 O Que É

**Feature Flags** = Interruptores que ligam/desligam funcionalidades em tempo real.

```text
┌──────────────────────────────────────────────────────────────┐
│                    FEATURE FLAGS                              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │                    PAINEL DE CONTROLE                    ││
│  │                                                          ││
│  │  [✓] CNPJ_ALFANUMERICO_VALIDACAO    ON                  ││
│  │  [ ] CNPJ_ALFANUMERICO_CADASTRO     OFF                 ││
│  │  [ ] CNPJ_ALFANUMERICO_NFE          OFF                 ││
│  │  [ ] CNPJ_ALFANUMERICO_RELATORIOS   OFF                 ││
│  │                                                          ││
│  │  Usuários habilitados: 10% (teste A/B)                  ││
│  │  Empresas habilitadas: [EMPRESA_TESTE_01, EMPRESA_02]   ││
│  │                                                          ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  VANTAGENS:                                                   │
│  ✅ Rollback instantâneo (só desligar a flag)               │
│  ✅ Deploy gradual por usuário/empresa                       │
│  ✅ Testes A/B em produção                                   │
│  ✅ Separação entre deploy e release                         │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 Implementação

```python
# Feature Flags para migração de CNPJ

class FeatureFlags:
    """Gerenciador de feature flags."""
    
    # Configuração (pode vir de banco, arquivo, serviço externo)
    FLAGS = {
        "CNPJ_ALFANUMERICO_HABILITADO": False,
        "CNPJ_ALFANUMERICO_PERCENTUAL": 0,
        "CNPJ_ALFANUMERICO_EMPRESAS": [],
    }
    
    @classmethod
    def is_enabled(cls, flag_name, contexto=None):
        """Verifica se flag está habilitada."""
        if flag_name not in cls.FLAGS:
            return False
        
        valor = cls.FLAGS[flag_name]
        
        # Flag booleana simples
        if isinstance(valor, bool):
            return valor
        
        # Flag com percentual
        if flag_name.endswith("_PERCENTUAL"):
            import random
            return random.randint(1, 100) <= valor
        
        # Flag com lista de empresas
        if flag_name.endswith("_EMPRESAS") and contexto:
            return contexto.get("empresa_id") in valor
        
        return False


class ValidadorCNPJComFlags:
    """Validador que usa feature flags."""
    
    def __init__(self):
        self.legado = ValidadorCNPJLegado()
        self.novo = ValidadorCNPJ2026()
    
    def validar(self, cnpj, contexto=None):
        """
        Valida CNPJ usando validador apropriado baseado em flags.
        """
        # CNPJ alfanumérico SEMPRE usa novo (não tem escolha)
        if any(c.isalpha() for c in cnpj):
            if FeatureFlags.is_enabled("CNPJ_ALFANUMERICO_HABILITADO"):
                return self.novo.validar(cnpj)
            else:
                # Flag desligada: rejeita alfanuméricos
                return False
        
        # CNPJ numérico: usa flag para decidir
        if FeatureFlags.is_enabled("CNPJ_ALFANUMERICO_HABILITADO", contexto):
            return self.novo.validar(cnpj)
        else:
            return self.legado.validar(cnpj)


# Uso:
validador = ValidadorCNPJComFlags()

# Fase 1: Flag OFF - usa legado para todos
resultado = validador.validar("11222333000181")

# Fase 2: Flag ON para empresa teste
FeatureFlags.FLAGS["CNPJ_ALFANUMERICO_HABILITADO"] = True
FeatureFlags.FLAGS["CNPJ_ALFANUMERICO_EMPRESAS"] = ["EMPRESA_TESTE"]

resultado = validador.validar(
    "11222333000181", 
    contexto={"empresa_id": "EMPRESA_TESTE"}
)  # Usa novo

# Fase 3: Flag ON para todos
FeatureFlags.FLAGS["CNPJ_ALFANUMERICO_PERCENTUAL"] = 100
```

---

## 6. Comparação das Estratégias

### 6.1 Tabela Comparativa

| Critério | Big Bang | Strangler Fig | Parallel Run | Feature Flags |
|----------|----------|---------------|--------------|---------------|
| **Velocidade** | ⚡ Rápido | 🐢 Lento | 🐢 Lento | ⚡ Médio |
| **Risco** | 🔴 Alto | 🟢 Baixo | 🟢 Muito baixo | 🟢 Baixo |
| **Custo** | 💰 Baixo | 💰💰 Médio | 💰💰💰 Alto | 💰💰 Médio |
| **Complexidade** | 📊 Baixa | 📊📊 Média | 📊📊📊 Alta | 📊📊 Média |
| **Rollback** | 😰 Difícil | 😊 Fácil | 😊 Muito fácil | 😊 Instantâneo |
| **Equipe mínima** | 2-3 devs | 1-2 devs | 3-5 devs | 2-3 devs |

### 6.2 Fluxograma de Decisão

```text
                    ┌─────────────────────┐
                    │ Sistema é crítico?  │
                    │ (24/7, muitos       │
                    │  usuários)          │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                  │
             SIM                                NÃO
              │                                  │
              ▼                                  ▼
    ┌─────────────────┐               ┌─────────────────┐
    │ Precisa de      │               │ Mudança é       │
    │ rollback        │               │ pequena e       │
    │ instantâneo?    │               │ isolada?        │
    └────────┬────────┘               └────────┬────────┘
             │                                  │
    ┌────────┴────────┐               ┌────────┴────────┐
    │                 │               │                 │
   SIM               NÃO             SIM               NÃO
    │                 │               │                 │
    ▼                 ▼               ▼                 ▼
┌────────┐    ┌────────────┐    ┌────────┐    ┌────────────┐
│FEATURE │    │ PARALLEL   │    │ BIG    │    │ STRANGLER  │
│FLAGS   │    │ RUN        │    │ BANG   │    │ FIG        │
└────────┘    └────────────┘    └────────┘    └────────────┘
```

---

## 7. Aplicando ao Cenário CNPJ 2026

### 7.1 Recomendação

Para migração de CNPJ alfanumérico, recomendamos:

**Estratégia principal**: Strangler Fig + Feature Flags

**Por quê**:
- Sistema de CNPJ é crítico (cadastros, NFe, integrações)
- Precisa de rollback rápido
- Migração pode ser gradual (jul/2026 não é "amanhã")
- Permite validar em produção com usuários reais

### 7.2 Plano de Implementação

```text
┌──────────────────────────────────────────────────────────────┐
│         PLANO DE MIGRAÇÃO CNPJ ALFANUMÉRICO                  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  MÊS 1-2: PREPARAÇÃO                                         │
│  ├── Criar testes de caracterização do legado                │
│  ├── Implementar novo validador (já feito!)                  │
│  ├── Implementar Feature Flags                               │
│  └── Parallel Run em ambiente de teste                       │
│                                                               │
│  MÊS 3: PILOTO                                               │
│  ├── Feature Flag ON para 1 empresa parceira                 │
│  ├── Monitorar erros e divergências                          │
│  └── Ajustar baseado em feedback                             │
│                                                               │
│  MÊS 4: EXPANSÃO GRADUAL                                     │
│  ├── Feature Flag ON para 10% dos usuários                   │
│  ├── Aumentar para 25%, 50%, 75%                             │
│  └── Coletar métricas de sucesso                             │
│                                                               │
│  MÊS 5: MIGRAÇÃO COMPLETA                                    │
│  ├── Feature Flag ON para 100%                               │
│  ├── Manter legado como fallback por 30 dias                 │
│  └── Documentar e comunicar mudança                          │
│                                                               │
│  MÊS 6: LIMPEZA                                              │
│  ├── Remover código legado                                   │
│  ├── Remover Feature Flags                                   │
│  └── Atualizar documentação                                  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. Resumo

### 8.1 As 4 Estratégias

| Estratégia | Quando Usar | Palavra-chave |
|------------|-------------|---------------|
| **Big Bang** | Mudanças pequenas, time confiante | Velocidade |
| **Strangler Fig** | Migrações longas, sistemas grandes | Gradualidade |
| **Parallel Run** | Sistemas críticos, precisa de certeza | Segurança |
| **Feature Flags** | Precisa de controle fino | Flexibilidade |

### 8.2 A Mensagem Principal

> **Não existe estratégia "melhor".**
> 
> A estratégia certa depende do seu contexto:
> - Criticidade do sistema
> - Tamanho da mudança
> - Experiência do time
> - Prazo disponível
> - Tolerância a risco

---

**Próximo módulo**: [02-tecnicas/01-characterization-tests.md](../02-tecnicas/01-characterization-tests.md)
