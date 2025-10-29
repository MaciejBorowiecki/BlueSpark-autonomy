# Different methods of calculating distance between auv and detected object

*TODO*: add requirements (python imports)
```
python3 -m venv venv
*activate venv and install requirements*
```

## 1) triangular similarity

*TODO*: add info about this method

**To configure new object**

Add its real width to `distance_utils.py` file inside dictionary.
Use `calibration.py` 

```bash
python3 calibration.py
c

```
where `c` will write info (pixel width and focal length) on terminal. Use these measurements to update dictionary.

**To use main program**

```bash
python3 main.py
```

## 2) Pose estimation using PNP from opencv2
*TODO*: configure using charuco and post results