# robo_magellan_main
## Setup and Installation
We are using ROS melodic + Gazebo 9. I'll let you figure out how to install them.
Clone this repo into your catkin ws as src
```
cd /wherever/your/catkin_ws/is
git clone git@github.com:Sea-Swindlers/robo_magellan_main.git src
cd src
git submodule init
git submodule update
source ./setup_paths.sh
```
To install other depandancies:
```
cd scripts
./install_robo_magellan_dep.sh
```
## Building
### ROS
We don't want to build px4 through catkin therefore we can disable it by running:
```
cd /wherever/your/catkin_ws/is
touch src/px4_autopilot/CATKIN_IGNORE
```
Not sure if there is a better way to do this but it works. We will build PX4 with the simulator in the next section.

To build everything run:
```
catkin_make_isolated
```

### PX4 + Simulator
To test the default `px4_sitl` rover simulation run:
```
make px4_sitl gazebo_rover__baylands
```
This will validate whether or not you can build and run the base simulation. Our simulator setup will build on top of this.

To run our custom simulator with sensors, obstacles, and cones run:
```
cd px4_autopilot
DONT_RUN=1 make px4_sitl_default gazebo
source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/sitl_gazebo
roslaunch px4 posix_sitl.launch world:="$SITL_GAZEBO_PATH/worlds/baylands.world" vehicle:="rover" sdf:="$RM_MODELS_PATH/rm_rover/rm_rover.sdf"
```
note: if you source /devel/setup.bash you can do roslaunch for some reason. Not sure why and I haven't found a solution to this yet. It might cause issues down the line but we will figure it out when we get there.