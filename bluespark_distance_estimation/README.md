# Different methods of calculating distance between auv and detected object

## 1. Triangle Similarity

### Description

The core logic is based on the following formula:

$$
Z = \frac{W \cdot F}{P}
$$

Where:
* $Z$ = distance (depth) to the object.
* $W$ = The **known real width** of the object in cm, which is stored in `KNOWN_WIDTHS` dictionary
* $F$ = The camera's **focal length in pixels `FX_PX`**. This is crucial value that must be found during calibration.
* $P$ = The **perceived width** of the object in the image (in pixels), as measured by the YOLO bounding box.


### Requirements

- openCV
- ultralytics

```bash
pip install opencv-python ultralytics
```

### How to use

#### Step 1:  Calibrate
   1. In `compute_focal_length.py` set `KNOWN_WIDTH` to real width in cm of the object which will be used to calibrate the camera.
   2. Place an object of known width ($W$) at a fixed, known distance ($Z$) from the camera.
   3. Run `compute_focal_length.py` and press `c` when the object is placed correctly *(in front of the camera, and step 2)*
   4. Copy the focal length value from the terminal and set `FX_PX` in `distance_utils.py` to this value.
#### Step 2: Configure
   1. Add real-world withs in cm for objects you want to measure to the `KNOWN_WIDTHS` dictionary in the `distance_utils.py` file.
#### Step 3: Run
   1. Execute `main.py` to start the live camera feed. The `detector.py` script will now use your calibrated `FX_PX` and `KNOWN_WIDTHS` to estimate the distance to objects in real-time.
   ```bash
   python main.py
   ```

## 2. Enhanced Triangle Similarity *(currently used)*

### Description

Overall idea for this method is the same as for the previous version of triangle similarity *(1)* but Unlike simpler models, this project relies on a full **camera calibration matrix (K)** to achieve higher accuracy.
1.  **Depth (Z):** The depth is calculated using the known real-world size of an object ($W_{\text{real}}$) and its perceived size in pixels ($P_{\text{pixels}}$), using the camera's calibrated focal length ($f_y$ or $f_x$).
   
    $$
    Z = \frac{W_{\text{real}} \cdot f_y}{P_{\text{height}}} \quad \text{or} \quad Z = \frac{W_{\text{real}} \cdot f_x}{P_{\text{width}}}
    $$

2.  **3D Position (X, Y):** Once the depth ($Z$) is known, we "un-project" the object's 2D pixel center ($p_x, p_y$) back into 3D space using the camera's calibrated principal point ($c_x, c_y$):
   
    $$
    X = \frac{(p_x - c_x) \cdot Z}{f_x}
    $$
    $$
    Y = \frac{(p_y - c_y) \cdot Z}{f_y}
    $$

All parameters ($f_x, f_y, c_x, c_y$) are loaded directly from the `camera_calibration.json` file.

### Requirements

- openCV
- ultralytics
- numpy
- img2pdf

```bash
pip install opencv-python ultralytics numpy img2pdf
```

### How to use

#### Step 1: Camera Calibration (Mandatory First Step)

Before you can estimate distances, you **must** calibrate your specific camera. This process generates the required `camera_calibration.json` file.

This folder contains a full suite of calibration scripts.

##### C_Step 1: Generate & Print the Board

1.  Run the script:
    ```bash
    python gen_charuco_pdf.py
    ```
2.  This creates `charuco_A4_for_print.pdf`.
3.  **CRITICAL:** Print this PDF at **100% SCALE**. Do not use "Fit to Page" or any other scaling, as the algorithm depends on the exact physical size you defined.

##### C_Step 2: Capture Calibration Images

1.  A helper script `run_capture.sh` is provided, which simply launches `auto_capture_charuco.py`.
2.  First, make the script executable:
    ```bash
    chmod +x run_capture.sh
    ```
3.  Run the capture script:
    ```bash
    ./run_capture.sh
    ```
4.  Move the printed board around in front of the camera. Vary the **angle, position, and distance** significantly. Get images of the board near the edges and corners of the frame.
5.  The script will automatically save images to the `charuco_images/` folder when it gets a clear view.
6.  Continue until it has collected the target number of images (by default it is 30) or press `q` to stop.

##### C_Step 3: Run the Calibration

1.  Run the main calibration script:
    ```bash
    python calibrate_charuco.py
    ```
