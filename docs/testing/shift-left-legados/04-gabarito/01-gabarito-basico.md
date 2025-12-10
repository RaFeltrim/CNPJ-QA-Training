# 📝 Gabarito - Exercícios Básicos

## Exercício 1: Teste de Caracterização para CEP

### Solução Completa

```python
# test_characterization_cep.py
"""
Testes de Caracterização para fmt_cep()

OBJETIVO: Documentar completamente o comportamento da função.
"""

import pytest


# Simulando a função legada
def fmt_cep(c):
    if not c: return c
    c = ''.join(x for x in str(c) if x.isdigit())
    if len(c) != 8: return c
    return f'{c[:5]}-{c[5:]}'


class TestCharacterizationFmtCep:
    """Documentação do comportamento de fmt_cep() via testes."""
    
    class TestValoresNulos:
        """O que acontece com valores nulos ou vazios?"""
        
        def test_none_retorna_none(self):
            """
            DESCOBERTA: None como input retorna None.
            
            Razão: A condição `if not c` é True para None.
            """
            assert fmt_cep(None) is None
        
        def test_string_vazia_retorna_string_vazia(self):
            """
            DESCOBERTA: String vazia retorna string vazia.
            
            Razão: "" é falsy em Python, então `if not c` é True.
            """
            assert fmt_cep("") == ""
        
        def test_zero_retorna_zero(self):
            """
            DESCOBERTA: 0 retorna 0.
            
            Razão: 0 também é falsy em Python.
            """
            assert fmt_cep(0) == 0
    
    class TestCEPsValidos:
        """Comportamento com CEPs de 8 dígitos."""
        
        def test_cep_8_digitos_formata(self):
            """CEP com 8 dígitos é formatado corretamente."""
            assert fmt_cep("01310100") == "01310-100"
        
        def test_cep_ja_formatado_reformata(self):
            """CEP já formatado é normalizado e reformatado."""
            assert fmt_cep("01310-100") == "01310-100"
        
        def test_cep_com_espacos_formata(self):
            """Espaços são removidos antes de formatar."""
            assert fmt_cep("01310 100") == "01310-100"
        
        def test_cep_com_pontos_formata(self):
            """Pontos são removidos antes de formatar."""
            assert fmt_cep("01.310.100") == "01310-100"
        
        def test_cep_numerico_inteiro(self):
            """
            DESCOBERTA: Aceita número inteiro.
            
            O str() converte antes de processar.
            """
            assert fmt_cep(1310100) == "01310-100"
    
    class TestCEPsTamanhoErrado:
        """Comportamento com CEPs de tamanho incorreto."""
        
        def test_cep_curto_retorna_limpo(self):
            """
            DESCOBERTA: CEP curto retorna valor limpo (só dígitos).
            
            ⚠️ PROBLEMA: Não valida! Aceita qualquer tamanho.
            """
            assert fmt_cep("123") == "123"
        
        def test_cep_longo_retorna_limpo(self):
            """CEP longo demais retorna valor limpo."""
            assert fmt_cep("123456789012") == "123456789012"
        
        def test_cep_7_digitos_nao_formata(self):
            """CEP com 7 dígitos não é formatado."""
            assert fmt_cep("0131010") == "0131010"
        
        def test_cep_9_digitos_nao_formata(self):
            """CEP com 9 dígitos não é formatado."""
            assert fmt_cep("013101001") == "013101001"
    
    class TestCEPsComLetras:
        """Comportamento com inputs contendo letras."""
        
        def test_letras_sao_removidas(self):
            """
            DESCOBERTA: Letras são silenciosamente removidas.
            
            O filtro isdigit() remove qualquer não-dígito.
            """
            assert fmt_cep("01310ABC") == "01310"
        
        def test_somente_letras_retorna_vazio(self):
            """String só com letras retorna string vazia."""
            assert fmt_cep("ABCDEFGH") == ""
        
        def test_cep_com_letras_no_meio(self):
            """Letras no meio são removidas."""
            assert fmt_cep("01X31Y01Z00") == "01310100"  # Tem 8 dígitos!
    
    class TestCasosEspeciais:
        """Casos especiais e de borda."""
        
        def test_cep_com_caracteres_especiais(self):
            """Caracteres especiais são removidos."""
            assert fmt_cep("01310@#$100") == "01310-100"
        
        def test_cep_todos_zeros(self):
            """CEP com todos zeros é formatado."""
            assert fmt_cep("00000000") == "00000-000"
        
        def test_cep_todos_noves(self):
            """CEP com todos noves é formatado."""
            assert fmt_cep("99999999") == "99999-999"


# Resumo das descobertas
"""
RESUMO DO COMPORTAMENTO DE fmt_cep():

1. INPUTS FALSY (None, "", 0):
   - Retorna o próprio valor sem processar

2. LIMPEZA:
   - Remove TUDO que não é dígito (letras, espaços, pontos, etc)
   - Silenciosamente, sem erro

3. FORMATAÇÃO:
   - SÓ formata se tiver EXATAMENTE 8 dígitos após limpeza
   - Formato de saída: XXXXX-XXX

4. VALIDAÇÃO:
   - NÃO VALIDA! Qualquer sequência de dígitos é aceita
   - CEPs inválidos ou de tamanho errado simplesmente não são formatados

⚠️ PROBLEMAS IDENTIFICADOS:
   - Não há validação de CEP válido
   - Erros silenciosos podem mascarar problemas
   - "00000-000" é aceito como CEP válido
"""
```

