import dash
from dash import dcc, html, Dash, Input, Output, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots


caminho = 'https://raw.githubusercontent.com/geovatatsuga/dashboard-e-previsao-churn/70f10acd9155f688744a6d0cfe3df480d42e06c9/DADOS/df_atualizado.csv'
df = pd.read_csv(caminho)
#Criando dfs para facilitar a visualização no dashboard

# Cálculo de métricas gerais
total_clientes = len(df)
novos_clientes = len(df[df['Status_do_Cliente'] == 'Novo Cliente'])
total_churn = len(df[df['Status_do_Cliente'] == 'Churned'])
taxa_churn_geral = round((total_churn / total_clientes) * 100, 2)

contagem_churn_demografico = df[df['Status_do_Churn'] == 1].groupby('Gênero').size().reset_index(name='Total de Churn')

taxa_churn_por_tipo_pagamento = df.groupby('Método_de_Pagamento')['Status_do_Churn'].mean() * 100
taxa_churn_por_tipo_pagamento = taxa_churn_por_tipo_pagamento.round(2).sort_values(ascending=False)

taxa_churn_por_contrato = df.groupby('Contrato')['Status_do_Churn'].mean() * 100
taxa_churn_por_contrato = taxa_churn_por_contrato.round(2).sort_values(ascending=False)

taxa_churn_estados_top5 = df.groupby('Estado')['Status_do_Churn'].mean().nlargest(5) * 100
taxa_churn_estados_top5 = taxa_churn_estados_top5.round(2)

total_churn_categoria = df.groupby('Categoria_de_Churn')['Status_do_Churn'].sum().sort_values(ascending=False)

total_churn_tipo_internet = df.groupby('Tipo_de_Internet')['Status_do_Churn'].sum().sort_values(ascending=False)

# Filtrar apenas clientes que sofreram Churn (Status_do_Churn == 1)
df_churn = df[df['Status_do_Churn'] == 1].copy()

# Definir os intervalos e rótulos das faixas etárias
bins = [0, 20, 36, 51, 130]  # 130 como idade máxima para abranger todos os casos
labels = ['<20', '20-35', '36-50', '>50']

# Criar a coluna de faixa etária no DataFrame filtrado
df_churn['Faixa_etaria'] = pd.cut(df_churn['Idade'],
                                  bins=bins,
                                  labels=labels,
                                  right=False)  # Intervalo fechado à esquerda

# Contar as ocorrências de cada faixa etária
ttidade = df_churn['Faixa_etaria'].value_counts().sort_index()

#Criando Total de VALORES Churn POR ESDTADOS

# Filtrar churn, agrupar por estado e renomear a coluna de soma
total_valores_estados = (
    df[df['Status_do_Churn'] == 1]  # Filtra apenas churn
    .groupby('Estado')['Receita_Total']  # Agrupa por estado
    .sum()  # Soma a receita total
    .rename('Total_Receita_Churn_Estados')  # Renomeia a coluna
    .sort_values(ascending=False)  # Ordena do maior para o menor
)
# Definir a ordem correta das faixas etárias
ordem_correta = ['< 20', '20-35', '36-50', '> 50']

# Agrupar e contar o número de clientes por faixa etária
total_cliente_grupo_idade = df.groupby('Faixa_Idade').size().reset_index(name='Total_Clientes')

# Converter a coluna 'Faixa_Idade' para categórica com ordem definida
total_cliente_grupo_idade['Faixa_Idade'] = pd.Categorical(total_cliente_grupo_idade['Faixa_Idade'],
                                                          categories=ordem_correta,
                                                          ordered=True)

# Ordenar pela coluna categorizada
total_cliente_grupo_idade = total_cliente_grupo_idade.sort_values('Faixa_Idade')


taxa_churn_grupo_idade = df.groupby('Faixa_Idade')['Status_do_Churn'].mean() * 100
taxa_churn_grupo_idade = taxa_churn_grupo_idade.round(2)

# Criar a categorização com ordem definida
taxa_churn_grupo_idade.index = pd.Categorical(taxa_churn_grupo_idade.index, categories=ordem_correta, ordered=True)

# Ordenar pelo índice categórico
taxa_churn_grupo_idade = taxa_churn_grupo_idade.sort_index().round(2)

# Filtrar churn, agrupar por estado e renomear a coluna de soma
total_valores_estados = (
    df[df['Status_do_Churn'] == 1]  # Filtra apenas churn
    .groupby('Estado')['Receita_Total']  # Agrupa por estado
    .sum()  # Soma a receita total
    .rename('Total_Receita_Churn_Estados')  # Renomeia a coluna
    .sort_values(ascending=False)  # Ordena do maior para o menor
)


