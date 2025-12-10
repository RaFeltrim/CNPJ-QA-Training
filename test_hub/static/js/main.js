/**
 * ================================================================================
 * Test Hub - JavaScript Principal
 * ================================================================================
 * 
 * Este arquivo contém toda a lógica do frontend do Test Hub.
 * Ele gerencia:
 * - Carregamento e exibição dos projetos
 * - Execução de testes e acompanhamento de progresso
 * - Geração e exportação de relatórios
 * 
 * CONCEITOS IMPORTANTES PARA APRENDIZADO:
 * ---------------------------------------
 * 
 * 1. FETCH API: API moderna do JavaScript para fazer requisições HTTP
 *    - Substituiu o antigo XMLHttpRequest
 *    - Retorna Promises (permite usar async/await)
 * 
 * 2. ASYNC/AWAIT: Sintaxe moderna para código assíncrono
 *    - async: marca uma função como assíncrona
 *    - await: espera uma Promise resolver
 * 
 * 3. DOM MANIPULATION: Manipulação do HTML via JavaScript
 *    - document.getElementById(): busca elemento por ID
 *    - element.innerHTML: altera conteúdo HTML
 *    - element.classList: manipula classes CSS
 * 
 * 4. EVENT LISTENERS: "Ouvintes" de eventos
 *    - Permitem executar código quando algo acontece (clique, carregamento, etc.)
 * 
 * 5. POLLING: Técnica de consulta periódica
 *    - Usamos setInterval para verificar o progresso a cada X segundos
 * 
 * ================================================================================
 */

// ============================================================================
// CONFIGURAÇÕES E VARIÁVEIS GLOBAIS
// ============================================================================

/**
 * URL base da API do backend.
 * Em desenvolvimento, o Flask roda na porta 5000.
 * Em produção, você mudaria isso para o endereço do servidor.
 */
const API_BASE_URL = '';  // String vazia = mesmo servidor que serviu o HTML

/**
 * Intervalo de polling em milissegundos.
 * A cada 1 segundo, verificamos o progresso da execução.
 */
const POLLING_INTERVAL = 1000;

/**
 * Variáveis de estado da aplicação.
 * Armazenam informações sobre o estado atual do hub.
 */
let currentProjectId = null;     // ID do projeto sendo executado
let pollingIntervalId = null;    // ID do setInterval (para poder cancelar)
let executionInProgress = false; // Flag indicando se há execução em andamento
let lastReport = null;           // Último relatório gerado


// ============================================================================
// INICIALIZAÇÃO
// ============================================================================

/**
 * Evento DOMContentLoaded: dispara quando o HTML foi carregado.
 * 
 * Por que usar este evento?
 * -------------------------
 * O JavaScript pode ser executado antes do HTML estar completamente carregado.
 * Isso causaria erros ao tentar acessar elementos que ainda não existem.
 * Este evento garante que todo o HTML está disponível.
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🧪 Test Hub inicializado');
    
    // Carrega a lista de projetos
    loadProjects();
    
    // Configura os event listeners (botões, etc.)
    setupEventListeners();
});


// ============================================================================
// FUNÇÕES DE CARREGAMENTO DE PROJETOS
// ============================================================================

/**
 * Carrega a lista de projetos do backend e renderiza os cards.
 * 
 * Fluxo:
 * 1. Faz requisição GET para /api/projects
 * 2. Recebe lista de projetos em JSON
 * 3. Para cada projeto, cria um card na interface
 */
async function loadProjects() {
    try {
        // Mostra indicador de carregamento
        const projectsGrid = document.getElementById('projects-grid');
        projectsGrid.innerHTML = `
            <div class="loading-placeholder">
                <span class="loading-spinner"></span>
                <span>Carregando projetos...</span>
            </div>
        `;
        
        // Faz a requisição para a API
        // await pausa a execução até a Promise resolver
        const response = await fetch(`${API_BASE_URL}/api/projects`);
        
        // Verifica se a requisição foi bem-sucedida
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        // Converte a resposta para JSON
        const data = await response.json();
        
        // Verifica se a resposta foi bem-sucedida
        if (!data.success) {
            throw new Error(data.error || 'Erro desconhecido');
        }
        
        // Renderiza os cards dos projetos
        renderProjectCards(data.projects);
        
    } catch (error) {
        // Exibe mensagem de erro na interface
        console.error('Erro ao carregar projetos:', error);
        
        const projectsGrid = document.getElementById('projects-grid');
        projectsGrid.innerHTML = `
            <div class="loading-placeholder" style="color: var(--color-danger);">
                <span>❌ Erro ao carregar projetos: ${error.message}</span>
            </div>
        `;
    }
}

