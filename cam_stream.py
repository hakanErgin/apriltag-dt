import cv2 as cv
import os
# from detection_test.draw_pose_box import draw_axis
from dt_apriltags import Detector
from calibration.calibrate import get_params

display_ip = os.environ.get('DISP')
print(display_ip)

params = get_params()
camera_parameters = ( params[0,0], params[1,1], params[0,2], params[1,2] )
print('params', params)

at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
rtsp_stream = "rtsp://" + display_ip + ":8554/cam"
print(rtsp_stream)
cap = cv.VideoCapture(rtsp_stream)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    tags = at_detector.detect(gray, estimate_tag_pose=True, camera_params=camera_parameters, tag_size=0.2)

    for tag in tags:
        for idx in range(len(tag.corners)):
            cv.line(frame, tuple(tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))
        # uncomment for draw test
        # draw_axis(frame, tag.pose_R, tag.pose_t, params)
        

    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
