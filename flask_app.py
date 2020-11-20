import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

print(pd.__version__)
### REGULAR CODE HERE ###
color_data = pd.read_csv('/home/KenPomGraphs/mysite/static_data/team_color_legend.csv', index_col=0)
kp_data = pd.read_csv('/home/KenPomGraphs/mysite/static_data/current_data.csv', index_col=0)

conf_list = list(kp_data['Conf'].unique())
COLORS = {key: None for key in conf_list}
COLORS['B12'] = '#ef483e'
COLORS['WCC'] = '#33cad1'
COLORS['ACC'] = '#013ca6'
COLORS['BE'] = '#e41c39'
COLORS['B10'] = '#0088ce'
COLORS['SEC'] = '#ffd046'
COLORS['P12'] = '#004b91'
COLORS['Amer'] = '#e2231a'
COLORS['MWC'] = '#4f2d7f'
COLORS['A10'] = '#232220'
COLORS['MVC'] = '#e51636'
COLORS['SC'] = '#da291c'
COLORS['CUSA'] = '#bbbcbc'
COLORS['AE'] = '#1d2247'
COLORS['OVC'] = '#A51341'
COLORS['Sum'] = '#939598'
COLORS['Ivy'] = '#01563f'
COLORS['WAC'] = '#d9d4cc'
COLORS['SB'] = '#f2a900'
COLORS['Horz'] = '#f5a01a'
COLORS['BSth'] = '#F47B20'
COLORS['MAC'] = '#00a160'
COLORS['BW'] = '#2b265b'
COLORS['MAAC'] = '#004fa3'
COLORS['BSky'] = '#70cde3'
COLORS['Pat'] = '#FFFFFF'
COLORS['Slnd'] = '#FEB825'
COLORS['CAA'] = '#D4B07E'
COLORS['ASun'] = '#f3e500'
COLORS['NEC'] = '#006BA3'
COLORS['MEAC'] = '#34006D'
COLORS['SWAC'] = '#030303'



path = '/home/KenPomGraphs/mysite/historical_data/'
all_files = os.listdir(path)
li = []
for filename in all_files:
    df = pd.read_csv('/home/KenPomGraphs/mysite/historical_data/'+filename, index_col=0, header=0)
    li.append(df)
glob_data = pd.concat(li, axis=0, ignore_index=True)

glob_data.set_index(['Team', 'Date'], inplace=True)
glob_data.sort_index(inplace=True)
glob_data.sort_values(by=['Rk', 'Date'], inplace=True)

print(glob_data.index)

keys = list(color_data['Team'])
values = list(color_data['Color'])
COLOR_DICT = {keys[i]: values[i] for i in range(len(keys))}

### DASH GOES HERE ###

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = kp_data
num_cols = [column for column in kp_data.columns if column not in ['Team', 'Conf', 'W-L', 'Rk', 'Date']]

available_stats = kp_data[num_cols].columns

