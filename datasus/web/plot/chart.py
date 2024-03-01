import streamlit as st
import plotly.express as px
import pandas as pd


@st.cache_data
def plot(df):
    # Determine the null values:
    df_null_vals = df.isnull().sum().to_frame()
    df_null_vals = df_null_vals.rename(columns={0: 'Nulo'})
    # Determine the not null values:
    df_not_null_vals = df.notna().sum().to_frame()
    df_not_null_vals = df_not_null_vals.rename(columns={0: 'Não Nulo'})
    # Combine the dataframes:
    df_null_count = pd.concat([df_null_vals, df_not_null_vals], ignore_index=False, axis=1).reset_index()

    df_null_count = df_null_count.rename(columns={'index': 'Procedimento'})

    df_g = df_null_count.groupby(['Nulo', 'Não Nulo']).size().reset_index()
    df_g = df_g.rename(columns={0: 'total'})

    df_g['percent'] = df_null_count.groupby(['Nulo', 'Não Nulo']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values


    st.write(df_g.head())

    # Generate Plot
    fig = px.bar(df_g, x="Procedimento", y=['total'],
                 color_discrete_map={'Não Nulo': 'blue', 'Nulo': 'red'}, text=df_g['percent'])
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
