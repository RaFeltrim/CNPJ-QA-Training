# 2. Exercícios CNPJ - Treinamento Prático para QA

## Documento 2: Treinamento Prático, Cálculos Simplificados e Estratégia de Testes

---

## 1. INTRODUÇÃO AO DOCUMENTO

Este documento é complementar ao **1. Guia_CNPJ**. Aqui você encontrará:

- **Planejamento de estudo estruturado**: Semanas de aprendizado progressivo
- **Explicações simplificadas** de conceitos complexos
- **Exercícios práticos** para consolidar conhecimento
- **Exemplos de casos de teste**: Cenários reais de QA
- **Calculadora de DV passo a passo**: Para entender cada operação
- **Desafios de validação**: Para treinar a profundidade necessária

---

### Como Usar Este Documento

**IMPORTANTE**: Este é um documento de **TREINAMENTO** com exercícios para prática.

- **Metodologia progressiva aplicada** - Do básico ao avançado  
- **Exercícios estruturados** - Com níveis de dificuldade crescente  
- **Gabarito separado** - Disponível após conclusão dos exercícios  

**Objetivo**: Desenvolver sua autonomia através de uma metodologia pedagógica comprovada, onde o suporte é gradualmente removido para que você construa confiança e competência.

---

## 2. METODOLOGIA DE APRENDIZADO PROGRESSIVO

### Entendendo a Abordagem Pedagógica

Este documento utiliza a técnica de **Scaffolding** (Andaimes Educacionais), uma metodologia cientificamente comprovada onde:

1. **Início com suporte total** - Você aprende observando exemplos completos
2. **Redução gradual do apoio** - Pratica com orientação estruturada
3. **Autonomia progressiva** - Resolve com menos dicas
4. **Independência completa** - Aplica o conhecimento sozinho

### Sistema de Níveis

Utilizamos 4 níveis de suporte identificados por cores:

| Nível | Cor | Descrição | O que você encontra |
|-------|-----|-----------|---------------------|
| **Nível 1** | 🟢 | **Exemplo Completo** | Resposta detalhada com todos os passos explicados |
| **Nível 2** | 🟡 | **Estrutura Guiada** | Campos para preencher com dicas e orientação |
| **Nível 3** | 🟠 | **Modelo Simplificado** | Formato básico para você relembrar o processo |
| **Nível 4** | 🔴 | **Resolução Independente** | Apenas o enunciado - resolva sozinho |

### Como a Progressão Funciona

```
Nível de Suporte ↓              Autonomia do Aluno ↑
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 100% Apoio  →  Aprende observando o método completo
🟡  70% Apoio  →  Pratica com estrutura e dicas
🟠  40% Apoio  →  Relembra com formato básico
🔴   0% Apoio  →  Aplica conhecimento de forma autônoma
```

### Por Que Esta Metodologia Funciona?

**Baseado em pesquisas de neurociência e pedagogia:**

1. **Reduz Frustração Inicial**
   - Começar com exemplos completos evita desistência
   - Você entende o "porquê" antes de fazer sozinho

2. **Aumenta Retenção**
   - Prática ativa aumenta memorização em 50%
   - Repetição espaçada com menos apoio consolida aprendizado

3. **Desenvolve Confiança**
   - Cada nível prepara para o próximo
   - Sucessos graduais constroem autoeficácia

4. **Cria Autonomia Real**
   - Ao final, você não depende de modelos
   - Consegue aplicar em situações novas

### Exercícios com Metodologia Aplicada

Este documento possui **7 conjuntos de exercícios** com progressão:

| Exercício | Tema | Níveis |
|-----------|------|--------|
| **Ex. 1-4** | Cálculo de Dígitos Verificadores (Numéricos) | 🟢🟡🟠🔴 |
| **Ex. 5** | Reconhecer Componentes do CNPJ | 🟢🟡🟠🔴 |
| **Ex. 9-11** | Prática Adicional de Cálculos | 🟢🟡🔴 |
| **Ex. 13** | Conversão ASCII | 🟢🟡🟠🔴 |
| **Ex. 14** | Completar Sequência | 🟢🔴 |
| **Ex. 16-18** | Cálculos Alfanuméricos | 🟢🟡🔴 |
| **Ex. 20** | Validação de Caracteres | 🟢🟡🟠🔴 |

### Instruções Importantes

1. **Siga a Ordem**: Não pule exercícios - cada um prepara para o próximo
2. **Resista à Tentação**: Tente resolver antes de consultar o gabarito
3. **Anote Dúvidas**: Revise conceitos no Guia_CNPJ quando necessário
4. **Pratique Escrevendo**: Fazer à mão aumenta memorização
5. **Gabarito ao Final**: Disponível após conclusão de todos os exercícios

### O Que Você Será Capaz de Fazer

Após completar este documento seguindo a metodologia:

- Calcular dígitos verificadores de qualquer CNPJ (numérico ou alfanumérico)  
- Validar CNPJs manualmente e identificar erros  
- Converter caracteres ASCII para valores de cálculo  
- Criar casos de teste apropriados para sistemas  
- Planejar estratégias de validação completas  
- Ensinar outros profissionais sobre CNPJ  

**Agora você está pronto para começar os exercícios!**

---

## 3. PLANEJAMENTO DE ESTUDO (4 SEMANAS)

### SEMANA 1: Fundamentos

**Objetivo**: Entender a história e a estrutura básica do CNPJ

| Dia | Tema | Tempo | Atividade |
|-----|------|-------|----------|
| Segunda | Histórico do CNPJ | 1h | Ler seções 2 e 3 do Guia Completo |
| Terça | Estrutura do CNPJ Numérico | 1h | Entender os componentes (raiz, ordem, verificadores) |
| Quarta | Exemplos e Formatação | 45min | Exercícios 1-3 |
| Quinta | Legislação e Contexto | 1h | Revisar cronograma e mudanças |
| Sexta | Revisão Semana 1 | 30min | Quiz de conhecimento |

**Entregáveis**: Entender a estrutura básica, saber os componentes de um CNPJ

---

### SEMANA 2: Cálculos de Validação - Formato Numérico

**Objetivo**: Dominar completamente o cálculo do dígito verificador no formato numérico

