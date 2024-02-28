import os
from data_clear.utils import create_directory, get_path_filename, get_arquivos_formato
from data_clear.merge import get_periodos
import streamlit as st
import pandas as pd


def get_arquivos_agrupados_por_periodo(arquivos_csv, periodos):
    arquivos_agrupados_por_periodo = {}
    for periodo in periodos:
        arquivos_agrupados_por_periodo[periodo] = []
        for arquivo in arquivos_csv:
            if periodo in arquivo:
                arquivos_agrupados_por_periodo[periodo].append(arquivo)
    return arquivos_agrupados_por_periodo


def merge_grupo_subgrupo(grupo: dict, diretorio_input: str, diretorio_merged: str) -> int:

    grupo_tamanho = len(grupo.keys())
    grupo_merged = 0
    st.caption("Mesclando Grupos e Subgrupos para um mesmo período.")
    with st.empty():
        for k, mes_ano in enumerate(grupo.keys()):
            nome_arquivo = 'grupo_subgrupo_procedimento_quantidade_valor_aprovado_' + mes_ano + '.csv'

            if len(grupo[mes_ano]) == 2:
                # Ordena os arquivos .csv do grupo alfabeticamente
                grupo[mes_ano] = sorted(grupo[mes_ano])
                # Arquivo csv grupo procedimento quantidade a ser lido
                csv_quantidade = get_path_filename(diretorio_input, grupo[mes_ano][0])  # os.path.join(diretorio_output, grupo[mes_ano][0])
                # Arquivo csv grupo procedimento valor a ser lido
                csv_valor = get_path_filename(diretorio_input, grupo[mes_ano][1])
                # Dataframe grupo procedimento quantidade a ser lido
                df_quantidade = pd.read_csv(csv_quantidade, sep=',', encoding='utf-8')
                # Dataframe grupo procedimento valor a ser lido
                df_valor = pd.read_csv(csv_valor, sep=',', encoding='utf-8')
                # Dataframe grupo procedimento quantidade valor a ser mesclado
                df_merged = pd.merge(df_quantidade, df_valor, on=['cod_municipio', 'uf', 'municipio', 'ano', 'mes'],
                                     suffixes=('_grupo', '_subgrupo'))
                # Arquivo csv mesclado a ser salvo
                path_filename = get_path_filename(diretorio_merged, nome_arquivo)
                df_merged.to_csv(path_filename, sep=',', index=False, encoding='utf-8')
                out = f"Arquivo {k + 1}/{grupo_tamanho}: {nome_arquivo} gerado com sucesso."
                grupo_merged += 1
            else:
                out = f"Arquivo {k + 1}/{grupo_tamanho}: {nome_arquivo} não gerado."
            st.caption(out)
    return grupo_merged


def start(input_dir, output_dir):
    arquivos_csv = get_arquivos_formato(input_dir, '.csv')
    periodos = get_periodos(arquivos_csv)
    grupo_subgrupo = get_arquivos_agrupados_por_periodo(arquivos_csv, periodos)
    numero_arquivos_grupo_subgrupo = merge_grupo_subgrupo(grupo_subgrupo, input_dir, output_dir)
    st.caption(f"Total de arquivos .csv gerados com merge: {numero_arquivos_grupo_subgrupo}")
    st.caption("Merge finalizado!")

