"""
Report Generator Service - Serviço de Geração de Relatórios
===========================================================

Este módulo é responsável por gerar relatórios consolidados dos resultados
de execução de testes. Suporta exportação em múltiplos formatos (JSON, Markdown).

Conceitos importantes para aprendizado:
---------------------------------------
1. CONSOLIDAÇÃO DE DADOS: Agrupa resultados de múltiplas fontes em um único relatório
2. FORMATAÇÃO: Transforma dados brutos em formatos legíveis
3. EXPORTAÇÃO: Gera arquivos em diferentes formatos para diferentes necessidades
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class ReportGenerator:
    """
    Classe responsável por gerar relatórios de execução de testes.
    
    Um relatório contém:
    - Resumo geral (totais de testes, tempo de execução)
    - Detalhes por suíte/arquivo de teste
    - Lista de testes com falha (com mensagens de erro)
    - Metadados (data/hora, projeto, etc.)
    """
    
    def __init__(self, project_name: str, progress_data: Dict[str, Any], raw_results: Optional[Dict] = None):
        """
        Inicializa o gerador de relatórios.
        
        Args:
            project_name: Nome do projeto de teste
            progress_data: Dados de progresso coletados durante a execução
            raw_results: Resultados brutos do pytest (JSON), se disponível
        """
        self.project_name = project_name
        self.progress_data = progress_data
        self.raw_results = raw_results
        
    def generate_report(self) -> Dict[str, Any]:
        """
        Gera o relatório consolidado em formato de dicionário.
        
        O relatório é estruturado de forma hierárquica:
        - metadata: informações sobre o relatório em si
        - summary: números consolidados (totais)
        - suites: detalhamento por arquivo de teste
        - failures: lista de testes que falharam (para análise)
        
        Returns:
            Dicionário com o relatório completo
        """
        # Calcula o tempo total de execução
        duration = self._calculate_duration()
        
        # Monta o relatório
        report = {
            # METADADOS
            # Informações sobre quando e como o relatório foi gerado
            'metadata': {
                'project_name': self.project_name,
                'generated_at': datetime.now().isoformat(),
                'started_at': self.progress_data.get('started_at'),
                'finished_at': self.progress_data.get('finished_at'),
                'duration_seconds': duration,
                'report_version': '1.0'
            },
            
            # RESUMO GERAL
            # Números consolidados para visão rápida do resultado
            'summary': {
                'total_tests': self.progress_data.get('tests_run', 0),
                'passed': self.progress_data.get('tests_passed', 0),
                'failed': self.progress_data.get('tests_failed', 0),
                'skipped': self.progress_data.get('tests_skipped', 0),
                'success_rate': self._calculate_success_rate(),
                'status': self._determine_overall_status()
            },
            
            # DETALHAMENTO POR SUÍTE
            # Cada suíte representa um arquivo de teste
            'suites': self._format_suites(),
            
            # TESTES COM FALHA
            # Lista detalhada para facilitar a análise e correção
            'failures': self._extract_failures()
        }
        
        return report
    
    def _calculate_duration(self) -> float:
        """
        Calcula a duração da execução em segundos.
        
        Returns:
            Duração em segundos, ou 0 se não for possível calcular
        """
        try:
            started = self.progress_data.get('started_at')
            finished = self.progress_data.get('finished_at')
            
            if started and finished:
                start_time = datetime.fromisoformat(started)
                end_time = datetime.fromisoformat(finished)
                return (end_time - start_time).total_seconds()
        except Exception:
            pass
        
        return 0.0
    
    def _calculate_success_rate(self) -> float:
        """
        Calcula a taxa de sucesso (porcentagem de testes que passaram).
        
        Fórmula: (testes_passaram / total_testes) * 100
        
        Returns:
            Taxa de sucesso como porcentagem (0-100)
        """
        total = self.progress_data.get('tests_run', 0)
        passed = self.progress_data.get('tests_passed', 0)
        
        if total > 0:
            return round((passed / total) * 100, 2)
        return 0.0
    
    def _determine_overall_status(self) -> str:
        """
        Determina o status geral da execução.
        
        Regras:
        - Se houve falhas → 'failed'
        - Se todos passaram → 'passed'
        - Se nenhum teste rodou → 'no_tests'
        
        Returns:
            String indicando o status geral
        """
        failed = self.progress_data.get('tests_failed', 0)
        total = self.progress_data.get('tests_run', 0)
        
        if total == 0:
            return 'no_tests'
        elif failed > 0:
            return 'failed'
        else:
            return 'passed'
    
    def _format_suites(self) -> List[Dict[str, Any]]:
        """
        Formata os dados das suítes para o relatório.
        
        Cada suíte inclui:
        - Nome do arquivo
        - Tipo de teste (unit, integration, etc.)
        - Contagem de resultados
        - Status final
        
        Returns:
            Lista de dicionários com dados das suítes
        """
        suites = []
        suites_data = self.progress_data.get('suites', {})
        
        for suite_name, suite_info in suites_data.items():
            suites.append({
                'name': suite_name,
                'type': suite_info.get('type', 'unknown'),
                'status': suite_info.get('status', 'unknown'),
                'passed': suite_info.get('tests_passed', 0),
                'failed': suite_info.get('tests_failed', 0),
                'skipped': suite_info.get('tests_skipped', 0),
                'total': (
                    suite_info.get('tests_passed', 0) +
                    suite_info.get('tests_failed', 0) +
                    suite_info.get('tests_skipped', 0)
                )
            })
        
        # Ordena por status (falhas primeiro) e depois por nome
        suites.sort(key=lambda x: (0 if x['status'] == 'failed' else 1, x['name']))
        
        return suites
    
    def _extract_failures(self) -> List[Dict[str, Any]]:
        """
        Extrai informações detalhadas dos testes que falharam.
        
        Para cada falha, incluímos:
        - Nome do teste
        - Arquivo onde está localizado
        - Tipo de teste
        - Mensagem de erro (se disponível)
        
        Returns:
            Lista de dicionários com detalhes das falhas
        """
        failures = []
        
        # Tenta extrair do JSON de resultados do pytest (mais detalhado)
        if self.raw_results and 'tests' in self.raw_results:
            for test in self.raw_results['tests']:
                if test.get('outcome') in ('failed', 'error'):
                    failure_info = {
                        'test_name': test.get('nodeid', 'Unknown test'),
                        'file': test.get('nodeid', '').split('::')[0] if '::' in test.get('nodeid', '') else '',
                        'type': self._get_test_type(test.get('nodeid', '')),
                        'error_message': self._extract_error_message(test),
                        'duration': test.get('duration', 0)
                    }
                    failures.append(failure_info)
        
        # Se não tiver o JSON, tenta extrair das linhas de saída
        elif not failures:
            output_lines = self.progress_data.get('output_lines', [])
            failures = self._parse_failures_from_output(output_lines)
        
        return failures
    
    def _get_test_type(self, nodeid: str) -> str:
        """
        Determina o tipo de teste baseado no nome do arquivo.
        
        Args:
            nodeid: Identificador do teste (ex: tests/test_integration.py::test_exemplo)
            
        Returns:
            Tipo do teste (unit, integration, api, cli)
        """
        if 'integration' in nodeid.lower():
            return 'integration'
        elif 'api' in nodeid.lower():
            return 'api'
        elif 'cli' in nodeid.lower():
            return 'cli'
        else:
            return 'unit'
    
    def _extract_error_message(self, test_data: Dict) -> str:
        """
        Extrai a mensagem de erro de um teste que falhou.
        
        Args:
            test_data: Dados do teste do JSON do pytest
            
        Returns:
            Mensagem de erro resumida
        """
        # Tenta diferentes locais onde o erro pode estar
        if 'call' in test_data and 'longrepr' in test_data['call']:
            return test_data['call']['longrepr'][:500]  # Limita a 500 chars
        
        if 'longrepr' in test_data:
            return str(test_data['longrepr'])[:500]
        
        return 'Erro não especificado'
    
    def _parse_failures_from_output(self, output_lines: List[str]) -> List[Dict[str, Any]]:
        """
        Tenta extrair informações de falhas das linhas de saída do pytest.
        
        Este é um fallback quando o JSON de resultados não está disponível.
        
        Args:
            output_lines: Lista de linhas da saída do pytest
            
        Returns:
            Lista de falhas encontradas
        """
        failures = []
        current_failure = None
        
        for line in output_lines:
            # Detecta linha com teste falhando
            if 'FAILED' in line and '::' in line:
                # Extrai o nome do teste
                parts = line.split()
                for part in parts:
                    if '::' in part:
                        current_failure = {
                            'test_name': part,
                            'file': part.split('::')[0] if '::' in part else '',
                            'type': self._get_test_type(part),
                            'error_message': '',
                            'duration': 0
                        }
                        failures.append(current_failure)
                        break
            
            # Tenta capturar mensagens de erro (linhas após o FAILED)
            elif current_failure and line.startswith(('E ', 'AssertionError', 'ValueError', 'TypeError')):
                if len(current_failure['error_message']) < 500:
                    current_failure['error_message'] += line + '\n'
        
        return failures
    
    def to_json(self) -> str:
        """
        Exporta o relatório como string JSON formatada.
        
        JSON é ideal para:
        - Integração com outras ferramentas
        - Armazenamento estruturado
        - Processamento automatizado
        
        Returns:
            String JSON formatada com indentação
        """
        report = self.generate_report()
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def to_markdown(self) -> str:
        """
        Exporta o relatório como Markdown formatado.
        
        Markdown é ideal para:
        - Visualização humana
        - Documentação
        - Inserção em pull requests ou issues
        
        Returns:
            String Markdown formatada
        """
        report = self.generate_report()
        
        # Ícones de status
        status_icons = {
            'passed': '✅',
            'failed': '❌',
            'skipped': '⏭️',
            'no_tests': '⚠️'
        }
        
        # Monta o Markdown
        md = []
        
        # Cabeçalho
        md.append(f"# 📊 Relatório de Testes - {report['metadata']['project_name']}")
        md.append("")
        md.append(f"**Gerado em:** {report['metadata']['generated_at']}")
        md.append(f"**Duração:** {report['metadata']['duration_seconds']:.2f} segundos")
        md.append("")
        
        # Resumo
        summary = report['summary']
        status_icon = status_icons.get(summary['status'], '❓')
        
        md.append("## 📋 Resumo")
        md.append("")
        md.append(f"| Métrica | Valor |")
        md.append("|---------|-------|")
        md.append(f"| Status Geral | {status_icon} {summary['status'].upper()} |")
        md.append(f"| Total de Testes | {summary['total_tests']} |")
        md.append(f"| ✅ Passou | {summary['passed']} |")
        md.append(f"| ❌ Falhou | {summary['failed']} |")
        md.append(f"| ⏭️ Ignorado | {summary['skipped']} |")
        md.append(f"| Taxa de Sucesso | {summary['success_rate']}% |")
        md.append("")
        
        # Suítes
        if report['suites']:
            md.append("## 📁 Suítes de Teste")
            md.append("")
            md.append("| Suíte | Tipo | Status | Passou | Falhou | Ignorado |")
            md.append("|-------|------|--------|--------|--------|----------|")
            
            for suite in report['suites']:
                suite_icon = status_icons.get(suite['status'], '❓')
                md.append(
                    f"| {suite['name']} | {suite['type']} | {suite_icon} | "
                    f"{suite['passed']} | {suite['failed']} | {suite['skipped']} |"
                )
            md.append("")
        
        # Falhas
        if report['failures']:
            md.append("## ❌ Testes com Falha")
            md.append("")
            
            for i, failure in enumerate(report['failures'], 1):
                md.append(f"### {i}. {failure['test_name']}")
                md.append(f"- **Tipo:** {failure['type']}")
                md.append(f"- **Arquivo:** {failure['file']}")
                if failure.get('error_message'):
                    md.append(f"- **Erro:**")
                    md.append("```")
                    md.append(failure['error_message'][:300])
                    md.append("```")
                md.append("")
        
        # Rodapé
        md.append("---")
        md.append("*Relatório gerado pelo Test Hub*")
        
        return '\n'.join(md)
    
    def save_report(self, output_dir: str, formats: List[str] = ['json', 'md']) -> Dict[str, str]:
        """
        Salva o relatório em arquivos nos formatos especificados.
        
        Args:
            output_dir: Diretório onde salvar os arquivos
            formats: Lista de formatos desejados ('json', 'md')
            
        Returns:
            Dicionário com caminhos dos arquivos salvos
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saved_files = {}
        
        if 'json' in formats:
            json_path = os.path.join(output_dir, f'report_{timestamp}.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(self.to_json())
            saved_files['json'] = json_path
        
        if 'md' in formats:
            md_path = os.path.join(output_dir, f'report_{timestamp}.md')
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(self.to_markdown())
            saved_files['md'] = md_path
        
        return saved_files
