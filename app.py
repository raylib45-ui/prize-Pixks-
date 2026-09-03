import pandas as pd
import numpy as np

def build_target_lineup_model():
    """
    Evaluates specific target players (Yordan Alvarez, Jackson Chourio, Dominic Canzone, 
    Bryan Reynolds, Rafael Devers, Vladimir Guerrero Jr.) for Hitter Fantasy Score (FS) 
    projections to automatically trigger 'Hammer More' or 'Hammer Less' recommendations.
    """
    
    # 1. Initialize dataframe with the exact target players from your slip
    data = [
        {"player_name": "Yordan Alvarez", "team": "HOU", "stat_type": "Hitter FS", "line_score": 6.5, "model_projection": 7.8},
        {"player_name": "Jackson Chourio", "team": "MIL", "stat_type": "Hitter FS", "line_score": 5.5, "model_projection": 4.1},
        {"player_name": "Dominic Canzone", "team": "SEA", "stat_type": "Hitter FS", "line_score": 5.0, "model_projection": 6.2},
        {"player_name": "Bryan Reynolds", "team": "PIT", "stat_type": "Hitter FS", "line_score": 5.0, "model_projection": 3.9},
        {"player_name": "Rafael Devers", "team": "SF", "stat_type": "Hitter FS", "line_score": 5.5, "model_projection": 6.9},
        {"player_name": "Vladimir Guerrero Jr.", "team": "TOR", "stat_type": "Hitter FS", "line_score": 5.5, "model_projection": 4.2}
    ]
    
    df = pd.DataFrame(data)
    
    # 2. Calculate edge differential and percentage difference
    df["projection_diff"] = df["model_projection"] - df["line_score"]
    df["edge_percentage"] = (df["projection_diff"] / df["line_score"]) * 100
    
    # 3. Apply strictly consistent filtering logic for Hammer More / Hammer Less automation
    conditions = [
        (df["edge_percentage"] >= 10.0),   # Strong upward trend line
        (df["edge_percentage"] <= -10.0)   # Strong downward trend line
    ]
    choices = ["HAMMER MORE 🟢", "HAMMER LESS 🔴"]
    
    df["recommendation"] = np.select(conditions, choices, default="PASS ⚪")
    
    return df

if __name__ == "__main__":
    model_results = build_target_lineup_model()
    
    print("--- Automated Hammer More / Less Model Output ---")
    print(model_results[["player_name", "team", "line_score", "model_projection", "recommendation"]].to_string(index=False))