| Dia | Tema | Tempo | Atividade |
|-----|------|-------|----------|
| Segunda | Módulo 11 Explicado | 1,5h | Entender o algoritmo de forma simples |
| Terça | Cálculo Passo a Passo | 1,5h | Exercícios 4-7 (cálculos básicos) |
| Quarta | Prática Intensiva | 2h | Exercícios 8-12 (cálculos avançados) |
| Quinta | Validação vs Cálculo | 1h | Entender diferenças e casos especiais |
| Sexta | Teste Prático Completo | 2h | Exercício Final da Semana 2 |

**Entregáveis**: Calcular DV de qualquer CNPJ numérico sem erros

---

### SEMANA 3: Novo Formato Alfanumérico

**Objetivo**: Compreender e calcular o dígito verificador do novo formato

| Dia | Tema | Tempo | Atividade |
|-----|------|-------|----------|
| Segunda | Tabela ASCII e Conversão | 1,5h | Entender conversão ASCII, Exercícios 13-14 |
| Terça | Cálculo com Letras | 1,5h | Exercícios 15-18 (cálculos alfanuméricos) |
| Quarta | Casos Especiais | 1h | Exercícios 19-20 (combinações de letras/números) |
| Quinta | Comparação dos Formatos | 1h | Entender diferenças, Exercício 21 |
| Sexta | Teste Completo Alfanumérico | 2h | Exercício Final da Semana 3 |

**Entregáveis**: Calcular DV de qualquer CNPJ alfanumérico com precisão

---

### SEMANA 4: Estratégia de Testes e Preparação

**Objetivo**: Desenvolver plano de testes e preparação para projetos reais

| Dia | Tema | Tempo | Atividade |
|-----|------|-------|----------|
| Segunda | Casos de Teste Numéricos | 1,5h | Exercício 22-24 (casos de teste) |
| Terça | Casos de Teste Alfanuméricos | 1,5h | Exercício 25-27 (casos de teste novo formato) |
| Quarta | Plano de Testes Completo | 2h | Criar seu próprio plano de testes |
| Quinta | Validação de Sistemas | 1,5h | Entender impactos em DB, API, etc |
| Sexta | Review Final e Revisão | 2h | Fazer todos os testes em sequência |

**Entregáveis**: Plano de testes pronto para executar em projeto real

---

## 4. CÁLCULO DO DÍGITO VERIFICADOR - EXPLICADO DE FORMA SIMPLES

### Conceito Fundamental: Módulo 11

Imagine que você quer verificar se um CNPJ é válido sem fraude. O método é usar uma **conta matemática especial** chamada **Módulo 11**.

**Módulo** significa o **resto de uma divisão** (Resto arredondar para cima Ex: 1,81 = 2).

Exemplo simples:
- 15 ÷ 11 = 1 com **resto 4**
- O módulo 11 de 15 é **4**

### Por Que Funciona?

O Módulo 11 funciona porque:
1. Distribui **pesos diferentes** para cada dígito (alguns contam mais, outros menos)
2. Se alguém **mudar um dígito**, o resultado da conta muda
3. Se o resultado da conta **não bater**, o CNPJ é falso

---

## 5. EXERCÍCIOS PRÁTICOS

### Aplicação da Metodologia

Este capítulo usa uma abordagem pedagógica que remove gradualmente o suporte, permitindo que você desenvolva autonomia:

| Exercício | CNPJ | Nível de Apoio | Objetivo |
|-----------|------|----------------|----------|
| **1** | 12.345.678/0001-XX | 🟢 **Completo** | Aprenda o método passo a passo |
| **2** | 98.765.432/0002-XX | 🟡 **Estrutura guiada** | Pratique com campos para preencher |
| **3** | 11.111.111/0001-XX | 🟠 **Modelo simplificado** | Relembre o formato de cálculo |
| **4** | 99.999.999/9999-XX | 🔴 **Independente** | Resolva sozinho, sem assistência |

**Dica**: Siga a ordem dos exercícios para melhor aproveitamento do aprendizado!

---

### EXERCÍCIO 1: Calcular Dígitos Verificadores [EXEMPLO COMPLETO]

**CNPJ: 12.345.678/0001-XX**

**Objetivo**: Aprender o passo a passo completo do cálculo dos dígitos verificadores.

**Nível**: 🟢 Resposta completa - Use como referência

---

#### **1. CNPJ: 12.345.678/0001-XX**

**Identificação das Partes:**
```
Raiz:          12.345.678
Ordem:         0001
Verificadores: XX (a calcular)
```

---

**CÁLCULO DO PRIMEIRO DÍGITO VERIFICADOR (DV1)**

**Passo 1:** Escrever os 12 primeiros dígitos (raiz + ordem)
```
1  2  3  4  5  6  7  8  0  0  0  1
```

**Passo 2:** Alinhar com os pesos para o primeiro DV
```
Dígitos:  1    2    3    4    5    6    7    8    0    0    0    1
Pesos:    5    4    3    2    9    8    7    6    5    4    3    2
```

**Passo 3:** Multiplicar cada dígito pelo seu peso correspondente
```
1×5  = 5
2×4  = 8
3×3  = 9
4×2  = 8
5×9  = 45
6×8  = 48
7×7  = 49
8×6  = 48
0×5  = 0
0×4  = 0
0×3  = 0
1×2  = 2
```

**Passo 4:** Somar todos os resultados
```
Soma = 5 + 8 + 9 + 8 + 45 + 48 + 49 + 48 + 0 + 0 + 0 + 2 = 222
```

**Passo 5:** Dividir a soma por 11 e obter o resto (módulo 11)
```
222 ÷ 11 = 20 com resto 2
```

**Passo 6:** Aplicar a regra do dígito verificador
```
Regra: Se resto = 0 ou 1 → DV = 0
       Caso contrário → DV = 11 - resto

Resto = 2
DV1 = 11 - 2 = 9
```

**✓ Primeiro Dígito Verificador: 9**

---

**CÁLCULO DO SEGUNDO DÍGITO VERIFICADOR (DV2)**

**Passo 1:** Adicionar o primeiro DV aos 12 dígitos anteriores
```
1  2  3  4  5  6  7  8  0  0  0  1  9
```

**Passo 2:** Alinhar com os pesos para o segundo DV
```
Dígitos:  1    2    3    4    5    6    7    8    0    0    0    1    9
Pesos:    6    5    4    3    2    9    8    7    6    5    4    3    2
```

