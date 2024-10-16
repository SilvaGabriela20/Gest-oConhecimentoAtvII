import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from itertools import combinations

# Configuração de estilo
style_metric_cards(
    border_left_color="#3D5077",
    background_color="#F0F2F6",
    border_size_px=3,
    border_color="#CECED0",
    border_radius_px=20,
    box_shadow=True
)

# Definindo as dimensões e medidas com base na base de dados
dimensao = ['COUNTRY', 'PRODUCTLINE', 'DEALSIZE', 'YEAR_ID', 'STATUS']
medida = ['SALES', 'QUANTITYORDERED', 'PRICEEACH']

# Seleção de dimensões e métricas
cols = st.columns(4)
coluna = cols[0].selectbox('Dimensão', dimensao)
conteudo = cols[1].selectbox('Classe', st.session_state['df'][coluna].unique())
medida_selecionada = cols[2].selectbox('Medida', medida)
mes = cols[3].selectbox('Mês', st.session_state['df']['MONTH_ID'].unique())

# Filtrando os dados para o mês e ano selecionados
mes_atual = st.session_state['df'][(st.session_state['df']['YEAR_ID'] == 2023) & (st.session_state['df']['MONTH_ID'] == mes)]

# Exibindo as métricas
cols[0].subheader(f'Métrica de {medida_selecionada} no mês {mes}')
if mes == 1:
    cols[0].metric(label=f'{medida_selecionada} em relação ao mês anterior', value=round(mes_atual[medida_selecionada].sum(), 2))
else:
    mes_anterior = st.session_state['df'][(st.session_state['df']['YEAR_ID'] == 2023) & (st.session_state['df']['MONTH_ID'] == mes - 1)]
    cols[0].metric(
        label=f'{medida_selecionada} em relação ao mês anterior',
        value=round(mes_atual[medida_selecionada].sum(), 2),
        delta=str(round(mes_atual[medida_selecionada].sum() - mes_anterior[medida_selecionada].sum(), 2))
    )

# Gráfico de caixa para comparativo
cols[0].subheader(f'Comparativo em {coluna}')
cols[0].plotly_chart(px.box(mes_atual, x=coluna, y=medida_selecionada))

# Análise Tukey HSD
tukeyhsd = pairwise_tukeyhsd(endog=mes_atual[medida_selecionada], groups=mes_atual[coluna], alpha=0.05)
tukey = pd.DataFrame(data={'grupo1': tukeyhsd.groupsunique, 'grupo2': tukeyhsd.groupsunique[::-1], 'meandiffs': tukeyhsd.meandiffs, 'reject': tukeyhsd.reject})
if cols[0].toggle('Mostrar todos'):
    cols[0].dataframe(tukey)
else:
    cols[0].dataframe(tukey[tukey['reject']])

# Evolução ao longo do tempo
cols[1].subheader(f'Evolução de {medida_selecionada} em {coluna} - {conteudo}')
evolucao = st.session_state['df'][st.session_state['df'][coluna] == conteudo].groupby('MONTH_ID')[medida_selecionada].sum().reset_index()
cols[1].plotly_chart(px.bar(evolucao, x='MONTH_ID', y=medida_selecionada, color_discrete_sequence=['blue']))
