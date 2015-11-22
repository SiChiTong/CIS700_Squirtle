# test_rplidar_mapping
Q: Why we use hector mapping instead of gmapping.
A: Of course it is more reasonable to use gmapping on robots with good odometry like turtlebot.
    But rplidar provide a large amount of noise when rotating, makes the odometry combined with laser unreliable. 
    Using hector mapping with a wider search will work well.
    Also hector mapping can be used without turtlebot, which is fun.

rplidar mapping testing code and user guide

Some step-by-step user guides can be found in "user_guide" directory

NOTE: before you do anything to rplidar, run the bash script:

$ sudo bash setup_rplidar.bash

This will set the rplidar rules, create symlink "rplidar" and chmod to "0666", otherwise rplidar.launch won't work
