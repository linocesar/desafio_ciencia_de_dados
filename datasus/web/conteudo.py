from render import generator_multiple_choices

conteudo = {
    "Quantidade aprovada": "Quantidade_aprovada",
    "Valor aprovado": "Valor_aprovado"
}


def render_conteudo():
    generator_multiple_choices("Conteúdo", conteudo)