**Passo 3:** Multiplicar cada dígito pelo seu peso correspondente
```
1×6  = 6
2×5  = 10
3×4  = 12
4×3  = 12
5×2  = 10
6×9  = 54
7×8  = 56
8×7  = 56
0×6  = 0
0×5  = 0
0×4  = 0
1×3  = 3
9×2  = 18
```

**Passo 4:** Somar todos os resultados
```
Soma = 6 + 10 + 12 + 12 + 10 + 54 + 56 + 56 + 0 + 0 + 0 + 3 + 18 = 237
```

**Passo 5:** Dividir a soma por 11 e obter o resto
```
237 ÷ 11 = 21 com resto 6
```

**Passo 6:** Aplicar a regra do dígito verificador
```
Resto = 6
DV2 = 11 - 6 = 5
```

**✓ Segundo Dígito Verificador: 5**

---

**RESPOSTA FINAL:**
```
CNPJ Completo: 12.345.678/0001-95

Raiz:          12.345.678
Ordem:         0001
Verificadores: 95
```

---

### EXERCÍCIO 2: Calcular Dígitos Verificadores [ESTRUTURA GUIADA]

**CNPJ: 98.765.432/0002-XX**

**Objetivo**: Praticar o cálculo com apoio da estrutura.

**Nível**: 🟡 Estrutura guiada - Preencha os espaços em branco

---

**CÁLCULO DO PRIMEIRO DÍGITO VERIFICADOR (DV1)**

**Passo 1:** Escrever os 12 primeiros dígitos
```
9  8  7  6  5  4  3  2  0  0  0  2
```

**Passo 2:** Alinhar com os pesos
```
Dígitos:  9    8    7    6    5    4    3    2    0    0    0    2
Pesos:    5    4    3    2    9    8    7    6    5    4    3    2
```

**Passo 3:** Multiplicar cada dígito pelo seu peso
```
9×5  = _____
8×4  = _____
7×3  = _____
6×2  = _____
5×9  = _____
4×8  = _____
3×7  = _____
2×6  = _____
0×5  = _____
0×4  = _____
0×3  = _____
2×2  = _____
```

**Passo 4:** Somar todos os resultados
```
Soma = _____ + _____ + _____ + _____ + _____ + _____ + _____ + _____ + _____ + _____ + _____ + _____ = _____
```

**Passo 5:** Dividir por 11 e obter o resto
```
_____ ÷ 11 = _____ com resto _____
```

**Passo 6:** Aplicar a regra
```
Resto = _____
DV1 = 11 - _____ = _____
```

**✓ Primeiro Dígito Verificador: _____**

---

**CÁLCULO DO SEGUNDO DÍGITO VERIFICADOR (DV2)**

**Passo 1:** Adicionar o primeiro DV
```
9  8  7  6  5  4  3  2  0  0  0  2  [DV1]
```

**Passo 2:** Alinhar com os pesos
```
Dígitos:  9    8    7    6    5    4    3    2    0    0    0    2    [___]
Pesos:    6    5    4    3    2    9    8    7    6    5    4    3    2
```

**Passo 3:** Multiplicar
```
9×6  = _____
8×5  = _____
7×4  = _____
6×3  = _____
5×2  = _____
4×9  = _____
3×8  = _____
2×7  = _____
0×6  = _____
0×5  = _____
0×4  = _____
2×3  = _____
[DV1]×2 = _____
```

**Passo 4:** Somar
```
Soma = _____ (complete a soma de todos os valores acima)
```

**Passo 5:** Dividir por 11
```
_____ ÷ 11 = _____ com resto _____
```

**Passo 6:** Aplicar a regra
```
Resto = _____
DV2 = 11 - _____ = _____
```

**✓ Segundo Dígito Verificador: _____**

---

**RESPOSTA FINAL:**
```
CNPJ Completo: 98.765.432/0002-_____

Raiz:          98.765.432
Ordem:         0002
Verificadores: _____
```

<!-- 
GABARITO EXERCÍCIO 2:
Primeiro DV: 9×5=45, 8×4=32, 7×3=21, 6×2=12, 5×9=45, 4×8=32, 3×7=21, 2×6=12, 0×5=0, 0×4=0, 0×3=0, 2×2=4
Soma = 224, 224÷11 = 20 resto 4, DV1 = 11-4 = 7
Segundo DV: 9×6=54, 8×5=40, 7×4=28, 6×3=18, 5×2=10, 4×9=36, 3×8=24, 2×7=14, 0×6=0, 0×5=0, 0×4=0, 2×3=6, 7×2=14
Soma = 244, 244÷11 = 22 resto 2, DV2 = 11-2 = 9
CNPJ: 98.765.432/0002-79
-->

---

### EXERCÍCIO 3: Calcular Dígitos Verificadores [MODELO SIMPLIFICADO]

**CNPJ: 11.111.111/0001-XX**

**Objetivo**: Relembrar o processo usando o formato de cálculo.

**Nível**: 🟠 Modelo simplificado - Use o formato para organizar

---

**CÁLCULO DO PRIMEIRO DÍGITO VERIFICADOR**

```
CNPJ:  1  1  1  1  1  1  1  1  0  0  0  1
Peso:  5  4  3  2  9  8  7  6  5  4  3  2

Multiplicação:
__ __ __ __ __ __ __ __ __ __ __ __

Soma = _____

_____ ÷ 11 = _____ com resto _____

DV1 = 11 - _____ = _____
```

---

**CÁLCULO DO SEGUNDO DÍGITO VERIFICADOR**

```
CNPJ:  1  1  1  1  1  1  1  1  0  0  0  1  [DV1]
Peso:  6  5  4  3  2  9  8  7  6  5  4  3  2

Multiplicação:
__ __ __ __ __ __ __ __ __ __ __ __ __

Soma = _____

_____ ÷ 11 = _____ com resto _____

DV2 = 11 - _____ = _____
```

---

**RESPOSTA FINAL:**
```
CNPJ Completo: 11.111.111/0001-_____
```

<!-- 
GABARITO EXERCÍCIO 3:
DV1: 1×5+1×4+1×3+1×2+1×9+1×8+1×7+1×6+0×5+0×4+0×3+1×2 = 46
46÷11 = 4 resto 2, DV1 = 11-2 = 9
DV2: 1×6+1×5+1×4+1×3+1×2+1×9+1×8+1×7+0×6+0×5+0×4+1×3+9×2 = 65
65÷11 = 5 resto 10, DV2 = 11-10 = 1
CNPJ: 11.111.111/0001-91
-->

