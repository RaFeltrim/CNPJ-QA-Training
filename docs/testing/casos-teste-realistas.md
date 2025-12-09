# 5. Casos de Teste Realistas - Validação de CNPJ

## Documento 5: Cenários de Teste Práticos e Massa de Dados

---

## 1. INTRODUÇÃO

Este documento fornece uma coletânea completa de **casos de teste realistas** para validação de CNPJ, organizados por categoria e complexidade. É uma ferramenta essencial para QA que precisam:

- Planejar testes de validação de CNPJ
- Criar massa de dados para automação
- Validar implementações de código
- Documentar cenários de edge cases
- Treinar equipes em validação de documentos

**Público-Alvo**: QA Júnior a Sênior, Desenvolvedores, Analistas de Negócio

---

## 2. ORGANIZAÇÃO DOS CASOS DE TESTE

### 2.1 Estrutura de Cada Caso

Cada caso de teste contém:
- **ID do Teste**: Identificador único
- **Categoria**: Tipo de validação
- **Cenário**: Descrição do que está sendo testado
- **Entrada**: CNPJ fornecido para teste
- **Resultado Esperado**: Válido ou Inválido
- **Motivo**: Explicação técnica do resultado
- **Prioridade**: Alta, Média, Baixa
- **Tags**: Para filtros e busca

### 2.2 Categorias de Teste

```
Casos de Teste
├── Formato Válido (Happy Path)
├── Formato Inválido (Validação de Estrutura)
├── Dígitos Verificadores
├── CNPJs Especiais e Edge Cases
├── Formato Alfanumérico (Futuro)
├── Integração com API da Receita
└── Testes de Performance e Carga
```

---

## 3. CASOS DE TESTE - FORMATO VÁLIDO (Happy Path)

### CT-001: CNPJ Válido - Formato Padrão
**Categoria**: Formato Válido  
**Prioridade**: Alta  
**Tags**: `happy-path`, `numerico`, `validacao-basica`

**Cenário**: Validar CNPJ com estrutura correta e DVs válidos

**Entrada**: `11.222.333/0001-81`

**Resultado Esperado**: **VÁLIDO**

**Motivo**: 
- Raiz: 11.222.333 (formato correto)
- Ordem: 0001 (matriz)
- DVs: 81 (calculados corretamente)

**Evidências de Cálculo**:
```
Primeiro DV: 8
Segundo DV: 1
CNPJ: 11.222.333/0001-81 (verificado)
```

---

### CT-002: CNPJ Válido - Filial
**Categoria**: Formato Válido  
**Prioridade**: Alta  
**Tags**: `happy-path`, `filial`, `numerico`

**Cenário**: Validar CNPJ de filial (ordem > 0001)

**Entrada**: `12.345.678/0002-95`

**Resultado Esperado**: **VÁLIDO**

**Motivo**:
- Mesma raiz da matriz (12.345.678)
- Ordem: 0002 (primeira filial)
- DVs recalculados para esta ordem específica

---

### CT-003: CNPJ Válido - Sem Formatação
**Categoria**: Formato Válido  
**Prioridade**: Alta  
**Tags**: `happy-path`, `sem-formatacao`, `numerico`

**Cenário**: Validar CNPJ fornecido sem pontos, barras e hífen

**Entrada**: `11222333000181`

**Resultado Esperado**: **VÁLIDO**

**Motivo**:
- CNPJ deve ser validado mesmo sem formatação
- Corresponde ao CNPJ 11.222.333/0001-81

**Observação**: Sistema deve aceitar ambos formatos (com e sem máscara)

---

### CT-004: CNPJ Válido - Múltiplas Filiais
**Categoria**: Formato Válido  
**Prioridade**: Média  
**Tags**: `happy-path`, `filiais-multiplas`, `numerico`

**Cenário**: Validar CNPJs de uma empresa com várias filiais

**Entradas**:
- Matriz: `98.765.432/0001-79`
- Filial 1: `98.765.432/0002-59`
- Filial 2: `98.765.432/0003-39`
- Filial 100: `98.765.432/0100-09`

**Resultado Esperado**: **VÁLIDO** Todos **VÁLIDOS**

**Motivo**:
- Raiz idêntica (98.765.432)
- Ordens sequenciais com DVs recalculados
- Até 9999 filiais possíveis por raiz

---

### CT-005: CNPJ Válido - Grandes Empresas Reais
**Categoria**: Formato Válido  
**Prioridade**: Média  
**Tags**: `happy-path`, `empresas-reais`, `numerico`

