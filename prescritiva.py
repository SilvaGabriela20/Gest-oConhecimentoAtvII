import streamlit as st
import pandas as pd
from prophet import Prophet
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# Configuração inicial da aplicação
st.title("Análise Prescritiva")

if st.button('Executar Análise Prescritiva'):
    # Preparando os dados
    df = st.session_state['df']
    medida = st.session_state.get('medida', ['Sales', 'Profit', 'Quantity'])
    grupo = df.groupby(['Order Date Month', 'Sub-Category'])[medida].sum().reset_index()

    # Projeção usando Prophet
    projecao = pd.DataFrame()
    for subcategoria in grupo['Sub-Category'].unique():
        grupo_sub = grupo[grupo['Sub-Category'] == subcategoria]
        for m in medida:
            grupo_medida = grupo_sub[['Order Date Month', m]]
            grupo_medida.columns = ['ds', 'y']

            # Modelo Prophet
            modelo = Prophet()
            modelo.fit(grupo_medida)
            future = modelo.make_future_dataframe(periods=1, freq='MS')
            forecast = modelo.predict(future).tail(1)
            forecast['Sub-Category'] = subcategoria
            forecast['medida'] = m
            projecao = pd.concat([projecao, forecast])

    # Otimização com Pyomo
    projecao_pivot = projecao.pivot_table(
        index='Sub-Category',
        columns='medida',
        values='yhat',
        aggfunc='sum'
    ).reset_index()

    valor_total = projecao_pivot['Sales'].sum() - projecao_pivot['Profit'].sum()
    unidades = projecao_pivot['Quantity'].sum() * 0.7
    indice = projecao_pivot.index.tolist()
    lucro = projecao_pivot['Profit'].values
    quantidade = projecao_pivot['Quantity'].values
    valor = projecao_pivot['Sales'].values

    model = pyo.ConcreteModel()
    model.x = pyo.Var(indice, within=pyo.Binary)
    model.valores_constraint = pyo.Constraint(expr=sum(model.x[i] * valor[i] for i in indice) <= valor_total)
    model.quantidade_constraint = pyo.Constraint(expr=sum(model.x[i] * quantidade[i] for i in indice) <= unidades)
    model.objective = pyo.Objective(expr=sum(model.x[i] * lucro[i] for i in indice), sense=pyo.maximize)

    # Resolução do modelo
    solver = SolverFactory('glpk')
    results = solver.solve(model)
    solution = [pyo.value(model.x[i]) for i in indice]

    # Exibição dos resultados
    projecao_pivot['Comprar'] = solution
    st.subheader("Resultados da Otimização")
    st.dataframe(projecao_pivot, use_container_width=True)
