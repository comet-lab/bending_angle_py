# bending_angle_py
# Description #
This package is for finding the bending angle of the wrist robot by 2 different color marker attached to tip.

wrist_marker_filter contains all the color filtering and angle calculation function.
The main body of function is in main.py

# Run
Run main.py

Click 4 points for perspective transformation (left top, right top, right bottom, left bottom). Space key.

Click the tip, center line of the base portion, and another point of the base portion.

# Dependencies
- python-opencv
- pyrealsense2
- numpy