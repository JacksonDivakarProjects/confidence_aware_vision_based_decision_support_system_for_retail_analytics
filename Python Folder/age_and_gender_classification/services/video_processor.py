
import cv2
import os
import time
from services.db import insert_to_db

# ---------------- FACE TRACKING ---------------- #

tracked_faces = {}
face_counter = 0

IOU_THRESHOLD = 0.5
FACE_TIMEOUT = 10  # seconds


def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    inter = max(0, xB - xA) * max(0, yB - yA)
    areaA = boxA[2] * boxA[3]
    areaB = boxB[2] * boxB[3]

    return inter / (areaA + areaB - inter + 1e-6)


def get_face_id(bbox):
    global face_counter
    now = time.time()

    for fid, data in tracked_faces.items():
        if iou(bbox, data["bbox"]) > IOU_THRESHOLD:
            tracked_faces[fid]["bbox"] = bbox
            tracked_faces[fid]["last_seen"] = now
            return fid, False  # existing face

    face_counter += 1
    tracked_faces[face_counter] = {
        "bbox": bbox,
        "last_seen": now
    }
    return face_counter, True  # new face


def cleanup_faces():
    now = time.time()
    for fid in list(tracked_faces.keys()):
        if now - tracked_faces[fid]["last_seen"] > FACE_TIMEOUT:
            del tracked_faces[fid]

class VideoProcessor:
    def __init__(self, age_classifier, gender_classifier):
        self.age_classifier = age_classifier
        self.gender_classifier = gender_classifier

        # 🔒 Absolute path handling (FIX)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "models"))

        prototxt_path = os.path.join(MODEL_DIR, "deploy.prototxt")
        model_path = os.path.join(MODEL_DIR, "res10_300x300_ssd_iter_140000.caffemodel")

        print("Loading face model:")
        print(prototxt_path)
        print(model_path)

        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    def run(self):
        # 🔁 Choose ONE
        # cap = cv2.VideoCapture(0)  # Laptop webcam
        ip_address = "http://192.168.31.100:8080/video"
        cap = cv2.VideoCapture(ip_address)  # IP Webcam (example)

        if not cap.isOpened():
            print("❌ Camera not opened")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)),
                1.0,
                (300, 300),
                (104.0, 177.0, 123.0)
            )

            self.net.setInput(blob)
            detections = self.net.forward()

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > 0.6:
                    box = detections[0, 0, i, 3:7] * [w, h, w, h]
                    x1, y1, x2, y2 = box.astype(int)

                    face = frame[y1:y2, x1:x2]
                    if face.size == 0:
                        continue

                    bbox = (x1, y1, x2 - x1, y2 - y1)
                    face_id, is_new = get_face_id(bbox)

                    if is_new:
                        gender, g_conf = self.gender_classifier.predict(face)
                        age, a_conf = self.age_classifier.predict(face)

                        # 🔽 INSERT INTO DATABASE HERE
                        insert_to_db(face_id, gender, age, max(g_conf, a_conf))


                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame, f"{gender} ({g_conf:.1f}%)",
                        (x1, y1 - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
                    )
                    cv2.putText(
                        frame, f"{age} ({a_conf:.1f}%)",
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
                    )

            cv2.imshow("Age & Gender Classification", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            cleanup_faces()

        cap.release()
        cv2.destroyAllWindows()
