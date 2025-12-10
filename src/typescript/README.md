# CNPJ Validator - TypeScript/JavaScript

Validador de CNPJ brasileiro com suporte completo ao novo formato alfanumérico que será implementado pela Receita Federal em julho de 2026.

## 📦 Instalação

```bash
npm install cnpj-validator-br
```

## 🚀 Uso Rápido

```typescript
import { validate, isValid, format, generate } from 'cnpj-validator-br';

// Validação simples
console.log(isValid('11.222.333/0001-81')); // true

// Validação completa
const result = validate('11.222.333/0001-81');
console.log(result);
// {
//   valid: true,
//   cnpjClean: '11222333000181',
//   cnpjFormatted: '11.222.333/0001-81',
//   isAlphanumeric: false,
//   isMatrix: true,
//   branchNumber: 1,
//   errors: []
// }

// Formatação
console.log(format('11222333000181')); // '11.222.333/0001-81'

// Geração para testes
const cnpjNumerico = generate();
const cnpjAlfanumerico = generate({ alphanumeric: true });
const cnpjComRaiz = generate({ root: 'ABCD1234' });
```

## 📋 API

### `validate(cnpj: string): ValidationResult`

Valida um CNPJ e retorna informações detalhadas.

### `isValid(cnpj: string): boolean`

Validação rápida - retorna apenas true/false.

### `format(cnpj: string): string`

Formata o CNPJ no padrão XX.XXX.XXX/YYYY-ZZ.

### `generate(options?): string`

Gera um CNPJ válido para testes.

**Opções:**
- `alphanumeric: boolean` - Se true, gera CNPJ alfanumérico
- `root: string` - Raiz específica (8 caracteres)
- `branch: number` - Número da filial (padrão: 1)

### `getInfo(cnpj: string): CNPJInfo | null`

Retorna informações detalhadas do CNPJ.

## 🔄 CNPJ Alfanumérico 2026

A partir de julho de 2026, a Receita Federal implementará o novo formato de CNPJ alfanumérico:

```typescript
// Formato atual (numérico)
validate('11.222.333/0001-81');

// Novo formato (alfanumérico)
validate('AB.CDE.123/0001-45');
```

O validador suporta ambos os formatos de forma transparente.

## 🧪 Testes

```bash
npm test
npm run test:coverage
```

## 📄 Licença

MIT