/**
 * Renderiza os cards dos projetos na interface.
 * 
 * @param {Array} projects - Lista de objetos de projeto
 */
function renderProjectCards(projects) {
    const projectsGrid = document.getElementById('projects-grid');
    
    // Se não há projetos, mostra mensagem
    if (!projects || projects.length === 0) {
        projectsGrid.innerHTML = `
            <div class="loading-placeholder">
                <span>📭 Nenhum projeto cadastrado. Adicione projetos em config/projects.json</span>
            </div>
        `;
        return;
    }
    
    // Limpa o container
    projectsGrid.innerHTML = '';
    
    // Obtém o template do card
    const template = document.getElementById('project-card-template');
    
    // Para cada projeto, cria um card
    projects.forEach(project => {
        // Clona o template
        // true = clona também os filhos (deep clone)
        const card = template.content.cloneNode(true);
        
        // Preenche os dados do card
        const cardElement = card.querySelector('.project-card');
        cardElement.dataset.projectId = project.id;
        
        card.querySelector('.card-icon').textContent = project.icon || '🧪';
        card.querySelector('.card-title').textContent = project.name;
        card.querySelector('.card-description').textContent = project.description;
        
        // Status do card
        const statusElement = card.querySelector('.card-status');
        statusElement.textContent = getStatusLabel(project.status);
        statusElement.classList.add(project.status);
        
        // Tags de tipos de teste
        const tagsContainer = card.querySelector('.card-tags');
        if (project.test_types && project.test_types.length > 0) {
            project.test_types.forEach(type => {
                const tag = document.createElement('span');
                tag.className = 'card-tag';
                tag.textContent = type;
                tagsContainer.appendChild(tag);
            });
        }
        
        // Botão de executar
        const runButton = card.querySelector('.btn-run');
        runButton.addEventListener('click', () => runTests(project.id, project.name, project.icon));
        
        // Desabilita botão se já há execução em andamento
        if (project.status === 'running') {
            runButton.disabled = true;
            runButton.textContent = '⏳ Executando...';
        }
        
        // Adiciona o card ao grid
        projectsGrid.appendChild(card);
    });
}

/**
 * Retorna o label traduzido para cada status.
 * 
 * @param {string} status - Status do projeto (idle, running, completed, failed)
 * @returns {string} Label traduzido
 */
function getStatusLabel(status) {
    const labels = {
        'idle': 'Pronto',
        'running': 'Executando',
        'completed': 'Concluído',
        'failed': 'Falhou',
        'cancelled': 'Cancelado'
    };
    return labels[status] || status;
}


// ============================================================================
// FUNÇÕES DE EXECUÇÃO DE TESTES
// ============================================================================

/**
 * Inicia a execução dos testes de um projeto.
 * 
 * @param {string} projectId - ID do projeto
 * @param {string} projectName - Nome do projeto (para exibição)
 * @param {string} projectIcon - Ícone do projeto
 */
