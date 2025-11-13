import pandas as pd

def classify_turn_phases(angle_df, threshold=5):
    phases = []
    for _, row in angle_df.iterrows():
        l_angle = row["left_inclination"]
        r_angle = row["right_inclination"]

        if l_angle > threshold and r_angle < threshold:
            phases.append("left_turn")
        elif r_angle > threshold and l_angle < threshold:
            phases.append("right_turn")
        else:
            phases.append("neutral")
    return pd.Series(phases)


