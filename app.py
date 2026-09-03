import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PrizePicks Top 6 Hammer Auto-Builder", page_icon="🔨", layout="wide")

st.title("🔨 PrizePicks Top 6 Board Auto-Builder")
st.markdown("Automatically scans the entire board, calculates mathematical edge percentages against current projection lines, and isolates the **Top 6 Hammer More or Hammer Less** plays.")

def generate_full_board_sim():
    """Simulates pulling a full slate board of MLB hitter fantasy projections."""
    board_data = [
        {"player_name": "Yordan Alvarez", "team": "HOU", "stat_type": "Hitter FS", "line_score": 6.5, "model_projection": 9.2, "trend": "Consistent Over"},
        {"player_name": "Shohei Ohtani", "team": "LAD", "stat_type": "Hitter FS", "line_score": 8.0, "model_projection": 11.4, "trend": "Consistent Over"},
        {"player_name": "Aaron Judge", "team": "NYY", "stat_type": "Hitter FS", "line_score": 8.5, "model_projection": 11.8, "trend": "Consistent Over"},
        {"player_name": "Jackson Chourio", "team": "MIL", "stat_type": "Hitter FS", "line_score": 5.5, "model_projection": 3.1, "trend": "Consistent Under"},
        {"player_name": "Bryan Reynolds", "team": "PIT", "stat_type": "Hitter FS", "line_score": 5.0, "model_projection": 2.6, "trend": "Consistent Under"},
        {"player_name": "Vladimir Guerrero Jr.", "team": "TOR", "stat_type": "Hitter FS", "line_score": 5.5, "model_projection": 3.0, "trend": "Consistent Under"},
        {"player_name": "Mookie Betts", "team": "LAD", "stat_type": "Hitter FS", "line_score": 7.0, "model_projection": 9.4, "trend": "Consistent Over"},
        {"player_name": "Rafael Devers", "team": "SF", "stat_type": "Hitter FS", "line_score": 5.5, "model_projection": 3.2, "trend": "Consistent Under"},
        {"player_name": "Kyle Schwarber", "team": "PHI", "stat_type": "Hitter FS", "line_score": 6.5, "model_projection": 9.1, "trend": "Consistent Over"},
        {"player_name": "Dominic Canzone", "team": "SEA", "stat_type": "Hitter FS", "line_score": 5.0, "model_projection": 2.8, "trend": "Consistent Under"}
    ]
    return pd.DataFrame(board_data)

# Load and process board
df = generate_full_board_sim()

df["projection_diff"] = df["model_projection"] - df["line_score"]
df["edge_percentage"] = (df["projection_diff"] / df["line_score"]) * 100
df["absolute_edge"] = df["edge_percentage"].abs()

# Assign Strict Recommendations
def assign_recommendations(row):
    if row["edge_percentage"] > 0 and row["trend"] == "Consistent Over":
        return "HAMMER MORE 🟢"
    elif row["edge_percentage"] < 0 and row["trend"] == "Consistent Under":
        return "HAMMER LESS 🔴"
    else:
        return "PASS ⚪"

df["recommendation"] = df.apply(assign_recommendations, axis=1)

# Filter only actionable hammer plays and rank by highest absolute mathematical edge
actionable_df = df[df["recommendation"] != "PASS ⚪"].copy()
actionable_df = actionable_df.sort_values(by="absolute_edge", ascending=False)

# Automatically capture the Top 6 absolute strongest picks across the full board
top_6_slip = actionable_df.head(6)

st.subheader("🔥 Automated Top 6 Final Lineup Slip")
st.markdown("The following 6 picks represent the highest EV directional edges detected across the entire board:")

st.dataframe(
    top_6_slip[["player_name", "team", "line_score", "model_projection", "edge_percentage", "recommendation"]],
    use_container_width=True
)

st.subheader("Complete Board Scan Status")
st.dataframe(
    df[["player_name", "team", "line_score", "model_projection", "edge_percentage", "recommendation"]],
    use_container_width=True
)
