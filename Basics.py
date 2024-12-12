
# Import library

import pandas as pd
from scipy.stats import trim_mean
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from numpy.ma.extras import average
from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


# Path to the CSV file
file_path = "C:/Users/smial/Desktop/state.csv"

# Load data from the CSV file
state = pd.read_csv(file_path)

## Display  data
#print(state)

## Display the structure and data types of the columns
# print(state.info())

## Basic Statistical Calculations

# 1. Calculate the mean (average) of the 'Population' column
mean1 = state['Population'].mean()

# 2. Calculate the trimmed mean (excluding the lowest and highest 10% of values)
trim_mean1 = trim_mean(state['Population'], 0.1)

# 3. Calculate the median of the 'Population' column
median1 = state['Population'].median()

# 4. Calculate the weighted average of the 'Murder.Rate' column, weighted by the 'Population' column
ave = np.average(state['Murder.Rate'], weights=state['Population'])

# 5. Calculate the standard deviation of the 'Population' column (used for measuring spread)
std_dev = state['Population'].std()

# 6. Calculate the interquartile range (Q3 - Q1) for the 'Population' column
Q1 = state['Population'].quantile(0.75) - state['Population'].quantile(0.25)

# 7. Calculate key quantiles for the 'Murder.Rate' column
Quantile = state['Murder.Rate'].quantile([0.05, 0.25, 0.5, 0.75, 0.95])

## Visualizations

# 8. Create a boxplot for the 'Population' column using Plotly Express
boxplot_fig = px.box(state, y='Population', title='Population Boxplot')

# 9. Create a histogram and density plot for the 'Murder.Rate' column
x = state['Murder.Rate']  # Extract data for 'Murder.Rate'

# Generate histogram and density plot with Plotly's Figure Factory
fig = ff.create_distplot(
    [x],  # List of data to plot
    group_labels=['Murder Rate'],  # Label for the dataset
    bin_size=1,  # Size of bins for the histogram
    show_rug=False  # Do not show rug plot (small ticks for data points)
)

# Update layout for better presentation
fig.update_layout(
    title="Histogram and Density Plot for Murder Rate",
    xaxis_title="Murder Rate (per 100,000 people)",
    yaxis_title="Density"
)
# Create an interactive bar chart
bar_chart = px.bar(state,
             x='State',
             y='Murder.Rate',
             title="Murder Rate by State",
             labels={'Murder.Rate': 'Murder Rate (per 100,000 people)', 'State': 'State'},
             color='Murder.Rate')  # Color based on murder rate

###  Creating a Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Statystyki"),
    html.Div([
        html.H3("Podstawowe statystyki populacji:"),
        html.P(f"Średnia: {mean1:.2f}"),
        html.P(f"Mediana: {median1:.2f}"),
        html.P(f"Trimowana średnia: {trim_mean1:.2f}"),
        html.P(f"Kwantyle wskaźnika Murder Rate: {Quantile.to_dict()}"),
    ]),
    dcc.Graph(figure=boxplot_fig),
    dcc.Graph(figure=fig),
    dcc.Graph(figure =bar_chart),

])

if __name__ == '__main__':
    app.run_server(debug=True)



