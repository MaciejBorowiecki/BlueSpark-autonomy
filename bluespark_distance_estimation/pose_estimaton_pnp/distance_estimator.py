import cv2
import numpy as np

def load_camera_params():
    data = np.load("camera_params.npz")
    return data["camera_matrix"], data["dist_coeffs"]

def estimate_distance(frame, bbox, camera_matrix, dist_coeffs):
    x1, y1, x2, y2 = bbox
    object_points = np.array([
        [0, 0, 0],
        [0.07, 0, 0],
        [0.07, 0.25, 0],
        [0, 0.25, 0]
    ], dtype=np.float32)

    image_points = np.array([
        [x1, y1],
        [x2, y1],
        [x2, y2],
        [x1, y2]
    ], dtype=np.float32)

    success, rvec, tvec = cv2.solvePnP(
        object_points, image_points, camera_matrix, dist_coeffs
    )

    if success:
        distance = np.linalg.norm(tvec)
        cv2.putText(frame, f"{distance:.2f} m", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        return distance
    return None
