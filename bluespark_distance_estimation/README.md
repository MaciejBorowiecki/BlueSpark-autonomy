# Different methods of calculating distance between auv and detected object

## 1. triangular similarity

#### Description
The core logic is based on the following formula:
$$
Z = \frac{W * F}{P}
$$
Where:
* $Z$ = distance (depth) to the object.
* $W$ = The **known real width** of the object in cm, which is stored in `KNOWN_WIDTHS` dictionary
* $F$ = The camera's **focal length in pixels `FX_PX`**. This is crucial value that must be found during calibration.
* $P$ = The **perceived width** of the object in the image (in pixels), as measured by the YOLO bounding box.


#### Requirements
- openCV
- ultralytics

```bash
pip install opencv-python ultralytics
```

#### How to use

1. **Calibrate**:
   1. In `compute_focal_length.py` set `KNOWN_WIDTH` to real width in cm of the object which will be used to calibrate the camera.
   2. Place an object of known width ($W$) at a fixed, known distance ($Z$) from the camera.
   3. Run `compute_focal_length.py` and press `c` when the object is placed correctly *(in front of the camera, and step 2)*
   4. Copy the focal length value from the terminal and set `FX_PX` in `distance_utils.py` to this value.
2. **Configure:**
   1. Add real-world withs in cm for objects you want to measure to the `KNOWN_WIDTHS` dictionary in the `distance_utils.py` file.
3. **Run:**
   1. Execute `main.py` to start the live camera feed. The `detector.py` script will now use your calibrated `FX_PX` and `KNOWN_WIDTHS` to estimate the distance to objects in real-time.

## 2. Pose estimation using PNP from opencv2
*TODO*: configure using charuco and post resultso and post results  