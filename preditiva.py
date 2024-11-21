import streamlit as st
import pandas as pd
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
import random

# Configuração inicial da aplicação
st.title("Análise Preditiva")

# Configurando abas para as análises
tabs = st.tabs(['Projeção de Valores', 'Previsão de Valor'])

# Projeção de Valores
with tabs[0]:
    st.header("Projeção de Valores")
    medida = st.selectbox('Medidas para Predição', st.session_state.get('medida', []))
    if st.button('Calcular Projeção'):
        # Preparando dados
        df = st.session_state['df']
        projecao = df.groupby('Order Date Month')[[medida]].sum().reset_index()
        projecao.columns = ['ds', 'y']

        # Configurando Prophet
        modelo = Prophet()
        modelo.fit(projecao)

        # Criando projeções
        future = modelo.make_future_dataframe(periods=12, freq='MS')
        forecast = modelo.predict(future)

        # Resultados
        st.subheader("Resultados da Projeção")
        cols = st.columns(2)
        cols[0].pyplot(modelo.plot(forecast))
        cols[1].dataframe(
            forecast.tail(12)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
            hide_index=True,
            use_container_width=True,
            height=480
        )

# Previsão com RandomForest
with tabs[1]:
    st.header("Previsão com RandomForest")
    medida = st.selectbox('Selecione a Medida', st.session_state.get('medida', []))
    dimensao = st.multiselect('Selecione a dimensão:', st.session_state.get('dimensao', []) + st.session_state.get('dimensao_tempo', []))
    if dimensao and st.button('Calcular Previsão'):
        df = st.session_state['df']

        # Criando variáveis dummies
        dummies = pd.get_dummies(df[dimensao])

        # Modelo Random Forest
        rf = RandomForestRegressor(n_estimators=1000, random_state=42)
        rf.fit(dummies, df[medida])

        # Amostra para previsão
        amostra = dummies.sample(10, random_state=42)
        previsao = rf.predict(amostra)
        amostra['Previsão'] = previsao

        # Resultados
        st.subheader("Resultados da Previsão")
        st.dataframe(amostra, use_container_width=True)
