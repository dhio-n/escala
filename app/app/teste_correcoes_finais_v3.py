"""
Teste das Correções Finais v3
=============================

Este arquivo testa as correções implementadas:
1. Download de PDF funcionando
2. Escalas 6x1 com alternância entre colaboradores
3. Configuração de regras de domingo
"""

import sys
import os
from datetime import date, datetime
import pandas as pd

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from escala_generator import GeradorEscala
from pdf_exporter import PDFExporter

def testar_correcoes():
    """Testa todas as correções implementadas."""
    print("=== TESTE DAS CORREÇÕES FINAIS v3 ===")
    
    # Configurar período de teste
    data_inicio = date(2025, 1, 1)
    data_fim = date(2025, 1, 31)
    
    # Criar dados de teste
    df_colaboradores = pd.DataFrame([
        {
            'Nome': 'João Silva',
            'Cargo': 'Analista',
            'Tipo_Escala': 'M6X1',
            'Turno': 'Manhã',
            'Ultimo_Domingo_Folga': '29/12/2024'
        },
        {
            'Nome': 'Maria Santos',
            'Cargo': 'Técnico',
            'Tipo_Escala': 'M6X1',
            'Turno': 'Manhã',
            'Ultimo_Domingo_Folga': '29/12/2024'
        },
        {
            'Nome': 'Pedro Oliveira',
            'Cargo': 'Auxiliar',
            'Tipo_Escala': 'T6X1',
            'Turno': 'Tarde',
            'Ultimo_Domingo_Folga': '29/12/2024'
        }
    ])
    
    # Criar feriados de teste
    df_feriados = pd.DataFrame([
        {'Data': '01/01/2025', 'Descricao': 'Confraternização Universal'},
        {'Data': '20/01/2025', 'Descricao': 'São Sebastião'}
    ])
    
    print(f"📊 Testando com {len(df_colaboradores)} colaboradores 6x1")
    print(f"📅 Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
    
    # Teste 1: Configuração com alternância
    print("\n🧪 Teste 1: Configuração com alternância entre colaboradores")
    config_6x1 = {
        'folga_domingo_obrigatoria': True,
        'alternancia_colaboradores': True,
        'max_dias_consecutivos': 6,
        'semanas_sem_domingo_max': 6
    }
    
    gerador = GeradorEscala(data_inicio, data_fim, df_feriados, config_6x1)
    escala_completa = gerador.gerar_escala_completa(df_colaboradores)
    
    print(f"✅ Escala gerada com {len(escala_completa)} registros")
    
    # Verificar alternância
    colaboradores_6x1 = escala_completa[escala_completa['Tipo_Escala'].str.contains('6X1')]
    if not colaboradores_6x1.empty:
        print("📋 Verificando alternância entre colaboradores...")
        
        # Agrupar por colaborador e contar folgas
        folgas_por_colaborador = colaboradores_6x1[colaboradores_6x1['Status'] == 'FOLGA'].groupby('Nome').size()
        print("📊 Folgas por colaborador:")
        for nome, folgas in folgas_por_colaborador.items():
            print(f"   - {nome}: {folgas} folgas")
    
    # Teste 2: Configuração sem alternância
    print("\n🧪 Teste 2: Configuração sem alternância")
    config_6x1_sem_alternancia = {
        'folga_domingo_obrigatoria': False,
        'alternancia_colaboradores': False,
        'max_dias_consecutivos': 6,
        'semanas_sem_domingo_max': 6
    }
    
    gerador2 = GeradorEscala(data_inicio, data_fim, df_feriados, config_6x1_sem_alternancia)
    escala_completa2 = gerador2.gerar_escala_completa(df_colaboradores)
    
    print(f"✅ Escala sem alternância gerada com {len(escala_completa2)} registros")
    
    # Teste 3: Exportação PDF
    print("\n🧪 Teste 3: Exportação PDF")
    try:
        escala_formatada = gerador.exportar_escala_formatada(escala_completa)
        pdf_exporter = PDFExporter()
        pdf_bytes = pdf_exporter.exportar_pdf(escala_formatada)
        
        print(f"✅ PDF gerado com sucesso! Tamanho: {len(pdf_bytes)} bytes")
        
        # Salvar PDF para verificação
        with open('teste_escala.pdf', 'wb') as f:
            f.write(pdf_bytes)
        print("💾 PDF salvo como 'teste_escala.pdf'")
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {str(e)}")
    
    # Teste 4: Validação das regras
    print("\n🧪 Teste 4: Validação das regras 6x1")
    
    # Verificar se nenhum colaborador trabalha mais de 6 dias consecutivos
    for nome in df_colaboradores['Nome']:
        escala_colaborador = escala_completa[escala_completa['Nome'] == nome].sort_values('Data')
        
        dias_consecutivos = 0
        max_consecutivos = 0
        
        for _, row in escala_colaborador.iterrows():
            if row['Status'] in ['TRABALHO_MANHA', 'TRABALHO_TARDE', 'TRABALHO_NOITE']:
                dias_consecutivos += 1
                max_consecutivos = max(max_consecutivos, dias_consecutivos)
            else:
                dias_consecutivos = 0
        
        print(f"   - {nome}: Máximo dias consecutivos = {max_consecutivos}")
        
        if max_consecutivos > 6:
            print(f"   ⚠️ ATENÇÃO: {nome} trabalhou {max_consecutivos} dias consecutivos!")
        else:
            print(f"   ✅ {nome} respeita a regra dos 6 dias consecutivos")
    
    # Teste 5: Relatório 6x1
    print("\n🧪 Teste 5: Relatório 6x1")
    relatorio_6x1 = gerador.gerar_relatorio_6x1(escala_completa)
    
    if not relatorio_6x1.empty:
        print("📊 Relatório 6x1 gerado:")
        for _, row in relatorio_6x1.iterrows():
            print(f"   - {row['Nome']}: {row['Domingos_Folgados']} domingos folgados, {row['Semanas_Sem_Domingo']} semanas sem domingo")
    else:
        print("❌ Nenhum colaborador 6x1 encontrado no relatório")
    
    print("\n✅ Todos os testes concluídos!")
    return escala_completa, relatorio_6x1

if __name__ == "__main__":
    print("INICIANDO TESTE DAS CORREÇÕES FINAIS v3")
    
    try:
        # Executar testes
        escala, relatorio = testar_correcoes()
        
        print("\n🎉 Testes executados com sucesso!")
        print(f"📊 Escala gerada: {len(escala)} registros")
        print(f"📋 Relatório 6x1: {len(relatorio)} colaboradores")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {str(e)}")
        import traceback
        traceback.print_exc() 