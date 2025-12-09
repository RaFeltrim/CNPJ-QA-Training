# 7. Guia de Implementação - Validador de CNPJ

## Documento 7: Código, Arquitetura e Boas Práticas

---

## 1. INTRODUÇÃO

Este documento fornece um **guia prático de implementação** de validadores de CNPJ, com exemplos de código em múltiplas linguagens, arquitetura recomendada e boas práticas de desenvolvimento.

**Público-Alvo**: Desenvolvedores e QA com conhecimento em programação

**Linguagens Cobertas**: TypeScript, Python, Java, C#

---

## 2. ARQUITETURA RECOMENDADA

### 2.1 Estrutura de Diretórios

```
cnpj-validator/
├── src/
│   ├── validators/
│   │   ├── cnpj-numerico.validator.ts
│   │   ├── cnpj-alfanumerico.validator.ts
│   │   └── cnpj.validator.ts (facade)
│   ├── utils/
│   │   ├── ascii-converter.util.ts
│   │   ├── modulo11.util.ts
│   │   └── normalizer.util.ts
│   ├── types/
│   │   └── cnpj.types.ts
│   └── index.ts
├── tests/
│   ├── unit/
│   │   ├── cnpj-numerico.spec.ts
│   │   ├── cnpj-alfanumerico.spec.ts
│   │   └── utils.spec.ts
│   ├── integration/
│   │   └── cnpj-validator.spec.ts
│   └── fixtures/
│       └── cnpj-test-data.ts
├── docs/
│   └── api.md
├── package.json
├── tsconfig.json
└── README.md
```

---

### 2.2 Princípios de Design

**SOLID**:
- **S**ingle Responsibility: Cada função tem uma responsabilidade única
- **O**pen/Closed: Extensível para novos formatos sem modificar código existente
- **L**iskov Substitution: Validadores numérico e alfanumérico são intercambiáveis
- **I**nterface Segregation: Interfaces específicas para cada tipo de validação
- **D**ependency Inversion: Depender de abstrações, não de implementações

