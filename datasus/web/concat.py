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
        print(f"Directory {path} created")
        return path
    return path


def concat_grupo(merged_dir: str, concat_dir: str):
    """Concatena os arquivos do grupo

    :param str merged_dir: Diretorio dos arquivos mesclados
    :param str concat_dir: Diretorio dos arquivos concatenados
    """
    padrao_grupo = r'^grupo_.*$'
    grupo = []
    arquivos = (
                [arquivo for arquivo in os.listdir(merged_dir)
                 if arquivo.endswith('.csv') and
                 re.match(padrao_grupo, arquivo)]
    )
    for arquivo in arquivos:
        csv = os.path.join(merged_dir, arquivo)
        df = pd.read_csv(csv, sep=',', encoding='utf-8')
        grupo.append(df)
    df_concat = pd.concat(grupo, ignore_index=True)
    try:
        df_concat.to_csv(os.path.join(concat_dir, 'grupo_procedimento.csv'), index=False, encoding='utf-8')
    except FileNotFoundError:
        print(f"Directory {concat_dir} not found")

def concat_subgrupo(merged_dir: str, concat_dir: str):
    """Concatena os arquivos do subgrupo procedimento

    :param str merged_dir: Diretorio dos arquivos mesclados
    :param str concat_dir: Diretorio dos arquivos concatenados
    """
    padrao_subgrupo = r'^subgrupo_.*$'
    subgrupo = []
    arquivos = (
                [arquivo for arquivo in os.listdir(merged_dir)
                 if arquivo.endswith('.csv') and
                 re.match(padrao_subgrupo, arquivo)]
    )
    for arquivo in arquivos:
        csv = os.path.join(merged_dir, arquivo)
        df = pd.read_csv(csv, sep=',', encoding='utf-8')
        subgrupo.append(df)
    df_concat = pd.concat(subgrupo, ignore_index=True)
    try:
        df_concat.to_csv(os.path.join(concat_dir, 'subgrupo_procedimento.csv'), index=False, encoding='utf-8')
    except FileNotFoundError:
        print(f"Directory {concat_dir} not found")


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