**Cenário**: Validar CNPJs de grandes empresas brasileiras (dados públicos)

**Entradas** (exemplos fictícios, estrutura similar à realidade):
- Banco do Brasil: `00.000.000/0001-91`
- Petrobras: `33.000.167/0001-01`
- Vale: `33.592.510/0001-54`

**Resultado Esperado**: **VÁLIDO** **VÁLIDOS**

**Observação**: Use CNPJs reais disponíveis em sites oficiais para testes mais realistas

---

## 4. CASOS DE TESTE - FORMATO INVÁLIDO (Validação de Estrutura)

### CT-006: CNPJ com Menos de 14 Caracteres
**Categoria**: Formato Inválido  
**Prioridade**: Alta  
**Tags**: `error`, `estrutura`, `tamanho-invalido`

**Cenário**: Rejeitar CNPJ com quantidade insuficiente de dígitos

**Entradas**:
- `11.222.333/0001-8` (13 dígitos)
- `1122233300018` (13 dígitos sem formatação)
- `11.222.333/001-81` (12 dígitos)

**Resultado Esperado**: **INVÁLIDO**

**Motivo**: CNPJ deve ter exatamente 14 caracteres numéricos

**Mensagem Sugerida**: "CNPJ incompleto. São necessários 14 dígitos."

---

### CT-007: CNPJ com Mais de 14 Caracteres
**Categoria**: Formato Inválido  
**Prioridade**: Alta  
**Tags**: `error`, `estrutura`, `tamanho-invalido`

**Cenário**: Rejeitar CNPJ com dígitos extras

**Entradas**:
- `11.222.333/0001-811` (15 dígitos)
- `112223330001811` (15 dígitos sem formatação)

**Resultado Esperado**: **INVÁLIDO**

**Motivo**: CNPJ excede os 14 caracteres permitidos

**Mensagem Sugerida**: "CNPJ inválido. Deve conter exatamente 14 dígitos."

---

### CT-008: CNPJ com Caracteres Não Numéricos
**Categoria**: Formato Inválido  
**Prioridade**: Alta  
**Tags**: `error`, `estrutura`, `caracteres-invalidos`

**Cenário**: Rejeitar CNPJ contendo letras ou símbolos (formato numérico)

**Entradas**:
- `AB.222.333/0001-81` (letras)
- `11.222.333/000A-81` (letra no meio)
- `11.222.333/0001-8#` (símbolo especial)
- `11.222.333/0001-8 ` (espaço no final)

**Resultado Esperado**: **INVÁLIDO**

**Motivo**: CNPJ numérico aceita apenas dígitos 0-9 (até julho/2026)

**Mensagem Sugerida**: "CNPJ contém caracteres inválidos. Use apenas números."

---

### CT-009: CNPJ com Formatação Incorreta
**Categoria**: Formato Inválido  
**Prioridade**: Média  
**Tags**: `error`, `estrutura`, `formatacao-incorreta`

**Cenário**: Rejeitar ou normalizar CNPJs com formatação errada

**Entradas**:
- `11222333/0001-81` (faltam pontos)
- `11.222.333-0001/81` (separadores trocados)
- `11-222-333/0001-81` (hífens no lugar de pontos)

**Resultado Esperado**: 
- **Opção 1**: **INVÁLIDO** (validação rígida)
- **Opção 2**: **VÁLIDO** após normalização (remover formatação)

**Recomendação**: Implementar normalização automática antes da validação

---

### CT-010: CNPJ Vazio ou Nulo
**Categoria**: Formato Inválido  
**Prioridade**: Alta  
**Tags**: `error`, `estrutura`, `campo-vazio`

**Cenário**: Rejeitar entradas vazias, nulas ou apenas espaços

**Entradas**:
- `""` (string vazia)
- `null`
- `undefined`
- `   ` (apenas espaços)

**Resultado Esperado**: **INVÁLIDO**

**Mensagem Sugerida**: "CNPJ não pode estar vazio."

---

## 5. CASOS DE TESTE - DÍGITOS VERIFICADORES

### CT-011: CNPJ com Primeiro DV Incorreto
**Categoria**: Dígitos Verificadores  
**Prioridade**: Alta  
**Tags**: `error`, `dv`, `primeiro-dv-invalido`

**Cenário**: Rejeitar CNPJ onde apenas o primeiro DV está errado

**Entrada**: `11.222.333/0001-91` (correto seria -81)

**Resultado Esperado**: **INVÁLIDO**

**Motivo**:
- Primeiro DV correto: 8
- Primeiro DV fornecido: 9
- Segundo DV correto: 1

