# 🟢 Exercícios Nível Básico - Suporte 100%

## Objetivo

Exercícios com guia completo para iniciantes. Cada passo é detalhado
com explicações e código modelo. O foco é aprender os conceitos
fundamentais de testes em sistemas legados.

---

## Exercício 1: Criando Seu Primeiro Teste de Caracterização

### Contexto

Você recebeu uma função legada que formata CEPs. Não há documentação.

```python
# legacy/cep_utils.py
def fmt_cep(c):
    if not c: return c
    c = ''.join(x for x in str(c) if x.isdigit())
    if len(c) != 8: return c
    return f'{c[:5]}-{c[5:]}'
```

### Tarefa

Criar testes de caracterização para documentar o comportamento da função.

### Passo a Passo

#### Passo 1: Criar arquivo de teste

Crie um arquivo `test_characterization_cep.py`:

```python
# test_characterization_cep.py
"""
Testes de Caracterização para fmt_cep()

OBJETIVO: Descobrir e documentar o que essa função faz.
"""

import pytest

# Vamos importar a função (ajuste o caminho se necessário)
from legacy.cep_utils import fmt_cep


class TestCharacterizationFmtCep:
    """Documentação do comportamento de fmt_cep() via testes."""
    pass
```

#### Passo 2: Testar valores nulos

Primeiro, vamos descobrir o que acontece com valores nulos:

```python
class TestCharacterizationFmtCep:
    """Documentação do comportamento de fmt_cep() via testes."""
    
    class TestValoresNulos:
        """O que acontece com valores nulos ou vazios?"""
        
        def test_none_retorna_none(self):
            """
            DESCOBERTA: None como input retorna None.
            
            Isso significa que a função não lança exceção,
            apenas retorna o próprio valor.
            """
            resultado = fmt_cep(None)
            # Descubra: imprima para ver o que retorna
            print(f"fmt_cep(None) = {resultado}")
            
            # Depois de descobrir, documente:
            assert resultado is None
        
        def test_string_vazia_retorna_string_vazia(self):
            """
            DESCOBERTA: String vazia retorna string vazia.
            
            A função trata strings vazias como valor "falsy".
            """
            resultado = fmt_cep("")
            print(f"fmt_cep('') = {resultado}")
            
            assert resultado == ""
```

#### Passo 3: Testar CEPs válidos

```python
        def test_cep_8_digitos_formata(self):
            """
            DESCOBERTA: CEP com 8 dígitos é formatado com hífen.
            
            Formato de saída: XXXXX-XXX
            """
            resultado = fmt_cep("01310100")
            print(f"fmt_cep('01310100') = {resultado}")
            
            assert resultado == "01310-100"
        
        def test_cep_ja_formatado_reformata(self):
            """
            DESCOBERTA: CEP já formatado é reformatado.
            
            A função remove caracteres não numéricos e reformata.
            """
            resultado = fmt_cep("01310-100")
            print(f"fmt_cep('01310-100') = {resultado}")
            
            assert resultado == "01310-100"
```

#### Passo 4: Testar casos de borda

```python
        def test_cep_tamanho_errado_retorna_original(self):
            """
            DESCOBERTA: CEP com tamanho errado retorna o valor limpo.
            
            ⚠️ ATENÇÃO: Não valida, apenas retorna!
            Isso pode ser um problema de segurança de dados.
            """
            resultado = fmt_cep("123")
            print(f"fmt_cep('123') = {resultado}")
            
            # A função retorna "123" (limpo, mas não formatado)
            assert resultado == "123"
        
        def test_cep_com_letras_remove_letras(self):
            """
            DESCOBERTA: Letras são removidas silenciosamente.
            
            O CEP "01310ABC" vira "01310" (7 dígitos) e não formata.
            """
            resultado = fmt_cep("01310ABC")
            print(f"fmt_cep('01310ABC') = {resultado}")
            
            # Só sobram 5 dígitos, não formata
            assert resultado == "01310"
```

#### Passo 5: Executar e validar

```bash
# Rodar os testes
pytest test_characterization_cep.py -v -s

# O -s mostra os prints para você ver os resultados
```

### Resultado Esperado

```text
test_characterization_cep.py::TestCharacterizationFmtCep::TestValoresNulos::test_none_retorna_none PASSED
test_characterization_cep.py::TestCharacterizationFmtCep::TestValoresNulos::test_string_vazia_retorna_string_vazia PASSED
...

====================== 6 passed in 0.02s ======================
```

### O Que Você Aprendeu

✅ Como explorar código desconhecido com testes
✅ Como documentar comportamento via asserts
✅ Como identificar comportamentos estranhos (CEP inválido não dá erro)
✅ A importância de testar casos de borda

---

## Exercício 2: Criando um Golden Master Simples

### Contexto

