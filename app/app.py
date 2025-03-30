# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Q5v8XgoOtJg3_2-XZV9Kvg6xOfqiAzas
"""

# app.py
import dash
from dash import Dash
import dash_bootstrap_components as dbc
from data import carregar_dados
from layout import criar_layout
from callbacks import registrar_callbacks
import os

# Inicializa o app com o tema DARKLY e os ícones do Font Awesome
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME])
server = app.server  # Necessário para o deploy (por exemplo, no Heroku)

# Carrega os dados e cálculos do projeto
dados = carregar_dados()

# Define o layout do app com base nos dados carregados
app.layout = criar_layout(dados)

# Registra os callbacks (se houver)
registrar_callbacks(app, dados)

if __name__ == '__main__':
    app.run(debug=True)
     port = int(os.environ.get("PORT", 8050))  # Usa a porta do Heroku ou 8050 como fallback
    app.run(host="0.0.0.0", port=port, debug=False)
