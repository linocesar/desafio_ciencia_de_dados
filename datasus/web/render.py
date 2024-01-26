import streamlit as st


def generator_multiple_choices(titulo: str, itens: dict):

    selecionados = st.multiselect(f"Selecione {titulo}", list(itens.keys()), placeholder="Selecione itens")

    selecionar_todos_button = st.button("Selecionar Todos", key=titulo)

    if selecionar_todos_button:
        selecionados = list(itens.keys())

    itens_selecionados = [itens[iten] for iten in selecionados]

    st.write("Selecionados: ", itens_selecionados)