---

### EXERCÍCIO 4: Calcular Dígitos Verificadores [RESOLUÇÃO INDEPENDENTE]

**CNPJ: 99.999.999/9999-XX**

**Objetivo**: Aplicar todo o conhecimento adquirido sem assistência.

**Nível**: 🔴 Independente - Resolva sem apoio

**Instruções**: Calcule os dois dígitos verificadores seguindo o método aprendido nos exercícios anteriores. Organize sua resolução de forma clara e detalhada, mostrando:
- Alinhamento dos dígitos com os pesos
- Todas as multiplicações
- Soma total
- Cálculo do resto
- Aplicação da regra para obter o DV

---

**Espaço para sua resolução:**

```
[Escreva aqui todo o processo de cálculo]




























```

---

**RESPOSTA FINAL:**
```
CNPJ Completo: 99.999.999/9999-_____
```

<!-- 
GABARITO EXERCÍCIO 4:
Cálculo do Primeiro DV:
9×5=45, 9×4=36, 9×3=27, 9×2=18, 9×9=81, 9×8=72, 9×7=63, 9×6=54, 9×5=45, 9×4=36, 9×3=27, 9×2=18
Soma = 522
522÷11 = 47 com resto 5
DV1 = 11-5 = 6

Cálculo do Segundo DV:
9×6=54, 9×5=45, 9×4=36, 9×3=27, 9×2=18, 9×9=81, 9×8=72, 9×7=63, 9×6=54, 9×5=45, 9×4=36, 9×3=27, 6×2=12
Soma = 570
570÷11 = 51 com resto 9
DV2 = 11-9 = 2

CNPJ: 99.999.999/9999-62
-->

---

## 6. EXERCÍCIOS COMPLEMENTARES

**Nota Pedagógica**: Todos os exercícios desta seção seguem a metodologia progressiva 🟢🟡🟠🔴, removendo gradualmente o apoio para desenvolver sua autonomia.

---

### EXERCÍCIO 5: Reconhecer Componentes de um CNPJ

**Metodologia Progressiva**: Do exemplo completo até identificação independente.

**Instrução**: Classifique os trechos abaixo como RAIZ, ORDEM ou VERIFICADOR:

**1. 12.345.678 → 🟢 RAIZ**
```
Explicação: São os 8 primeiros dígitos do CNPJ, representam a empresa matriz.
```

**2. 0001 → 🟡 ___________**
```
Dica: São 4 dígitos que aparecem após a raiz, antes dos verificadores.
```

**3. 95 → 🟡 ___________**
```
Dica: São os 2 últimos dígitos, calculados para validação.
```

**4. 45.678 → 🟠 ___________**
```
Dica: Quantos dígitos tem? Faz parte de qual componente?
```

**5. 01 → 🔴 ___________**

<!-- 
GABARITO EXERCÍCIO 2:
1. RAIZ
2. ORDEM
3. VERIFICADOR
4. Parte da RAIZ (últimos 3 dígitos da raiz)
5. Parte da ORDEM (primeiros 2 dígitos da ordem)
-->

---

### EXERCÍCIO 6: Contar Dígitos

**Instrução**: Quantos dígitos tem cada parte do CNPJ?

1. Raiz: _____ dígitos
2. Ordem: _____ dígitos
3. Verificadores: _____ dígitos
4. Total: _____ dígitos

<!-- 
GABARITO EXERCÍCIO 6:
1. Raiz: 8 dígitos
2. Ordem: 4 dígitos
3. Verificadores: 2 dígitos
4. Total: 14 dígitos
-->

---

### EXERCÍCIO 7: Validar um CNPJ Conhecido

**CNPJ dado: 11.222.333/0001-81**

Recalcule os DVs seguindo os passos aprendidos e responda: **Este CNPJ é válido?**

```
Primeiro DV calculado: _____
Segundo DV calculado: _____

CNPJ dado: 11.222.333/0001-81
DVs dados: 81

É válido? ☐ SIM ☐ NÃO
```

<!-- 
GABARITO EXERCÍCIO 7:
Primeiro DV: 1×5+1×4+2×3+2×2+2×9+3×8+3×7+3×6+0×5+0×4+0×3+1×2 = 5+4+6+4+18+24+21+18+0+0+0+2 = 102
102÷11 = 9 resto 3, DV1 = 11-3 = 8
Segundo DV: 1×6+1×5+2×4+2×3+2×2+3×9+3×8+3×7+0×6+0×5+0×4+1×3+8×2 = 6+5+8+6+4+27+24+21+0+0+0+3+16 = 120
120÷11 = 10 resto 10, DV2 = 11-10 = 1
CNPJ Completo: 11.222.333/0001-81
Resposta: ☑ SIM - É válido!
-->

---

### EXERCÍCIO 8: Criar Seu Próprio CNPJ

**Instruções**: 
1. Escolha 8 dígitos para a raiz
2. Escolha 4 dígitos para a ordem
3. Calcule os dois dígitos verificadores

```
Raiz escolhida:   __.__.___
Ordem escolhida:  ____

[Realize todos os cálculos necessários]

Primeiro DV: _____
Segundo DV: _____

CNPJ Completo: _______________
```

---

### EXERCÍCIO 9-11: Prática Adicional de Cálculos

**Metodologia Progressiva**: Da estrutura guiada à resolução independente.

**Instruções**: Calcule os dígitos verificadores dos CNPJs abaixo.

---

**9. CNPJ: 33.333.333/0001-??** 🟢 **[Com estrutura guiada]**

```
CNPJ:  3  3  3  3  3  3  3  3  0  0  0  1
Peso:  5  4  3  2  9  8  7  6  5  4  3  2

Multiplicação:
3×5=___ 3×4=___ 3×3=___ 3×2=___ 3×9=___ 3×8=___ 
3×7=___ 3×6=___ 0×5=___ 0×4=___ 0×3=___ 1×2=___

Soma = _____
_____ ÷ 11 = _____ com resto _____
Primeiro DV = _____

[Calcule o segundo DV seguindo o mesmo processo]

Segundo DV = _____
CNPJ Completo: 33.333.333/0001-_____
```

---

**10. CNPJ: 87.654.321/0001-??** 🟡 **[Modelo simplificado]**

