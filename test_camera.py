import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

print("Camera starting... Press 'q' to quit")

for i in range(30):
    cap.read()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not found!")
        break
    
    cv2.imshow("Camera Test", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Camera closed successfully!")