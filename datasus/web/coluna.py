from render import generator_multiple_choices

colunas = {"Grupo Procedimento": "Grupo_procedimento",
           "Subgrupo Procedimento": "Subgrupo_proced."
           }


def render_coluna():
    generator_multiple_choices("Coluna", colunas)
