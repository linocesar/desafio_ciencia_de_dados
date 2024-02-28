import pandas as pd
import streamlit as st
from data_clear.utils import get_arquivos_formato, create_directory, get_path_filename


def get_ordem_colunas():
    colunas_ordem = ['cod_municipio', 'municipio', 'uf', 'uf_nome',
                     'regiao_nome',
                     'longitude', 'latitude',
                     'nu_populacao', 'mes',
                     'ano',
                     'procedimentos_com_finalidade_diagnostica_qtd',
                     'procedimentos_com_finalidade_diagnostica_val',
                     'procedimentos_clinicos_qtd',
                     'procedimentos_clinicos_val',
                     'procedimentos_cirurgicos_qtd',
                     'procedimentos_cirurgicos_val',
                     'transplantes_de_orgaos_tecidos_e_celulas_qtd',
                     'transplantes_de_orgaos_tecidos_e_celulas_val',
                     'medicamentos_qtd',
                     'medicamentos_val',
                     'orteses_proteses_e_materiais_especiais_qtd',
                     'orteses_proteses_e_materiais_especiais_val',
                     'acoes_complementares_da_atencao_a_saude_qtd',
                     'acoes_complementares_da_atencao_a_saude_val',
                     'coleta_de_material_qtd',
                     'coleta_de_material_val',
                     'diagnostico_em_laboratorio_clinico_qtd',
                     'diagnostico_em_laboratorio_clinico_val',
                     'diagnostico_por_anatomia_patologica_e_citopatologia_qtd',
                     'diagnostico_por_anatomia_patologica_e_citopatologia_val',
                     'diagnostico_por_radiologia_qtd',
                     'diagnostico_por_radiologia_val',
                     'diagnostico_por_ultrasonografia_qtd',
                     'diagnostico_por_ultrasonografia_val',
                     'diagnostico_por_tomografia_qtd',
                     'diagnostico_por_tomografia_val',
                     'diagnostico_por_ressonancia_magnetica_qtd',
                     'diagnostico_por_ressonancia_magnetica_val',
                     'diagnostico_por_medicina_nuclear_in_vivo_qtd',
                     'diagnostico_por_medicina_nuclear_in_vivo_val',
                     'diagnostico_por_endoscopia_qtd',
                     'diagnostico_por_endoscopia_val',
                     'diagnostico_por_radiologia_intervencionista_qtd',
                     'diagnostico_por_radiologia_intervencionista_val',
                     'metodos_diagnosticos_em_especialidades_qtd',
                     'metodos_diagnosticos_em_especialidades_val',
                     'diagnostico_e_procedimentos_especiais_em_hemoterapia_qtd',
                     'diagnostico_e_procedimentos_especiais_em_hemoterapia_val',
                     'diagnostico_por_teste_rapido_qtd',
                     'diagnostico_por_teste_rapido_val',
                     'consultas_atendimentos_acompanhamentos_qtd',
                     'consultas_atendimentos_acompanhamentos_val',
                     'fisioterapia_qtd',
                     'fisioterapia_val',
                     'tratamentos_clinicos_outras_especialidades_qtd',
                     'tratamentos_clinicos_outras_especialidades_val',
                     'tratamento_em_oncologia_qtd',
                     'tratamento_em_oncologia_val',
                     'tratamento_em_nefrologia_qtd',
                     'tratamento_em_nefrologia_val',
                     'hemoterapia_qtd',
                     'hemoterapia_val',
                     'tratamento_de_lesoes_envenenamentos_e_outros_decorrentes_de_causas_externas_qtd',
                     'tratamento_de_lesoes_envenenamentos_e_outros_decorrentes_de_causas_externas_val',
                     'terapias_especializadas_qtd',
                     'terapias_especializadas_val',
                     'parto_e_nascimento_qtd',
                     'parto_e_nascimento_val',
                     'pequenas_cirurgias_e_cirurgias_de_pele_tecido_subcutaneo_e_mucosa_qtd',
                     'pequenas_cirurgias_e_cirurgias_de_pele_tecido_subcutaneo_e_mucosa_val',
                     'cirurgia_de_glandulas_endocrinas_qtd',
                     'cirurgia_de_glandulas_endocrinas_val',
                     'cirurgia_do_sistema_nervoso_central_e_periferico_qtd',
                     'cirurgia_do_sistema_nervoso_central_e_periferico_val',
                     'cirurgia_das_vias_aereas_superiores_da_face_da_cabeca_e_do_pescoco_qtd',
                     'cirurgia_das_vias_aereas_superiores_da_face_da_cabeca_e_do_pescoco_val',
                     'cirurgia_do_aparelho_da_visao_qtd',
                     'cirurgia_do_aparelho_da_visao_val',
                     'cirurgia_do_aparelho_circulatorio_qtd',
                     'cirurgia_do_aparelho_circulatorio_val',
                     'cirurgia_do_aparelho_digestivo_orgaos_anexos_e_parede_abdominal_qtd',
                     'cirurgia_do_aparelho_digestivo_orgaos_anexos_e_parede_abdominal_val',
                     'cirurgia_do_sistema_osteomuscular_qtd',
                     'cirurgia_do_sistema_osteomuscular_val',
                     'cirurgia_do_aparelho_geniturinario_qtd',
                     'cirurgia_do_aparelho_geniturinario_val',
                     'cirurgia_de_mama_qtd',
                     'cirurgia_de_mama_val',
                     'cirurgia_obstetrica_qtd',
                     'cirurgia_obstetrica_val',
                     'cirurgia_toracica_qtd',
                     'cirurgia_toracica_val',
                     'cirurgia_reparadora_qtd',
                     'cirurgia_reparadora_val',
                     'bucomaxilofacial_qtd',
                     'bucomaxilofacial_val',
                     'outras_cirurgias_qtd',
                     'outras_cirurgias_val',
                     'cirurgia_em_oncologia_qtd',
                     'cirurgia_em_oncologia_val',
                     'cirurgia_em_nefrologia_qtd',
                     'cirurgia_em_nefrologia_val',
                     'coleta_e_exames_para_fins_de_doacao_de_orgaos_tecidos_e_celulas_e_de_transplante_qtd',
                     'coleta_e_exames_para_fins_de_doacao_de_orgaos_tecidos_e_celulas_e_de_transplante_val',
                     'avaliacao_de_morte_encefalica_qtd',
                     'avaliacao_de_morte_encefalica_val',
                     'acoes_relacionadas_a_doacao_de_orgaos_e_tecidos_para_transplante_qtd',
                     'acoes_relacionadas_a_doacao_de_orgaos_e_tecidos_para_transplante_val',
                     'processamento_de_tecidos_para_transplante_qtd',
                     'processamento_de_tecidos_para_transplante_val',
                     'transplante_de_orgaos_tecidos_e_celulas_qtd',
                     'transplante_de_orgaos_tecidos_e_celulas_val',
                     'acompanhamento_e_intercorrencias_no_pre_e_pos_transplante_qtd',
                     'acompanhamento_e_intercorrencias_no_pre_e_pos_transplante_val',
                     'medicamentos_de_ambito_hospitalar_e_urgencia_qtd',
                     'medicamentos_de_ambito_hospitalar_e_urgencia_val',
                     'orteses_proteses_e_materiais_especiais_relacionados_ao_ato_cirurgico_qtd',
                     'orteses_proteses_e_materiais_especiais_relacionados_ao_ato_cirurgico_val',
                     'acoes_relacionadas_ao_estabelecimento_qtd',
                     'acoes_relacionadas_ao_estabelecimento_val',
                     'acoes_relacionadas_ao_atendimento_qtd',
                     'acoes_relacionadas_ao_atendimento_val',
                     'acoes_de_promocao_e_prevencao_em_saude',
                     'acoes_coletivas_individuais_em_saude',
                     'anestesiologia',
                     'tratamentos_odontologicos_qtd',
                     'tratamentos_odontologicos_val']

    return colunas_ordem


