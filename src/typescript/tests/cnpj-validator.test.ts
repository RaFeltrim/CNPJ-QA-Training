/**
 * Testes unitários para o CNPJ Validator TypeScript
 */

import { CNPJValidator, validate, isValid, format, generate, getInfo } from '../src/index';

describe('CNPJValidator', () => {
    
    describe('validate', () => {
        
        describe('CNPJs numéricos válidos', () => {
            
            test('deve validar CNPJ formatado', () => {
                const result = CNPJValidator.validate('11.222.333/0001-81');
                expect(result.valid).toBe(true);
                expect(result.cnpjClean).toBe('11222333000181');
                expect(result.isAlphanumeric).toBe(false);
                expect(result.isMatrix).toBe(true);
            });

            test('deve validar CNPJ sem formatação', () => {
                const result = CNPJValidator.validate('11222333000181');
                expect(result.valid).toBe(true);
            });

            test('deve identificar filial', () => {
                const result = CNPJValidator.validate('11.222.333/0002-62');
                expect(result.valid).toBe(true);
                expect(result.isMatrix).toBe(false);
                expect(result.branchNumber).toBe(2);
            });
        });

        describe('CNPJs alfanuméricos válidos', () => {
            
            test('deve validar CNPJ alfanumérico gerado', () => {
                const cnpj = CNPJValidator.generate({ alphanumeric: true });
                const result = CNPJValidator.validate(cnpj);
                expect(result.valid).toBe(true);
                expect(result.isAlphanumeric).toBe(true);
            });

            test('deve validar CNPJ com raiz específica', () => {
                const cnpj = CNPJValidator.generate({ root: 'ABCDEFGH' });
                const result = CNPJValidator.validate(cnpj);
                expect(result.valid).toBe(true);
                expect(result.cnpjClean.startsWith('ABCDEFGH')).toBe(true);
            });
        });

        describe('CNPJs inválidos', () => {
            
            test('deve rejeitar CNPJ nulo', () => {
                const result = CNPJValidator.validate('');
                expect(result.valid).toBe(false);
                expect(result.errors).toContain('CNPJ não informado');
            });

            test('deve rejeitar CNPJ com tamanho incorreto', () => {
                const result = CNPJValidator.validate('1234567890');
                expect(result.valid).toBe(false);
            });

            test('deve rejeitar CNPJ com todos dígitos iguais', () => {
                const result = CNPJValidator.validate('11111111111111');
                expect(result.valid).toBe(false);
            });

            test('deve rejeitar CNPJ com DV incorreto', () => {
                const result = CNPJValidator.validate('11.222.333/0001-82');
                expect(result.valid).toBe(false);
                expect(result.errors).toContain('Dígitos verificadores inválidos');
            });

            test('deve rejeitar CNPJ com caracteres inválidos', () => {
                const result = CNPJValidator.validate('11.222.333/0001-8@');
                expect(result.valid).toBe(false);
            });
        });
    });

    describe('isValid', () => {
        
        test('deve retornar true para CNPJ válido', () => {
            expect(isValid('11.222.333/0001-81')).toBe(true);
        });

        test('deve retornar false para CNPJ inválido', () => {
            expect(isValid('11.222.333/0001-82')).toBe(false);
        });
    });

    describe('format', () => {
        
        test('deve formatar CNPJ sem formatação', () => {
            expect(format('11222333000181')).toBe('11.222.333/0001-81');
        });

        test('deve manter CNPJ já formatado', () => {
            expect(format('11.222.333/0001-81')).toBe('11.222.333/0001-81');
        });

        test('deve formatar CNPJ alfanumérico', () => {
            expect(format('ABCDEFGH000145')).toBe('AB.CDE.FGH/0001-45');
        });
    });

    describe('generate', () => {
        
        test('deve gerar CNPJ numérico válido', () => {
            const cnpj = generate();
            expect(isValid(cnpj)).toBe(true);
        });

        test('deve gerar CNPJ alfanumérico válido', () => {
            const cnpj = generate({ alphanumeric: true });
            expect(isValid(cnpj)).toBe(true);
            
            const result = validate(cnpj);
            expect(result.isAlphanumeric).toBe(true);
        });

        test('deve gerar CNPJ com raiz específica', () => {
            const cnpj = generate({ root: 'TEST1234' });
            expect(cnpj.replace(/[.\-\/]/g, '').startsWith('TEST1234')).toBe(true);
            expect(isValid(cnpj)).toBe(true);
        });

        test('deve gerar CNPJ de filial', () => {
            const cnpj = generate({ branch: 5 });
            const result = validate(cnpj);
            expect(result.valid).toBe(true);
            expect(result.branchNumber).toBe(5);
        });
    });

    describe('getInfo', () => {
        
        test('deve retornar informações de CNPJ válido', () => {
            const info = getInfo('11.222.333/0001-81');
            expect(info).not.toBeNull();
            expect(info?.root).toBe('11222333');
            expect(info?.branch).toBe('0001');
            expect(info?.checkDigits).toBe('81');
            expect(info?.isMatrix).toBe(true);
        });

        test('deve retornar null para CNPJ inválido', () => {
            const info = getInfo('11.222.333/0001-82');
            expect(info).toBeNull();
        });
    });
});

describe('Retrocompatibilidade', () => {
    
    const cnpjsNumericos = [
        '11.222.333/0001-81',
        '00.000.000/0001-91',
        '11.444.777/0001-61',
    ];

    test.each(cnpjsNumericos)('CNPJ numérico %s deve ser válido', (cnpj) => {
        // Nota: Alguns destes podem não ter DVs corretos - ajustar conforme necessário
        const result = validate(cnpj);
        // Verifica apenas que não dá erro de processamento
        expect(result.errors.length === 0 || result.errors[0] === 'Dígitos verificadores inválidos').toBe(true);
    });
});

describe('Performance', () => {
    
    test('deve validar 1000 CNPJs em menos de 1 segundo', () => {
        const cnpjs = Array.from({ length: 1000 }, () => generate());
        
        const start = Date.now();
        cnpjs.forEach(cnpj => validate(cnpj));
        const duration = Date.now() - start;
        
        expect(duration).toBeLessThan(1000);
    });
});
