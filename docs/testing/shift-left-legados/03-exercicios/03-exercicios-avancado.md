# 🔴 Exercícios Nível Avançado - Suporte 0%

## Objetivo

Exercícios com mínima orientação. Você recebe apenas os requisitos de negócio
e deve projetar a solução completa. Estes exercícios simulam cenários reais
de migração de sistemas legados.

---

## Exercício 1: Migração Completa de Módulo de Pagamentos

### Cenário de Negócio

A empresa XYZ tem um módulo de processamento de pagamentos legado que precisa
ser substituído por uma nova implementação. O módulo processa milhões de
transações por dia e qualquer erro pode causar prejuízos financeiros.

### Requisitos de Negócio

1. **Zero downtime**: A migração não pode interromper o serviço
2. **Rollback instantâneo**: Em caso de problema, deve reverter em segundos
3. **Auditoria**: Todas as transações devem ser logadas para auditoria
4. **Paridade**: Nova implementação deve ter 100% de paridade com legado
5. **Performance**: Nova implementação não pode ser mais que 10% mais lenta

### Código Legado Simplificado

```python
# legacy/payment_processor.py
class PaymentProcessor:
    """
    Processador de pagamentos legado.
    Em produção há 8 anos, processa R$ 50M/dia.
    """
    
    def process(self, transaction):
        """
        Processa uma transação de pagamento.
        
        Args:
            transaction: {
                'id': str,
                'amount': float,
                'currency': str,
                'type': 'credit' | 'debit' | 'pix',
                'customer_id': str,
                'merchant_id': str,
            }
        
        Returns:
            {
                'transaction_id': str,
                'status': 'approved' | 'declined' | 'error',
                'code': str,
                'message': str,
            }
        """
        # Validações
        if not transaction.get('amount') or transaction['amount'] <= 0:
            return {'status': 'error', 'code': 'E001', 'message': 'Invalid amount'}
        
        if transaction['amount'] > 50000:
            return {'status': 'declined', 'code': 'D001', 'message': 'Amount exceeds limit'}
        
        # Processamento simplificado
        approved = transaction['amount'] < 10000  # Simula regra de negócio
        
        return {
            'transaction_id': f"TXN-{transaction['id']}",
            'status': 'approved' if approved else 'declined',
            'code': 'A001' if approved else 'D002',
            'message': 'Transaction approved' if approved else 'Risk analysis declined'
        }
    
    def refund(self, transaction_id, amount):
        """Processa estorno."""
        # Implementação simplificada
        return {
            'refund_id': f"REF-{transaction_id}",
            'status': 'approved',
            'amount': amount
        }
    
    def get_status(self, transaction_id):
        """Consulta status de transação."""
        # Implementação simplificada
        return {
            'transaction_id': transaction_id,
            'status': 'completed',
            'amount': 100.00
        }
```

### Suas Tarefas

1. **Projetar Estratégia de Migração**
   - Escolher padrão apropriado (Strangler Fig, Feature Flags, ou combinação)
   - Definir fases do rollout
   - Criar plano de rollback

2. **Implementar Testes de Caracterização**
   - Descobrir todos os comportamentos do sistema legado
   - Documentar regras de negócio implícitas
   - Criar suite de testes abrangente

3. **Criar Golden Master**
   - Capturar comportamento para milhares de cenários
   - Incluir casos de borda e erros
   - Implementar comparação automatizada

4. **Implementar Facade de Migração**
   - Suportar rollout gradual por porcentagem
   - Implementar shadow mode
   - Criar logging detalhado para auditoria
   - Normalizar respostas para compatibilidade

5. **Criar Suite de Testes de Regressão**
   - Smoke tests (< 1 min)
   - Sanity tests (< 5 min)
   - Core regression (< 30 min)
   - Full regression (todas as combinações)

6. **Implementar Monitoramento**
   - Métricas de sucesso/falha
   - Alertas para divergências
   - Dashboard de migração

### Entregáveis