# Definir a ordem correta das faixas de tempo contratado (somente em Meses)
ordem_correta = ['< 6 Meses', '6-12 Meses', '12-18 Meses', '18-24 Meses', '>= 24 Meses']

# Agrupar e contar o número de clientes por faixa de tempo contratado
Total_clientes_por_tempo_contratado = df.groupby('Faixa_Tempo_Contrato').size().reset_index(name='Total_Clientes')

# Converter a coluna 'Faixa_Tempo_Contrato' para categórica com ordem definida
Total_clientes_por_tempo_contratado['Faixa_Tempo_Contrato'] = pd.Categorical(
    Total_clientes_por_tempo_contratado['Faixa_Tempo_Contrato'],
    categories=ordem_correta,
    ordered=True
)

# Ordenar pela coluna categorizada
Total_clientes_por_tempo_contratado = Total_clientes_por_tempo_contratado.sort_values('Faixa_Tempo_Contrato')



# Calcular a taxa de churn por faixa de tempo contratado
taxa_churn_por_tempo_contratado = df.groupby('Faixa_Tempo_Contrato')['Status_do_Churn'].mean() * 100

# Converter o índice para categórico com ordem definida
taxa_churn_por_tempo_contratado.index = pd.Categorical(
    taxa_churn_por_tempo_contratado.index,
    categories=ordem_correta,
    ordered=True
)

# Ordenar pelo índice categórico
taxa_churn_por_tempo_contratado = taxa_churn_por_tempo_contratado.sort_index().round(2)

data = df.copy()

fill_values = {
    'Promoção': 'Nenhuma',
    'Múltiplas_Linhas': 'Não',
    'Tipo_de_Internet': 'Nenhum',
    'Segurança_Online': 'Não',
    'Backup_Online': 'Não',
    'Proteção_de_Dispositivo': 'Não',
    'Suporte_Premium': 'Não',
    'TV_Streaming': 'Não',
    'Filmes_Streaming': 'Não',
    'Música_Streaming': 'Não',
    'Dados_Ilimitados': 'Não',
    'Categoria_de_Churn': 'Outros',
    'Motivo_de_Churn': 'Outros'
}

data.fillna(fill_values, inplace=True)

caminho3 = "https://raw.githubusercontent.com/geovatatsuga/dashboard-e-previsao-churn/main/DADOS/clientes_predictos.csv"

clientes_Predicted = pd.read_csv(caminho3)
clientespred = clientes_Predicted

# Cálculo de métricas gerais
total_clientes_previsto = len(clientespred)

# Churn por gênero
contagem_pred_demografico = clientespred[clientespred['Churn_Predict'] == 1].groupby('Gênero').size().reset_index(name='Total de previstos')

# Churn por método de pagamento
total_pred_por_tipo_pagamento = clientespred.groupby('Método_de_Pagamento')['Churn_Predict'].sum().reset_index()
total_pred_por_tipo_pagamento = total_pred_por_tipo_pagamento.sort_values(by='Churn_Predict', ascending=False)

# Churn por tipo de contrato
total_pred_por_contrato = clientespred.groupby('Contrato')['Churn_Predict'].sum().reset_index()
total_pred_por_contrato = total_pred_por_contrato.sort_values(by='Churn_Predict', ascending=False)

# Churn por estado (top 5)
total_pred_estados = clientespred.groupby('Estado')['Churn_Predict'].sum().reset_index()
total_pred_estados_top5 = total_pred_estados.sort_values(by='Churn_Predict', ascending=False).head(5)

# Churn por categoria e tipo de internet
total_pred_categoria = clientespred.groupby('Categoria_de_Churn')['Churn_Predict'].sum().sort_values(ascending=False)
total_pred_tipo_internet = clientespred.groupby('Tipo_de_Internet')['Churn_Predict'].sum().sort_values(ascending=False)



# Distribuição por faixa etária (Eixo X: Faixa, Eixo Y: Total)
# =====================================================
ordem_idade = ['< 20', '20-35', '36-50', '> 50']
total_cliente_grupo_idade_pred = clientespred.groupby('Faixa_Idade').size().reset_index(name='Total_Clientes')
total_cliente_grupo_idade_pred['Faixa_Idade'] = pd.Categorical(total_cliente_grupo_idade_pred['Faixa_Idade'], categories=ordem_idade, ordered=True)
total_cliente_grupo_idade_pred = total_cliente_grupo_idade_pred.sort_values('Faixa_Idade')

