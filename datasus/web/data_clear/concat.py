import os
import re
import pandas as pd

from data_clear.utils import get_arquivos_formato, create_directory, get_path_filename

import streamlit as st


def concat_grupo(merged_dir: str, concat_dir: str):
    """Concatena os arquivos do grupo

    :param str merged_dir: Diretorio dos arquivos mesclados
    :param str concat_dir: Diretorio dos arquivos concatenados
    """
    grupo = []
    filename = 'grupo_subgrupo_procedimento_quantidade_valor_aprovado.csv'
    # Lista os arquivos do diretorio merged_dir que terminam com '.csv' e que contem o padrao_grupo.
    arquivos = (
        [arquivo for arquivo in os.listdir(merged_dir)
         if arquivo.endswith('.csv')]
    )
    try:
        if len(arquivos) == 0:
            raise ValueError
        # Itera sobre os arquivos e adiciona ao grupo.
        st.caption("Concatenando dataset..")
        for arquivo in arquivos:
            csv = os.path.join(merged_dir, arquivo)
            df = pd.read_csv(csv, sep=',', encoding='utf-8')
            grupo.append(df)
        #  Concatena os dataframes do grupo.
        df_concat = pd.concat(grupo, ignore_index=True)

        # Salva o arquivo concatenado no diretorio concat_dir.
        # O arquivo concatenado sera salvo com o nome 'grupo_procedimento.csv'.
        df_concat.to_csv(os.path.join(concat_dir, filename), index=False, encoding='utf-8')
        st.caption("Concatenado!")
        st.caption(f"Arquivo {filename} gerado com sucesso.")
    except Exception as e:
        st.caption('Nenhum arquivo .csv foi encontrado')


def concat_subgrupo(merged_dir: str, concat_dir: str):
    """Concatena os arquivos do subgrupo procedimento

    :param str merged_dir: Diretorio dos arquivos mesclados
    :param str concat_dir: Diretorio dos arquivos concatenados
    """
    padrao_subgrupo = r'^subgrupo_.*$'
    subgrupo = []

    # Lista os arquivos do diretorio merged_dir que terminam com '.csv' e que contem o padrao_subgrupo.
    arquivos = (
        [arquivo for arquivo in os.listdir(merged_dir)
         if arquivo.endswith('.csv') and
         re.match(padrao_subgrupo, arquivo)]
    )
    # Itera sobre os arquivos e adiciona ao subgrupo.
    for arquivo in arquivos:
        csv = os.path.join(merged_dir, arquivo)
        df = pd.read_csv(csv, sep=',', encoding='utf-8')
        subgrupo.append(df)
    # Concatena os dataframes do subgrupo.
    df_concat = pd.concat(subgrupo, ignore_index=True)
    try:
        # Salva o arquivo concatenado no diretorio concat_dir.
        # O arquivo concatenado sera salvo com o nome 'subgrupo_procedimento.csv'.
        df_concat.to_csv(os.path.join(concat_dir, 'subgrupo_procedimento.csv'), index=False, encoding='utf-8')
        st.caption(f"Arquivo subgrupo_procedimento.csv gerado com sucesso.")
    except FileNotFoundError:
        st.caption(f"Diretório {concat_dir} não encontrado")
        st.caption(f"Arquivo subgrupo_procedimento.csv não gerado.")


def start(input_dir, output_dir):
    concat_grupo(input_dir, output_dir)
