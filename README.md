# Project Report

**1. Project Overview**  

This project implements a Streamlit-based data visualization app that displays shot locations for Euro 2024 matches. The app helps users analyze team and player shooting patterns — highlighting where shots were taken, their expected goal (xG) value, and whether they resulted in goals.  

The project leverages:

**Streamlit** — for the interactive dashboard UI. 

**mplsoccer** (VerticalPitch) — for drawing a football pitch and plotting shot coordinates. 

**Pandas** — for data filtering and transformation.  

**Matplotlib** — for rendering visual charts.  

![View App](https://socceranalyst.streamlit.app/)

**2. Data Description**  

Column	Description  
team -	Name of the team taking the shot  
player -	Player who took the shot  
type -	Event type (filtered to "Shot")  
location -	JSON-formatted list [x, y] indicating shot coordinates on the pitch  
shot_outcome -	Describes if the shot was a goal, saved, blocked, etc.  
shot_statsbomb_xg -	Expected goals (xG) value assigned to the shot  

**3. Workflow Summary**  

**Step 1 — Data Loading & Cleaning** 
```python
df = pd.read_csv("euros_2024_shot_map.csv")
df = df[df["type"] == "Shot"].reset_index(drop=True)
df["location"] = df["location"].apply(json.loads)
Filters only events classified as “Shot”.
```
Converted the JSON-style location field into numerical [x, y] coordinates.  

**Step 2 — User Input Filters**  
```python
team = st.selectbox("Select a team", df["team"].sort_values().unique())
player = st.selectbox("Select a player", df[df["team"] == team]["player"].sort_values().unique())
Enables interactive filtering by team and player through dropdowns.
```
Automatically updates the player list once a team is selected.  

**Step 3 — Data Filtering**  
```python
def filter_data(df, team, player):
    if team:
        df = df[df["team"] == team]
    if player:
        df = df[df["player"] == player]
    return df
```
Dynamically filters data for visualization based on user selections.  
Ensures the display reflects the chosen subset (team or player).  

**Step 4 — Pitch Creation**  
```python
pitch = VerticalPitch(pitch_type="statsbomb", half=True, pitch_color="green",
                      line_color="white", stripe=True, stripe_color="#80f380")
fig, ax = pitch.draw(figsize=[10, 10])
```
Creates a half-pitch layout, perfect for shot visualizations.  
Visual appeal added using green pitch with light stripes.  

**Step 5 — Shot Plotting**  
```python
pitch.scatter(
    x=float(x["location"][0]),
    y=float(x["location"][1]),
    s=1000 * x["shot_statsbomb_xg"],
    color="gold" if x["shot_outcome"] == "Goal" else "red",
    edgecolor="black"
)
```
Color coding:  

🟡 Gold → Goals  
🔴 Red → Missed or saved shots  

Bubble size proportional to xG → higher xG = larger circle  

Edge color and transparency enhance clarity.  

**Step 6 — Visualization Output**  
```python
st.pyplot(fig)
```
Displays the resulting figure directly inside the Streamlit app.  

**4. Analytic Insights**  

This visualization provides key insights for analysts, coaches, or fans:  

**A. Shot Distribution**  
Clusters of shots near the penalty box suggest tactical preference for short-range shooting.  
Sparse long-range attempts may indicate disciplined or possession-based play.  

**B. Expected Goals (xG) Quality**  
Bubble size shows shot quality — players taking high-xG shots are positioned closer to goal.  
Teams with high average xG per shot are creating better scoring chances rather than speculative attempts.  

**C. Player-Specific Tendencies**  
Some players may shoot predominantly from specific zones (e.g., left channel or penalty spot).  
Consistent goal outcomes (gold bubbles) in similar coordinates may reveal preferred finishing zones.  

**D. Tactical & Defensive Insights**  
Comparing team maps highlights defensive weaknesses — e.g., repeated concessions from similar positions.  
Teams with spread-out shot maps tend to have flexible attacking strategies.  