# =====================================================
# Distribuição por tempo de contrato (Eixo X: Faixa, Eixo Y: Total)
# =====================================================
ordem_tempo = ['< 6 Meses', '6-12 Meses', '12-18 Meses', '18-24 Meses', '>= 24 Meses']
total_clientes_tempo_contratado_pred = clientespred.groupby('Faixa_Tempo_Contrato').size().reset_index(name='Total_Clientes')
total_clientes_tempo_contratado_pred['Faixa_Tempo_Contrato'] = pd.Categorical(total_clientes_tempo_contratado_pred['Faixa_Tempo_Contrato'], categories=ordem_tempo, ordered=True)
total_clientes_tempo_contratado_pred = total_clientes_tempo_contratado_pred.sort_values('Faixa_Tempo_Contrato')

# CONSTANTES DE CORES
COR_PRIMARIA = "#8e44ad"
COR_SECUNDARIA = "#e74c3c"
COR_SUCESSO = "#27ae60"
COR_ALERTA = "#c0392b"
COR_AVISO = "#f39c12"
FUNDO_ESCURO = "#1a1a1a"
TEXTO_CLARO = "#ffffff"
SLOT_CLARO = "#ffffff"

todos_estados = pd.Series({
    'Uttar Pradesh': 629, 'Tamil Nadu': 600, 'Maharashtra': 504,
    'Karnataka': 470, 'Haryana': 398, 'Andhra Pradesh': 395,
    'West Bengal': 368, 'Punjab': 342, 'Bihar': 336, 'Gujarat': 335,
    'Jammu & Kashmir': 320, 'Madhya Pradesh': 288, 'Telangana': 281,
    'Rajasthan': 259, 'Kerala': 200, 'Odisha': 152, 'Assam': 139,
    'Delhi': 127, 'Jharkhand': 113, 'Uttarakhand': 62,
    'Chhattisgarh': 59, 'Puducherry': 41
})
total_valores_estados = total_valores_estados.reset_index()
# ================================
# FUNÇÕES AUXILIARES
# ================================
def criar_card(valor, titulo, cor_fundo, icone, card_id):
    return dbc.Card(
        dbc.CardBody([
            html.Div(className="d-flex align-items-center", children=[
                html.Div(className="icon-container me-3", children=[
                    html.I(className=icone, style={"fontSize": "2.5rem", "color": cor_fundo})
                ]),
                html.Div([
                    html.H2(valor, className="card-value mb-0", style={'color': cor_fundo}),
                    html.P(titulo, className="card-title mb-0", style={'color': '#555555'})
                ])
            ])
        ]),
        className="shadow-lg metric-card",
        style={
            'borderRadius': '15px',
            'backgroundColor': SLOT_CLARO,
            'transition': 'transform 0.2s',
            'margin': '0.5rem',
            'border': '1px solid #e0e0e0'
        },
        id=card_id
    )

