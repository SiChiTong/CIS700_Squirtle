#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/objdetect/objdetect.hpp"

#include <stdlib.h>
#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;


static const std::string OPENCV_WINDOW = "Image window";
static const std::string OPENCV_TABLE = "Tabletop window";

class ImageConverter{
    ros::NodeHandle nh_;
    image_transport::ImageTransport it_;
    image_transport::Subscriber image_sub_;
    image_transport::Subscriber rgbimage_sub_;
    image_transport::Publisher image_pub_;
    Mat rgb_im;   
    public:
    ImageConverter() : it_(nh_){
        // Subscribe to camera input
        image_sub_ = it_.subscribe("/camera/depth/image", 1, &ImageConverter::imageCallback, this);
        rgbimage_sub_ = it_.subscribe("/camera/rgb/image_color", 1, &ImageConverter::rgbCallback, this);
        
        // Publish output
        image_pub_ = it_.advertise("/image_detection", 1);
        rgb_im = Mat::zeros(480,640,CV_8UC3);
        // Visualize
        namedWindow(OPENCV_WINDOW);
        namedWindow(OPENCV_TABLE);
    }

    ~ImageConverter(){
        destroyWindow(OPENCV_WINDOW);
        destroyWindow(OPENCV_TABLE);
    }

    void rgbCallback(const sensor_msgs::ImageConstPtr& msg){
        cv_bridge::CvImagePtr cv_ptr;
        try{
            cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_8UC3);
        }
        catch (cv_bridge::Exception& e){
            ROS_ERROR("cv_bridge exception: %s", e.what());
            return;
        }
        rgb_im = cv_ptr->image;
        
