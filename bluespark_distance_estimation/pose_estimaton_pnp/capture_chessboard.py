# capture_chessboard.py
import cv2
import os
import time
import argparse

def main(output_dir="calibration_images", camera_index=0,
         board_w=9, board_h=6, target_images=20, delay_between_saves=0.8):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # ustaw natywną/pożądaną rozdzielczość
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # spróbuj wyłączyć autofocus / auto exposure - działa jeśli sterownik obsługuje
    try:
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    except Exception:
        pass

    board_size = (board_w, board_h)
    saved = 0
    last_save_time = 0

    print("Naciśnij 'q' aby przerwać. Pokazuj szachownicę w różnych pozycjach...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, board_size,
                                                   cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)
        display = frame.copy()

        if found:
            # doprecyzowanie pozycji rogów
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
                                        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            cv2.drawChessboardCorners(display, board_size, corners2, found)

            # zapisuj tylko co pewien czas (by nie zapisać wielu niemal-identycznych)
            if time.time() - last_save_time > delay_between_saves and saved < target_images:
                filename = os.path.join(output_dir, f"calib_{saved:02d}.jpg")
                cv2.imwrite(filename, frame)
                saved += 1
                last_save_time = time.time()
                print(f"Zapisano {filename}  ({saved}/{target_images})")

        # tekst informacyjny
        cv2.putText(display, f"Saved: {saved}/{target_images}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        cv2.imshow("Capture Chessboard (press q to quit)", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or saved >= target_images:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Gotowe. Zamknięto kamerę.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", "-o", default="calibration_images")
    parser.add_argument("--cam", "-c", type=int, default=0)
    parser.add_argument("--w", type=int, default=9, help="liczba wewnętrznych narożników w szer.")
    parser.add_argument("--h", type=int, default=6, help="liczba wewnętrznych narożników w wys.")
    parser.add_argument("--n", type=int, default=20, help="ile zdjęć zapisać")
    args = parser.parse_args()
    main(output_dir=args.out, camera_index=args.cam, board_w=args.w, board_h=args.h, target_images=args.n)
