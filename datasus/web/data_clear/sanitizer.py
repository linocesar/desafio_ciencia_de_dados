import pandas as pd
import os
import re
import unicodedata
import time

import streamlit as st


def limpar_nome_colunas(nome):
    nome_sem_acentos = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('utf-8')
    nome_sem_pontuacoes = re.sub(r'[^\w\s]', ' ', nome_sem_acentos)
    nome_sem_numeros = re.sub(r'\d+', '', nome_sem_pontuacoes)
    nome_corrigido = " ".join(nome_sem_numeros.split())
    nome_sem_espacos = nome_corrigido.strip().replace(' ', '_').lower()
    return nome_sem_espacos


def get_mes_ano(arquivo: str) -> tuple:
    mes: str = arquivo.rsplit('.tab')[0].split('_')[-2].upper()
    ano: str = arquivo.rsplit('.tab')[0].split('_')[-1]
    return mes, ano


def start():
    # Diretório onde estão os arquivos .tab
    diretorio_saida = 'storage/output'
    diretorio = 'storage/'
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
        print("Diretório criado:", diretorio_saida)
    # Listar todos os arquivos .tab no diretório
    arquivos_tab = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.tab')]
    total_arquivos = len(arquivos_tab)
    conta_arquivos = 0
    arquivos_com_soma_errada = []
    encoding = 'windows-1252'  # ISO-8859-15

    with st.empty():
        # Iterar sobre cada arquivo .tab
        for arquivo in arquivos_tab:
            # Ler o arquivo .tab
            df = pd.read_csv(os.path.join(diretorio, arquivo), sep=';', encoding=encoding, skiprows=4)

            # Realizar as alterações necessárias no DataFrame df
            # Renomear as colunas do DataFrame df
            df.columns = [limpar_nome_colunas(col) for col in df.columns]

            # Ajustar os valores das colunas do DataFrame df para float dos arquivos .tab que contenham a nome 'valor'.
            if arquivo.__contains__('valor'):
                colunas_ajuste = df.columns[1:]
                for coluna in colunas_ajuste:
                    df[coluna] = df[coluna].astype(str).str.replace(',', '.').astype(float)

            # Calcular o total do arquivo .tab.
            total_tabnet = df.iloc[-1, -1]

            # Adicionar colunas 'mes' e 'ano' com os valores correspondentes do nome do arquivo .tab.
            df['mes'], df['ano'] = get_mes_ano(arquivo)

            # Adicionar coluna 'cod_municipio' com o código do município.
            df['cod_municipio'] = df['municipio'].apply(lambda x: x.split(' ')[0].strip())
            # Remover o código do município do nome do município.
            df['municipio'] = df['municipio'].apply(lambda x: ' '.join(x.split(' ')[1:]))

            # Criar um DataFrame com os dados de UF ignorados.
            df_uf = df[df['municipio'].str.contains('IGNORADO')].copy()
            df_uf['uf'] = df_uf['municipio'].apply(lambda x: x.split('-')[1].strip())
            df_uf.reset_index(inplace=True)

            # Adicionar coluna 'prox_index' com o valor do índice anterior.
            df_uf['prox_index'] = df_uf['index'].shift(-1)

            # Alterar tipo de dados da coluna 'prox_index' para inteiros.
            df_uf['prox_index'] = df_uf['prox_index'].fillna(len(df)).astype(int)

            # Trabalhando apenas com as colunas index, prox_index e uf.
            df_uf = df_uf[['index', 'prox_index', 'uf']]

            # Iterar sobre cada linha do DataFrame df_uf.
            for index, row in df_uf.iterrows():
                # Seleciona os municípios do primeiro DataFrame no intervalo entre 'index' e 'prox_index' e atribui o
                # valor de 'uf'
                df.loc[row['index']:row['prox_index'] - 1, 'uf'] = row['uf']

            # Descartar as linhas que contenham 'IGNORADO' na coluna 'municipio'
            df = df[~df['municipio'].str.contains('IGNORADO')]

            # Ignorar as duas últimas linhas
            df = df.iloc[:-2]

            # Somar os valores de todas as linhas e colunas com exceção de: 'municipio', 'mes', 'ano','cod_municipio',
            # 'uf' e 'total'
            total_app = df.iloc[0:, 1:-5].sum().sum()

            # Converter as colunas 'mes' e 'uf' para tipos categóricos.
            df['mes'] = df['mes'].astype('category')
            df['uf'] = df['uf'].astype('category')

            # Trocar o formato do arquivo .tab para .csv.
            arquivo = arquivo.replace('.tab', '.csv')

            # Salvar o DataFrame com o mesmo nome do arquivo original
            df.to_csv(os.path.join(diretorio_saida, arquivo), sep=',', index=False, encoding='utf-8')

            # Atualizar o contador de arquivos processados.
            conta_arquivos += 1

            out = f'Arquivo {conta_arquivos} de {total_arquivos}: alterações aplicadas ao arquivo {arquivo} 📝 \n'
            # print(f'Total tabnet: {total_tabnet}')
            # print(f'Total app: {round(total_app, 2)}')

            # Testando total encontrado no tabnet contra o total realizado pela aplicação
            if total_tabnet == round(total_app, 2):
                out += f'\nTotal tabnet: {total_tabnet}   Total app: {round(total_app, 2)} ✅'
            else:
                out += f'\nTotal tabnet: {total_tabnet}   Total app: {round(total_app, 2)}  ❌'
                arquivos_com_soma_errada.append(arquivo)
            time.sleep(0.1)
            st.caption(out)

        out_desc = f'Total de arquivos processados: {conta_arquivos}\n'
        if len(arquivos_com_soma_errada) > 0:
            out_desc += f'Total de arquivos com soma errada: {len(arquivos_com_soma_errada)}\n'
            for arquivo in arquivos_com_soma_errada:
                out_desc += f'\n{arquivo}\n'
        else:
            out_desc += '\nTodos os arquivos foram processados com sucesso!'
        st.caption(out_desc)
