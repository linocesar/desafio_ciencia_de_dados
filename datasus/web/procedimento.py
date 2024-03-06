from render import generator_seleted_box_procedimentos, generator_seleted_box_todos_os_procedimentos

item_procedimentos_regex = {'Cirurgias': r'regiao_nome|^cirurgia_.*_qtd$|cirurgia.*_qtd$|bucomaxilofacial_qtd$',
                            'Procedimentos': r'regiao_nome|^procedimentos_.*_qtd$',
                            'Transplantes': r'regiao_nome|^transplante.*_qtd$|pos_transplante.*_qtd$',
                            'Medicamentos': r'regiao_nome|medicamentos.*_qtd$|medicamentos_.*_qtd',
                            'Proteses': r'regiao_nome|proteses_.*_qtd$',
                            'Ações de Saúde': r'regiao_nome|^acoes_.*_qtd$',
                            'Consultas e Tratamentos': r'regiao_nome|^consultas.*_qtd$|^tratamentos_.*_qtd$'
                                                       r'|^tratamento_'
                                                       r'.*_qtd$|terapia.*_qtd$',
                            'Parto e Nascimento': r'regiao_nome$|parto_.*_qtd$',
                            'Coleta e Diagnóstico': r'regiao_nome|^coleta.*_qtd$|^diagnostico_.*_qtd$',
                            'Todos': r'regiao_nome|_qtd$'
                            }

