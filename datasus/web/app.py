import streamlit as st
import urllib.request as request
import requests
import os
import concurrent.futures

from bs4 import BeautifulSoup

from periodos import render_periodos
from coluna import render_coluna
from conteudo import render_conteudo
from sidebar import render_sidebar
import coluna as item_colunas
import conteudo as item_conteudos
import periodos as item_periodos


st.title("DATASUS")
st.write("DADOS DETALHADOS DAS AIH - POR LOCAL INTERNAÇÃO - BRASIL")


def page_data_extraction():
    row1, row2 = st.columns(2, gap="large")
    with row1:
        colunas_selecionadas = render_coluna()
    with row2:
        conteudos_selecionados = render_conteudo()
    periodos_selecionados = render_periodos()
    return periodos_selecionados, colunas_selecionadas, conteudos_selecionados


def page_data_processing():
    st.write("Processamento de dados")


def page_data_loading():
    st.write("Carregamento de dados")


def bot(my_payload, my_filename: str, conta_arquivo, total_arquivos):
    url = "http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sih/cnv/spabr.def"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'TS014879da=01e046ca4c445832e6f2cfb8df59fc3595c3c6f8c62e94977c4cb3bb5c81d260d639d01408f73fbbaa6974d28b7a6f93347c58fac3; TS014879da=01e046ca4cc962acf44854618d460670689b95a0bd4cf7fe0b31dc126280d02900f4a74385c4f5b3c5d9f623dbdc872d70dcead90e',
        'DNT': '1',
        'Origin': 'http://tabnet.datasus.gov.br',
        'Referer': 'http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/spabr.def',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 X11; Linux x86_64 AppleWebKit/537.36 KHTML: like Gecko Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=my_payload, timeout=15)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar a tag 'A' dentro da tag 'td'
    tag_a = soup.find('td', class_='botao_opcao').findAll('a')

    # Extrair o HREF e o texto da tag 'A'
    filename_tabnet = tag_a[1].get('href')

    download_file(filename_tabnet, my_filename, conta_arquivo, total_arquivos)
    #download_files_parallel(filename_tabnet, my_filename)


def format_filename(my_coluna: str, my_conteudo: str, my_periodo: str) -> str:
    my_filename = f"{my_coluna}_{my_conteudo}_{my_periodo}.tab"
    return my_filename


def download_file(filename_tabnet: str, my_filename: str, conta_arquivo, total_arquivos):
    diretorio = "storage"
    if not os.path.exists(diretorio):
        os.mkdir(diretorio)
        print(f"Diretório {diretorio} criado com sucesso.")
    caminho_arquivo = os.path.join(diretorio, my_filename)

    url = "http://tabnet.datasus.gov.br" + filename_tabnet
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'TS014879da=01e046ca4ce6c7798b4ea0cc135f51846c393958a053b1e1ede05d76e32700406eb7c5c8f7fada65ddaf62cd3d2933fbe9ce45558d'
    }

    response = request.Request(url=url, headers=headers)
    response = request.urlopen(response, timeout=15)
    content = response.read()

    # Write the response to a file
    try:
        with open(caminho_arquivo, "wb") as f:
            f.write(content)
        print(f"Arquivo {conta_arquivo} de {total_arquivos}: {my_filename} downloaded successfully.")
    except IOError:
        print(f"Error writing file {my_filename}.")


def download_files_parallel(urls, local_paths):
    total_arquivos = range(len(urls))
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(bot, url, local_path, conta_arquivo + 1, len(total_arquivos)) for url, local_path, conta_arquivo in zip(urls, local_paths, total_arquivos)]
        concurrent.futures.wait(futures)


def busca_chaves(itens: dict, valor_item: str) -> str:
    chave_encontrada = ""
    for chave, valor in itens.items():
        if valor == valor_item:
            chave_encontrada = chave
    chave_encontrada = chave_encontrada.replace(" ", "_")
    chave_encontrada = chave_encontrada.replace("/", "_")
    return chave_encontrada.lower()


