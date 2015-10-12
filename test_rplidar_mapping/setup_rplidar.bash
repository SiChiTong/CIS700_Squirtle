echo "Writing rplidar rules..."
echo 'KERNEL=="ttyUSB*", SUBSYSTEM=="tty", DRIVERS=="cp210x", SYMLINK+="rplidar", MODE="0666"' > /etc/udev/rules.d/90-rplidar.rules
echo "rules complete, added symlink 'rplidar', chmod to 0666"