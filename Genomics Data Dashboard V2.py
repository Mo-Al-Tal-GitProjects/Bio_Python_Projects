# Enhanced Import Section
import dash
from dash import dcc, html, Input, Output, State
from dash import dash_table
from dash.exceptions import PreventUpdate

import plotly.express as px  # For creating interactive plots
import datetime
import base64
import io
import pandas as pd

# Import GenomicsData class from data_definitions module
from data_definitions import GenomicsData

# Initialize the Dash application
app = dash.Dash(__name__, title="Genomics Data Dashboard", suppress_callback_exceptions=True)

# App layout with added class names for CSS
app.layout = html.Div([
    # Header
    html.H1("Genomics Data Dashboard", className='header'),
    
    # Content Section
    html.Section(id='content', children=[
        # Data Upload Section
        html.Div(id='data-upload-section', children=[
            html.H2("Data Upload", className='h2'),
            dcc.Upload(
                id='upload-data',
                className='upload-area',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                multiple=True
            ),
        ], className='six columns'),
        
        # Analysis Selector Section
        html.Div(id='analysis-selector-section', children=[
            html.H2("Analysis Selector", className='h2'),
            dcc.Dropdown(
                id='analysis-type-dropdown',
                className='analysis-selector',
                options=[
                    {'label': 'Genomic Sequence Analysis', 'value': 'GSA'},
                    {'label': 'Gene Expression Analysis', 'value': 'GEA'},
                    {'label': 'Variant Analysis', 'value': 'VA'},
                ],
                value='GSA',  # Default value
                clearable=False,
            ),
        ], className='six columns'),

        # Toolbar Section for additional controls
        html.Div(id='toolbar', className='toolbar', children=[
            html.Button('New Analysis', id='new-analysis-button', n_clicks=0),
            html.Button('Reset', id='reset-button', n_clicks=0),
            html.Button('Download Results', id='download-button', n_clicks=0),
        ], style={'textAlign': 'center', 'margin': '20px'}),

        html.Div(id='output-data-upload'),

    ], className='row'),
    
    # Interactive Data Table Section
    html.Div(id='interactive-table', children=[
        dash_table.DataTable(
            id='genomic-data-table',
            columns=[
                {'name': 'Gene', 'id': 'gene'},
                {'name': 'Sequence', 'id': 'sequence'},
                {'name': 'Length', 'id': 'length'},
                # Add more columns as needed
            ],
            data=[],  # Placeholder data
            editable=True,  # Allow inline editing of data
            filter_action="native",  # Allow filtering of data by user
            sort_action="native",  # Allow sorting of data by user
            sort_mode="multi",  # Allow sorting across multiple columns
            row_selectable="multi",  # Allow users to select multiple rows
            page_action="native",  # All records are paginated
            page_current=0,  # Page number that user is currently on
            page_size=10,  # Number of rows visible per page
        ),
    ]),
    
    # Visualization Area Section
    html.Div(id='visualization-area', children=[
        dcc.Graph(
            id='genomic-data-visualization',
            figure={}  # Placeholder for the actual figure, to be updated dynamically
        )
    ]),
    
    # Footer Section
    html.Footer(id='footer', children=[
        html.P("Genomics Data Dashboard - All Rights Reserved."),
        html.P("Powered by Dash")
    ], style={'textAlign': 'center', 'padding': '10px', 'background': 'lightgrey'}),

])

# Callback to handle file upload and display its content
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True  # This prevents the callback from running on startup
)
def update_output(contents, filename):
    if contents is None:
        # No file was uploaded, return empty Div
        return html.Div()

    try:
        if isinstance(contents, list):
            # Take the first item in the list (assuming only one file is uploaded)
            content_type, content_string = contents[0].split(',')
        else:
            content_type, content_string = contents.split(',')
        
        print("Filename:", filename)
        print("Content type:", content_type)
        
        decoded = base64.b64decode(content_string)
        if 'csv' in content_type:
            # Use GenomicsData.from_csv method to load data
            genomics_data = GenomicsData.from_csv(io.StringIO(decoded.decode('utf-8')))
            # Convert data to DataFrame for display
            df = pd.DataFrame([vars(data) for data in genomics_data])
            # Display the data table
            table = dash_table.DataTable(
                id='genomic-data-table',
                columns=[{'name': i, 'id': i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=10
            )
            # Generate visualization
            if 'Gene' in df and 'Sequence' in df:
                figure = px.bar(df, x='Gene', y='Sequence')
                visualization = dcc.Graph(figure=figure)
            else:
                visualization = html.Div("Gene and/or Sequence columns not found in the uploaded CSV file.")
            
            return html.Div([table, visualization])
        else:
            return html.Div('File type not supported: please upload a CSV file.')
    except Exception as e:
        return html.Div(f'An error occurred while processing the file: {e}')

# Callback for resetting the dashboard
@app.callback(
    [
        Output('genomic-data-table', 'data'),
        Output('analysis-type-dropdown', 'value'),
        Output('genomic-data-visualization', 'figure'),
        # Add Outputs here for any other components that should be reset
    ],
    [Input('reset-button', 'n_clicks')],
    # Include States here if you need to maintain the state of any component while resetting others
)
def reset_dashboard(n_clicks):
    # If the reset button has been clicked (n_clicks > 0), we reset the table data, dropdown, and figure
    if n_clicks and n_clicks > 0:
        return [[], 'GSA', {}]  # Return the initial state for each component
    else:
        raise PreventUpdate  # If button has not been clicked, do nothing

# Helper function to parse contents
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div([
                'Unsupported file type.'
            ])
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ])
    
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.Hr(),
        dcc.Graph(
            figure=px.bar(df, x=df.columns[0], y=df.columns[1])  # Example graph, modify as needed
        ),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
