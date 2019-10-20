# Open House Aruco
Code for actuating robot claw based on Aruco marker IDs and distances for the 2019 UofA open house.

## Use
1. Generate markers or use the ones in `\markers`
2. Capture calibration images and calibrate
3. Use either `trackAruco` for straight image processing or `blockManipulator` to coordinate with a gripper over serial (need Arduino with `main.ino` sketch)
