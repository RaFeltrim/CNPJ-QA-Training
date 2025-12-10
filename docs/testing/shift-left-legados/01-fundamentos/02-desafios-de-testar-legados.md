# ⚠️ Desafios de Testar Sistemas Legados

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- ✅ Identificar os principais desafios de testar legados
- ✅ Entender por que abordagens tradicionais falham
- ✅ Reconhecer as armadilhas comuns
- ✅ Preparar-se mentalmente para trabalhar com legados

---

## 1. O Grande Problema

### 1.1 A Realidade do QA em Legados

```text
┌─────────────────────────────────────────────────────────────────┐
│                    CENÁRIO TÍPICO                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Gerente: "Precisamos adicionar suporte a CNPJ alfanumérico"    │
│                                                                  │
│  QA: "Ok, deixa eu ver os testes existentes..."                 │
│                                                                  │
│  [Abre o projeto]                                                │
│                                                                  │
│  tests/                                                          │
│  └── (vazio)                                                     │
│                                                                  │
│  QA: "... 😱"                                                    │
│                                                                  │
│  Gerente: "Ah, e precisa estar pronto em 2 semanas."            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Por Que Isso Acontece?

| Fator | Explicação |
|-------|------------|
| **Cultura antiga** | "Testes são perda de tempo" era comum há 15 anos |
| **Pressão de prazo** | "Entrega primeiro, testa depois" |
| **Turnover** | Quem criou não está mais lá |
| **Falta de padrões** | Cada dev fazia do seu jeito |
| **Tecnologia limitada** | Frameworks de teste não existiam ou eram ruins |

---

## 2. Os 7 Desafios Principais

### Desafio #1: Ausência de Testes

**Problema**: Não existe rede de segurança.

```python
# Situação real encontrada em legados:

# arquivo: core/business/validations/cnpj_utils.py
# Linhas: 2,847
# Testes: 0
# Último commit: 2012
# Comentários: 3
```

**Por que é difícil**:
- Qualquer mudança pode quebrar funcionalidades
- Não há como saber se algo parou de funcionar
- O código foi escrito sem pensar em testabilidade

**Pergunta para reflexão**: *Como você testaria uma função de 500 linhas sem documentação?*

---

### Desafio #2: Código Fortemente Acoplado

**Problema**: Tudo depende de tudo.

```python
# Exemplo de código acoplado (difícil de testar)
class ValidadorCNPJ:
    def validar(self, cnpj):
        # Conecta no banco de dados
        db = DatabaseConnection.get_instance()
        
        # Chama serviço externo
        api = ReceitaFederalAPI()
        
        # Usa configuração global
        config = GlobalConfig.load()
        
        # Envia email se inválido
        mailer = EmailService()
        
        # Como testar isso de forma isolada? 🤔
```

**Consequências**:
- Para testar validação, precisa de banco, API, config e email
- Testes são lentos (dependências externas)
- Testes são frágeis (falham por motivos externos)

---

### Desafio #3: Conhecimento Perdido

**Problema**: Ninguém sabe o que o código faz.

```python
# Código real encontrado em sistema legado
def calc_dv(n, t=1):
    """Calcula."""
    s = 0
    m = 2
    for i in range(len(n)-1, -1, -1):
        s += int(n[i]) * m
        m = m + 1 if m < 9 else 2
    r = s % 11
    return 0 if r < 2 else 11 - r if t else r

# Perguntas que surgem:
# - O que é 'n'? (Número? Qual?)
# - O que é 't'? (Tipo? Flag?)
# - Por que 'm' reseta em 9?
# - Por que a lógica muda baseada em 't'?
# - Isso funciona para CNPJ alfanumérico?
```

**Impacto**:
- Leva horas/dias para entender uma função simples
- Alto risco de introduzir bugs ao modificar
- Medo de refatorar

---

### Desafio #4: Efeitos Colaterais Escondidos

**Problema**: Funções fazem mais do que aparentam.

```python
def formatar_cnpj(cnpj):
    """Formata o CNPJ no padrão XX.XXX.XXX/XXXX-XX"""
    
    # Efeito colateral 1: Modifica variável global
    global ultimo_cnpj_formatado
    ultimo_cnpj_formatado = cnpj
    
    # Efeito colateral 2: Grava log no banco
    LogDatabase.insert(f"CNPJ formatado: {cnpj}")
    
    # Efeito colateral 3: Incrementa contador
    MetricsCollector.increment("cnpj_format_count")
    
    # Finalmente faz o que promete...
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
```

**Por que é perigoso**:
- Testar a função pode gravar dados reais
- Efeitos invisíveis podem quebrar outros sistemas
- Difícil reproduzir condições de teste

---

### Desafio #5: Dependências de Ambiente

**Problema**: O código só funciona em produção.

```text
┌─────────────────────────────────────────────────────────────────┐
│  "Funciona na minha máquina!" → "Mas não funciona no teste"     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Dependências típicas de legados:                                │
│                                                                  │
│  ❌ Variáveis de ambiente hardcoded                              │
│  ❌ Caminhos absolutos de arquivos                               │
│  ❌ Conexões diretas com banco de produção                       │
│  ❌ Certificados específicos da máquina                          │
│  ❌ Bibliotecas instaladas globalmente                           │
│  ❌ Configurações no registro do Windows                         │
│  ❌ Dependência de hora/data do sistema                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Exemplo real**:

```python
# Código que só funciona em um servidor específico
import os

def carregar_configuracao():
    # Caminho absoluto de 2008
    return open("C:/Sistemas/ERP/Config/cnpj.ini").read()
    
def conectar_banco():
    # IP hardcoded do servidor de produção
    return connect("192.168.1.100", "usuario_prod", "senha123")
```