```
CNPJ:  8  7  6  5  4  3  2  1  0  0  0  1
Peso:  5  4  3  2  9  8  7  6  5  4  3  2

Multiplicações: __ __ __ __ __ __ __ __ __ __ __ __

Soma = _____
Resto = _____
Primeiro DV = _____

[Calcule o segundo DV]

Segundo DV = _____
CNPJ Completo: 87.654.321/0001-_____
```

---

**11. CNPJ: 00.000.000/0001-??** 🔴 **[Resolução independente]**

```
[Espaço para sua resolução completa]









CNPJ Completo: 00.000.000/0001-_____
```

<!-- 
GABARITO EXERCÍCIOS 9-11:

9. CNPJ: 33.333.333/0001-48
   DV1: 3×5+3×4+3×3+3×2+3×9+3×8+3×7+3×6+0×5+0×4+0×3+1×2 = 15+12+9+6+27+24+21+18+0+0+0+2 = 134
   134÷11 = 12 resto 2, DV1 = 11-2 = 9... [continuar cálculo do DV2]
    
10. CNPJ: 87.654.321/0001-74
    DV1: 8×5+7×4+6×3+5×2+4×9+3×8+2×7+1×6+0×5+0×4+0×3+1×2 = 40+28+18+10+36+24+14+6+0+0+0+2 = 178
    178÷11 = 16 resto 2, DV1 = 11-2 = 9... [continuar cálculo do DV2]

11. CNPJ: 00.000.000/0001-91
    DV1: 0×5+0×4+0×3+0×2+0×9+0×8+0×7+0×6+0×5+0×4+0×3+1×2 = 2
    2÷11 = 0 resto 2, DV1 = 11-2 = 9
    DV2: 0×6+0×5+0×4+0×3+0×2+0×9+0×8+0×7+0×6+0×5+0×4+1×3+9×2 = 3+18 = 21
    21÷11 = 1 resto 10, DV2 = 11-10 = 1
-->

---

## 7. TRANSIÇÃO PARA FORMATO ALFANUMÉRICO

### Entendendo a Tabela ASCII de Forma Simples

Cada letra tem um **número secreto** chamado código ASCII. Precisamos saber este número para fazer o cálculo.

**O truque**: Subtrair **48** do código ASCII para obter o valor que usaremos.

**Tabela Simplificada**:

| Letra | ASCII | ASCII - 48 | Valor |
|-------|-------|-----------|-------|
| 0 | 48 | 48 - 48 | 0 |
| 1 | 49 | 49 - 48 | 1 |
| ... | ... | ... | ... |
| 9 | 57 | 57 - 48 | 9 |
| A | 65 | 65 - 48 | **17** |
| B | 66 | 66 - 48 | **18** |
| C | 67 | 67 - 48 | **19** |
| D | 68 | 68 - 48 | **20** |
| E | 69 | 69 - 48 | **21** |
| ... | ... | ... | ... |
| Z | 90 | 90 - 48 | **42** |

**Regra Simples**:
- Os números (0-9) mantêm seus valores (0-9)
- As letras (A-Z) viram números de 17 a 42
- A = 17, B = 18, C = 19, ... Z = 42

---

### EXERCÍCIO 13: Conversão ASCII

**Metodologia Progressiva**: Exemplos completos → Dicas → Resolução independente.

**Instrução**: Converta os caracteres para seus valores (número mantém valor, letra = ASCII - 48):

```
1.  "0" → 🟢 0  (Número mantém o valor)
2.  "5" → 🟢 5  (Número mantém o valor)
3.  "A" → 🟢 17 (ASCII 65 - 48 = 17)
4.  "B" → 🟡 _____ (Dica: ASCII 66 - 48)
5.  "C" → 🟡 _____ (Dica: ASCII 67 - 48)
6.  "D" → 🟡 _____ (Dica: Letra após C)
7.  "E" → 🟠 _____ (Lembre: ASCII - 48)
8.  "Z" → 🟠 _____ (Última letra do alfabeto)
9.  "M" → 🔴 _____ (13ª letra)
10. "9" → 🔴 _____ (É número ou letra?)
```

<!-- 
GABARITO EXERCÍCIO 13:
1. "0" → 0
2. "5" → 5
3. "A" → 17 (ASCII 65 - 48)
4. "B" → 18 (ASCII 66 - 48)
5. "C" → 19 (ASCII 67 - 48)
6. "D" → 20 (ASCII 68 - 48)
7. "E" → 21 (ASCII 69 - 48)
8. "Z" → 42 (ASCII 90 - 48)
9. "M" → 29 (ASCII 77 - 48)
10. "9" → 9
-->

---

### EXERCÍCIO 14: Completar a Sequência

**Metodologia Progressiva**: 2 itens = 🟢 (com dica) e 🔴 (independente)

**Instrução**: Encontre os valores que faltam:

| Letra | Valor | Nível |
|-------|-------|-------|
| A | 17 | - |
| B | 18 | - |
| C | _____ | 🟢 Dica: B=18, então C=? |
| D | 20 | - |
| E | 21 | - |
| F | _____ | 🔴 (resolva independente) |
| ... | ... | ... |
| Z | 42 | - |

<!-- 
GABARITO EXERCÍCIO 14:
C = 19 (ASCII 67 - 48) - Sequência: 17, 18, 19...
F = 22 (ASCII 70 - 48) - Sequência continua: 20, 21, 22...
-->

---

### EXERCÍCIO 15: Calcular DV - CNPJ Alfanumérico Simples

**CNPJ: 1A.AAA.AAA/01AA-XX**

**Passo 1**: Converter para valores

```
Caractere: 1  A  A  A  A  A  A  A  0  1  A  A
Valor:     1  17 17 17 17 17 17 17 0  1  17 17
Peso:      5  4  3  2  9  8  7  6  5  4  3  2
```

**Passo 2**: Multiplicar cada valor pelo peso

```
1×5  = _____
17×4 = _____
17×3 = _____
17×2 = _____
17×9 = _____
17×8 = _____
17×7 = _____
17×6 = _____
0×5  = _____
1×4  = _____
17×3 = _____
17×2 = _____
```

**Passo 3**: Somar e calcular DV

```
Soma = _____
Resto = _____
Primeiro DV = _____
Segundo DV = _____
CNPJ Completo: _________________
```

