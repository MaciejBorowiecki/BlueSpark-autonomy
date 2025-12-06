# BlueSpark-autonomy

    important: paths to files are wrong in most scripts after newest update, needs to be fixed before using

## Purpose

This repository is focused on research and development of everything related to autonomy of BlueSpark *here should be link to webpage / git* AUV project.

## What's the next step?

1. Apply currently best methodology to ros2 piloting
   1. test on gazeebo
   2. test in real life pool
2. Test other methodologies / fine tune these ones for better results

## Project Structure

```text
BlueSpark-autonomy
├── bluespark_custom_training/
│   ├── data/
│   ├── gate_trained_test_od.py
│   ├── gate_trained_test_pose.py
│   └── README.md
├── bluespark_distance_estimation/
│   ├── calibration/
│   ├── enhanced_triangle_similarity/
│   ├── pnp_pose_estimation/
│   ├── triangle_similarity/
│   └── README.md
├── ml_models/
├── draft_notes.md
└── README.md  
```

| Directory / File | Description |
| :--- | :--- |
| `bluespark_custom_training/` | Contains methodology research and validation scripts for developing the best vision model. |
| `gate_trained_test_od.py` | Validation script for **Object Detection** models. Outputs bounding boxes ( `x1, y1, x2, y2` ) for general obstacle avoidance. |
| `gate_trained_test_pose.py` | Validation script for **Pose Estimation** models. Outputs precise keypoints ( `lb, lt, rt, rb` ) for identifying gate corners. |
| `bluespark_distance_estimation/` | Contains the active navigation logic and distance calculation algorithms. |
| `calibration/` | Tools for generating Charuco boards and calculating the Camera Matrix required for advanced distance estimation. |
| `enhanced_triangle_similarity/` | Distance estimation logic combining **Object Detection** bounding boxes with the Camera Calibration Matrix. |
| `pnp_pose_estimation/` | 3D Pose logic combining **Pose Estimation** (Keypoints) with SolvePNP algorithms to find orientation. |
| `triangle_similarity/` | Legacy distance logic using simple focal length calculations. |
| `ml_models/` | Storage directory for trained model weights (e.g., `best.pt`, `yolov8n.pt`). |
| `draft_notes.md` | Preliminary research, competitor analysis (SAUVC), and optimization notes for edge devices. |