---

### Desafio #6: Dados de Teste Inadequados

**Problema**: Não existe massa de dados representativa.

```text
Situação comum:

1. Desenvolvedor cria teste manual:
   - Usa seu próprio CPF/CNPJ
   - Usa dados fake óbvios ("11111111111")
   
2. Anos depois:
   - Dados reais muito diferentes
   - Edge cases nunca testados
   - Volume de dados não simulado
```

**Exemplo com CNPJ**:

```python
# Testes criados em 2010 (antes de pensar em alfanumérico)
CNPJS_TESTE = [
    "11222333000181",  # ✅ Funciona
    "00000000000000",  # ✅ Inválido detectado
    "11111111111111",  # ✅ Inválido detectado
]

# Mas e em 2026?
CNPJS_NOVOS = [
    "ABCDE123000145",  # ❌ Não testado
    "TESTECNP000199",  # ❌ Não testado
    "12345ABC000178",  # ❌ Não testado (misto)
]
```

---

### Desafio #7: Resistência Organizacional

**Problema**: Pessoas resistem a mudanças.

```text
┌─────────────────────────────────────────────────────────────────┐
│  FRASES QUE VOCÊ VAI OUVIR:                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  😰 "Não mexe que está funcionando"                             │
│                                                                  │
│  😤 "Não temos tempo para escrever testes"                      │
│                                                                  │
│  🙄 "Testes são responsabilidade do QA, não dos devs"           │
│                                                                  │
│  😱 "E se os testes encontrarem bugs? Vai atrasar o projeto!"   │
│                                                                  │
│  🤷 "O sistema funciona há 10 anos sem testes, por que mudar?"  │
│                                                                  │
│  💰 "Não temos budget para isso"                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. O Custo de Não Testar

### 3.1 Exemplo Real: Migração de CNPJ

Sem testes adequados, uma migração de CNPJ pode resultar em:

| Problema | Impacto | Custo Estimado |
|----------|---------|----------------|
| Clientes não conseguem se cadastrar | Perda de vendas | R$ 500k/dia |
| Notas fiscais rejeitadas | Multas da Receita | R$ 50k/ocorrência |
| Integrações bancárias falham | Operações paradas | R$ 200k/dia |
| Rollback emergencial | Horas extras, stress | R$ 100k |
| Dano à reputação | Clientes perdidos | Incalculável |

### 3.2 A Conta

```text
Custo de CRIAR testes antes da migração:
- 2 semanas de trabalho
- R$ 30.000 (equipe)

Custo de NÃO TER testes (se algo quebrar):
- 1 dia de sistema fora: R$ 500.000+
- Multas e processos: R$ 200.000+
- Horas extras e stress: R$ 50.000+
- Total: R$ 750.000+

ROI de testes em legados: 25x (2500%)
```

---

## 4. Mas Há Esperança!

### 4.1 A Boa Notícia

Existem **técnicas específicas** para testar sistemas legados com segurança:

| Técnica | Descrição | Quando Usar |
|---------|-----------|-------------|
| **Characterization Tests** | Documenta comportamento atual | Antes de qualquer mudança |
| **Golden Master** | Compara saídas antes/depois | Transformações de dados |
| **Strangler Fig** | Substitui gradualmente | Migrações grandes |
| **Feature Flags** | Liga/desliga funcionalidades | Deploy gradual |

### 4.2 O Caminho

```text
┌─────────────────────────────────────────────────────────────────┐
│                 DE                    PARA                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  "Não temos testes"     →    "Temos testes de caracterização"   │
│                                                                  │
│  "Ninguém sabe o que    →    "Documentamos o comportamento      │
│   faz"                        esperado"                          │
│                                                                  │
│  "Medo de mexer"        →    "Mudamos com confiança"            │
│                                                                  │
│  "Deploy é roleta"      →    "Deploy é rotina"                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Exercício Prático

### 5.1 Análise de Risco

Para o sistema legado de CNPJ mostrado anteriormente:

1. Liste **3 cenários que podem quebrar** se mudarmos a validação
2. Para cada cenário, estime o **impacto no negócio**
3. Ordene por **prioridade de teste**

**Dica**: Pense em cadastros, integrações, relatórios, NFe...

### 5.2 Gabarito Mental

```text
Cenário 1: Cadastro de novo cliente
- Impacto: Cliente não consegue comprar
- Prioridade: ALTA

Cenário 2: Emissão de NF-e
- Impacto: Empresa não pode vender
- Prioridade: CRÍTICA

Cenário 3: Relatório mensal
- Impacto: Informação gerencial atrasada
- Prioridade: MÉDIA
```

---

## 6. Resumo

### 6.1 Os 7 Desafios

1. ❌ Ausência de testes existentes
2. ❌ Código fortemente acoplado
3. ❌ Conhecimento perdido
4. ❌ Efeitos colaterais escondidos
5. ❌ Dependências de ambiente
6. ❌ Dados de teste inadequados
7. ❌ Resistência organizacional

### 6.2 A Mensagem Principal

> **Testar legados é difícil, mas não impossível.**
> 
> O segredo é usar as técnicas certas e começar pequeno.
> 
> Um teste de caracterização hoje pode salvar seu emprego amanhã.

---

## 📚 Referências

- Feathers, Michael. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- Meszaros, Gerard. *xUnit Test Patterns*. Addison-Wesley, 2007.

---

**Próximo**: [03-shift-left-em-contexto-legado.md](03-shift-left-em-contexto-legado.md)