<!-- 
GABARITO EXERCÍCIO 15:
1×5=5, 17×4=68, 17×3=51, 17×2=34, 17×9=153, 17×8=136, 17×7=119, 17×6=102, 0×5=0, 1×4=4, 17×3=51, 17×2=34
Soma = 5+68+51+34+153+136+119+102+0+4+51+34 = 757
757÷11 = 68 resto 9
Primeiro DV = 11-9 = 2
[Cálculo do segundo DV necessário para completar]
-->

---

### EXERCÍCIO 16-18: Cálculos Alfanuméricos Progressivos

**Metodologia Progressiva**: Da conversão guiada à resolução independente.

---

**16. CNPJ: 12.ABC.345/01DE-??** 🟢 **[Estrutura guiada]**

```
Passo 1: Conversão para valores
1=1, 2=2, A=17, B=18, C=19, 3=3, 4=4, 5=5, 0=0, 1=1, D=20, E=21

Passo 2: Alinhar com pesos
Valores: 1  2  17 18 19 3  4  5  0  1  20 21
Pesos:   5  4  3  2  9  8  7  6  5  4  3  2

Passo 3: Multiplicar
1×5=___  2×4=___  17×3=___  18×2=___  19×9=___  3×8=___
4×7=___  5×6=___  0×5=___   1×4=___   20×3=___ 21×2=___

Passo 4: Somar e calcular
Soma = _____
Resto = _____
Primeiro DV = _____

[Calcule o segundo DV]

Segundo DV = _____
CNPJ Completo: 12.ABC.345/01DE-_____
```

---

**17. CNPJ: AB.CDE.FGH/IJKL-??** 🟡 **[Modelo simplificado]**

```
Passo 1: Conversão (complete você)
A=___ B=___ C=___ D=___ E=___ F=___ 
G=___ H=___ I=___ J=___ K=___ L=___

Passo 2: Multiplique pelos pesos (5,4,3,2,9,8,7,6,5,4,3,2)

Multiplicações: _______________________________

Soma = _____
Primeiro DV = _____
Segundo DV = _____

CNPJ Completo: AB.CDE.FGH/IJKL-_____
```

---

**18. CNPJ: ZZ.ZZZ.ZZZ/ZZZZ-??** 🔴 **[Resolução independente]**

```
[Espaço para sua resolução completa]

Conversão: Z = _____









CNPJ Completo: ZZ.ZZZ.ZZZ/ZZZZ-_____
```

<!-- 
GABARITO EXERCÍCIOS 16-18:

16. CNPJ: 12.ABC.345/01DE-??
    Valores: 1,2,17,18,19,3,4,5,0,1,20,21
    [Cálculos completos necessários]

17. CNPJ: AB.CDE.FGH/IJKL-??
    Conversão: A=17,B=18,C=19,D=20,E=21,F=22,G=23,H=24,I=25,J=26,K=27,L=28
    [Cálculos completos necessários]

18. CNPJ: ZZ.ZZZ.ZZZ/ZZZZ-??
    Conversão: Z=42 (todas as posições)
    [Cálculos completos necessários]
-->

---

### EXERCÍCIO 19: Comparar Cálculos (Numérico vs Alfanumérico)

**Instrução**: Calcule ambos os formatos e compare

```
Numérico:      11.111.111/0001-??
Cálculos: _________________________________
DVs: _____

Alfanumérico:  AA.AAA.AAA/AAAA-??
Cálculos: _________________________________
DVs: _____

Qual teve o DV maior? _______
Qual foi mais fácil de calcular? _______
Qual requer mais cuidado com erros? _______
```

<!-- 
GABARITO EXERCÍCIO 19:
Numérico: 11.111.111/0001-91 (DV=91)
Alfanumérico: AA.AAA.AAA/AAAA-?? (A=17 em todas posições)
[Cálculos completos necessários]

Qual teve o DV maior? Depende do resultado
Qual foi mais fácil? Numérico (sem conversão)
Qual requer mais cuidado? Alfanumérico (conversão ASCII)
-->

---

### EXERCÍCIO 20: Validação de Caracteres Inválidos

**Metodologia Progressiva**: De explicações completas até análise independente.

**Instrução**: Identifique quais CNPJs são válidos ou inválidos e justifique:

---

**1. 12.345.678/0001-95** 🟢 **[Com explicação]**
```
☑ Válido   ☐ Inválido

Por quê? 
Formato correto: XX.XXX.XXX/XXXX-XX ✓
Apenas números na raiz e ordem ✓
DV tem 2 dígitos ✓
DV calculado está correto (visto no Exercício 1) ✓
```

---

**2. 12.345.678/0001-100** 🟡 **[Com dica]**
```
☐ Válido   ☐ Inválido

Dica: Quantos dígitos pode ter o verificador?

Por quê? _________________________________
_________________________________________
```

---

**3. 12.34&.678/0001-95** 🟡 **[Com dica]**
```
☐ Válido   ☐ Inválido

Dica: O caractere "&" é permitido no CNPJ?

Por quê? _________________________________
_________________________________________
```

---

**4. 12.345.678-0001-95** 🟠 **[Análise estrutural]**
```
☐ Válido   ☐ Inválido

Analise: Compare o formato com o padrão correto.

Por quê? _________________________________
_________________________________________
```

---

**5. AA.AAA.AAA/AAAA-99** 🔴 **[Análise independente]**
```
☐ Válido   ☐ Inválido

Por quê? _________________________________
_________________________________________
_________________________________________
```

<!-- 
GABARITO EXERCÍCIO 20:
1. ☑ Válido - Formato correto, DV calculado corretamente
2. ☑ Inválido - DV tem apenas 2 dígitos, não pode ser 100
3. ☑ Inválido - Caractere especial & não é permitido
4. ☑ Inválido - Formato incorreto (usa - em vez de /)
5. Depende do cálculo - Formato válido, mas precisa validar se DV está correto
-->

---

### EXERCÍCIO 21: Criar Seu Próprio CNPJ Válido

**Instrução**: Crie um CNPJ alfanumérico válido do zero

Escolha a raiz e ordem (você pode usar números e letras):

```
Raiz escolhida: __.__.___
Ordem escolhida: ____

[Realize os cálculos dos DVs]

Primeiro DV: _____
Segundo DV: _____

CNPJ Válido Completo: _______________
```

<!-- 
GABARITO EXERCÍCIO 21:
Exercício livre - o aluno deve:
1. Escolher 8 caracteres para raiz (números ou letras)
2. Escolher 4 caracteres para ordem
3. Calcular ambos os DVs corretamente
4. Verificar o resultado final
-->

