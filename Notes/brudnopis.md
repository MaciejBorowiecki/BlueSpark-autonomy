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

3. **Object Tracking**
   - Apply SORT to track dynamic obstacles over time and maintain consistent IDs.

4. **Spatial Mapping & Classification**
   - Convert YOLO detections + SORT tracking into world coordinates.
   - Classify each object: avoid vs pass-through.
   - Update a local map of obstacles.

5. **Motion Planning**
   - Integrate a planner that uses the classified map to decide:
     - Which obstacles to avoid,
     - Which obstacles can be passed through,
     - How to safely navigate around moving objects.

6. **Control**
   - Translate planned paths into robot commands for motors/actuators.

7. **Testing & Iteration**
   - Test in controlled environments, refine object classification and tracking thresholds.

