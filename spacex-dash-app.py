# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                 dcc.Dropdown(id='site-dropdown',  options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'site1', 'value': 'CCAFS LC-40'}, {'label': 'site2', 'value': 'CCAFS SLC-40'},{'label': 'site3', 'value': 'KSC LC-39A'},{'label': 'site4', 'value': 'VAFB SLC-4E'}],
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100'},
                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),  # Output is the figure for the pie chart
    [Input('site-dropdown', 'value')]      # Input is the selected dropdown value
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Aggregate data for all sites
        total_success = spacex_df[spacex_df['class'] == 1].shape[0]
        total_failure = spacex_df[spacex_df['class'] == 0].shape[0]
        
        # Create pie chart
        fig = px.pie(
            names=['Success', 'Failure'],
            values=[total_success, total_failure],
            title="Total Success and Failure Counts for All Sites"
        )
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_count = filtered_df['class'].sum()
        failure_count = len(filtered_df) - success_count
        
        # Create pie chart
        fig = px.pie(
            names=['Success', 'Failure'],
            values=[success_count, failure_count],
            title=f"Success vs Failure for {selected_site}"
        )
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
    # Filter data based on payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    if selected_site == 'ALL':
        # Scatter plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Sites',
            labels={'class': 'Launch Outcome'}
        )
    else:
        # Filter data for selected site
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        
        # Scatter plot for selected site
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for {selected_site}',
            labels={'class': 'Launch Outcome'}
        )
    
    return fig



# Run the app
if __name__ == '__main__':
    app.run()
