import streamlit as st

from periodos import render_periodos
from coluna import render_coluna
from conteudo import render_conteudo
from sidebar import render_sidebar

st.title("DATASUS")
st.write("DADOS DETALHADOS DAS AIH - POR LOCAL INTERNAÇÃO - BRASIL")


def page_data_extraction():
    row1, row2 = st.columns(2, gap="large")

    with row1:
        render_coluna()

    with row2:
        render_conteudo()

    render_periodos()


def page_data_processing():
    st.write("Processamento de dados")


def page_data_loading():
    st.write("Carregamento de dados")


opcao_selecionada = render_sidebar()

if opcao_selecionada == "Extração de dados":
    page_data_extraction()
elif opcao_selecionada == "Processamento de dados":
    page_data_processing()
else:
    page_data_loading()
