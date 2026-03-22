import plotly.express as px
import streamlit as st
import pandas as pd

COLORS = ["#ef5350", "#42a5f5"]


def render_stat_chart(melted_df: pd.DataFrame):
    fig = px.bar(
        melted_df,
        x="stat",
        y="value",
        color="pokemon",
        barmode="group",
        title="Base Stats Comparison",
        labels={"stat": "Stat", "value": "Value", "pokemon": "Pokémon"},
        color_discrete_sequence=COLORS,
    )
    fig.update_layout(xaxis_tickangle=-30, legend_title_text="Pokémon")
    st.plotly_chart(fig, use_container_width=True)


def render_hp_chart(hp_df: pd.DataFrame):
    fig = px.line(
        hp_df,
        x="round",
        y="hp",
        color="pokemon",
        title="HP Remaining Each Round",
        labels={"round": "Round", "hp": "HP", "pokemon": "Pokémon"},
        markers=True,
        color_discrete_sequence=COLORS,
    )
    fig.update_layout(legend_title_text="Pokémon")
    st.plotly_chart(fig, use_container_width=True)