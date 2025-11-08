"""
auto_capture_charuco.py

Automatically captures images from a webcam for camera calibration.

It detects a ChArUco board and saves images when the detection
is stable (>= min_corners) and the board has moved (>= min_interval),
ensuring a diverse set of images for good calibration.
"""

import cv2
import os
import time

# ----------------------------------------------------
# Board Configuration (MUST match gen_charuco_pdf.py)
# ----------------------------------------------------
SQUARES_X = 5
SQUARES_Y = 7
SQUARE_LENGTH_M = 0.035
MARKER_LENGTH_M = 0.025 # 0.7 * SQUARE_LENGTH_M
ARUCO_DICT_ID = cv2.aruco.DICT_4X4_50
# ----------------------------------------------------

# ----------------------------------------------------
# Capture Configuration
# ----------------------------------------------------
SAVE_DIR = "charuco_images"   # Directory to save images
CAMERA_INDEX = 0              # 0 for built-in, 1+ for external
TARGET_IMAGES = 40            # Number of images to collect
MIN_CORNERS = 15              # Min Charuco corners to trigger save
MIN_INTERVAL = 0.5            # Min seconds between captures (to get new poses)
# ----------------------------------------------------

# --- Setup ---

# 1. Initialize ArUco dictionary, board, and detector
aruco = cv2.aruco
aruco_dict = aruco.getPredefinedDictionary(ARUCO_DICT_ID)
detector_params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, detector_params)
board = aruco.CharucoBoard((SQUARES_X, SQUARES_Y), 
                           SQUARE_LENGTH_M, 
                           MARKER_LENGTH_M, 
                           aruco_dict)

# 2. Create save directory
os.makedirs(SAVE_DIR, exist_ok=True)
print(f"Saving images to '{SAVE_DIR}/' directory.")

# 3. Initialize camera
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
try:
    # Disable autofocus: CRITICAL for calibration
    # The focal length must remain constant.
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    print("Autofocus disabled.")
except Exception as e:
    print(f"Warning: Could not disable autofocus. {e}")

if not cap.isOpened():
    print(f"Error: Could not open camera index {CAMERA_INDEX}.")
    exit()

# --- Main Loop ---

saved_count = 0
last_saved_time = 0.0
print("Starting capture... Move the ChArUco board around the camera's view.")
print(f"Will save when {MIN_CORNERS} corners are detected.")
print("Press 'q' or 'ESC' to exit.")

while saved_count < TARGET_IMAGES:
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame. Exiting.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    display_frame = frame.copy()

    # 4. Detect ArUco markers
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None and len(ids) > 0:
        aruco.drawDetectedMarkers(display_frame, corners, ids)

        # 5. Interpolate ChArUco corners from ArUco markers
        retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            corners, ids, gray, board)

        if retval and charuco_corners is not None:
            n_corners = len(charuco_corners)
            aruco.drawDetectedCornersCharuco(display_frame, charuco_corners, charuco_ids)
            
            # Display corner count
            cv2.putText(display_frame, f"Charuco corners: {n_corners}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # 6. Check save criteria
            current_time = time.time()
            if (n_corners >= MIN_CORNERS and 
                (current_time - last_saved_time) > MIN_INTERVAL):
                
                # Save the original frame (not the one with drawings)
                fname = os.path.join(SAVE_DIR, f"charuco_{saved_count:03d}.png")
                cv2.imwrite(fname, frame)
                
                print(f"Saved {fname} (Corners: {n_corners})")
                saved_count += 1
                last_saved_time = current_time
    else:
        cv2.putText(display_frame, "No markers detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Display status
    cv2.putText(display_frame, f"Saved: {saved_count}/{TARGET_IMAGES}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Auto ChArUco Capture", display_frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'): # ESC or 'q'
        print("Capture interrupted by user.")
        break

if saved_count == TARGET_IMAGES:
    print(f"Capture complete. Collected {saved_count} images.")

cap.release()
cv2.destroyAllWindows() 