---

## Exercício 2: Golden Master para Cálculo de Impostos

### Solução Completa

```python
# test_golden_master_tax.py
"""
Golden Master para calc_tax()
"""

import json
import pytest
from pathlib import Path


# Função legada
def calc_tax(valor, tipo='icms'):
    if not valor or valor < 0: return 0
    taxas = {'icms': 0.18, 'iss': 0.05, 'pis': 0.0165, 'cofins': 0.076}
    taxa = taxas.get(tipo, 0)
    return round(valor * taxa, 2)


class GoldenMasterTax:
    """Gerenciador de Golden Master para calc_tax."""
    
    GOLDEN_FILE = Path("golden_masters/tax_calculator.json")
    
    @classmethod
    def gerar_casos_teste(cls) -> dict:
        """
        Gera todos os casos de teste possíveis.
        """
        valores = [
            None,           # Nulo
            -100,           # Negativo
            -0.01,          # Negativo pequeno
            0,              # Zero
            0.01,           # Muito pequeno
            1,              # Unitário
            100,            # Comum
            1000,           # Mil
            10000,          # Dez mil
            99999.99,       # Grande
            100000000,      # Muito grande
            0.001,          # Precisão
        ]
        
        tipos = [
            'icms',         # 18%
            'iss',          # 5%
            'pis',          # 1.65%
            'cofins',       # 7.6%
            'invalido',     # Tipo não existe
            '',             # Vazio
            None,           # Nulo
        ]
        
        casos = {}
        
        for valor in valores:
            for tipo in tipos:
                chave = f"calc_tax({valor}, '{tipo}')"
                try:
                    resultado = calc_tax(valor, tipo)
                except Exception as e:
                    resultado = f"EXCEPTION: {type(e).__name__}: {str(e)}"
                
                casos[chave] = resultado
        
        return casos
    
    @classmethod
    def capturar(cls):
        """Captura Golden Master."""
        cls.GOLDEN_FILE.parent.mkdir(exist_ok=True)
        casos = cls.gerar_casos_teste()
        
        with open(cls.GOLDEN_FILE, 'w') as f:
            json.dump(casos, f, indent=2)
        
        print(f"✅ Golden Master capturado: {cls.GOLDEN_FILE}")
        print(f"   Total de casos: {len(casos)}")
        
        return casos
    
    @classmethod
    def carregar(cls) -> dict:
        """Carrega Golden Master existente."""
        with open(cls.GOLDEN_FILE, 'r') as f:
            return json.load(f)
    
    @classmethod
    def comparar(cls, casos_atuais: dict) -> dict:
        """Compara com Golden Master."""
        golden = cls.carregar()
        
        diferencas = []
        matches = 0
        
        for chave, esperado in golden.items():
            atual = casos_atuais.get(chave)
            
            if atual != esperado:
                diferencas.append({
                    'caso': chave,
                    'esperado': esperado,
                    'atual': atual
                })
            else:
                matches += 1
        
        # Verificar novos casos
        novos = []
        for chave in casos_atuais:
            if chave not in golden:
                novos.append(chave)
        
        return {
            'passed': len(diferencas) == 0,
            'total': len(golden),
            'matches': matches,
            'diferencas': diferencas,
            'novos_casos': novos
        }


class TestGoldenMasterTax:
    """Testes usando Golden Master."""
    
    @pytest.mark.capture
    def test_capturar_golden_master(self):
        """Captura novo Golden Master."""
        casos = GoldenMasterTax.capturar()
        assert len(casos) > 0
    
    def test_comparar_com_golden_master(self):
        """Compara implementação atual com Golden Master."""
        if not GoldenMasterTax.GOLDEN_FILE.exists():
            pytest.skip("Golden Master não existe. Execute pytest -m capture primeiro.")
        
        casos_atuais = GoldenMasterTax.gerar_casos_teste()
        relatorio = GoldenMasterTax.comparar(casos_atuais)
        
        if not relatorio['passed']:
            msg = f"\n❌ Golden Master FALHOU!\n"
            msg += f"   Matches: {relatorio['matches']}/{relatorio['total']}\n"
            msg += f"\n   DIFERENÇAS:\n"
            
            for d in relatorio['diferencas'][:5]:
                msg += f"\n   Caso: {d['caso']}\n"
                msg += f"   Esperado: {d['esperado']}\n"
                msg += f"   Atual: {d['atual']}\n"
            
            pytest.fail(msg)
        
        print(f"\n✅ Golden Master PASSOU! ({relatorio['matches']} casos)")


# Se executar diretamente, captura Golden Master
if __name__ == '__main__':
    GoldenMasterTax.capturar()
```