**Mensagem Sugerida**: "Dígito verificador inválido."

---

### CT-012: CNPJ com Segundo DV Incorreto
**Categoria**: Dígitos Verificadores  
**Prioridade**: Alta  
**Tags**: `error`, `dv`, `segundo-dv-invalido`

**Cenário**: Rejeitar CNPJ onde apenas o segundo DV está errado

**Entrada**: `11.222.333/0001-82` (correto seria -81)

**Resultado Esperado**: **INVÁLIDO**

**Motivo**:
- Primeiro DV correto: 8
- Segundo DV correto: 1
- Segundo DV fornecido: 2

**Mensagem Sugerida**: "Dígito verificador inválido."

---

### CT-013: CNPJ com Ambos DVs Incorretos
**Categoria**: Dígitos Verificadores  
**Prioridade**: Alta  
**Tags**: `error`, `dv`, `ambos-dvs-invalidos`

**Cenário**: Rejeitar CNPJ onde ambos os DVs estão errados

**Entrada**: `11.222.333/0001-00` (correto seria -81)

**Resultado Esperado**: **INVÁLIDO**

**Motivo**:
- DVs corretos: 81
- DVs fornecidos: 00

**Mensagem Sugerida**: "Dígitos verificadores inválidos."

---

### CT-014: CNPJ com DV Resultante de Resto 0
**Categoria**: Dígitos Verificadores  
**Prioridade**: Média  
**Tags**: `edge-case`, `dv`, `resto-zero`

**Cenário**: Validar CNPJ cujo cálculo resulta em resto 0 ou 1

**Entrada**: `00.000.000/0001-91` (primeiro DV com resto 0)

**Resultado Esperado**: **VÁLIDO**

**Motivo**:
- Quando resto da divisão = 0 ou 1, DV = 0
- Regra especial do algoritmo Módulo 11

**Observação**: Teste essencial para garantir que a regra está implementada

---

### CT-015: CNPJ com Transposição de Dígitos
**Categoria**: Dígitos Verificadores  
**Prioridade**: Média  
**Tags**: `error`, `dv`, `transposicao`

**Cenário**: Detectar erro de digitação (troca de posição de dígitos)

**Entrada**: `11.222.333/0010-81` (correto: /0001-)

**Resultado Esperado**: **INVÁLIDO**

**Motivo**:
- Ordem alterada de 0001 para 0010
- DVs não correspondem à nova ordem
- Algoritmo deve detectar inconsistência

---

## 6. CASOS DE TESTE - CNPJs ESPECIAIS E EDGE CASES

### CT-016: CNPJ com Todos Dígitos Iguais
**Categoria**: Edge Cases  
**Prioridade**: Alta  
**Tags**: `edge-case`, `digitos-repetidos`, `cnpj-invalido`

**Cenário**: Rejeitar CNPJs com todos os dígitos idênticos

**Entradas**:
- `00.000.000/0000-00`
- `11.111.111/1111-11`
- `22.222.222/2222-22`
- `99.999.999/9999-99`

**Resultado Esperado**: **INVÁLIDO**

**Motivo**:
- CNPJs com dígitos repetidos não são emitidos pela Receita
- São considerados inválidos por padrão
- Mesmo que o cálculo de DV seja matematicamente correto

**Observação**: Validação adicional além do algoritmo de DV

---

### CT-017: CNPJ com Sequência Numérica
**Categoria**: Edge Cases  
**Prioridade**: Média  
**Tags**: `edge-case`, `sequencia`, `validacao-adicional`

**Cenário**: Detectar padrões suspeitos (sequências crescentes/decrescentes)

**Entradas**:
- `12.345.678/9012-XX` (sequência crescente)
- `98.765.432/1098-XX` (sequência decrescente)

**Resultado Esperado**: 
- **Opção 1**: **INVÁLIDO** (regra de negócio)
- **Opção 2**: **VÁLIDO** se DVs corretos (apenas validação matemática)

**Recomendação**: Implementar como regra de negócio adicional (flag de alerta)

---

### CT-018: CNPJ de Matriz (Ordem 0001)
**Categoria**: Edge Cases  
**Prioridade**: Média  
**Tags**: `edge-case`, `matriz`, `ordem-especial`

**Cenário**: Validar que ordem 0001 sempre indica matriz

**Entrada**: `11.222.333/0001-81`

**Resultado Esperado**: **VÁLIDO** + Flag "É Matriz"

**Observação**: Útil para lógica de negócio que diferencia matriz de filial

---

