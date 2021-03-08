#include "ros/ros.h"
#include "std_msgs/String.h"
#include "nav_msgs/Odometry.h"
// #include <tf/transform_datatypes.h>

#include "rm_obj_detector/ObjectDetection.h"


static nav_msgs::Odometry::ConstPtr reference_gt;
static nav_msgs::Odometry::ConstPtr target_gt;

void setReferenceGtCallback(nav_msgs::Odometry::ConstPtr msg) {
    ROS_INFO("Setting reference gt: %s", msg->child_frame_id.c_str());
    // reference_gt = msg;
}

void setTargetGtCallback(nav_msgs::Odometry::ConstPtr msg){
    ROS_INFO("Setting target gt: %s", msg->child_frame_id.c_str());
    // target_gt = msg;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "object_detector_gt_publisher");

    ros::NodeHandle nh;

    ros::Publisher obj_detector_pub = nh.advertise<rm_obj_detector::ObjectDetection>("/obj_detections", 1000);
    ros::Subscriber reference_obj = nh.subscribe("/rm_rover/ground_truth_state", 1000, setReferenceGtCallback);
    ros::Subscriber target_obj = nh.subscribe("/cone/ground_truth_state", 1000, setTargetGtCallback);

    ros::Rate loop_rate(10);

    while (ros::ok())
    {
        rm_obj_detector::ObjectDetection msg;

        msg.detection_name = "Testing";
        msg.detection_direction = 1.0;
        msg.detection_distance = 2.0;

        obj_detector_pub.publish(msg);

        ros::spinOnce();

        loop_rate.sleep();
    }

    return 0;
}