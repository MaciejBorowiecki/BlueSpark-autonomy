# This notepad contains information gathered before the repository was created

### List of teams from SAUVC 2024/2025 and their technologies (generated with ChatGPT)

[List of Teams](https://chatgpt.com/c/68a5a966-1ad4-8333-97df-87877f8706c3)

### Winning Teams (models / strategies)

* [mecatron](https://mecatron.sg/computervision) - yolo, no info about strategy
* [hydronautics](https://github.com/hydronautics-team/stingray) - yolo, SORT
  * Some kind of algorithm for calculating distance / angle from single frame
* **Sort - object tracking algorithm** - [SORT basic info](https://arxiv.org/abs/1602.00763)
  * *UPDATE* SORT algorithm is not going to steer and thus make robot autonomous. What it's going to do is create ID for every single object that is detected and track it.
  


## Action Plan for Implementation

1. **Sensors & Data Acquisition**
   - Install RGB-D camera, possibly sonar later.
   - Stream video/images for object detection.

2. **Object Detection**
   - Implement YOLO for real-time detection of obstacles.

3. **Object Tracking** *Possibly won't be necessary for static obstacles*
   - Apply SORT to track dynamic obstacles over time and maintain consistent IDs.

4. **Spatial Mapping & Classification**
   - Convert YOLO detections + SORT tracking into world coordinates.
   - Classify each object: avoid vs pass-through.
   - Update a local map of obstacles.

5. **Motion Planning**
   - Integrate a planner that uses the classified map to decide:
     - Which obstacles to avoid,
     - Which obstacles can be passed through,
     - How to safely navigate around objects.

6. **Control**
   - Translate planned paths into robot commands for motors/actuators.

7. **Testing & Iteration**
   - Test in controlled environments, refine object classification and tracking thresholds.

## Research

Based on [this article](https://drive.google.com/file/d/1Y0a3Y5Xk32tmBIXpi-BSFWalChpfiyJg/view?usp=sharing) comparing different YOLO versions for underwater vision tasks, the accuracy remains relatively consistent across models, while the main improvement lies in inference speed — with newer versions, particularly YOLOv10, achieving the fastest performance.

### Artykuły o optymalizacji YOLO na raspberry pi
###### Jakieś losowe może warte przeczytania
 - [ ] [learnOpenCV  - ogólne podsumowanie](https://learnopencv.com/yolo11-on-raspberry-pi/)
 - [ ] [kilka odpowiedzi na GitHub o sposobach optymalizacji](https://github.com/ultralytics/ultralytics/issues/6019)
 - [ ] [losowa strona z optymalizacją YOLO na raspberry i jetson](https://www.cohorte.co/blog/optimizing-yolofor-edge-devices)
###### Na pewno warte przeczytania
- [ ] [oficjalny poradnik ultralytics do raspberry](https://docs.ultralytics.com/guides/raspberry-pi/#raspberry-pi-series-comparison)
- [ ] [dyskusja o używaniu YOLO z raspberry](https://github.com/orgs/ultralytics/discussions/8277)
- [ ] [filmik ktoś osiągnął 30 fps na wykrywaniu z raspberry](https://www.youtube.com/watch?v=XKIm_R_rIeQ)
- [ ] [techniki optymalizacyjne dla raspberry](https://medium.com/academy-team/model-optimization-techniques-for-yolo-models-f440afa93adb)

