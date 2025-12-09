# Documentação CNPJ-QA-Training

Este diretório contém toda a documentação técnica, guias de estudo e material de treinamento do projeto.

> **Versão 2.0.0** - Agora com integração à API da Receita Federal!

## 📂 Estrutura

### 📘 Guides (Guias Técnicos)

Documentação técnica e referências sobre CNPJ:

- **[guia-completo-cnpj.md](guides/guia-completo-cnpj.md)** - Guia completo sobre CNPJ: história, estrutura, legislação e algoritmo de validação
- **[guia-implementacao.md](guides/guia-implementacao.md)** - Guia prático de implementação com exemplos de código em múltiplas linguagens
- **[glossario-referencias.md](guides/glossario-referencias.md)** - Glossário técnico completo e referências oficiais

### 📚 Training (Material de Treinamento)

Material didático estruturado para aprendizado progressivo:

- **[exercicios-praticos.md](training/exercicios-praticos.md)** - 21 exercícios práticos com metodologia Scaffolding
- **[gabarito-exercicios.md](training/gabarito-exercicios.md)** - Respostas detalhadas e explicações dos exercícios
- **[plano-estudo-6-semanas.md](training/plano-estudo-6-semanas.md)** - Plano híbrido de estudo (teoria + prática) para 6 semanas
- **[plano-estudo.md](training/plano-estudo.md)** - Plano de estudo resumido

### 🧪 Testing (Testes e QA)

Documentação sobre testes, casos de teste e metodologias:

- **[casos-teste-realistas.md](testing/casos-teste-realistas.md)** - 33 casos de teste detalhados com massa de dados
- **[shift-left-testing.md](testing/shift-left-testing.md)** - Guia de Shift Left Testing aplicado ao projeto
- **[zephyr-integration.md](testing/zephyr-integration.md)** - Integração com Zephyr Scale (Jira)

## 🆕 API da Receita Federal

O projeto agora inclui integração com APIs públicas para consulta de dados cadastrais de empresas:

### Classes Disponíveis

| Classe | Descrição |
|--------|-----------|
| `ReceitaFederalAPI` | Cliente para consulta de CNPJs |
| `CNPJData` | Dataclass com dados da empresa |
| `ReceitaFederalAPIError` | Exceção para erros da API |

### Exemplo Rápido

```python
from cnpj_validator import ReceitaFederalAPI

api = ReceitaFederalAPI()
dados = api.consultar("11.222.333/0001-81")

print(f"Empresa: {dados.razao_social}")
print(f"Situação: {dados.situacao_cadastral}")
print(f"Ativa: {dados.is_ativa()}")
```

### Métodos da API

| Método | Descrição |
|--------|-----------|
| `consultar(cnpj)` | Consulta completa de dados cadastrais |
| `verificar_situacao(cnpj)` | Apenas situação cadastral |
| `buscar_socios(cnpj)` | Lista do quadro societário |

### Dados Retornados

A classe `CNPJData` contém:

- Razão social e nome fantasia
- Situação cadastral e data
- Data de abertura
- Porte da empresa
- Natureza jurídica
- CNAE principal e secundários
- Endereço completo
- Telefone e email
- Capital social
- Quadro societário
- Informações do Simples Nacional/MEI

## 🎯 Navegação Rápida

### Para iniciantes:
1. Comece com o [Guia Completo CNPJ](guides/guia-completo-cnpj.md)
2. Pratique com os [Exercícios](training/exercicios-praticos.md)
3. Confira o [Gabarito](training/gabarito-exercicios.md) após resolver

### Para QA profissionais:
1. [Casos de Teste Realistas](testing/casos-teste-realistas.md)
2. [Shift Left Testing](testing/shift-left-testing.md)
3. [Guia de Implementação](guides/guia-implementacao.md)

### Para desenvolvedores:
1. [Guia de Implementação](guides/guia-implementacao.md)
2. [Glossário e Referências](guides/glossario-referencias.md)
3. Código fonte em `/src`

## 📖 Metodologia

Este material utiliza a técnica pedagógica **Scaffolding** (Andaimes Educacionais), onde o suporte é gradualmente reduzido conforme o aluno desenvolve autonomia:

- 🟢 **Nível 1**: Exemplo completo com todos os passos
- 🟡 **Nível 2**: Estrutura guiada com dicas
- 🟠 **Nível 3**: Modelo simplificado para relembrar
- 🔴 **Nível 4**: Resolução totalmente independente

## 🤝 Contribuindo

Para contribuir com a documentação:

1. Mantenha a estrutura de pastas atual
2. Use nomenclatura `kebab-case.md`
3. Siga o padrão de formatação Markdown
4. Adicione links cruzados entre documentos relacionados
5. Atualize este índice ao adicionar novos documentos

---

**Nota**: Toda documentação está em português brasileiro para facilitar o aprendizado de profissionais de QA no Brasil.