        //imshow(OPENCV_WINDOW, rgb_im);
        //waitKey(1);
    }

    /** function called by the subscriber **/
    void imageCallback(const sensor_msgs::ImageConstPtr& msg){
        cv_bridge::CvImagePtr cv_ptr;
        try{
            cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_32FC1);
        }
        catch (cv_bridge::Exception& e){
            ROS_ERROR("cv_bridge exception: %s", e.what());
            return;
        }

        Mat frame_gray = cv_ptr->image;
        
        Mat frame_color;
        cvtColor(frame_gray, frame_color, CV_GRAY2RGB);

        sensor_msgs::ImagePtr img_msg;

        /*
			Mat faceROI = frame_color( faces[i] );
			resize(faceROI, faceROI, Size(100,100));
			
			// Output modified video stream
			img_msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", faceROI).toImageMsg();
			image_pub_.publish(img_msg);
			imshow(OPENCV_TABLE, faceROI );
        */
		
        int rows = frame_gray.rows;
        int cols = frame_gray.cols;

        // Get mat of X,Y,Z points
        Mat triples = Mat(rows*cols, 3, CV_32FC1);
        Mat notnan = Mat::zeros(rows*cols, 1, CV_8UC1);
        int sum = 0;
        int notsum = 0;
        for(int i=0;i<rows;i++){
            for(int j=0;j<cols;j++){
                triples.at<float>(i*cols+j,0) = i;
                triples.at<float>(i*cols+j,1) = j;
                triples.at<float>(i*cols+j,2) = frame_gray.at<float>(i,j)+0.0;
                if(!isnan(frame_gray.at<float>(i,j))){
                    notnan.at<uchar>(i*cols+j,0) = 1;
                    sum++;
                }else{
                    notnan.at<uchar>(i*cols+j,0) = 0;
                }
                
            }
        } 
        
        // Remove NANs
        Mat points = Mat(sum, 3, CV_32FC1);
        Mat column = Mat(sum,1,CV_32FC1);
        int id = 0;
        for(int i=0;i<rows*cols;i++){
            
            if(notnan.at<char>(i,0)==1){
                points.at<float>(id,0) = triples.at<float>(i,0);
                points.at<float>(id,1) = triples.at<float>(i,1);
                points.at<float>(id,2) = triples.at<float>(i,2);
                column.at<float>(id,0) = triples.at<float>(i,2);
                id++; 
            }
        }

        //RANSAC
        float inlier_thresh = .005;
        Mat ones = Mat::ones(3,1, CV_32FC1);
        Mat best_coeffs = ones;
        int max_inliers = 0;
        int ransac_trials = 100;
        for(int i=0;i<ransac_trials;i++){
            int r1 = rand()%sum;
            int r2 = rand()%sum;
            int r3 = rand()%sum;
            Mat pts3 = Mat(3,3,CV_32FC1);
            for(int j=0;j<3;j++){
                pts3.at<float>(0,j) = points.at<float>(r1,j);
                pts3.at<float>(1,j) = points.at<float>(r2,j);
                pts3.at<float>(2,j) = points.at<float>(r3,j);
            }
            //find plane defined by 3 points
            Mat coeffs = pts3.inv()*ones;

            // calculate distance from point to plane
            Mat vals = points*coeffs;
            Mat dist = vals-1;
            Mat powdist = dist.mul(dist);

            // count inliers
            int counter = 0;
            for(int j=0;j<sum;j++){
                if(powdist.at<float>(j,0)<inlier_thresh){
                    counter++;
                }
            }

            if (counter>max_inliers){
                max_inliers = counter;
                best_coeffs = coeffs;
            }
        }

        // color inliers
        Mat vals = triples*best_coeffs;
        Mat dist = vals-1;
        Mat powdist = dist.mul(dist);
        Mat objectMask = Mat::zeros(rows,cols, CV_8UC1);
        vector<Mat> channels;
        split(frame_color, channels); 

        for(int i=0;i<rows*cols;i++){
            if(powdist.at<float>(i,0)<inlier_thresh){
                channels[0].at<float>(i/cols,i%cols) = 0;
            }
            if(dist.at<float>(i,0)<-10*inlier_thresh){
                channels[1].at<float>(i/cols,i%cols) = 0;
                channels[2].at<float>(i/cols,i%cols) = 50;
                objectMask.at<uchar>(i/cols,i%cols) = 255;
            }
        }

        // clean up the regions 
        int dilation_size = 2;

        Mat element = getStructuringElement( MORPH_ELLIPSE, Size( 2*dilation_size + 1, 2*dilation_size+1 ), Point( dilation_size, dilation_size ) );
        erode( objectMask, objectMask, element );
        element = getStructuringElement( MORPH_ELLIPSE, Size( 4*dilation_size + 1, 4*dilation_size+1 ), Point( dilation_size, dilation_size ) );
        dilate( objectMask, objectMask, element );
        
        // extract object proposals
        vector<Mat> contours;
        findContours(objectMask, contours, CV_RETR_CCOMP, CV_CHAIN_APPROX_NONE);

        Point2f center;
        float radius;

        merge(channels, frame_color);

        // Find Connected Components
        Mat object;
        Mat temp;
        int obnum = 0;
        for(int i=0;i<contours.size();i++){
            //int i=0;
            minEnclosingCircle(contours[i], center, radius);
            ellipse( frame_color, center, Size( radius, radius), 0, 0, 360, Scalar( 255, 0, 255 ), 4, 8, 0 );
            ellipse( rgb_im, center, Size( radius, radius), 0, 0, 360, Scalar( 255, 0, 255 ), 4, 8, 0 );
            
            int xpt;
            if(center.x-radius<1){
                xpt = 1;
            }else{
                xpt = floor(center.x-radius);
            }
            int ypt;
            if(center.y-radius<1){
                ypt = 1;
            }else{
                ypt = floor(center.y-radius);
            }
            int radx = floor(radius);
            int rady = floor(radius);
            if(xpt+2*radius>rgb_im.cols){
                radx = rgb_im.cols-xpt;
            }
            if(xpt+2*radius>rgb_im.rows){
                rady = rgb_im.rows-ypt;
            }
            int minsize = 20;
            if(radx<minsize || rady<minsize){
                continue;
            }

            try{
                //object = rgb_im( Rect(ypt, xpt, rady, radx) );
                temp = rgb_im( Rect(xpt,ypt,radx*2,rady*2) );
                resize(temp, temp, Size(100,100));
                if(obnum==0){
                    object = temp;
                }else{
                    hconcat(object, temp, object);
                }
                obnum++;
                
            }catch( cv::Exception& e ){
                const char* err_msg = e.what();
                cout<<xpt<<" "<<ypt<<" "<<" "<<radx<<" "<<rady<<endl;
                std::cout << "exception caught: " << err_msg << std::endl;
            }
        }
        
        

        // Update GUI Window
        
        imshow(OPENCV_WINDOW, object);
        imshow(OPENCV_TABLE, frame_color);
        //imshow(OPENCV_WINDOW, rgb_im);

        waitKey(1);

    }
};

int main(int argc, char** argv){
 
    ros::init(argc, argv, "image_converter");
    ImageConverter ic;
    ros::spin();
    return 0;
}
