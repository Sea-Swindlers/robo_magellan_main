cd ..
export RM_CATKIN_WS_SRC_PATH="$(pwd)"
export RM_MODELS_PATH="$(pwd)/rm_models"
export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:$(pwd)/rm_models
cd scripts

