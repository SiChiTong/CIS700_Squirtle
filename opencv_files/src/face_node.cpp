#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/objdetect/objdetect.hpp"

#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

String Turtlepath = "/home/turtlebot/catkin_ws/src/CIS700_Squirtle/opencv_files/include/opencv_files/haarcascades/"; 
String Davidpath = "/home/alienbot/Documents/turtlebot/my_workspace/src/CIS700_Squirtle/opencv_files/include/opencv_files/haarcascades/";

String face_cascade_name = Davidpath + "haarcascade_frontalface_alt.xml";
String eyes_cascade_name = Davidpath + "haarcascade_eye.xml"; 

CascadeClassifier face_cascade;
CascadeClassifier eyes_cascade;

static const std::string OPENCV_WINDOW = "Image window";
static const std::string OPENCV_FACE = "Face window";

class ImageConverter{
    ros::NodeHandle nh_;
    image_transport::ImageTransport it_;
    image_transport::Subscriber image_sub_;
    image_transport::Publisher image_pub_;
  
    public:
    ImageConverter() : it_(nh_){
        // Subscribe to camera input
        image_sub_ = it_.subscribe("/camera/rgb/image_color", 1, &ImageConverter::imageCallback, this);
        // Publish output
        image_pub_ = it_.advertise("/image_converter/output_video", 1);

        // Visualize
        namedWindow(OPENCV_WINDOW);
    }

    ~ImageConverter(){
        destroyWindow(OPENCV_WINDOW);
    }

    /** function called by the subscriber **/
    void imageCallback(const sensor_msgs::ImageConstPtr& msg){
        cv_bridge::CvImagePtr cv_ptr;
        try{
            cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
        }
        catch (cv_bridge::Exception& e){
            ROS_ERROR("cv_bridge exception: %s", e.what());
            return;
        }

        // Draw an example circle on the video stream
        vector<Rect> faces;
        Mat frame_gray;
        Mat frame_color = cv_ptr->image;
        sensor_msgs::ImagePtr img_msg;

        cvtColor( cv_ptr->image, frame_gray, CV_BGR2GRAY );
        equalizeHist( frame_gray, frame_gray );

        // FACE DETECTION
        face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) );

        for( size_t i = 0; i < faces.size(); i++ ){
			Mat faceROI = frame_color( faces[i] );
			resize(faceROI, faceROI, Size(100,100));
			
			// Output modified video stream
			img_msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", faceROI).toImageMsg();
			image_pub_.publish(img_msg);
			imshow(OPENCV_FACE, faceROI );

			// Draw the face
			Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );
			ellipse( cv_ptr->image, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 4, 8, 0 );
			
        }
        // Update GUI Window
        imshow(OPENCV_WINDOW, cv_ptr->image);
        waitKey(1);

    }
};

int main(int argc, char** argv){
    if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading haar face (check the path on line 19)\n"); return -1; };
    if( !eyes_cascade.load( eyes_cascade_name ) ){ printf("--(!)Error loading haar eyes\n"); return -1; };
  
    ros::init(argc, argv, "image_converter");
    ImageConverter ic;
    ros::spin();
    return 0;
}
