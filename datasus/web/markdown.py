import streamlit as st


def get_markdown_text_data_clean():
    markdown_text = """
    ###### Funções:
    - `limpar_nome_colunas(nome)`: Esta função recebe um nome de coluna como entrada, remove acentos, pontuações, números e espaços em branco desnecessários, substituindo-os por um sublinhado e convertendo o texto para minúsculas. Retorna o nome da coluna limpo.
    - `get_mes_ano(arquivo: str) -> tuple`: Esta função recebe o nome de um arquivo como entrada e extrai o mês e o ano do nome do arquivo, retornando-os como uma tupla.

    ###### Função `start()`:
    - Define algumas variáveis, como os diretórios de entrada e saída e o encoding a ser utilizado.
    - Verifica se o diretório de saída existe e, se não existir, o cria.
    - Lista todos os arquivos com extensão "" no diretório de entrada.
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
      - Altera o formato do arquivo de "" para ".csv" e salva o DataFrame no diretório de saída.
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

- **`get_arquivos_agrupados_por_periodo(arquivos_csv, periodos)`**:
   - Esta função recebe uma lista de nomes de arquivos CSV e uma lista de períodos (mes, ano) como entrada e retorna um dicionário onde as chaves são os períodos e os valores são listas de arquivos CSV correspondentes a cada período.

- **`merge_grupo_subgrupo(grupo: dict, diretorio_input: str, diretorio_merged: str) -> int`**:
   - Esta função mescla conjuntos de dados de grupos e subgrupos de procedimentos para um mesmo período (mes, ano). Ela lê os arquivos CSV correspondentes aos grupos e subgrupos, mescla-os com base em colunas-chave específicas e salva o arquivo mesclado no diretório de saída. Retorna o número total de conjuntos de dados mesclados.

- **`start(input_dir, output_dir)`**:
   - Esta é a função principal. Ela recebe os diretórios de entrada e saída como entrada.
   - Primeiro, obtém uma lista de todos os arquivos CSV no diretório de entrada e os períodos correspondentes a partir desses arquivos.
   - Em seguida, agrupa os arquivos CSV por período usando a função `get_arquivos_agrupados_por_periodo`.
   - Depois, mescla os conjuntos de dados de grupo e subgrupo para cada período usando a função `merge_grupo_subgrupo`.
   - Por fim, exibe algumas informações sobre o processo, como o número total de arquivos gerados com mesclagem e uma mensagem indicando que o processo de mesclagem foi concluído.

    """
    with st.expander("Ver descrição da etapa:"):
        st.markdown(markdown_text, unsafe_allow_html=True)


def get_makdown_text_data_concatenate():
    markdown_text = """
    ###### Funções:

#### `concat_grupo_subgrupo(merged_dir: str, concat_dir: str)`:
- Esta função concatena os arquivos mesclados de grupos e subgrupos.
    - **Parâmetros**:
        - `merged_dir`: Diretório dos arquivos mesclados.
        - `concat_dir`: Diretório onde os arquivos concatenados serão salvos.
    - **Funcionamento**:
        - Lista os arquivos CSV no diretório mesclado.
        - Itera sobre os arquivos, lê cada um como DataFrame e os adiciona a uma lista.
        - Concatena os DataFrames da lista em um único DataFrame.
        - Salva o DataFrame concatenado como um arquivo CSV no diretório de saída com o nome `grupo_subgrupo_procedimento_quantidade_valor_aprovado.csv`.
    - **Exceções tratadas**:
        - Se nenhum arquivo CSV for encontrado no diretório mesclado, uma mensagem indicando isso é exibida.

#### `start(input_dir, output_dir)`:
- Esta é a função principal que inicia o processo de concatenação dos arquivos.
    - **Parâmetros**:
        - `input_dir`: Diretório dos arquivos mesclados.
        - `output_dir`: Diretório onde os arquivos concatenados serão salvos.
    """
    with st.expander("Ver descrição da etapa:"):
        st.markdown(markdown_text, unsafe_allow_html=True)


def get_markdown_data_merge_censo():
    markdown_text = """
    #### Funções:
    
#### `start(filename: str, data_concat_dir: str, output_dir: str)`:

Esta função é responsável por processar os dados do CENSO 2022:

- **Leitura do arquivo CSV de entrada**:
   - O código lê um arquivo CSV fornecido como entrada (`filename`). Este arquivo contém dados demográficos ou de censo.

- **Seleção de colunas necessárias**:
   - São selecionadas apenas as colunas necessárias para a análise. As colunas escolhidas incluem: 'CODIGO_MUNICIPIO', 'UF', 'UF_Nome', 'Regiao_Nome', 'LONGITUDE', 'LATITUDE' e 'NU_Populacao'.

- **Padronização dos nomes das colunas**:
   - Os nomes das colunas são renomeados para minúsculas para garantir consistência e facilidade de uso.

- **Padronização de valores de colunas**:
   - Os valores das colunas 'uf_nome' e 'regiao_nome' são convertidos para maiúsculas para garantir consistência e facilitar a correspondência com outros conjuntos de dados.

- **Leitura do dataset concatenado**:
   - O código busca pelo dataset concatenado gerado em uma etapa anterior, cujo caminho é fornecido pelo argumento `data_concat_dir`.

- **Mesclagem dos dataframes**:
   - Os dados do dataset concatenado e os dados demográficos são mesclados com base na coluna 'cod_municipio' do dataset concatenado e na coluna 'codigo_municipio' do dataset demográfico.

- **Remoção da coluna 'codigo_municipio'**:
   - Após a mesclagem, a coluna 'codigo_municipio' é removida do dataframe resultante.

- **Ordenação das colunas**:
   - As colunas do dataframe resultante são reordenadas de acordo com uma ordem específica.

- **Salvamento do arquivo processado**:
   - O dataframe resultante é salvo como um novo arquivo CSV no diretório de saída especificado pelo argumento `output_dir`.

- **Mensagem de conclusão**:
    - Se o processo for concluído com êxito, uma mensagem de sucesso é exibida. Caso contrário, uma mensagem de erro é exibida junto com a exceção que ocorreu.

Esse código realiza uma série de operações para preparar e processar os dados demográficos e de censo, produzindo um novo conjunto de dados pronto para análise.

    """
    with st.expander("Ver descrição da etapa:"):
        st.markdown(markdown_text, unsafe_allow_html=True)