/*BASIC OPENCV VIDEO COLLECTION
 By David Isele*/


#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <vector>

using namespace cv;
using namespace std;

VideoCapture capture;
Mat frame;
Mat image;

int process(VideoCapture& capture) {
	string window_name = "video | q or esc to quit";
	cout << "press q or esc to quit" << endl;
	namedWindow(window_name, CV_WINDOW_KEEPRATIO); //resizable window;

	while(1==1) {
		//CAPTURE AN IMAGE FROM THE CAMERA
		capture >> frame;
		if (frame.empty())
			continue;
		imshow(window_name, frame);
		
		//COPY THE FRAME 
		//frame.copyTo(image);
        //cvtColor(image, hsv, CV_BGR2HSV);
		
		
		//EXIT STUFF
		char key = (char)waitKey(5); //delay N millis, usually long enough to display and capture input
		switch (key) {
		case 'q':
		case 'Q':
		case 27: //escape key
			return 0;
		default:
			break;
		}
	}
}



int main(int argc, char** argv) {
	//USE CAMERA 0 UNLESS ANOTHER CAMERA IS SPECIFIED AS AN ARGUMENT
    if( argc == 1 || (argc == 2 && strlen(argv[1]) == 1 && isdigit(argv[1][0])))
        capture.open(argc == 2 ? argv[1][0] - '0' : 0);
    else if( argc == 2 )
        capture.open(argv[1]);

	process(capture);
	return 0;
}
