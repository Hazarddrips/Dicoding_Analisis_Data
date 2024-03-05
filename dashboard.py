import streamlit as st
import pandas as pd
import plotly.express as plotex


@st.cache_resource
def load_data():
    dfDay = pd.read_csv("day.csv")
    return dfDay


dfDay = load_data()

st.title("Bike Share Dashboard")

st.sidebar.title("About Me")
st.sidebar.markdown("**Nama         : Haidar Zakki**")
st.sidebar.markdown("**Dicoding Id  : hazarddrips**")
st.sidebar.markdown("**Email        : m258d4ky1421@bangkit.academy**")

st.sidebar.title("Dataset Bike Share")

if st.sidebar.checkbox("Display Dataset"):
    st.subheader("Raw Data")
    st.write(dfDay)

if st.sidebar.checkbox("Display Descriptive Statistics"):
    st.subheader("Descriptive Statistics")
    st.write(dfDay.describe())

if st.sidebar.checkbox("Display Weather Parameter"):
    st.subheader("Parameter")
    st.markdown(
        "Weathersit : \n - 1: Clear, Few clouds, Partly cloudy, Partly cloudy \n - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist \n- 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds \n- 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog"
    )

if st.sidebar.checkbox("Display Season Parameter"):
    st.subheader("Parameter")
    st.markdown("Season : \n - 1: spring \n - 2: summer  \n - 3: fall \n - 4: winter")


season_mapping = {1: "spring", 2: "summer", 3: "fall", 4: "winter"}
dfDay["season_label"] = dfDay["season"].map(season_mapping)

seasonC = dfDay.groupby("season_label")["cnt"].sum().reset_index()
seasonC_figure = plotex.bar(
    seasonC, x="season_label", y="cnt", title="Season Bike Share Count"
)
seasonC_figure.update_traces(marker_color=['#FF5733', '#33FF57', '#3366FF', '#FF33CC'])
st.plotly_chart(seasonC_figure, use_container_width=True, height=400, width=600)

weatherC = dfDay.groupby("weathersit")["cnt"].sum().reset_index()
weatherC_figure = plotex.bar(
    weatherC, x="weathersit", y="cnt", title="Weather Situation Bike Share Count"
)
weatherC_figure.update_traces(marker_color=['#FF5733', '#33FF57', '#3366FF'])
st.plotly_chart(weatherC_figure, use_container_width=True, height=400, width=800)

filtered_data = dfDay[(dfDay["workingday"] == 0) & (dfDay["registered"] > 0)]
fig = plotex.bar(filtered_data, x="weekday", y="registered", title="Jumlah Sewa Sepeda Registered Pada Weekday Namun Hari Libur")
fig.update_xaxes(title="Hari Kerja namun pada hari libur")
fig.update_yaxes(title="Jumlah Sewa Sepeda Registered")
st.plotly_chart(fig)