Você precisa garantir que uma função de cálculo de impostos não mude
durante uma refatoração.

```python
# legacy/tax_calculator.py
def calc_tax(valor, tipo='icms'):
    if not valor or valor < 0: return 0
    taxas = {'icms': 0.18, 'iss': 0.05, 'pis': 0.0165, 'cofins': 0.076}
    taxa = taxas.get(tipo, 0)
    return round(valor * taxa, 2)
```

### Tarefa

Criar um Golden Master que capture o comportamento atual.

### Passo a Passo

#### Passo 1: Criar casos de teste

```python
# test_golden_master_tax.py
"""
Golden Master para calc_tax()

Captura todos os resultados possíveis para garantir
que refatorações não mudem o comportamento.
"""

import json
from pathlib import Path
from legacy.tax_calculator import calc_tax


def gerar_casos_teste():
    """
    Gera todos os casos de teste possíveis.
    
    Combinações:
    - Valores: None, -1, 0, 100, 1000, 99999.99
    - Tipos: 'icms', 'iss', 'pis', 'cofins', 'invalido'
    """
    valores = [None, -1, 0, 100, 1000, 99999.99]
    tipos = ['icms', 'iss', 'pis', 'cofins', 'invalido']
    
    casos = {}
    
    for valor in valores:
        for tipo in tipos:
            # Criar chave única para este caso
            chave = f"valor={valor}|tipo={tipo}"
            
            # Executar função e capturar resultado
            resultado = calc_tax(valor, tipo)
            
            casos[chave] = resultado
    
    return casos


def salvar_golden_master(casos, arquivo='golden_master_tax.json'):
    """Salva os casos como Golden Master."""
    with open(arquivo, 'w') as f:
        json.dump(casos, f, indent=2)
    print(f"✅ Golden Master salvo em {arquivo}")
    print(f"   Total de casos: {len(casos)}")


def carregar_golden_master(arquivo='golden_master_tax.json'):
    """Carrega Golden Master existente."""
    with open(arquivo, 'r') as f:
        return json.load(f)


# === MODO CAPTURA ===
# Execute uma vez para criar o Golden Master

if __name__ == '__main__':
    casos = gerar_casos_teste()
    salvar_golden_master(casos)
```

#### Passo 2: Criar teste de comparação

```python
# test_golden_master_tax.py (continuação)

import pytest


class TestGoldenMasterTax:
    """Testa calc_tax contra o Golden Master."""
    
    @pytest.fixture
    def golden_master(self):
        """Carrega o Golden Master."""
        return carregar_golden_master()
    
    @pytest.fixture
    def casos_atuais(self):
        """Gera casos com a implementação atual."""
        return gerar_casos_teste()
    
    def test_comparar_com_golden_master(self, golden_master, casos_atuais):
        """
        Compara todos os casos atuais com o Golden Master.
        
        Se QUALQUER resultado for diferente, o teste falha.
        """
        diferencas = []
        
        for chave, esperado in golden_master.items():
            atual = casos_atuais.get(chave)
            
            if atual != esperado:
                diferencas.append({
                    'caso': chave,
                    'esperado': esperado,
                    'atual': atual
                })
        
        # Se houver diferenças, falhar com relatório
        if diferencas:
            msg = "❌ DIFERENÇAS ENCONTRADAS:\n"
            for d in diferencas:
                msg += f"\n  Caso: {d['caso']}\n"
                msg += f"  Esperado: {d['esperado']}\n"
                msg += f"  Atual: {d['atual']}\n"
            
            pytest.fail(msg)
        
        print(f"\n✅ Todos os {len(golden_master)} casos conferem!")
```

#### Passo 3: Executar

```bash
# 1. Primeiro, criar o Golden Master
python test_golden_master_tax.py

# 2. Depois, rodar os testes
pytest test_golden_master_tax.py -v
```

### O Que Você Aprendeu

✅ Como capturar comportamento em arquivo
✅ Como comparar execuções atuais com referência
✅ A importância de cobrir todas as combinações
✅ Como detectar regressões automaticamente

---

## Exercício 3: Primeiro Facade Strangler Fig

### Contexto

Você tem uma função legada e uma nova. Precisa criar um facade
para migrar gradualmente.

```python
# Função legada
def validar_email_legado(email):
    """Validação simples (só verifica @)."""
    return '@' in str(email) if email else False

# Função nova (mais completa)
def validar_email_novo(email):
    """Validação completa com regex."""
    import re
    if not email:
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email)))
```

### Tarefa

Criar um facade que permita migrar entre as duas implementações.

### Passo a Passo

#### Passo 1: Criar o facade básico

