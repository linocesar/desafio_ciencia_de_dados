import pandas as pd
import streamlit as st
from data_clear.utils import get_arquivos_formato, create_directory, get_path_filename


def start(filename: str, data_concat_dir: str, output_dir: str):
    try:
        # Lendo arquivo csv
        df_censo = pd.read_csv(filename, sep=';', encoding='latin1')
        # Selecionando colunas necessarias
        df_censo = df_censo[['CODIGO_MUNICIPIO', 'UF_Nome', 'Regiao_Nome', 'LONGITUDE', 'LATITUDE', 'NU_Populacao']]
        # Renomear colunas para minúsculo
        df_censo.rename(columns=lambda x: x.lower(), inplace=True)
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
        # Salvando o arquivo
        df.to_csv(get_path_filename(output_dir, 'datasus.csv'), sep=',',  index=False, encoding='utf-8')
        st.success("Processo concluído.")
    except Exception as e:
        st.error(f"Não foi possível executar o processo.{e}")
