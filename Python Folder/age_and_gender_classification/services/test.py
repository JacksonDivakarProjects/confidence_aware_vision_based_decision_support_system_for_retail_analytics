import cv2
import os
from dotenv import load_dotenv

load_dotenv()
IP_VIDEO_URL = "http://" + os.getenv("IP_ADDRESS") + "/video"

# 0 = default camera (webcam)
cap = cv2.VideoCapture(IP_VIDEO_URL)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Camera", frame)

    # press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()