- [ ] Documento de estratégia de migração
- [ ] Suite de testes de caracterização
- [ ] Golden Master com 1000+ casos
- [ ] Facade com rollout gradual
- [ ] Suite de regressão em 4 níveis
- [ ] Script de monitoramento
- [ ] Plano de rollback documentado

---

## Exercício 2: Sistema de Regras de Negócio

### Cenário de Negócio

Uma seguradora tem um motor de regras legado que calcula prêmios de seguros.
O sistema tem mais de 200 regras de negócio, algumas conflitantes, e ninguém
sabe exatamente como todas funcionam juntas.

### Desafio

O sistema legado usa uma linguagem proprietária de regras:

```text
# Arquivo: regras_auto.rules (exemplo)
RULE premium_base
  IF vehicle_type = "car" THEN premium = 1000
  IF vehicle_type = "motorcycle" THEN premium = 500
  IF vehicle_type = "truck" THEN premium = 2000
END

RULE age_modifier
  IF driver_age < 25 THEN premium = premium * 1.5
  IF driver_age > 65 THEN premium = premium * 1.2
END

RULE history_modifier
  IF accidents_5_years > 0 THEN premium = premium * (1 + accidents_5_years * 0.1)
  IF years_without_claims > 3 THEN premium = premium * 0.9
END

RULE location_modifier
  IF state IN ["SP", "RJ"] THEN premium = premium * 1.3
  IF city_risk = "high" THEN premium = premium * 1.2
END

# ... mais 196 regras ...
```

### Suas Tarefas

1. **Reverse Engineering das Regras**
   - Criar parser para o formato proprietário
   - Documentar cada regra em formato legível
   - Identificar conflitos e sobreposições

2. **Caracterização via Fuzzing**
   - Gerar milhares de inputs aleatórios
   - Capturar outputs como Golden Master
   - Identificar casos de borda não documentados

3. **Nova Implementação**
   - Reimplementar regras em Python
   - Usar estrutura testável e manutenível
   - Garantir 100% de paridade com legado

4. **Migração Gradual**
   - Implementar facade com feature flags por regra
   - Permitir migrar uma regra de cada vez
   - Criar dashboard de progresso

### Entregáveis

- [ ] Parser do formato proprietário
- [ ] Documentação de todas as regras
- [ ] Suite de fuzzing para Golden Master
- [ ] Nova implementação em Python
- [ ] Facade com flags por regra
- [ ] Testes de paridade
- [ ] Dashboard de migração

---

## Exercício 3: Migração de Banco de Dados

### Cenário de Negócio

Uma empresa está migrando de um banco de dados Oracle legado para PostgreSQL.
O sistema processa milhões de registros e tem procedures complexas.

### Desafio

```sql
-- Procedure legada Oracle (simplificada)
CREATE OR REPLACE PROCEDURE calcular_comissao(
    p_vendedor_id IN NUMBER,
    p_mes IN NUMBER,
    p_ano IN NUMBER,
    p_comissao OUT NUMBER,
    p_detalhes OUT SYS_REFCURSOR
) AS
    v_total_vendas NUMBER;
    v_meta NUMBER;
    v_percentual NUMBER;
    v_bonus NUMBER := 0;
BEGIN
    -- Calcular total de vendas
    SELECT NVL(SUM(valor), 0) INTO v_total_vendas
    FROM vendas
    WHERE vendedor_id = p_vendedor_id
      AND EXTRACT(MONTH FROM data_venda) = p_mes
      AND EXTRACT(YEAR FROM data_venda) = p_ano
      AND status = 'APROVADA';
    
    -- Buscar meta
    SELECT meta INTO v_meta
    FROM metas_vendedores
    WHERE vendedor_id = p_vendedor_id
      AND mes = p_mes AND ano = p_ano;
    
    -- Calcular percentual baseado em faixa
    IF v_total_vendas >= v_meta * 1.5 THEN
        v_percentual := 0.15;
        v_bonus := 500;
    ELSIF v_total_vendas >= v_meta THEN
        v_percentual := 0.10;
    ELSIF v_total_vendas >= v_meta * 0.8 THEN
        v_percentual := 0.05;
    ELSE
        v_percentual := 0.02;
    END IF;
    
    -- Calcular comissão
    p_comissao := (v_total_vendas * v_percentual) + v_bonus;
    
    -- Abrir cursor de detalhes
    OPEN p_detalhes FOR
        SELECT v.*, (v.valor * v_percentual) as comissao_item
        FROM vendas v
        WHERE vendedor_id = p_vendedor_id
          AND EXTRACT(MONTH FROM data_venda) = p_mes
          AND EXTRACT(YEAR FROM data_venda) = p_ano;
          
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        p_comissao := 0;
END;
```