### CT-019: CNPJ com Ordem 9999 (Última Filial)
**Categoria**: Edge Cases  
**Prioridade**: Baixa  
**Tags**: `edge-case`, `ultima-filial`, `ordem-maxima`

**Cenário**: Validar o limite máximo de filiais (9999)

**Entrada**: `11.222.333/9999-XX` (calcular DVs)

**Resultado Esperado**: **VÁLIDO** (se DVs corretos)

**Motivo**: Sistema deve suportar até 9999 filiais por raiz

---

### CT-020: CNPJ com Raiz 00.000.000
**Categoria**: Edge Cases  
**Prioridade**: Média  
**Tags**: `edge-case`, `raiz-zero`, `caso-especial`

**Cenário**: Validar CNPJ com raiz composta por zeros

**Entrada**: `00.000.000/0001-91`

**Resultado Esperado**: 
- **Matematicamente**: **VÁLIDO** (se DVs corretos)
- **Receita Federal**: **INVÁLIDO** (não emitidos)

**Recomendação**: Implementar validação de negócio adicional

---

## 7. CASOS DE TESTE - FORMATO ALFANUMÉRICO (Futuro - 2026+)

### CT-021: CNPJ Alfanumérico Válido - Padrão
**Categoria**: Formato Alfanumérico  
**Prioridade**: Alta  
**Tags**: `alfanumerico`, `futuro`, `happy-path`

**Cenário**: Validar CNPJ no novo formato com letras e números

**Entrada**: `12.ABC.345/01DE-35`

**Resultado Esperado**: **VÁLIDO** (após jul/2026)

**Motivo**:
- Raiz: 12.ABC.345 (alfanumérico)
- Ordem: 01DE (alfanumérico)
- DVs: 35 (calculados com conversão ASCII)

**Cálculo com ASCII**:
```
Caractere:  1  2  A  B  C  3  4  5  0  1  D  E
Valor:      1  2  17 18 19 3  4  5  0  1  20 21
Primeiro DV: 3
Segundo DV: 5
CNPJ: 12.ABC.345/01DE-35 (verificado)
```

---

### CT-022: CNPJ Alfanumérico com Letras Minúsculas
**Categoria**: Formato Alfanumérico  
**Prioridade**: Média  
**Tags**: `alfanumerico`, `normalizacao`, `case-sensitivity`

**Cenário**: Validar tratamento de letras minúsculas

**Entrada**: `12.abc.345/01de-35` (minúsculas)

**Resultado Esperado**: 
- **Opção 1**: **VÁLIDO** após normalizar para maiúsculas
- **Opção 2**: **INVÁLIDO** (exigir maiúsculas)

**Recomendação**: Implementar conversão automática para UPPERCASE antes da validação

---

### CT-023: CNPJ Alfanumérico com Caracteres Especiais
**Categoria**: Formato Alfanumérico  
**Prioridade**: Alta  
**Tags**: `alfanumerico`, `error`, `caracteres-invalidos`

**Cenário**: Rejeitar CNPJs alfanuméricos com caracteres não permitidos

**Entradas**:
- `12.A@C.345/01DE-35` (@ não permitido)
- `12.ÁBC.345/01DE-35` (acentuação não permitida)
- `12.A C.345/01DE-35` (espaço não permitido)

**Resultado Esperado**: **INVÁLIDO**

**Motivo**: Apenas A-Z e 0-9 são permitidos na raiz e ordem

**Mensagem Sugerida**: "CNPJ alfanumérico contém caracteres inválidos. Use apenas A-Z e 0-9."

---

### CT-024: CNPJ Alfanumérico com DVs Alfanuméricos
**Categoria**: Formato Alfanumérico  
**Prioridade**: Alta  
**Tags**: `alfanumerico`, `error`, `dv-incorreto`

**Cenário**: Rejeitar CNPJs onde os DVs contêm letras

**Entrada**: `12.ABC.345/01DE-AB` (DVs com letras)

**Resultado Esperado**: **INVÁLIDO**

**Motivo**: Segundo a IN 2.229/2024, os DVs permanecem **numéricos** mesmo no formato alfanumérico

**Mensagem Sugerida**: "Dígitos verificadores devem ser numéricos (0-9)."

---

### CT-025: Coexistência de Formatos (Numérico + Alfanumérico)
**Categoria**: Formato Alfanumérico  
**Prioridade**: Alta  
**Tags**: `alfanumerico`, `coexistencia`, `transicao`

**Cenário**: Validar que ambos os formatos são aceitos simultaneamente

**Entradas**:
- `11.222.333/0001-81` (numérico - empresa antiga)
- `12.ABC.345/01DE-35` (alfanumérico - empresa nova)

