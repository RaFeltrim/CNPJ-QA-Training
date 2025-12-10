/**
 * CNPJ Validator - TypeScript/JavaScript
 * 
 * Validador completo de CNPJ brasileiro com suporte ao novo formato
 * alfanumérico que será implementado pela Receita Federal em julho de 2026.
 * 
 * @author Rafael Feltrim
 * @license MIT
 * @version 2.0.0
 */

/**
 * Tabela de conversão de caracteres para valores numéricos.
 * Usada no cálculo dos dígitos verificadores para CNPJs alfanuméricos.
 */
const ASCII_MAP: Record<string, number> = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 17, 'B': 18, 'C': 19, 'D': 20, 'E': 21,
    'F': 22, 'G': 23, 'H': 24, 'I': 25, 'J': 26,
    'K': 27, 'L': 28, 'M': 29, 'N': 30, 'O': 31,
    'P': 32, 'Q': 33, 'R': 34, 'S': 35, 'T': 36,
    'U': 37, 'V': 38, 'W': 39, 'X': 40, 'Y': 41,
    'Z': 42
};

/**
 * Pesos para cálculo do primeiro dígito verificador
 */
const WEIGHTS_DV1: number[] = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];

/**
 * Pesos para cálculo do segundo dígito verificador
 */
const WEIGHTS_DV2: number[] = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];

/**
 * Interface para o resultado da validação
 */
export interface ValidationResult {
    valid: boolean;
    cnpjInput: string;
    cnpjClean: string;
    cnpjFormatted: string;
    isAlphanumeric: boolean;
    isMatrix: boolean;
    branchNumber: number;
    errors: string[];
}

/**
 * Interface para informações detalhadas do CNPJ
 */
export interface CNPJInfo {
    root: string;         // 8 primeiros caracteres
    branch: string;       // 4 dígitos da filial
    checkDigits: string;  // 2 dígitos verificadores
    isMatrix: boolean;
    branchNumber: number;
}

/**
 * Classe principal do validador de CNPJ
 */
export class CNPJValidator {
    
    /**
     * Remove caracteres de formatação do CNPJ
     */
    private static cleanCNPJ(cnpj: string): string {
        if (!cnpj) return '';
        return cnpj.replace(/[.\-\/\s]/g, '').toUpperCase();
    }

    /**
     * Verifica se o CNPJ contém caracteres alfanuméricos na raiz
     */
    private static isAlphanumeric(cnpjClean: string): boolean {
        if (cnpjClean.length < 8) return false;
        const root = cnpjClean.substring(0, 8);
        return /[A-Z]/.test(root);
    }

    /**
     * Converte um caractere para seu valor numérico
     */
    private static charToValue(char: string): number {
        const value = ASCII_MAP[char.toUpperCase()];
        if (value === undefined) {
            throw new Error(`Caractere inválido: ${char}`);
        }
        return value;
    }

    /**
     * Calcula os dígitos verificadores
     */
    private static calculateCheckDigits(cnpjBase: string): [number, number] {
        // Primeiro DV
        let sum = 0;
        for (let i = 0; i < 12; i++) {
            sum += this.charToValue(cnpjBase[i]) * WEIGHTS_DV1[i];
        }
        let remainder = sum % 11;
        const dv1 = remainder < 2 ? 0 : 11 - remainder;

        // Segundo DV
        sum = 0;
        const cnpjWithDV1 = cnpjBase + dv1.toString();
        for (let i = 0; i < 13; i++) {
            sum += this.charToValue(cnpjWithDV1[i]) * WEIGHTS_DV2[i];
        }
        remainder = sum % 11;
        const dv2 = remainder < 2 ? 0 : 11 - remainder;

        return [dv1, dv2];
    }

    /**
     * Formata o CNPJ no padrão XX.XXX.XXX/YYYY-ZZ
     */
    static format(cnpj: string): string {
        const clean = this.cleanCNPJ(cnpj);
        if (clean.length !== 14) return cnpj;
        
        return `${clean.substring(0, 2)}.${clean.substring(2, 5)}.${clean.substring(5, 8)}/` +
               `${clean.substring(8, 12)}-${clean.substring(12, 14)}`;
    }

