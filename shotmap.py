import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
import pandas as pd
import json

# styles
# column-styles
st.markdown('<style>[data-testid="stMain"]{ background-color: #05112c; color: white;}</style>', unsafe_allow_html=True)
st.markdown('<style>[data-testid="stWidgetLabel"]>[data-testid="stMarkdownContainer"]{ color: white;}</style>', unsafe_allow_html=True)

# page config.
st.set_page_config(page_title="SoccerLysis",
                   initial_sidebar_state="auto",
                   page_icon="⚽",
                   layout="centered")

st.title("Euro 2024 Shot Map")
st.subheader("Filter to any team/player to analyzes all of their shots")

# loading data
df = pd.read_csv(r"c:\Users\USER\Documents\CODES\Python Work to Do\euros_2024_shot_map.csv")
df = df[df["type"] == "Shot"].reset_index(drop=True)
df["location"] = df["location"].apply(json.loads)

# select box
team = st.selectbox("Select a team", df["team"].sort_values().unique(), index=None)
player = st.selectbox("Select a player", df[df["team"] == team]["player"].sort_values().unique(), index=None)


# filter function
def filter_data(df, team, player):
    if team:
        df = df[df["team"] == team]
    if player:
        df = df[df["player"] == player]

    return df


# calling filter function
filtered_df = filter_data(df, team, player)

# pitch plot
pitch = VerticalPitch(pitch_type="statsbomb", half=True, pitch_color="green",
                      line_color="white", stripe=True, stripe_color="#80f380")
fig, ax = pitch.draw(figsize=[10, 10])


# plot style functions
def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient="records"):
        pitch.scatter(
            x=float(x["location"][0]),
            y=float(x["location"][1]),
            ax=ax,
            s=1000 * x["shot_statsbomb_xg"],
            color="gold" if x["shot_outcome"] == "Goal" else "red",
            edgecolor="black",
            alpha=2 if x["type"] == "goal" else 1,
            zorder=2 if x["type"] == "goal" else 1
        )


plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)
