import cv2
import time
from detector import detect_objects


# main method
def main(camera_index=0):

    # open and set camerea
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Can't open camera.")
        return

    print("Camera is working - press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        start_time = time.time()
        frame, detected_objects = detect_objects(frame)
        fps = 1 / (time.time() - start_time)  # compute fps

        # show fps in the corner
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # title
        cv2.imshow("BlueSpark", frame)

        # exit if "q" pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
