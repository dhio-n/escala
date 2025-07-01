# Sistema de Geração de Escalas de Trabalho - CLT

Sistema desenvolvido em Python utilizando Streamlit para gerar escalas de trabalho automatizadas respeitando integralmente as leis da CLT brasileira.

## 🎯 Objetivo

O sistema tem como objetivo otimizar a geração de escalas com critérios legais, automatizar processos do RH e garantir confiabilidade no controle de jornada, sendo flexível, validado e seguro para uso contínuo.

## 🛠️ Tecnologias Utilizadas

- **Python** - Linguagem principal
- **Streamlit** - Interface web interativa
- **Pandas** - Manipulação de dados
- **openpyxl** - Exportação Excel
- **fpdf2** - Geração de PDF
- **python-dateutil** - Manipulação de datas

## 📁 Estrutura do Projeto

```
ESCALA/
├── requirements.txt          # Dependências do projeto
├── README.md                # Documentação
└── app/
    ├── app.py               # Interface principal com Streamlit
    ├── escala_generator.py  # Lógica para geração de escalas
    ├── regras_clt.py        # Regras de jornada e CLT
    ├── excel_utils.py       # Leitura e exportação de arquivos Excel
    ├── pdf_exporter.py      # Geração de relatórios PDF
    ├── data/
    │   └── uploads/         # Armazenamento de arquivos enviados
    └── templates/           # Templates para exportações (PDF/Excel)
```

## 🚀 Instalação e Execução

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o Sistema

```bash
cd app
streamlit run app.py
```

O sistema estará disponível em `http://localhost:8501`

## 📊 Funcionalidades Principais

### 1. Definição do Período Contábil
- Seleção de data de início e fim do período
- Validação automática do período

### 2. Upload de Planilhas
- **Colaboradores**: Nome, Cargo, Tipo_Escala, Turno, Atestados, Férias, Escalas_Manuais
- **Feriados**: Data e Descrição dos feriados do período

### 3. Tipos de Escala Suportados

| Código | Descrição |
|--------|-----------|
| **M44** | 44H - Manhã (Segunda a sexta, 8h/dia) |
| **T44** | 44H - Tarde (Segunda a sexta, 8h/dia) |
| **N44** | 44H - Noite (Segunda a sexta, 8h/dia) |
| **M40** | 40H - Manhã (Segunda a sexta, 8h/dia) |
| **T40** | 40H - Tarde (Segunda a sexta, 8h/dia) |
| **N40** | 40H - Noite (Segunda a sexta, 8h/dia) |
| **M6X1** | 6x1 - Manhã (6 dias trabalho, 1 dia folga) |
| **T6X1** | 6x1 - Tarde (6 dias trabalho, 1 dia folga) |
| **N6X1** | 6x1 - Noite (6 dias trabalho, 1 dia folga) |
| **P_D** | Plantão Par - Dia (dias pares do mês) |
| **P_N** | Plantão Par - Noite (dias pares do mês) |
| **I_D** | Plantão Ímpar - Dia (dias ímpares do mês) |
| **I_N** | Plantão Ímpar - Noite (dias ímpares do mês) |

### 4. Regras de Exceção
- **Atestados**: Dias marcados como "ATESTADO"
- **Férias**: Períodos marcados como "FÉRIAS"
- **Escalas Manuais**: Dias especiais marcados como "ESCALA MANUAL"

## 🎨 Código de Cores

| Cor | Status |
|-----|--------|
| 🟢 **Verde** | Trabalho regular |
| 🔵 **Azul** | Folga |
| ⚫ **Cinza** | Feriado |
| 🟣 **Roxo** | Escala manual |
| 🟠 **Laranja** | Atestado |
| 🟡 **Amarelo** | Férias |

## 📋 Estrutura da Planilha de Colaboradores

A planilha deve conter as seguintes colunas:

