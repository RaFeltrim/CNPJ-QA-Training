"""
Test Hub - Aplicação Principal (Backend Flask)
==============================================

Este é o arquivo principal do Test Hub, responsável por:
1. Configurar o servidor web Flask
2. Definir as rotas (endpoints) da API
3. Servir os arquivos estáticos (HTML, CSS, JS)
4. Integrar os serviços de execução de testes e geração de relatórios

CONCEITOS IMPORTANTES PARA APRENDIZADO:
---------------------------------------

1. FLASK: É um "microframework" web para Python.
   - "Micro" significa que é minimalista, sem muitas dependências
   - Perfeito para APIs simples e aplicações pequenas
   - Usa decoradores (@app.route) para definir rotas

2. ROTAS (ENDPOINTS): São os caminhos URL que a aplicação responde
   - GET /api/projects → retorna lista de projetos
   - POST /api/projects/{id}/run → inicia execução de testes
   - Cada rota é associada a uma função Python

3. API REST: Padrão de arquitetura para APIs web
   - GET: buscar dados
   - POST: criar/executar algo
   - PUT: atualizar
   - DELETE: remover

4. JSON: Formato de troca de dados entre frontend e backend
   - Fácil de ler para humanos
   - Fácil de processar para máquinas

COMO EXECUTAR:
--------------
    cd test_hub
    pip install -r requirements.txt
    python app.py

    Acesse: http://localhost:5000
"""

# ============================================================================
# IMPORTS
# ============================================================================

# Flask e utilitários
from flask import Flask, jsonify, request, Response, send_from_directory, render_template
from flask_cors import CORS

# Bibliotecas padrão do Python
import json
import os
from datetime import datetime

# Nossos serviços (módulos que criamos)
from services.test_runner import TestRunner, runner_manager
from services.report_generator import ReportGenerator


# ============================================================================
# CONFIGURAÇÃO DO FLASK
# ============================================================================

# Cria a instância do Flask
# __name__ ajuda o Flask a encontrar os arquivos (templates, static)
app = Flask(
    __name__,
    static_folder='static',      # Pasta com CSS, JS e imagens
    template_folder='templates'  # Pasta com arquivos HTML
)

# Habilita CORS (Cross-Origin Resource Sharing)
# Isso permite que o frontend (mesmo em outra porta) acesse o backend
# Em produção, você limitaria isso a domínios específicos
CORS(app)

# Configurações da aplicação
app.config['JSON_AS_ASCII'] = False  # Permite caracteres UTF-8 no JSON


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def load_projects_config():
    """
    Carrega a configuração dos projetos de teste do arquivo JSON.
    
    O arquivo projects.json contém a lista de todos os projetos
    de teste cadastrados no hub, com suas configurações.
    
    Returns:
        Lista de dicionários com configurações dos projetos
    """
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'projects.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('projects', [])
    except FileNotFoundError:
        # Se o arquivo não existir, retorna lista vazia
        print(f"⚠️  Arquivo de configuração não encontrado: {config_path}")
        return []
    except json.JSONDecodeError as e:
        # Se o JSON estiver mal formatado
        print(f"❌ Erro ao ler configuração: {e}")
        return []


def get_project_by_id(project_id: str):
    """
    Busca um projeto específico pelo seu ID.
    
    Args:
        project_id: Identificador único do projeto
        
    Returns:
        Dicionário com configuração do projeto, ou None se não encontrado
    """
    projects = load_projects_config()
    for project in projects:
        if project.get('id') == project_id:
            return project
    return None


# ============================================================================
# ROTAS DA PÁGINA WEB (HTML)
# ============================================================================

@app.route('/')
def index():
    """
    Rota principal - Serve a página HTML do hub.
    
    Quando alguém acessa http://localhost:5000/ no navegador,
    esta função é chamada e retorna o arquivo index.html.
    
    O decorador @app.route('/') associa a URL '/' a esta função.
    """
    return render_template('index.html')


