import streamlit as st
from utils.mediapipe_utils import extract_inclination_angles
from utils.phase_classifier import classify_turn_phases
from utils.video_overlay import overlay_phase_on_video

st.title("アルペンスキー内傾角フェーズ分析")

video_file = st.file_uploader("動画をアップロード", type=["mp4"])
if video_file:
    with open("temp.mp4", "wb") as f:
        f.write(video_file.read())
    st.video("temp.mp4")

    if st.button("分析開始"):
        angle_df = extract_inclination_angles("temp.mp4")
        phases = classify_turn_phases(angle_df)
        angle_df["phase"] = phases
        st.dataframe(angle_df)

        st.write("フェーズ別統計")

        st.dataframe(angle_df.groupby("phase")[["left_inclination", "right_inclination"]].mean())

if st.button("フェーズ付き動画を生成"):
    overlay_phase_on_video("temp.mp4", "output_with_phase.mp4", angle_df["phase"])
    st.video("output_with_phase.mp4")

