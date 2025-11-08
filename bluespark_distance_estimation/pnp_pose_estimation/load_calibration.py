import json
import numpy as np
import cv2

# load json file
with open("calibration/camera_calibration.json", "r") as f:
    calib = json.load(f)

# extact data
camera_matrix = np.array(calib["camera_matrix"], dtype=np.float32)
dist_coeffs = np.array(calib["dist_coeffs"], dtype=np.float32)
image_size = tuple(calib["image_size"])

print("Camera matrix:\n", camera_matrix)
print("Distortion coefficients:\n", dist_coeffs)
print("Image size:", image_size)