import dash
import pandas as pd
import datetime
from dash import dcc
from dash import html
from plotly import graph_objs as go
import plotly.express as px

# ------------------------------------------------------------------------------
# Init
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Grabbing the data
# ------------------------------------------------------------------------------
dat = '../gmaps/gmaps/data.csv'
df = pd.read_csv(dat)
# ==============================================================================
# Manipulate the data
# ==============================================================================
# ------------------------------------------------------------------------------
# Change the time to minutes
# ------------------------------------------------------------------------------

df['return'] = df['return']/60.0
df['go'] = df['go']/60.0
# ------------------------------------------------------------------------------
# Change the time to PST
# ------------------------------------------------------------------------------
time = df['timestamp'].to_list()
finaltime = []
for i in time:
    thistime = datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%f')
    thistime = thistime - datetime.timedelta(hours=8)
    finaltime.append(thistime.strftime('%H:%M'))
df['time'] = finaltime
# ==============================================================================
# Sort and group the times
# ==============================================================================
# ------------------------------------------------------------------------------
# Means/stdv
# ------------------------------------------------------------------------------
df.sort_values('time',inplace=True)
meandf = df.groupby('time').mean()
stdvdf = df.groupby('time').std()
highdf = meandf + 2*stdvdf
lowdf = meandf - 2*stdvdf
# ------------------------------------------------------------------------------
# Q1/Q3 with mean graph
# ------------------------------------------------------------------------------
qrtrdf = df.groupby('time').quantile([0.25,0.75]).unstack()
qrtrdf.columns = ['go_q1','go_q3','return_q1','return_q3']
minmaxdf = df[['time','go','return']].groupby('time').agg(['min','max'])
minmaxdf.columns = ['go_min','go_max','return_min','return_max']
finaldf2 = pd.concat([meandf,qrtrdf,minmaxdf],axis=1)
returndf2 = finaldf2[['return','return_q1','return_q3','return_min','return_max']].copy()
goingdf2 = finaldf2[['go','go_q1','go_q3','go_min','go_max']].copy()
returndf2['time'] = returndf2.index.to_list()
goingdf2['time'] = goingdf2.index.to_list()
# ------------------------------------------------------------------------------
# Set up the final dataframe
# ------------------------------------------------------------------------------
finaldf = pd.concat([meandf,highdf,lowdf],axis=1)
finaldf.columns = ['go','return','go_high','return_high','go_low','return_low']
returndf = finaldf[['return','return_high','return_low']].copy()
returndf['time'] = returndf.index.to_list()
goingdf = finaldf[['go','go_high','go_low']].copy()
goingdf['time'] = goingdf.index.to_list()
# ==============================================================================
# Create the plot
# ==============================================================================
# ------------------------------------------------------------------------------
# Return graphs
# ------------------------------------------------------------------------------
returnfig = go.Figure()
returnfig.add_trace(go.Scatter(x=returndf['time'],y=returndf['return_high'],name='high',line_shape='spline'))
returnfig.add_trace(go.Scatter(x=returndf['time'],y=returndf['return'],name='mean',line_shape='spline'))
returnfig.add_trace(go.Scatter(x=returndf['time'],y=returndf['return_low'],name='low',line_shape='spline'))
returnfig.update_layout(xaxis_title='Time of Day',yaxis_title='Time (min)')
# ------------------------------------------------------------------------------
# Going graphs
# ------------------------------------------------------------------------------
goingfig = go.Figure()
goingfig.add_trace(go.Scatter(x=goingdf['time'],y=goingdf['go_high'],name='high',line_shape='spline'))
goingfig.add_trace(go.Scatter(x=goingdf['time'],y=goingdf['go'],name='mean',line_shape='spline'))
goingfig.add_trace(go.Scatter(x=goingdf['time'],y=goingdf['go_low'],name='low',line_shape='spline'))
goingfig.update_layout(xaxis_title='Time of Day',yaxis_title='Time (min)')
# ==============================================================================
# Create the plots for min/max/mean/q1/q3
# ==============================================================================
# ------------------------------------------------------------------------------
# Return graphs
# ------------------------------------------------------------------------------
returnfig2 = go.Figure()
returnfig2.add_trace(go.Scatter(x=returndf2['time'],y=returndf2['return_q3'],name='q3',line_shape='spline'))
returnfig2.add_trace(go.Scatter(x=returndf2['time'],y=returndf2['return'],name='mean',line_shape='spline'))
returnfig2.add_trace(go.Scatter(x=returndf2['time'],y=returndf2['return_q1'],name='q1',line_shape='spline'))
# returnfig2.add_trace(go.Scatter(x=returndf2['time'],y=returndf2['return_min'],name='min'))
# returnfig2.add_trace(go.Scatter(x=returndf2['time'],y=returndf2['return_max'],name='max'))
returnfig2.update_layout(xaxis_title='Time of Day',yaxis_title='Time (min)')
# ------------------------------------------------------------------------------
# Going graphs
# ------------------------------------------------------------------------------
goingfig2 = go.Figure()
goingfig2.add_trace(go.Scatter(x=goingdf2['time'],y=goingdf2['go_q3'],name='q3',line_shape='spline'))
goingfig2.add_trace(go.Scatter(x=goingdf2['time'],y=goingdf2['go'],name='mean',line_shape='spline'))
goingfig2.add_trace(go.Scatter(x=goingdf2['time'],y=goingdf2['go_q1'],name='q1',line_shape='spline'))
# goingfig2.add_trace(go.Scatter(x=goingdf2['time'],y=goingdf2['go_min'],name='min'))
# goingfig2.add_trace(go.Scatter(x=goingdf2['time'],y=goingdf2['go_max'],name='max'))
goingfig2.update_layout(xaxis_title='Time of Day',yaxis_title='Time (min)')

# ==============================================================================
# Building the page
# ==============================================================================
# ------------------------------------------------------------------------------
# Return graphs
# ------------------------------------------------------------------------------
layout = []
layout.append(html.H1(children='Return'))
layout.append(html.H2(children='Mean and variance graph'))
layout.append(dcc.Graph(figure=returnfig))
layout.append(html.H2(children='Mean and Q1/Q3 graph'))
layout.append(dcc.Graph(figure=returnfig2))
layout.append(html.H1(children='Going'))
layout.append(html.H2(children='Mean and variance graph'))
layout.append(dcc.Graph(figure=goingfig))
layout.append(html.H2(children='Mean and Q1/Q3 graph'))
layout.append(dcc.Graph(figure=goingfig2))
# ------------------------------------------------------------------------------
# Going graphs
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Initialize the page in the app
# ------------------------------------------------------------------------------
es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=es)


app.layout = html.Div(children=layout)
server = app.server
# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)