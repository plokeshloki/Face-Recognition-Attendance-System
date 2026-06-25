import cv2
import os

# Folder to save faces
KNOWN_FACES_DIR = "known_faces"

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# Warmup
for i in range(30):
    cap.read()

# Ask for student name
name = input("Enter student name: ")

print(f"Camera ready! Press 'c' to capture photo, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Register Face - Press 'c' to capture", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        # Save photo
        photo_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
        cv2.imwrite(photo_path, frame)
        print(f"Photo saved for {name}!")
        break

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()