import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

# Based off grid from http://awesome-streamlit.org --> Gallery --> "Layout and Style Experiments"
def make_grid():
    grid = make_subplots(
        rows = 9,
        cols = 12,
        subplot_titles = (""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  ,
                          ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , "ME",
                          "WA", "MT", "ND", "MN", "WI", "MI", ""  , ""  , "NY", "VT", "NH", "MA",
                          "OR", "ID", "WY", "SD", "IA", "IL", "IN", "OH", "PA", "NJ", "CT", "RI",
                          "NV", "UT", "CO", "NE", "KS", "MO", "TN", "KY", "WV", "VA", "MD", "DE",
                          ""  , "CA", "AZ", "NM", "OK", "AR", "MS", "AL", "GA", "SC", "NC", ""  ,
                          ""  , ""  , ""  , ""  , "TX", "LA", ""  , ""  , "FL", ""  , ""  , ""  ,
                          ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  ,
                          ""  , "AK", ""  , "HI", ""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  ,),
        specs = [
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
            [ {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"} ],
        ],
    )

    grid.update_layout(
        width = 1200,
        height = 1133,
        #template = "plotly",
        paper_bgcolor = '#000000',
        font=dict(family = 'Helvetica Neue', size = 18, color = '#ffffff'),
    )

    #grid.add_trace(px.bar(
    
    return grid



st.title("COVID-19 Death Rates in Prisons")

# Formatting trick: https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/24, https://discuss.streamlit.io/t/creating-a-nicely-formatted-search-field/1804/2
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.plotly_chart(make_grid())
