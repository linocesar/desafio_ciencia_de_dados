import streamlit as st
import plotly.express as px
import pandas as pd
import folium
from branca.element import Template, MacroElement

from streamlit_folium import st_folium, folium_static

from procedimento import item_procedimentos_regex, procedimentos


# @st.cache_data
def plot_nulos(df):
    # Determine the null values:
    df_null_vals = df.isnull().sum().to_frame()
    df_null_vals = df_null_vals.rename(columns={0: 'Nulo'})
    # Determine the not null values:
    df_not_null_vals = df.notna().sum().to_frame()
    df_not_null_vals = df_not_null_vals.rename(columns={0: 'Não Nulo'})
    # Combine the dataframes:
    df_null_count = pd.concat([df_null_vals, df_not_null_vals], ignore_index=False, axis=1).reset_index()

    df_null_count = df_null_count.rename(columns={'index': 'Procedimento'})

    # df_g = df_null_count.groupby(['Nulo', 'Não Nulo']).size().reset_index()
    # df_g = df_g.rename(columns={0: 'total'})

    # Generate Plot
    fig = px.bar(df_null_count, x="Procedimento", y=['Não Nulo', 'Nulo'],
                 color_discrete_map={'Não Nulo': 'blue', 'Nulo': 'red'})
    fig.update_xaxes(categoryorder='total descending')
    fig.update_layout(
        title={'text': "Contagem de nulos e não nulos",
               'xanchor': 'center',
               'yanchor': 'top',
               'x': 0.5},
        xaxis_title="Procedimento",
        yaxis_title="Total")
    fig.update_layout(legend_title_text='Categoria')
    st.plotly_chart(fig, use_container_width=True)


def get_procedimento(item):
    return item_procedimentos_regex[item]


def get_tipo_procedimento(item):
    return procedimentos[item]


@st.cache_data
def plot_area_chart(df_datasus, procedimento):
    item_selecionado = get_procedimento(procedimento)

    df_datasus_agrupado_ano_regiao = (df_datasus.groupby(['ano', 'regiao_nome'], observed=True).agg(
        {coluna: lambda x: x.sum() for coluna in df_datasus.columns if '_qtd' in coluna}).reset_index())

    df_datasus_agrupado_ano_regiao.set_index('ano', inplace=True)

    fig = px.area(df_datasus_agrupado_ano_regiao.filter(regex=item_selecionado),
                  facet_col_wrap=1,
                  color='variable',
                  height=1000,
                  facet_col="regiao_nome")

    fig.update_yaxes(title_text='Quantidade')

    fig.update_layout(template='plotly_white',
                      title='Número de procedimentos por região entre 2008 a 2023',
                      xaxis=dict(tickmode='linear', tick0=2008, dtick=1),
                      legend=dict(
                          orientation="h", )
                      )
    st.plotly_chart(fig, use_container_width=True)


def plot_chart_unica_variavel_por_regiao(df_datasus, tipo_procedimento):
    item = get_tipo_procedimento(tipo_procedimento)

    df_datasus_agrupado_ano_regiao = (df_datasus.groupby(['ano', 'regiao_nome'], observed=True).agg(
        {coluna: lambda x: x.sum() for coluna in df_datasus.columns if
         '_qtd' in coluna or '_val' in coluna}).reset_index())

    df_datasus_agrupado_ano_regiao.set_index('ano', inplace=True)

    df_variable_regiao = df_datasus_agrupado_ano_regiao.filter(regex='regiao_nome$|_qtd$|_val$').loc[0:,
                         ['regiao_nome', item]]

    df_variable_regiao.sort_values(by=item, ascending=True, inplace=True)

    fig2 = px.bar(df_variable_regiao,
                  x=df_variable_regiao.index,
                  y=df_variable_regiao[item],
                  color='regiao_nome')

    fig2.update_layout(template='plotly_white', title='Número de procedimentos por região entre 2008 a 2023',
                       xaxis=dict(
                           tickmode='linear',
                           tick0=2008,
                           dtick=1
                       ))
    st.plotly_chart(fig2, use_container_width=True)


