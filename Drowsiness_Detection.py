import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance
from pygame import mixer
import time
import csv
import datetime

# for alarm
mixer.init()
mixer.music.load("music.wav")

# mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# EAR function
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

#  eye landmarks
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

thresh = 0.25
frame_check = 40
flag = 0

cap = cv2.VideoCapture(0)

prev_time = 0

# logging setup for csv file
log_file = open("drowsiness_log.csv", "a", newline="")
writer = csv.writer(log_file)

if log_file.tell() == 0:
    writer.writerow(["Time", "EAR", "Status"])

last_log_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            h, w, _ = frame.shape

            left_eye = []
            right_eye = []

            for idx in LEFT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                left_eye.append((x, y))

            for idx in RIGHT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                right_eye.append((x, y))

            leftEAR = eye_aspect_ratio(left_eye)
            rightEAR = eye_aspect_ratio(right_eye)
            ear = (leftEAR + rightEAR) / 2.0

            # for eyes
            for p in left_eye:
                cv2.circle(frame, p, 2, (0,255,0), -1)
            for p in right_eye:
                cv2.circle(frame, p, 2, (0,255,0), -1)

            # face bounding box
            xs = [int(lm.x * w) for lm in face_landmarks.landmark]
            ys = [int(lm.y * h) for lm in face_landmarks.landmark]
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255,0,0), 2)

            # EAR display
            cv2.putText(frame, f"EAR: {ear:.2f}", (450,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

            # the main logic for drowsiness detection   
            if ear < thresh:
                flag += 1
                status = "DROWSY"

                if flag >= frame_check:
                    cv2.putText(frame, "ALERT! WAKE UP!", (150,50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                    # log every 2 seconds when drowsy
                    
                    if time.time() - last_log_time > 2:
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        writer.writerow([current_time, round(ear,3), "Drowsy"])
                        last_log_time = time.time()

                    if not mixer.music.get_busy():
                        mixer.music.play(-1)

            else:
                flag = 0
                status = "AWAKE"
                mixer.music.stop()

            cv2.putText(frame, f"Status: {status}", (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0,255,0) if status=="AWAKE" else (0,0,255), 2)

    # FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    cv2.putText(frame, f"FPS: {int(fps)}", (10,460),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

    cv2.imshow("Driver Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
log_file.close()