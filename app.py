import streamlit as st
import pandas as pd
import numpy as np

# Page Layout Configuration
st.set_page_config(
    page_title="PrizePicks Hammer Model",
    page_icon="🔨",
    layout="centered"
)

st.title("🔨 PrizePicks Hammer Model")
st.markdown("Automated edge detection and evaluation for your target slips.")

def load_slip_data():
    """Loads the specific player data from your slip."""
    data = [
        {"player_name": "Yordan Alvarez", "team": "HOU", "stat_type": "Hitter FS", "line_score": 6.5, "model_projection": 7.8},
        {"player_name": "Jackson Chourio", "team": "MIL", "stat_type": "Hitter FS", "line_score": 5.5, "model_projection": 4.1},
        {"player_name": "Dominic Canzone", "team": "SEA", "stat_type": "Hitter FS", "line_score": 5.0, "model_projection": 6.2},
        {"player_name": "Bryan Reynolds", "team": "PIT", "stat_type": "Hitter FS", "line_score": 5.0, "model_projection": 3.9},
        {"player_name": "Rafael Devers", "team": "SF", "stat_type": "Hitter FS", "line_score": 5.5, "model_projection": 6.9},
        {"player_name": "Vladimir Guerrero Jr.", "team": "TOR", "stat_type": "Hitter FS", "line_score": 5.5, "model_projection": 4.2}
    ]
    return pd.DataFrame(data)

# Load data dataframe
df = load_slip_data()

# Model Edge Calculations
df["projection_diff"] = df["model_projection"] - df["line_score"]
df["edge_percentage"] = (df["projection_diff"] / df["line_score"]) * 100

# Strict Filtering Logic
conditions = [
    (df["edge_percentage"] >= 8.0),   
    (df["edge_percentage"] <= -8.0)   
]
choices = ["HAMMER MORE 🟢", "HAMMER LESS 🔴"]
df["recommendation"] = np.select(conditions, choices, default="PASS ⚪")

# Display metrics overview
col1, col2, col3 = st.columns(3)
col1.metric("Total Slates Analyzed", len(df))
col2.metric("Hammer More Picks", len(df[df["recommendation"] == "HAMMER MORE 🟢"]))
col3.metric("Hammer Less Picks", len(df[df["recommendation"] == "HAMMMER LESS 🔴"] if "HAMMMER LESS 🔴" in df["recommendation"].values else df[df["recommendation"] == "HAMMER LESS 🔴"]))

st.subheader("Target Player Projections & Recommendations")
st.dataframe(
    df[["player_name", "team", "line_score", "model_projection", "edge_percentage", "recommendation"]],
    use_container_width=True
)

# Interactive Adjustments
st.subheader("Fine-Tune Projections")
selected_player = st.selectbox("Select Player to Test Line Adjustment", df["player_name"].tolist())
player_row = df[df["player_name"] == selected_player].iloc[0]

new_projection = st.slider(
    f"Adjust Model Projection for {selected_player}", 
    min_value=1.0, 
    max_value=15.0, 
    value=float(player_row["model_projection"]), 
    step=0.1
)

if st.button("Recalculate Edge"):
    diff = new_projection - player_row["line_score"]
    edge = (diff / player_row["line_score"]) * 100
    if edge >= 8.0:
        rec = "HAMMER MORE 🟢"
    elif edge <= -8.0:
        rec = "HAMMER LESS 🔴"
    else:
        rec = "PASS ⚪"
    st.success(f"Updated Recommendation for {selected_player}: **{rec}** (Edge: {edge:.1f}%)")
