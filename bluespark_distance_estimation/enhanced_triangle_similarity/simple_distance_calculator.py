import math
import json
import cv2
import numpy as np


class SimpleDistanceCalculator:

    # init
    def __init__(self, calibration_file="../calibration/camera_calibration.json"):
        self.camera_matrix, self.dist_coeffs = self.load_calibration(
            calibration_file)

        # objects attributes
        self.object_attrs = self.load_object_config("object_config.json")

    # load objects configuration
    def load_object_config(self, config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                return config["objects"]
        except FileNotFoundError:
            print(f"ERROR: file not found: {config_file}")
            return {}
        except KeyError:
            print(f"Error: json file must contain key 'objects'.")
            return {}

    # load camera calibration information
    def load_calibration(self, calibration_file):
        with open(calibration_file, "r") as f:
            calib = json.load(f)

        camera_matrix = np.array(calib["camera_matrix"])
        dist_coeffs = np.array(calib["dist_coeffs"])

        return camera_matrix, dist_coeffs

    # calculate distance and from detected objects
    def calculate_distance_and_angle(self, bbox, label_name):
        """
        Calculates distance and angle using bounding box.

        Args:
            bbox: [x1, y1, x2, y2] - bounding box
            label_name: object name (must be in objext_attrs)

        Returns:
            pos_x, pos_y, pos_z, horizontal_angle, vertical_angle
        """
        if label_name not in self.object_attrs:
            return None, None, None, None, None

        # camera parameters from camera matrix
        fx = self.camera_matrix[0, 0]   # focal length x
        fy = self.camera_matrix[1, 1]   # focal length y
        ppx = self.camera_matrix[0, 2]  # principal point x
        ppy = self.camera_matrix[1, 2]  # principal point y

        x1, y1, x2, y2 = bbox

        # bounding box dimensions
        obj_width = x2 - x1
        obj_height = y2 - y1
        obj_center_x = (x2 + x1) / 2
        obj_center_y = (y2 + y1) / 2

        # objects attributes
        real_size = self.object_attrs[label_name]["real_size"]
        reference_dim = self.object_attrs[label_name]["reference_dim"]

        # calculate distance (z dimension)
        if reference_dim == "width":
            pos_z = real_size * fx / obj_width
        elif reference_dim == "height":
            pos_z = real_size * fy / obj_height
        else:
            return None, None, None, None, None

        # calculate X,Y position in 3 dimensions
        pos_x = (obj_center_x - ppx) * pos_z / fx
        pos_y = (obj_center_y - ppy) * pos_z / fy

        # calculate angles in degrees
        horizontal_angle = math.atan2(pos_x, pos_z) * (180.0 / math.pi)
        vertical_angle = math.atan2(pos_y, pos_z) * (180.0 / math.pi)

        return pos_x, pos_y, pos_z, horizontal_angle, vertical_angle

    # Draw objects info
    def draw_info(self, frame, bbox, label_name, confidence):
        x1, y1, x2, y2 = bbox

        # calculate distance and angles
        pos_x, pos_y, pos_z, h_angle, v_angle = self.calculate_distance_and_angle(
            bbox, label_name)

        if pos_z is None:
            return

        # draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # prepere information to print
        distance_text = f"{pos_z:.2f}m"
        angle_text = f"H:{h_angle:.1f}° V:{v_angle:.1f}°"
        position_text = f"X:{pos_x:.2f}m Y:{pos_y:.2f}m"
        label_text = f"{label_name}: {confidence:.2f}"

        # print information
        y_offset = y1 - 10
        texts = [distance_text, angle_text, position_text, label_text]
        colors = [(0, 255, 255), (255, 255, 0), (255, 0, 255), (0, 255, 0)]

        for i, text in enumerate(texts):
            if y_offset < 20:  # decide where to put information (above or under object)
                y_offset = y2 + 20 + i * 20
            else:
                y_offset = y1 - 10 - i * 20

            cv2.putText(frame, text, (x1, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[i], 1)