---

## 8. EXEMPLOS DE CASOS DE TESTE

### CASO DE TESTE 1: Validação de Formato Numérico

```
ID: CT-001
Nome: Validar formato CNPJ numérico válido
Pré-condição: Sistema aceita entrada de CNPJ
Passos:
  1. Inserir CNPJ: 11.222.333/0001-81
  2. Clicar em "Validar"
Resultado Esperado: Sistema aceita, exibe "CNPJ válido"
Tipo: Teste Positivo
Prioridade: Alta
```

---

### CASO DE TESTE 2: Validação de DV Incorreto

```
ID: CT-002
Nome: Rejeitar CNPJ com dígito verificador errado
Pré-condição: Sistema valida dígito verificador
Passos:
  1. Inserir CNPJ: 11.222.333/0001-99 (DV errado, deveria ser 81)
  2. Clicar em "Validar"
Resultado Esperado: Sistema rejeita, exibe "Dígito verificador inválido"
Tipo: Teste Negativo
Prioridade: Alta
```

---

### CASO DE TESTE 3: Validação de Formato Alfanumérico

```
ID: CT-003
Nome: Validar formato CNPJ alfanumérico válido
Pré-condição: Sistema suporta novo formato (após julho 2026)
Passos:
  1. Inserir CNPJ: 12.ABC.345/01DE-35
  2. Clicar em "Validar"
Resultado Esperado: Sistema aceita, exibe "CNPJ válido"
Tipo: Teste Positivo
Prioridade: Crítica
```

---

### CASO DE TESTE 4: Rejeitar Caracteres Inválidos

```
ID: CT-004
Nome: Rejeitar CNPJ com caracteres especiais
Pré-condição: Sistema valida formato
Passos:
  1. Inserir CNPJ: 12.345.67@/0001-95
  2. Clicar em "Validar"
Resultado Esperado: Sistema rejeita com mensagem de erro
Tipo: Teste Negativo
Prioridade: Alta
```

---

### CASO DE TESTE 5: Coexistência de Formatos

```
ID: CT-005
Nome: Aceitar ambos os formatos simultaneamente
Pré-condição: Sistema em período de transição
Passos:
  1. Cadastrar CNPJ numérico: 11.222.333/0001-81
  2. Cadastrar CNPJ alfanumérico: 12.ABC.345/01DE-35
  3. Buscar ambos
Resultado Esperado: Sistema aceita e busca ambos sem erros
Tipo: Teste Positivo
Prioridade: Crítica
```

---

### CASO DE TESTE 6: Armazenamento em Banco de Dados

```
ID: CT-006
Nome: Validar armazenamento de CNPJ alfanumérico em BD
Pré-condição: Banco de dados atualizado para varchar
Passos:
  1. Inserir CNPJ: 12.ABC.345/01DE-35
  2. Consultar BD diretamente
  3. Recuperar valor
Resultado Esperado: Valor armazenado e recuperado sem alterações
Tipo: Teste de Integração
Prioridade: Alta
```

---

### CASO DE TESTE 7: Cálculo de DV em API

```
ID: CT-007
Nome: Validar cálculo correto do DV via API
Pré-condição: API de validação CNPJ implementada
Passos:
  1. Fazer requisição POST: /api/cnpj/validate
  2. Body: { "cnpj": "12ABC34501DE" }
  3. Validar resposta
Resultado Esperado: 
  HTTP 200
  { "valid": true, "dv": "35" }
Tipo: Teste de API
Prioridade: Crítica
```

---

### CASO DE TESTE 8: Senibilidade a Maiúsculas/Minúsculas

```
ID: CT-008
Nome: Validar tratamento de letras maiúsculas/minúsculas
Pré-condição: Sistema processando CNPJs alfanuméricos
Passos:
  1. Inserir: 12.abc.345/01de-35
  2. Inserir: 12.ABC.345/01DE-35
  3. Inserir: 12.Abc.345/01De-35
Resultado Esperado: Sistema trata todas como válidas (case-insensitive)
Tipo: Teste Negativo/Positivo
Prioridade: Média
```

---

### CASO DE TESTE 9: Remoção de Máscara

```
ID: CT-009
Nome: Validar CNPJ sem formatação
Pré-condição: Sistema aceita CNPJ sem pontos/barras
Passos:
  1. Inserir: 12ABC34501DE35
  2. Inserir: 12.ABC.345/01DE-35
  3. Comparar
Resultado Esperado: Sistema reconhece como mesma empresa
Tipo: Teste de Validação
Prioridade: Alta
```

---

### CASO DE TESTE 10: Performance com Validação

```
ID: CT-010
Nome: Validar performance de validação em lote
Pré-condição: Sistema recebe múltiplas validações
Passos:
  1. Submeter 10.000 CNPJs para validação
  2. Medir tempo de resposta
  3. Validar 100% de acurácia
Resultado Esperado: 
  - Tempo < 5 segundos
  - Acurácia 100%
Tipo: Teste de Performance
Prioridade: Média
```

---

## 9. EXEMPLO DE PLANO DE TESTES PARA PROJETO CNPJ

### Estrutura Recomendada

```
PLANO DE TESTES - CNPJ ALFANUMÉRICO

1. ESCOPO
   - Validação de CNPJs numéricos (regressão)
   - Validação de CNPJs alfanuméricos (novo)
   - Armazenamento em banco de dados
   - APIs de consulta e validação
   - Coexistência dos dois formatos

2. FUNCIONALIDADES A TESTAR
   2.1. Validação de Formato
   2.2. Cálculo de Dígito Verificador
   2.3. Armazenamento de Dados
   2.4. Busca e Filtros
   2.5. Integração com Serviços Externos

3. TIPOS DE TESTE
   3.1. Testes Unitários
   3.2. Testes de Integração
   3.3. Testes de Validação
   3.4. Testes de Performance
   3.5. Testes de Regressão

4. CASOS DE TESTE POR CATEGORIA
   4.1. Validação (15 casos)
   4.2. Cálculo (20 casos)
   4.3. Banco de Dados (10 casos)
   4.4. API (12 casos)
   4.5. Coexistência (8 casos)

5. DADOS DE TESTE
   5.1. CNPJs válidos numéricos (10)
   5.2. CNPJs válidos alfanuméricos (10)
   5.3. CNPJs inválidos (20)
   5.4. Casos limites (15)
   5.5. Dados malformados (10)

6. AMBIENTE DE TESTE
   - Dev, QA, Staging
   - Banco de dados de teste com dados anônimos
   - Ferramenta de teste da Receita Federal

7. CRITÉRIOS DE ACEITO
   - 100% dos casos de teste executados
   - Validação manual dos cálculos de DV
   - Homologação com Receita Federal
```

