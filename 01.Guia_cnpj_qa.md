# Guia Completo CNPJ para Profissionais de QA

## Documento 1: História, Estrutura e Mudança para Formato Alfanumérico

---

## 1. INTRODUÇÃO

Este documento apresenta documentação técnica detalhada sobre o Cadastro Nacional da Pessoa Jurídica (CNPJ), abrangendo desde sua criação até as mudanças regulatórias que entrarão em vigor a partir de julho de 2026. Para profissionais de Quality Assurance atuando em projetos relacionados a CNPJ, é fundamental compreender não apenas o funcionamento atual do sistema, mas também preparar-se adequadamente para validar a implementação do novo formato alfanumérico.

---

## 2. HISTÓRICO DO CNPJ

### 2.1 Origem e Evolução

O Cadastro Nacional da Pessoa Jurídica possui origem histórica anterior à sua instituição oficial. O Brasil desenvolveu progressivamente diferentes sistemas de identificação de entidades jurídicas até estabelecer o formato atual:

**Cadastro Geral de Contribuintes (CGC) - 1964 a 1998**
- Criado pela Lei nº 4.503/64 e Lei nº 5.614/70
- Sistema pioneiro de cadastro de entidades jurídicas
- Utilizado para controle fiscal e tributário
- O primeiro CGC foi registrado em 1939, com o Banco do Brasil sendo a primeira instituição a receber este registro
- Operou por mais de 30 anos, acumulando informações sobre as empresas brasileiras

**Criação do CNPJ - 1º de julho de 1998**
- Instituído por meio da Instrução Normativa SRF nº 27/1998
- Surgiu como uma evolução necessária do CGC
- Mantinha os mesmos princípios, mas com melhorias na estrutura e capacidade de processamento
- Foi um passo importante para modernizar o sistema de identificação de pessoas jurídicas

**Modernização com a Lei nº 9.250/1995**
- Estabeleceu formalmente a criação de um número único de inscrição cadastral
- Artigo 37 determinou os critérios para identificação de pessoas jurídicas

**Regulamentações Posteriores**
- Decreto nº 3.000/1999 (Regulamento do Imposto de Renda)
- Decreto nº 9.580/2018 (atual Regulamento do Imposto de Renda)
- Instrução Normativa RFB nº 1.863/2018 (revogada)
- Instrução Normativa RFB nº 2.119/2022 (norma atual que unifica e moderniza as regras)

### 2.2 Impacto Econômico e Administrativo

A instituição do CNPJ produziu impactos significativos na estrutura econômica e administrativa do país:

- **Formalização de empresas**: Permitiu maior controle e formalização do ambiente de negócios
- **Arrecadação tributária**: Facilitou o controle da arrecadação de impostos
- **Transparência**: Trouxe maior transparência nas transações comerciais
- **Redução da informalidade**: Incentivou a formalização de micro e pequenas empresas
- **Alinhamento com práticas globais**: Preparou o Brasil para alinhar-se a padrões internacionais de eficiência empresarial

---

## 3. ESTRUTURA DO CNPJ NUMÉRICO (FORMATO ATUAL)

Antes de entender as mudanças, é crucial compreender como o CNPJ numérico funciona atualmente.

### 3.1 Formato e Composição

O CNPJ numérico possui **14 dígitos** divididos em três partes:

```
XX.XXX.XXX/YYYY-ZZ
```

Onde:
- **XX.XXX.XXX (Raiz)**: Os primeiros 8 dígitos identificam a empresa matriz
- **YYYY (Ordem)**: Os 4 dígitos seguintes (após a barra) identificam filiais ou unidades da mesma empresa
- **ZZ (Dígitos Verificadores)**: Os 2 últimos dígitos são verificadores, calculados matematicamente

### 3.2 Exemplo Ilustrativo

**CNPJ de referência**: 11.222.333/0001-95

