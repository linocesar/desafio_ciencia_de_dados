import streamlit as st


def get_markdown_text_data_clean():
    markdown_text = """
    ###### Funções:
    - `limpar_nome_colunas(nome)`: Esta função recebe um nome de coluna como entrada, remove acentos, pontuações, números e espaços em branco desnecessários, substituindo-os por um sublinhado e convertendo o texto para minúsculas. Retorna o nome da coluna limpo.
    - `get_mes_ano(arquivo: str) -> tuple`: Esta função recebe o nome de um arquivo como entrada e extrai o mês e o ano do nome do arquivo, retornando-os como uma tupla.

    ###### Função `start()`:
    - Define algumas variáveis, como os diretórios de entrada e saída e o encoding a ser utilizado.
    - Verifica se o diretório de saída existe e, se não existir, o cria.
    - Lista todos os arquivos com extensão ".tab" no diretório de entrada.
    - Itera sobre cada arquivo encontrado:
      - Lê o arquivo usando o Pandas, aplicando o encoding especificado.
      - Renomeia as colunas do DataFrame usando a função `limpar_nome_colunas`.
      - Converte os valores das colunas para float se o arquivo tiver "valor" em seu nome.
      - Calcula o total do arquivo.
      - Adiciona colunas "mes" e "ano" com base no nome do arquivo.
      - Adiciona uma coluna "cod_municipio" com o código do município.
      - Cria um DataFrame contendo apenas linhas com municípios "IGNORADO" e extrai a UF a partir dessas linhas.
      - Usa esse DataFrame para atribuir corretamente a UF para as linhas correspondentes no DataFrame original.
      - Descarta linhas com municípios "IGNORADO".
      - Ignora as duas últimas linhas do DataFrame.
      - Calcula o total dos valores no DataFrame.
      - Converte as colunas "mes" e "uf" para tipos categóricos.
      - Altera o formato do arquivo de ".tab" para ".csv" e salva o DataFrame no diretório de saída.
      - Verifica se o total calculado bate com o total do arquivo. Se não bater, adiciona o nome do arquivo a uma lista de arquivos com soma errada.
    - Imprime mensagens informando o progresso e resultados do processamento.
    - No final, imprime o total de arquivos processados e, se houver algum com soma errada, lista esses arquivos.
    """
    with st.expander("Ver descrição da etapa:"):
        st.markdown(markdown_text, unsafe_allow_html=True)


def get_markdown_text_data_merge():
    markdown_text = """
    ###### Funções:
- **`get_periodos(arquivos: list) -> list`**:
   - Essa função recebe uma lista de nomes de arquivos .csv como entrada e retorna uma lista dos períodos (mes, ano) presentes nos nomes dos arquivos. Ela extrai o período a partir dos nomes dos arquivos.

- **`get_agrupagem(padrao: str, periodos: list, arquivos: list) -> dict`**:
   - Essa função cria um dicionário onde as chaves são os períodos (mes, ano) e os valores são listas dos arquivos .csv correspondentes a cada período. Ela filtra os arquivos com base em um padrão especificado, nos períodos fornecidos e se o arquivo já foi mapeado anteriormente.

- **`merge_grupo_procedimento(grupo: dict, diretorio_output: str, diretorio_merged: str) -> int`**:
   - Esta função mescla conjuntos de dados de grupos de procedimentos (quantidades e valores) por período (mes, ano), utilizando o código do município como chave de junção. Ela lê os arquivos CSV, mescla os conjuntos de dados correspondentes, salva o arquivo mesclado e retorna o número total de conjuntos de dados mesclados.

- **`merged_subgrupo_procedimento(subgrupo: dict, diretorio_output: str, diretorio_merged: str) -> int`**:
   - Similar à função anterior, mas trabalha com subgrupos de procedimentos (quantidades e valores) em vez de grupos.

- **`start()`**:
   - Esta é a função principal. Ela inicializa alguns diretórios e variáveis, como os diretórios de entrada e saída. Em seguida, obtém os arquivos CSV disponíveis e os períodos correspondentes a partir desses arquivos.
   - Depois, faz a agregação dos arquivos em grupos e subgrupos com base em padrões especificados.
   - Em seguida, realiza a mesclagem dos dados tanto para grupos quanto para subgrupos, utilizando as funções mencionadas anteriormente.
   - Por fim, exibe algumas informações sobre o processo, como o número total de arquivos processados e o número de arquivos mesclados.
"""
    with st.expander("Ver descrição da etapa:"):
        st.markdown(markdown_text, unsafe_allow_html=True)


def get_markdown_text_data_merge_grupo():
    markdown_text = """
    ###### Funções:
    """
    with st.expander("Ver descrição da etapa:"):
        st.markdown(markdown_text, unsafe_allow_html=True)
