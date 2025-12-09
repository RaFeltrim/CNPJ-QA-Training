# 4. Plano Híbrido de Estudo - 6 Semanas (Teoria + Prática)

## Documento 4: Plano Integrado - Compreensão Teórica + Implementação Técnica

---

## 1. VISÃO GERAL DO PLANO HÍBRIDO

Este plano segue uma progressão lógica de aprendizado ponta a ponta:

- **Fundamentos Teóricos** (Semanas 1-2): Compreensão profunda do algoritmo através de exercícios manuais
- **Conceitos de QA e Testing** (Semana 3): Metodologias, casos de teste e boas práticas
- **Implementação Guiada** (Semana 4): Criação do próprio código seguindo o aprendizado
- **Execução do Projeto Base** (Semana 5): Executar e testar o CNPJ-QA-Training
- **Automação & Conformidade** (Semana 6): Testes E2E, API Receita Federal, performance e LGPD

**Público-Alvo**: QA Pleno que deseja domínio completo (teoria + prática)

**Carga Horária Total**: 60-80 horas (2h/dia útil × 30 dias)

**Pré-requisitos**:
- Conhecimento básico de Python 3.8+
- Familiaridade com linha de comando
- Git básico

---

## 2. FASE 1: FUNDAMENTOS TEÓRICOS (Semanas 1-2)

### Semana 1 - Estrutura e Algoritmo Numérico

**Objetivo**: Dominar o cálculo manual de dígitos verificadores

| Dia | Atividade | Documento | Entrega | Tempo |
|-----|-----------|-----------|---------|-------|
| **Seg** | Leitura: Estrutura do CNPJ, histórico, legislação | [guia-completo-cnpj.md](../guides/guia-completo-cnpj.md) | Resumo em 10 bullets | 2h |
| **Ter** | Exercício 1: Exemplo completo (🟢) | [exercicios-praticos.md](exercicios-praticos.md) | CNPJ calculado manualmente | 2h |
| **Qua** | Exercício 2: Estrutura guiada (🟡) | [exercicios-praticos.md](exercicios-praticos.md) | CNPJ resolvido | 2h |
| **Qui** | Exercício 3: Modelo simplificado (🟠) | [exercicios-praticos.md](exercicios-praticos.md) | CNPJ resolvido | 1,5h |
| **Sex** | Exercício 4: Resolução independente (🔴) | [exercicios-praticos.md](exercicios-praticos.md) | CNPJ resolvido sem apoio | 2h |

**Entregável da Semana**: 4 CNPJs calculados manualmente + anotações sobre o algoritmo Módulo 11

---

### Semana 2 - Formato Alfanumérico e Casos Especiais

**Objetivo**: Dominar conversão ASCII e validações alfanuméricas

| Dia | Atividade | Documento | Entrega | Tempo |
|-----|-----------|-----------|---------|-------|
| **Seg** | Leitura: Transição para formato alfanumérico (2026-2028) | [guia-completo-cnpj.md](../guides/guia-completo-cnpj.md) | Timeline documentada | 2h |
| **Ter** | Exercício: Conversão ASCII (🟢🟡🟠🔴) | [exercicios-praticos.md](exercicios-praticos.md) | Tabela de conversões | 2h |
| **Qua** | Exercícios: CNPJs alfanuméricos | [exercicios-praticos.md](exercicios-praticos.md) | 3 CNPJs alfanuméricos resolvidos | 2h |
| **Qui** | Exercícios: Comparação numérico vs alfanumérico | [exercicios-praticos.md](exercicios-praticos.md) | Análise comparativa | 1,5h |
| **Sex** | Revisão + Criar seu próprio CNPJ alfanumérico | [exercicios-praticos.md](exercicios-praticos.md) | CNPJ criado e validado | 2h |

**Entregável da Semana**: 5 CNPJs alfanuméricos + documento comparativo

**Checkpoint Semana 2**: Você deve ser capaz de calcular **qualquer CNPJ** (numérico ou alfanumérico) manualmente sem consultar o guia.

---

## 3. FASE 2: CONCEITOS DE QA (Semana 3)

### Semana 3 - Metodologias de Teste e Casos de Teste

**Objetivo**: Aprender metodologias de QA e design de casos de teste

