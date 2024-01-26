import streamlit as st

opcoes_ferramentas = [
    "Extração de dados",
    "Processamento de dados",
    "Carregamento de dados"
]


def render_sidebar():
    st.sidebar.title("Ferramentas")
    opcao_selecionada = st.sidebar.selectbox("Selecione uma opção:", opcoes_ferramentas)
    return opcao_selecionada