def criar_grafico_combinado(total_df, taxa_series, titulo, eixo_x):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=total_df.iloc[:, 0],
            y=total_df['Total_Clientes'],
            name='Total de Clientes',
            marker_color=COR_PRIMARIA,
            opacity=0.7,
            text=total_df['Total_Clientes'],
            textposition='outside',
            texttemplate='%{text:,}',
            textfont=dict(color=TEXTO_CLARO)
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=taxa_series.index,
            y=taxa_series.values,
            name='Taxa de Churn',
            line=dict(color='red', width=2),
            mode='lines+markers+text',
            marker=dict(size=6, symbol='diamond'),
            text=[f'{val:.1f}%' for val in taxa_series.values],
            textposition='top center',
            textfont=dict(color=TEXTO_CLARO)
        ),
        secondary_y=True
    )
    max_churn = max(taxa_series.values)
    max_tick = 10 * ((int(max_churn) // 10 + 1))
    fig.update_layout(
        title_text=titulo,
        template='plotly_dark',
        height=320,
        margin=dict(l=15, r=15, t=60, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis_title=eixo_x,
        xaxis=dict(showgrid=False, color=TEXTO_CLARO),
        yaxis=dict(showgrid=False, color=TEXTO_CLARO),
        title_font=dict(size=18, family='Arial', color=TEXTO_CLARO),
        title_x=0.5,
        paper_bgcolor=FUNDO_ESCURO,
        plot_bgcolor=FUNDO_ESCURO
    )
    fig.update_yaxes(title_text="Clientes", secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="Churn (%)", secondary_y=True,
                   range=[0, max_tick], showgrid=False)
    return fig

def criar_grafico_horizontal(data_series, titulo, label_y, label_x, formato_percent=False):
    if formato_percent:
        text_template = '%{text:.1f}%'
        tick_format = '.1f%'
    else:
        text_template = '%{text:,}'
        tick_format = ','
    fig = px.bar(
        y=[str(i) for i in data_series.index],
        x=data_series.values,
        orientation='h',
        title=titulo,
        labels={'y': label_y, 'x': label_x},
        color_discrete_sequence=[COR_PRIMARIA]
    )
    fig.update_traces(
        text=data_series.values,
        textposition='outside',
        texttemplate=text_template,
        textfont=dict(color=TEXTO_CLARO)
    )
    fig.update_layout(
        template='plotly_dark',
        height=280,
        margin=dict(l=15, r=15, t=60, b=20),
        xaxis=dict(
            showgrid=False,
            tickformat=tick_format,
            range=[0, data_series.max() * 1.15],
            color=TEXTO_CLARO
        ),
        yaxis=dict(showgrid=False, color=TEXTO_CLARO),
        title_font=dict(size=16, family='Arial', color=TEXTO_CLARO),
        title_x=0.5,
        paper_bgcolor=FUNDO_ESCURO,
        plot_bgcolor=FUNDO_ESCURO
    )
    return fig

def criar_mapa_churn():
    df_map = todos_estados.reset_index()
    df_map.columns = ['Estado', 'Churn']
    df_map['Estado'] = df_map['Estado'].replace({
        'Jammu & Kashmir': 'Jammu and Kashmir',
        'Andhra Pradesh': 'Andhra Pradesh',
        'Uttar Pradesh': 'Uttar Pradesh'
    })
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    fig = px.choropleth_mapbox(
        df_map,
        geojson=geojson_url,
        locations='Estado',
        featureidkey='properties.ST_NM',
        color='Churn',
        color_continuous_scale='Viridis',
        range_color=(0, todos_estados.max()),
        mapbox_style="carto-darkmatter",
        zoom=3.5,
        center={"lat": 22.9734, "lon": 78.6569},
        opacity=0.8,
        hover_data={'Estado': True, 'Churn': ':,.0f'},
        labels={'Churn': 'Casos de Churn'}
    )
    fig.update_layout(
        title={
            'text': "<b>Distribuição de Churn por Estado</b>",
            'font': {'size': 24, 'color': TEXTO_CLARO, 'family': 'Arial Black'},
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'b': 20}
        },
        margin={"r":20,"t":80,"l":20,"b":20},
        coloraxis_colorbar=dict(
            title='Casos de Churn',
            thickness=15,
            len=0.6,
            title_font=dict(color=TEXTO_CLARO, size=12),
            tickfont=dict(color=TEXTO_CLARO, size=10),
            orientation='v',
            yanchor='middle',
            y=0.5,
            x=0.93
        ),
        paper_bgcolor=FUNDO_ESCURO,
        plot_bgcolor=FUNDO_ESCURO
    )
    fig.update_geos(
        visible=False,
        bgcolor='rgba(0,0,0,0)',
        lakecolor='#2a2a2a',
        landcolor='#1a1a1a',
        showcountries=True,
        countrycolor='#444444',
        countrywidth=0.5
    )
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>" +
                      "Churn: %{customdata[1]}<extra></extra>",
        marker=dict(line=dict(width=0.5, color='#333333'))
    )
    mapbox_layers=[
            {
                "sourcetype": "geojson",
                "source": geojson_url,
                "type": "symbol",
                "text-field": ["get", "ST_NM"],
                "text-size": 12,
                "text-color": "white",
                "text-halo-color": "#2a2a2a",
                "text-halo-width": 1
            }
        ]
    return fig

# ================================
# CRIAÇÃO DO SCATTER PLOT
# ================================
# Novo gráfico de dispersão com os dados corretos
fig_scatter_receita = px.scatter(
    total_valores_estados,
    x='Total_Receita_Churn_Estados',
    y='Estado',
    color='Total_Receita_Churn_Estados',
    color_continuous_scale='Viridis',  # Mesma escala do mapa
    title='Receita de Churn por Estado',
    labels={
        'Total_Receita_Churn_Estados': 'Receita Total de Churn',
        'Estado': 'Estado'
    },
    height=400
)

# Ajustes de estilo para combinar com o mapa
fig_scatter_receita.update_layout(
    template='plotly_dark',
    paper_bgcolor=FUNDO_ESCURO,
    plot_bgcolor=FUNDO_ESCURO,
    xaxis_title='Receita Total de Churn',
    yaxis_title='Estados',
    margin=dict(l=20, r=20, t=40, b=20),
    coloraxis_colorbar=dict(
        title='Receita Churn',
        thickness=15,
        len=0.6,
        title_font=dict(color=TEXTO_CLARO, size=12),
        tickfont=dict(color=TEXTO_CLARO, size=10)
    )
)

# Ajuste para ordenar os estados por receita (opcional)
fig_scatter_receita.update_yaxes(categoryorder='total ascending')

# ================================
# COMPONENTES PRINCIPAIS
# ================================
cabecalho_e_metricas = [
    dbc.Row(
        dbc.Col(
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-line me-2",
                          style={"color": COR_PRIMARIA, "fontSize": "2.5rem"}),
                    html.H1("Dashboard de Churn",
                           className="display-4 mb-0",
                           style={'color': TEXTO_CLARO})
                ], className="d-flex justify-content-center align-items-center"),
                html.P("Análise de Retenção de Clientes",
                      className="lead",
                      style={'color': COR_PRIMARIA})
            ], className="text-center py-4"),
            width=12
        )
    ),
    dbc.Row([
        dbc.Col(criar_card(
            f"{total_clientes:,}",
            "Total Clientes",
            COR_PRIMARIA,
            "fas fa-users",
            {'type': 'metric-card', 'index': 0}
        ), width=3),
        dbc.Col(criar_card(
            f"{novos_clientes:,}",
            "Novos Clientes",
            COR_SUCESSO,
            "fas fa-user-plus",
            {'type': 'metric-card', 'index': 1}
        ), width=3),
        dbc.Col(criar_card(
            f"{total_churn:,}",
            "Clientes Perdidos",
            COR_ALERTA,
            "fas fa-user-minus",
            {'type': 'metric-card', 'index': 2}
        ), width=3),
        dbc.Col(criar_card(
            f"{taxa_churn_geral:.1f}%",
            "Taxa de Churn",
            COR_AVISO,
            "fas fa-percentage",
            {'type': 'metric-card', 'index': 3}
        ), width=3)
    ], className="g-4 mb-4")
]

