import streamlit as st
import plotly.express as px
import pandas as pd

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
                      title='Número de procedimentos por região entre 2008 a 2023', xaxis=dict(tickmode='linear',
                                                                                               tick0=2008,
                                                                                               dtick=1
                                                                                               )
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
