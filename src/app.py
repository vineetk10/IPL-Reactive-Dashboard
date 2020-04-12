import streamlit as st
import plotly.express as px
from .preprocess import matches, list_of_teams, matches_cities
import pandas as pd
from uuid import uuid4


def plot(fig):
    st.plotly_chart(fig, use_container_width=True)


def overall_best(matches):
    df = matches["winner"].value_counts().reset_index()
    fig = px.bar(df.head(), x="index", y="winner", barmode="group")
    plot(fig)


def best_team_yoy(matches, year: int):
    query = f"season == {year}"
    df = matches.query(query)["winner"].value_counts().reset_index()
    df.columns = ["Team name", "No. of Wins"]
    fig = px.bar(df, x="Team name", y="No. of Wins", barmode="group",)
    plot(fig)


def best_mvp_yoy(matches, year: int):
    query = f"season == {year}"
    mom_yoy = (
        pd.pivot_table(
            matches.query(query),
            values=["date"],
            index=["player_of_match"],
            aggfunc="count",
        )
        .sort_values(["date"], ascending=[False])
        .reset_index()
    )  # PoM yoy basis
    fig = px.bar(mom_yoy, x="player_of_match", y="date", barmode="group",)
    plot(fig)


def city_map(matches_cities, year: str = "2019"):
    fig = px.scatter_mapbox(
        matches_cities,
        lat="lat",
        lon="lng",
        size=year,
        color=year,
        hover_data=["City"],
        color_discrete_sequence=["fuchsia"],
        zoom=2,
        height=600,
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    plot(fig)


def main():

    st.header("1. Which team has the best overall performance?")
    overall_best(matches)
    year_best_team = st.slider(
        label="Select Year",
        min_value=int(matches["season"].min()),
        max_value=int(matches["season"].max()),
    )
    st.header(f"2. Which is the Best performing Team in {year_best_team}?")
    best_team_yoy(matches, year_best_team)
    year_mvp = st.slider(
        label="Select Year for Best Team",
        min_value=int(matches["season"].min()),
        max_value=int(matches["season"].max()),
    )
    st.header(f"3. Best player or MVP in {year_mvp}?")
    best_mvp_yoy(matches, year_mvp)
    st.header(f"4. City with most number of IPL matches in 2019")
    city_map(matches_cities, year="2019")
