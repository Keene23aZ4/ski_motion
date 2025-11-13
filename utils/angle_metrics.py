def compute_metrics(angle_df, phases):
    result = {}
    for phase in ["early", "late", "neutral"]:
        subset = angle_df[phases == phase]
        result[phase] = {
            "hip_flexion_range": subset["hip_flexion"].max() - subset["hip_flexion"].min(),
            "knee_flexion_range": subset["knee_flexion"].max() - subset["knee_flexion"].min(),
            # 他の角度も同様に
        }
    return pd.DataFrame(result).T