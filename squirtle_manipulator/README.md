Initialize arm
-> roslaunch squirtle_arm squirtle_arm_bringup.launch 
Run gui
-> arbotix_gui
To just run an arm planning code:
run moveit
-> roslaunch turtlebot_arm_moveit_config turtlebot_arm_moveit.launch sim:=false --screen
run sendPose script
-> rosrun squirtle_arm_kinematics senPose.py
run a planning script
-> rosrun squirtle_arm_kinematics armPlanning.py
OR run foll. for flower demo
-> rosrun squirtle_arm_kinematics squirtleFlowerGreeting.py

