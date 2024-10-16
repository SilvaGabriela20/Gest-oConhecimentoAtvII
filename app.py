import pandas as pd
import datetime as dt
import streamlit as st
import pygwalker as pyg

@st.cache_data
def load_database():
    # Usando o caminho absoluto para o arquivo
    df = pd.read_excel(r'C:\Users\gabri\OneDrive\Documentos\gestao_conhecimento\gestaodeconhecimento\data\sales_data_sample.xlsx')
    
    # Renomeando colunas para letras maiúsculas
    df.columns = [col.upper() for col in df.columns]
    
    # Verificando se as colunas esperadas estão presentes
    if 'ORDER DATE' in df.columns and 'SHIP DATE' in df.columns:
        df['ORDER MONTH'] = df['ORDER DATE'].astype(str)
        df['ORDER YEAR'] = df['ORDER DATE'].astype(str)
        df['SHIP YEAR'] = df['SHIP DATE'].astype(str)
        df['SHIP MONTH'] = df['SHIP DATE'].astype(str)
        df['ORDER DATE'] = pd.to_datetime(df['ORDER DATE'], errors='coerce')
        df['SHIP DATE'] = pd.to_datetime(df['SHIP DATE'], errors='coerce')
        df['ORDER DATE MONTH'] = df['ORDER DATE'].apply(lambda x: x.strftime("%Y-%m-01") if pd.notnull(x) else None)
        df = df.drop(columns=['ORDER ID', 'ORDER PRIORITY'], errors='ignore')
        df['ORDER YEAR'] = df['ORDER DATE'].dt.year
        df['ORDER MONTH'] = df['ORDER DATE'].dt.month
        df['SHIP YEAR'] = df['SHIP DATE'].dt.year
        df['SHIP MONTH'] = df['SHIP DATE'].dt.month
    else:
        st.error("As colunas 'ORDER DATE' e/ou 'SHIP DATE' não foram encontradas no arquivo.")
    
    return df

st.session_state['dimensao_tempo'] = ['ORDER DATE', 'SHIP DATE', 'ORDER MONTH', 'SHIP MONTH', 'ORDER YEAR']
st.session_state['medida'] = ['UNITS SOLD', 'TOTAL PROFIT', 'TOTAL REVENUE']
st.session_state['agregador'] = ['SUM', 'MEAN', 'COUNT', 'MIN', 'MAX']
st.set_page_config(page_title="Gestão do Conhecimento", layout="wide")
st.session_state['df'] = load_database()
st.session_state['dimensao'] = [
    'SALES CHANNEL', 'COUNTRY', 'REGION',  'ITEM TYPE'
]
st.title("Gestão do Conhecimento")

pg = st.navigation(
    {
        'Introdução': [
            st.Page(page='Introducao/tabela.py', title='Tabela', icon=':material/house:'),
            st.Page(page='introducao/cubo.py', title='Cubo', icon=':material/help:'),
            st.Page(page='introducao/dashboard.py', title='Dashboard', icon=':material/help:'),
            st.Page(page='introducao/visualizacao.py', title='Visualização', icon=':material/help:'),
        ],
        "Visualização": [
            st.Page(page='visualizacao/descritiva.py', title='Analise Descritiva', icon=':material/house:'),
            st.Page(page='visualizacao/diagnostica.py', title='Analise Diagnostica', icon=':material/house:'),
            st.Page(page='visualizacao/preditiva.py', title='Analise Preditiva', icon=':material/house:'),
            st.Page(page='visualizacao/prescritiva.py', title='Analise Prescritiva', icon=':material/house:'),
        ]
    }
)
pg.run()
