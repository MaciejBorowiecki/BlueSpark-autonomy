import cv2
import time
from detector import detect_objects


def main(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Nie można otworzyć kamery.")
        return

    print("Uruchomiono kamerę — naciśnij 'q' aby zakończyć.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        start_time = time.time()
        frame, detected_objects = detect_objects(frame)
        fps = 1 / (time.time() - start_time)

        # FPS w rogu
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("BlueSpark", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
