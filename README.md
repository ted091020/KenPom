# KenPom
A visualization tool for KenPom data

[KenPomGraphs.com](https://KenPomGraphs.pythonanywhere.com)

## flask_app.py
This file imports the data and creates the visualizations with plotly. The layout of the website is created using dash.

## kp_scrape.py
This file is executed once per day. It scrapes KenPom.com and Sports-Reference.com and saves the data as a csv file to PythonAnywhere.
