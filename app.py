import streamlit as st
import os
from utils.mediapipe_utils import extract_inclination_angles
from utils.phase_classifier import classify_turn_phases
from utils.video_overlay import overlay_phase_on_video

st.set_page_config(page_title="スキー動画フェーズ分析", layout="centered")
st.title("⛷️ アルペンスキー フェーズ分析アプリ")

# 動画アップロード
video_file = st.file_uploader("動画をアップロードしてください", type=["mp4", "mov"])
if video_file:
    temp_video_path = "temp.mp4"
    with open(temp_video_path, "wb") as f:
        f.write(video_file.read())
    st.video(temp_video_path)

    # 分析開始ボタン
    if st.button("フェーズ分析を実行"):
        with st.spinner("内傾角を抽出中..."):
            angle_df = extract_inclination_angles(temp_video_path)

        with st.spinner("フェーズ分類中..."):
            phases = classify_turn_phases(angle_df)
            angle_df["phase"] = phases

        st.success("フェーズ分類完了！")
        st.dataframe(angle_df.head())

        # フェーズ付き動画生成
        output_path = "output_with_phase.mp4"
        with st.spinner("フェーズラベル付き動画を生成中..."):
            overlay_phase_on_video(temp_video_path, output_path, angle_df["phase"])

        st.success("動画生成完了！")
        st.video(output_path)
