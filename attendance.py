import cv2
import os
import csv
from datetime import datetime
from deepface import DeepFace

KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_DIR = "attendance"

# Load known faces
known_faces = []
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        name = filename.split(".")[0]
        known_faces.append(name)

print(f"Loaded students: {known_faces}")

# Today's attendance file
date = datetime.now().strftime("%Y-%m-%d")
attendance_file = os.path.join(ATTENDANCE_DIR, f"attendance_{date}.csv")

# Create CSV if not exists
if not os.path.exists(attendance_file):
    with open(attendance_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Time", "Status"])

marked = []

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# Warmup
for i in range(30):
    cap.read()

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("Attendance system started... Press 's' to scan, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect and draw bounding box
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Face Detected", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Attendance System", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        temp_path = "temp.jpg"
        cv2.imwrite(temp_path, frame)

        for name in known_faces:
            if name in marked:
                continue
            try:
                known_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
                result = DeepFace.verify(temp_path, known_path, enforce_detection=False)

                if result["verified"]:
                    time_now = datetime.now().strftime("%H:%M:%S")
                    with open(attendance_file, "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([name, time_now, "Present"])
                    marked.append(name)
                    print(f"Attendance marked for {name}!")
                    cv2.putText(frame, f"{name} - Present!", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Attendance System", frame)
                    cv2.waitKey(2000)

            except Exception as e:
                print(f"Error: {e}")

    elif key == ord('q'):
        break

# Auto mark absent
with open(attendance_file, "a", newline="") as f:
    writer = csv.writer(f)
    for name in known_faces:
        if name not in marked:
            writer.writerow([name, "--", "Absent"])
            print(f"{name} marked as Absent.")

cap.release()
cv2.destroyAllWindows()
print("Attendance saved!")