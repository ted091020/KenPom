import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import plotly.express as px
import pandas as pd
import os
from scipy import stats
import numpy as np
from datetime import datetime, timedelta



### REGULAR CODE HERE ###
color_data = pd.read_csv('/home/KenPomGraphs/mysite/static_data/team_color_legend.csv', index_col=0)
kp_data = pd.read_csv('/home/KenPomGraphs/mysite/static_data/current_data.csv', index_col=0)
kp_data.rename(columns={'School': 'Team', 'Tm.': 'Points For', 'Opp.': 'Points Against', 'W.1': 'Conf Wins', 'L.1': 'Conf Losses', 'W.2': 'Home Wins', 'L.2': 'Home Losses', 'W.3': 'Away Wins', 'L.3': 'Away Losses', 'MP': 'Minutes Played'}, inplace=True)

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
glob_data.rename(columns={'School': 'Team', 'Tm.': 'Points For', 'Opp.': 'Points Against', 'W.1': 'Conf Wins', 'L.1': 'Conf Losses', 'W.2': 'Home Wins', 'L.2': 'Home Losses', 'W.3': 'Away Wins', 'L.3': 'Away Losses', 'MP': 'Minutes Played'}, inplace=True)


keys = list(color_data['Team'])
values = list(color_data['Color'])
COLOR_DICT = {keys[i]: values[i] for i in range(len(keys))}

low_is_good = ['AdjD', 'OppD', 'TOV', 'PF', 'L', 'Conf Losses', 'Home Losses', 'Away Losses', 'Points Against']

### DASH GOES HERE ###

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=False)

df = kp_data
num_cols = [column for column in kp_data.columns if column not in ['Team', 'Conf', 'W-L', 'Rk', 'Date']]
line_cols = [column for column in glob_data.columns if column not in ['Team', 'Conf', 'W-L', 'Rk', 'Date']]

available_stats = kp_data[num_cols].columns
available_stats_line = glob_data[line_cols].columns

app.title = 'KenPomGraphs'
app.layout = html.Div([
    html.Div([
        html.H1('Ken Pom Visualizer', id='header1')
    ]),
    html.P(['Source:',
            html.A('kenpom.com', href='https://kenpom.com/', target='_blank')
        ],
        style={'text-align': 'left'}
        ),
    html.P(['Source:',
            html.A('sports-reference.com', href='https://www.sports-reference.com/cbb/seasons/2021-school-stats.html', target='_blank'),
            ' (per-game averages)'
        ],
        style={'text-align': 'left'}
        ),

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
        ),
        html.P('Color by:'),
        dcc.RadioItems(
            id='color-by',
            options=[{'label': 'Team', 'value': 'Team'},
                     {'label': 'Conference', 'value': 'Conference'}],
            value='Conference',
            labelStyle={'display': 'inline-block'}
        )
    ],
    style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}
    ),
    dcc.Graph(id='fig1'),
    html.Div([html.Button("Download csv", id="btn"), Download(id="download")], style={'width':'8%'}),
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
            ),
        html.P('Color by:'),
        dcc.RadioItems(
            id='color-by-scatter',
            options=[{'label': 'Team', 'value': 'Team'},
                     {'label': 'Conference', 'value': 'Conference'}],
            value='Conference',
            labelStyle={'display': 'inline-block'}
        )
        ],
        style={'width': '100%', 'display': 'inline-block'}
        ),
        dcc.Graph(id='fig2', style={'height': 800}),
        html.Div([html.Button("Download csv", id="btn-scatter"), Download(id="download-scatter")], style={'width':'8%'}),
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
        html.P(f'Data as of: {kp_data["Date"][0]}'),
        html.Div([
            dcc.Dropdown(
                id='line-stat',
                options=[{'label': i, 'value': i} for i in available_stats_line],
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
        html.Div([html.Button("Download csv", id="btn-line"), Download(id="download-line")], style={'width':'8%'}),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=min(glob_data.index.get_level_values(1)),
            start_date=min(glob_data.index.get_level_values(1)),
            end_date=max(glob_data.index.get_level_values(1))
            ),
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
        ),
        html.P(['Source:',
            html.A('sports-reference.com', href='https://www.sports-reference.com/cbb/seasons/2021-school-stats.html', target='_blank')
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
    Input('conf', 'value'),
    Input('color-by', 'value')]
)

def update_figure_1(stat_column_name, number_teams, conf, color_by):
    global dff
    if stat_column_name in ['AdjD', 'OppD']:
        dff = df.loc[df['Conf'].isin(conf)].sort_values(by=stat_column_name, ascending=True).head(number_teams).reset_index().copy()
    else: dff = df.loc[df['Conf'].isin(conf)].sort_values(by=stat_column_name, ascending=False).head(number_teams).reset_index().copy()

    if color_by == 'Team':
        fig1 = px.bar(data_frame=dff,
                    x='Team',
                    y=stat_column_name,
                    color='Team',
                    color_discrete_map=COLOR_DICT,
                    category_orders={'Team': list(dff['Team'])}
                    )
    else:
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
    if stat_column_name in ['W-L%', 'FG%', '3P%', 'FT%']:
        fig1.update_yaxes(range=[0,1])
    if stat_column_name in ['Points For', 'Points Against', 'Conf Wins', 'Conf Losses', 'Home Wins', 'Home Losses', 'Away Wins', 'Away Losses', 'G', 'W', 'L']:
        fig1.update_yaxes(range=[0,max(dff[stat_column_name])*1.15])
    fig1.update_layout(transition_duration=500)
    fig1.update_yaxes(title=stat_column_name)
    fig1.update_xaxes(title='')
    return [fig1]

@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])