| Dia | Atividade | Documento | Entrega | Tempo |
|-----|-----------|-----------|---------|-------|
| **Seg** | Leitura: Shift Left Testing | [shift-left-testing.md](../testing/shift-left-testing.md) | Resumo da metodologia | 2h |
| **Ter** | Estudo: Casos de Teste Realistas | [casos-teste-realistas.md](../testing/casos-teste-realistas.md) | Lista de 10 casos importantes | 2h |
| **Qua** | Análise: Categorias de teste (Happy Path, Edge Cases) | [casos-teste-realistas.md](../testing/casos-teste-realistas.md) | Mapa mental das categorias | 2h |
| **Qui** | Estudo: Integração com ferramentas (Zephyr/Jira) | [zephyr-integration.md](../testing/zephyr-integration.md) | Fluxo de trabalho documentado | 2h |
| **Sex** | Criar seus próprios casos de teste | Documento próprio | 5 novos casos de teste originais | 2h |

**Entregável da Semana**: 
- Resumo das metodologias
- 5 casos de teste originais criados por você
- Mapa mental de categorias de teste

**Checkpoint Semana 3**: Você compreende as metodologias de QA e sabe projetar casos de teste efetivos.

---

## 4. FASE 3: IMPLEMENTAÇÃO GUIADA (Semana 4)

### Semana 4 - Criando Seu Próprio Validador

**Objetivo**: Aplicar conhecimento teórico criando seu próprio código

| Dia | Atividade | Referência | Entrega | Tempo |
|-----|-----------|------------|---------|-------|
| **Seg** | Estudo: Guia de Implementação | [guia-implementacao.md](../guides/guia-implementacao.md) | Pseudocódigo do validador | 2h |
| **Ter** | Implementar `validar_cnpj_numerico()` | Seu código | Função básica funcionando | 2,5h |
| **Qua** | Implementar `validar_cnpj_alfanumerico()` | Seu código | Função com conversão ASCII | 2,5h |
| **Qui** | Adicionar tratamento de erros e formatação | Seu código | Validador completo | 2h |
| **Sex** | Escrever testes unitários para seu código | Seu código | 10+ testes escritos | 2h |

**Estrutura Sugerida do Seu Projeto**:
```
meu-validador-cnpj/
├── validador.py          # Seu código de validação
├── test_validador.py     # Seus testes
└── README.md             # Documentação
```

**Entregável da Semana**: Repositório pessoal com validador funcional + testes

**Checkpoint Semana 4**: Você tem seu próprio validador de CNPJ funcionando.

---

## 5. FASE 4: EXECUÇÃO DO PROJETO BASE (Semana 5) 🆕

### Semana 5 - Explorando o CNPJ-QA-Training

**Objetivo**: Executar, testar e explorar o projeto base completo

| Dia | Atividade | Comando/Arquivo | Entrega | Tempo |
|-----|-----------|-----------------|---------|-------|
| **Seg** | Setup: Clonar e configurar ambiente | `git clone`, `pip install -e .` | Ambiente funcionando | 2h |
| **Ter** | Executar exemplos e demos | `python examples/demo.py` | Relatório de execução | 2h |
| **Qua** | Executar suite de testes completa | `pytest tests/ -v` | Relatório de cobertura | 2,5h |
| **Qui** | Explorar API da Receita Federal | `python examples/demo_api_receita.py` | Consultas documentadas | 2h |
| **Sex** | Comparar: Seu código vs Projeto Base | Análise comparativa | Documento de melhorias | 2h |

**Comandos Importantes**:
```bash
# 1. Clonar o projeto
git clone https://github.com/RaFeltrim/CNPJ-QA-Training.git
cd CNPJ-QA-Training

# 2. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -e .
pip install -r requirements.txt

# 4. Executar demo básica
python examples/quick-start.py
python examples/demo.py

# 5. Executar testes
pytest tests/ -v --cov=cnpj_validator

# 6. Demo da API Receita Federal
python examples/demo_api_receita.py
```

**Análise Comparativa** (Sexta-feira):
- O que seu código faz diferente?
- Que técnicas do projeto base você pode aplicar?
- Que melhorias você faria no projeto base?

**Entregável da Semana**:
- Ambiente configurado e funcionando
- Relatório de execução dos testes
- Documento comparativo (seu código vs projeto base)
- Lista de aprendizados

**Checkpoint Semana 5**: Você executou o projeto completo e compreende sua arquitetura.

---

## 6. FASE 5: AUTOMAÇÃO & CONFORMIDADE (Semana 6)

### Semana 6 - Testes Avançados, API e Documentação

