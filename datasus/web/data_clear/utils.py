import os


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
        return path
    return path


def get_path_filename(base: str, filename: str) -> str:
    """Retorna o caminho completo do arquivo

    :param str base: Diretorio base
    :param str filename: Nome do arquivo
    :return: Caminho completo do arquivo
    :rtype: str
    """
    return os.path.join(base, filename)


def get_arquivos_formato(diretorio: str, formato: str) -> list:
    """Retorna uma lista de arquivos do formato especificado

    :param str diretorio: Diretorio base
    :param str formato: Formato dos arquivos
    :return: Lista de arquivos do formato especificado
    :rtype: list
    """
    return [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith(formato)]
