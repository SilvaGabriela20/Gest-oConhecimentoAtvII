import pandas as pd
import streamlit as st

# Definindo as opções de dimensões com base na base de dados
dimensao = ['COUNTRY', 'PRODUCTLINE', 'DEALSIZE', 'YEAR_ID', 'STATUS']
dimensao_tempo = ['ORDERDATE', 'QTR_ID', 'MONTH_ID', 'YEAR_ID']
medida = ['SALES', 'QUANTITYORDERED', 'PRICEEACH']
agregador = ['sum', 'mean', 'count']

cols = st.columns(4)
linhas = cols[0].multiselect(
    'Dimensões Linha',
    dimensao
)
colunas = cols[1].multiselect(
    'Dimensões Coluna',
    dimensao + dimensao_tempo
)
valor = cols[2].selectbox(
    'Medidas',
    medida
)
agg = cols[3].selectbox(
    'Agregador',
    agregador
)

if (len(linhas) > 0) & (len(colunas) > 0) & (linhas != colunas):
    st.dataframe(
        st.session_state['df'].pivot_table(
            index=linhas,
            columns=colunas,
            values=valor,
            aggfunc=agg,
            fill_value=0
        )
    )
    st.dataframe(
        st.session_state['df'].groupby(linhas)[valor].sum().reset_index()
    )
