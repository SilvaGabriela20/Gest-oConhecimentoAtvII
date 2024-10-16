import streamlit as st

st.title('Tabela')
st.dataframe(
    st.session_state['df'],
    hide_index=True,
    use_container_width=True,
    column_config={
        'ORDERDATE': st.column_config.DateColumn(label='Data de Pedido'),
        'SALES': st.column_config.NumberColumn(label='Vendas', format='R$ %.2f'),
        'QUANTITYORDERED': st.column_config.NumberColumn(label='Quantidade'),
    }
)