procedimentos = {
    'procedimentos_com_finalidade_diagnostica_qtd': 'procedimentos_com_finalidade_diagnostica_qtd',
    'procedimentos_com_finalidade_diagnostica_val': 'procedimentos_com_finalidade_diagnostica_val',
    'procedimentos_clinicos_qtd': 'procedimentos_clinicos_qtd',
    'procedimentos_clinicos_val': 'procedimentos_clinicos_val',
    'procedimentos_cirurgicos_qtd': 'procedimentos_cirurgicos_qtd',
    'procedimentos_cirurgicos_val': 'procedimentos_cirurgicos_val',
    'transplantes_de_orgaos_tecidos_e_celulas_qtd': 'transplantes_de_orgaos_tecidos_e_celulas_qtd',
    'transplantes_de_orgaos_tecidos_e_celulas_val': 'transplantes_de_orgaos_tecidos_e_celulas_val',
    'medicamentos_qtd': 'medicamentos_qtd',
    'medicamentos_val': 'medicamentos_val',
    'orteses_proteses_e_materiais_especiais_qtd': 'orteses_proteses_e_materiais_especiais_qtd',
    'orteses_proteses_e_materiais_especiais_val': 'orteses_proteses_e_materiais_especiais_val',
    'acoes_complementares_da_atencao_a_saude_qtd': 'acoes_complementares_da_atencao_a_saude_qtd',
    'acoes_complementares_da_atencao_a_saude_val': 'acoes_complementares_da_atencao_a_saude_val',
    'coleta_de_material_qtd': 'coleta_de_material_qtd',
    'coleta_de_material_val': 'coleta_de_material_val',
    'diagnostico_em_laboratorio_clinico_qtd': 'diagnostico_em_laboratorio_clinico_qtd',
    'diagnostico_em_laboratorio_clinico_val': 'diagnostico_em_laboratorio_clinico_val',
    'diagnostico_por_anatomia_patologica_e_citopatologia_qtd': 'diagnostico_por_anatomia_patologica_e_citopatologia_qtd',
    'diagnostico_por_anatomia_patologica_e_citopatologia_val': 'diagnostico_por_anatomia_patologica_e_citopatologia_val',
    'diagnostico_por_radiologia_qtd': 'diagnostico_por_radiologia_qtd',
    'diagnostico_por_radiologia_val': 'diagnostico_por_radiologia_val',
    'diagnostico_por_ultrasonografia_qtd': 'diagnostico_por_ultrasonografia_qtd',
    'diagnostico_por_ultrasonografia_val': 'diagnostico_por_ultrasonografia_val',
    'diagnostico_por_tomografia_qtd': 'diagnostico_por_tomografia_qtd',
    'diagnostico_por_tomografia_val': 'diagnostico_por_tomografia_val',
    'diagnostico_por_ressonancia_magnetica_qtd': 'diagnostico_por_ressonancia_magnetica_qtd',
    'diagnostico_por_ressonancia_magnetica_val': 'diagnostico_por_ressonancia_magnetica_val',
    'diagnostico_por_medicina_nuclear_in_vivo_qtd': 'diagnostico_por_medicina_nuclear_in_vivo_qtd',
    'diagnostico_por_medicina_nuclear_in_vivo_val': 'diagnostico_por_medicina_nuclear_in_vivo_val',
    'diagnostico_por_endoscopia_qtd': 'diagnostico_por_endoscopia_qtd',
    'diagnostico_por_endoscopia_val': 'diagnostico_por_endoscopia_val',
    'diagnostico_por_radiologia_intervencionista_qtd': 'diagnostico_por_radiologia_intervencionista_qtd',
    'diagnostico_por_radiologia_intervencionista_val': 'diagnostico_por_radiologia_intervencionista_val',
    'metodos_diagnosticos_em_especialidades_qtd': 'metodos_diagnosticos_em_especialidades_qtd',
    'metodos_diagnosticos_em_especialidades_val': 'metodos_diagnosticos_em_especialidades_val',
    'diagnostico_e_procedimentos_especiais_em_hemoterapia_qtd': 'diagnostico_e_procedimentos_especiais_em_hemoterapia_qtd',
    'diagnostico_e_procedimentos_especiais_em_hemoterapia_val': 'diagnostico_e_procedimentos_especiais_em_hemoterapia_val',
    'diagnostico_por_teste_rapido_qtd': 'diagnostico_por_teste_rapido_qtd',
    'diagnostico_por_teste_rapido_val': 'diagnostico_por_teste_rapido_val',
    'consultas_atendimentos_acompanhamentos_qtd': 'consultas_atendimentos_acompanhamentos_qtd',
    'consultas_atendimentos_acompanhamentos_val': 'consultas_atendimentos_acompanhamentos_val',
    'fisioterapia_qtd': 'fisioterapia_qtd',
    'fisioterapia_val': 'fisioterapia_val',
    'tratamentos_clinicos_outras_especialidades_qtd': 'tratamentos_clinicos_outras_especialidades_qtd',
    'tratamentos_clinicos_outras_especialidades_val': 'tratamentos_clinicos_outras_especialidades_val',
    'tratamento_em_oncologia_qtd': 'tratamento_em_oncologia_qtd',
    'tratamento_em_oncologia_val': 'tratamento_em_oncologia_val',
    'tratamento_em_nefrologia_qtd': 'tratamento_em_nefrologia_qtd',
    'tratamento_em_nefrologia_val': 'tratamento_em_nefrologia_val',
    'hemoterapia_qtd': 'hemoterapia_qtd',
    'hemoterapia_val': 'hemoterapia_val'}


