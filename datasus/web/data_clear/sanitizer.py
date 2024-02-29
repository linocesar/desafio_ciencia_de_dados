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
    mes: str = arquivo.rsplit('.csv')[0].split('_')[-2].upper()
    ano: str = arquivo.rsplit('.csv')[0].split('_')[-1]
    return mes, ano


def start(input_dir: str, output_dir: str):

    # Listar todos os arquivos  no diretório
    arquivos_tab = [arquivo for arquivo in os.listdir(input_dir) if arquivo.endswith('.csv')]
    total_arquivos = len(arquivos_tab)
    conta_arquivos = 0
    arquivos_com_soma_errada = []
    encoding = 'windows-1252'  # ISO-8859-15

    with st.empty():
        # Iterar sobre cada arquivo
        for arquivo in arquivos_tab:
            # Ler o arquivo
            df = pd.read_csv(os.path.join(input_dir, arquivo), sep=';', encoding='latin1', skiprows=3, skipfooter=5, engine='python')

            # Realizar as alterações necessárias no DataFrame df
            # Renomear as colunas do DataFrame df
            df.columns = [limpar_nome_colunas(col) for col in df.columns]

            # Adicionar coluna 'cod_municipio' com o código do município.
            df['cod_municipio'] = df['municipio'].apply(lambda x: x.split(' ')[0].strip())
            # Remover o código do município do nome do município.
            df['municipio'] = df['municipio'].apply(lambda x: ' '.join(x.split(' ')[1:]))

            # Descartar as linhas que contenham 'IGNORADO' na coluna 'municipio'
            df = df[~df['municipio'].str.contains('IGNORADO')]

            # Ajustar os valores das colunas do DataFrame df para float dos arquivos  que contenham a nome 'valor'.
            if arquivo.__contains__('valor'):
                df = df.replace('-', 0.0)
                colunas_ajuste = df.columns[1:-1]
                for coluna in colunas_ajuste:
                    df[coluna] = df[coluna].astype(str).str.replace(',', '.').astype(float)
            else:
                df = df.replace('-', 0)
                for coluna in df.columns[1:-1]:
                    df[coluna] = df[coluna].apply(lambda x: int(x))

            # Calcular o total do arquivo .csv.
            total_tabnet = df.iloc[-1, -2]

            # Dropa coluna 'total' do DataFrame df.
            df = df.drop('total', axis=1)

            # Ignorar as duas últimas linhas
            df = df.iloc[:-2]

            # Converter todas as colunas para tipo inteiro usando lambda e um loop
            df['municipio'] = df['municipio'].astype('category')

            # Somar os valores de todas as linhas e colunas com exceção de: 'municipio', 'mes', 'ano','cod_municipio',
            # e 'total'
            total_app = df.iloc[0:, 1:-1].sum().sum()

            # Adicionar colunas 'mes' e 'ano' com os valores correspondentes do nome do arquivo .
            df['mes'], df['ano'] = get_mes_ano(arquivo)

            # Salvar o DataFrame com o mesmo nome do arquivo original
            df.to_csv(os.path.join(output_dir, arquivo), sep=',', index=False, encoding='utf-8')

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
