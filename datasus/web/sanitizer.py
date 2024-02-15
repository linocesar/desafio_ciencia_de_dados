import pandas as pd
import os
import re

# Diretório onde estão os arquivos .tab
diretorio_saida = 'storage/teste'
diretorio = 'storage/'
# Listar todos os arquivos .tab no diretório
arquivos_tab = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.tab')]
total_arquivos = len(arquivos_tab)
conta_arquivos = 0
encoding = 'windows-1252' # ISO-8859-15
# Iterar sobre cada arquivo .tab
for arquivo in arquivos_tab:
    # Ler o arquivo .tab
    df = pd.read_csv(os.path.join(diretorio, arquivo), sep='\t', encoding=encoding, skiprows=4)

    # Realizar as alterações necessárias no DataFrame df

    # Salvar o DataFrame com o mesmo nome do arquivo original
    df.to_csv(os.path.join(diretorio_saida, arquivo), sep=';', index=False, encoding='utf-8')
    conta_arquivos += 1

    print(f'Arquivo {conta_arquivos} de {total_arquivos}: alterações aplicadas ao arquivo {arquivo}')
