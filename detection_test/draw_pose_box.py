import numpy as np
import cv2

# not working
def draw_axis(img, rotation_vec, t, K, scale=0.2, dist=None):
    """
    Draw a 6dof axis (XYZ -> RGB) in the given rotation and translation
    :param img - rgb numpy array
    :rotation_vec - euler rotations, numpy array of length 3,
    use cv2.Rodrigues(R)[0] to convert from rotation matrix
    :t - 3d translation vector, in meters (dtype must be float)
    :K - intrinsic calibration matrix , 3x3
    :scale - factor to control the axis lengths
    :dist - optional distortion coefficients, numpy array of length 4. If None distortion is ignored.
    """
    img = img.astype(np.float32)
    dist = np.zeros(4, dtype=float) if dist is None else dist
    points = scale * np.float32([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]).reshape(-1, 3)
    axis_points, _ = cv2.projectPoints(points, cv2.Rodrigues(rotation_vec)[0], t, K, dist)
    # print(type(t[0][0]))
    # print(t)
    # print(type(axis_points[0][0]))
    print(axis_points[0][0])
    print(type(tuple(axis_points[0].ravel())))
    img = cv2.line(img, tuple(axis_points[3].ravel()), tuple(axis_points[0].ravel()), (255, 0, 0), 3)
    img = cv2.line(img, tuple(axis_points[3].ravel()), tuple(axis_points[1].ravel()), (0, 255, 0), 3)
    img = cv2.line(img, tuple(axis_points[3].ravel()), tuple(axis_points[2].ravel()), (0, 0, 255), 3)


# Detection object:
# tag_family = b'tag36h11'
# tag_id = 2
# hamming = 0
# decision_margin = 22.096973419189453
# homography = [[ 9.76114686e+01 -1.27009410e+01  3.60749961e+02]
#  [ 7.47323395e+00  8.18810531e+01  2.66440090e+02]
#  [ 1.79935862e-02 -3.45950810e-02  1.00000000e+00]]
# center = [360.74996132 266.44009048]
# corners = [[264.33877563 359.76760864]
#  [453.184021   361.80081177]
#  [447.52749634 182.43809509]
#  [271.33486938 174.19392395]]
# pose_R = [[ 2.13228050e-01 -4.43808351e-04 -9.77002355e-01]
#  [ 1.75276706e-02  9.99840695e-01  3.37118264e-03]
#  [ 9.76845218e-01 -1.78434062e-02  2.13201861e-01]]
# pose_t = [[-0.06467931]
#  [-0.05606699]
#  [ 5.13034643]]
# pose_err = 2.548827680031747e-06

# problem with z axis
def _draw_pose(overlay, camera_params, tag_size, rvec, tvec, z_sign=1):
    opoints = np.array([
        -2, -2, 0,
        2, -2, 0,
        2, 2, 0,
        2, -2, -4 * z_sign,
    ]).reshape(-1, 1, 3) * 0.5 * tag_size

    fx, fy, cx, cy = camera_params

    K = np.array([fx, 0, cx, 0, fy, cy, 0, 0, 1]).reshape(3, 3)

    rvec, _ = cv2.Rodrigues(rvec)
    # tvec = pose[:3, 3]

    dcoeffs = np.zeros(5)

    ipoints, _ = cv2.projectPoints(opoints, rvec, tvec, K, dcoeffs)

    ipoints = np.round(ipoints).astype(int)

    ipoints = [tuple(pt) for pt in ipoints.reshape(-1, 2)]

    cv2.line(overlay, ipoints[0], ipoints[1], (0,0,255), 2)
    cv2.line(overlay, ipoints[1], ipoints[2], (0,255,0), 2)
    cv2.line(overlay, ipoints[1], ipoints[3], (255,0,0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(overlay, 'X', ipoints[0], font, 0.5, (0,0,255), 2, cv2.LINE_AA)
    cv2.putText(overlay, 'Y', ipoints[2], font, 0.5, (0,255,0), 2, cv2.LINE_AA)
    cv2.putText(overlay, 'Z', ipoints[3], font, 0.5, (255,0,0), 2, cv2.LINE_AA)

def _draw_cube(overlay, camera_params, tag_size, rvec, tvec, centroid, z_sign=1):

    opoints = np.array([
        -10, -8, 0,
        10, -8, 0,
        10, 8, 0,
        -10, 8, 0,
        -10, -8, 2 * z_sign,
        10, -8, 2 * z_sign,
        10, 8, 2 * z_sign,
        -10, 8, 2 * z_sign,
    ]).reshape(-1, 1, 3) * 0.5 * tag_size

    edges = np.array([
        0, 1,
        1, 2,
        2, 3,
        3, 0,
        0, 4,
        1, 5,
        2, 6,
        3, 7,
        4, 5,
        5, 6,
        6, 7,
        7, 4
    ]).reshape(-1, 2)

    fx, fy, cx, cy = camera_params

    K = np.array([fx, 0, cx, 0, fy, cy, 0, 0, 1]).reshape(3, 3)

    rvec, _ = cv2.Rodrigues(rvec)
    # tvec = pose[:3, 3]

    dcoeffs = np.zeros(5)

    ipoints, _ = cv2.projectPoints(opoints, rvec, tvec, K, dcoeffs)

    ipoints = np.round(ipoints).astype(int)

    ipoints = [tuple(pt) for pt in ipoints.reshape(-1, 2)]

    for i, j in edges:
        cv2.line(overlay, ipoints[i], ipoints[j], (0, 255, 0), 1, 16)