- Raiz: 11.222.333
- Ordem: 0001 (indica que é a matriz, primeira unidade)
- Verificadores: 95

### 3.3 Componentes Detalhados

| Parte | Posição | Caracteres | Função |
|-------|---------|-----------|--------|
| Raiz | 1-8 | Numéricos (0-9) | Identifica a empresa matriz |
| Ordem | 9-12 | Numéricos (0-9) | Identifica filiais/unidades |
| Verificadores | 13-14 | Numéricos (0-9) | Validação matemática |

---

## 4. CÁLCULO DO DÍGITO VERIFICADOR - FORMATO NUMÉRICO

### 4.1 Algoritmo do Módulo 11

O CNPJ utiliza o algoritmo de **Módulo 11** para calcular seus dígitos verificadores, o mesmo utilizado no CPF. Este é um cálculo matemático essencial para validação.

### 4.2 Passo a Passo do Cálculo (Primeiro Dígito)

Usando o CNPJ **11.222.333/0001-XX** como exemplo:

**Passo 1**: Alinhar os 12 primeiros dígitos com seus respectivos pesos

Os pesos seguem o padrão: **5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2**

```
Dígito:  1  1  2  2  2  3  3  3  0  0  0  1
Peso:    5  4  3  2  9  8  7  6  5  4  3  2
```

**Passo 2**: Multiplicar cada dígito pelo seu peso correspondente

```
1×5 = 5
1×4 = 4
2×3 = 6
2×2 = 4
2×9 = 18
3×8 = 24
3×7 = 21
3×6 = 18
0×5 = 0
0×4 = 0
0×3 = 0
1×2 = 2
```

**Passo 3**: Somar todos os resultados

```
5 + 4 + 6 + 4 + 18 + 24 + 21 + 18 + 0 + 0 + 0 + 2 = 102
```

**Passo 4**: Dividir a soma por 11 e obter o resto (módulo)

```
102 ÷ 11 = 9 com resto 3
```

**Passo 5**: Aplicar a regra para obter o primeiro dígito verificador

- Se o resto for **0 ou 1**, o dígito verificador = **0**
- Caso contrário, dígito verificador = **11 - resto**

```
11 - 3 = 8
Primeiro DV = 8
```

### 4.3 Cálculo do Segundo Dígito Verificador

**Passo 1**: Adicionar o primeiro dígito verificador (8) ao CNPJ

```
1  1  2  2  2  3  3  3  0  0  0  1  8
```

**Passo 2**: Alinhar com os novos pesos: **6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2**

```
Dígito:  1  1  2  2  2  3  3  3  0  0  0  1  8
Peso:    6  5  4  3  2  9  8  7  6  5  4  3  2
```

**Passo 3**: Multiplicar cada dígito pelo seu novo peso

```
1×6 = 6
1×5 = 5
2×4 = 8
2×3 = 6
2×2 = 4
3×9 = 27
3×8 = 24
3×7 = 21
0×6 = 0
0×5 = 0
0×4 = 0
1×3 = 3
8×2 = 16
```

**Passo 4**: Somar todos os resultados

```
6 + 5 + 8 + 6 + 4 + 27 + 24 + 21 + 0 + 0 + 0 + 3 + 16 = 120
```

**Passo 5**: Dividir por 11 e obter o resto

```
120 ÷ 11 = 10 com resto 10
```

**Passo 6**: Aplicar a mesma regra

```
11 - 10 = 1
Segundo DV = 1
```

### 4.4 Resultado do Cálculo

**CNPJ validado: 11.222.333/0001-81**

---

## 5. O NOVO CNPJ ALFANUMÉRICO

### 5.1 Justificativa Técnica da Transição

O Brasil registra atualmente aproximadamente 60 milhões de CNPJs ativos. O crescimento exponencial de novas empresas, particularmente no segmento de startups e MEIs (Microempreendedores Individuais), evidencia a proximidade do esgotamento da capacidade do sistema numérico. Em julho de 2024, foram registradas aproximadamente 400 mil novas empresas, estabelecendo recorde histórico na série estatística.

