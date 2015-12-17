echo "Writing rplidar rules..."
echo 'KERNEL=="ttyACM*",ATTRS{idVendor}=="15d1",SYMLINK+="hokuyolidar",MODE="0666"' > /etc/udev/rules.d/91-hokuyo.rules
echo "rules complete, added symlink 'hokuyolidar', chmod to 0666"