# Automation Scripts

## Visão Geral

Esta pasta contém scripts de automação para QA, organizados por linguagem de programação. O objetivo é fornecer uma estrutura modular para testes automatizados, incluindo testes E2E com Playwright, scripts Python para integração e exemplos práticos.

### Estrutura de Pastas

```
automation-scripts/
├── README.md                    # Este arquivo
├── examples/                    # Exemplos de uso
│   ├── python/                  # Scripts Python de exemplo
│   └── typescript/              # Scripts TypeScript de exemplo
├── typescript/                  # Scripts TypeScript
│   └── playwright-e2e/          # Testes E2E com Playwright
│       ├── package.json         # Dependências e scripts
│       ├── playwright.config.ts # Configuração do Playwright
│       ├── tests/               # Arquivos de teste
│       │   ├── dashboard.spec.ts
│       │   ├── filters.spec.ts
│       │   ├── export.spec.ts
│       │   └── realtime-update.spec.ts
│       └── pages/               # Page Objects
│           ├── DashboardPage.ts
│           ├── FiltersPage.ts
│           └── ...
└── python/                      # Scripts Python (futuro)
    └── scripts/
        └── send_to_qadash.py
```

## Requisitos

- **Node.js**: Versão 18 ou superior
- **npm**: Versão 8 ou superior (geralmente vem com Node.js)
- **Python**: Versão 3.8 ou superior (para scripts Python)
- **Git**: Para controle de versão

## Setup Inicial

1. **Clone o repositório** (se aplicável):
   ```bash
   git clone <repository-url>
   cd fabrica-de-testes/automation-scripts
   ```

2. **Instale as dependências do Playwright**:
   ```bash
   cd typescript/playwright-e2e
   npm install
   ```

3. **Instale os navegadores do Playwright**:
   ```bash
   npx playwright install
   ```

4. **Verifique a instalação**:
   ```bash
   npm test
   ```

## Como Rodar Testes

### Playwright E2E
- **Todos os testes**: `cd typescript/playwright-e2e && npm test`
- **Teste específico**: `npm run test:dashboard`
- **Modo debug**: `npm run test:debug`
- **Modo visual**: `npm run test:headed`

### Scripts Python
- **Enviar dados para QADash**: `python scripts/send_to_qadash.py`

## Geração de Seletores

Para gerar seletores automaticamente, use o Playwright Codegen:

```bash
cd typescript/playwright-e2e
npm run codegen
```

Isso abrirá uma janela do navegador onde você pode navegar pelo site e o Playwright gerará o código correspondente com os seletores apropriados.

## Padrões de Código

### Page Object Model
Usamos o padrão Page Object Model para organizar os testes. Cada página ou componente tem sua própria classe:

```typescript
// pages/DashboardPage.ts
export class DashboardPage {
  constructor(private page: Page) {}

  async navigate() {
    await this.page.goto('/');
  }

  async getTestResultsCount() {
    return await this.page.locator('.test-results').count();
  }
}
```

### Seletores Recomendados
- **Prefira seletores semânticos**: `getByRole('button', { name: 'Export' })`
- **Use texto quando apropriado**: `getByText('Real-time updates active')`
- **Evite seletores frágeis**: Não use `locator('.class-name')` se a classe pode mudar
- **Use data-testid para testes**: Adicione `data-testid` aos elementos para testes estáveis

### Best Practices de E2E
- Teste cenários completos do usuário, não apenas componentes isolados
- Use waits implícitos do Playwright em vez de `waitForTimeout`
- Capture screenshots/videos apenas em falhas para performance
- Mantenha testes independentes e paralelizáveis

## Troubleshooting

### Erros Comuns

1. **"Browser not found"**
   - Solução: Execute `npx playwright install` para instalar navegadores

2. **"Connection refused"**
   - Solução: Certifique-se que o servidor frontend está rodando em `http://localhost:5173`

3. **Testes falhando intermitentemente**
   - Solução: Adicione waits apropriados ou use `await page.waitForLoadState('networkidle')`

4. **Seletores não encontrados**
   - Solução: Use `npx playwright codegen` para gerar seletores atualizados

### Debug
- Use `npm run test:debug` para executar testes passo a passo
- Verifique os traces e screenshots gerados em caso de falha
- Use `console.log` nos Page Objects para debug

## Próximas Expansões

- **Cypress**: Para testes E2E alternativos
- **Jest API**: Para testes de API
- **Selenium**: Para compatibilidade com projetos legados
- **Mobile Testing**: Com Appium ou similar
- **Performance Testing**: Integração com Lighthouse ou k6

Para adicionar novos testes:
1. Crie uma nova pasta em `typescript/` ou `python/`
2. Siga a estrutura existente
3. Atualize este README
4. Adicione scripts no `package.json` correspondente