2.  This script will process all images in the `charuco_images/` folder.
3.  It will output the **RMS Reprojection Error**. A value **below 1.0 is good**, and **below 0.5 is excellent**.
4.  If the RMS error is high, your images were not good (e.g., blurry, not enough variation) or your printed board measurements are wrong.

This script generates the **`camera_calibration.json`** file, which is now ready to be used by the main application.

---

#### Step 2: Setting up known objects

Once your camera is `camera_calibration.json` file exisits you can run the main program.


Define the real-world sizes (in **meters**) of the objects you want to track in `object_config.json`. The `reference_dim` tells the algorithm whether to use the object's `height` or `width` for its calculation.

**`object_config.json`**
```json
{
    "objects": {
        "bottle": {
            "real_size": 0.25,
            "reference_dim": "height",
            "description": "bottle - 25cm height"
        },
        "cell phone": {
            "real_size": 0.15, 
            "reference_dim": "width",
            "description": "Phone - 15cm width"
        },
        // etc.
    }
}
```

#### Step 3: Running program

Run the main script. It will automatically load camera_calibration.json and object_config.json.

```bash
python main.py
```

## 3. SolvePNP *(Perspective-n-Point)*

### Core Principle

The Perspective-n-Point (PnP) algorithm is a powerful method used to find the **full 3D pose** (position and orientation) of an object relative to the camera.

It works by finding a correspondence between 3D points in the *object's own coordinate system* and their 2D projection in the *camera's image plane*.



To work, it requires three key pieces of information:
1.  **3D Model Points (`object_points`):** We must define a 3D "model" of the object. In this project, we use a simple 4-point planar model representing the bottle's height and width (e.g., `[bottom-center, top-left, top-right, top-center]`).
2.  **2D Image Points (`image_points`):** We find the corresponding 2D pixel coordinates of those model points in the camera image. We derive these from the YOLO bounding box (e.g., `[center_x, y2]`, `[x1, y1]`, `[x2, y1]`, etc.).
3.  **Camera Parameters (K, D):** This is the **critical** part. We *must* use the `camera_matrix` (K) and `dist_coeffs` (D) obtained from a one-time camera calibration.

### How it Works

The `cv2.solvePnP` function takes these three inputs and mathematically solves for the **Rotation Vector (`rvec`)** and **Translation Vector (`tvec`)** that best "fit" or "project" the 3D model points onto their 2D image locations.

* `rvec` describes the object's orientation (its "roll, pitch, yaw").
* `tvec` describes the object's position (its `[X, Y, Z]` coordinates) in the camera's 3D coordinate system.

### Finding the Distance

Once `solvePnP` is successful, the `tvec` gives us the `[X, Y, Z]` position of the object's origin (which we defined as its bottom-center) relative to the camera lens.

To find the direct, "as-the-crow-flies" distance, we simply calculate the **Euclidean norm** (or magnitude) of this translation vector:

$$
Distance = \sqrt{X^2 + Y^2 + Z^2}
$$

This method is generally more robust than "Similar Triangles" because it inherently accounts for perspective distortion and can even handle object rotation (if the 3D model is accurate enough), however since we need to choose the most appriopriate model to work with raspberry pi **this method is too computationally heavy.**

### Requirements

1.  **Libraries:**
- opencv-python
- numpy
- ultralytics

1.  **Camera Calibration File:**
    * This method **requires** a `camera_calibration.json` file generated from a proper calibration process (e.g., using a ChArUco board like in `enhanced triangle similarity`).
    * The `main.py` script expects this file to be located at `../calibration/camera_calibration.json`.

2.  **Known Object Dimensions:**
    * You must know the **real-world height and width** (in meters) of the object you are tracking. These values are hardcoded in the `estimate_distance_pnp` function calls within `main.py`.

### How to Use

1.  **Place Calibration File:** Ensure your `camera_calibration.json` file is in the correct directory (`../calibration/`).

2.  **Verify Object Dimensions:** Open `main.py` and check that the `real_height` and `real_width` parameters passed to `estimate_distance_pnp` match the object you are detecting.

3.  **Run the Main Script:**
    ```bash
    python main.py
    ```

4.  **Controls:**
    * `q`: Press 'q' to quit the application.
    * `m`: Press 'm' to toggle between the "Full PnP" (4-point) and "Simple PnP" (2-point) estimation methods.