Análises técnicas indicam que o formato numérico oferece aproximadamente 10^12 combinações possíveis, volume insuficiente para garantir sustentabilidade de longo prazo considerando as taxas atuais de crescimento.

O formato alfanumérico amplia exponencialmente o universo de combinações possíveis, assegurando a viabilidade operacional do sistema nas próximas décadas.

### 5.2 Legislação Base

- **Instrução Normativa RFB nº 2.229**, publicada em **15 de outubro de 2024**
- Entrada em vigor: **25 de outubro de 2024**
- Implementação obrigatória: **Julho de 2026**

### 5.3 Estrutura do Novo CNPJ Alfanumérico

O novo formato mantém a estrutura de **14 caracteres**, mas agora inclui letras:

```
AA.AAA.AAA/AAAA-DV
```

Onde:
- **AA.AAA.AAA (Raiz)**: 8 caracteres **alfanuméricos** (letras A-Z e números 0-9)
- **AAAA (Ordem)**: 4 caracteres **alfanuméricos** (letras A-Z e números 0-9)
- **DV (Verificadores)**: 2 dígitos **numéricos** (sempre números 0-9)

### 5.4 Exemplo Ilustrativo de CNPJ Alfanumérico

**Formato de referência: 12.ABC.345/01DE-35**

- Raiz: 12.ABC.345 (inclui letras A, B, C)
- Ordem: 01DE (inclui letras D, E)
- Verificadores: 35

---

## 6. CÁLCULO DO DÍGITO VERIFICADOR - NOVO FORMATO

### 6.1 Introdução à Tabela ASCII

O grande diferencial do novo CNPJ é a necessidade de converter letras em números usando a **tabela ASCII** (American Standard Code for Information Interchange).

Cada caractere (letra ou número) possui um código decimal na tabela ASCII:

| Caractere | ASCII Decimal |
|-----------|---------------|
| 0 | 48 |
| 1 | 49 |
| 2 | 50 |
| 3 | 51 |
| 4 | 52 |
| 5 | 53 |
| 6 | 54 |
| 7 | 55 |
| 8 | 56 |
| 9 | 57 |
| A | 65 |
| B | 66 |
| C | 67 |
| D | 68 |
| E | 69 |
| F | 70 |
| ... | ... |
| Z | 90 |

### 6.2 Fórmula de Conversão

Para calcular o valor a usar no módulo 11:

```
Valor para cálculo = Código ASCII - 48
```

**Exemplos:**
- Número "0": 48 - 48 = **0**
- Número "1": 49 - 48 = **1**
- Número "9": 57 - 48 = **9**
- Letra "A": 65 - 48 = **17**
- Letra "B": 66 - 48 = **18**
- Letra "C": 67 - 48 = **19**
- Letra "Z": 90 - 48 = **42**

### 6.3 Passo a Passo do Cálculo (Primeiro Dígito)

Usando o CNPJ alfanumérico **12.ABC.345/01DE-XX** como exemplo:

**Passo 1**: Converter cada caractere para seu valor ASCII subtraído de 48

```
Caractere:  1  2  A  B  C  3  4  5  0  1  D  E
Valor:      1  2  17 18 19 3  4  5  0  1  20 21
```

**Passo 2**: Alinhar com os pesos: **5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2**

```
Valor:  1  2  17 18 19 3  4  5  0  1  20 21
Peso:   5  4  3  2  9  8  7  6  5  4  3  2
```

**Passo 3**: Multiplicar valor por peso

```
1×5 = 5
2×4 = 8
17×3 = 51
18×2 = 36
19×9 = 171
3×8 = 24
4×7 = 28
5×6 = 30
0×5 = 0
1×4 = 4
20×3 = 60
21×2 = 42
```

**Passo 4**: Somar todos os resultados

