import streamlit as st


def generator_multiple_choices_periodos(titulo: str, itens: dict):

    selecionados = st.multiselect(f"Selecione {titulo}", list(itens.keys()), placeholder="Selecione itens")

    selecionar_todos_button = st.button("Selecionar Todos")

    if selecionar_todos_button:
        selecionados = list(itens.keys())

    itens_selecionados = [itens[iten] for iten in selecionados]

    st.write("Selecionados: ", itens_selecionados)
    return itens_selecionados


def generator_multiple_choices_colunas(titulo: str, itens: dict):

    selecionados = st.multiselect(f"Selecione {titulo}", list(itens.keys()), placeholder="Selecione itens")

    itens_selecionados = [itens[iten] for iten in selecionados]

    st.write("Selecionados: ", itens_selecionados)
    return itens_selecionados


def generator_multiple_choices_conteudo(titulo: str, itens: dict):

    selecionados = st.multiselect(f"Selecione {titulo}", list(itens.keys()), placeholder="Selecione itens")

    # selecionar_todos_button = st.button("Selecionar Todos", key=f"selecionar_todos_{titulo}")
    #
    # if selecionar_todos_button:
    #     selecionados = list(itens.keys())

    itens_selecionados = [itens[iten] for iten in selecionados]

    st.write("Selecionados: ", itens_selecionados)

    return itens_selecionados

