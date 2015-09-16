#include<cstdio>
#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h> 
#include <actionlib/client/simple_action_client.h> 
#include <frontier_exploration/ExploreTaskAction.h>

int main(int argc, char** argv){ 
ros::init(argc, argv, "frontierExplore"); 
//tell the action client that we want to spin a thread by default
actionlib::SimpleActionClient<frontier_exploration::ExploreTaskAction> ac("explore_server", true); 

//wait for the action server to come up 
ROS_INFO("Waiting for action server to start."); 

// wait for the action server to start 
ac.waitForServer(); //will wait for infinite time 

ROS_INFO("Action server started, sending goal."); // send a goal to the action
frontier_exploration::ExploreTaskGoal goal; 
frontier_exploration::ExploreTaskFeedback feedback;

goal.explore_boundary.header.seq = 1; 
goal.explore_boundary.header.frame_id = "map"; 
goal.explore_boundary.polygon.points = {};
goal.explore_center.point.x = 0.2; 
goal.explore_center.point.y = 0; 
goal.explore_center.point.z = 0; 
//feedback.next_frontier.pose.position.x = 0.1;
//feedback.next_frontier.pose.position.y = 0.0;
ac.sendGoal(goal); 

ROS_INFO("Goal has been sent, waiting for action"); 
ac.waitForResult(); 
if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED) 
	ROS_INFO("Hooray, the base moved 0.1 meter forward"); 
else 
	ROS_INFO("The base failed to move forward 0.1 meter for some reason");

return 0; 
}
