# 🚗 Driver Drowsiness Detection System

A real-time computer vision system that detects driver drowsiness using **Eye Aspect Ratio (EAR)** and **MediaPipe facial landmarks**, and alerts the driver to prevent accidents.

---

## 📌 Problem Statement

Driver fatigue is one of the leading causes of road accidents. This project aims to build a **real-time monitoring system** that detects signs of drowsiness and alerts the driver instantly.

---

## 🎯 Objective

- Detect eye closure using facial landmarks
- Identify drowsiness in real-time
- Trigger an alert system to prevent accidents
- Log drowsiness events for analysis

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV** – video processing
- **MediaPipe** – facial landmark detection
- **NumPy & SciPy** – numerical computation
- **Pygame** – alarm system

---

## ⚙️ How It Works

1. Webcam captures live video stream
2. MediaPipe detects **facial landmarks (468 points)**
3. Extract eye coordinates
4. Compute **Eye Aspect Ratio (EAR)**:
   
   EAR = (vertical eye distance) / (horizontal eye distance)

5. If EAR drops below threshold → eyes are closed
6. If eyes remain closed for consecutive frames → **Drowsiness detected**
7. Alarm is triggered and event is logged

---

## 🔥 Features

- ✅ Real-time face and eye tracking
- ✅ EAR-based drowsiness detection
- ✅ Audio alert system
- ✅ FPS (performance monitoring)
- ✅ Face bounding box visualization
- ✅ Status display (Awake / Drowsy)
- ✅ Drowsiness logging (CSV file with timestamps)

---

## 📊 Output

- Displays EAR value on screen
- Shows driver status (Awake / Drowsy)
- Triggers alert sound when drowsiness detected
- Logs events in `drowsiness_log.csv`

---

## 🎥 Demo Video

👉 [Click here to watch demo](https://drive.google.com/file/d/1Xzf-k5EEaoDGZ_FEwpkAqyfURpLT3jGN/view?usp=drivesdk)

---