async function runTests(projectId, projectName, projectIcon) {
    try {
        // Verifica se já há execução em andamento
        if (executionInProgress) {
            alert('Já existe uma execução em andamento. Aguarde ou cancele.');
            return;
        }
        
        console.log(`🚀 Iniciando testes do projeto: ${projectId}`);
        
        // Faz requisição POST para iniciar a execução
        const response = await fetch(`${API_BASE_URL}/api/projects/${projectId}/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Erro ao iniciar execução');
        }
        
        // Atualiza estado
        currentProjectId = projectId;
        executionInProgress = true;
        
        // Mostra a seção de execução
        showExecutionPanel(projectId, projectName, projectIcon);
        
        // Inicia o polling de progresso
        startProgressPolling(projectId);
        
        // Atualiza os cards
        loadProjects();
        
    } catch (error) {
        console.error('Erro ao iniciar testes:', error);
        alert(`Erro ao iniciar testes: ${error.message}`);
    }
}

/**
 * Exibe o painel de execução com as informações do projeto.
 * 
 * @param {string} projectId - ID do projeto
 * @param {string} projectName - Nome do projeto
 * @param {string} projectIcon - Ícone do projeto
 */
function showExecutionPanel(projectId, projectName, projectIcon) {
    // Atualiza informações do projeto
    document.getElementById('execution-project-name').textContent = projectName;
    document.getElementById('execution-project-icon').textContent = projectIcon || '🧪';
    
    // Reseta o painel
    document.getElementById('progress-fill').style.width = '0%';
    document.getElementById('stat-total').textContent = '0';
    document.getElementById('stat-passed').textContent = '0';
    document.getElementById('stat-failed').textContent = '0';
    document.getElementById('stat-skipped').textContent = '0';
    document.getElementById('suites-list').innerHTML = '';
    document.getElementById('console-output').innerHTML = '';
    
    // Mostra a seção de execução, esconde relatório
    document.getElementById('execution-section').classList.remove('hidden');
    document.getElementById('report-section').classList.add('hidden');
    
    // Scroll para a seção de execução
    document.getElementById('execution-section').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Inicia o polling periódico para atualizar o progresso.
 * 
 * O que é Polling?
 * ----------------
 * É uma técnica onde o cliente (frontend) consulta o servidor
 * periodicamente para verificar se há atualizações.
 * 
 * Alternativas:
 * - WebSockets: conexão bidirecional permanente
 * - Server-Sent Events (SSE): servidor envia eventos
 * 
 * Usamos polling aqui por ser mais simples de implementar.
 * 
 * @param {string} projectId - ID do projeto
 */
function startProgressPolling(projectId) {
    // Cancela polling anterior se existir
    if (pollingIntervalId) {
        clearInterval(pollingIntervalId);
    }
    
    // Faz primeira consulta imediatamente
    updateProgress(projectId);
    
    // Configura polling periódico
    // setInterval executa a função a cada X milissegundos
    pollingIntervalId = setInterval(() => {
        updateProgress(projectId);
    }, POLLING_INTERVAL);
}

/**
 * Consulta o progresso atual e atualiza a interface.
 * 
 * @param {string} projectId - ID do projeto
 */
async function updateProgress(projectId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/projects/${projectId}/progress`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Erro ao obter progresso');
        }
        
        // Atualiza a interface com os dados de progresso
        renderProgress(data.status, data.progress);
        
        // Se a execução terminou, para o polling
        if (data.status !== 'running') {
            stopProgressPolling();
            handleExecutionComplete(data.status, data.progress);
        }
        
    } catch (error) {
        console.error('Erro ao atualizar progresso:', error);
    }
}

/**
 * Para o polling de progresso.
 */
function stopProgressPolling() {
    if (pollingIntervalId) {
        clearInterval(pollingIntervalId);
        pollingIntervalId = null;
    }
}

/**
 * Renderiza os dados de progresso na interface.
 * 
 * @param {string} status - Status atual (running, completed, failed)
 * @param {Object} progress - Dados de progresso
 */
function renderProgress(status, progress) {
    if (!progress) return;
    
    // Atualiza estatísticas
    document.getElementById('stat-total').textContent = progress.tests_run || 0;
    document.getElementById('stat-passed').textContent = progress.tests_passed || 0;
    document.getElementById('stat-failed').textContent = progress.tests_failed || 0;
    document.getElementById('stat-skipped').textContent = progress.tests_skipped || 0;
    
    // Calcula e atualiza barra de progresso
    const percentage = progress.percentage || 0;
    document.getElementById('progress-fill').style.width = `${percentage}%`;
    
    // Atualiza lista de suítes
    if (progress.suites) {
        renderSuites(progress.suites);
    }
    
    // Atualiza console de output
    if (progress.output_lines) {
        renderConsoleOutput(progress.output_lines);
    }
}

/**
 * Renderiza a lista de suítes de teste.
 * 
 * @param {Object} suites - Objeto com suítes e seus status
 */
function renderSuites(suites) {
    const suitesList = document.getElementById('suites-list');
    suitesList.innerHTML = '';
    
    // Ícones de status
    const statusIcons = {
        'pending': '⏸️',
        'running': '🔄',
        'passed': '✅',
        'failed': '❌'
    };
    
    // Para cada suíte, cria um item
    for (const [suiteName, suiteData] of Object.entries(suites)) {
        const suiteItem = document.createElement('div');
        suiteItem.className = `suite-item ${suiteData.status}`;
        
        suiteItem.innerHTML = `
            <span class="suite-status ${suiteData.status}">
                ${statusIcons[suiteData.status] || '❓'}
            </span>
            <span class="suite-name" title="${suiteName}">${suiteName}</span>
            <span class="suite-type">${suiteData.type || 'test'}</span>
        `;
        
        suitesList.appendChild(suiteItem);
    }
}

/**
 * Renderiza as linhas de output no console.
 * 
 * @param {Array} lines - Linhas de output
 */