---

## 10. RESUMO DE APRENDIZADO

Após completar este documento, você será capaz de:

✅ Explicar o histórico completo do CNPJ
✅ Identificar componentes de um CNPJ
✅ Calcular dígitos verificadores no formato numérico
✅ Converter caracteres ASCII para valores de cálculo
✅ Calcular dígitos verificadores no formato alfanumérico
✅ Validar CNPJs de ambos os formatos
✅ Criar casos de teste apropriados
✅ Planejar testes para projetos CNPJ
✅ Entender impactos em sistemas e bancos de dados
✅ Preparar-se para homologação com Receita Federal

---

## 11. ESTATÍSTICAS DA METODOLOGIA APLICADA

### 📊 Exercícios com Metodologia Progressiva 🟢🟡🟠🔴

Este documento utiliza uma abordagem pedagógica cientificamente comprovada: **Scaffolding** (andaimes educacionais), onde o suporte é gradualmente removido para desenvolver autonomia.

| Seção | Exercício | Itens | Metodologia Aplicada |
|-------|-----------|-------|---------------------|
| **4. Práticos** | 1-4: Cálculo de DVs | 4 CNPJs | 🟢 Completo → 🟡 Guiado → 🟠 Simplificado → 🔴 Independente |
| **5. Complementares** | 5: Componentes | 5 itens | 🟢 (1) → 🟡 (2) → 🟠 (1) → 🔴 (1) |
| **5. Complementares** | 9-11: Cálculos Extra | 3 CNPJs | 🟢 Guiado → 🟡 Simplificado → 🔴 Independente |
| **5. Transição** | 13: Conversão ASCII | 10 itens | 🟢 (3) → 🟡 (3) → 🟠 (2) → 🔴 (2) |
| **5. Transição** | 14: Sequência | 2 itens | 🟢 Com dica → 🔴 Independente |
| **5. Transição** | 16-18: Alfanuméricos | 3 CNPJs | 🟢 Guiado → 🟡 Simplificado → 🔴 Independente |
| **5. Transição** | 20: Validação | 5 casos | 🟢 (1) → 🟡 (2) → 🟠 (1) → 🔴 (1) |

**Total**: 7 exercícios com metodologia progressiva aplicada

### 🎯 Benefícios desta Abordagem

1. **Aprendizado Natural**: Imita como aprendemos na vida real
2. **Redução de Frustração**: Suporte inicial evita desistência
3. **Desenvolvimento de Confiança**: Cada nível prepara para o próximo
4. **Autonomia Gradual**: Remove dependência progressivamente
5. **Melhor Retenção**: Prática ativa aumenta memorização em 50%

---

## 12. GABARITO

🔒 **O gabarito completo está disponível em um documento separado:**

**Arquivo**: `3.Gabarito_exercicios_CNPJ.md`  
**Localização**: Pasta comprimida protegida por senha  
**Acesso**: Senha será fornecida após conclusão de todos os exercícios

### ℹ️ Sobre o Gabarito

- ✅ Contém todas as respostas detalhadas
- ✅ Explicações passo a passo dos cálculos
- ✅ Justificativas para cada resposta
- ✅ Dicas para evitar erros comuns

### 🎯 Como Obter Acesso

1. Complete todos os exercícios deste documento
2. Documente suas respostas de forma organizada
3. Solicite revisão ao instrutor/coordenador
4. Receba a senha de acesso ao gabarito
5. Compare suas respostas e aprenda com os erros

**Importante**: Tente resolver todos os exercícios antes de consultar o gabarito. O aprendizado real acontece no esforço de resolver os problemas!

---

## 13. DICAS DE ESTUDO

### Para Iniciantes:
1. 📝 **Faça os exercícios à mão primeiro**: Não use calculadora, entenda o processo
2. 🔢 **Decore os pesos**: 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2 (primeiro DV)
3. 📖 **Estude o Exercício 1**: Ele está completo como exemplo
4. ⏰ **Pratique regularmente**: 30 minutos por dia durante uma semana

### Para Avançados:
5. 🏢 **Use exemplos reais**: Pegue CNPJs de empresas conhecidas e valide
6. 👥 **Compartilhe conhecimento**: Ensine um colega para fixar melhor
7. 🔧 **Teste em ferramentas**: Use calculadores online para validar seus cálculos
8. 🎯 **Crie seus próprios casos**: Invente CNPJs e valide

### Para QA:
9. 🧪 **Monte casos de teste**: Use os exemplos da seção 6
10. 📊 **Documente erros comuns**: Crie seu próprio catálogo
11. 🔄 **Revise regularmente**: Faça quiz uma vez por semana
12. 💡 **Prepare-se para perguntas**: Antecipe dúvidas de colegas e stakeholders

---

## 14. PRÓXIMOS PASSOS

1. ✅ Completar todos os exercícios deste documento
2. ✅ Revisar o Exercício 1 (exemplo completo) sempre que tiver dúvidas
3. 📚 Estudar ferramentas de teste da Receita Federal
4. 📚 Participar de treinamentos oficiais (quando disponíveis)
5. 🔧 Acompanhar atualizações da Receita Federal
6. 🎯 Criar plano de testes específico para seu projeto
7. 🧪 Começar testes com ferramenta de teste em outubro de 2025
8. ✅ Realizar homologação com Receita Federal antes de julho de 2026

---

## 15. INFORMAÇÕES SOBRE ESTE DOCUMENTO

**Nome do Documento**: 2. Exercícios_CNPJ  
**Documento Complementar**: 1. Guia_CNPJ  
**Formato de Distribuição**: PDF  
**Última Atualização**: Dezembro 2025

**Como usar este documento**:
- O Exercício 1 está completo como EXEMPLO de resolução
- Todos os demais exercícios têm apenas campos para resposta
- Os gabaritos estão salvos em comentários HTML (invisíveis no PDF)
- Use este documento para praticar e testar seus conhecimentos
- Consulte o Guia_CNPJ sempre que precisar revisar conceitos
