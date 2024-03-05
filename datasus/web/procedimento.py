from render import generator_seleted_box_procedimentos

item_procedimentos = {'Cirurgias': r'regiao_nome|^cirurgia_.*_qtd$|cirurgia.*_qtd$|bucomaxilofacial_qtd$',
                      'Procedimentos': r'regiao_nome|^procedimentos_.*_qtd$',
                      'Transplantes': r'regiao_nome|^transplante.*_qtd$|pos_transplante.*_qtd$',
                      'Medicamentos': r'regiao_nome|medicamentos.*_qtd$|medicamentos_.*_qtd',
                      'Proteses': r'regiao_nome|proteses_.*_qtd$',
                      'Ações de Saúde': r'regiao_nome|^acoes_.*_qtd$',
                      'Consultas e Tratamentos': r'regiao_nome|^consultas.*_qtd$|^tratamentos_.*_qtd$|^tratamento_.*_qtd$|terapia.*_qtd$',
                      'Parto e Nascimento': r'regiao_nome$|parto_.*_qtd$',
                      'Coleta e Diagnóstico': r'regiao_nome|^coleta.*_qtd$|^diagnostico_.*_qtd$',
                      'Todos': r'regiao_nome|_qtd$'
                      }


def render_selectbox():
    item_selecioando = generator_seleted_box_procedimentos("um item:", itens=item_procedimentos)
    return item_selecioando
