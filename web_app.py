import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# How to handle data from federal prisons and D.C.? Federal prisons: not exactly state-based, but it would be misleading
# to use "nationwide" COVID data? D.C.: Marshall data doesn't include, but JHU data does.

# Need to convert all values to "per capita" for prison data (currently just numerical), consider making separate (own) CSV,
# also maybe match "name" (state) column name to "Province_State", change column labels (currently misleading -- e.g.
# "Mortality_Rate" is referring to JHU data, but could be confused with Marshall-derived data

# Visuals: shift grid map to the left, bold state abbreviations, add column of zeroes to combined data to create gap between two bars
# add titles to grid map and bar chart

# Would be cool if could transform grid map => bar chart with a button, and animate the transformation; also, sort bar chart; also,
# bar chart hover-over pop-ups are weird


COVID_PRISON_DATA_URL = ('https://raw.githubusercontent.com/themarshallproject/COVID_prison_data/master/data/covid_prison_cases.csv')
covid_prison_data = pd.read_csv(COVID_PRISON_DATA_URL, nrows = 50,
                    names = ["name", "abbreviation", "staff_tests", "staff_tests_with_multiples", "prisoner_tests", "prisoner_tests_with_multiples",
                            "total_staff_cases", "total_prisoner_cases", "staff_recovered", "prisoners_recovered", "total_staff_deaths","total_prisoner_deaths",
                            "as_of_date", "notes"],
                    usecols = ["name", "total_prisoner_deaths", "as_of_date"],
                    skiprows = [0, 51],
                    )


COVID_DATA_URL = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/07-07-2020.csv')
covid_data = pd.read_csv(COVID_DATA_URL,
                    names = ["Province_State", "Country_Region", "Last_Update", "Lat", "Long_", "Confirmed", "Deaths", "Recovered", "Active", "FIPS",
                            "Incident_Rate", "People_Tested", "People_Hospitalized", "Mortality_Rate", "UID", "ISO3", "Testing_Rate", "Hospitalization_Rate"],
                    usecols = ["Province_State", "Last_Update", "Mortality_Rate"],
                    skiprows = [0, 3, 10, 11, 14, 15, 40, 45, 53],
                    )


combined_data = pd.concat([covid_prison_data, covid_data], axis = 1)
combined_data = combined_data.drop(columns = "as_of_date")
combined_data = combined_data.drop(columns = "Province_State")
combined_data = combined_data.drop(columns = "Last_Update")


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
                          ""  , "AK", ""  , "HI", ""  , ""  , ""  , ""  , ""  , ""  , "FED", "" ,),
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
        plot_bgcolor = '#ffffff',
        font = dict(family = 'IBM Plex Sans', size = 18, color = '#000000'),
    )

    #grid.add_trace(px.bar(
    
    return grid


st.title("COVID-19 in US Prisons")
# CSS trick: https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/24, https://discuss.streamlit.io/t/creating-a-nicely-formatted-search-field/1804/2
#with open("style.css") as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


# Show grid map with Plotly
st.markdown('<h3>Grid Map</h3>', unsafe_allow_html = True)
st.plotly_chart(make_grid())


# Show bar chart with Plotly
st.markdown('<h3>Bar Chart</h3>', unsafe_allow_html = True)
bar_chart = go.Figure()
bar_chart.add_trace(go.Bar(
    x = combined_data['total_prisoner_deaths'],
    y = combined_data['name'],
    orientation = 'h',
    name = 'total_prisoner_deaths => "In prisons"',
    marker_color = '#f13b3b',
))
bar_chart.add_trace(go.Bar(
    x = combined_data['Mortality_Rate'],
    y = combined_data['name'],
    orientation = 'h',
    name = 'Mortality_Rate => "Statewide"',
    marker_color = '#000000',
))
bar_chart.update_layout(
    xaxis_title = 'COVID-19 Mortality Rate (deaths per 100,000 persons)',
    yaxis_title = 'State',
    width = 1000,
    height = 1100,
    barmode = 'group',
    plot_bgcolor = '#ffffff',
    font = dict(family = 'IBM Plex Sans', size = 14, color = '#000000'),
)
bar_chart.update_yaxes(autorange = 'reversed')
st.write(bar_chart)


# Show raw data with Streamlit
st.markdown('<h3>Raw Data</h3>', unsafe_allow_html = True)
st.markdown('<h4>COVID-19 in US Prisons by State</h4>', unsafe_allow_html = True)
st.write(covid_prison_data)
st.markdown("[Data](https://github.com/themarshallproject/COVID_prison_data) from The Marshall Project, a nonprofit investigative newsroom dedicated to the U.S. criminal justice system.")
st.markdown('<h4>COVID-19 in US States</h4>', unsafe_allow_html = True)
st.write(covid_data)
st.markdown("[Data](https://github.com/CSSEGISandData/COVID-19) from the COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.")
st.markdown('<h4>Side-by-Side</h4>', unsafe_allow_html = True)
st.write(combined_data)


