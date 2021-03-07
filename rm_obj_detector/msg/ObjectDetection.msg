# Name of the detection. (eg: 'person', 'cone', etc,)
string detection_name

# Estimated direction of the detection wrt to the robot.
# Assumes that we are working off a flat plane.
#     units: radians 
#     range: [-pi,pi]
 
float32 detection_direction

# Estimated distance of the detection
#     units: meters
#     range: [0, MAX_FLOAT)
float32 detection_distance
