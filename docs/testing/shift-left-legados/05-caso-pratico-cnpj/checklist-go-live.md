# ✅ Checklist Go-Live - Migração CNPJ Alfanumérico 2026

> **Objetivo**: Lista de verificação completa para garantir migração segura
> do validador de CNPJ numérico para alfanumérico.

---

## 📋 Sumário

1. [Pré-Requisitos](#1-pré-requisitos)
2. [Validação de Código](#2-validação-de-código)
3. [Testes e Qualidade](#3-testes-e-qualidade)
4. [Infraestrutura](#4-infraestrutura)
5. [Rollout](#5-rollout)
6. [Monitoramento](#6-monitoramento)
7. [Rollback](#7-rollback)
8. [Comunicação](#8-comunicação)
9. [Pós Go-Live](#9-pós-go-live)

---

## 1. Pré-Requisitos

### 1.1 Documentação

| Item | Responsável | Status |
|------|-------------|--------|
| ☐ Documentação técnica atualizada | Dev Lead | 🔄 |
| ☐ Regras de negócio documentadas | BA/QA | 🔄 |
| ☐ Runbook de operações criado | DevOps | 🔄 |
| ☐ Plano de rollback documentado | Dev Lead | 🔄 |
| ☐ Comunicação para stakeholders preparada | PM | 🔄 |

### 1.2 Aprovações

| Aprovação | Aprovador | Data | Status |
|-----------|-----------|------|--------|
| ☐ Code Review completo | Tech Lead | | 🔄 |
| ☐ QA Sign-off | QA Lead | | 🔄 |
| ☐ Security Review | SecOps | | 🔄 |
| ☐ Product Sign-off | Product Owner | | 🔄 |
| ☐ Go/No-Go final | Steering Committee | | 🔄 |

---

## 2. Validação de Código

### 2.1 Qualidade do Código

```text
┌─────────────────────────────────────────────────────────────────┐
│                    CRITÉRIOS DE QUALIDADE                       │
├─────────────────────────────────────────────────────────────────┤
│ ☐ Lint: 0 erros                                                 │
│ ☐ Type hints: 100% cobertura                                    │
│ ☐ Docstrings: todas as funções públicas                         │
│ ☐ Complexidade ciclomática: < 10 por função                     │
│ ☐ Código duplicado: < 3%                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Checklist de Código

| Item | Comando | Status |
|------|---------|--------|
| ☐ Lint passa | `flake8 src/` | 🔄 |
| ☐ Formatação correta | `black --check src/` | 🔄 |
| ☐ Type check passa | `mypy src/` | 🔄 |
| ☐ Sem vulnerabilidades | `bandit -r src/` | 🔄 |
| ☐ Dependências seguras | `safety check` | 🔄 |

### 2.3 Code Review

| Área | Revisor | Aprovado |
|------|---------|----------|
| ☐ Validador Alfanumérico | | 🔄 |
| ☐ Facade de Migração | | 🔄 |
| ☐ Feature Flags | | 🔄 |
| ☐ Métricas e Logging | | 🔄 |
| ☐ Testes | | 🔄 |

---

## 3. Testes e Qualidade

### 3.1 Suites de Teste

| Suite | Resultado | Cobertura | Status |
|-------|-----------|-----------|--------|
| ☐ Smoke Tests | /  | N/A | 🔄 |
| ☐ Sanity Tests | /  | N/A | 🔄 |
| ☐ Core Regression | /  | N/A | 🔄 |
| ☐ Full Regression | /  | N/A | 🔄 |
| ☐ Golden Master | 100% paridade | N/A | 🔄 |
| ☐ Performance | Dentro do limite | N/A | 🔄 |

### 3.2 Métricas de Qualidade

```text
┌─────────────────────────────────────────────────────────────────┐
│                    MÉTRICAS REQUERIDAS                          │
├─────────────────────────────────────────────────────────────────┤
│ Cobertura de código:          ___% (mínimo: 90%)     ☐ OK      │
│ Cobertura de branches:        ___% (mínimo: 85%)     ☐ OK      │
│ Testes passando:              ___% (requerido: 100%) ☐ OK      │
│ Golden Master paridade:       ___% (requerido: 100%) ☐ OK      │
│ Performance (throughput):     ___/s (mínimo: 10k)    ☐ OK      │
│ Performance (p99 latência):   ___ms (máximo: 10ms)   ☐ OK      │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Testes de Integração

| Sistema | Testado | Resultado | Status |
|---------|---------|-----------|--------|
| ☐ API REST | | Passa/Falha | 🔄 |
| ☐ Banco de Dados | | Passa/Falha | 🔄 |
| ☐ Cache | | Passa/Falha | 🔄 |
| ☐ Sistemas dependentes | | Passa/Falha | 🔄 |

---

## 4. Infraestrutura

### 4.1 Ambiente de Produção

| Item | Verificação | Status |
|------|-------------|--------|
| ☐ Servidores provisionados | Capacidade suficiente | 🔄 |
| ☐ Load balancer configurado | Health checks OK | 🔄 |
| ☐ DNS configurado | Resolução OK | 🔄 |
| ☐ SSL/TLS válido | Certificado válido | 🔄 |
| ☐ Firewall configurado | Regras aplicadas | 🔄 |

### 4.2 Feature Flags

| Flag | Descrição | Estado Inicial |
|------|-----------|----------------|
| ☐ `cnpj.validator.new.enabled` | Habilita novo validador | `false` |
| ☐ `cnpj.validator.rollout.percentage` | % de tráfego | `0` |
| ☐ `cnpj.validator.shadow.enabled` | Shadow mode | `false` |
| ☐ `cnpj.validator.auto.rollback` | Rollback automático | `true` |

### 4.3 Configurações

```yaml
# Configuração inicial de produção

cnpj:
  validator:
    new:
      enabled: false
    rollout:
      percentage: 0
      shadow: true
    auto_rollback:
      enabled: true
      threshold: 0.001  # 0.1%
    monitoring:
      enabled: true
      alert_threshold: 0.01
```

---

## 5. Rollout

### 5.1 Plano de Rollout

| Fase | % Tráfego | Duração | Critério de Avanço |
|------|-----------|---------|-------------------|
| 0 | Shadow only | 1 semana | 0 divergências |
| 1 | 1% | 3 dias | Taxa erro < 0.01% |
| 2 | 5% | 3 dias | Taxa erro < 0.01% |
| 3 | 10% | 1 semana | Taxa erro < 0.01% |
| 4 | 25% | 1 semana | Taxa erro < 0.01% |
| 5 | 50% | 2 semanas | Taxa erro < 0.01% |
| 6 | 100% | Final | Monitoramento 1 mês |

### 5.2 Checklist por Fase

#### Fase 0: Shadow Mode

| Item | Status |
|------|--------|
| ☐ Shadow mode ativado | 🔄 |
| ☐ Métricas de comparação coletadas | 🔄 |
| ☐ 0 divergências por 24h | 🔄 |
| ☐ 0 divergências por 72h | 🔄 |
| ☐ 0 divergências por 1 semana | 🔄 |

#### Fase 1: 1% Tráfego

| Item | Status |
|------|--------|
| ☐ Rollout aumentado para 1% | 🔄 |
| ☐ Alertas configurados | 🔄 |
| ☐ Taxa de erro < 0.01% por 24h | 🔄 |
| ☐ Taxa de erro < 0.01% por 72h | 🔄 |
| ☐ Aprovação para próxima fase | 🔄 |

#### Fases 2-5: Avanço Gradual

| Fase | % | Início | Fim | Aprovador | Status |
|------|---|--------|-----|-----------|--------|
| 2 | 5% | | | | 🔄 |
| 3 | 10% | | | | 🔄 |
| 4 | 25% | | | | 🔄 |
| 5 | 50% | | | | 🔄 |

#### Fase 6: 100% - Go-Live Final

| Item | Status |
|------|--------|
| ☐ Rollout aumentado para 100% | 🔄 |
| ☐ Sistema legado em standby | 🔄 |
| ☐ Monitoramento intensivo por 24h | 🔄 |
| ☐ Monitoramento por 1 semana | 🔄 |
| ☐ Monitoramento por 1 mês | 🔄 |
| ☐ Legado desativado | 🔄 |
| ☐ Feature flags removidas | 🔄 |

---

## 6. Monitoramento

### 6.1 Dashboards

| Dashboard | URL | Responsável |
|-----------|-----|-------------|
| ☐ Métricas de validação | | SRE |
| ☐ Comparação legado vs novo | | SRE |
| ☐ Taxa de erro | | SRE |
| ☐ Latência | | SRE |
| ☐ Throughput | | SRE |

### 6.2 Alertas Configurados

| Alerta | Threshold | Ação | Status |
|--------|-----------|------|--------|
| ☐ Taxa de erro alta | > 0.1% | Rollback 50% | 🔄 |
| ☐ Taxa de erro crítica | > 1% | Rollback 0% | 🔄 |
| ☐ Divergência detectada | Qualquer | Alerta + Log | 🔄 |
| ☐ Latência alta | p99 > 10ms | Alerta | 🔄 |
| ☐ Throughput baixo | < 5k/s | Alerta | 🔄 |

### 6.3 Métricas a Monitorar

```text
┌─────────────────────────────────────────────────────────────────┐
│                    MÉTRICAS DE MONITORAMENTO                    │
├─────────────────────────────────────────────────────────────────┤
│ 📊 Taxa de sucesso:        ___% (alvo: > 99.99%)               │
│ 📊 Taxa de erro:           ___% (alvo: < 0.01%)                │
│ 📊 Divergências:           ___ (alvo: 0)                       │
│ 📊 Latência média:         ___ms (alvo: < 1ms)                 │
│ 📊 Latência p99:           ___ms (alvo: < 10ms)                │
│ 📊 Throughput:             ___/s (alvo: > 10k)                 │
│ 📊 Chamadas legado:        ___                                 │
│ 📊 Chamadas novo:          ___                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Rollback

### 7.1 Triggers de Rollback

| Condição | Ação Automática | Ação Manual |
|----------|-----------------|-------------|
| Taxa erro > 0.1% | Reduz para 50% | Avaliar |
| Taxa erro > 1% | Reduz para 0% | Investigar |
| Divergência detectada | Log + Alerta | Avaliar |
| Latência p99 > 50ms | Alerta | Avaliar |
| Incidente P1 | Rollback imediato | Comunicar |

### 7.2 Procedimento de Rollback

```text
┌─────────────────────────────────────────────────────────────────┐
│                 PROCEDIMENTO DE ROLLBACK                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 1. IDENTIFICAR                                                   │
│    ☐ Verificar alertas e métricas                               │
│    ☐ Confirmar necessidade de rollback                          │
│    ☐ Comunicar equipe                                           │
│                                                                  │
│ 2. EXECUTAR                                                      │
│    ☐ Executar: facade.emergency_rollback()                      │
│    ☐ OU: Atualizar flag cnpj.validator.rollout.percentage = 0   │
│    ☐ Verificar que tráfego voltou para legado                   │
│                                                                  │
│ 3. VERIFICAR                                                     │
│    ☐ Confirmar 100% no legado                                   │
│    ☐ Verificar métricas normalizando                            │
│    ☐ Confirmar taxa de erro < 0.01%                             │
│                                                                  │
│ 4. COMUNICAR                                                     │
│    ☐ Notificar stakeholders                                     │
│    ☐ Criar incidente/post-mortem                                │
│    ☐ Documentar lições aprendidas                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Comandos de Rollback

```bash
# Rollback via API
curl -X POST https://api.example.com/admin/rollback \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"percentage": 0}'

# Rollback via Feature Flag
curl -X PUT https://flags.example.com/cnpj.validator.rollout.percentage \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"value": 0}'

# Rollback via CLI
python -m cnpj_validator.admin rollback --immediate
```

---

## 8. Comunicação

### 8.1 Stakeholders

| Grupo | Canal | Quando Comunicar |
|-------|-------|------------------|
| Time de Dev | Slack #dev-cnpj | Sempre |
| Time de QA | Slack #qa-cnpj | Sempre |
| SRE/DevOps | Slack #sre-alerts | Incidentes |
| Product | Email | Início/Fim de fases |
| Executivos | Email | Go-Live final |

### 8.2 Templates de Comunicação

#### Início de Fase

```text
🚀 [CNPJ 2026] Iniciando Fase X - Y% Tráfego

Equipe,

Estamos iniciando a Fase X do rollout do novo validador CNPJ.

📊 Detalhes:
- Porcentagem: Y%
- Início: [DATA/HORA]
- Duração esperada: [DURAÇÃO]
- Critério de sucesso: Taxa erro < 0.01%

📈 Monitoramento:
- Dashboard: [LINK]
- Alertas: Configurados

Em caso de problemas, contatar: [RESPONSÁVEL]
```

#### Rollback

```text
⚠️ [CNPJ 2026] ROLLBACK Executado

Equipe,

Foi executado rollback do novo validador CNPJ.

📊 Detalhes:
- Motivo: [MOTIVO]
- Horário: [DATA/HORA]
- Ação: Rollout reduzido para 0%

📈 Status:
- Sistema operando normalmente com validador legado
- Investigação em andamento

Próximos passos: [AÇÃO]
Post-mortem: [DATA]
```

---

## 9. Pós Go-Live

### 9.1 Validação Pós-Deploy

| Item | Prazo | Status |
|------|-------|--------|
| ☐ Verificar métricas por 24h | D+1 | 🔄 |
| ☐ Verificar métricas por 72h | D+3 | 🔄 |
| ☐ Verificar métricas por 1 semana | D+7 | 🔄 |
| ☐ Verificar métricas por 1 mês | D+30 | 🔄 |
| ☐ Coletar feedback de usuários | D+7 | 🔄 |

### 9.2 Cleanup

| Item | Prazo | Status |
|------|-------|--------|
| ☐ Remover código legado | D+60 | 🔄 |
| ☐ Remover feature flags | D+60 | 🔄 |
| ☐ Atualizar documentação | D+30 | 🔄 |
| ☐ Arquivar Golden Master legado | D+90 | 🔄 |
| ☐ Desprovisionar recursos legado | D+90 | 🔄 |

### 9.3 Retrospectiva

| Item | Data | Status |
|------|------|--------|
| ☐ Agendar retrospectiva | | 🔄 |
| ☐ Coletar métricas finais | | 🔄 |
| ☐ Documentar lições aprendidas | | 🔄 |
| ☐ Criar template para futuras migrações | | 🔄 |
| ☐ Celebrar sucesso! 🎉 | | 🔄 |

---

## 📊 Dashboard de Status

```text
╔═════════════════════════════════════════════════════════════════╗
║              STATUS GERAL DA MIGRAÇÃO                           ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                  ║
║   Fase Atual:        [_______________]                          ║
║   % Rollout:         [___]%                                     ║
║   Status:            [🟢 OK / 🟡 Atenção / 🔴 Crítico]          ║
║                                                                  ║
║   ┌─────────────────────────────────────────────────────────┐   ║
║   │ Pré-Requisitos:  [██████████] 100%                      │   ║
║   │ Código:          [████████░░]  80%                      │   ║
║   │ Testes:          [██████████] 100%                      │   ║
║   │ Infraestrutura:  [████████░░]  80%                      │   ║
║   │ Rollout:         [████░░░░░░]  40%                      │   ║
║   │ Monitoramento:   [██████████] 100%                      │   ║
║   └─────────────────────────────────────────────────────────┘   ║
║                                                                  ║
║   Última atualização: [DATA/HORA]                               ║
║   Próxima revisão:    [DATA/HORA]                               ║
║                                                                  ║
╚═════════════════════════════════════════════════════════════════╝
```

---

## 🔗 Links Úteis

| Recurso | Link |
|---------|------|
| Documentação Técnica | [docs/](../) |
| Dashboard de Métricas | [link] |
| Runbook de Operações | [link] |
| Canal de Comunicação | Slack #cnpj-2026 |
| Repositório de Código | GitHub |

---

## 📚 Referências

- [Cenário de Migração](cenario-migracao.md)
- [Plano de Testes](plano-de-testes.md)
- [Implementação dos Testes](implementacao-testes.md)
- [Guia de Shift Left em Legados](../01-fundamentos/)