### Golden Master Esperado (Parcial)

```json
{
  "calc_tax(None, 'icms')": 0,
  "calc_tax(-100, 'icms')": 0,
  "calc_tax(0, 'icms')": 0,
  "calc_tax(100, 'icms')": 18.0,
  "calc_tax(1000, 'icms')": 180.0,
  "calc_tax(100, 'iss')": 5.0,
  "calc_tax(100, 'pis')": 1.65,
  "calc_tax(100, 'cofins')": 7.6,
  "calc_tax(100, 'invalido')": 0,
  "calc_tax(99999.99, 'icms')": 18000.0
}
```

---

## Exercício 3: Strangler Facade para Email

### Solução Completa

```python
# email_facade.py
"""
Strangler Fig Facade para migração de validador de email.
"""


def validar_email_legado(email):
    """Validação simples (só verifica @)."""
    return '@' in str(email) if email else False


def validar_email_novo(email):
    """Validação completa com regex."""
    import re
    if not email:
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email)))


class EmailValidatorFacade:
    """
    Facade que permite trocar entre implementação legada e nova.
    """
    
    def __init__(self, usar_novo=False):
        self.usar_novo = usar_novo
        self._comparacoes = []
    
    def _validar_legado(self, email):
        """Chama validação legada."""
        return validar_email_legado(email)
    
    def _validar_novo(self, email):
        """Chama validação nova."""
        return validar_email_novo(email)
    
    def validar(self, email):
        """Valida email usando a implementação configurada."""
        if self.usar_novo:
            return self._validar_novo(email)
        else:
            return self._validar_legado(email)
    
    def validar_comparando(self, email):
        """Valida com AMBAS implementações e retorna comparação."""
        resultado_legado = self._validar_legado(email)
        resultado_novo = self._validar_novo(email)
        
        comparacao = {
            'email': email,
            'legado': resultado_legado,
            'novo': resultado_novo,
            'match': resultado_legado == resultado_novo
        }
        
        self._comparacoes.append(comparacao)
        return comparacao
    
    def get_divergencias(self):
        """Retorna apenas as divergências encontradas."""
        return [c for c in self._comparacoes if not c['match']]
    
    def get_estatisticas(self):
        """Retorna estatísticas das comparações."""
        total = len(self._comparacoes)
        divergencias = len(self.get_divergencias())
        
        return {
            'total': total,
            'matches': total - divergencias,
            'divergencias': divergencias,
            'taxa_divergencia': f"{(divergencias/total*100):.1f}%" if total > 0 else "N/A"
        }


# === Testes ===

import pytest


class TestEmailFacade:
    """Testes do facade de validação de email."""
    
    @pytest.fixture
    def facade_legado(self):
        return EmailValidatorFacade(usar_novo=False)
    
    @pytest.fixture
    def facade_novo(self):
        return EmailValidatorFacade(usar_novo=True)
    
    # === Testes Modo Legado ===
    
    class TestModoLegado:
        """Testes da implementação legada."""
        
        def test_email_valido_aceito(self):
            facade = EmailValidatorFacade(usar_novo=False)
            assert facade.validar("teste@email.com") == True
        
        def test_email_simples_aceito(self):
            """Legado aceita qualquer coisa com @."""
            facade = EmailValidatorFacade(usar_novo=False)
            assert facade.validar("a@b") == True
        
        def test_email_incompleto_aceito(self):
            """⚠️ PROBLEMA: Legado aceita emails incompletos."""
            facade = EmailValidatorFacade(usar_novo=False)
            assert facade.validar("teste@") == True
        
        def test_sem_arroba_rejeitado(self):
            facade = EmailValidatorFacade(usar_novo=False)
            assert facade.validar("testeemail.com") == False
        
        def test_none_rejeitado(self):
            facade = EmailValidatorFacade(usar_novo=False)
            assert facade.validar(None) == False
        
        def test_vazio_rejeitado(self):
            facade = EmailValidatorFacade(usar_novo=False)
            assert facade.validar("") == False
    
    # === Testes Modo Novo ===
    
    class TestModoNovo:
        """Testes da nova implementação."""
        
        def test_email_valido_aceito(self):
            facade = EmailValidatorFacade(usar_novo=True)
            assert facade.validar("teste@email.com") == True
        
        def test_email_com_ponto_aceito(self):
            facade = EmailValidatorFacade(usar_novo=True)
            assert facade.validar("teste.nome@email.com.br") == True
        
        def test_email_incompleto_rejeitado(self):
            """✅ Novo rejeita emails incompletos."""
            facade = EmailValidatorFacade(usar_novo=True)
            assert facade.validar("teste@") == False
        
        def test_email_simples_rejeitado(self):
            """Novo rejeita a@b (sem domínio completo)."""
            facade = EmailValidatorFacade(usar_novo=True)
            assert facade.validar("a@b") == False
        
        def test_none_rejeitado(self):
            facade = EmailValidatorFacade(usar_novo=True)
            assert facade.validar(None) == False
    
    # === Testes de Comparação ===
    
    class TestComparacao:
        """Testes do modo de comparação."""
        
        def test_email_valido_match(self):
            """Emails válidos têm mesmo resultado em ambos."""
            facade = EmailValidatorFacade()
            resultado = facade.validar_comparando("teste@email.com")
            
            assert resultado['match'] == True
            assert resultado['legado'] == True
            assert resultado['novo'] == True
        
        def test_email_invalido_match(self):
            """Emails claramente inválidos têm mesmo resultado."""
            facade = EmailValidatorFacade()
            resultado = facade.validar_comparando("invalido")
            
            assert resultado['match'] == True
            assert resultado['legado'] == False
            assert resultado['novo'] == False
        
        def test_divergencia_email_incompleto(self):
            """Email incompleto causa divergência."""
            facade = EmailValidatorFacade()
            resultado = facade.validar_comparando("teste@")
            
            assert resultado['match'] == False
            assert resultado['legado'] == True  # Aceita
            assert resultado['novo'] == False   # Rejeita
        
        def test_divergencia_email_simples(self):
            """a@b causa divergência."""
            facade = EmailValidatorFacade()
            resultado = facade.validar_comparando("a@b")
            
            assert resultado['match'] == False
        
        def test_estatisticas(self):
            """Estatísticas são calculadas corretamente."""
            facade = EmailValidatorFacade()
            
            # Testar vários emails
            emails = [
                "teste@email.com",   # Match
                "invalido",          # Match
                "teste@",            # Divergência
                "a@b",               # Divergência
                "",                  # Match
            ]
            
            for email in emails:
                facade.validar_comparando(email)
            
            stats = facade.get_estatisticas()
            
            assert stats['total'] == 5
            assert stats['matches'] == 3
            assert stats['divergencias'] == 2
        
        def test_get_divergencias(self):
            """get_divergencias retorna apenas divergências."""
            facade = EmailValidatorFacade()
            
            facade.validar_comparando("teste@email.com")  # Match
            facade.validar_comparando("teste@")           # Divergência
            facade.validar_comparando("a@b")              # Divergência
            
            divergencias = facade.get_divergencias()
            
            assert len(divergencias) == 2
            assert all(not d['match'] for d in divergencias)


# === Relatório de Divergências ===

def gerar_relatorio_divergencias():
    """Gera relatório completo de divergências entre implementações."""
    facade = EmailValidatorFacade()
    
    # Dataset de teste
    emails_teste = [
        # Claramente válidos
        "teste@email.com",
        "nome.sobrenome@empresa.com.br",
        "user123@mail.org",
        
        # Claramente inválidos
        "",
        None,
        "invalido",
        "sem-arroba.com",
        
        # Casos de borda (potenciais divergências)
        "a@b",
        "teste@",
        "@teste.com",
        "teste@.",
        "teste@.com",
        "teste@com",
        ".teste@email.com",
        "teste.@email.com",
        "teste..nome@email.com",
        "teste@email..com",
    ]
    
    print("=" * 60)
    print("RELATÓRIO DE DIVERGÊNCIAS - EMAIL VALIDATOR")
    print("=" * 60)
    
    for email in emails_teste:
        resultado = facade.validar_comparando(email)
        
        if not resultado['match']:
            print(f"\n⚠️ DIVERGÊNCIA: '{email}'")
            print(f"   Legado: {resultado['legado']}")
            print(f"   Novo:   {resultado['novo']}")
    
    print("\n" + "=" * 60)
    stats = facade.get_estatisticas()
    print(f"RESUMO:")
    print(f"  Total testados: {stats['total']}")
    print(f"  Matches: {stats['matches']}")
    print(f"  Divergências: {stats['divergencias']}")
    print(f"  Taxa de divergência: {stats['taxa_divergencia']}")
    print("=" * 60)


if __name__ == '__main__':
    gerar_relatorio_divergencias()
```

### Output Esperado do Relatório

```text
============================================================
RELATÓRIO DE DIVERGÊNCIAS - EMAIL VALIDATOR
============================================================

⚠️ DIVERGÊNCIA: 'a@b'
   Legado: True
   Novo:   False

⚠️ DIVERGÊNCIA: 'teste@'
   Legado: True
   Novo:   False

⚠️ DIVERGÊNCIA: '@teste.com'
   Legado: True
   Novo:   False

⚠️ DIVERGÊNCIA: 'teste@.'
   Legado: True
   Novo:   False

⚠️ DIVERGÊNCIA: 'teste@.com'
   Legado: True
   Novo:   False

⚠️ DIVERGÊNCIA: 'teste@com'
   Legado: True
   Novo:   False

============================================================
RESUMO:
  Total testados: 17
  Matches: 11
  Divergências: 6
  Taxa de divergência: 35.3%
============================================================
```

---

## Conclusão

Os exercícios básicos ensinam os fundamentos:

1. **Caracterização**: Descobrir comportamento via testes
2. **Golden Master**: Capturar e comparar comportamento
3. **Strangler Facade**: Migrar gradualmente entre implementações

Estes conceitos são a base para técnicas mais avançadas.