```python
# email_facade.py
"""
Strangler Fig Facade para migração de validador de email.
"""


class EmailValidatorFacade:
    """
    Facade que permite trocar entre implementação legada e nova.
    
    Uso:
        # Começar com legado
        facade = EmailValidatorFacade(usar_novo=False)
        resultado = facade.validar("teste@email.com")
        
        # Migrar para novo
        facade.usar_novo = True
        resultado = facade.validar("teste@email.com")
    """
    
    def __init__(self, usar_novo=False):
        """
        Inicializa o facade.
        
        Args:
            usar_novo: Se True, usa implementação nova. Se False, usa legada.
        """
        self.usar_novo = usar_novo
    
    def _validar_legado(self, email):
        """Chama validação legada."""
        return '@' in str(email) if email else False
    
    def _validar_novo(self, email):
        """Chama validação nova."""
        import re
        if not email:
            return False
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, str(email)))
    
    def validar(self, email):
        """
        Valida email usando a implementação configurada.
        
        Args:
            email: Email a validar
            
        Returns:
            True se válido, False caso contrário
        """
        if self.usar_novo:
            return self._validar_novo(email)
        else:
            return self._validar_legado(email)
    
    def validar_comparando(self, email):
        """
        Valida com AMBAS implementações e retorna comparação.
        
        Útil para encontrar divergências durante migração.
        
        Returns:
            Dict com resultados de ambas implementações
        """
        resultado_legado = self._validar_legado(email)
        resultado_novo = self._validar_novo(email)
        
        return {
            'email': email,
            'legado': resultado_legado,
            'novo': resultado_novo,
            'match': resultado_legado == resultado_novo
        }
```

#### Passo 2: Criar testes para o facade

```python
# test_email_facade.py
"""
Testes para o EmailValidatorFacade.
"""

import pytest
from email_facade import EmailValidatorFacade


class TestEmailFacade:
    """Testes do facade de validação de email."""
    
    @pytest.fixture
    def facade_legado(self):
        """Facade configurado para usar legado."""
        return EmailValidatorFacade(usar_novo=False)
    
    @pytest.fixture
    def facade_novo(self):
        """Facade configurado para usar novo."""
        return EmailValidatorFacade(usar_novo=True)
    
    # === Testes do modo legado ===
    
    def test_legado_aceita_email_simples(self, facade_legado):
        """Legado aceita qualquer coisa com @."""
        assert facade_legado.validar("a@b") == True
    
    def test_legado_aceita_email_incompleto(self, facade_legado):
        """
        Legado aceita emails incompletos!
        
        ⚠️ PROBLEMA: "teste@" é aceito pelo legado.
        """
        assert facade_legado.validar("teste@") == True
    
    # === Testes do modo novo ===
    
    def test_novo_aceita_email_valido(self, facade_novo):
        """Novo aceita email válido completo."""
        assert facade_novo.validar("teste@email.com") == True
    
    def test_novo_rejeita_email_incompleto(self, facade_novo):
        """
        Novo rejeita emails incompletos.
        
        ✅ CORREÇÃO: "teste@" é rejeitado pelo novo.
        """
        assert facade_novo.validar("teste@") == False
    
    # === Testes de paridade ===
    
    def test_encontrar_divergencias(self, facade_legado):
        """Encontra casos onde legado e novo divergem."""
        emails_teste = [
            "teste@email.com",    # Ambos aceitam
            "teste@",             # Legado aceita, novo rejeita
            "a@b",                # Legado aceita, novo rejeita
            "invalido",           # Ambos rejeitam
            "",                   # Ambos rejeitam
        ]
        
        divergencias = []
        
        for email in emails_teste:
            resultado = facade_legado.validar_comparando(email)
            if not resultado['match']:
                divergencias.append(resultado)
        
        # Imprimir divergências encontradas
        print("\n📋 DIVERGÊNCIAS ENCONTRADAS:")
        for d in divergencias:
            print(f"  Email: '{d['email']}'")
            print(f"    Legado: {d['legado']}")
            print(f"    Novo:   {d['novo']}")
        
        # Este teste não falha, apenas documenta
        assert len(divergencias) > 0, "Deveria haver divergências"
```

#### Passo 3: Executar e analisar

```bash
pytest test_email_facade.py -v -s
```

### O Que Você Aprendeu

✅ Como criar um facade para migração gradual
✅ Como comparar implementações para encontrar divergências
✅ A importância de testar ambas implementações
✅ Como documentar diferenças de comportamento

---

## Checklist de Conclusão

Após completar os exercícios básicos, você deve ser capaz de:

- [ ] Criar testes de caracterização para código desconhecido
- [ ] Implementar Golden Master simples com JSON
- [ ] Construir facade básico para Strangler Fig Pattern
- [ ] Identificar divergências entre implementações
- [ ] Documentar comportamentos estranhos em testes

**Próximo**: [02-exercicios-intermediario.md](02-exercicios-intermediario.md)