```
5 + 8 + 51 + 36 + 171 + 24 + 28 + 30 + 0 + 4 + 60 + 42 = 459
```

**Passo 5**: Dividir por 11 e obter o resto

```
459 ÷ 11 = 41 com resto 8
```

**Passo 6**: Aplicar a regra

```
Se resto = 0 ou 1: DV = 0
Senão: DV = 11 - resto

11 - 8 = 3
Primeiro DV = 3
```

### 6.4 Cálculo do Segundo Dígito

Repete-se todo o processo, agora **incluindo o primeiro DV (3)** no final:

```
Caractere:  1  2  A  B  C  3  4  5  0  1  D  E  3
Valor:      1  2  17 18 19 3  4  5  0  1  20 21 3
Peso:       6  5  4  3  2  9  8  7  6  5  4  3  2
```

Multiplicação:
```
1×6 = 6
2×5 = 10
17×4 = 68
18×3 = 54
19×2 = 38
3×9 = 27
4×8 = 32
5×7 = 35
0×6 = 0
1×5 = 5
20×4 = 80
21×3 = 63
3×2 = 6
```

Soma:
```
6 + 10 + 68 + 54 + 38 + 27 + 32 + 35 + 0 + 5 + 80 + 63 + 6 = 424
```

Resto:
```
424 ÷ 11 = 38 com resto 6
11 - 6 = 5
Segundo DV = 5
```

### 6.5 Resultado do Cálculo

**CNPJ alfanumérico validado: 12.ABC.345/01DE-35**

---

## 7. IMPACTOS NA INFRAESTRUTURA DE SISTEMAS

### 7.1 Sistemas Afetados

Todo sistema que trabalha com CNPJ precisa ser atualizado para suportar o novo formato:

- **Bancos de dados**: Devem permitir armazenamento de caracteres alfanuméricos
- **APIs de consulta**: Precisam aceitar e validar CNPJs alfanuméricos
- **Sistemas de validação**: Devem implementar o novo algoritmo de módulo 11 com suporte a ASCII
- **Softwares de gestão empresarial**: ERPs, sistemas de RH, contábil
- **Plataformas de e-commerce**: Integração com CNPJ para validação de vendedores
- **Emissão de notas fiscais**: Sistemas fiscais precisam suportar o novo formato
- **Serviços financeiros**: Sistemas bancários, de crédito e scoring
- **Plataformas públicas**: Integração com órgãos governamentais

### 7.2 Considerações Técnicas

- **Tipo de dado**: De inteiro para string/varchar
- **Validação**: Necessidade de ajustar regex e validadores
- **Busca e filtros**: Deve ser case-sensitive ou não?
- **Remoção de duplicatas**: Deve considerar ambos os formatos
- **Compatibilidade**: Período de coexistência de ambos formatos

### 7.3 Ferramenta de Teste da Receita Federal

- Em parceria com o **Serpro**, está sendo desenvolvida uma **ferramenta de teste**
- Permitirá validar integração com CNPJs alfanuméricos
- Previsão: testes começarão até **outubro de 2025**
- Será essencial para homologação antes de julho de 2026

---

## 8. CRONOGRAMA OFICIAL

| Data | Evento |
|------|--------|
| 15 de outubro de 2024 | Publicação da Instrução Normativa 2.229 |
| 25 de outubro de 2024 | Entrada em vigor da Instrução Normativa |
| Até outubro de 2025 | Definição oficial das datas de testes |
| Julho de 2026 | Implementação obrigatória do novo formato |

---

## 9. COEXISTÊNCIA DOS DOIS FORMATOS

### 9.1 CNPJs Existentes

- **Não sofrerão alteração**: Empresas com CNPJ numérico continuarão com o mesmo número
- **Permanecerão válidos**: Continuarão sendo aceitos em todos os sistemas
- **Sem necessidade de atualização**: Empresários não precisam fazer nada

### 9.2 Novos CNPJs (A partir de julho de 2026)

