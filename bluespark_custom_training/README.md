# Custom Vision Model 

This package contains the validation scripts and experimental logic used to develop the vision backend for the **Bluespark AUV** (primarily SAUVC competition).

The primary purpose of this module is to determine the **best methodology** for underwater perception and to train the most robust model possible. We are actively comparing standard Object Detection against Pose Estimation to see which architecture provides the most reliable data for autonomous navigation.

## Core Objectives

1.  **Methodology Research:** Evaluating whether simple bounding boxes (Object Detection) are sufficient, or if structural keypoints (Pose Estimation) *(or perhaps other methodology)* are required for complex tasks.
2.  **Model Optimization:** Training and fine-tuning models to achieve the highest accuracy for specific competition elements, particularly the **gate**.
    * *Used datasets further in the documentation*
3.  **Inference Strategy:** Finding the most efficient way to extract geometry data (distance and angle) from visual inputs.

## Methodologies Tested

### 1. Object Detection (OD)
* **Approach:** Standard YOLOv8 and YOLOv11 detection.
* **Role:** Identifies the presence of the gate and provides a Bounding Box.
* **Navigation Logic:** The width/height of the box is used to estimate distance ($Z$) via **Triangle Similarity**.
* **Validation:** Tested using `gate_trained_test_od.py`.

### 2. Pose Estimation (Keypoints)
* **Approach:** YOLOv8 Pose (Keypoint detection).
* **Role:** Identifies specific structural corners of the gate *(objects may differ in the future)*.
* **Navigation Logic:**
    * This methodology was specifically tested to see if it improves the calculation of the **angle of the gate** relative to the AUV.
    * By extracting precise 2D coordinates of the corners, we can use **Perspective-n-Point (PnP)** algorithms to derive the gate's full 3D orientation (roll, pitch, yaw) and swim through the gate at the correct angle.
* **Validation:** Tested using `gate_trained_test_pose.py`.

---

## Datasets & Training

**Note:** The actual training of these models was performed using standard Ultralytics workflows on **Google Colab** to leverage GPU acceleration. The scripts in this folder are primarily for local inference and validation of those Colab-trained weights (`best.pt`, `best1070.pt`).

Several different dataset variations were created and tested to improve robustness against underwater noise and lighting conditions.

- [ ] **TODO:** which datasets  (roboflow, local)

---

## Validation Scripts

### `gate_trained_test_od.py`
**Object Detection Inference**
This script loads the trained OD model (e.g., `best1070.pt`) and runs inference on a directory of images to verify detection performance.
* **Output:** Prints Class IDs, Confidence scores, and Bounding Box coordinates (`x1, y1, x2, y2`).
* **Visuals:** Saves annotated images with bounding boxes to `runs/detect/predict`.

### `gate_trained_test_pose.py`
**Pose Estimation Inference**
This script loads the trained Pose model (e.g., `best.pt`) to verify if the model can accurately lock onto the gate's corners.
* **Output:** Iterates through detected objects and prints the precise ($x, y$) coordinates of every visible keypoint.
* **Visuals:** Saves annotated images with keypoint skeletons to `runs/pose/predict`.