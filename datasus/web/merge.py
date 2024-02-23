import os
import re
import pandas as pd

diretorio_base = 'storage/'
diretorio_output = diretorio_base + 'output/'
diretorio_merged = diretorio_base + 'merged/'

if not os.path.exists(diretorio_merged):
    os.makedirs(diretorio_merged)
    print(f"Diretório {diretorio_merged} criado")

arquivos_csv = [arquivo for arquivo in os.listdir(diretorio_output) if arquivo.endswith('.csv')]

print(f"Números de arquivos: {len(arquivos_csv)}")

mes_ano = []

for file in arquivos_csv:
    mes_ano.append(file.strip('.csv').split('_')[-2] + '_' + file.strip('.csv').split('_')[-1])
periodos = list(set(mes_ano))

padrao_grupo = r'^grupo_.*$'
padrao_subgrupo = r'^subgrupo_.*$'
grupo = {}
subgrupo = {}

for periodo in periodos:
    for arquivo in arquivos_csv:
        if re.match(padrao_grupo, arquivo):
            if arquivo.__contains__(periodo):
                if periodo not in grupo:
                    grupo[periodo] = []
                grupo[periodo].append(arquivo)

        if re.match(padrao_subgrupo, arquivo):
            if arquivo.__contains__(periodo):
                if periodo not in subgrupo:
                    subgrupo[periodo] = []
                subgrupo[periodo].append(arquivo)

grupo_tamanho = len(grupo.keys())
subgrupo_tamanho = len(subgrupo.keys())

print('Grupo merged quantidade - valor')
grupo_merged = 0
for k, mes_ano in enumerate(grupo.keys()):
    nome_arquivo = 'grupo_procedimento_quantidade_valor_aprovado_' + mes_ano + '.csv'
    if len(grupo[mes_ano]) == 2:

        csv_quantidade = diretorio_output + grupo[mes_ano][0]
        csv_valor = diretorio_output + grupo[mes_ano][1]
        df_quantidade = pd.read_csv(csv_quantidade, sep=',', encoding='utf-8')
        df_valor = pd.read_csv(csv_valor, sep=',', encoding='utf-8')
        df_merged = pd.merge(df_quantidade, df_valor, left_on='cod_municipio', right_on='cod_municipio', how='inner',
                             suffixes=('_qdt', '_val'))
        df_merged.to_csv(diretorio_merged + nome_arquivo, sep=',', index=False, encoding='utf-8')
        print(f"Arquivo {k+1}/{grupo_tamanho}: {nome_arquivo} gerado com sucesso.")
        grupo_merged += 1
    else:
        print(f"Arquivo {k+1}/{grupo_tamanho}: {nome_arquivo} não gerado.")

print('Subgrupo merged quantidade - valor')
subgrupo_merged = 0
for k, mes_ano in enumerate(subgrupo.keys()):
    nome_arquivo = 'subgrupo_procedimento_quantidade_valor_aprovado_' + mes_ano + '.csv'
    if len(subgrupo[mes_ano]) == 2:
        csv_quantidade = diretorio_output + subgrupo[mes_ano][0]
        csv_valor = diretorio_output + subgrupo[mes_ano][1]
        df_quantidade = pd.read_csv(csv_quantidade, sep=',', encoding='utf-8')
        df_valor = pd.read_csv(csv_valor, sep=',', encoding='utf-8')
        df_merged = pd.merge(df_quantidade, df_valor, left_on='cod_municipio', right_on='cod_municipio', how='inner',
                             suffixes=('_qdt', '_val'))
        df_merged.to_csv(diretorio_merged + nome_arquivo, sep=',', index=False, encoding='utf-8')
        print(f"Arquivo {k+1}/{subgrupo_tamanho}: {nome_arquivo} gerado com sucesso.")
        subgrupo_merged += 1
    else:
        print(f"Arquivo {k+1}/{subgrupo_tamanho}: {nome_arquivo} não gerado.")

print(f"Total de arquivos .csv processados: {len(arquivos_csv)}")
print(f"Total de arquivos .csv gerados com merge: {grupo_merged + subgrupo_merged}")
