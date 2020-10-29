import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df_house= pd.read_csv(os.path.join('resources','house_vis_minorities.csv'))
df_senate= pd.read_csv(os.path.join('resources','senate_vis_minorities.csv'))

# Canadian population demographics from 2016 census (relies on self reporting)
total_population= 34460065
total_visible_minority= 7674580
south_asian= 1924635
chinese= 1577060
black= 1198540
other= total_visible_minority - south_asian - chinese - black
non_visible_minority= total_population - total_visible_minority

# These python lists will be used as input to our pie charts after
cdn_labels= ['Not Visible Minority','South Asian', 'Chinese', 'Black', 'Other']
cdn_values= [non_visible_minority, south_asian, chinese, black, other]

size_house= 338
size_senate= 105

house_vals= df_house['Notes'].value_counts()
house_labels= house_vals.index.tolist()
house_values= house_vals.values.tolist()
house_labels= ['Not Visible Minority'] + house_labels
house_values=  [size_house - sum(house_values)] + house_values


senate_vals= df_senate['Notes'].value_counts()
senate_labels= senate_vals.index.tolist()
senate_values= senate_vals.values.tolist()
senate_labels= ["Not Visible Minority"] + senate_labels
senate_values= [size_senate - sum(senate_values)] + senate_values

fig = make_subplots(rows=1, cols=3, 
		subplot_titles= ('Canadian Demographics', 'House of Commons Demographics', 'Senate Demographics'),
		specs=[[{"type":"pie"},{"type":"pie"},{"type":"pie"}]])

fig.add_trace(go.Pie(labels=cdn_labels, values=cdn_values), row=1, col=1)
fig.add_trace(go.Pie(labels=house_labels, values=house_values), row=1, col=2)
fig.add_trace(go.Pie(labels=senate_labels, values=senate_values), row=1, col=3)
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
fig.update_traces(textposition='inside')
fig.update_layout(showlegend=False)

app.layout = html.Div(children=[
	html.H3(children='''
			Comparing the makeup of the Canadian Parliament to the makeup of Canada
	'''),
	dcc.Graph(
		id='pie-chart-politics',
		figure=fig
	)
])

if __name__ == '__main__':
	app.run_server()