**Resultado Esperado**: **VÁLIDO** Ambos **VÁLIDOS**

**Motivo**: Período de transição (2026-2028+) exige suporte a ambos formatos

**Observação**: Sistema deve detectar automaticamente o formato e aplicar validação apropriada

---

## 8. CASOS DE TESTE - INTEGRAÇÃO COM API DA RECEITA

### CT-026: Consulta de CNPJ Válido e Ativo
**Categoria**: Integração API  
**Prioridade**: Alta  
**Tags**: `api`, `receita-federal`, `happy-path`

**Cenário**: Consultar CNPJ válido na base da Receita Federal

**Entrada**: CNPJ válido de empresa ativa

**Resultado Esperado**: 
- **VÁLIDO** CNPJ existe na base
- Status: ATIVA
- Retorna: Razão social, endereço, CNAE, data de abertura

**Observação**: Requer integração com API oficial ou web scraping (com captcha)

---

### CT-027: Consulta de CNPJ Válido mas Inativo
**Categoria**: Integração API  
**Prioridade**: Alta  
**Tags**: `api`, `receita-federal`, `empresa-inativa`

**Cenário**: Consultar CNPJ de empresa baixada/suspensa

**Entrada**: CNPJ válido de empresa inativa

**Resultado Esperado**:
- **VÁLIDO** CNPJ existe na base
- Status: BAIXADA / SUSPENSA / INAPTA
- Retorna: Data de encerramento, motivo

**Observação**: Importante para regras de negócio que exigem empresa ativa

---

### CT-028: Consulta de CNPJ Inexistente
**Categoria**: Integração API  
**Prioridade**: Média  
**Tags**: `api`, `receita-federal`, `cnpj-inexistente`

**Cenário**: Consultar CNPJ com DVs válidos mas não cadastrado

**Entrada**: CNPJ matematicamente válido mas não emitido

**Resultado Esperado**:
- ⚠️ CNPJ não encontrado na base da Receita
- Status: INEXISTENTE

**Motivo**: Dígitos verificadores corretos não garantem existência real

**Mensagem Sugerida**: "CNPJ válido matematicamente, mas não cadastrado na Receita Federal."

---

### CT-029: Timeout na Consulta à API
**Categoria**: Integração API  
**Prioridade**: Média  
**Tags**: `api`, `timeout`, `erro-rede`

**Cenário**: Tratar falhas de conexão ou timeout

**Entrada**: Qualquer CNPJ válido

**Resultado Esperado**:
- ⚠️ Erro de timeout
- Mensagem amigável ao usuário
- Retry automático (opcional)

**Mensagem Sugerida**: "Não foi possível consultar a Receita Federal. Tente novamente."

---

### CT-030: Rate Limiting da API
**Categoria**: Integração API  
**Prioridade**: Alta  
**Tags**: `api`, `rate-limit`, `throttling`

**Cenário**: Tratar limite de requisições por minuto

**Entrada**: Múltiplas consultas sequenciais rápidas

**Resultado Esperado**:
- ⚠️ HTTP 429 (Too Many Requests)
- Implementar backoff exponencial
- Queue de requisições

**Recomendação**: Respeitar limites da API para evitar bloqueio

---

## 9. CASOS DE TESTE - PERFORMANCE E CARGA

### CT-031: Validação de 1.000 CNPJs Sequenciais
**Categoria**: Performance  
**Prioridade**: Média  
**Tags**: `performance`, `carga`, `batch`

**Cenário**: Validar lote de CNPJs em tempo aceitável

**Entrada**: Lista com 1.000 CNPJs diversos

**Resultado Esperado**:
- Tempo total: < 5 segundos
- Tempo médio por CNPJ: < 5ms
- Sem perda de precisão

**Métrica**: Throughput > 200 CNPJs/segundo

---

### CT-032: Validação Concorrente (100 Threads)
**Categoria**: Performance  
**Prioridade**: Alta  
**Tags**: `performance`, `concorrencia`, `stress`

**Cenário**: Validar comportamento sob carga concorrente

**Entrada**: 100 threads validando CNPJs simultaneamente

**Resultado Esperado**:
- Sistema permanece responsivo
- Sem race conditions
- Sem memory leaks
- CPU < 80%

---

### CT-033: Validação com Entrada Extremamente Grande
**Categoria**: Performance  
**Prioridade**: Baixa  
**Tags**: `performance`, `edge-case`, `entrada-grande`

**Cenário**: Testar comportamento com string muito grande

