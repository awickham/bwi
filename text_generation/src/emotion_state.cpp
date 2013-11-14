#include <ros/ros.h>
#include <image_transport/image_transport.h>

#include <cv_bridge/cv_bridge.h>
#include <opencv/cv.h>

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sstream>

#include <unistd.h>

void imageCallback(const sensor_msgs::ImageConstPtr &imgptr) {
    //Load image into OpenCV
    const sensor_msgs::Image img = *imgptr;
    cv_bridge::CvImagePtr image = cv_bridge::toCvCopy(img);
    cv::Mat cvImage = image->image;
    cv::Mat cvGray;

    //Convert image to grayscale
    cvtColor(cvImage, cvGray, CV_RGB2GRAY);
    cv::Mat cvOutput(cvGray);
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "emotion_state");
    ros::NodeHandle nh;

    image_transport::ImageTransport it(nh);
    image_transport::Subscriber sub = it.subscribe("input", 1, imageCallback);
}
