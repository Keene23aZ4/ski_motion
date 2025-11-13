import cv2

def overlay_phase_on_video(input_path, output_path, phase_series):
    cap = cv2.VideoCapture(input_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out    = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_idx >= len(phase_series):
            break

        phase = phase_series.iloc[frame_idx]
        color = (0, 255, 0) if phase == "neutral" else (255, 0, 0) if phase == "left_turn" else (0, 0, 255)
        label = f"Phase: {phase}"

        cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()