def plot_mapa_with_folium(df_datasus_cirurgias_agrupado, ano):
    my_map = folium.Map(location=[-3.849458, -52.402002],
                        tiles="OpenStreetMap",
                        zoom_start=4)

    df_datasus_cirurgias_agrupado_ano = df_datasus_cirurgias_agrupado.query('ano == @ano and total_ano > 100')

    df_faixa = pd.Series(pd.cut(x=df_datasus_cirurgias_agrupado_ano['total_ano'],
                                bins=4,
                                include_lowest=True,
                                right=False)).value_counts(sort=False).reset_index().rename(
        columns={'total_ano': 'faixa'})

    for municipio, uf, ano, total, latitude, longitude in zip(df_datasus_cirurgias_agrupado_ano.municipio,
                                                              df_datasus_cirurgias_agrupado_ano.uf,
                                                              df_datasus_cirurgias_agrupado_ano.ano,
                                                              df_datasus_cirurgias_agrupado_ano.total_ano,
                                                              df_datasus_cirurgias_agrupado_ano.latitude,
                                                              df_datasus_cirurgias_agrupado_ano.longitude):
        cor, radius = get_raio_cor(df_faixa.faixa[0:], total)

        folium.Circle(
            location=[latitude, longitude],
            radius=radius,
            weight=1,
            fill_opacity=0.6,
            opacity=0.6,
            color='black',
            fill_color=cor,
            fill=True,  # gets overridden by fill_color
            # popup="{} meters".format(total),
            tooltip="Município: {}-{}<br>Número de cirurgias em {}: {}".format(municipio, uf, ano, total),
        ).add_to(my_map)
    leg = legend(df_faixa.faixa[0:])
    my_map.get_root().add_child(leg)
    st_data = folium_static(my_map, width=1200, height=500)

    st.dataframe(df_datasus_cirurgias_agrupado_ano.filter(regex="municipio$|uf$|_qtd$|ano$").sort_values(by='total_ano', ascending=False))

def get_raio_cor(df, valor):
    cor = ""
    raio = 0
    for i, intervalo in enumerate(df):
        if valor in intervalo:
            match i:
                case 0:
                    cor = "#ffff8a"  # "rgb(253, 216, 117)"
                    raio = 5000
                case 1:
                    cor = "#ffff66"  # rgb(253, 158, 67)"
                    raio = 20000
                case 2:
                    cor = "#edef47"  # "rgb(251, 77, 41)"
                    raio = 40000
                case 3:
                    cor = "#cbcf32"  # 'rgb(128, 0, 37)'
                    raio = 50000
    return cor, raio


def legend(faixa):
    html1 = '''
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    bottom: 50px;
    right: 50px;
    width: 150px;
    height: 80px;
    z-index:9999;
    font-size:12px;">
    <div><b>Cirúrgias</div>
    <div style="background: #ffff8a;
    border-color: rgb(184, 152, 56);"></i><span>'''

    html2 = f"{faixa[0]}"

    html3 = '''</span></div>
    <div style="background: #ffff66;
    border-color: rgb(181, 98, 0);"></i><span>'''

    html4 = f"{faixa[1]}"

    '''</span></div>
    <div i style="background: #edef47;
    border-color: rgb(175, 0, 0);"></i><span>'''

    html5 = f"{faixa[2]}"

    html6 = '''</span></div>
    <div i style="background: #cbcf32;
    border-color: rgb(65, 0, 0);"></i><span>'''

    html7 = f"{faixa[3]}"

    html8 = '''</span></div>
    </div>
</div>

<div style="
    position: fixed;
    bottom: 50px;
    right: 50px;
    width: 150px;
    height: 80px;
    z-index:9998;
    font-size:14px;
    background-color: #ffffff;
    ">
</div>
}
{% endmacro %}
'''
    html = html1 + html2 + html3 + html4 + html5 + html6 + html7 + html8
    macro = MacroElement()
    macro._template = Template(html)
    return macro
