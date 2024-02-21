import streamlit as st
import urllib.request as request
import requests
import os
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
from bs4 import BeautifulSoup

from periodos import render_periodos
from coluna import render_coluna
from conteudo import render_conteudo
from sidebar import render_sidebar
import coluna as item_colunas
import conteudo as item_conteudos
import periodos as item_periodos

st.set_page_config(layout="wide", page_title='DATASUS')
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
    if "file_uploader" not in st.session_state:
        st.session_state["file_uploader"] = 0

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    st.write("Processamento de dados")
    files_path = os.getcwd() + "/storage/"
    file_list = [file for file in os.listdir(files_path) if
                 os.path.isfile(os.path.join(files_path, file)) and file.endswith(".tab")]
    st.info(f"{len(file_list)} arquivos .tab presentes no diretório {files_path}")

    files = st.file_uploader("Selecione o arquivo .tab", type=['tab'], accept_multiple_files=True,
                             key=st.session_state["file_uploader"], )

    if files:
        st.session_state["uploaded_files"] = files

    if st.button("Limpar arquivos"):
        st.session_state["file_uploader"] += 1
        st.rerun()

    st.write("Número de arquivos selecionados: ", len(files))


def uploader_callback():
    if st.session_state['file_uploader'] is not None:
        st.session_state['ctr'] += 1
        print('Uploaded file #%d' % st.session_state['ctr'])


def page_data_loading():
    st.write("Carregamento de dados")


def bot(my_payload: str, my_filename: str, conta_arquivo: int, total_arquivos: int):
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

    result = download_file(filename_tabnet, my_filename, conta_arquivo, total_arquivos)

    print(result)


def format_filename(my_coluna: str, my_conteudo: str, my_periodo: str) -> str:
    my_filename = f"{my_coluna}_{my_conteudo}_{my_periodo}.tab"
    return my_filename


def download_file(filename_tabnet: str, my_filename: str, conta_arquivo: int, total_arquivos: int):
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
    try:
        time = 15
        response = request.Request(url=url, headers=headers)
        response = request.urlopen(response, timeout=time)
        content = response.read()
    except Exception as e:
        return f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - INFO - Arquivo {conta_arquivo} de {total_arquivos}: {my_filename} não foi possível baixar. ❌"

    # Write the response to a file
    try:
        with open(caminho_arquivo, "wb") as f:
            f.write(content)
        return f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - INFO - Arquivo {conta_arquivo} de {total_arquivos}: {my_filename} baixado com sucesso. ✅"
    except IOError:
        return f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - INFO - Arquivo {conta_arquivo} de {total_arquivos}: {my_filename} não foi possível salvar. ❌"


def download_files_parallel(urls: list, local_paths: list):
    arquivos = range(len(urls))
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = {executor.submit(bot, url, local_path, conta_arquivo + 1, len(arquivos)) for
                 url, local_path, conta_arquivo in zip(urls, local_paths, arquivos)}
        concluido, nao_concluido = wait(tasks, timeout=3)
    return concluido, nao_concluido


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


def on_download_button_click(my_periodos: list, my_colunas: list, my_conteudos: list):
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


def run_bot(my_payload, my_filename, conta_arquivo, numero_arquivos):
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
    try:
        time = 15
        response = requests.request("POST", url, headers=headers, data=my_payload, timeout=time)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar a tag 'A' dentro da tag 'td'
        tag_a = soup.find('td', class_='botao_opcao').findAll('a')

        # Extrair o HREF e o texto da tag 'A'
        filename_tabnet = tag_a[1].get('href')

        result = download_file(filename_tabnet, my_filename, conta_arquivo, numero_arquivos)

        return result
    except Exception as e:
        return f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - INFO - Arquivo {conta_arquivo} de {total_arquivos}: {my_filename} não foi possível baixar. ❌"


if __name__ == '__main__':

    opcao_selecionada = render_sidebar()

    if opcao_selecionada == "Extração de dados":

        periodos, colunas, conteudos = page_data_extraction()

        if st.button("Download", key=1):
            if len(colunas) > 0 and len(conteudos) > 0 and len(periodos) > 0:
                payloads, filenames, total_arquivos = on_download_button_click(periodos, colunas, conteudos)
                st.write(f"Total de arquivos: {total_arquivos}")

                with st.spinner("Running..."):
                    total = range(len(payloads))
                    bar = st.progress(0)
                    placeholder = st.empty()
                    log_area = st.empty()
                    log_data = ""
                    for payload, filename, idx in zip(payloads, filenames, total):
                        log_data += run_bot(payload, filename, filenames.index(filename) + 1,
                                            total_arquivos) + "\n"
                        idx += 1
                        progress = idx / len(total)
                        placeholder.text(f"{int(progress * 100)}%")
                        # update progress bar
                        bar.progress(progress)
                        log_area.markdown(f"```\n{log_data}\n```")
                # falhou, sucesso = download_files_parallel(payloads, filenames)
                # if len(sucesso) > 0:
                #     st.success(f"Arquivos baixados com sucesso: {len(sucesso)}")
                # if len(falhou) > 0:
                #     st.error(f"Arquivos falhados: {len(falhou)}")

    elif opcao_selecionada == "Processamento de dados":
        page_data_processing()
    else:
        page_data_loading()