**Entrada**: String com 10.000 caracteres (simulando ataque)

**Resultado Esperado**:
- **INVÁLIDO** INVÁLIDO detectado rapidamente (< 10ms)
- Sem crash ou travamento
- Memória não dispara

**Recomendação**: Validar tamanho antes de processar

---

## 10. MATRIZ DE PRIORIZAÇÃO

### 10.1 Testes Obrigatórios (P0 - Alta Prioridade)

| ID | Caso de Teste | Categoria | Motivo |
|----|---------------|-----------|--------|
| CT-001 | CNPJ válido padrão | Happy Path | Caso mais comum |
| CT-006 | Menos de 14 dígitos | Estrutura | Erro frequente de usuários |
| CT-008 | Caracteres não numéricos | Estrutura | Erro de digitação comum |
| CT-010 | Campo vazio/nulo | Estrutura | Validação básica obrigatória |
| CT-011 | Primeiro DV incorreto | Dígitos Verificadores | Essencial para algoritmo |
| CT-013 | Ambos DVs incorretos | Dígitos Verificadores | Validação completa |
| CT-016 | Dígitos todos iguais | Edge Cases | Regra de negócio crítica |
| CT-021 | CNPJ alfanumérico válido | Alfanumérico | Preparação para 2026 |
| CT-024 | DVs alfanuméricos (erro) | Alfanumérico | Regra específica da IN |

---

### 10.2 Testes Importantes (P1 - Média Prioridade)

| ID | Caso de Teste | Categoria | Motivo |
|----|---------------|-----------|--------|
| CT-002 | CNPJ de filial | Happy Path | Cenário comum em empresas |
| CT-004 | Múltiplas filiais | Happy Path | Validação de negócio |
| CT-009 | Formatação incorreta | Estrutura | Melhora UX com normalização |
| CT-014 | DV com resto 0 | Dígitos Verificadores | Edge case do algoritmo |
| CT-017 | Sequência numérica | Edge Cases | Detecção de fraude |
| CT-022 | Letras minúsculas (alfa) | Alfanumérico | Tolerância de entrada |
| CT-027 | CNPJ inativo | Integração API | Regra de negócio comum |

---

### 10.3 Testes Opcionais (P2 - Baixa Prioridade)

| ID | Caso de Teste | Categoria | Motivo |
|----|---------------|-----------|--------|
| CT-019 | Ordem 9999 | Edge Cases | Cenário muito raro |
| CT-020 | Raiz 00.000.000 | Edge Cases | Quase nunca ocorre |
| CT-033 | Entrada extremamente grande | Performance | Proteção contra ataques |

---

## 11. MASSA DE DADOS PARA TESTES

### 11.1 CNPJs Numéricos Válidos (Para Automação)

```
11.222.333/0001-81
12.345.678/0001-95
98.765.432/0001-79
11.111.111/0001-18
99.999.999/9999-04
00.000.000/0001-91
34.028.316/0001-03
60.746.948/0001-12
11.222.333/0002-62
12.345.678/0002-76
```

---

### 11.2 CNPJs Inválidos (Para Testes Negativos)

```
11.222.333/0001-00  (DVs incorretos)
11.111.111/1111-11  (Todos dígitos iguais)
12.345.678/0001-99  (Primeiro DV errado)
98.765.432/0001-70  (Segundo DV errado)
1234567800019      (Apenas 13 dígitos)
AB.222.333/0001-81  (Contém letras - formato numérico)
12.345.678/0001-8   (Faltam dígitos)
12.345.678/0001-811 (Dígitos extras)
```

---

### 11.3 CNPJs Alfanuméricos Válidos (2026+)

```
12.ABC.345/01DE-35
A1.B2C.3D4/E5F6-72
99.ZZZ.999/ABCD-18
00.AAA.000/0001-05
1A.2B3.C4D/5E6F-49
```

---

### 11.4 CNPJs Alfanuméricos Inválidos (2026+)

```
12.@BC.345/01DE-35  (Caractere especial @)
12.ÁBC.345/01DE-35  (Acentuação)
12.ABC.345/01DE-AB  (DVs alfanuméricos - erro)
12.abc.345/01de-35  (Minúsculas - depende da implementação)
1A.2B3.C4D/5E6F-00  (DVs incorretos)
```

---

## 12. ESTRATÉGIA DE COBERTURA DE TESTES

### 12.1 Pirâmide de Testes para Validação de CNPJ

