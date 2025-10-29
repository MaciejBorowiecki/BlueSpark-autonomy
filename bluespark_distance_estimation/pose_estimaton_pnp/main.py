# main.py
import cv2
import time
from detector import detect_bottle
from distance_estimator import load_camera_params, estimate_distance

def main(camera_index=0, imgsz=224):
    camera_matrix, dist_coeffs = load_camera_params()
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Nie można otworzyć kamery.")
        return

    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        # detekcja (przekazujemy imgsz)
        bottles = detect_bottle(frame, imgsz=imgsz, threshold=0.5)
        for bbox in bottles:
            x1, y1, x2, y2, conf = bbox
            estimate_distance(frame, (x1, y1, x2, y2), camera_matrix, dist_coeffs)

        end_time = time.time()
        fps = 1.0 / (end_time - start_time) if (end_time - start_time) > 0 else 0.0
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Bottle Distance - SolvePnP", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(imgsz=224)