**Objetivo**: Dominar testes avançados, API e conformidade

| Dia | Atividade | Ferramenta | Entrega | Tempo |
|-----|-----------|------------|---------|-------|
| **Seg** | Testes E2E com projeto base | pytest + markers | Testes de integração rodando | 2h |
| **Ter** | Explorar ReceitaFederalAPI em profundidade | API do projeto | 5 consultas diferentes | 2,5h |
| **Qua** | Criar novos testes para a API | pytest | 5+ testes novos para API | 2h |
| **Qui** | Documentação LGPD e Logging | Markdown | Política de dados documentada | 2h |
| **Sex** | Projeto final: Apresentação + Documentação | Todas | README + apresentação | 2,5h |

**Explorando a API da Receita Federal**:
```python
from cnpj_validator import CNPJValidator, ReceitaFederalAPI

# Validar localmente primeiro
validator = CNPJValidator()
resultado = validator.validate("11.222.333/0001-81")

if resultado['valid']:
    # Consultar na Receita Federal
    api = ReceitaFederalAPI()
    dados = api.consultar(resultado['cnpj_clean'])
    
    print(f"Empresa: {dados.razao_social}")
    print(f"Situação: {dados.situacao_cadastral}")
    print(f"Ativa: {dados.is_ativa()}")
    print(f"Endereço: {dados.get_endereco_completo()}")
    
    # Verificar sócios
    socios = api.buscar_socios(resultado['cnpj_clean'])
    for socio in socios:
        print(f"Sócio: {socio['nome']}")
```