function renderConsoleOutput(lines) {
    const consoleOutput = document.getElementById('console-output');
    
    // Limpa e recria (poderia ser otimizado para apenas adicionar novas linhas)
    consoleOutput.innerHTML = '';
    
    // Adiciona cada linha
    lines.forEach(line => {
        const lineElement = document.createElement('div');
        lineElement.className = 'console-line';
        
        // Adiciona classe baseada no conteúdo
        if (line.includes('PASSED')) {
            lineElement.classList.add('passed');
        } else if (line.includes('FAILED') || line.includes('ERROR')) {
            lineElement.classList.add('failed');
        } else if (line.includes('SKIPPED')) {
            lineElement.classList.add('skipped');
        }
        
        lineElement.textContent = line;
        consoleOutput.appendChild(lineElement);
    });
    
    // Scroll para o final (mostrar linhas mais recentes)
    consoleOutput.scrollTop = consoleOutput.scrollHeight;
}

/**
 * Tratamento quando a execução termina.
 * 
 * @param {string} status - Status final (completed, failed, cancelled)
 * @param {Object} progress - Dados finais de progresso
 */
function handleExecutionComplete(status, progress) {
    executionInProgress = false;
    
    console.log(`✅ Execução finalizada com status: ${status}`);
    
    // Atualiza os cards
    loadProjects();
    
    // Mostra a seção de relatório
    document.getElementById('report-section').classList.remove('hidden');
    
    // Scroll para a seção de relatório
    setTimeout(() => {
        document.getElementById('report-section').scrollIntoView({ behavior: 'smooth' });
    }, 500);
}

/**
 * Cancela a execução de testes em andamento.
 */
async function cancelTests() {
    if (!currentProjectId || !executionInProgress) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/projects/${currentProjectId}/cancel`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('🛑 Execução cancelada');
            stopProgressPolling();
            executionInProgress = false;
            loadProjects();
        }
        
    } catch (error) {
        console.error('Erro ao cancelar execução:', error);
    }
}


// ============================================================================
// FUNÇÕES DE RELATÓRIO
// ============================================================================

/**
 * Gera e exibe o relatório de resultados.
 */
async function generateReport() {
    if (!currentProjectId) {
        alert('Nenhuma execução encontrada. Execute os testes primeiro.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/projects/${currentProjectId}/report`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Erro ao gerar relatório');
        }
        
        // Armazena o relatório para exportação
        lastReport = data.report;
        
        // Renderiza o relatório na interface
        renderReport(data.report);
        
    } catch (error) {
        console.error('Erro ao gerar relatório:', error);
        alert(`Erro ao gerar relatório: ${error.message}`);
    }
}

/**
 * Renderiza o relatório na interface.
 * 
 * @param {Object} report - Dados do relatório
 */
function renderReport(report) {
    const summaryContainer = document.getElementById('report-summary');
    const failuresContainer = document.getElementById('failures-container');
    const failuresList = document.getElementById('failures-list');
    
    // Renderiza cards de resumo
    const summary = report.summary;
    summaryContainer.innerHTML = `
        <div class="summary-card">
            <div class="summary-card-value">${summary.total_tests}</div>
            <div class="summary-card-label">Total de Testes</div>
        </div>
        <div class="summary-card success">
            <div class="summary-card-value">${summary.passed}</div>
            <div class="summary-card-label">✅ Passou</div>
        </div>
        <div class="summary-card danger">
            <div class="summary-card-value">${summary.failed}</div>
            <div class="summary-card-label">❌ Falhou</div>
        </div>
        <div class="summary-card warning">
            <div class="summary-card-value">${summary.skipped}</div>
            <div class="summary-card-label">⏭️ Ignorado</div>
        </div>
        <div class="summary-card">
            <div class="summary-card-value">${summary.success_rate}%</div>
            <div class="summary-card-label">Taxa de Sucesso</div>
        </div>
        <div class="summary-card">
            <div class="summary-card-value">${report.metadata.duration_seconds.toFixed(1)}s</div>
            <div class="summary-card-label">Duração</div>
        </div>
    `;
    
    // Renderiza falhas (se houver)
    if (report.failures && report.failures.length > 0) {
        failuresContainer.classList.remove('hidden');
        failuresList.innerHTML = '';
        
        report.failures.forEach(failure => {
            const failureItem = document.createElement('div');
            failureItem.className = 'failure-item';
            
            failureItem.innerHTML = `
                <div class="failure-header">
                    <span class="failure-name">${failure.test_name}</span>
                    <span class="failure-type">${failure.type}</span>
                </div>
                ${failure.error_message ? `
                    <pre class="failure-error">${escapeHtml(failure.error_message)}</pre>
                ` : ''}
            `;
            
            failuresList.appendChild(failureItem);
        });
    } else {
        failuresContainer.classList.add('hidden');
    }
}