# ============================================================================
# ROTAS DA API - PROJETOS
# ============================================================================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """
    API: Lista todos os projetos de teste cadastrados.
    
    Endpoint: GET /api/projects
    
    Retorna informações básicas de cada projeto para exibir nos cards:
    - id: identificador único
    - name: nome para exibição
    - description: descrição breve
    - icon: emoji ou ícone
    - status: se tem execução em andamento
    
    Returns:
        JSON com lista de projetos
    """
    projects = load_projects_config()
    
    # Enriquece os projetos com status atual
    enriched_projects = []
    for project in projects:
        project_status = runner_manager.get_runner_status(project['id'])
        
        enriched_projects.append({
            'id': project['id'],
            'name': project['name'],
            'description': project['description'],
            'icon': project.get('icon', '🧪'),
            'test_framework': project.get('test_framework', 'unknown'),
            'status': project_status['status'] if project_status else 'idle',
            'test_types': list(project.get('test_types', {}).keys())
        })
    
    return jsonify({
        'success': True,
        'projects': enriched_projects
    })


@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id: str):
    """
    API: Obtém detalhes de um projeto específico.
    
    Endpoint: GET /api/projects/{project_id}
    
    Args:
        project_id: ID do projeto (vem da URL)
        
    Returns:
        JSON com detalhes do projeto ou erro 404
    """
    project = get_project_by_id(project_id)
    
    if not project:
        return jsonify({
            'success': False,
            'error': f'Projeto não encontrado: {project_id}'
        }), 404
    
    # Obtém status atual de execução
    runner_status = runner_manager.get_runner_status(project_id)
    
    return jsonify({
        'success': True,
        'project': {
            **project,
            'execution_status': runner_status['status'] if runner_status else 'idle',
            'progress': runner_status['progress'] if runner_status else None
        }
    })


# ============================================================================
# ROTAS DA API - EXECUÇÃO DE TESTES
# ============================================================================

@app.route('/api/projects/<project_id>/run', methods=['POST'])
def run_tests(project_id: str):
    """
    API: Inicia a execução dos testes de um projeto.
    
    Endpoint: POST /api/projects/{project_id}/run
    
    Este endpoint é chamado quando o usuário clica em "Executar Testes".
    Ele inicia a execução em background e retorna imediatamente.
    
    O frontend deve então fazer polling no endpoint /progress
    para acompanhar o andamento.
    
    Args:
        project_id: ID do projeto
        
    Returns:
        JSON indicando se a execução foi iniciada com sucesso
    """
    project = get_project_by_id(project_id)
    
    if not project:
        return jsonify({
            'success': False,
            'error': f'Projeto não encontrado: {project_id}'
        }), 404
    
    # Obtém ou cria o runner para este projeto
    runner = runner_manager.get_runner(project_id, project)
    
    # Tenta iniciar os testes
    started = runner.start_tests()
    
    if started:
        return jsonify({
            'success': True,
            'message': f'Execução de testes iniciada para {project["name"]}',
            'project_id': project_id
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Já existe uma execução em andamento para este projeto'
        }), 409  # 409 = Conflict


@app.route('/api/projects/<project_id>/progress', methods=['GET'])
def get_progress(project_id: str):
    """
    API: Obtém o progresso atual da execução de testes.
    
    Endpoint: GET /api/projects/{project_id}/progress
    
    O frontend chama este endpoint periodicamente (polling)
    para atualizar a interface com o progresso em tempo real.
    
    Args:
        project_id: ID do projeto
        
    Returns:
        JSON com status e dados de progresso
    """
    project = get_project_by_id(project_id)
    
    if not project:
        return jsonify({
            'success': False,
            'error': f'Projeto não encontrado: {project_id}'
        }), 404
    
    runner_status = runner_manager.get_runner_status(project_id)
    
    if runner_status:
        return jsonify({
            'success': True,
            'status': runner_status['status'],
            'progress': runner_status['progress']
        })
    else:
        return jsonify({
            'success': True,
            'status': 'idle',
            'progress': None
        })


@app.route('/api/projects/<project_id>/stream', methods=['GET'])
def stream_output(project_id: str):
    """
    API: Stream de saída em tempo real usando Server-Sent Events (SSE).
    
    Endpoint: GET /api/projects/{project_id}/stream
    
    O QUE É SSE (Server-Sent Events)?
    ---------------------------------
    É uma tecnologia que permite ao servidor enviar dados para o cliente
    automaticamente, sem o cliente precisar ficar perguntando.
    
    Diferente do polling (onde o cliente pergunta repetidamente),
    com SSE o servidor "empurra" os dados quando disponíveis.
    
    É mais eficiente que polling para atualizações em tempo real.
    
    Args:
        project_id: ID do projeto
        
    Returns:
        Stream de eventos SSE
    """
    project = get_project_by_id(project_id)
    
    if not project:
        return jsonify({
            'success': False,
            'error': f'Projeto não encontrado: {project_id}'
        }), 404
    
    runner = runner_manager.get_runner(project_id, project)
    
    # Retorna uma resposta de streaming
    # mimetype='text/event-stream' indica que é SSE
    return Response(
        runner.stream_output(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )


@app.route('/api/projects/<project_id>/cancel', methods=['POST'])
def cancel_tests(project_id: str):
    """
    API: Cancela a execução de testes em andamento.
    
    Endpoint: POST /api/projects/{project_id}/cancel
    
    Args:
        project_id: ID do projeto
        
    Returns:
        JSON indicando se o cancelamento foi bem-sucedido
    """
    runner_status = runner_manager.get_runner_status(project_id)
    
    if not runner_status:
        return jsonify({
            'success': False,
            'error': 'Nenhuma execução encontrada para este projeto'
        }), 404
    
    project = get_project_by_id(project_id)
    runner = runner_manager.get_runner(project_id, project)
    cancelled = runner.cancel()
    
    return jsonify({
        'success': cancelled,
        'message': 'Execução cancelada' if cancelled else 'Não havia execução para cancelar'
    })


# ============================================================================
# ROTAS DA API - RELATÓRIOS
# ============================================================================

@app.route('/api/projects/<project_id>/report', methods=['GET'])
def generate_report(project_id: str):
    """
    API: Gera um relatório consolidado dos resultados.
    
    Endpoint: GET /api/projects/{project_id}/report
    
    Query Parameters:
        format: 'json' ou 'markdown' (padrão: 'json')
        save: 'true' para salvar em arquivo (padrão: 'false')
    
    Args:
        project_id: ID do projeto
        
    Returns:
        JSON com o relatório ou arquivo para download
    """
    project = get_project_by_id(project_id)
    
    if not project:
        return jsonify({
            'success': False,
            'error': f'Projeto não encontrado: {project_id}'
        }), 404
    
    runner_status = runner_manager.get_runner_status(project_id)
    
    if not runner_status or not runner_status['progress']:
        return jsonify({
            'success': False,
            'error': 'Nenhum resultado de execução encontrado. Execute os testes primeiro.'
        }), 404
    
    # Cria o gerador de relatório
    runner = runner_manager.get_runner(project_id, project)
    report_gen = ReportGenerator(
        project_name=project['name'],
        progress_data=runner_status['progress'],
        raw_results=runner.results
    )
    
    # Verifica o formato solicitado
    output_format = request.args.get('format', 'json')
    save_to_file = request.args.get('save', 'false').lower() == 'true'
    
    if output_format == 'markdown':
        report_content = report_gen.to_markdown()
        
        if save_to_file:
            reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
            saved_files = report_gen.save_report(reports_dir, formats=['md'])
            return jsonify({
                'success': True,
                'message': 'Relatório salvo com sucesso',
                'files': saved_files,
                'content': report_content
            })
        
        return Response(
            report_content,
            mimetype='text/markdown',
            headers={
                'Content-Disposition': f'attachment; filename=report_{project_id}.md'
            }
        )
    else:
        report = report_gen.generate_report()
        
        if save_to_file:
            reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
            saved_files = report_gen.save_report(reports_dir, formats=['json'])
            return jsonify({
                'success': True,
                'message': 'Relatório salvo com sucesso',
                'files': saved_files,
                'report': report
            })
        
        return jsonify({
            'success': True,
            'report': report
        })


# ============================================================================
# TRATAMENTO DE ERROS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """
    Handler para erros 404 (página/recurso não encontrado).
    
    Quando alguém acessa uma URL que não existe,
    este handler retorna uma resposta amigável.
    """
    return jsonify({
        'success': False,
        'error': 'Recurso não encontrado'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handler para erros 500 (erro interno do servidor).
    
    Quando ocorre um erro inesperado no servidor,
    este handler retorna uma resposta sem expor detalhes técnicos.
    """
    return jsonify({
        'success': False,
        'error': 'Erro interno do servidor'
    }), 500


# ============================================================================
# PONTO DE ENTRADA DA APLICAÇÃO
# ============================================================================

if __name__ == '__main__':
    """
    Este bloco só é executado quando rodamos o arquivo diretamente:
        python app.py
    
    Não é executado quando o arquivo é importado como módulo.
    
    Parâmetros do app.run():
    - debug=True: Recarrega automaticamente quando o código muda
    - host='0.0.0.0': Aceita conexões de qualquer IP (não só localhost)
    - port=5000: Porta onde o servidor escuta
    
    ⚠️  Em PRODUÇÃO, não use debug=True nem app.run() diretamente.
        Use um servidor WSGI como Gunicorn ou uWSGI.
    """
    print("=" * 60)
    print("🧪 Test Hub - Central de Testes Automatizados")
    print("=" * 60)
    print()
    print("📍 Servidor iniciando em: http://localhost:5050")
    print("📁 Projetos configurados em: config/projects.json")
    print()
    print("Pressione Ctrl+C para encerrar")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5050)
