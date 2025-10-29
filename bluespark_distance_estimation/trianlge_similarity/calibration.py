# calibration.py
import cv2
from ultralytics import YOLO
from distance_utils import KNOWN_WIDTH

model = YOLO("yolo11s.pt").to("cpu")

DISTANCE_CM = 30.0   # odległość, na której ustawisz obiekt (cm)
THRESH = 0.5

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Ustaw obiekt o szerokości KNOWN_WIDTH na odległość DISTANCE_CM i naciśnij 'c' aby zmierzyć.")
print("Naciśnij 'q' aby wyjść.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, imgsz=224, verbose=False)
    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0])
            if conf < THRESH:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            w = x2 - x1
            cv2.putText(frame, f"w_px: {w}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

    cv2.imshow("calibration", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):  # compute focal length
        # znajdź pierwszy bbox w ostatniej klatce
        found = False
        for r in results:
            for box in r.boxes:
                if float(box.conf[0]) >= THRESH:
                    w_px = int(box.xyxy[0][2] - box.xyxy[0][0])
                    focal_length = (w_px * DISTANCE_CM) / KNOWN_WIDTH
                    print(f"Measured pixel width: {w_px} px")
                    print(f"Computed focal_length: {focal_length:.2f}")
                    print("Wklej tę wartość do distance_utils.py -> FOCAL_LENGTH")
                    found = True
                    break
            if found:
                break
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