# diagnostico_por_endoscopia_val
# diagnostico_por_radiologia_intervencionista_qtd
# diagnostico_por_radiologia_intervencionista_val
# metodos_diagnosticos_em_especialidades_qtd
# metodos_diagnosticos_em_especialidades_val
# diagnostico_e_procedimentos_especiais_em_hemoterapia_qtd
# diagnostico_e_procedimentos_especiais_em_hemoterapia_val
# diagnostico_por_teste_rapido_qtd
# diagnostico_por_teste_rapido_val
# consultas_atendimentos_acompanhamentos_qtd
# consultas_atendimentos_acompanhamentos_val
# fisioterapia_qtd
# fisioterapia_val
# tratamentos_clinicos_outras_especialidades_qtd
# tratamentos_clinicos_outras_especialidades_val
# tratamento_em_oncologia_qtd
# tratamento_em_oncologia_val
# tratamento_em_nefrologia_qtd
# tratamento_em_nefrologia_val
# hemoterapia_qtd
# hemoterapia_val
# tratamento_de_lesoes_envenenamentos_e_outros_decorrentes_de_causas_externas_qtd
# tratamento_de_lesoes_envenenamentos_e_outros_decorrentes_de_causas_externas_val
# terapias_especializadas_qtd
# terapias_especializadas_val
# parto_e_nascimento_qtd
# parto_e_nascimento_val
# pequenas_cirurgias_e_cirurgias_de_pele_tecido_subcutaneo_e_mucosa_qtd
# pequenas_cirurgias_e_cirurgias_de_pele_tecido_subcutaneo_e_mucosa_val
# cirurgia_de_glandulas_endocrinas_qtd
# cirurgia_de_glandulas_endocrinas_val
# cirurgia_do_sistema_nervoso_central_e_periferico_qtd
# cirurgia_do_sistema_nervoso_central_e_periferico_val
# cirurgia_das_vias_aereas_superiores_da_face_da_cabeca_e_do_pescoco_qtd
# cirurgia_das_vias_aereas_superiores_da_face_da_cabeca_e_do_pescoco_val
# cirurgia_do_aparelho_da_visao_qtd
# cirurgia_do_aparelho_da_visao_val
# cirurgia_do_aparelho_circulatorio_qtd
# cirurgia_do_aparelho_circulatorio_val
# cirurgia_do_aparelho_digestivo_orgaos_anexos_e_parede_abdominal_qtd
# cirurgia_do_aparelho_digestivo_orgaos_anexos_e_parede_abdominal_val
# cirurgia_do_sistema_osteomuscular_qtd
# cirurgia_do_sistema_osteomuscular_val
# cirurgia_do_aparelho_geniturinario_qtd
# cirurgia_do_aparelho_geniturinario_val
# cirurgia_de_mama_qtd
# cirurgia_de_mama_val
# cirurgia_obstetrica_qtd
# cirurgia_obstetrica_val
# cirurgia_toracica_qtd
# cirurgia_toracica_val
# cirurgia_reparadora_qtd
# cirurgia_reparadora_val
# bucomaxilofacial_qtd
# bucomaxilofacial_val
# outras_cirurgias_qtd
# outras_cirurgias_val
# cirurgia_em_oncologia_qtd
# cirurgia_em_oncologia_val
# cirurgia_em_nefrologia_qtd
# cirurgia_em_nefrologia_val
# coleta_e_exames_para_fins_de_doacao_de_orgaos_tecidos_e_celulas_e_de_transplante_qtd
# coleta_e_exames_para_fins_de_doacao_de_orgaos_tecidos_e_celulas_e_de_transplante_val
# avaliacao_de_morte_encefalica_qtd
# avaliacao_de_morte_encefalica_val
# acoes_relacionadas_a_doacao_de_orgaos_e_tecidos_para_transplante_qtd
# acoes_relacionadas_a_doacao_de_orgaos_e_tecidos_para_transplante_val
# processamento_de_tecidos_para_transplante_qtd
# processamento_de_tecidos_para_transplante_val
# transplante_de_orgaos_tecidos_e_celulas_qtd
# transplante_de_orgaos_tecidos_e_celulas_val
# acompanhamento_e_intercorrencias_no_pre_e_pos_transplante_qtd
# acompanhamento_e_intercorrencias_no_pre_e_pos_transplante_val
# medicamentos_de_ambito_hospitalar_e_urgencia_qtd
# medicamentos_de_ambito_hospitalar_e_urgencia_val
# orteses_proteses_e_materiais_especiais_relacionados_ao_ato_cirurgico_qtd
# orteses_proteses_e_materiais_especiais_relacionados_ao_ato_cirurgico_val
# acoes_relacionadas_ao_estabelecimento_qtd
# acoes_relacionadas_ao_estabelecimento_val
# acoes_relacionadas_ao_atendimento_qtd
# acoes_relacionadas_ao_atendimento_val
# acoes_de_promocao_e_prevencao_em_saude
# acoes_coletivas_individuais_em_saude
# anestesiologia
# tratamentos_odontologicos_qtd
# }


def render_selectbox():
    item_selecioando = generator_seleted_box_procedimentos("um item:", itens=item_procedimentos_regex)
    return item_selecioando


def render_selecbox_procedimentos():
    item_selecionado = generator_seleted_box_todos_os_procedimentos("item:", itens=procedimentos)
    return item_selecionado