```
              /\
             /  \
            / E2E\    5% - Testes de Interface (CT-026 a CT-030)
           /______\
          /        \
         /Integration\ 15% - Testes de API (CT-026 a CT-030)
        /____________\
       /              \
      /  Unit Tests    \  80% - Testes Unitários (CT-001 a CT-025)
     /__________________\
```

**Distribuição Recomendada**:
- **80% Testes Unitários**: Validação de algoritmo, DVs, formatos
- **15% Testes de Integração**: API da Receita, banco de dados
- **5% Testes E2E**: Interface web, fluxos completos

---

### 12.2 Cobertura por Categoria

| Categoria | Casos de Teste | % Cobertura Mínima |
|-----------|----------------|--------------------|
| Happy Path | CT-001 a CT-005 | 100% |
| Estrutura Inválida | CT-006 a CT-010 | 100% |
| Dígitos Verificadores | CT-011 a CT-015 | 100% |
| Edge Cases | CT-016 a CT-020 | 80% |
| Alfanumérico | CT-021 a CT-025 | 100% (após jul/2026) |
| Integração API | CT-026 a CT-030 | 70% |
| Performance | CT-031 a CT-033 | 50% |

---

## 13. EXEMPLO DE PLANO DE TESTE COMPLETO

### 13.1 Objetivo
Validar implementação de algoritmo de validação de CNPJ (numérico e alfanumérico)

### 13.2 Escopo
- **VÁLIDO** Validação de estrutura (14 caracteres)
- **VÁLIDO** Cálculo de dígitos verificadores (Módulo 11)
- **VÁLIDO** Conversão ASCII (formato alfanumérico)
- **VÁLIDO** Normalização de entrada (remover formatação)
- **VÁLIDO** Validação de caracteres permitidos
- **VÁLIDO** Detecção de CNPJs inválidos (todos dígitos iguais)

### 13.3 Fora de Escopo
- **INVÁLIDO** Consulta real à Receita Federal (mock)
- **INVÁLIDO** Validação de status da empresa (ativa/inativa)
- **INVÁLIDO** Armazenamento de dados (LGPD)

### 13.4 Ambiente de Teste
- **Sistema Operacional**: Windows 11, Ubuntu 22.04, macOS 13+
- **Linguagem**: TypeScript 5.x
- **Framework de Testes**: Jest 29.x
- **Cobertura Mínima**: 95%

### 13.5 Critérios de Aceite
- **VÁLIDO** Todos os casos de teste P0 (alta prioridade) passando
- **VÁLIDO** 90%+ dos casos P1 (média prioridade) passando
- **VÁLIDO** Cobertura de código > 95%
- **VÁLIDO** Performance: validação < 5ms por CNPJ
- **VÁLIDO** Sem falsos positivos ou negativos

### 13.6 Riscos
- ⚠️ API da Receita pode estar indisponível (mitigar com mock)
- ⚠️ Formato alfanumérico ainda não está ativo (testar com dados fictícios)
- ⚠️ Captcha pode bloquear consultas automatizadas

---

## 14. AUTOMAÇÃO DE CASOS DE TESTE

### 14.1 Exemplo em TypeScript (Jest)

```typescript
// cnpj.validator.spec.ts
describe('Validação de CNPJ', () => {
  
  // CT-001: CNPJ válido padrão
  test('CT-001: Deve validar CNPJ numérico válido', () => {
    const cnpj = '11.222.333/0001-81';
    const resultado = validarCNPJ(cnpj);
    expect(resultado.valido).toBe(true);
  });
  
  // CT-006: Menos de 14 dígitos
  test('CT-006: Deve rejeitar CNPJ com menos de 14 dígitos', () => {
    const cnpj = '11.222.333/0001-8';
    const resultado = validarCNPJ(cnpj);
    expect(resultado.valido).toBe(false);
    expect(resultado.erro).toContain('incompleto');
  });
  
  // CT-011: Primeiro DV incorreto
  test('CT-011: Deve rejeitar CNPJ com primeiro DV incorreto', () => {
    const cnpj = '11.222.333/0001-91';
    const resultado = validarCNPJ(cnpj);
    expect(resultado.valido).toBe(false);
    expect(resultado.erro).toContain('verificador');
  });
  
  // CT-016: Todos dígitos iguais
  test('CT-016: Deve rejeitar CNPJ com todos dígitos iguais', () => {
    const cnpjs = [
      '00.000.000/0000-00',
      '11.111.111/1111-11',
      '99.999.999/9999-99'
    ];
    
    cnpjs.forEach(cnpj => {
      const resultado = validarCNPJ(cnpj);
      expect(resultado.valido).toBe(false);
      expect(resultado.erro).toContain('dígitos repetidos');
    });
  });
  
  // CT-021: CNPJ alfanumérico válido
  test('CT-021: Deve validar CNPJ alfanumérico válido', () => {
    const cnpj = '12.ABC.345/01DE-35';
    const resultado = validarCNPJ(cnpj, { formato: 'alfanumerico' });
    expect(resultado.valido).toBe(true);
  });
  
});
```

