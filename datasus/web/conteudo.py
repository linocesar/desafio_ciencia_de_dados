from render import generator_multiple_choices_conteudo

conteudo = {
    "Quantidade aprovada": "Quantidade_aprovada",
    "Valor aprovado": "Valor_aprovado"
}


def render_conteudo():
    itens = generator_multiple_choices_conteudo("Conteúdo", conteudo)
    return itens
