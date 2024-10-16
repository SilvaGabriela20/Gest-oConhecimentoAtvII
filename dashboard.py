import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
import pygwalker as pyg

# Definindo as dimensões e medidas a serem utilizadas
dimensao = ['COUNTRY', 'PRODUCTLINE', 'DEALSIZE', 'YEAR_ID', 'STATUS']
dimensao_tempo = ['ORDERDATE', 'QTR_ID', 'MONTH_ID', 'YEAR_ID']
medida = ['SALES', 'QUANTITYORDERED', 'PRICEEACH']

pyg_app = StreamlitRenderer(
    st.session_state['df'][
        dimensao + dimensao_tempo + medida
    ]
)
pyg.walk('df')
pyg_app.explorer()
