import streamlit
from gsheetsdb import connect
import pandas as pd
import plotly_express

#To place dashboard over entire screen-width
streamlit.set_page_config(layout="wide")

#Accessing data from google sheet database
gsheet_url = streamlit.secrets["GSHEET_URL"]
connect_instance = connect()
data = connect_instance.execute(f'SELECT * FROM "{gsheet_url}"')
data = pd.DataFrame(data)

#Adding separator b/w logo and visualization
streamlit.write('')

#Providing description to side-bar
streamlit.sidebar.markdown('# Controls')

#Select-box to choose session-start entity
entity = streamlit.sidebar.radio('Please choose one entity', 
                                 ('Graphic Design-D', 'Web Design-D', 
                                  'Marketing-D', 'Typography-D', 
                                  'Business-D', 'Brand-I'))

#Including a foot-note in side bar
streamlit.sidebar.write('##### *Note: Visualization is based on data for sessions starting with selected entity*')

#Visualization for selection 
figure = plotly_express.sunburst(data_frame = data[data['session_start'] == entity], 
                                 path = ['session_start', 'change_type', 'search_depth', 'entity'],
                                 values = 'percent_total',
                                 color = 'change_type',
                                 color_discrete_sequence = plotly_express.colors.qualitative.Safe,
                                 maxdepth = -1,
                                 template = 'ggplot2',
                                 title = f'Entity Addition/Deletion for Sessions beginning w/ {entity}')
figure.update_traces(textinfo = 'label')
figure.update_layout(autosize = False, width = 800, height = 550, margin = dict(l = 25, r = 25, b = 25, t = 25))
streamlit.plotly_chart(figure, use_container_width = True)

#How to improve resolution of diagram?
#How to host the dashboard by uploading script to git?