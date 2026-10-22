import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

df = px.data.iris()

ancho_min = float(df["sepal_width"].min())
ancho_max = float(df["sepal_width"].max())

app.layout= html.Div([
    html.H1("Filtro por especies"),
    html.P("Ancho del sépalo (sepal_width)"),
    dcc.Dropdown(
        id="dropdown-especies",
        options=[
            {"label": "setosa", "value": "setosa"},
            {"label": "versicolor", "value": "versicolor"},
            {"label": "virginica", "value": "virginica"},
        ],
        value="setosa",
        placeholder="Seleccione una especie"
    ),
    dcc.RangeSlider(
      id="slider_ancho",
      min=ancho_min,
      max=ancho_max,
      step=0.1,
      value=[ancho_min, ancho_max],
      marks={
        round(ancho_min, 1): str(round(ancho_min, 1)),
        round(ancho_max, 1): str(round(ancho_max, 1)),
      },
      tooltip={"placement": "top", "always_visible": True}
    ),
    dcc.Graph(id="grafico-iris")
])

@callback(
    Output('grafico-iris', 'figure'), # lo que actualiza
    Input('dropdown-especies', 'value'), # Qué escuchar
    Input('slider-ancho', 'value'), # Qué escuchar
)

def actualizar_graficos(especie, rango_ancho):
  df_filtrado = df[(df['species'] == especie) & (df['sepal_width'].between(rango_ancho[0],rango_ancho[1]))]
  fig= px.scatter(df_filtrado, x="sepal_width",y="sepal_length",color="species", title=f"Gráfico de {especie}")
  return fig

if __name__ == '__main__':
  app.run(debug=False, port=8051)