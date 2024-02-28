import os
import re
import pandas as pd

from data_clear.utils import get_arquivos_formato, create_directory, get_path_filename

import streamlit as st
import time


def get_periodos(arquivos: list) -> list:
    """Retorna uma lista dos periodos (mes, ano) dos arquivos .csv.

    :param list arquivos: Lista dos arquivos .csv
    :return: Lista com elementos unicos no formato mes_ano
    :rtype: list
    """
    mes_ano = []
    for file in arquivos:
        # Separa o mes e ano do nome do arquivo .csv. Exemplo: mes_ano = ['jan_2020', 'fev_2020']
        mes_ano.append(file.strip('.csv').split('_')[-2] + '_' + file.strip('.csv').split('_')[-1])
    return list(set(mes_ano))


def get_agrupagem(padrao: str, periodos: list, arquivos: list) -> dict:
    """Cria dicionario onde as chaves sao os periodos (mes, ano) e os valores sao representados por uma lista
    dos arquivos .csv por periodo (mes, ano).

    :param str padrao: Padrao para identificar os arquivos .csv
    :param list periodos: Periodos (mes, ano)
    :param list arquivos: Arquivos .csv
    :return: Dicionario com as chaves e valores
    :rtype: dict
    """
    # Dicionario: periodo (mes, ano) e lista de arquivos .csv.
    # Exemplo:
    # {
    #     'jan_2020': ['grupo_procedimento_quantidade_aprovado_jan_2020.csv', 'grupo_procedimento_valor_aprovado_jan_2020.csv'],
    #     'fev_2020': ['grupo_procedimento_quantidade_aprovado_fev_2020.csv', 'grupo_procedimento_valor_aprovado_fev_2020.csv'],
    grupo = {}
    for periodo in periodos:
        for arquivo in arquivos:
            # Verificar se o arquivo .csv corresponde ao padrao, periodo e se já foi mapeado.
            if re.match(padrao, arquivo) and arquivo.__contains__(periodo):
                if periodo not in grupo:
                    grupo[periodo] = []
                grupo[periodo].append(arquivo)
    return grupo


def merge_grupo_procedimento(grupo: dict, diretorio_input: str, diretorio_merged: str) -> int:
    """Mescla datasets grupos de procedimentos quantidades e valores por periodo (mes, ano),
    utilizando cod_municipio como chave de juncao.

    :param dict grupo: Datasets pertencentes ao grupo
    :param str diretorio_input: Diretorio dos arquivos .csv gerados pelo etapa data clean
    :param str diretorio_merged: Diretorio dos arquivos resultantes desta etapa, merged
    :return: Total de datasets mesclados
    :rtype: int
    """

    grupo_tamanho = len(grupo.keys())
    grupo_merged = 0
    st.caption("Mesclando grupo quantidade valor")
    with st.empty():
        for k, mes_ano in enumerate(grupo.keys()):
            nome_arquivo = 'grupo_procedimento_quantidade_valor_aprovado_' + mes_ano + '.csv'

            if len(grupo[mes_ano]) == 2:

                # Ordena os arquivos .csv por ordem alfabetica
                grupo[mes_ano] = sorted(grupo[mes_ano])
                # Arquivo csv grupo procedimento quantidade a ser lido
                csv_quantidade = get_path_filename(diretorio_input, grupo[mes_ano][0]) # os.path.join(diretorio_output, grupo[mes_ano][0])
                # Arquivo csv grupo procedimento valor a ser lido
                csv_valor = get_path_filename(diretorio_input, grupo[mes_ano][1])
                # Dataframe grupo procedimento quantidade a ser lido
                df_quantidade = pd.read_csv(csv_quantidade, sep=',', encoding='utf-8')
                # Dataframe grupo procedimento valor a ser lido
                df_valor = pd.read_csv(csv_valor, sep=',', encoding='utf-8')
                # Dataframe grupo procedimento quantidade valor a ser mesclado
                df_merged = pd.merge(df_quantidade, df_valor, on=['cod_municipio', 'uf', 'municipio', 'ano', 'mes'],
                                     suffixes=('_qtd', '_val'))
                # Arquivo csv mesclado a ser salvo
                path_filename = get_path_filename(diretorio_merged, nome_arquivo)
                df_merged.to_csv(path_filename, sep=',', index=False, encoding='utf-8')
                out = f"Arquivo {k + 1}/{grupo_tamanho}: {nome_arquivo} gerado com sucesso."
                grupo_merged += 1
            else:
                out = f"Arquivo {k + 1}/{grupo_tamanho}: {nome_arquivo} não gerado."
            st.caption(out)
    return grupo_merged