def start(filename: str, data_concat_dir: str, output_dir: str):
    try:
        # Lendo arquivo csv
        df_censo = pd.read_csv(filename, sep=';', encoding='latin1')
        # Selecionando colunas necessarias
        df_censo = df_censo[['CODIGO_MUNICIPIO', 'UF_Nome', 'Regiao_Nome', 'LONGITUDE', 'LATITUDE', 'NU_Populacao']]
        # Renomear colunas para minúsculo
        df_censo.rename(columns=lambda x: x.lower(), inplace=True)

        # Convertendo valores de colunas uf_nome e regiao_nome para minúsculo
        df_censo['uf_nome'] = df_censo['uf_nome'].str.upper()
        df_censo['regiao_nome'] = df_censo['regiao_nome'].str.upper()

        # Buscando dataset concantenado
        arquivo_csv = get_arquivos_formato(data_concat_dir, '.csv')
        # Caminho do arquivo concantenado
        arquivo_csv_file = get_path_filename(data_concat_dir, arquivo_csv[0])
        # Lendo dataset concantenado
        df_concat = pd.read_csv(arquivo_csv_file, sep=',', encoding='utf-8')
        # Mesclando os dataframes
        df = pd.merge(df_concat, df_censo, left_on='cod_municipio', right_on='codigo_municipio')
        #  Removendo coluna codigo municipio
        df.drop('codigo_municipio', axis=1, inplace=True)

        # Ordenando colunas
        df = df[get_ordem_colunas()]
        # Salvando o arquivo
        df.to_csv(get_path_filename(output_dir, 'datasus.csv'), sep=',', index=False, encoding='utf-8')
        st.success("Processo concluído.")
    except Exception as e:
        st.error(f"Não foi possível executar o processo.{e}")