app.title = 'KenPomGraphs'
app.layout = html.Div([
    html.Div([
        html.H1('Ken Pom Visualizer', id='header1')
    ]),
    html.Div([
        html.H2('Bar Charts'),
        html.P(f'Data as of: {kp_data["Date"][0]}'),
        html.Div([
            dcc.Dropdown(
                id='stat-column',
                options=[{'label': i, 'value': i} for i in available_stats],
                value='AdjEM'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}
        ),
        html.P('Top:'),
        dcc.RadioItems(
            id='number-teams',
            options=[{'label': i, 'value': i} for i in [10, 25, 64]],
            value=64,
            labelStyle={'display': 'inline-block'}
        )
    ],
    style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}
    ),
    dcc.Graph(id='fig1'),
    html.Div([
        dcc.Checklist(
            id='conf',
            options=[{'label': i, "value": i} for i in list(df['Conf'].unique())],
            value=list(df['Conf'].unique()),
            labelStyle={'display': 'inline-block', 'border-radius': '10px', 'border': '2px solid #555555', 'background-color': 'white', 'width': '70px', 'height': '40px', 'text-align': 'center'}
        ),
        html.Button('Deselect All', id='deselect-all-bar', n_clicks=0),
        html.Button('Select All', id='select-all-bar', n_clicks=0)
    ],
    style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        html.H2('Scatter Plots'),
        html.P(f'Data as of: {kp_data["Date"][0]}'),
        html.Div([
            dcc.Dropdown(
                id='x-stat-column',
                options=[{'label': i, 'value': i} for i in available_stats],
                value='AdjO'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Dropdown(
                id='y-stat-column',
                options=[{'label': i, 'value': i} for i in available_stats],
                value='AdjD'
            )],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
        ),
        html.P('Top:'),
        html.Div([
            dcc.RadioItems(
                id='number-teams-scatter',
                options=[{'label': i, 'value': i} for i in [10, 25, 64, 100, 250, 357]],
                value=357,
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '100%', 'display': 'inline-block'}
        ),
        dcc.Graph(id='fig2', style={'height': 800}),
        html.Div([
            dcc.Checklist(
                id='conf-scatter',
                options=[{'label': i, "value": i} for i in list(df['Conf'].unique())],
                value=list(df['Conf'].unique()),
                labelStyle={'display': 'inline-block', 'border-radius': '10px', 'border': '2px solid #555555', 'background-color': 'white', 'width': '70px', 'height': '40px', 'text-align': 'center'}
            ),
            html.Button('Deselect All', id='deselect-all-scatter', n_clicks=0),
            html.Button('Select All', id='select-all-scatter', n_clicks=0)
        ])
    ],
    style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        html.H2('Line Graphs'),
        html.P('Data will automatically be updated when the season starts. (11/25/20)'),
        html.Div([
            dcc.Dropdown(
                id='line-stat',
                options=[{'label': i, 'value': i} for i in available_stats],
                value='AdjEM'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}
        ),
        html.P('Top:'),
        html.Div([
            dcc.RadioItems(
                id='number-teams-line',
                options=[{'label': i, 'value': i} for i in [10, 25]],
                value=10,
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '100%', 'display': 'inline-block'}
        ),
        dcc.Graph(id='fig3', style={'height': 800}),
        html.Div([
            dcc.Checklist(
                id='conf-line',
                options=[{'label': i, "value": i} for i in list(df['Conf'].unique())],
                value=list(df['Conf'].unique()),
                labelStyle={'display': 'inline-block', 'border-radius': '10px', 'border': '2px solid #555555', 'background-color': 'white', 'width': '70px', 'height': '40px', 'text-align': 'center'}
            ),
            html.Button('Deselect All', id='deselect-all-line', n_clicks=0),
            html.Button('Select All', id='select-all-line', n_clicks=0)
            ]),
        html.P(['Source:',
            html.A('kenpom.com', href='https://kenpom.com/', target='_blank')
        ],
        style={'text-align': 'left'}
        )

    ],
    style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}
    )
],
style={'margin': 'auto', 'width': '55%'}
)

### CALLBACKS HERE ###

@app.callback(
    [Output('conf', 'value')],
    [Input('deselect-all-bar', 'n_clicks'),
    Input('select-all-bar', 'n_clicks')])

def update_conferences(deselect, select):
    changed_id = str(dash.callback_context.triggered[0]['prop_id'].split('.')[0])
    conference_selections = [list(df['Conf'].unique())]
    if changed_id == 'deselect-all-bar':
        conference_selections = [[]]
    if changed_id == 'select-all-bar':
        conference_selections = [list(df['Conf'].unique())]
    return conference_selections

@app.callback(
    [Output('conf-scatter', 'value')],
    [Input('deselect-all-scatter', 'n_clicks'),
    Input('select-all-scatter', 'n_clicks')])

def update_conferences_scatter(deselect, select):
    changed_id = str(dash.callback_context.triggered[0]['prop_id'].split('.')[0])
    conference_selections = [list(df['Conf'].unique())]
    if changed_id == 'deselect-all-scatter':
        conference_selections = [[]]
    if changed_id == 'select-all-scatter':
        conference_selections = [list(df['Conf'].unique())]
    return conference_selections

@app.callback(
    [Output('conf-line', 'value')],
    [Input('deselect-all-line', 'n_clicks'),
    Input('select-all-line', 'n_clicks')])

def update_conferences_line(deselect, select):
    changed_id = str(dash.callback_context.triggered[0]['prop_id'].split('.')[0])
    conference_selections = [list(df['Conf'].unique())]
    if changed_id == 'deselect-all-line':
        conference_selections = [[]]
    if changed_id == 'select-all-line':
        conference_selections = [list(df['Conf'].unique())]
    return conference_selections

@app.callback(
    [Output('fig1', 'figure')],
    [Input('stat-column', 'value'),
    Input('number-teams', 'value'),
    Input('conf', 'value')]
)

def update_figure_1(stat_column_name, number_teams, conf):
    if stat_column_name in ['AdjD', 'OppD']:
        dff = df.loc[df['Conf'].isin(conf)].sort_values(by=stat_column_name, ascending=True).head(number_teams).reset_index().copy()
    else: dff = df.loc[df['Conf'].isin(conf)].sort_values(by=stat_column_name, ascending=False).head(number_teams).reset_index().copy()

    fig1 = px.bar(data_frame=dff,
                x='Team',
                y=stat_column_name,
                color='Conf',
                color_discrete_map=COLORS,
                category_orders={'Team': list(dff['Team'])}
                )
    fig1.update_traces(hovertemplate='%{x}: %{y}')
    fig1.update_traces(marker=dict(line=dict(
                                            width=2,
                                            color='DarkSlateGrey')))
    fig1.update_yaxes(range=[min(dff[stat_column_name]) - abs((min(dff[stat_column_name])*.2)), max(5, max(dff[stat_column_name])*1.15)])

    fig1.update_layout(transition_duration=500)
    fig1.update_yaxes(title=stat_column_name)
    fig1.update_xaxes(title='')
    return [fig1]

@app.callback(
    [Output('fig2', 'figure')],
    [Input('x-stat-column', 'value'),
    Input('y-stat-column', 'value'),
    Input('conf-scatter', 'value'),
    Input('number-teams-scatter', 'value')]
)

def update_figure_2(x_stat_column, y_stat_column, conf_scatter, number_teams_scatter):
    df_scatter = df.loc[df['Conf'].isin(conf_scatter)].head(number_teams_scatter)
    fig2 = px.scatter(data_frame=df_scatter,
                    x=x_stat_column,
                    y=y_stat_column,
                    color='Conf',
                    color_discrete_map=COLORS,
                    hover_data={'Team':True})
    fig2.update_traces(marker=dict(size=12,
                                    line=dict(width=2)),
                        selector=dict(mode='markers'))
    fig2.update_layout(transition_duration=500)
    fig2.update_xaxes(title=x_stat_column)
    fig2.update_yaxes(title=y_stat_column)
    if x_stat_column == 'AdjD' or x_stat_column == 'OppD':
        fig2['layout']['xaxis']['autorange'] = 'reversed'
    if y_stat_column == 'AdjD' or x_stat_column == 'OppD':
        fig2['layout']['yaxis']['autorange'] = 'reversed'
    return [fig2]

@app.callback(
    [Output('fig3', 'figure')],
    [Input('line-stat', 'value'),
    Input('number-teams-line', 'value'),
    Input('conf-line', 'value')]
)

def update_figure_3(line_stat, number_teams_line, conf_line):
    if conf_line == None:
        df_line = glob_data
    else: df_line = glob_data.loc[glob_data['Conf'].isin(conf_line)]
    if line_stat in ['AdjD', 'OppD']:
        dff_line = df_line.sort_values(by=['Date',line_stat], ascending=[False, True])
        dff_line = dff_line.loc[dff_line.index.get_level_values(0).unique()[:number_teams_line].tolist()]
    else:
        dff_line = df_line.sort_values(by=['Date',line_stat], ascending=[False, False])
        dff_line = dff_line.loc[dff_line.index.get_level_values(0).unique()[:number_teams_line].tolist()]
    fig3 = px.line(dff_line,
                    x=dff_line.index.get_level_values(1),
                    y=line_stat,
                    color=dff_line.index.get_level_values(0),
                    color_discrete_map=COLOR_DICT)
    fig3.update_traces(line=dict(width=5))
    fig3.update_traces(mode='markers+lines')
    fig3.update_traces(marker=dict(size=10))
    fig3.update_xaxes(title='Date')
    fig3['layout']['xaxis']['autorange'] = 'reversed'
    return [fig3]



