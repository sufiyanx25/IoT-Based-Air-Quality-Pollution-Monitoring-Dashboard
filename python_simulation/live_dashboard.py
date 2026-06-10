from dash import Dash, dcc, html, Input, Output
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime
import os


DATA_CSV = os.path.join(os.path.dirname(__file__), '..', 'data', 'simulated_readings.csv')


def load_data():
    if os.path.exists(DATA_CSV):
        df = pd.read_csv(DATA_CSV, parse_dates=['timestamp'])
    else:
        df = pd.DataFrame(columns=['timestamp', 'node_id', 'pm25', 'pm10', 'gas', 'temperature', 'humidity'])
    return df


app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H2('IoT Air Quality — Live Dashboard'),
        html.Div(id='last-update', style={'color': '#666'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),

    dcc.Interval(id='interval', interval=10*1000, n_intervals=0),

    html.Div(id='indicators', style={'display': 'flex', 'gap': '12px', 'marginTop': '12px'}),

    dcc.Graph(id='pm-trend', style={'height': '380px'}),
    dcc.Graph(id='gas-trend', style={'height': '260px'}),

    html.H4('Recent Readings'),
    dash_table.DataTable(id='table', page_size=10, style_table={'overflowX': 'auto'}),
])


@app.callback(
    Output('indicators', 'children'),
    Output('pm-trend', 'figure'),
    Output('gas-trend', 'figure'),
    Output('table', 'data'),
    Output('last-update', 'children'),
    Input('interval', 'n_intervals')
)
def update(n):
    df = load_data()
    if df.empty:
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')
        return [html.Div('No data', style={'color': '#999'})], {}, {}, [], f'Last updated: {now}'

    df = df.sort_values('timestamp')
    latest = df.iloc[-1]

    # indicators
    def card(title, value, unit=''):
        return html.Div([
            html.Div(title, style={'fontSize': 12, 'color': '#444'}),
            html.Div(f"{value} {unit}", style={'fontSize': 20, 'fontWeight': '700'})
        ], style={'padding': '12px', 'background': 'white', 'borderRadius': '6px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)', 'minWidth': '140px'})

    indicators = [
        card('AQI (approx)', latest.get('aqi', '—')),
        card('PM2.5', latest.get('pm25', '—'), 'µg/m³'),
        card('PM10', latest.get('pm10', '—'), 'µg/m³'),
        card('Temp', latest.get('temperature', '—'), '°C'),
        card('Humidity', latest.get('humidity', '—'), '%'),
    ]

    # pm trend
    fig_pm = go.Figure()
    fig_pm.add_trace(go.Scatter(x=df['timestamp'], y=df['pm25'], mode='lines+markers', name='PM2.5'))
    fig_pm.add_trace(go.Scatter(x=df['timestamp'], y=df['pm10'], mode='lines+markers', name='PM10'))
    fig_pm.update_layout(title='Particulate Matter Trend', xaxis_title='Time', yaxis_title='µg/m³', template='plotly_white')

    # gas trend
    fig_gas = px.line(df, x='timestamp', y='gas', title='Gas Index Trend', template='plotly_white')

    table_data = df.sort_values('timestamp', ascending=False).head(50).to_dict('records')

    last_update = f"Last updated: {pd.to_datetime(latest['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}"

    return indicators, fig_pm, fig_gas, table_data, last_update


if __name__ == '__main__':
    app.run_server(debug=False, port=8050)