def merged_subgrupo_procedimento(subgrupo: dict, diretorio_input: str, diretorio_merged: str) -> int:
    """Mescla datasets subgrupos de procedimentos quantidades e valores por periodo (mes, ano),
    utilizando cod_municipio como chave de juncao.

    :param dict subgrupo: Datasets pertencentes ao subgrupo
    :param str diretorio_input: Diretorio dos arquivos .csv gerados pelo etapa data clean
    :param str diretorio_merged: Diretorio dos arquivos resultantes desta etapa, merged
    :return: Total de datasets mesclados
    :rtype: int
    """

    subgrupo_tamanho = len(subgrupo.keys())
    subgrupo_merged = 0
    st.caption("Mesclando Subgrupo quantidade valor")
    with st.empty():
        for k, mes_ano in enumerate(subgrupo.keys()):
            nome_arquivo = 'subgrupo_procedimento_quantidade_valor_aprovado_' + mes_ano + '.csv'
            if len(subgrupo[mes_ano]) == 2:

                # Ordena os arquivos .csv do subgrupo.
                subgrupo[mes_ano] = sorted(subgrupo[mes_ano])
                # Arquivo csv subgrupo procedimento quantidade mapeado
                csv_quantidade = get_path_filename(diretorio_input, subgrupo[mes_ano][0])
                # Arquivo csv subgrupo procedimento valor mapeado
                csv_valor = get_path_filename(diretorio_input, subgrupo[mes_ano][1])
                # Dataframe subgrupo procedimento quantidade gerado
                df_quantidade = pd.read_csv(csv_quantidade, sep=',', encoding='utf-8')
                # Dataframe subgrupo procedimento valor gerado
                df_valor = pd.read_csv(csv_valor, sep=',', encoding='utf-8')
                # Dataframe subgrupo procedimento quantidade valor mesclado
                df_merged = pd.merge(df_quantidade, df_valor, on=['cod_municipio', 'uf', 'municipio', 'ano', 'mes'],
                                     suffixes=('_qtd', '_val'))
                # Arquivo csv mesclado a ser salvo
                path_filename = get_path_filename(diretorio_merged, nome_arquivo)
                df_merged.to_csv(path_filename, sep=',', index=False, encoding='utf-8')
                out = f"Arquivo {k + 1}/{subgrupo_tamanho}: {nome_arquivo} gerado com sucesso."
                subgrupo_merged += 1
            else:
                out = f"Arquivo {k + 1}/{subgrupo_tamanho}: {nome_arquivo} não gerado."
            st.caption(out)
            time.sleep(2)
    return subgrupo_merged


def start(input_dir, output_dir):
    padrao_grupo = r'^grupo_.*$'
    padrao_subgrupo = r'^subgrupo_.*$'
    arquivos_csv = get_arquivos_formato(input_dir, '.csv')
    try:
        if len(arquivos_csv) == 0:
            raise ValueError('Nenhum arquivo .csv encontrado.')
        periodos = get_periodos(arquivos_csv)
        grupo = get_agrupagem(padrao_grupo, periodos, arquivos_csv)
        numero_arquivos_grupo = merge_grupo_procedimento(grupo, input_dir, output_dir)
        subgrupo = get_agrupagem(padrao_subgrupo, periodos, arquivos_csv)
        numero_arquivos_subgrupo = merged_subgrupo_procedimento(subgrupo, input_dir, output_dir)
        st.caption("Merge finalizado!")
        st.caption(f"Total de arquivos .csv processados: {len(arquivos_csv)}")
        st.caption(f"Total de arquivos .csv gerados com merge: {numero_arquivos_grupo + numero_arquivos_subgrupo}")
        st.caption(f"Total de arquivos .csv mesclados do grupo: {numero_arquivos_grupo}")
        st.caption(f"Total de arquivos .csv mesclados do subgrupo: {numero_arquivos_subgrupo}")
        st.caption(f"Total de arquivos não mesclados do grupo: {len(grupo) - numero_arquivos_grupo}")
        st.caption(f"Total de arquivos não mesclados do subgrupo: {len(subgrupo) - numero_arquivos_subgrupo}")
    except Exception:
        st.caption(f'Não foi possível realizar a concatenação.')
