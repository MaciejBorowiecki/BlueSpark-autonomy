import cv2
import numpy as np
import json
import os

# default calibration file path
CALIBRATION_FILE = os.path.join("..", "calibration", "camera_calibration.json")

# load camera parameters from calibration file
def load_camera_params(calibration_file=CALIBRATION_FILE):
    if not os.path.exists(calibration_file):
        raise FileNotFoundError(f"Calibration file not found at: {calibration_file}")

    with open(calibration_file, "r") as f:
        calib = json.load(f)
    
    camera_matrix = np.array(calib["camera_matrix"], dtype=np.float32)
    dist_coeffs = np.array(calib["dist_coeffs"], dtype=np.float32)
    
    return camera_matrix, dist_coeffs

# estimate distance using solvePnP (full 4-point model)
def estimate_distance_pnp(frame, bbox, camera_matrix, dist_coeffs, real_height=0.25, real_width=0.07):
    x1, y1, x2, y2 = bbox
    
    # define 3D model points (in meters)
    object_points = np.array([
        [0, 0, 0],                          # bottom-center
        [-real_width/2, real_height, 0],    # top-left
        [real_width/2, real_height, 0],     # top-right
        [0, real_height, 0]                 # top-center
    ], dtype=np.float32)
    
    # define corresponding 2D image points from the bounding box
    center_x = (x1 + x2) / 2
    image_points = np.array([
        [center_x, y2],  # bottom-center (mapped to y2)
        [x1, y1],        # top-left (mapped to x1, y1)
        [x2, y1],        # top-right (mapped to x2, y1)  
        [center_x, y1]   # top-center (mapped to center_x, y1)
    ], dtype=np.float32)
    
    try:
        # solve for the pose
        success, rvec, tvec = cv2.solvePnP(
            object_points, 
            image_points, 
            camera_matrix, 
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE # Iterative method
        )
        
        if success:
            # tvec is the translation vector [X, Y, Z] from camera to object
            # The distance is the Euclidean norm (length) of this vector.
            distance = np.linalg.norm(tvec)
            
            # (optional) draw debug points on the frame
            for point in image_points:
                cv2.circle(frame, (int(point[0]), int(point[1])), 3, (255, 0, 0), -1)
            
            return distance
            
    except Exception as e:
        print(f"solvePnP Error: {e}")
    
    return None

# estimate distance using solvePnP (simple 2-point model)
def estimate_distance_pnp_simple(frame, bbox, camera_matrix, dist_coeffs, real_height=0.25):
    x1, y1, x2, y2 = bbox
    
    # define 3D model points (a simple vertical line)
    object_points = np.array([
        [0, 0, 0],           # bottom-center
        [0, real_height, 0]  # top-center
    ], dtype=np.float32)
    
    # define corresponding 2D image points
    center_x = (x1 + x2) / 2
    image_points = np.array([
        [center_x, y2],  # bottom-center
        [center_x, y1]   # top-center
    ], dtype=np.float32)
    
    try:
        # solve for the pose
        success, rvec, tvec = cv2.solvePnP(
            object_points, 
            image_points, 
            camera_matrix, 
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        if success:
            distance = np.linalg.norm(tvec)
            return distance
            
    except Exception as e:
        print(f"solvePnP Error: {e}")
    
    return None