| Coluna | Obrigatória | Descrição |
|--------|-------------|-----------|
| Nome | ✅ | Nome completo do colaborador |
| Cargo | ✅ | Cargo/função do colaborador |
| Tipo_Escala | ✅ | Tipo de escala (M44, T44, N44, etc.) |
| Turno | ✅ | Turno de trabalho (Manhã, Tarde, Noite, Dia) |
| Atestados | ❌ | Datas de atestados (separadas por vírgula) |
| Ferias | ❌ | Período de férias (DD/MM/YYYY-DD/MM/YYYY) |
| Escalas_Manuais | ❌ | Datas de escalas manuais (separadas por vírgula) |

### Exemplo de Dados:

```csv
Nome,Cargo,Tipo_Escala,Turno,Atestados,Ferias,Escalas_Manuais
João Silva,Analista,M44,Manhã,,,
Maria Santos,Técnico,T44,Tarde,15/06/2025,,
Pedro Oliveira,Auxiliar,N6X1,Noite,,10/06/2025-20/06/2025,
Ana Costa,Supervisor,P_D,Dia,,,
Carlos Lima,Operador,I_N,Noite,20/06/2025,,
```

## 📋 Estrutura da Planilha de Feriados

A planilha deve conter as seguintes colunas:

| Coluna | Obrigatória | Descrição |
|--------|-------------|-----------|
| Data | ✅ | Data do feriado (DD/MM/YYYY) |
| Descricao | ❌ | Descrição do feriado |

### Exemplo de Dados:

```csv
Data,Descricao
12/06/2025,Corpus Christi
19/06/2025,São João
```

## 📤 Saídas do Sistema

### 1. Tabela Interativa
- Visualização completa da escala
- Filtros por nome, turno, escala e datas
- Código de cores para fácil identificação

### 2. Arquivo Excel (.xlsx)
- Escala mensal completa
- Organizada por colaborador e data
- Múltiplas abas com estatísticas

### 3. Arquivo PDF (.pdf)
- Relatório detalhado da escala
- Visualização por colaborador
- Estatísticas e resumos

## 🔧 Módulos do Sistema

### `app.py`
Interface principal com Streamlit, contendo:
- Upload de arquivos
- Configuração de período
- Visualização de resultados
- Download de relatórios

### `escala_generator.py`
Lógica principal para geração de escalas:
- Processamento de dados
- Aplicação de regras CLT
- Geração de escalas completas
- Validação de conformidade

### `regras_clt.py`
Implementação das regras da CLT:
- Regras específicas por tipo de escala
- Aplicação de exceções
- Validação de conformidade legal

### `excel_utils.py`
Manipulação de arquivos Excel:
- Leitura de planilhas
- Validação de dados
- Exportação de resultados

### `pdf_exporter.py`
Geração de relatórios PDF:
- Formatação de relatórios
- Estatísticas e resumos
- Múltiplos formatos de saída

## ⚖️ Conformidade CLT

O sistema garante conformidade com as seguintes regras da CLT:

- **Jornada de 44 horas semanais** para escala 44H
- **Descanso semanal remunerado** conforme legislação
- **Respeito aos feriados** conforme calendário oficial
- **Intervalos de descanso** entre jornadas
- **Limitação de horas extras** conforme legislação

## 🔍 Validações do Sistema

- Verificação de colunas obrigatórias
- Validação de tipos de escala
- Verificação de formatos de data
- Análise de conformidade CLT
- Detecção de conflitos de escala

## 🚀 Próximas Funcionalidades

- [ ] Integração com banco de dados
- [ ] Sincronização com sistemas ERP
- [ ] Notificações automáticas
- [ ] Dashboard de métricas
- [ ] API REST para integrações
- [ ] Módulo de gestão de turnos
- [ ] Relatórios avançados

## 📞 Suporte

Para dúvidas ou sugestões, entre em contato através dos canais oficiais da empresa.

---

**Desenvolvido com ❤️ para otimizar processos de RH e garantir conformidade legal.** 