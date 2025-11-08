"""
calibrate_charuco.py

Performs camera calibration using the ChArUco images captured by
auto_capture_charuco.py.

It iterates through the images, finds ChArUco corners, and then
calculates the camera's intrinsic matrix (K) and distortion
coefficients.

The results are saved to:
- camera_calibration.json (for human/web use)
- camera_calibration.npz (for Python/OpenCV use)
"""

import cv2
import numpy as np
import glob
import json
import os

# ----------------------------------------------------
# Board Configuration (MUST match gen_charuco_pdf.py)
# ----------------------------------------------------
SQUARES_X = 5
SQUARES_Y = 7
SQUARE_LENGTH_M = 0.035
MARKER_LENGTH_M = 0.025 # 0.7 * SQUARE_LENGTH_M
ARUCO_DICT_ID = cv2.aruco.DICT_4X4_50
# ----------------------------------------------------

# --- Setup ---
IMAGE_DIR = "charuco_images" # Folder with captured images
OUTPUT_JSON = "camera_calibration.json"
OUTPUT_NPZ = "camera_calibration.npz"

aruco = cv2.aruco
aruco_dict = aruco.getPredefinedDictionary(ARUCO_DICT_ID)
board = aruco.CharucoBoard((SQUARES_X, SQUARES_Y), 
                           SQUARE_LENGTH_M, 
                           MARKER_LENGTH_M, 
                           aruco_dict)
params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, params)

# --- Image Processing ---

images = sorted(glob.glob(os.path.join(IMAGE_DIR, "*.png")))
if len(images) == 0:
    print(f"Error: No images found in '{IMAGE_DIR}'.")
    print("Run auto_capture_charuco.py first.")
    exit(1)

print(f"Found {len(images)} images. Detecting corners...")

all_corners = []  # 2D pixel coordinates of corners in all images
all_ids = []      # IDs of those corners
img_size = None   # (width, height)

# 1. Loop through all images and find corners
for i, fname in enumerate(images):
    img = cv2.imread(fname)
    if img is None:
        print(f"Warning: Could not read {fname}, skipping.")
        continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img_size is None:
        # Get image size from the first valid image
        img_size = gray.shape[::-1] # (width, height)

    # 2. Detect ArUco markers first
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None and len(ids) > 0:
        # 3. If markers found, interpolate to find ChArUco corners
        retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            corners, ids, gray, board)
        
        # 4. If interpolation is successful, store the results
        if retval and charuco_corners is not None and charuco_ids is not None and len(charuco_corners) > 4:
            all_corners.append(charuco_corners)
            all_ids.append(charuco_ids)
    
    # Simple progress bar
    print(f"  Processed {i+1}/{len(images)}...", end='\r')

print(f"\nFound usable ChArUco corners in {len(all_corners)} of {len(images)} images.")

if len(all_corners) < 5:
    print("Error: Not enough valid images for calibration (need at least 5).")
    print("Try capturing more images from different angles and distances.")
    exit(1)

# --- Calibration ---

print("Calibrating camera...")

# 5. Initialize calibration flags (can be customized)
flags = (cv2.CALIB_RATIONAL_MODEL) # Use a 5-coeff distortion model

# 6. Run the calibration!
# This function finds the camera matrix, distortion coefficients,
# and rotation/translation vectors for each image.
ret, camera_matrix, dist_coeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
    charucoCorners=all_corners,
    charucoIds=all_ids,
    board=board,
    imageSize=img_size,
    cameraMatrix=None,    # We want the function to find this
    distCoeffs=None,    # We want the function to find this
    flags=flags
)

print("\n--- Calibration Results ---")
print(f"RMS Reprojection Error: {ret}")
print("  (A good value is < 1.0, an excellent value is < 0.5)")
print("\nCamera Matrix (K):\n", camera_matrix)
print("\nDistortion Coefficients:\n", dist_coeffs.ravel())

# --- Save Results ---

# 7. Save to NPZ (binary format for NumPy/OpenCV)
np.savez(OUTPUT_NPZ, 
         camera_matrix=camera_matrix, 
         dist_coeffs=dist_coeffs, 
         rms=ret,
         image_size=img_size)

# 8. Save to JSON (human-readable format)
data_for_json = {
    "camera_matrix": camera_matrix.tolist(),
    "dist_coeffs": dist_coeffs.tolist(),
    "rms": float(ret),
    "image_size": [int(img_size[0]), int(img_size[1])]
}
with open(OUTPUT_JSON, "w") as f:
    json.dump(data_for_json, f, indent=2)

print(f"\n[SUCCESS] Calibration saved to:")
print(f"  - {OUTPUT_NPZ}")
print(f"  - {OUTPUT_JSON}")