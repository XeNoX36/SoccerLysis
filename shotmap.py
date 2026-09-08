import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
import pandas as pd
import json
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SoccerLysis | UEFA Euro 2024 Shot Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# COLORS
# ============================================================

BG = "#080817"
CARD = "#160D20"
CARD_LIGHT = "#24112F"
GOLD = "#F4C95D"
GOLD_LIGHT = "#FFE7A3"
WHITE = "#FFFFFF"
TEXT = "#E8E2EE"
MUTED = "#B9A9C7"
PURPLE = "#49345C"
RED = "#D94A70"
PITCH = "#160D20"
PITCH_STRIPE = "#1D1129"


# ============================================================
# PAGE BACKGROUND / CUSTOM CSS
# ============================================================
# NOTE: Streamlit's st.markdown renders through a Markdown parser first.
# Any line indented with 4+ spaces is interpreted as a Markdown code
# block and printed as literal text instead of being rendered as HTML.
# To avoid this, every HTML/CSS string below is built with NO leading
# indentation on any line.

st.markdown(f"""
<style>
.stApp {{
background: radial-gradient(circle at 15% 10%, rgba(92,35,128,0.35), transparent 30%), radial-gradient(circle at 85% 15%, rgba(190,30,70,0.20), transparent 30%), linear-gradient(135deg, #080817 0%, #12091F 50%, #080B18 100%);
}}
[data-testid="stSidebar"] {{
background: #0D0915;
}}
.block-container {{
padding-top: 2rem;
padding-bottom: 2rem;
}}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(f"""
<div style="padding:10px 0 5px 0;">
<div style="color:{GOLD};font-size:14px;font-weight:700;letter-spacing:3px;text-transform:uppercase;margin-bottom:4px;">UEFA EURO 2024</div>
<h1 style="color:{WHITE};font-size:44px;font-weight:850;letter-spacing:2px;margin:0;padding:0;">⚽ SOCCERLYSIS</h1>
<div style="color:{MUTED};font-size:16px;margin-top:5px;">Interactive Shot & Finishing Analysis</div>
<div style="width:80px;height:3px;background:linear-gradient(90deg, {GOLD}, {RED});margin-top:14px;border-radius:5px;"></div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown(f"""
<div style="color:{TEXT};font-size:15px;line-height:1.6;margin:10px 0 20px 0;max-width:900px;">
Explore shooting patterns, expected goals (xG), finishing outcomes, and player performance through an interactive football analytics dashboard.
</div>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("euros_2024_shot_map.csv")

    # Keep only shot events
    if "type" in df.columns:
        df = df[df["type"].eq("Shot")].copy()

    # Parse shot location
    def parse_location(value):
        if isinstance(value, (list, tuple)):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, TypeError):
                pass
        return None

    df["location"] = df["location"].apply(parse_location)

    # Expected Goals
    df["xG"] = pd.to_numeric(df["shot_statsbomb_xg"], errors="coerce").fillna(0)

    # Goal indicator
    df["is_goal"] = df["shot_outcome"].astype(str).str.strip().str.lower().eq("goal")

    return df


# ============================================================
# LOAD DATA WITH ERROR HANDLING
# ============================================================

try:
    df = load_data()

except FileNotFoundError:
    st.error("⚠️ euros_2024_shot_map.csv could not be found.")

    st.markdown(f"""
<div style="background:{CARD};border:1px solid {RED};border-radius:12px;padding:20px;color:{TEXT};">
<strong style="color:{GOLD};">Required file:</strong><br><br>
Place <b>euros_2024_shot_map.csv</b> in the same folder as this Streamlit application.<br><br>
Recommended structure:
<pre style="color:{GOLD_LIGHT};background:#0D0912;padding:12px;border-radius:8px;">Sport_Analysis/
├── SoccerLysis_ShotMap_Improved.py
└── euros_2024_shot_map.csv</pre>
</div>
""", unsafe_allow_html=True)

    st.stop()

except Exception as e:
    st.error(f"Data loading error: {e}")
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(f"""
<div style="padding:8px 0 15px 0;border-bottom:1px solid {PURPLE};margin-bottom:15px;">
<div style="color:{GOLD};font-size:12px;font-weight:700;letter-spacing:2px;">SOCCERLYSIS</div>
<div style="color:{WHITE};font-size:22px;font-weight:800;margin-top:3px;">Match Filters</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# TEAM FILTER
# ============================================================

teams = sorted(df["team"].dropna().unique())
selected_team = st.sidebar.selectbox("Team", ["All Teams"] + teams)

if selected_team == "All Teams":
    team_df = df.copy()
else:
    team_df = df[df["team"].eq(selected_team)].copy()


# ============================================================
# PLAYER FILTER
# ============================================================

players = sorted(team_df["player"].dropna().unique())
selected_player = st.sidebar.selectbox("Player", ["All Players"] + players)

if selected_player == "All Players":
    analysis_df = team_df.copy()
else:
    analysis_df = team_df[team_df["player"].eq(selected_player)].copy()


# ============================================================
# OUTCOME FILTER
# ============================================================

outcomes = sorted(analysis_df["shot_outcome"].dropna().unique())
selected_outcome = st.sidebar.selectbox("Shot Outcome", ["All Outcomes"] + outcomes)

if selected_outcome != "All Outcomes":
    analysis_df = analysis_df[analysis_df["shot_outcome"].eq(selected_outcome)].copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

shots = len(analysis_df)
goals = int(analysis_df["is_goal"].sum())
total_xg = float(analysis_df["xG"].sum())
avg_xg = float(analysis_df["xG"].mean()) if shots else 0
conversion = (goals / shots * 100) if shots else 0
xg_overperformance = goals - total_xg


# ============================================================
# METRIC CARD FUNCTION
# ============================================================

def metric_card(title, value, subtitle=""):
    st.markdown(f"""
<div style="background:linear-gradient(145deg, {CARD_LIGHT}, {CARD});border:1px solid rgba(244,201,93,0.30);border-radius:14px;padding:17px 15px;min-height:105px;box-shadow:0 8px 25px rgba(0,0,0,0.30);">
<div style="color:{MUTED};font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;">{title}</div>
<div style="color:{GOLD};font-size:29px;font-weight:850;margin-top:7px;">{value}</div>
<div style="color:#806E91;font-size:10px;margin-top:2px;">{subtitle}</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# KPI ROW
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    metric_card("Shots", f"{shots:,}", "Total attempts")

with c2:
    metric_card("Goals", f"{goals:,}", "Successful finishes")

with c3:
    metric_card("Total xG", f"{total_xg:.2f}", "Expected goals")

with c4:
    metric_card("Avg. xG / Shot", f"{avg_xg:.2f}", "Chance quality")

with c5:
    metric_card("Conversion Rate", f"{conversion:.1f}%", "Shots converted")

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# SECTION TITLE FUNCTION
# ============================================================

def section_title(title, subtitle=""):
    st.markdown(f"""
<div style="margin:12px 0 12px 0;">
<div style="color:{GOLD};font-size:21px;font-weight:800;">{title}</div>
<div style="color:{MUTED};font-size:12px;margin-top:3px;">{subtitle}</div>
<div style="width:55px;height:2px;background:{GOLD};margin-top:7px;border-radius:5px;"></div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# MAIN CONTENT COLUMNS
# ============================================================

left, right = st.columns([1.25, 1])


# ============================================================
# SHOT MAP
# ============================================================

with left:
    section_title("Shot Map", "Shot location and expected-goal quality")

    pitch = VerticalPitch(
        pitch_type="statsbomb",
        half=True,
        pitch_color=PITCH,
        line_color="#E8D8B0",
        stripe=True,
        stripe_color=PITCH_STRIPE,
    )

    fig, ax = pitch.draw(figsize=(8, 8))

    if analysis_df.empty:
        ax.text(
            60, 40,
            "No shots match the selected filters",
            ha="center", va="center",
            color=WHITE, fontsize=13,
        )
    else:
        for row in analysis_df.itertuples():
            location = row.location

            if not isinstance(location, (list, tuple)):
                continue
            if len(location) < 2:
                continue

            try:
                x = float(location[0])
                y = float(location[1])
                xg_value = float(row.xG)
            except (TypeError, ValueError):
                continue

            is_goal = bool(row.is_goal)

            pitch.scatter(
                x=x, y=y, ax=ax,
                s=max(100, 2200 * xg_value),
                color=(GOLD if is_goal else RED),
                edgecolor=WHITE,
                linewidth=0.8,
                alpha=0.9,
                zorder=(3 if is_goal else 2),
            )

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # LEGEND
    st.markdown(f"""
<div style="display:flex;gap:22px;align-items:center;color:{MUTED};font-size:12px;margin-top:-5px;">
<span><span style="display:inline-block;width:10px;height:10px;background:{GOLD};border-radius:50%;margin-right:5px;"></span>Goal</span>
<span><span style="display:inline-block;width:10px;height:10px;background:{RED};border-radius:50%;margin-right:5px;"></span>Non-goal</span>
<span>Larger marker = higher xG</span>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PERFORMANCE SNAPSHOT
# ============================================================

with right:
    section_title("Performance Snapshot", "Finishing performance relative to expected goals")

    st.markdown(f"""
<div style="background:linear-gradient(135deg, {CARD_LIGHT}, {CARD});border:1px solid rgba(244,201,93,0.30);border-radius:14px;padding:20px;margin-bottom:15px;">
<div style="color:{MUTED};font-size:12px;text-transform:uppercase;letter-spacing:1px;font-weight:700;">Goals vs Expected Goals</div>
<div style="color:{GOLD};font-size:34px;font-weight:850;margin-top:6px;">{xg_overperformance:+.2f}</div>
<div style="color:{MUTED};font-size:11px;margin-top:3px;">Positive = finishing above expectation</div>
</div>
""", unsafe_allow_html=True)

    # SELECTION DESCRIPTION
    if selected_player != "All Players":
        selection_text = f"Showing <b>{selected_player}</b>'s shooting profile"
        if selected_team != "All Teams":
            selection_text += f" for <b>{selected_team}</b>"
        selection_text += "."
    elif selected_team != "All Teams":
        selection_text = f"Showing the shooting profile for <b>{selected_team}</b>."
    else:
        selection_text = "Showing all available Euro 2024 shot events."

    st.markdown(f"""
<div style="background:rgba(36,17,47,0.55);border-left:3px solid {GOLD};padding:13px 15px;border-radius:7px;color:{TEXT};font-size:13px;margin-bottom:15px;">
{selection_text}
</div>
""", unsafe_allow_html=True)

    # OUTCOME SUMMARY
    if not analysis_df.empty:
        summary = (
            analysis_df
            .groupby("shot_outcome", dropna=False)
            .agg(Shots=("shot_outcome", "size"), xG=("xG", "sum"))
            .sort_values("Shots", ascending=False)
            .reset_index()
        )
        summary["xG"] = summary["xG"].round(2)

        st.dataframe(summary, use_container_width=True, hide_index=True)
    else:
        st.info("No shot outcome data available for the selected filters.")


# ============================================================
# PLAYER SHOOTING LEADERBOARD
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

section_title("Player Shooting Leaderboard", "Top players ranked by goals, xG and shot volume")

leaderboard = (
    team_df
    .groupby("player")
    .agg(
        Shots=("player", "size"),
        Goals=("is_goal", "sum"),
        xG=("xG", "sum"),
    )
    .reset_index()
)

# CONVERSION RATE
leaderboard["Conversion %"] = (leaderboard["Goals"] / leaderboard["Shots"] * 100).round(1)
leaderboard["xG"] = leaderboard["xG"].round(2)
leaderboard["Goals"] = leaderboard["Goals"].astype(int)

# SORT LEADERBOARD
leaderboard = leaderboard.sort_values(
    ["Goals", "xG", "Shots"],
    ascending=[False, False, False],
)

# DISPLAY LEADERBOARD
st.dataframe(
    leaderboard.head(15),
    use_container_width=True,
    hide_index=True,
    column_config={
        "xG": st.column_config.NumberColumn("xG", format="%.2f"),
        "Conversion %": st.column_config.NumberColumn("Conversion %", format="%.1f%%"),
    },
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(f"""
<div style="margin-top:35px;padding:18px 0 5px 0;border-top:1px solid {PURPLE};text-align:center;">
<div style="color:{GOLD};font-size:12px;font-weight:700;letter-spacing:1px;">⚽ SOCCERLYSIS</div>
<div style="color:{MUTED};font-size:11px;margin-top:5px;">Football analytics focused on shot location, xG and finishing performance.</div>
<div style="color:#6F627C;font-size:10px;margin-top:7px;">Built with Python · Pandas · Streamlit · Matplotlib · mplsoccer</div>
</div>
""", unsafe_allow_html=True)
