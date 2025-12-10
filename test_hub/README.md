# 🧪 Test Hub - Central de Testes Automatizados

## O que é este projeto?

O **Test Hub** é uma aplicação web que centraliza a execução e monitoramento de testes automatizados.
Ele permite visualizar, executar e gerar relatórios de múltiplos projetos de teste em um único lugar.

## Arquitetura

```
test_hub/
├── app.py                 # Servidor Flask (Backend)
├── config/
│   └── projects.json      # Configuração dos projetos de teste
├── static/
│   ├── css/
│   │   └── styles.css     # Estilos da interface
│   └── js/
│       └── main.js        # Lógica do frontend
├── templates/
│   └── index.html         # Página principal
├── services/
│   ├── __init__.py
│   ├── test_runner.py     # Serviço que executa os testes
│   └── report_generator.py # Serviço que gera relatórios
├── requirements.txt       # Dependências do hub
└── README.md              # Este arquivo
```

## Como usar

### 1. Instalar dependências

```bash
cd test_hub
pip install -r requirements.txt
```

### 2. Iniciar o servidor

```bash
python app.py
```

### 3. Acessar no navegador

Abra: http://localhost:5000

## Funcionalidades

- ✅ Visualizar projetos de teste cadastrados
- ✅ Executar testes com um clique
- ✅ Acompanhar progresso em tempo real
- ✅ Gerar relatórios consolidados
- ✅ Exportar relatórios em JSON e Markdown

## Adicionando novos projetos

Edite o arquivo `config/projects.json` seguindo o modelo existente.

## Stack Técnica

- **Backend:** Python 3.8+ com Flask
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Execução de testes:** Subprocess + pytest

## Para Aprendizado

Este projeto foi desenvolvido com fins didáticos, com comentários extensivos
explicando cada parte do código. Ideal para quem está aprendendo:

- Arquitetura de aplicações web
- Automação de testes
- Observabilidade de resultados de teste
- Integração de ferramentas de QA
