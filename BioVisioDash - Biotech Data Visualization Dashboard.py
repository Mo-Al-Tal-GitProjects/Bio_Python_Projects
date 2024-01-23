import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Create a Dash application
app = dash.Dash(__name__)

# Initialize an empty DataFrame to hold the data
df = pd.DataFrame(columns=['X', 'Y'])

# Define the layout of the dashboard with a biotech theme
app.layout = html.Div([
    html.H1("Biotech Data Visualization", style={'color': 'green'}),  # Change title and color

    dcc.Input(id='x-input', type='number', placeholder='Enter X-axis data', style={'margin': '10px'}),
    dcc.Input(id='y-input', type='number', placeholder='Enter Y-axis data', style={'margin': '10px'}),
    html.Button('Add Data Set', id='add-data-button', n_clicks=0, style={'margin': '10px'}),

    dcc.Dropdown(
        id='chart-type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Pie Chart', 'value': 'pie'},
            {'label': 'Line Chart', 'value': 'line'},
        ],
        value='scatter',
        style={'margin': '10px'}
    ),

    dcc.Graph(id='chart-output')  # Add chart-output graph
])

@app.callback(
    Output('chart-output', 'figure'),
    Input('x-input', 'value'),
    Input('y-input', 'value'),
    Input('add-data-button', 'n_clicks'),
    Input('chart-type', 'value'),
    State('chart-output', 'figure')
)
def update_chart(x_value, y_value, n_clicks, chart_type, existing_figure):
    if n_clicks > 0 and x_value is not None and y_value is not None:
        df.loc[len(df)] = [x_value, y_value]

    if chart_type == 'scatter':
        fig = go.Figure()
        for i, row in df.iterrows():
            fig.add_trace(go.Scatter(x=[row['X']], y=[row['Y']], mode='markers', name=f'Data Set {i + 1}'))
        fig.update_layout(title='Scatter Plot')
    elif chart_type == 'bar':
        fig = px.bar(df, x='X', y='Y', title='Bar Chart')
    elif chart_type == 'pie':
        fig = px.pie(df, names='X', values='Y', title='Pie Chart')
    elif chart_type == 'line':
        fig = go.Figure()
        for i, row in df.iterrows():
            fig.add_trace(go.Scatter(x=list(range(1, len(df) + 1)), y=df['Y'], mode='lines+markers', name=f'Data Set {i + 1}'))
        fig.update_layout(title='Line Chart')
    else:
        fig = go.Figure()

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
