#include <ros/ros.h>
#include <image_transport/image_transport.h>

#include <cv_bridge/cv_bridge.h>
#include <opencv/cv.h>

#include <stdio.h>
#include <stdlib.h>
#include <string>

// Above this is happy.
#define HAPPY_THRESHOLD 150.0
// Below this is sad.
#define SAD_THRESHOLD 125.0

double getVariance(const sensor_msgs::ImageConstPtr &imgptr) {
    const sensor_msgs::Image img = *imgptr;
    double red, green, blue;
    double totalVariance;
    for(int i=0; i < img.height*img.step - 2; i+=3) {
        red = img.data[i];
        green = img.data[i+1];
        blue = img.data[i+2];
        double averageRGB = (red+green+blue) / 3.0;
        totalVariance += (pow(red-averageRGB, 2) + pow(green-averageRGB, 2) +
                          pow(blue-averageRGB, 2)) / 3.0;
    }
    double numElements = img.height*img.width;
    return totalVariance / numElements;
}

void imageCallback(const sensor_msgs::ImageConstPtr &imgptr) {
    const sensor_msgs::Image img = *imgptr;
    
    double variance = getVariance(imgptr);
    
    std::string emotion = "ambivalent";
    if(variance > HAPPY_THRESHOLD) {
        emotion = "happy";
    } else if(variance < SAD_THRESHOLD) {
        emotion = "sad";
    }
    std::cout << "I'm feeling " << emotion << "          \r";
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "emotion_state");
    ros::NodeHandle nh;

    image_transport::ImageTransport it(nh);
    image_transport::Subscriber sub = it.subscribe("/camera/rgb/image_color", 1, imageCallback);

    ros::spin();
    return 0;
}