### Suas Tarefas

1. **Análise da Procedure**
   - Documentar todas as regras de negócio
   - Identificar dependências (tabelas, outras procedures)
   - Mapear diferenças Oracle vs PostgreSQL

2. **Criar Wrapper Python**
   - Encapsular chamada ao Oracle
   - Permitir mock para testes
   - Capturar todos os outputs

3. **Implementar em PostgreSQL/Python**
   - Reescrever lógica em Python
   - Usar SQLAlchemy para abstração
   - Manter mesma interface

4. **Criar Suite de Paridade**
   - Gerar dados de teste
   - Comparar resultados Oracle vs PostgreSQL
   - Detectar diferenças de precisão numérica

5. **Implementar Migração Dual-Write**
   - Escrever em ambos bancos simultaneamente
   - Comparar resultados em tempo real
   - Detectar divergências automaticamente

### Entregáveis

- [ ] Documentação das regras de negócio
- [ ] Wrapper Python para Oracle
- [ ] Implementação PostgreSQL/Python
- [ ] Suite de testes de paridade
- [ ] Sistema de dual-write
- [ ] Scripts de migração de dados
- [ ] Plano de cutover

---

## Exercício 4: Projeto Final - CNPJ 2026

### Cenário

Aplicar TUDO que você aprendeu para criar um plano completo de migração
do validador de CNPJ numérico para alfanumérico (2026).

### Requisitos

Use o validador real do repositório `src/cnpj_validator/` e crie:

1. **Documentação Completa**
   - Análise do código legado
   - Regras de negócio documentadas
   - Plano de migração em fases

2. **Suite de Caracterização**
   - Todos os comportamentos documentados
   - Casos de borda identificados
   - Golden Master com 10.000+ casos

3. **Facade de Migração**
   - Strangler Fig Pattern
   - Feature Flags
   - Rollout gradual

4. **Suite de Regressão**
   - 4 níveis (smoke, sanity, core, full)
   - CI/CD configurado
   - Relatórios automatizados

5. **Monitoramento**
   - Métricas de uso
   - Alertas de divergência
   - Dashboard de migração

### Entregáveis

- [ ] Documento de estratégia (Markdown)
- [ ] 50+ testes de caracterização
- [ ] Golden Master em JSON
- [ ] Facade funcional com testes
- [ ] Pipeline CI/CD configurado
- [ ] Script de monitoramento
- [ ] Apresentação do projeto

---

## Critérios de Avaliação

### Para Exercícios 1-3

| Critério | Peso |
|----------|------|
| Cobertura de casos | 25% |
| Qualidade do código | 25% |
| Documentação | 20% |
| Testes passando | 20% |
| Tratamento de erros | 10% |

### Para Projeto Final (Exercício 4)

| Critério | Peso |
|----------|------|
| Completude da solução | 30% |
| Qualidade da documentação | 20% |
| Cobertura de testes | 20% |
| Robustez do facade | 15% |
| CI/CD e monitoramento | 15% |

---

## Dicas Finais

1. **Não subestime o legado**: Sempre há mais complexidade escondida
2. **Documente tudo**: Você vai esquecer por que fez algo em 2 semanas
3. **Teste obsessivamente**: Um bug em produção custa 10x mais que um teste
4. **Rollback rápido**: Sempre tenha um plano B pronto para executar
5. **Métricas são sua amiga**: Se não pode medir, não sabe se está funcionando

**Boa sorte!** 🚀
