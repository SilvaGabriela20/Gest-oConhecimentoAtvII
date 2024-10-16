import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Definindo dimensões e medidas com base na base de dados
dimensao = ['COUNTRY', 'PRODUCTLINE', 'DEALSIZE', 'YEAR_ID', 'STATUS']
dimensao_tempo = ['ORDERDATE', 'QTR_ID', 'MONTH_ID', 'YEAR_ID']
medida = ['SALES', 'QUANTITYORDERED', 'PRICEEACH']

# Seleção de colunas, medidas e cores
cols = st.columns(3)
colunas = cols[0].multiselect(
    'Dimensões Coluna',
    dimensao + dimensao_tempo
)
valor = cols[1].selectbox(
    'Medidas',
    medida
)
cor = cols[2].selectbox(
    'Cor',
    colunas
)

# Configurando as abas para visualização
tabs = st.tabs(['Treemap', 'Sunburst', 'Sankey', 'TimeSeries'])
if len(colunas) > 2:
    with tabs[0]:
        fig = px.treemap(
            st.session_state['df'],
            path=colunas,
            values=valor,
            color=cor,
            height=800,
            width=1200
        )
        fig.update_traces(textinfo='label+value')
        st.plotly_chart(fig)

    with tabs[1]:
        fig = px.sunburst(
            st.session_state['df'],
            path=colunas,
            values=valor,
            color=cor,
            height=800,
            width=1200
        )
        fig.update_traces(textinfo='label+value')
        st.plotly_chart(fig)

    with tabs[2]:
        grupo = st.session_state['df'].groupby(colunas)[valor].sum().reset_index().copy()
        rotulos, codigo = [], 0
        for coluna in colunas:
            for conteudo in grupo[coluna].unique():
                rotulos.append([codigo, conteudo])
                codigo += 1
        rotulos = pd.DataFrame(rotulos, columns=['codigo', 'conteudo'])
        sankey = []
        for i in range(0, len(colunas) - 1):
            for _, row in grupo.iterrows():
                sankey.append([
                    rotulos.loc[rotulos['conteudo'] == row[colunas[i]], 'codigo'].values[0],
                    rotulos.loc[rotulos['conteudo'] == row[colunas[i + 1]], 'codigo'].values[0],
                    row[valor]
                ])
        sankey = pd.DataFrame(sankey, columns=['source', 'target', 'value'])
        fig = go.Figure(go.Sankey(
            node=dict(label=rotulos['conteudo']),
            link=dict(source=sankey['source'], target=sankey['target'], value=sankey['value'])
        ))
        st.plotly_chart(fig)

    with tabs[3]:
        if 'ORDERDATE' in colunas:
            base = st.session_state['df'].pivot_table(
                index='ORDERDATE',
                columns=colunas,
                values=valor,
                aggfunc='sum'
            ).reset_index()
            st.plotly_chart(px.line(base, x='ORDERDATE', y=base.columns))