- Apenas novas inscrições receberão formato alfanumérico
- Filiais criadas após julho de 2026 podem receber alfanumérico mesmo se a matriz for numérica
- Sistema da Receita atribuirá letras e números de forma **aleatória**

---

## 10. LINHA DO TEMPO VISUAL DO CNPJ

```
1939
│
├─ Primeiro CGC registrado (Banco do Brasil)
│  Início do sistema de identificação de empresas
│
1964
│
├─ Lei nº 4.503 - Criação formal do Cadastro Geral de Contribuintes (CGC)
│  Instituído para controle fiscal e tributário
│
1970
│
├─ Lei nº 5.614 - Complementação da legislação do CGC
│  Expansão do sistema para mais entidades
│
1995
│
├─ Lei nº 9.250 - Determinação de número único de inscrição
│  Fundamento legal para modernização do sistema
│
1998
│
├─ 1º de julho - Criação oficial do CNPJ
│  Instrução Normativa SRF nº 27/1998
│  CNPJ substitui o CGC como sistema principal
│  Formato: 14 dígitos numéricos (XX.XXX.XXX/YYYY-ZZ)
│
1999
│
├─ Implementação do CNPJ Digital
│  Possibilidade de registro e consulta via internet
│  Modernização tecnológica do sistema
│
2022
│
├─ Instrução Normativa RFB nº 2.119
│  Unificação, simplificação e modernização das regras
│  Clareza nas disposições de informações cadastrais
│
2024 - 15 de outubro
│
├─ Publicação da Instrução Normativa RFB nº 2.229
│  Anúncio do novo formato alfanumérico
│  Resposta à crescente demanda por novos CNPJs
│
2024 - 25 de outubro
│
├─ Entrada em vigor da Instrução Normativa nº 2.229
│  Legislação passa a vigorar
│
2025 - Até outubro
│
├─ Definição das datas para testes integrados
│  Ferramenta de teste da Receita/Serpro em desenvolvimento
│  Validação das integrações de sistemas
│
2026 - JULHO
│
└─ IMPLEMENTAÇÃO OBRIGATÓRIA DO CNPJ ALFANUMÉRICO
   Novos CNPJs emitidos no formato: AA.AAA.AAA/AAAA-DV
   Início da coexistência de dois formatos
   Período de transição nos sistemas públicos e privados
```

---

## 11. RESUMO EXECUTIVO

### Mudanças Principais

| Aspecto | Formato Numérico (Até Julho 2026) | Formato Alfanumérico (A partir de Julho 2026) |
|--------|-------|-------|
| **Estrutura** | 14 dígitos numéricos | 14 caracteres (alfanuméricos + numéricos) |
| **Raiz** | 8 dígitos numéricos | 8 caracteres alfanuméricos |
| **Ordem** | 4 dígitos numéricos | 4 caracteres alfanuméricos |
| **Verificadores** | 2 dígitos numéricos | 2 dígitos numéricos |
| **Algoritmo DV** | Módulo 11 padrão | Módulo 11 com ASCII |
| **Combinações** | ~10^12 | Exponencialmente maior |
| **Exemplos** | 11.222.333/0001-95 | 12.ABC.345/01DE-35 |

### Impactos para QA

- Necessidade de testar validação de ambos os formatos
- Testes de cálculo do dígito verificador com letras
- Validação de armazenamento em bancos de dados
- Testes de compatibilidade com sistemas legados
- Integração com ferramenta de teste da Receita/Serpro

---

## 12. REFERÊNCIAS E LEGISLAÇÃO

- Instrução Normativa RFB nº 2.229/2024
- Instrução Normativa RFB nº 2.119/2022
- Lei nº 9.250/1995
- Decreto nº 9.580/2018 (Regulamento do Imposto de Renda)
- Portal Oficial: gov.br/receitafederal
- Serasa Experian: Material técnico sobre CNPJ alfanumérico