/**
 * Exporta o relatório em formato JSON.
 */
async function exportReportJSON() {
    if (!currentProjectId) {
        alert('Nenhuma execução encontrada.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/projects/${currentProjectId}/report?format=json&save=true`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error);
        }
        
        // Cria um blob com o JSON e dispara download
        const blob = new Blob([JSON.stringify(data.report, null, 2)], { type: 'application/json' });
        downloadBlob(blob, `report_${currentProjectId}.json`);
        
    } catch (error) {
        console.error('Erro ao exportar JSON:', error);
        alert(`Erro ao exportar: ${error.message}`);
    }
}

/**
 * Exporta o relatório em formato Markdown.
 */
async function exportReportMarkdown() {
    if (!currentProjectId) {
        alert('Nenhuma execução encontrada.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/projects/${currentProjectId}/report?format=markdown`);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const markdown = await response.text();
        
        // Cria um blob com o Markdown e dispara download
        const blob = new Blob([markdown], { type: 'text/markdown' });
        downloadBlob(blob, `report_${currentProjectId}.md`);
        
    } catch (error) {
        console.error('Erro ao exportar Markdown:', error);
        alert(`Erro ao exportar: ${error.message}`);
    }
}

/**
 * Função auxiliar para disparar download de blob.
 * 
 * @param {Blob} blob - Dados para download
 * @param {string} filename - Nome do arquivo
 */
function downloadBlob(blob, filename) {
    // Cria URL temporária para o blob
    const url = URL.createObjectURL(blob);
    
    // Cria elemento <a> temporário para download
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    
    // Adiciona ao DOM, clica e remove
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    // Libera a URL
    URL.revokeObjectURL(url);
}


// ============================================================================
// FUNÇÕES UTILITÁRIAS
// ============================================================================

/**
 * Escapa caracteres HTML para evitar XSS.
 * 
 * O que é XSS?
 * -----------
 * Cross-Site Scripting é um ataque onde código malicioso é injetado na página.
 * Se não escaparmos HTML, um atacante poderia injetar <script> malicioso.
 * 
 * @param {string} text - Texto a ser escapado
 * @returns {string} Texto com caracteres HTML escapados
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


// ============================================================================
// EVENT LISTENERS
// ============================================================================

/**
 * Configura todos os event listeners da aplicação.
 */
function setupEventListeners() {
    // Botão cancelar
    document.getElementById('btn-cancel').addEventListener('click', cancelTests);
    
    // Botão toggle console
    document.getElementById('btn-toggle-console').addEventListener('click', () => {
        const consoleOutput = document.getElementById('console-output');
        const toggleBtn = document.getElementById('btn-toggle-console');
        
        consoleOutput.classList.toggle('expanded');
        toggleBtn.textContent = consoleOutput.classList.contains('expanded') ? 'Recolher' : 'Expandir';
    });
    
    // Botões de relatório
    document.getElementById('btn-generate-report').addEventListener('click', generateReport);
    document.getElementById('btn-export-json').addEventListener('click', exportReportJSON);
    document.getElementById('btn-export-markdown').addEventListener('click', exportReportMarkdown);
    
    // Modal
    document.getElementById('modal-close').addEventListener('click', closeModal);
    document.getElementById('modal-cancel').addEventListener('click', closeModal);
    document.getElementById('modal-overlay').addEventListener('click', (e) => {
        if (e.target === document.getElementById('modal-overlay')) {
            closeModal();
        }
    });
}

/**
 * Abre o modal com conteúdo personalizado.
 * 
 * @param {string} title - Título do modal
 * @param {string} content - Conteúdo HTML do modal
 * @param {Function} onConfirm - Callback ao confirmar
 */
function openModal(title, content, onConfirm) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-body').innerHTML = content;
    document.getElementById('modal-overlay').classList.remove('hidden');
    
    // Configura callback de confirmação
    const confirmBtn = document.getElementById('modal-confirm');
    confirmBtn.onclick = () => {
        if (onConfirm) onConfirm();
        closeModal();
    };
}

/**
 * Fecha o modal.
 */
function closeModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
}


// ============================================================================
// FIM DO ARQUIVO
// ============================================================================
console.log('📦 main.js carregado');
