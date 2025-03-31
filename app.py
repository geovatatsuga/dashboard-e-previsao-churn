# app.py
from dash import Dash
import dash_bootstrap_components as dbc
from layout import layout

# Criação da instância do Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME])
app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)
