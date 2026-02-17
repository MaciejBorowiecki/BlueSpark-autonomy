# This directory contains additional tools for remote work with object detection

## TODO

- [ ] Auto image capture
- [ ] *maybe* drawing bboxes and info 

## VisionControl *`vision_manager.py`*

The main controller class that acts as a facade for the vision system. It parses command-line arguments and coordinates the camera and streamer instances.

```python
from remote_addons.vision_manager import VisionControl
vision = VisionControl()
ret, frame = vision.read()
vision.update(frame)
```

## RemoteStreamer *`remote_streamer.py`*

Handles preview of the detections in real time on local machine or on local network/ethernet connection.

#### args
* `--remote-preview`
    * boolean
    * Preview of the object detection will be shown on localhost site using flask, without this flag preview will be shown locally on computer
* `--stream-port`
    * integer
    * User can specify on which port will the stream be available *(defaults to 5000)*

## UniversalCamera *`camera.py`*

Makes camera actions universal whether user wants to use CSI raspberry camera *(in which case opencv is not working)* or usb camera. Check whether camera or necessary camera modules are available.

**Additional requirement for raspberry pi**: `python3-picamera2`

#### args
* `--cam`
    * string
    * can be set as **'AUTO', 'RPI', 'USB'**
    * Program will try to use camera chosen by user, in case of no argument defaults to auto