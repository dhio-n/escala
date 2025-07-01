"""
Exportador de Relatórios PDF
===========================

Módulo para geração de relatórios PDF das escalas de trabalho.
"""

import pandas as pd
from datetime import datetime, date
from typing import Dict, List, Any
import os
try:
    from fpdf import FPDF
except ImportError:
    from fpdf2 import FPDF

class PDFExporter:
    """Classe para exportação de escalas em formato PDF."""
    
    def __init__(self):
        """Inicializa o exportador PDF."""
        self.pdf = None
        self.setup_pdf()
    
    def setup_pdf(self):
        """Configura o documento PDF."""
        self.pdf = FPDF(orientation='L', unit='mm', format='A4')
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 12)
    
    def exportar_escala_completa(self, escala_completa: pd.DataFrame, 
                                data_inicio: date, data_fim: date,
                                nome_arquivo: str = None) -> bytes:
        """
        Exporta a escala completa para PDF.
        
        Args:
            escala_completa: DataFrame com a escala completa
            data_inicio: Data de início do período
            data_fim: Data de fim do período
            nome_arquivo: Nome do arquivo de saída
            
        Returns:
            bytes: Conteúdo do arquivo PDF
        """
        if escala_completa.empty:
            raise ValueError("Escala vazia - não é possível gerar PDF")
        
        # Configurar PDF
        self.setup_pdf()
        
        # Cabeçalho
        self._adicionar_cabecalho(data_inicio, data_fim)
        
        # Tabela da escala
        self._adicionar_tabela_escala(escala_completa)
        
        # Estatísticas
        self._adicionar_estatisticas(escala_completa)
        
        # Gerar arquivo
        if nome_arquivo is None:
            nome_arquivo = f"escala_{data_inicio.strftime('%Y%m')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        self.pdf.output(nome_arquivo)
        
        # Ler arquivo gerado e retornar bytes
        with open(nome_arquivo, 'rb') as f:
            conteudo = f.read()
        
        # Remover arquivo temporário
        os.remove(nome_arquivo)
        
        return conteudo
    
    def exportar_escala_por_colaborador(self, escala_completa: pd.DataFrame,
                                       data_inicio: date, data_fim: date,
                                       nome_arquivo: str = None) -> bytes:
        """
        Exporta a escala organizada por colaborador.
        
        Args:
            escala_completa: DataFrame com a escala completa
            data_inicio: Data de início do período
            data_fim: Data de fim do período
            nome_arquivo: Nome do arquivo de saída
            
        Returns:
            bytes: Conteúdo do arquivo PDF
        """
        if escala_completa.empty:
            raise ValueError("Escala vazia - não é possível gerar PDF")
        
        # Configurar PDF
        self.setup_pdf()
        
        # Cabeçalho
        self._adicionar_cabecalho(data_inicio, data_fim)
        
        # Agrupar por colaborador
        colaboradores = escala_completa['Nome'].unique()
        
        for colaborador in colaboradores:
            # Nova página para cada colaborador
            self.pdf.add_page()
            
            # Dados do colaborador
            dados_colaborador = escala_completa[escala_completa['Nome'] == colaborador].iloc[0]
            
            # Cabeçalho do colaborador
            self.pdf.set_font('Arial', 'B', 14)
            self.pdf.cell(0, 10, f"Colaborador: {colaborador}", ln=True)
            self.pdf.set_font('Arial', '', 10)
            self.pdf.cell(0, 8, f"Cargo: {dados_colaborador['Cargo']}", ln=True)
            self.pdf.cell(0, 8, f"Tipo de Escala: {dados_colaborador['Tipo_Escala']}", ln=True)
            self.pdf.cell(0, 8, f"Turno: {dados_colaborador['Turno']}", ln=True)
            self.pdf.ln(5)
            
            # Escala do colaborador
            escala_colaborador = escala_completa[escala_completa['Nome'] == colaborador]
            self._adicionar_tabela_colaborador(escala_colaborador)
        
        # Gerar arquivo
        if nome_arquivo is None:
            nome_arquivo = f"escala_colaboradores_{data_inicio.strftime('%Y%m')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        self.pdf.output(nome_arquivo)
        
        # Ler arquivo gerado e retornar bytes
        with open(nome_arquivo, 'rb') as f:
            conteudo = f.read()
        
        # Remover arquivo temporário
        os.remove(nome_arquivo)
        
        return conteudo
    
    def _adicionar_cabecalho(self, data_inicio: date, data_fim: date):
        """Adiciona cabeçalho ao PDF."""
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, "ESCALA DE TRABALHO", ln=True, align='C')
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 8, f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}", ln=True, align='C')
        self.pdf.cell(0, 8, f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", ln=True, align='C')
        self.pdf.ln(10)
    
    def _adicionar_tabela_escala(self, escala_completa: pd.DataFrame):
        """Adiciona tabela da escala completa."""
        # Cabeçalho da tabela
        self.pdf.set_font('Arial', 'B', 10)
        colunas = ['Nome', 'Cargo', 'Tipo_Escala', 'Turno', 'Data', 'Status']
        
        # Larguras das colunas
        larguras = [40, 30, 25, 20, 25, 30]
        
        # Cabeçalho
        for i, coluna in enumerate(colunas):
            self.pdf.cell(larguras[i], 8, coluna, border=1, align='C')
        self.pdf.ln()
        
        # Dados
        self.pdf.set_font('Arial', '', 8)
        for _, linha in escala_completa.iterrows():
            for i, coluna in enumerate(colunas):
                valor = str(linha[coluna])
                if coluna == 'Data':
                    valor = linha[coluna].strftime('%d/%m/%Y')
                self.pdf.cell(larguras[i], 6, valor, border=1, align='C')
            self.pdf.ln()
    
    def _adicionar_tabela_colaborador(self, escala_colaborador: pd.DataFrame):
        """Adiciona tabela da escala de um colaborador específico."""
        # Cabeçalho da tabela
        self.pdf.set_font('Arial', 'B', 10)
        colunas = ['Data', 'Status']
        larguras = [50, 50]
        
        # Cabeçalho
        for i, coluna in enumerate(colunas):
            self.pdf.cell(larguras[i], 8, coluna, border=1, align='C')
        self.pdf.ln()
        
        # Dados
        self.pdf.set_font('Arial', '', 10)
        for _, linha in escala_colaborador.iterrows():
            self.pdf.cell(larguras[0], 8, linha['Data'].strftime('%d/%m/%Y'), border=1, align='C')
            self.pdf.cell(larguras[1], 8, linha['Status'], border=1, align='C')
            self.pdf.ln()
    
    def _adicionar_estatisticas(self, escala_completa: pd.DataFrame):
        """Adiciona estatísticas da escala."""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "ESTATÍSTICAS DA ESCALA", ln=True)
        self.pdf.ln(5)
        
        # Estatísticas por status
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, "Distribuição por Status:", ln=True)
        self.pdf.ln(3)
        
        estatisticas = escala_completa['Status'].value_counts()
        
        self.pdf.set_font('Arial', '', 10)
        for status, quantidade in estatisticas.items():
            self.pdf.cell(0, 6, f"{status}: {quantidade} dias", ln=True)
        
        self.pdf.ln(5)
        
        # Estatísticas por colaborador
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, "Dias de Trabalho por Colaborador:", ln=True)
        self.pdf.ln(3)
        
        estatisticas_colaborador = escala_completa[escala_completa['Status'] == 'TRABALHO']['Nome'].value_counts()
        
        self.pdf.set_font('Arial', '', 10)
        for colaborador, quantidade in estatisticas_colaborador.items():
            self.pdf.cell(0, 6, f"{colaborador}: {quantidade} dias", ln=True)
    
    def _adicionar_legenda(self):
        """Adiciona legenda das cores ao PDF."""
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, "LEGENDA", ln=True)
        self.pdf.ln(5)
        
        legenda = {
            'TRABALHO': 'Trabalho regular',
            'FOLGA': 'Folga',
            'FERIADO': 'Feriado',
            'ESCALA MANUAL': 'Escala manual',
            'ATESTADO': 'Atestado',
            'FÉRIAS': 'Férias'
        }
        
        self.pdf.set_font('Arial', '', 10)
        for status, descricao in legenda.items():
            self.pdf.cell(0, 6, f"{status}: {descricao}", ln=True)
    
    def exportar_pdf(self, escala_formatada: pd.DataFrame) -> bytes:
        """
        Exporta a escala formatada para PDF.
        
        Args:
            escala_formatada: DataFrame com a escala formatada
            
        Returns:
            bytes: Conteúdo do arquivo PDF
        """
        if escala_formatada.empty:
            raise ValueError("Escala vazia - não é possível gerar PDF")
        
        # Configurar PDF
        self.setup_pdf()
        
        # Cabeçalho
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, "ESCALA DE TRABALHO", ln=True, align='C')
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 8, f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", ln=True, align='C')
        self.pdf.ln(10)
        
        # Tabela da escala
        self._adicionar_tabela_escala_formatada(escala_formatada)
        
        # Legenda
        self._adicionar_legenda()
        
        # Gerar arquivo temporário
        nome_arquivo = f"escala_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.pdf.output(nome_arquivo)
        
        # Ler arquivo gerado e retornar bytes
        with open(nome_arquivo, 'rb') as f:
            conteudo = f.read()
        
        # Remover arquivo temporário
        os.remove(nome_arquivo)
        
        return conteudo
    
    def _adicionar_tabela_escala_formatada(self, escala_formatada: pd.DataFrame):
        """Adiciona tabela da escala formatada ao PDF."""
        # Obter colunas de informações e datas
        colunas_info = ['Nome', 'Cargo', 'Tipo_Escala', 'Turno']
        colunas_datas = [col for col in escala_formatada.columns if col not in colunas_info]
        
        # Configurar fonte para cabeçalho
        self.pdf.set_font('Arial', 'B', 8)
        
        # Cabeçalho - Informações
        for col in colunas_info:
            self.pdf.cell(30, 6, col, border=1, align='C')
        
        # Cabeçalho - Datas (formato reduzido)
        for col in colunas_datas:
            # Formatar data para exibição compacta
            try:
                data_obj = pd.to_datetime(col).date()
                data_formatada = data_obj.strftime('%d/%m')
            except:
                data_formatada = str(col)[:5]
            self.pdf.cell(8, 6, data_formatada, border=1, align='C')
        
        self.pdf.ln()
        
        # Dados
        self.pdf.set_font('Arial', '', 6)
        for _, linha in escala_formatada.iterrows():
            # Informações do colaborador
            for col in colunas_info:
                valor = str(linha[col])[:25]  # Limitar tamanho
                self.pdf.cell(30, 4, valor, border=1, align='C')
            
            # Status dos dias
            for col in colunas_datas:
                status = str(linha[col])
                # Usar símbolos para economizar espaço
                if '🟢' in status:
                    simbolo = 'T'
                elif '🔵' in status:
                    simbolo = 'F'
                elif '⚫' in status:
                    simbolo = 'H'
                elif '🟣' in status:
                    simbolo = 'M'
                elif '🟠' in status:
                    simbolo = 'A'
                elif '🟡' in status:
                    simbolo = 'V'
                else:
                    simbolo = status[:1]
                
                self.pdf.cell(8, 4, simbolo, border=1, align='C')
            
            self.pdf.ln() 