---

### 14.2 Exemplo em Robot Framework (BDD)

```robot
*** Settings ***
Library    CNPJValidator

*** Test Cases ***
CT-001 Validar CNPJ Numérico Válido
    ${cnpj}=    Set Variable    11.222.333/0001-81
    ${resultado}=    Validar CNPJ    ${cnpj}
    Should Be True    ${resultado['valido']}

CT-006 Rejeitar CNPJ com Menos de 14 Dígitos
    ${cnpj}=    Set Variable    11.222.333/0001-8
    ${resultado}=    Validar CNPJ    ${cnpj}
    Should Be False    ${resultado['valido']}
    Should Contain    ${resultado['erro']}    incompleto

CT-016 Rejeitar Todos Dígitos Iguais
    @{cnpjs}=    Create List
    ...    00.000.000/0000-00
    ...    11.111.111/1111-11
    ...    99.999.999/9999-99
    
    FOR    ${cnpj}    IN    @{cnpjs}
        ${resultado}=    Validar CNPJ    ${cnpj}
        Should Be False    ${resultado['valido']}
    END
```

---

## 15. CHECKLIST DE VALIDAÇÃO

### Para QA: Use Este Checklist ao Testar

#### Validação Básica
- [ ] CNPJ tem exatamente 14 caracteres (sem formatação)?
- [ ] Todos os caracteres são válidos (0-9 para numérico, A-Z e 0-9 para alfanumérico)?
- [ ] Dígitos verificadores são numéricos?
- [ ] Sistema aceita entrada sem formatação (pontos, barra, hífen)?

#### Validação de Dígitos Verificadores
- [ ] Primeiro DV está correto?
- [ ] Segundo DV está correto?
- [ ] Regra de resto 0 ou 1 está implementada?
- [ ] Conversão ASCII funciona corretamente (formato alfanumérico)?

#### Validações de Negócio
- [ ] CNPJs com todos dígitos iguais são rejeitados?
- [ ] Sistema diferencia matriz (0001) de filiais?
- [ ] Sistema suporta ambos formatos (numérico e alfanumérico)?

#### Validações de UX
- [ ] Mensagens de erro são claras e específicas?
- [ ] Feedback visual ((verificado) válido / ✗ inválido) está visível?
- [ ] Máscara de entrada funciona corretamente?
- [ ] Campo não aceita mais de 14 caracteres (sem formatação)?

#### Performance
- [ ] Validação de 1 CNPJ leva < 10ms?
- [ ] Validação de 1000 CNPJs leva < 10s?
- [ ] Sistema não trava com entrada muito grande?

---

## 16. REFERÊNCIAS E RECURSOS

### Documentação Oficial
- [Receita Federal - Consulta CNPJ](https://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp)
- [Instrução Normativa RFB nº 2.229/2024](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/cnpj)
- [IN RFB nº 2.119/2022](https://www.gov.br/receitafederal/pt-br)

### Ferramentas Úteis
- [Gerador de CNPJ Válido](https://www.4devs.com.br/gerador_de_cnpj) (para massa de testes)
- [Calculadora de DV Online](https://www.geradorcnpj.com/algoritmo_do_cnpj.htm)
- [Tabela ASCII Completa](https://www.asciitable.com/)

### Frameworks de Teste
- **Jest**: Framework de testes unitários JavaScript/TypeScript
- **Cypress**: Testes E2E para aplicações web
- **Robot Framework**: Automação de testes BDD
- **k6**: Testes de carga e performance

---

## 17. CONCLUSÃO

Este documento fornece uma base sólida de **casos de teste realistas** para validação de CNPJ. Use-o como:

**VÁLIDO** **Referência** ao criar planos de teste  
**VÁLIDO** **Checklist** durante execução de testes  
**VÁLIDO** **Base** para automação de testes  
**VÁLIDO** **Guia** para massa de dados de teste  
**VÁLIDO** **Material de treinamento** para novos QAs  

**Lembre-se**: Testes abrangentes garantem qualidade, mas o entendimento profundo do algoritmo é essencial para criar casos de teste eficazes.

---

**Desenvolvido para a comunidade QA**  
*Última atualização: Dezembro 2025*