# ================================
# CRIAÇÃO DOS GRÁFICOS
# ================================
fig_faixa_etaria = criar_grafico_combinado(
    total_cliente_grupo_idade,
    taxa_churn_grupo_idade,
    "Churn por Faixa Etária",
    "Faixa Etária"
)

fig_tempo_contrato = criar_grafico_combinado(
    Total_clientes_por_tempo_contratado,
    taxa_churn_por_tempo_contratado,
    "Churn por Tempo de Contrato",
    "Meses de Contrato"
)

fig_churn_genero = px.pie(
    names=contagem_churn_demografico['Gênero'],
    values=contagem_churn_demografico['Total de Churn'],
    title='Churn por Gênero',
    color_discrete_sequence=[COR_PRIMARIA, COR_SECUNDARIA]
)

legenda_genero = html.Div([
    html.Table(
        className="table",
        children=[
            html.Thead(html.Tr([
                html.Th("Cor"),
                html.Th("Gênero"),
                html.Th("Clientes")
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(html.Div(style={'width': '20px', 'height': '20px', 'backgroundColor': COR_PRIMARIA})),
                    html.Td("Feminino"),
                    html.Td(f"{contagem_churn_demografico[contagem_churn_demografico['Gênero'] == 'Feminino']['Total de Churn'].values[0]:,}")
                ]),
                html.Tr([
                    html.Td(html.Div(style={'width': '20px', 'height': '20px', 'backgroundColor': COR_SECUNDARIA})),
                    html.Td("Masculino"),
                    html.Td(f"{contagem_churn_demografico[contagem_churn_demografico['Gênero'] == 'Masculino']['Total de Churn'].values[0]:,}")
                ])
            ])
        ],
        style={
            'marginTop': '20px',
            'backgroundColor': FUNDO_ESCURO,
            'color': TEXTO_CLARO,
            'width': '100%'
        }
    )
])

fig_churn_genero.update_traces(
    textinfo='label+percent+value',
    texttemplate='%{label}<br>%{value} (%{percent})',
    marker=dict(line=dict(color='black', width=1)),
    textfont=dict(color=TEXTO_CLARO, size=14),
    hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Porcentagem: %{percent}<extra></extra>",
    textposition='auto',
    insidetextorientation='horizontal'
)

fig_churn_genero.update_layout(
    template='plotly_dark',
    height=320,
    margin=dict(l=15, r=15, t=60, b=20),
    title_font=dict(size=18, family='Arial', color=TEXTO_CLARO),
    title_x=0.5,
    paper_bgcolor=FUNDO_ESCURO,
    showlegend=False
)

fig_taxa_pagamento = criar_grafico_horizontal(
    taxa_churn_por_tipo_pagamento,
    'Taxa de Churn por Método de Pagamento',
    'Método de Pagamento',
    'Taxa de Churn (%)',
    formato_percent=True
)

