# robo_magellan_main
## Installation
We are using ROS melodic + Gazebo 9. I'll let you figure out how to install them.
Clone this repo into your catkin ws as src
```
cd <RoboMagellan-catkin_ws>
git clone git@github.com:Sea-Swindlers/robo_magellan_main.git src
cd src
git submodule init
git submodule update
cd scripts
source setup_paths.sh
```
To install other depandancies:
```
./install_robo_magellan_dep.sh
```
To build everything run:
```
cd <RoboMagellan-catkin_ws>
catkin_make_isolated
```
## Run
Work in progress

# Simulator
## px4_sitl Installation
Clone the PX4
```
git clone git@github.com:PX4/PX4-Autopilot.git --recursive
```

To test the default `px4_sitl` rover simulation run:
```
cd <PX4-Autopilot_clone>
make px4_sitl gazebo_rover__baylands
```
This will validate whether or not you can build and run the base simulation. Our simulator setup will build on top of this.

## Test Custom Models
To test if you can get our custom models to run:

in the first terminal run, start an empty sim:
```
cd <RoboMagellan-catkin_ws>
cd src/scripts
source setup_paths.sh
cd <PX4-Autopilot_clone>
export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:$(pwd)/Tools/sitl_gazebo/build
export GAZEBO_MODEL_DATABASE_URI=""
roslaunch gazebo_ros empty_world.launch
```
An empty Gazebo sim should pop up. Now go to the insert tab an insert the ```rm_rover``` model into the sim.

in the second terminal, validate that the topics are being published properly:
```
rostopic list
```
and make sure that data is being published to the following topics:
```
/bumper/raw
/laser/scan
/ultrasonic_sensor_1/reading
/ultrasonic_sensor_2/reading
/ultrasonic_sensor_3/reading
/zed/depth/image_raw
```

## Run 
To run our custom simulator with sensors, obstacles, and cones run:
```
cd <PX4-Autopilot_clone>
DONT_RUN=1 make px4_sitl_default gazebo
source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/sitl_gazebo
export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:$(pwd)/Tools/sitl_gazebo/build
export GAZEBO_MODEL_DATABASE_URI=""
roslaunch px4 posix_sitl.launch world:="$RM_WORLDS_PATH/worlds/baylands.world" vehicle:="rover" sdf:="$RM_MODELS_PATH/rm_rover/rm_rover.sdf"
```