    /**
     * Valida um CNPJ (numérico ou alfanumérico)
     */
    static validate(cnpj: string): ValidationResult {
        const result: ValidationResult = {
            valid: false,
            cnpjInput: cnpj,
            cnpjClean: '',
            cnpjFormatted: '',
            isAlphanumeric: false,
            isMatrix: false,
            branchNumber: 0,
            errors: []
        };

        // Verificar entrada nula ou vazia
        if (!cnpj || cnpj.trim() === '') {
            result.errors.push('CNPJ não informado');
            return result;
        }

        // Limpar CNPJ
        const cnpjClean = this.cleanCNPJ(cnpj);
        result.cnpjClean = cnpjClean;

        // Verificar tamanho
        if (cnpjClean.length !== 14) {
            result.errors.push(`CNPJ deve ter 14 caracteres, recebeu ${cnpjClean.length}`);
            return result;
        }

        // Verificar caracteres válidos
        const validCharsRegex = /^[A-Z0-9]{8}[0-9]{6}$/;
        if (!validCharsRegex.test(cnpjClean)) {
            result.errors.push('CNPJ contém caracteres inválidos');
            return result;
        }

        // Verificar se todos os caracteres são iguais
        if (new Set(cnpjClean.split('')).size === 1) {
            result.errors.push('CNPJ não pode ter todos os caracteres iguais');
            return result;
        }

        // Identificar tipo
        result.isAlphanumeric = this.isAlphanumeric(cnpjClean);

        // Extrair partes
        const root = cnpjClean.substring(0, 8);
        const branch = cnpjClean.substring(8, 12);
        const checkDigits = cnpjClean.substring(12, 14);
        
        result.branchNumber = parseInt(branch, 10);
        result.isMatrix = result.branchNumber === 1;

        // Calcular e verificar dígitos verificadores
        try {
            const [expectedDV1, expectedDV2] = this.calculateCheckDigits(root + branch);
            const expectedCheckDigits = `${expectedDV1}${expectedDV2}`;

            if (checkDigits !== expectedCheckDigits) {
                result.errors.push('Dígitos verificadores inválidos');
                return result;
            }
        } catch (error) {
            result.errors.push(`Erro ao calcular DV: ${error}`);
            return result;
        }

        // CNPJ válido
        result.valid = true;
        result.cnpjFormatted = this.format(cnpjClean);
        
        return result;
    }

    /**
     * Método de conveniência para validação rápida
     */
    static isValid(cnpj: string): boolean {
        return this.validate(cnpj).valid;
    }

    /**
     * Obtém informações detalhadas do CNPJ
     */
    static getInfo(cnpj: string): CNPJInfo | null {
        const validation = this.validate(cnpj);
        if (!validation.valid) return null;

        const cnpjClean = validation.cnpjClean;
        return {
            root: cnpjClean.substring(0, 8),
            branch: cnpjClean.substring(8, 12),
            checkDigits: cnpjClean.substring(12, 14),
            isMatrix: validation.isMatrix,
            branchNumber: validation.branchNumber
        };
    }

    /**
     * Gera um CNPJ válido para testes
     */
    static generate(options?: {
        alphanumeric?: boolean;
        root?: string;
        branch?: number;
    }): string {
        const opts = {
            alphanumeric: false,
            root: '',
            branch: 1,
            ...options
        };

        let root: string;
        
        if (opts.root && opts.root.length === 8) {
            root = opts.root.toUpperCase();
        } else if (opts.alphanumeric) {
            // Gerar raiz alfanumérica aleatória
            const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
            root = '';
            for (let i = 0; i < 8; i++) {
                root += chars.charAt(Math.floor(Math.random() * chars.length));
            }
        } else {
            // Gerar raiz numérica aleatória
            root = '';
            for (let i = 0; i < 8; i++) {
                root += Math.floor(Math.random() * 10).toString();
            }
        }

        const branch = opts.branch.toString().padStart(4, '0');
        const base = root + branch;
        
        const [dv1, dv2] = this.calculateCheckDigits(base);
        const cnpj = base + dv1.toString() + dv2.toString();

        return this.format(cnpj);
    }
}

// Exports para uso direto
export const validate = CNPJValidator.validate.bind(CNPJValidator);
export const isValid = CNPJValidator.isValid.bind(CNPJValidator);
export const format = CNPJValidator.format.bind(CNPJValidator);
export const generate = CNPJValidator.generate.bind(CNPJValidator);
export const getInfo = CNPJValidator.getInfo.bind(CNPJValidator);

export default CNPJValidator;