fig_churn_contrato = criar_grafico_horizontal(
    taxa_churn_por_contrato,
    'Taxa de Churn por Tipo de Contrato',
    'Tipo de Contrato',
    'Taxa de Churn (%)',
    formato_percent=True
)

fig_estado = criar_grafico_horizontal(
    todos_estados.sort_values(ascending=False).head(5),
    'Taxa de Churn por Estado (Top 5)',
    'Estado',
    'Taxa de Churn (%)',
    formato_percent=False
)

fig_categoria = criar_grafico_horizontal(
    total_churn_categoria,
    'Total de Churn por Categoria',
    'Categoria',
    'Clientes',
    formato_percent=False
)

fig_internet = criar_grafico_horizontal(
    total_churn_tipo_internet,
    'Total de Churn por Tipo de Internet',
    'Tipo de Internet',
    'Clientes',
    formato_percent=False
)

# ================================
# LAYOUT PRINCIPAL COM ABAS
# ================================

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME])
server = app.server  # Necessário para o deploy no Heroku
app.layout = dbc.Container([
    dbc.Tabs([
        # Aba Principal Existente
        dbc.Tab(
            label="Dashboard Principal",
            children=[
                *cabecalho_e_metricas,
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            html.Div([
                                dcc.Graph(figure=fig_churn_genero),
                                legenda_genero
                            ]),
                            style={'backgroundColor': FUNDO_ESCURO, 'border': '1px solid #333'}
                        ), width=4
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=fig_faixa_etaria),
                            style={'backgroundColor': FUNDO_ESCURO, 'border': '1px solid #333'}
                        ), width=4
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=fig_tempo_contrato),
                            style={'backgroundColor': FUNDO_ESCURO, 'border': '1px solid #333'}
                        ), width=4
                    )
                ], className="mb-4"),
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=fig_taxa_pagamento),
                            style={'backgroundColor': FUNDO_ESCURO, 'border': '1px solid #333'}
                        ), width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=fig_churn_contrato),
                            style={'backgroundColor': FUNDO_ESCURO, 'border': '1px solid #333'}
                        ), width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=fig_estado),
                            style={'backgroundColor': FUNDO_ESCURO, 'border': '1px solid #333'}
                        ), width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=fig_categoria),
                            style={'backgroundColor': FUNDO_ESCURO, 'border': '1px solid #333'}
                        ), width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=fig_internet),
                            style={'backgroundColor': FUNDO_ESCURO, 'border': '1px solid #333'}
                        ), width=3
                    )
                ], className="mb-4 g-2", justify="around")
            ],
            tabClassName="fw-bold"
        ),
        # Aba de Mapa Atualizada
        dbc.Tab(
            label="Mapa de Churn",
            children=[
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(
                                id='mapa-churn',
                                figure=criar_mapa_churn(),
                                config={
                                    'displayModeBar': True,
                                    'scrollZoom': True,
                                    'modeBarButtonsToAdd': ['zoomInMapbox', 'zoomOutMapbox']
                                }
                            ),
                            style={
                                'border': f'2px solid {COR_PRIMARIA}',
                                'borderRadius': '15px',
                                'backgroundColor': FUNDO_ESCURO
                            }
                        ), width=12
                    )
                ], className="mt-4"),

                # Novo Scatter Plot
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(figure=fig_scatter_receita),
                            style={'backgroundColor': FUNDO_ESCURO, 'border': '1px solid #333'}
                        ), width=12
                    )
                ], className="mt-4")
            ],
            tabClassName="fw-bold"
        ),
        # NOVA ABA DE ANÁLISE PREDITIVA
        dbc.Tab(
            label="Análise Preditiva",
            children=[
                # Cabeçalho
                dbc.Row([
                    dbc.Col(html.H1("Dashboard de Churn - Análise Preditiva",
                                   className='text-center mb-4',
                                   style={'color': COR_PRIMARIA, 'fontWeight': 'bold'}), width=12)
                ]),
                # Seção de Métricas e Tabela
                dbc.Row([
                    dbc.Col([
                        dbc.Card(style={'backgroundColor': FUNDO_ESCURO, 'border': f'2px solid {COR_PRIMARIA}'}, children=[
                            dbc.CardBody([
                                html.H4("Total de Clientes Previstos", className="card-title", style={'color': COR_PRIMARIA}),
                                html.H3(id='total-clientes', children=f"{total_clientes_previsto}",
                                       className="card-text text-center", style={'color': TEXTO_CLARO, 'fontWeight': 'bold'})
                            ])
                        ])
                    ], width=3),
                    dbc.Col([
                        dbc.Card(style={'backgroundColor': FUNDO_ESCURO, 'border': f'2px solid {COR_PRIMARIA}'}, children=[
                            dbc.CardBody([
                                html.H5("Clientes com Risco de Churn", className="card-title", style={'color': COR_PRIMARIA}),
                                dash_table.DataTable(
                                    id='clientes-pred-table',
                                    columns=[
                                        {'name': 'Customer ID', 'id': 'Customer_ID'},
                                        {'name': 'Idade', 'id': 'Idade'},
                                        {'name': 'Estado', 'id': 'Estado'}
                                    ],
                                    data=clientespred.to_dict('records'),
                                    page_size=10,
                                    style_table={
                                        'overflowX': 'auto',
                                        'height': '400px',
                                        'backgroundColor': FUNDO_ESCURO
                                    },
                                    style_cell={
                                        'textAlign': 'left',
                                        'padding': '8px',
                                        'backgroundColor': FUNDO_ESCURO,
                                        'color': TEXTO_CLARO,
                                        'border': f'1px solid {FUNDO_ESCURO}'
                                    },
                                    style_header={
                                        'backgroundColor': FUNDO_ESCURO,
                                        'fontWeight': 'bold',
                                        'color': TEXTO_CLARO,
                                        'borderBottom': f'2px solid {FUNDO_ESCURO}'
                                    },
                                    style_data_conditional=[
                                        {'if': {'row_index': 'odd'},
                                         'backgroundColor': '#373737'}
                                    ]
                                )
                            ])
                        ])
                    ], width=9)
                ], className='mb-4'),
                # Primeira Linha de Gráficos
               dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            style={
                                'backgroundColor': FUNDO_ESCURO,
                                'border': f'2px solid {COR_PRIMARIA}',
                                'height': '100%',
                                'display': 'flex',
                                'flexDirection': 'column'
                            },
                            children=[
                                dbc.CardBody([
                                    html.H5("Churn por Gênero",
                                           className="card-title mb-4",
                                           style={'color': COR_PRIMARIA, 'textAlign': 'center'}),
                                    # Gráfico de Pizza
                                    dcc.Graph(
                                        figure=px.pie(
                                            contagem_pred_demografico,
                                            names='Gênero',
                                            values='Total de previstos',
                                            title='Distribuição por Gênero',
                                            color_discrete_sequence=[COR_PRIMARIA, COR_SECUNDARIA],
                                            template='plotly_dark'
                                        ).update_layout(
                                            paper_bgcolor=FUNDO_ESCURO,
                                            plot_bgcolor=FUNDO_ESCURO,
                                            autosize=False,
                                            width=380,
                                            height=380,
                                            margin=dict(l=20, r=20, t=40, b=20),
                                            title_x=0.5
                                        ),
                                        style={"width": "100%", "height": "300px"}
                                    ),
                                    # Cards de Legendas
                                    html.Div([
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Card(
                                                    style={'backgroundColor': COR_PRIMARIA, 'borderRadius': '10px'},
                                                    children=[
                                                        dbc.CardBody([
                                                            html.H6("Feminino",
                                                                   style={'color': 'white', 'textAlign': 'center'}),
                                                            html.H4(f"{contagem_pred_demografico[contagem_pred_demografico['Gênero'] == 'Feminino']['Total de previstos'].values[0]:,}",
                                                                   style={'color': 'white', 'textAlign': 'center'})
                                                        ])
                                                    ])
                                            ], width=6),
                                            dbc.Col([
                                                dbc.Card(
                                                    style={'backgroundColor': COR_SECUNDARIA, 'borderRadius': '10px'},
                                                    children=[
                                                        dbc.CardBody([
                                                            html.H6("Masculino",
                                                                   style={'color': 'white', 'textAlign': 'center'}),
                                                            html.H4(f"{contagem_pred_demografico[contagem_pred_demografico['Gênero'] == 'Masculino']['Total de previstos'].values[0]:,}",
                                                                   style={'color': 'white', 'textAlign': 'center'})
                                                        ])
                                                    ])
                                            ], width=6)
                                        ], className="mt-3")
                                    ])
                                ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column'})
                            ]
                        )
                    ], width=4, className="d-flex justify-content-center"),
                    dbc.Col([
                        dbc.Card(style={'backgroundColor': FUNDO_ESCURO, 'border': f'2px solid {COR_PRIMARIA}'}, children=[
                            dbc.CardBody([
                                html.H5("Churn por Método de Pagamento", className="card-title", style={'color': COR_PRIMARIA}),
                                dcc.Graph(
                                    figure=px.bar(total_pred_por_tipo_pagamento,
                                                 x='Método_de_Pagamento',
                                                 y='Churn_Predict',
                                                 color='Método_de_Pagamento',
                                                 title='Comparativo por Método de Pagamento',
                                                 color_discrete_sequence=[COR_PRIMARIA, COR_SECUNDARIA, COR_SUCESSO],
                                                 template='plotly_dark')
                                    .update_layout(paper_bgcolor=FUNDO_ESCURO, plot_bgcolor=FUNDO_ESCURO)
                                )
                            ])
                        ])
                    ], width=8)
                ], className='mb-4'),
                # Segunda Linha de Gráficos
                dbc.Row([
                    dbc.Col([
                        dbc.Card(style={'backgroundColor': FUNDO_ESCURO, 'border': f'2px solid {COR_PRIMARIA}'}, children=[
                            dbc.CardBody([
                                html.H5("Top 5 Estados com Mais Previsões", className="card-title", style={'color': COR_PRIMARIA}),
                                dcc.Graph(
                                    figure=px.bar(total_pred_estados_top5,
                                                 x='Estado',
                                                 y='Churn_Predict',
                                                 color='Estado',
                                                 title='Estados com Maior Risco',
                                                 color_discrete_sequence=px.colors.sequential.Purpor_r,
                                                 template='plotly_dark')
                                    .update_layout(paper_bgcolor=FUNDO_ESCURO, plot_bgcolor=FUNDO_ESCURO)
                                )
                            ])
                        ])
                    ], width=12)
                ], className='mb-4'),
                # Terceira Linha de Gráficos
                dbc.Row([
                    dbc.Col([
                        dbc.Card(style={'backgroundColor': FUNDO_ESCURO, 'border': f'2px solid {COR_PRIMARIA}'}, children=[
                            dbc.CardBody([
                                html.H5("Churn por Tipo de Internet", className="card-title", style={'color': COR_PRIMARIA}),
                                dcc.Graph(
                                    figure=px.bar(total_pred_tipo_internet.reset_index(),
                                                 x='Tipo_de_Internet',
                                                 y='Churn_Predict',
                                                 color='Tipo_de_Internet',
                                                 title='Comparativo de Serviço de Internet',
                                                 color_discrete_sequence=[COR_PRIMARIA, COR_SECUNDARIA],
                                                 template='plotly_dark')
                                    .update_layout(paper_bgcolor=FUNDO_ESCURO, plot_bgcolor=FUNDO_ESCURO)
                                )
                            ])
                        ])
                    ], width=6),
                    dbc.Col([
                        dbc.Card(style={'backgroundColor': FUNDO_ESCURO, 'border': f'2px solid {COR_PRIMARIA}'}, children=[
                            dbc.CardBody([
                                html.H5("Distribuição por Faixa Etária", className="card-title", style={'color': COR_PRIMARIA}),
                                dcc.Graph(
                                    figure=px.bar(total_cliente_grupo_idade_pred,
                                                 x='Faixa_Idade',
                                                 y='Total_Clientes',
                                                 category_orders={'Faixa_Idade': ordem_idade},
                                                 title='Distribuição Etária',
                                                 color_discrete_sequence=[COR_PRIMARIA],
                                                 template='plotly_dark')
                                    .update_layout(paper_bgcolor=FUNDO_ESCURO, plot_bgcolor=FUNDO_ESCURO)
                                )
                            ])
                        ])
                    ], width=6)
                ], className='mb-4'),
                # Quarta Linha de Gráficos
                dbc.Row([
                    dbc.Col([
                        dbc.Card(style={'backgroundColor': FUNDO_ESCURO, 'border': f'2px solid {COR_PRIMARIA}'}, children=[
                            dbc.CardBody([
                                html.H5("Distribuição por Tempo de Contrato", className="card-title", style={'color': COR_PRIMARIA}),
                                dcc.Graph(
                                    figure=px.bar(total_clientes_tempo_contratado_pred,
                                                 x='Faixa_Tempo_Contrato',
                                                 y='Total_Clientes',
                                                 category_orders={'Faixa_Tempo_Contrato': ordem_tempo},
                                                 title='Tempo de Contrato Ativo',
                                                 color_discrete_sequence=px.colors.sequential.Purpor_r,
                                                 template='plotly_dark')
                                    .update_layout(paper_bgcolor=FUNDO_ESCURO, plot_bgcolor=FUNDO_ESCURO)
                                )
                            ])
                        ])
                    ], width=12)
                ], className='mb-4')
            ],
            tabClassName="fw-bold"
        )
    ])
], fluid=True, style={
    'backgroundColor': FUNDO_ESCURO,
    'padding': '20px',
    'minHeight': '100vh'
})

if __name__ == '__main__':
    app.run(debug=True)
