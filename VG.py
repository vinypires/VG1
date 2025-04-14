import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Análise de Empresas - Várzea Grande", layout="wide")

# Título do dashboard
st.title("📊 Análise de Empresas em Várzea Grande")
st.markdown("Dashboard interativo para análise da evolução mensal de empresas")

# Carregar dados (simulando os dados que você tem no Excel)
@st.cache_data
def load_data():
    # Criando DataFrame simulado baseado na sua estrutura
    data = {
        'ANO': [2020, 2020, 2021, 2021, 2022, 2022],
        'MES': [1, 2, 1, 2, 1, 2],
        'MES_NOME': ['JANUARY', 'FEBRUARY', 'JANUARY', 'FEBRUARY', 'JANUARY', 'FEBRUARY'],
        'TOTAL_EMPRESAS': [81, 81, 83, 96, 94, 122],
        'TIPOS_MAIS_COMUNS': ['NÃO INFORMADO']*6
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar com filtros
st.sidebar.header("Filtros")
anos = st.sidebar.multiselect(
    "Selecione os anos:",
    options=df['ANO'].unique(),
    default=df['ANO'].unique()
)

meses = st.sidebar.multiselect(
    "Selecione os meses:",
    options=df['MES_NOME'].unique(),
    default=df['MES_NOME'].unique()
)

# Filtrar dados
df_filtered = df[
    (df['ANO'].isin(anos)) & 
    (df['MES_NOME'].isin(meses))
]

# Layout com colunas
col1, col2, col3 = st.columns(3)

# Métricas principais
with col1:
    st.metric("Total de Empresas", df_filtered['TOTAL_EMPRESAS'].sum())
    
with col2:
    st.metric("Média Mensal", round(df_filtered['TOTAL_EMPRESAS'].mean(), 2))
    
with col3:
    ultimo_ano = df_filtered['ANO'].max()
    st.metric("Último Ano Analisado", ultimo_ano)

# Gráfico de evolução temporal
st.subheader("Evolução Mensal de Empresas Cadastradas")
fig = px.line(
    df_filtered,
    x='MES_NOME',
    y='TOTAL_EMPRESAS',
    color='ANO',
    markers=True,
    labels={'TOTAL_EMPRESAS': 'Número de Empresas', 'MES_NOME': 'Mês'},
    title='Evolução por Mês e Ano'
)
st.plotly_chart(fig, use_container_width=True)

# Gráfico de comparação anual
st.subheader("Comparação Anual")
fig2 = px.bar(
    df_filtered,
    x='ANO',
    y='TOTAL_EMPRESAS',
    color='MES_NOME',
    barmode='group',
    labels={'TOTAL_EMPRESAS': 'Número de Empresas', 'ANO': 'Ano'},
    title='Comparação entre Anos'
)
st.plotly_chart(fig2, use_container_width=True)

# Tabela com dados detalhados
st.subheader("Dados Detalhados")
st.dataframe(df_filtered.sort_values(by=['ANO', 'MES']), hide_index=True)

# Análise de tendência
st.subheader("Análise de Tendência")
st.line_chart(df_filtered.set_index(['ANO', 'MES_NOME'])['TOTAL_EMPRESAS'])

# Rodapé
st.markdown("---")
st.caption("Dashboard criado com Streamlit | Dados fictícios para exemplo")