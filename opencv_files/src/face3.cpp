#include "opencv2/objdetect/objdetect.hpp"
 #include "opencv2/highgui/highgui.hpp"
 #include "opencv2/imgproc/imgproc.hpp"

 #include <iostream>
 #include <stdio.h>

 using namespace std;
 using namespace cv;

 /** Function Headers */
 void detectAndDisplay( Mat frame );

 /** Global variables */
 String face_cascade_name = "/home/alienbot/Documents/opencv/haarcascades/haarcascade_frontalface_alt.xml";
 String eyes_cascade_name = "/home/alienbot/Documents/opencv/haarcascades/haarcascade_eye_tree_eyeglasses.xml";
 String f2_cascade_name = "/home/alienbot/Documents/opencv/haarcascades/haarcascade_frontalface_alt2.xml";
 String f3_cascade_name = "/home/alienbot/Documents/opencv/haarcascades/haarcascade_frontalface_alt_tree.xml";
 String f4_cascade_name = "/home/alienbot/Documents/opencv/haarcascades/haarcascade_frontalface_default.xml";
 String f5_cascade_name = "/home/alienbot/Documents/opencv/haarcascades/haarcascade_profileface.xml";
 
 CascadeClassifier face_cascade;
 CascadeClassifier eyes_cascade;
 CascadeClassifier f2_cascade;
 CascadeClassifier f3_cascade;
 CascadeClassifier f4_cascade;
 CascadeClassifier f5_cascade;
 string window_name = "Capture - Face detection";
 RNG rng(12345);

 /** @function main */
 int main( int argc, const char** argv )
 {
   CvCapture* capture;
   Mat frame;
   namedWindow( "Display window", WINDOW_AUTOSIZE );

   //-- 1. Load the cascades
   if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };
   if( !eyes_cascade.load( eyes_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };
   if( !f2_cascade.load( f2_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };
   if( !f3_cascade.load( f3_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };
   if( !f4_cascade.load( f4_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };
   if( !f5_cascade.load( f5_cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };



   //-- 2. Read the video stream
   capture = cvCaptureFromCAM( -1 );
   if( capture )
   {
     while( true )
     {
   frame = cvQueryFrame( capture );

   //-- 3. Apply the classifier to the frame
       if( !frame.empty() )
       { detectAndDisplay( frame ); }
       else
       { printf(" --(!) No captured frame -- Break!"); break; }

       int c = waitKey(10);
       if( (char)c == 'c' ) { break; }
      }
   }
   return 0;
 }

/** @function detectAndDisplay */
void detectAndDisplay( Mat frame )
{
  std::vector<Rect> faces;
  Mat frame_gray;

  cvtColor( frame, frame_gray, CV_BGR2GRAY );
  equalizeHist( frame_gray, frame_gray );

  //-- Detect faces
  face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(30, 30) );

  for( size_t i = 0; i < faces.size(); i++ )
  {
    Point center( faces[i].x + faces[i].width*0.5, faces[i].y + faces[i].height*0.5 );
    ellipse( frame, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar( 255, 0, 255 ), 4, 8, 0 );

    Mat faceROI = frame_gray( faces[i] );
    std::vector<Rect> eyes;

    //-- In each face, detect eyes
    eyes_cascade.detectMultiScale( faceROI, eyes, 1.1, 2, 0 |CV_HAAR_SCALE_IMAGE, Size(30, 30) );

    for( size_t j = 0; j < eyes.size(); j++ )
     {
       Point center( faces[i].x + eyes[j].x + eyes[j].width*0.5, faces[i].y + eyes[j].y + eyes[j].height*0.5 );
       int radius = cvRound( (eyes[j].width + eyes[j].height)*0.25 );
       circle( frame, center, radius, Scalar( 255, 0, 0 ), 4, 8, 0 );
     }

     resize(faceROI, faceROI, Size(100,100));
     imshow( "Display window", faceROI ); 
    //printf("height:%d width:%d \n", faceROI.rows, faceROI.cols);
    //-- In each face, detect smiles
    // std::vector<Rect> smiles;
    // smile_cascade.detectMultiScale( faceROI, smiles, 1.1, 2, 0 |CV_HAAR_SCALE_IMAGE, Size(30, 30) );

    // for( size_t j = 0; j < smiles.size(); j++ )
    //  {
    //    Point center( faces[i].x + smiles[j].x + smiles[j].width*0.5, faces[i].y + smiles[j].y + smiles[j].height*0.5 );
    //    int radius = cvRound( (smiles[j].width + smiles[j].height)*0.25 );
    //    circle( frame, center, radius, Scalar( 0, 0, 255 ), 4, 8, 0 );
    //  }
  }

/*  std::vector<Rect> f2;
  f2_cascade.detectMultiScale( frame_gray, f2, 1.1, 2, 0 |CV_HAAR_SCALE_IMAGE, Size(30, 30) );
  for( size_t i = 0; i < f2.size(); i++ ){
     Point center( f2[i].x + f2[i].width*0.5, f2[i].y + f2[i].height*0.5 );
     ellipse( frame, center, Size( f2[i].width*0.5, f2[i].height*0.5), 0, 0, 360, Scalar( 100, 100, 0 ), 4, 8, 0 );
   }

   std::vector<Rect> f3;
   f3_cascade.detectMultiScale( frame_gray, f3, 1.1, 2, 0 |CV_HAAR_SCALE_IMAGE, Size(30, 30) );
   for( size_t i = 0; i < f3.size(); i++ ){
     Point center( f3[i].x + f3[i].width*0.5, f3[i].y + f3[i].height*0.5 );
     ellipse( frame, center, Size( f3[i].width*0.5, f3[i].height*0.5), 0, 0, 360, Scalar( 0, 100, 100 ), 4, 8, 0 );
   }

   std::vector<Rect> f4;
   f4_cascade.detectMultiScale( frame_gray, f4, 1.1, 2, 0 |CV_HAAR_SCALE_IMAGE, Size(30, 30) );
   for( size_t i = 0; i < f4.size(); i++ ){
     Point center( f4[i].x + f4[i].width*0.5, f4[i].y + f4[i].height*0.5 );
     ellipse( frame, center, Size( f4[i].width*0.5, f4[i].height*0.5), 0, 0, 360, Scalar( 0, 0, 100 ), 4, 8, 0 );
   }

   std::vector<Rect> f5;
   f5_cascade.detectMultiScale( frame_gray, f5, 1.1, 2, 0 |CV_HAAR_SCALE_IMAGE, Size(30, 30) );
   for( size_t i = 0; i < f5.size(); i++ ){
     Point center( f5[i].x + f5[i].width*0.5, f5[i].y + f5[i].height*0.5 );
     ellipse( frame, center, Size( f5[i].width*0.5, f5[i].height*0.5), 0, 0, 360, Scalar( 100, 100, 100 ), 4, 8, 0 );
   }*/



  //-- Show what you got
  imshow( window_name, frame );
 }