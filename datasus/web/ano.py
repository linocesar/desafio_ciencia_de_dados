from render import generator_seleted_box_ano

ano = list(range(2008, 2024))


def render_selectbox_ano():
    item_selecionado = generator_seleted_box_ano("Ano:", itens=ano)
    return item_selecionado
