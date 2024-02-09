import urllib.request as request

import os

url_base = "http://tabnet.datasus.gov.br"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    # 'Cookie': 'TS014879da=01e046ca4ce6c7798b4ea0cc135f51846c393958a053b1e1ede05d76e32700406eb7c5c8f7fada65ddaf62cd3d2933fbe9ce45558d'
}


def download_file(filename: str):
    print(f"Iniciando o download do arquivo {filename}")
    diretorio = "storage"
    if not os.path.exists(diretorio):
        os.mkdir(diretorio)
        print(f"Directory {diretorio} created successfully.")
    caminho_arquivo = os.path.join(diretorio, filename.split("/")[2])

    # Send the request and save the response
    url = url_base + filename
    response = request.Request(url=url, headers=headers)
    response = request.urlopen(response)
    content = response.read()
    # Write the response to a file
    print(caminho_arquivo)
    try:
        with open(caminho_arquivo, "wb") as f:
            f.write(content)
        print(f"File {filename} downloaded successfully.")
    except IOError:
        print(f"Error writing file {filename}.")