def generate_csv(n_clicks):
    try:
        if n_clicks > 0:
            return send_data_frame(dff.to_csv, filename="bar_data.csv")
    except:
        pass

@app.callback(
    [Output('fig2', 'figure')],
    [Input('x-stat-column', 'value'),
    Input('y-stat-column', 'value'),
    Input('conf-scatter', 'value'),
    Input('number-teams-scatter', 'value'),
    Input('color-by-scatter', 'value')]
)

def update_figure_2(x_stat_column, y_stat_column, conf_scatter, number_teams_scatter, color_by):
    global df_scatter
    df_scatter = df.loc[df['Conf'].isin(conf_scatter)]
    if x_stat_column in low_is_good:
        x_zscore = [-x for x in stats.zscore(df_scatter[x_stat_column], nan_policy='omit')]
    else:
        x_zscore = [x for x in stats.zscore(df_scatter[x_stat_column], nan_policy='omit')]
    if y_stat_column in low_is_good:
        y_zscore = [-x for x in stats.zscore(df_scatter[y_stat_column], nan_policy='omit')]
    else:
        y_zscore = [x for x in stats.zscore(df_scatter[y_stat_column], nan_policy='omit')]
    df_scatter['z_ranker'] = np.add(x_zscore, y_zscore)
    df_scatter = df_scatter.sort_values(by='z_ranker', ascending=False).head(number_teams_scatter)
    if color_by == 'Conference':
        fig2 = px.scatter(data_frame=df_scatter,
                        x=x_stat_column,
                        y=y_stat_column,
                        color='Conf',
                        color_discrete_map=COLORS,
                        hover_data={'Team':True})
    else:
        fig2 = px.scatter(data_frame=df_scatter,
                        x=x_stat_column,
                        y=y_stat_column,
                        color='Team',
                        color_discrete_map=COLOR_DICT,
                        hover_data={'Team':True})
    fig2.update_traces(marker=dict(size=12,
                                    line=dict(width=2)),
                        selector=dict(mode='markers'))
    fig2.update_layout(transition_duration=500)
    fig2.update_xaxes(title=x_stat_column)
    fig2.update_yaxes(title=y_stat_column)
    if x_stat_column in low_is_good:
        fig2['layout']['xaxis']['autorange'] = 'reversed'
    if y_stat_column in low_is_good:
        fig2['layout']['yaxis']['autorange'] = 'reversed'
    return [fig2]

@app.callback(Output("download-scatter", "data"), [Input("btn-scatter", "n_clicks")])

def generate_scatter_csv(n_clicks):
    try:
        if n_clicks > 0:
            return send_data_frame(df_scatter.to_csv, filename="scatter_data.csv")
    except:
        pass

@app.callback(
    [Output('fig3', 'figure')],
    [Input('line-stat', 'value'),
    Input('number-teams-line', 'value'),
    Input('conf-line', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')]
)

def update_figure_3(line_stat, number_teams_line, conf_line, start_date, end_date):
    try:
        start_date = datetime.strftime(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=1), '%Y-%m-%d')
    except:
        pass
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%m/%d/%Y')
    except:
        pass
    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%m/%d/%Y')
    except:
        pass
    if conf_line == None:
        df_line = glob_data
    else: df_line = glob_data.loc[glob_data['Conf'].isin(conf_line)]
    idx = pd.IndexSlice
    df_line.sort_index(axis=0, inplace=True)
    df_line = df_line.loc[idx[:, start_date:end_date], :]
    global dff_line
    if line_stat in low_is_good:
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

@app.callback(Output("download-line", "data"), [Input("btn-line", "n_clicks")])

def generate_line_csv(n_clicks):
    try:
        if n_clicks > 0:
            return send_data_frame(dff_line.to_csv, filename="line_data.csv")
    except:
        pass