**Documentação LGPD**:
- Política de retenção de logs
- Mascaramento de CNPJs em logs (XX.XXX.XXX/****-**)
- Minimização de dados
- Direito ao esquecimento

**Entregável da Semana**: 
- Suite de testes expandida
- Consultas API documentadas
- Documentação LGPD
- Apresentação final do projeto

**Checkpoint Final**: Você domina validação de CNPJ de ponta a ponta!
|-----|-----------|------------|---------|-------|
| **Seg** | Formulário HTML + máscara CNPJ | HTML, CSS, JS | Form responsivo com validação | 2h |
| **Ter** | Feedback visual (válido / inválido) | CSS, JS | UX com estados claros | 2h |
| **Qua** | Integração com validadores TS | TypeScript | Form funcional + validação real-time | 2h |
| **Qui** | Service de consulta (mock Receita) | TypeScript | Mock de retorno de dados | 2h |
| **Sex** | Deploy + documentação de uso | Vercel/Netlify | Link público + guia de uso | 2h |

**Features Implementadas**:
- Máscara automática (XX.XXX.XXX/XXXX-XX)
- Validação em tempo real
- Suporte a formato numérico e alfanumérico
- Feedback visual claro
- Mensagens de erro específicas
- Link para consulta oficial (com aviso de captcha)

**Entregável da Semana**: Aplicação web funcional + documentação de uso

**Checkpoint Semana 4**: Você possui um validador completo e funcional, pronto para ser usado em projetos reais.

---

## 4. FASE 3: AUTOMAÇÃO & CONFORMIDADE (Semanas 5-6)

### Semana 5 - Testes Automatizados E2E

**Objetivo**: Garantir qualidade através de automação completa

| Dia | Atividade | Ferramenta | Entrega | Tempo |
|-----|-----------|------------|---------|-------|
| **Seg** | Setup Cypress + cenários base | Cypress | 5 testes E2E (happy paths) | 2h |
| **Ter** | Testes de validação (formatos) | Cypress | 10 testes (edge cases) | 2,5h |
| **Qua** | Testes de responsividade | Cypress | Testes mobile + tablet + desktop | 2h |
| **Qui** | Setup Robot Framework + BDD | Robot Framework | 5 cenários Gherkin | 2,5h |
| **Sex** | Pipeline CI/CD (GitHub Actions) | GitHub Actions | CI rodando testes automáticos | 2h |

**Cenários de Teste E2E**:
```gherkin
# Exemplo de cenário BDD
Feature: Validação de CNPJ

  Scenario: Validar CNPJ numérico válido
    Given o usuário acessa o formulário
    When preenche o CNPJ "12.345.678/0001-95"
    Then deve exibir mensagem "CNPJ válido ✓"
    And o botão de consulta deve estar habilitado

  Scenario: Rejeitar CNPJ com DV inválido
    Given o usuário acessa o formulário
    When preenche o CNPJ "12.345.678/0001-99"
    Then deve exibir mensagem "Dígito verificador inválido ✗"
    And o botão de consulta deve estar desabilitado
```

**Entregável da Semana**: Suite completa de testes E2E + CI/CD configurado

---

### Semana 6 - Performance, LGPD e Documentação Final

**Objetivo**: Garantir conformidade legal e performance

| Dia | Atividade | Ferramenta | Entrega | Tempo |
|-----|-----------|------------|---------|-------|
| **Seg** | Testes de performance (k6) | k6 | Relatório de carga (100-1000 req/s) | 2,5h |
| **Ter** | Análise de bottlenecks | k6, Chrome DevTools | Otimizações implementadas | 2h |
| **Qua** | Documentação LGPD | Markdown | Política de logs + mascaramento | 2h |
| **Qui** | Implementar logging seguro | Winston/Pino | Logs com dados sensíveis mascarados | 2h |
| **Sex** | Documentação final + apresentação | Markdown, Slides | README completo + apresentação | 2,5h |

**Testes de Performance (k6)**:
```javascript
// Exemplo de teste de carga
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 100 },  // Ramp-up
    { duration: '1m', target: 500 },   // Sustentado
    { duration: '30s', target: 1000 }, // Pico
    { duration: '30s', target: 0 },    // Ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% < 500ms
  },
};

export default function() {
  let response = http.post('https://api.exemplo.com/validar-cnpj', 
    JSON.stringify({ cnpj: '12.345.678/0001-95' }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
```

**Documentação LGPD**:
- Política de retenção de logs (30-90 dias)
- Mascaramento de CNPJs em logs (XX.XXX.XXX/****-**)
- Minimização de dados (não armazenar QSA sem necessidade)
- Direito ao esquecimento (processo de exclusão)
- Auditoria de acesso

**Entregável da Semana**: Projeto completo com performance validada + conformidade LGPD

**Checkpoint Final**: Você possui um projeto completo, testado, performático e em conformidade com LGPD, pronto para produção.

---

## 7. ENTREGÁVEIS FINAIS DO PLANO

Ao concluir as 6 semanas, você terá:

### Conhecimento Teórico

- Domínio completo do algoritmo Módulo 11
- Capacidade de calcular DVs manualmente (numérico e alfanumérico)
- Compreensão da legislação e histórico do CNPJ
- Conhecimento sobre transição 2026-2028

### Habilidades de QA

- Design de casos de teste efetivos
- Metodologia Shift Left Testing
- Categorização de testes (Happy Path, Edge Cases, etc.)
- Integração com ferramentas (Zephyr/Jira)

### Implementação Técnica

- Seu próprio validador Python funcional
- Experiência com o projeto CNPJ-QA-Training
- Testes unitários e de integração
- Uso da API da Receita Federal

### Conformidade e Qualidade

- Documentação LGPD
- Boas práticas de logging
- Análise comparativa de código

### Documentação

- README técnico do seu projeto
- Casos de teste documentados
- Apresentação final

---

## 6. CRONOGRAMA VISUAL

```text
┌─────────────────────────────────────────────────────────────────┐
│  PLANO DE ESTUDO - 6 SEMANAS (Ponta a Ponta)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1: FUNDAMENTOS TEÓRICOS (Semanas 1-2)                    │
│  ═══════════════════════════════════════════                    │
│  Semana 1  ████████████  Algoritmo Numérico                     │
│  Semana 2  ████████████  Formato Alfanumérico                   │
│                                                                 │
│  FASE 2: CONCEITOS DE QA (Semana 3)                            │
│  ════════════════════════════════════                           │
│  Semana 3  ████████████  Metodologias + Casos de Teste         │
│                                                                 │
│  FASE 3: IMPLEMENTAÇÃO GUIADA (Semana 4)                       │
│  ═════════════════════════════════════════                      │
│  Semana 4  ████████████  Criar Seu Próprio Validador           │
│                                                                 │
│  FASE 4: EXECUÇÃO PROJETO BASE (Semana 5)  ⭐                   │
│  ═══════════════════════════════════════════                    │
│  Semana 5  ████████████  CNPJ-QA-Training + API Receita        │
│                                                                 │
│  FASE 5: AUTOMAÇÃO & FINALIZAÇÃO (Semana 6)                    │
│  ═══════════════════════════════════════════════════════════    │
│  Semana 6  ████████████  Testes Avançados + LGPD + Apresentação│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Legenda: ████ = 10 horas de estudo | ⭐ = Etapa chave do projeto
```

---

## 8. CRITÉRIOS DE SUCESSO

Para considerar o plano concluído com êxito:

### (Concluido) Critérios Teóricos

- [ ] Calcular manualmente qualquer CNPJ numérico sem consultar material
- [ ] Calcular manualmente qualquer CNPJ alfanumérico
- [ ] Explicar o algoritmo Módulo 11 para um colega

### (Concluido) Critérios de QA

- [ ] Criar casos de teste efetivos
- [ ] Categorizar testes corretamente
- [ ] Aplicar metodologia Shift Left

### (Concluido) Critérios Técnicos

- [ ] Seu validador próprio funcionando
- [ ] Projeto CNPJ-QA-Training executado com sucesso
- [ ] Testes passando (seu código + projeto base)
- [ ] API da Receita Federal utilizada

### (Concluido) Critérios de Documentação

- [ ] README do seu projeto
- [ ] Casos de teste documentados
- [ ] Análise comparativa concluída
- [ ] Apresentação final preparada

---

## 9. RECURSOS E FERRAMENTAS

### 📚 Documentação Oficial

- [Portal CNPJ - Receita Federal](https://solucoes.receita.fazenda.gov.br/Servicos/cnpjreva/cnpjreva_solicitacao.asp)
- [Comprovante de Inscrição](https://servicos.receita.fazenda.gov.br/servicos/cnpj/cnpjreva/cnpjreva_solicitacao.asp)
- [IN SRF 2.119/2022 - Novo Formato](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/cnpj)

### 💻 Stack Tecnológica

- **Linguagem**: Python 3.8 - 3.12
- **Testes**: pytest, pytest-cov
- **API**: requests (para Receita Federal)
- **Linting**: flake8, pylint, black
- **CI/CD**: GitHub Actions

### 🔧 Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/RaFeltrim/CNPJ-QA-Training.git
cd CNPJ-QA-Training

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -e .
pip install -r requirements.txt

# Executar testes
pytest tests/ -v --cov=cnpj_validator

# Executar exemplos
python examples/demo.py
python examples/demo_api_receita.py
```

---

## 10. DICAS PARA MAXIMIZAR O APRENDIZADO

### 💡 Boas Práticas

1. **Não pule etapas**: A teoria é essencial para a prática
2. **Pratique diariamente**: 2h/dia é melhor que 14h no fim de semana
3. **Documente suas dúvidas**: Mantenha um diário de aprendizado
4. **Compartilhe conhecimento**: Ensine um colega para fixar o conteúdo
5. **Compare seu código**: Analise diferenças entre seu validador e o projeto base

### ⚠️ Armadilhas Comuns

- ❌ Pular a fase teórica e ir direto para código
- ❌ Copiar código sem entender o algoritmo
- ❌ Ignorar casos de teste edge cases
- ❌ Não executar os testes do projeto base
- ❌ Não explorar a API da Receita Federal

### 🎯 Marcos de Motivação

- **Semana 2**: "Já sei calcular qualquer CNPJ manualmente!"
- **Semana 3**: "Sei projetar casos de teste efetivos!"
- **Semana 4**: "Meu próprio validador está funcionando!"
- **Semana 5**: "Executei o projeto completo com sucesso!"
- **Semana 6**: "Domino validação de CNPJ de ponta a ponta!"

---

## 11. PRÓXIMOS PASSOS APÓS CONCLUSÃO

Após concluir o plano:

1. **Contribua para o projeto**: Abra PRs no CNPJ-QA-Training
2. **Expanda seu validador**: Adicione validação de CPF, NIS, etc
3. **Crie conteúdo**: Escreva artigos técnicos sobre sua jornada
4. **Mentoria**: Ajude outros QAs a aprender validação de CNPJ
5. **Aplique no trabalho**: Use o conhecimento em projetos reais

---

## 12. CONTATO E SUPORTE

**Repositório**: [github.com/RaFeltrim/CNPJ-QA-Training](https://github.com/RaFeltrim/CNPJ-QA-Training)

**Issues**: Reporte bugs ou sugira melhorias nas Issues do GitHub

**Contribuições**: Pull requests são bem-vindos!

---

Boa sorte no seu treinamento! 🚀

Última atualização: Dezembro 2025