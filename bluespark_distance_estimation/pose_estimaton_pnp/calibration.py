# calibration.py
import cv2
import numpy as np
import glob

def calibrate_camera(images_path, board_size=(9,6), square_size=0.024):
    # przygotowanie punktów 3D (rzeczywiste wymiary szachownicy)
    objp = np.zeros((board_size[0]*board_size[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1,2)
    objp *= square_size  # rozmiar pola szachownicy w metrach

    objpoints = [] # punkty 3D
    imgpoints = [] # punkty 2D

    images = glob.glob(images_path + "/*.jpg")

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, board_size, None)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
            cv2.drawChessboardCorners(img, board_size, corners, ret)
            cv2.imshow('Calibration', img)
            cv2.waitKey(200)

    cv2.destroyAllWindows()

    # kalibracja
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    np.savez("camera_params.npz", camera_matrix=mtx, dist_coeffs=dist)
    print("Kalibracja zakończona. Zapisano: camera_params.npz")

if __name__ == "__main__":
    calibrate_camera("calibration_images")
