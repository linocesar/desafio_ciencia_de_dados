from render import generator_multiple_choices_colunas

colunas = {"Grupo Procedimento": "Grupo_procedimento",
           "Subgrupo Procedimento": "Subgrupo_proced."
           }


def render_coluna():
    colunas_selecionadas = generator_multiple_choices_colunas("Coluna", itens=colunas)
    return colunas_selecionadas
