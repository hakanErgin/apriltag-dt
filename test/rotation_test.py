from dt_apriltags import Detector
import numpy
import os

test_images_path = 'test_files'

visualization = True
try:
    import cv2
except:
    raise Exception('You need cv2 in order to run the demo. However, you can still use the library without it.')

try:
    from cv2 import imshow
except:
    print("The function imshow was not implemented in this installation. Rebuild OpenCV from source to use it")
    print("VIsualization will be disabled.")
    visualization = False

try:
    import yaml
except:
    raise Exception('You need yaml in order to run the tests. However, you can still use the library without it.')

at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

with open(test_images_path + '/test_info.yaml', 'r') as stream:
    parameters = yaml.load(stream)

#### test WITH THE ROTATION IMAGES ####

import time

print("\n\nTESTING WITH ROTATION IMAGES")

time_num = 0
time_sum = 0

test_images_path = 'test_files'
image_names = parameters['rotation_test']['files']

for image_name in image_names:
    print("Testing image ", image_name)
    ab_path = test_images_path + '/' + image_name
    if(not os.path.isfile(ab_path)):
        continue
    groundtruth = float(image_name.split('_')[-1].split('.')[0])  # name of test_files image should be set to its groundtruth

    parameters['rotation_test']['rotz'] = groundtruth
    cameraMatrix = numpy.array(parameters['rotation_test']['K']).reshape((3,3))
    camera_params = ( cameraMatrix[0,0], cameraMatrix[1,1], cameraMatrix[0,2], cameraMatrix[1,2] )

    img = cv2.imread(ab_path, cv2.IMREAD_GRAYSCALE)

    start = time.time()
    tags = at_detector.detect(img, True, camera_params, parameters['rotation_test']['tag_size'])

    time_sum+=time.time()-start
    time_num+=1

    print(tags[0].pose_t, parameters['rotation_test']['posx'], parameters['rotation_test']['posy'], parameters['rotation_test']['posz'])
    print(tags[0].pose_R, parameters['rotation_test']['rotx'], parameters['rotation_test']['roty'], parameters['rotation_test']['rotz'])

print("AVG time per detection: ", time_sum/time_num)

