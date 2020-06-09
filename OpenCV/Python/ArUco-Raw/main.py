from CalibrateCamera import CalibrateCamera
from Vision import Vision

def main():
    # Set desired parameters
    desiredWidth  = 1280
    desiredHeight = 960
    desiredFPS    = 30

    ################
    # Calibration
    ################
    
    CC = CalibrateCamera()

    # CC.generateCharucoBoard()
    # CC.generateArucoMarker(ID=97, size=100)
    # CC.generateArucoMarker(ID=35, size=300)
    # CC.generateArucoMarker(ID=17, size=700)

    CC.connectCamera(desiredWidth, desiredHeight, desiredFPS)
    CC.captureCalibrationImages()
    # CC.calibrateCamera()
    # CC.getCalibration()
    # print(CC.mtx)
    # print(CC.dist)
    
    ################
    # Testing
    ################
    
    # V = Vision(desiredWidth, desiredHeight, desiredFPS, autoFocus)
    # V.trackAruco()

# Main loop
if __name__ == '__main__':
    main()