**DRY (Don't Repeat Yourself)**:
- Funções reutilizáveis para cálculo de DV
- Normalização centralizada

**KISS (Keep It Simple, Stupid)**:
- Código legível e autoexplicativo
- Evitar otimizações prematuras

---

## 3. IMPLEMENTAÇÃO EM TYPESCRIPT

### 3.1 Tipos e Interfaces

```typescript
// src/types/cnpj.types.ts

export enum FormatoCNPJ {
  NUMERICO = 'numerico',
  ALFANUMERICO = 'alfanumerico',
}

export interface ResultadoValidacao {
  valido: boolean;
  cnpj?: string;
  erro?: string;
  formato?: FormatoCNPJ;
  raiz?: string;
  ordem?: string;
  dv?: string;
}

export interface OpcoesPeso {
  primeiroDV: number[];
  segundoDV: number[];
}

export type CNPJInput = string | number;
```

---

### 3.2 Utilitários

```typescript
// src/utils/normalizer.util.ts

export class CNPJNormalizer {
  /**
   * Remove formatação e padroniza CNPJ
   */
  static normalizar(cnpj: CNPJInput): string {
    return String(cnpj)
      .replace(/\D/g, '')           // Remove não-dígitos
      .toUpperCase()                // Maiúsculas (alfanumérico)
      .trim()                       // Remove espaços
      .padStart(14, '0');           // Completa zeros à esquerda
  }

  /**
   * Formata CNPJ: XX.XXX.XXX/YYYY-ZZ
   */
  static formatar(cnpj: string): string {
    const limpo = this.normalizar(cnpj);
    return limpo.replace(
      /^(\w{2})(\w{3})(\w{3})(\w{4})(\w{2})$/,
      '$1.$2.$3/$4-$5'
    );
  }

  /**
   * Detecta se CNPJ é numérico ou alfanumérico
   */
  static detectarFormato(cnpj: string): FormatoCNPJ {
    const limpo = this.normalizar(cnpj);
    const raizOrdem = limpo.substring(0, 12);
    
    return /^[0-9]+$/.test(raizOrdem)
      ? FormatoCNPJ.NUMERICO
      : FormatoCNPJ.ALFANUMERICO;
  }

  /**
   * Valida estrutura básica (14 caracteres)
   */
  static validarEstrutura(cnpj: string): boolean {
    const limpo = this.normalizar(cnpj);
    
    if (limpo.length !== 14) {
      return false;
    }

    // DVs devem ser sempre numéricos
    const dvs = limpo.substring(12, 14);
    if (!/^[0-9]{2}$/.test(dvs)) {
      return false;
    }

    return true;
  }

  /**
   * Verifica se todos os dígitos são iguais
   */
  static todosDigitosIguais(cnpj: string): boolean {
    const limpo = this.normalizar(cnpj);
    return /^(\d)\1+$/.test(limpo);
  }
}
```

```typescript
// src/utils/ascii-converter.util.ts

export class ASCIIConverter {
  /**
   * Converte caractere para valor usado no cálculo de DV
   * Fórmula: ASCII - 48
   */
  static caracterParaValor(caractere: string): number {
    const ascii = caractere.toUpperCase().charCodeAt(0);
    return ascii - 48;
  }

  /**
   * Converte string para array de valores
   */
  static stringParaValores(str: string): number[] {
    return str.split('').map(char => this.caracterParaValor(char));
  }

  /**
   * Valida se caractere é permitido
   * Numérico: 0-9
   * Alfanumérico: 0-9, A-Z
   */
  static caracterValido(
    caractere: string,
    formato: FormatoCNPJ
  ): boolean {
    if (formato === FormatoCNPJ.NUMERICO) {
      return /^[0-9]$/.test(caractere);
    }
    return /^[0-9A-Z]$/i.test(caractere);
  }
}
```

```typescript
// src/utils/modulo11.util.ts

export class Modulo11 {
  /**
   * Calcula dígito verificador usando Módulo 11
   */
  static calcularDV(
    valores: number[],
    pesos: number[]
  ): number {
    // Multiplicar cada valor pelo seu peso
    const produtos = valores.map((valor, index) => valor * pesos[index]);
    
    // Somar todos os produtos
    const soma = produtos.reduce((acc, val) => acc + val, 0);
    
    // Calcular resto da divisão por 11
    const resto = soma % 11;
    
    // Aplicar regra: resto 0 ou 1 = DV 0, senão DV = 11 - resto
    return resto < 2 ? 0 : 11 - resto;
  }

  /**
   * Pesos para cálculo dos DVs do CNPJ
   */
  static get PESOS(): OpcoesPeso {
    return {
      primeiroDV: [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
      segundoDV: [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
    };
  }
}
```

---

### 3.3 Validador Numérico

```typescript
// src/validators/cnpj-numerico.validator.ts

import { CNPJNormalizer } from '../utils/normalizer.util';
import { Modulo11 } from '../utils/modulo11.util';
import { ASCIIConverter } from '../utils/ascii-converter.util';
import { ResultadoValidacao, FormatoCNPJ } from '../types/cnpj.types';

export class CNPJNumericoValidator {
  /**
   * Valida CNPJ numérico completo
   */
  static validar(cnpj: string): ResultadoValidacao {
    const limpo = CNPJNormalizer.normalizar(cnpj);

    // Validação de estrutura
    if (!CNPJNormalizer.validarEstrutura(limpo)) {
      return {
        valido: false,
        erro: 'CNPJ deve ter exatamente 14 caracteres',
      };
    }

    // Verifica dígitos todos iguais
    if (CNPJNormalizer.todosDigitosIguais(limpo)) {
      return {
        valido: false,
        erro: 'CNPJ não pode ter todos os dígitos iguais',
      };
    }

    // Validar caracteres (apenas numéricos)
    const raizOrdem = limpo.substring(0, 12);
    if (!/^[0-9]+$/.test(raizOrdem)) {
      return {
        valido: false,
        erro: 'CNPJ numérico deve conter apenas dígitos 0-9',
      };
    }

    // Validar dígitos verificadores
    const dvsValidos = this.validarDVs(limpo);
    if (!dvsValidos) {
      return {
        valido: false,
        erro: 'Dígitos verificadores inválidos',
      };
    }

    return {
      valido: true,
      cnpj: CNPJNormalizer.formatar(limpo),
      formato: FormatoCNPJ.NUMERICO,
      raiz: limpo.substring(0, 8),
      ordem: limpo.substring(8, 12),
      dv: limpo.substring(12, 14),
    };
  }

  /**
   * Valida dígitos verificadores
   */
  private static validarDVs(cnpj: string): boolean {
    const raizOrdem = cnpj.substring(0, 12);
    const dvsInformados = cnpj.substring(12, 14);

    // Converter para valores
    const valores = ASCIIConverter.stringParaValores(raizOrdem);

    // Calcular primeiro DV
    const primeiroDV = Modulo11.calcularDV(
      valores,
      Modulo11.PESOS.primeiroDV
    );

    // Calcular segundo DV
    const valoresComPrimeiroDV = [...valores, primeiroDV];
    const segundoDV = Modulo11.calcularDV(
      valoresComPrimeiroDV,
      Modulo11.PESOS.segundoDV
    );

    const dvsCalculados = `${primeiroDV}${segundoDV}`;
    return dvsCalculados === dvsInformados;
  }

  /**
   * Calcula dígitos verificadores para CNPJ sem DVs
   */
  static calcularDVs(cnpjSemDV: string): string {
    const limpo = CNPJNormalizer.normalizar(cnpjSemDV).substring(0, 12);
    const valores = ASCIIConverter.stringParaValores(limpo);

    const primeiroDV = Modulo11.calcularDV(
      valores,
      Modulo11.PESOS.primeiroDV
    );

    const valoresComPrimeiroDV = [...valores, primeiroDV];
    const segundoDV = Modulo11.calcularDV(
      valoresComPrimeiroDV,
      Modulo11.PESOS.segundoDV
    );

    return `${primeiroDV}${segundoDV}`;
  }
}
```

---

### 3.4 Validador Alfanumérico

```typescript
// src/validators/cnpj-alfanumerico.validator.ts

import { CNPJNormalizer } from '../utils/normalizer.util';
import { Modulo11 } from '../utils/modulo11.util';
import { ASCIIConverter } from '../utils/ascii-converter.util';
import { ResultadoValidacao, FormatoCNPJ } from '../types/cnpj.types';

export class CNPJAlfanumericoValidator {
  /**
   * Valida CNPJ alfanumérico completo
   */
  static validar(cnpj: string): ResultadoValidacao {
    const limpo = CNPJNormalizer.normalizar(cnpj);

    // Validação de estrutura
    if (!CNPJNormalizer.validarEstrutura(limpo)) {
      return {
        valido: false,
        erro: 'CNPJ deve ter exatamente 14 caracteres',
      };
    }

    // Validar caracteres permitidos
    const raizOrdem = limpo.substring(0, 12);
    if (!/^[0-9A-Z]+$/i.test(raizOrdem)) {
      return {
        valido: false,
        erro: 'CNPJ alfanumérico deve conter apenas 0-9 e A-Z',
      };
    }

    // DVs devem ser numéricos
    const dvs = limpo.substring(12, 14);
    if (!/^[0-9]{2}$/.test(dvs)) {
      return {
        valido: false,
        erro: 'Dígitos verificadores devem ser numéricos',
      };
    }

    // Validar dígitos verificadores
    const dvsValidos = this.validarDVs(limpo);
    if (!dvsValidos) {
      return {
        valido: false,
        erro: 'Dígitos verificadores inválidos',
      };
    }

    return {
      valido: true,
      cnpj: CNPJNormalizer.formatar(limpo),
      formato: FormatoCNPJ.ALFANUMERICO,
      raiz: limpo.substring(0, 8),
      ordem: limpo.substring(8, 12),
      dv: limpo.substring(12, 14),
    };
  }

  /**
   * Valida dígitos verificadores com conversão ASCII
   */
  private static validarDVs(cnpj: string): boolean {
    const raizOrdem = cnpj.substring(0, 12);
    const dvsInformados = cnpj.substring(12, 14);

    // Converter para valores ASCII
    const valores = ASCIIConverter.stringParaValores(raizOrdem);

    // Calcular primeiro DV
    const primeiroDV = Modulo11.calcularDV(
      valores,
      Modulo11.PESOS.primeiroDV
    );

    // Calcular segundo DV
    const valoresComPrimeiroDV = [...valores, primeiroDV];
    const segundoDV = Modulo11.calcularDV(
      valoresComPrimeiroDV,
      Modulo11.PESOS.segundoDV
    );

    const dvsCalculados = `${primeiroDV}${segundoDV}`;
    return dvsCalculados === dvsInformados;
  }

  /**
   * Calcula dígitos verificadores para CNPJ alfanumérico sem DVs
   */
  static calcularDVs(cnpjSemDV: string): string {
    const limpo = CNPJNormalizer.normalizar(cnpjSemDV).substring(0, 12);
    const valores = ASCIIConverter.stringParaValores(limpo);

    const primeiroDV = Modulo11.calcularDV(
      valores,
      Modulo11.PESOS.primeiroDV
    );

    const valoresComPrimeiroDV = [...valores, primeiroDV];
    const segundoDV = Modulo11.calcularDV(
      valoresComPrimeiroDV,
      Modulo11.PESOS.segundoDV
    );

    return `${primeiroDV}${segundoDV}`;
  }
}
```

---

### 3.5 Facade (Interface Unificada)

```typescript
// src/validators/cnpj.validator.ts

import { CNPJNumericoValidator } from './cnpj-numerico.validator';
import { CNPJAlfanumericoValidator } from './cnpj-alfanumerico.validator';
import { CNPJNormalizer } from '../utils/normalizer.util';
import { ResultadoValidacao, FormatoCNPJ } from '../types/cnpj.types';

export class CNPJValidator {
  /**
   * Valida CNPJ (detecta automaticamente o formato)
   */
  static validar(cnpj: string): ResultadoValidacao {
    if (!cnpj || typeof cnpj !== 'string') {
      return {
        valido: false,
        erro: 'CNPJ não pode estar vazio',
      };
    }

    const limpo = CNPJNormalizer.normalizar(cnpj);
    const formato = CNPJNormalizer.detectarFormato(limpo);

    if (formato === FormatoCNPJ.NUMERICO) {
      return CNPJNumericoValidator.validar(limpo);
    } else {
      return CNPJAlfanumericoValidator.validar(limpo);
    }
  }

  /**
   * Valida apenas se é válido (retorna boolean)
   */
  static ehValido(cnpj: string): boolean {
    return this.validar(cnpj).valido;
  }

  /**
   * Calcula DVs para CNPJ sem dígitos verificadores
   */
  static calcularDVs(cnpjSemDV: string): string {
    const limpo = CNPJNormalizer.normalizar(cnpjSemDV).substring(0, 12);
    const formato = CNPJNormalizer.detectarFormato(limpo);

    if (formato === FormatoCNPJ.NUMERICO) {
      return CNPJNumericoValidator.calcularDVs(limpo);
    } else {
      return CNPJAlfanumericoValidator.calcularDVs(limpo);
    }
  }

  /**
   * Formata CNPJ
   */
  static formatar(cnpj: string): string | null {
    const resultado = this.validar(cnpj);
    return resultado.valido ? resultado.cnpj! : null;
  }
}
```

---

### 3.6 Ponto de Entrada (Index)

```typescript
// src/index.ts

export { CNPJValidator } from './validators/cnpj.validator';
export { CNPJNumericoValidator } from './validators/cnpj-numerico.validator';
export { CNPJAlfanumericoValidator } from './validators/cnpj-alfanumerico.validator';
export { CNPJNormalizer } from './utils/normalizer.util';
export { ASCIIConverter } from './utils/ascii-converter.util';
export { Modulo11 } from './utils/modulo11.util';
export * from './types/cnpj.types';

// Uso simples
import { CNPJValidator } from './validators/cnpj.validator';

const cnpj = '11.222.333/0001-81';
const resultado = CNPJValidator.validar(cnpj);

console.log(resultado);
// {
//   valido: true,
//   cnpj: '11.222.333/0001-81',
//   formato: 'numerico',
//   raiz: '11222333',
//   ordem: '0001',
//   dv: '81'
// }
```

---

## 4. TESTES UNITÁRIOS (JEST)

### 4.1 Testes do Validador Numérico

```typescript
// tests/unit/cnpj-numerico.spec.ts

import { CNPJNumericoValidator } from '../../src/validators/cnpj-numerico.validator';
import { FormatoCNPJ } from '../../src/types/cnpj.types';

describe('CNPJNumericoValidator', () => {
  describe('validar()', () => {
    test('CT-001: Deve validar CNPJ numérico válido', () => {
      const cnpj = '11.222.333/0001-81';
      const resultado = CNPJNumericoValidator.validar(cnpj);

      expect(resultado.valido).toBe(true);
      expect(resultado.formato).toBe(FormatoCNPJ.NUMERICO);
      expect(resultado.raiz).toBe('11222333');
      expect(resultado.ordem).toBe('0001');
      expect(resultado.dv).toBe('81');
    });

    test('CT-003: Deve validar CNPJ sem formatação', () => {
      const cnpj = '11222333000181';
      const resultado = CNPJNumericoValidator.validar(cnpj);

      expect(resultado.valido).toBe(true);
      expect(resultado.cnpj).toBe('11.222.333/0001-81');
    });

    test('CT-006: Deve rejeitar CNPJ com menos de 14 dígitos', () => {
      const cnpj = '11.222.333/0001-8';
      const resultado = CNPJNumericoValidator.validar(cnpj);

      expect(resultado.valido).toBe(false);
      expect(resultado.erro).toContain('14 caracteres');
    });

    test('CT-011: Deve rejeitar CNPJ com primeiro DV incorreto', () => {
      const cnpj = '11.222.333/0001-91';
      const resultado = CNPJNumericoValidator.validar(cnpj);

      expect(resultado.valido).toBe(false);
      expect(resultado.erro).toContain('verificadores');
    });

    test('CT-016: Deve rejeitar CNPJ com todos dígitos iguais', () => {
      const cnpjs = [
        '00.000.000/0000-00',
        '11.111.111/1111-11',
        '99.999.999/9999-99',
      ];

      cnpjs.forEach(cnpj => {
        const resultado = CNPJNumericoValidator.validar(cnpj);
        expect(resultado.valido).toBe(false);
        expect(resultado.erro).toContain('iguais');
      });
    });
  });

  describe('calcularDVs()', () => {
    test('Deve calcular DVs corretamente', () => {
      const cnpjSemDV = '11.222.333/0001';
      const dvs = CNPJNumericoValidator.calcularDVs(cnpjSemDV);

      expect(dvs).toBe('81');
    });
  });
});
```

---

### 4.2 Testes do Validador Alfanumérico

```typescript
// tests/unit/cnpj-alfanumerico.spec.ts

import { CNPJAlfanumericoValidator } from '../../src/validators/cnpj-alfanumerico.validator';
import { FormatoCNPJ } from '../../src/types/cnpj.types';

describe('CNPJAlfanumericoValidator', () => {
  test('CT-021: Deve validar CNPJ alfanumérico válido', () => {
    const cnpj = '12.ABC.345/01DE-35';
    const resultado = CNPJAlfanumericoValidator.validar(cnpj);

    expect(resultado.valido).toBe(true);
    expect(resultado.formato).toBe(FormatoCNPJ.ALFANUMERICO);
  });

  test('CT-024: Deve rejeitar DVs alfanuméricos', () => {
    const cnpj = '12.ABC.345/01DE-AB';
    const resultado = CNPJAlfanumericoValidator.validar(cnpj);

    expect(resultado.valido).toBe(false);
    expect(resultado.erro).toContain('numéricos');
  });

  test('CT-023: Deve rejeitar caracteres especiais', () => {
    const cnpj = '12.A@C.345/01DE-35';
    const resultado = CNPJAlfanumericoValidator.validar(cnpj);

    expect(resultado.valido).toBe(false);
    expect(resultado.erro).toContain('0-9 e A-Z');
  });
});
```

---

## 5. IMPLEMENTAÇÃO EM PYTHON

### 5.1 Validador Completo

```python
# cnpj_validator.py

import re
from enum import Enum
from typing import Optional, Dict, List

class FormatoCNPJ(Enum):
    NUMERICO = "numerico"
    ALFANUMERICO = "alfanumerico"

class CNPJValidator:
    PESOS_PRIMEIRO_DV = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    PESOS_SEGUNDO_DV = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    @staticmethod
    def normalizar(cnpj: str) -> str:
        """Remove formatação e converte para maiúsculas"""
        return re.sub(r'\D', '', str(cnpj)).upper().zfill(14)

    @staticmethod
    def formatar(cnpj: str) -> str:
        """Formata CNPJ: XX.XXX.XXX/YYYY-ZZ"""
        limpo = CNPJValidator.normalizar(cnpj)
        return f"{limpo[:2]}.{limpo[2:5]}.{limpo[5:8]}/{limpo[8:12]}-{limpo[12:]}"

    @staticmethod
    def detectar_formato(cnpj: str) -> FormatoCNPJ:
        """Detecta se CNPJ é numérico ou alfanumérico"""
        limpo = CNPJValidator.normalizar(cnpj)
        raiz_ordem = limpo[:12]
        
        return (FormatoCNPJ.NUMERICO if raiz_ordem.isdigit() 
                else FormatoCNPJ.ALFANUMERICO)

    @staticmethod
    def caractere_para_valor(caractere: str) -> int:
        """Converte caractere para valor ASCII - 48"""
        return ord(caractere.upper()) - 48

    @staticmethod
    def calcular_dv(valores: List[int], pesos: List[int]) -> int:
        """Calcula dígito verificador usando Módulo 11"""
        soma = sum(v * p for v, p in zip(valores, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    @classmethod
    def validar(cls, cnpj: str) -> Dict:
        """Valida CNPJ completo"""
        if not cnpj:
            return {"valido": False, "erro": "CNPJ não pode estar vazio"}

        limpo = cls.normalizar(cnpj)

        # Validar estrutura
        if len(limpo) != 14:
            return {"valido": False, "erro": "CNPJ deve ter 14 caracteres"}

        # Verificar dígitos todos iguais
        if len(set(limpo)) == 1:
            return {"valido": False, "erro": "Todos os dígitos são iguais"}

        # Validar DVs
        raiz_ordem = limpo[:12]
        dvs_informados = limpo[12:]

        # Converter para valores
        valores = [cls.caractere_para_valor(c) for c in raiz_ordem]

        # Calcular primeiro DV
        primeiro_dv = cls.calcular_dv(valores, cls.PESOS_PRIMEIRO_DV)

        # Calcular segundo DV
        valores_com_primeiro = valores + [primeiro_dv]
        segundo_dv = cls.calcular_dv(valores_com_primeiro, cls.PESOS_SEGUNDO_DV)

        dvs_calculados = f"{primeiro_dv}{segundo_dv}"

        if dvs_calculados != dvs_informados:
            return {"valido": False, "erro": "Dígitos verificadores inválidos"}

        return {
            "valido": True,
            "cnpj": cls.formatar(limpo),
            "formato": cls.detectar_formato(limpo).value,
            "raiz": limpo[:8],
            "ordem": limpo[8:12],
            "dv": limpo[12:],
        }

    @classmethod
    def eh_valido(cls, cnpj: str) -> bool:
        """Retorna apenas boolean"""
        return cls.validar(cnpj)["valido"]

# Uso
if __name__ == "__main__":
    cnpj = "11.222.333/0001-81"
    resultado = CNPJValidator.validar(cnpj)
    print(resultado)
```

---

### 5.2 Testes Unitários (pytest)

```python
# test_cnpj_validator.py

import pytest
from cnpj_validator import CNPJValidator, FormatoCNPJ

class TestCNPJValidator:
    def test_ct001_validar_cnpj_numerico_valido(self):
        cnpj = "11.222.333/0001-81"
        resultado = CNPJValidator.validar(cnpj)
        
        assert resultado["valido"] is True
        assert resultado["formato"] == FormatoCNPJ.NUMERICO.value
        assert resultado["raiz"] == "11222333"
        assert resultado["ordem"] == "0001"
        assert resultado["dv"] == "81"

    def test_ct006_rejeitar_cnpj_incompleto(self):
        cnpj = "11.222.333/0001-8"
        resultado = CNPJValidator.validar(cnpj)
        
        assert resultado["valido"] is False
        assert "14 caracteres" in resultado["erro"]

    def test_ct016_rejeitar_digitos_iguais(self):
        cnpjs = [
            "00.000.000/0000-00",
            "11.111.111/1111-11",
            "99.999.999/9999-99",
        ]
        
        for cnpj in cnpjs:
            resultado = CNPJValidator.validar(cnpj)
            assert resultado["valido"] is False
            assert "iguais" in resultado["erro"]

    def test_ct021_validar_cnpj_alfanumerico_valido(self):
        cnpj = "12.ABC.345/01DE-35"
        resultado = CNPJValidator.validar(cnpj)
        
        assert resultado["valido"] is True
        assert resultado["formato"] == FormatoCNPJ.ALFANUMERICO.value
```

---

## 6. BOAS PRÁTICAS

### 6.1 Performance

**✅ Faça**:
- Normalizar entrada apenas uma vez
- Usar regex compiladas
- Evitar conversões desnecessárias

**❌ Evite**:
- Validar formatação múltiplas vezes
- Criar objetos complexos em loops
- Consultar API em validações síncronas

---

### 6.2 Segurança

**✅ Faça**:
- Sanitizar entrada (prevenir XSS)
- Mascarar CNPJs em logs
- Validar comprimento antes de processar
- Usar HTTPS para consultas à API

**❌ Evite**:
- Armazenar CNPJs sem criptografia
- Logar CNPJs completos
- Confiar cegamente na entrada do usuário

---

### 6.3 Manutenibilidade

**✅ Faça**:
- Documentar com JSDoc/docstrings
- Escrever testes unitários (cobertura > 90%)
- Usar nomes descritivos
- Seguir princípios SOLID

**❌ Evite**:
- Funções com múltiplas responsabilidades
- Código duplicado
- Lógica complexa sem comentários

---

## 7. INTEGRAÇÃO COM FRAMEWORKS

### 7.1 Express.js (Middleware)

```typescript
// middleware/cnpj-validator.middleware.ts

import { Request, Response, NextFunction } from 'express';
import { CNPJValidator } from '../validators/cnpj.validator';

export function validarCNPJMiddleware(campo: string = 'cnpj') {
  return (req: Request, res: Response, next: NextFunction) => {
    const cnpj = req.body[campo] || req.params[campo] || req.query[campo];

    if (!cnpj) {
      return res.status(400).json({
        erro: `Campo ${campo} é obrigatório`,
      });
    }

    const resultado = CNPJValidator.validar(cnpj);

    if (!resultado.valido) {
      return res.status(400).json({
        erro: resultado.erro,
      });
    }

    // Armazena CNPJ normalizado no request
    req.body[`${campo}Normalizado`] = resultado.cnpj;
    next();
  };
}

// Uso
app.post('/empresas', validarCNPJMiddleware('cnpj'), (req, res) => {
  const cnpj = req.body.cnpjNormalizado;
  // ... lógica da rota
});
```

---

### 7.2 React (Hook Customizado)

```typescript
// hooks/useCNPJValidator.ts

import { useState, useCallback } from 'react';
import { CNPJValidator } from '../validators/cnpj.validator';
import type { ResultadoValidacao } from '../types/cnpj.types';

export function useCNPJValidator() {
  const [resultado, setResultado] = useState<ResultadoValidacao | null>(null);
  const [isValidating, setIsValidating] = useState(false);

  const validar = useCallback((cnpj: string) => {
    setIsValidating(true);
    
    try {
      const res = CNPJValidator.validar(cnpj);
      setResultado(res);
      return res;
    } finally {
      setIsValidating(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResultado(null);
  }, []);

  return {
    validar,
    reset,
    resultado,
    isValidating,
    valido: resultado?.valido ?? null,
    erro: resultado?.erro ?? null,
  };
}

// Uso no componente
function FormularioCNPJ() {
  const { validar, valido, erro } = useCNPJValidator();
  const [cnpj, setCNPJ] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const valor = e.target.value;
    setCNPJ(valor);
    
    if (valor.replace(/\D/g, '').length === 14) {
      validar(valor);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={cnpj}
        onChange={handleChange}
        className={valido === false ? 'error' : ''}
      />
      {valido === true && <span className="success">✓ CNPJ válido</span>}
      {valido === false && <span className="error">✗ {erro}</span>}
    </div>
  );
}
```

---

## 8. LOGGING E MONITORAMENTO

### 8.1 Logging Seguro (Winston)

```typescript
// utils/logger.util.ts

import winston from 'winston';

const maskCNPJ = (cnpj: string): string => {
  const limpo = cnpj.replace(/\D/g, '');
  if (limpo.length !== 14) return '***';
  
  return `XX.XXX.XXX/****-**`;
};

export const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json(),
    winston.format((info) => {
      // Mascarar CNPJs em logs
      if (info.cnpj) {
        info.cnpjMasked = maskCNPJ(info.cnpj);
        delete info.cnpj;
      }
      return info;
    })()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/cnpj-validator.log' }),
  ],
});

// Uso
logger.info('Validação realizada', {
  cnpj: '11.222.333/0001-81', // Será mascarado automaticamente
  resultado: 'valido',
});
```

---

## 9. DEPLOY E CI/CD

### 9.1 GitHub Actions

```yaml
# .github/workflows/test.yml

name: Testes CNPJ Validator

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Instalar dependências
        run: npm ci
      
      - name: Executar testes
        run: npm test -- --coverage
      
      - name: Verificar cobertura
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 95" | bc -l) )); then
            echo "Cobertura abaixo de 95%: $COVERAGE%"
            exit 1
          fi
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

---

## 10. DOCUMENTAÇÃO DA API

### 10.1 Swagger/OpenAPI

```yaml
# swagger.yaml

openapi: 3.0.0
info:
  title: API Validador de CNPJ
  version: 1.0.0
  description: API para validação de CNPJs numéricos e alfanuméricos

paths:
  /validar:
    post:
      summary: Valida um CNPJ
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                cnpj:
                  type: string
                  example: "11.222.333/0001-81"
              required:
                - cnpj
      responses:
        '200':
          description: Validação realizada com sucesso
          content:
            application/json:
              schema:
                type: object
                properties:
                  valido:
                    type: boolean
                  cnpj:
                    type: string
                  formato:
                    type: string
                    enum: [numerico, alfanumerico]
                  raiz:
                    type: string
                  ordem:
                    type: string
                  dv:
                    type: string
                  erro:
                    type: string
        '400':
          description: Erro de validação
```

---

## 11. CONCLUSÃO

Este guia fornece uma base sólida para implementar validadores de CNPJ em produção. Adapte o código conforme as necessidades do seu projeto, mantendo sempre:

✅ **Testes abrangentes** (cobertura > 90%)  
✅ **Código limpo** (SOLID, DRY, KISS)  
✅ **Segurança** (mascaramento, sanitização)  
✅ **Performance** (otimizações adequadas)  
✅ **Documentação** (código e API)

---

**Desenvolvido para a comunidade QA**  
*Última atualização: Dezembro 2025*
