import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

mp_pose = mp.solutions.pose

def compute_inclination_angle(left_hip, left_ankle):
    vec = np.array([left_hip.x - left_ankle.x, left_hip.y - left_ankle.y])
    vertical = np.array([0, 1])
    angle_rad = np.arccos(np.dot(vec, vertical) / (np.linalg.norm(vec)))
    return np.degrees(angle_rad)

def extract_inclination_angles(video_path):
    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose()
    angles = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP]
            left_ankle = lm[mp_pose.PoseLandmark.LEFT_ANKLE]
            right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP]
            right_ankle = lm[mp_pose.PoseLandmark.RIGHT_ANKLE]

            left_angle = compute_inclination_angle(left_hip, left_ankle)
            right_angle = compute_inclination_angle(right_hip, right_ankle)

            angles.append({
                "frame": int(cap.get(cv2.CAP_PROP_POS_FRAMES)),
                "left_inclination": left_angle,
                "right_inclination": right_angle
            })

    cap.release()
    return pd.DataFrame(angles)