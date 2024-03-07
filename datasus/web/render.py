import streamlit as st


def generator_multiple_choices_periodos(titulo: str, itens: dict):

    selecionados = st.multiselect(label=f"Selecione {titulo}",
                                  options=list(itens.keys()),
                                  placeholder="Selecione itens",
                                  )

    selecionar_todos_button = st.checkbox("Selecionar Todos")

    if selecionar_todos_button:
        selecionados = list(itens.keys())

    itens_selecionados = [itens[iten] for iten in selecionados]

    st.write("Selecionados: ", itens_selecionados)
    return itens_selecionados


def generator_multiple_choices_colunas(titulo: str, itens: dict):

    selecionados = st.multiselect(f"Selecione {titulo}", list(itens.keys()), placeholder="Selecione itens")

    selecionar_todos_button = st.checkbox("Selecionar Todos", key=f"selecionar_todos_{titulo}")

    if selecionar_todos_button:
        selecionados = list(itens.keys())

    itens_selecionados = [itens[iten] for iten in selecionados]

    st.write("Selecionados: ", itens_selecionados)
    return itens_selecionados


def generator_multiple_choices_conteudo(titulo: str, itens: dict):

    selecionados = st.multiselect(f"Selecione {titulo}", list(itens.keys()), placeholder="Selecione itens")

    selecionar_todos_button = st.checkbox("Selecionar Todos", key=f"selecionar_todos_{titulo}")

    if selecionar_todos_button:
        selecionados = list(itens.keys())

    itens_selecionados = [itens[iten] for iten in selecionados]

    st.write("Selecionados: ", itens_selecionados)

    return itens_selecionados


def generator_seleted_box_procedimentos(titulo: str, itens: dict):
    opcao = st.selectbox(f"Selecione {titulo}", list(itens.keys()), placeholder="Selecione um item", key='procedimento')
    return opcao


def generator_seleted_box_todos_os_procedimentos(titulo: str, itens: dict):
    opcao = st.selectbox(f"Selecione {titulo}", list(itens.keys()), placeholder="Selecione um item", key='procedimento_todos')
    return opcao


def generator_seleted_box_ano(titulo: str, itens: list):
    opcao = st.selectbox(f"Selecione {titulo}", itens, placeholder="Selecione um ano", key='ano')
    return opcao