def get_payload(my_coluna: str, my_conteudo: str, my_periodo: str):
    valor = f"Linha=Munic%EDpio&Coluna={my_coluna}&Incremento={my_conteudo}&Arquivos={my_periodo}&pesqmes1=Digite+o+texto+e+ache+f%E1cil&SMunic%EDpio=TODAS_AS_CATEGORIAS__&pesqmes2=Digite+o+texto+e+ache+f%E1cil&SCapital=TODAS_AS_CATEGORIAS__&pesqmes3=Digite+o+texto+e+ache+f%E1cil&SRegi%E3o_de_Sa%FAde_%28CIR%29=TODAS_AS_CATEGORIAS__&pesqmes4=Digite+o+texto+e+ache+f%E1cil&SMacrorregi%E3o_de_Sa%FAde=TODAS_AS_CATEGORIAS__&pesqmes5=Digite+o+texto+e+ache+f%E1cil&SMicrorregi%E3o_IBGE=TODAS_AS_CATEGORIAS__&pesqmes6=Digite+o+texto+e+ache+f%E1cil&SRegi%E3o_Metropolitana_-_RIDE=TODAS_AS_CATEGORIAS__&pesqmes7=Digite+o+texto+e+ache+f%E1cil&STerrit%F3rio_da_Cidadania=TODAS_AS_CATEGORIAS__&pesqmes8=Digite+o+texto+e+ache+f%E1cil&SMesorregi%E3o_PNDR=TODAS_AS_CATEGORIAS__&SAmaz%F4nia_Legal=TODAS_AS_CATEGORIAS__&SSemi%E1rido=TODAS_AS_CATEGORIAS__&SFaixa_de_Fronteira=TODAS_AS_CATEGORIAS__&SZona_de_Fronteira=TODAS_AS_CATEGORIAS__&SMunic%EDpio_de_extrema_pobreza=TODAS_AS_CATEGORIAS__&pesqmes14=Digite+o+texto+e+ache+f%E1cil&SProcedimento_Principal=TODAS_AS_CATEGORIAS__&SGrupo_Procedimento_Principal=TODAS_AS_CATEGORIAS__&pesqmes16=Digite+o+texto+e+ache+f%E1cil&SSubgrupo_Proced.Principal=TODAS_AS_CATEGORIAS__&pesqmes17=Digite+o+texto+e+ache+f%E1cil&SForma_organiza%E7%E3o_Principal=TODAS_AS_CATEGORIAS__&pesqmes18=Digite+o+texto+e+ache+f%E1cil&SProcedimento=TODAS_AS_CATEGORIAS__&SGrupo_procedimento=TODAS_AS_CATEGORIAS__&pesqmes20=Digite+o+texto+e+ache+f%E1cil&SSubgrupo_proced.=TODAS_AS_CATEGORIAS__&pesqmes21=Digite+o+texto+e+ache+f%E1cil&SForma_organiza%E7%E3o=TODAS_AS_CATEGORIAS__&SComplexidade=TODAS_AS_CATEGORIAS__&STipo_de_Financiamento=TODAS_AS_CATEGORIAS__&pesqmes24=Digite+o+texto+e+ache+f%E1cil&SSubTipo_de_Financiamento=TODAS_AS_CATEGORIAS__&pesqmes25=Digite+o+texto+e+ache+f%E1cil&SServi%E7o%2FClassifica%E7%E3o=TODAS_AS_CATEGORIAS__&SCBO_do_Profissional=TODAS_AS_CATEGORIAS__&zeradas=exibirlz&formato=table&mostre=Mostra"
    payloader = {"data-raw": valor}
    saida_formatada = "{" + ', '.join([f'"{k}": "{v}"' for k, v in payloader.items()]) + "}"
    return saida_formatada


def on_download_button_click(my_periodos, my_colunas, my_conteudos):
    payloads = []
    filenames = []
    arquivos = 0

    for coluna in my_colunas:
        for conteudo in my_conteudos:
            for periodo in my_periodos:
                minha_coluna = busca_chaves(item_colunas.colunas, coluna)
                meu_conteudo = busca_chaves(item_conteudos.conteudo, conteudo)
                meu_periodo = busca_chaves(item_periodos.periodos, periodo)

                filename = format_filename(minha_coluna, meu_conteudo, meu_periodo)
                my_payload = get_payload(coluna, conteudo, periodo)
                filenames.append(filename)
                payloads.append(my_payload)
                arquivos += 1

    return payloads, filenames, arquivos


opcao_selecionada = render_sidebar()


if opcao_selecionada == "Extração de dados":

    periodos, colunas, conteudos = page_data_extraction()

    if st.button("Download", key=1):
        if len(colunas) > 0 and len(conteudos) > 0 and len(periodos) > 0:
            payloads, filenames, arquivos = on_download_button_click(periodos, colunas, conteudos)
            st.write(f"Total de arquivos: {arquivos}")
            download_files_parallel(payloads, filenames)

elif opcao_selecionada == "Processamento de dados":
    page_data_processing()
else:
    page_data_loading()
