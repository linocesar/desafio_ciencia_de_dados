import os
import re
import pandas as pd


def create_directory(base: str, directory: str) -> str:
    """Cria um diretorio se ele nao existir

    :param str base:
    :param str directory: Nome do diretorio
    :return: Caminho do diretorio criado
    :rtype: str
    """
    path = os.path.join(base, directory)
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Diretório {directory} criado.")
        return path
    return path


def concat_grupo(merged_dir: str, concat_dir: str):
    """Concatena os arquivos do grupo

    :param str merged_dir: Diretorio dos arquivos mesclados
    :param str concat_dir: Diretorio dos arquivos concatenados
    """
    padrao_grupo = r'^grupo_.*$'
    grupo = []

    # Lista os arquivos do diretorio merged_dir que terminam com '.csv' e que contem o padrao_grupo.
    arquivos = (
                [arquivo for arquivo in os.listdir(merged_dir)
                 if arquivo.endswith('.csv') and
                 re.match(padrao_grupo, arquivo)]
    )
    # Itera sobre os arquivos e adiciona ao grupo.
    for arquivo in arquivos:
        csv = os.path.join(merged_dir, arquivo)
        df = pd.read_csv(csv, sep=',', encoding='utf-8')
        grupo.append(df)
    #  Concatena os dataframes do grupo.
    df_concat = pd.concat(grupo, ignore_index=True)
    try:
        # Salva o arquivo concatenado no diretorio concat_dir.
        # O arquivo concatenado sera salvo com o nome 'grupo_procedimento.csv'.
        df_concat.to_csv(os.path.join(concat_dir, 'grupo_procedimento.csv'), index=False, encoding='utf-8')
    except FileNotFoundError:
        print(f"Directório {concat_dir} não encontrado")


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
    except FileNotFoundError:
        print(f"Directório {concat_dir} não encontrado")


if __name__ == "__main__":
    path_base = os.path.dirname(os.path.abspath(__file__))
    storage = os.path.join(path_base, 'storage')
    merged = os.path.join(storage, 'merged')
    concat = create_directory(storage, 'concat')
    print("Concatenando grupo dataset..")
    concat_grupo(merged, concat)
    print("Concatenando subgrupo dataset..")
    concat_subgrupo(merged, concat)
    print("Concatenado!")
