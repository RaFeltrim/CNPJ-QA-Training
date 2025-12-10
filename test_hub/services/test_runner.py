"""
Test Runner Service - Serviço de Execução de Testes
===================================================

Este módulo é responsável por executar os testes de cada projeto cadastrado.
Ele utiliza subprocess para rodar comandos de terminal (como pytest) e
captura a saída em tempo real para atualizar o frontend.

Conceitos importantes para aprendizado:
---------------------------------------
1. SUBPROCESS: Permite executar comandos do sistema operacional a partir do Python
2. THREADING: Permite executar tarefas em paralelo sem bloquear o servidor
3. QUEUE: Estrutura de dados thread-safe para comunicação entre threads
4. GENERATOR: Função que retorna valores incrementalmente (yield)
"""

import subprocess
import threading
import json
import os
import re
import time
from queue import Queue
from datetime import datetime
from typing import Dict, List, Optional, Generator, Any


class TestRunner:
    """
    Classe responsável por executar testes e monitorar o progresso.
    
    Atributos:
        project_config: Configuração do projeto de teste
        status: Status atual da execução ('idle', 'running', 'completed', 'failed')
        progress: Dicionário com informações de progresso
        results: Resultados finais dos testes
    """
    
    def __init__(self, project_config: Dict[str, Any]):
        """
        Inicializa o TestRunner com a configuração do projeto.
        
        Args:
            project_config: Dicionário com configurações do projeto (de projects.json)
        """
        # Armazena a configuração do projeto (nome, caminho, comando, etc.)
        self.project_config = project_config
        
        # Status inicial: ocioso, aguardando comando de execução
        self.status = 'idle'
        
        # Dicionário para armazenar o progresso da execução
        # Será atualizado em tempo real durante a execução
        self.progress = {
            'current_test': None,      # Teste sendo executado no momento
            'tests_run': 0,            # Total de testes executados
            'tests_passed': 0,         # Testes que passaram
            'tests_failed': 0,         # Testes que falharam
            'tests_skipped': 0,        # Testes ignorados/pulados
            'suites': {},              # Status de cada suíte/arquivo de teste
            'started_at': None,        # Timestamp de início
            'finished_at': None,       # Timestamp de fim
            'output_lines': [],        # Linhas de saída do terminal
            'percentage': 0            # Porcentagem de conclusão
        }
        
        # Resultados finais após execução completa
        self.results = None
        
        # Fila para comunicação thread-safe entre a thread de execução e o servidor
        self._output_queue = Queue()
        
        # Thread que executa os testes (para não bloquear o servidor)
        self._runner_thread = None
        
        # Flag para indicar se a execução foi cancelada
        self._cancelled = False
        
    def start_tests(self) -> bool:
        """
        Inicia a execução dos testes em uma thread separada.
        
        Por que usar uma thread separada?
        ---------------------------------
        Se executássemos os testes na thread principal do servidor Flask,
        o servidor ficaria "travado" até os testes terminarem, sem poder
        responder a outras requisições HTTP (como consultas de progresso).
        
        Returns:
            True se a execução foi iniciada, False se já estava em execução
        """
        # Verifica se já existe uma execução em andamento
        if self.status == 'running':
            return False
        
        # Reseta o estado para uma nova execução
        self._reset_state()
        
        # Marca o status como "em execução"
        self.status = 'running'
        self.progress['started_at'] = datetime.now().isoformat()
        
        # Cria e inicia a thread de execução
        # target: função que será executada na thread
        # daemon=True: a thread será finalizada quando o programa principal terminar
        self._runner_thread = threading.Thread(target=self._run_tests, daemon=True)
        self._runner_thread.start()
        
        return True
    
    def _reset_state(self):
        """
        Reseta o estado interno para uma nova execução.
        Chamado antes de iniciar uma nova bateria de testes.
        """
        self._cancelled = False
        self.results = None
        self.progress = {
            'current_test': None,
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'tests_skipped': 0,
            'suites': {},
            'started_at': None,
            'finished_at': None,
            'output_lines': [],
            'percentage': 0
        }
        # Limpa a fila de saída
        while not self._output_queue.empty():
            self._output_queue.get()
    
    def _run_tests(self):
        """
        Método interno que executa os testes em subprocess.
        Roda em uma thread separada para não bloquear o servidor.
        
        Fluxo de execução:
        1. Monta o comando a ser executado (pytest + argumentos)
        2. Inicia o subprocess com captura de saída
        3. Lê a saída linha por linha (em tempo real)
        4. Analisa cada linha para atualizar o progresso
        5. Ao terminar, consolida os resultados
        """
        try:
            # Define o diretório de trabalho (onde os testes serão executados)
            # O caminho é relativo ao diretório do test_hub
            hub_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            project_path = os.path.normpath(
                os.path.join(hub_dir, self.project_config.get('path', '.'))
            )
            
            # Garante que o diretório de reports existe
            reports_dir = os.path.join(hub_dir, 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            # Monta o comando a ser executado
            # IMPORTANTE: Usamos sys.executable para garantir que o pytest
            # seja executado com o mesmo Python que está rodando o servidor.
            # Isso resolve o problema de "comando não encontrado" quando
            # pytest está instalado apenas no ambiente virtual.
            # 
            # Ao invés de: ['pytest', ...]
            # Usamos: [sys.executable, '-m', 'pytest', ...]
            import sys
            base_command = self.project_config['command']
            
            # Se o comando for pytest, rodamos como módulo Python
            if base_command in ('pytest', 'py.test'):
                command = [sys.executable, '-m', 'pytest'] + self.project_config.get('args', [])
            else:
                # Para outros comandos, tenta usar diretamente
                command = [base_command] + self.project_config.get('args', [])
            
            # Inicializa as suítes de teste com status "pendente"
            test_types = self.project_config.get('test_types', {})
            for test_type, files in test_types.items():
                for file in files:
                    self.progress['suites'][file] = {
                        'status': 'pending',  # pending, running, passed, failed
                        'type': test_type,
                        'tests_passed': 0,
                        'tests_failed': 0,
                        'tests_skipped': 0
                    }
            
            # Inicia o subprocess
            # subprocess.Popen permite executar comandos externos e capturar a saída
            # 
            # Parâmetros importantes:
            # - stdout=subprocess.PIPE: captura a saída padrão
            # - stderr=subprocess.STDOUT: redireciona erros para stdout
            # - text=True: retorna strings ao invés de bytes
            # - bufsize=1: buffer de linha (saída disponível a cada linha)
            # - cwd: diretório de trabalho onde o comando será executado
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=project_path,
                # No Windows, evita abrir uma janela de console
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            # Lê a saída linha por linha em tempo real
            # Isso permite atualizar o progresso enquanto os testes rodam
            for line in iter(process.stdout.readline, ''):
                if self._cancelled:
                    process.terminate()
                    break
                    
                # Remove espaços em branco do início e fim
                line = line.strip()
                if line:
                    # Adiciona a linha à lista de saída (para exibir no frontend)
                    self.progress['output_lines'].append(line)
                    
                    # Analisa a linha para atualizar o progresso
                    self._parse_output_line(line)
                    
                    # Coloca a linha na fila para streaming
                    self._output_queue.put(line)
            
            # Aguarda o processo terminar e obtém o código de retorno
            process.wait()
            
            # Tenta ler o arquivo JSON de resultados (se pytest-json-report estiver instalado)
            self._load_json_results()
            
            # Atualiza o status final baseado no código de retorno
            # 0 = sucesso, qualquer outro valor = falha
            if process.returncode == 0:
                self.status = 'completed'
            else:
                self.status = 'failed' if self.progress['tests_failed'] > 0 else 'completed'
                
        except FileNotFoundError as e:
            # Erro comum: comando não encontrado (ex: pytest não instalado)
            self.status = 'failed'
            error_msg = f"Erro: Comando '{self.project_config['command']}' não encontrado. Verifique se está instalado."
            self.progress['output_lines'].append(error_msg)
            self._output_queue.put(error_msg)
            
        except Exception as e:
            # Captura qualquer outro erro inesperado
            self.status = 'failed'
            error_msg = f"Erro durante execução: {str(e)}"
            self.progress['output_lines'].append(error_msg)
            self._output_queue.put(error_msg)
            
        finally:
            # Marca o timestamp de fim
            self.progress['finished_at'] = datetime.now().isoformat()
            # Sinaliza fim do streaming
            self._output_queue.put(None)
    
    def _parse_output_line(self, line: str):
        """
        Analisa uma linha de saída do pytest para atualizar o progresso.
        
        O pytest tem um formato específico de saída que podemos interpretar:
        - Linhas com "PASSED" indicam testes que passaram
        - Linhas com "FAILED" indicam testes que falharam
        - Linhas com "SKIPPED" indicam testes ignorados
        - A linha de resumo final contém totais
        
        Args:
            line: Uma linha de saída do pytest
        """
        # Padrão para detectar resultado de teste individual
        # Exemplo: "tests/test_numeric_validator.py::test_cnpj_valido PASSED"
        test_result_pattern = r'(tests/[^\s:]+\.py)::(\S+)\s+(PASSED|FAILED|SKIPPED|ERROR)'
        match = re.search(test_result_pattern, line)
        
        if match:
            file_name = match.group(1).split('/')[-1]  # Extrai nome do arquivo
            test_name = match.group(2)                  # Nome do teste
            result = match.group(3)                     # PASSED, FAILED, etc.
            
            # Atualiza o teste atual sendo exibido
            self.progress['current_test'] = f"{file_name}::{test_name}"
            
            # Incrementa contadores baseado no resultado
            self.progress['tests_run'] += 1
            
            if result == 'PASSED':
                self.progress['tests_passed'] += 1
            elif result in ('FAILED', 'ERROR'):
                self.progress['tests_failed'] += 1
            elif result == 'SKIPPED':
                self.progress['tests_skipped'] += 1
            
            # Atualiza status da suíte (arquivo de teste)
            if file_name in self.progress['suites']:
                suite = self.progress['suites'][file_name]
                suite['status'] = 'running'
                if result == 'PASSED':
                    suite['tests_passed'] += 1
                elif result in ('FAILED', 'ERROR'):
                    suite['tests_failed'] += 1
                elif result == 'SKIPPED':
                    suite['tests_skipped'] += 1
        
        # Detecta início de um arquivo de teste
        # Exemplo: "tests/test_numeric_validator.py ."
        file_start_pattern = r'^(tests/[^\s]+\.py)\s'
        file_match = re.match(file_start_pattern, line)
        if file_match:
            file_name = file_match.group(1).split('/')[-1]
            if file_name in self.progress['suites']:
                self.progress['suites'][file_name]['status'] = 'running'
        
        # Detecta linha de resumo final
        # Exemplo: "====== 42 passed, 3 failed, 1 skipped in 2.34s ======"
        summary_pattern = r'(\d+)\s+passed|(\d+)\s+failed|(\d+)\s+skipped|(\d+)\s+error'
        if '=' in line and ('passed' in line or 'failed' in line):
            # Finaliza todas as suítes em execução
            for suite in self.progress['suites'].values():
                if suite['status'] == 'running':
                    if suite['tests_failed'] > 0:
                        suite['status'] = 'failed'
                    else:
                        suite['status'] = 'passed'
            
            # Calcula porcentagem final
            self.progress['percentage'] = 100
    
    def _load_json_results(self):
        """
        Tenta carregar os resultados do pytest em formato JSON.
        
        O pytest-json-report é um plugin que gera um arquivo JSON detalhado
        com todos os resultados dos testes. Se estiver instalado e configurado,
        usamos esses dados para um relatório mais rico.
        """
        try:
            hub_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(hub_dir, 'reports', 'latest_result.json')
            
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    self.results = json.load(f)
        except Exception:
            # Se não conseguir carregar, não é crítico
            pass
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Retorna o estado atual do progresso da execução.
        
        Este método é chamado pelo frontend periodicamente (polling)
        para atualizar a interface com o progresso em tempo real.
        
        Returns:
            Dicionário com status e informações de progresso
        """
        return {
            'status': self.status,
            'progress': self.progress
        }
    
    def stream_output(self) -> Generator[str, None, None]:
        """
        Generator que produz linhas de saída em tempo real.
        
        O que é um Generator?
        --------------------
        É uma função especial do Python que usa 'yield' ao invés de 'return'.
        Ela não retorna todos os valores de uma vez, mas um por vez,
        cada vez que o código que a chamou pede o próximo valor.
        
        Isso é perfeito para streaming: enviamos cada linha assim que disponível,
        sem esperar todos os testes terminarem.
        
        Yields:
            Linhas de saída formatadas como Server-Sent Events (SSE)
        """
        while True:
            # Aguarda uma nova linha na fila (bloqueia até haver dados)
            line = self._output_queue.get()
            
            # None sinaliza fim do streaming
            if line is None:
                yield f"data: {json.dumps({'type': 'end', 'status': self.status})}\n\n"
                break
            
            # Formata como Server-Sent Event
            # SSE é um padrão para streaming do servidor para o cliente
            yield f"data: {json.dumps({'type': 'output', 'line': line})}\n\n"
    
    def cancel(self) -> bool:
        """
        Cancela a execução dos testes em andamento.
        
        Returns:
            True se havia uma execução para cancelar, False caso contrário
        """
        if self.status == 'running':
            self._cancelled = True
            self.status = 'cancelled'
            return True
        return False


# ============================================================================
# GERENCIADOR DE RUNNERS
# ============================================================================

class TestRunnerManager:
    """
    Gerenciador que mantém instâncias de TestRunner para cada projeto.
    
    Por que ter um gerenciador?
    --------------------------
    Queremos manter o estado de cada projeto separadamente.
    Por exemplo, se temos 3 projetos, cada um pode estar em um estado diferente:
    - Projeto A: executando testes
    - Projeto B: ocioso
    - Projeto C: execução concluída com falhas
    
    O gerenciador mantém essa separação organizada.
    """
    
    def __init__(self):
        """Inicializa o gerenciador com dicionário vazio de runners."""
        self._runners: Dict[str, TestRunner] = {}
    
    def get_runner(self, project_id: str, project_config: Dict[str, Any]) -> TestRunner:
        """
        Obtém ou cria um runner para um projeto específico.
        
        Args:
            project_id: Identificador único do projeto
            project_config: Configuração do projeto
            
        Returns:
            Instância de TestRunner para o projeto
        """
        if project_id not in self._runners:
            self._runners[project_id] = TestRunner(project_config)
        return self._runners[project_id]
    
    def get_runner_status(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém o status de um runner específico.
        
        Args:
            project_id: Identificador do projeto
            
        Returns:
            Dicionário com status e progresso, ou None se não existir
        """
        if project_id in self._runners:
            return self._runners[project_id].get_progress()
        return None


# Instância global do gerenciador (Singleton pattern)
# Isso permite que todas as rotas do Flask acessem o mesmo gerenciador
runner_manager = TestRunnerManager()
