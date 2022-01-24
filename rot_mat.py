import numpy as np
import math

# https://learnopencv.com/rotation-matrix-to-euler-angles/
# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :

    assert(isRotationMatrix(R))

    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])

    singular = sy < 1e-6

    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        # z = math.atan2(R[2,1], -R[1,1])
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return np.array([x, y, z])


"""
https://stackoverflow.com/questions/15022630/how-to-calculate-the-angle-from-rotation-matrix
Illustration of the rotation matrix / sometimes called 'orientation' matrix
R = [ 
       R[0, 0] , R[0, 1] , R[0, 2], 
       R[1, 0] , R22 , R23,
       R[2,0] , R[2, 1] , R[2, 2]  
    ]

REMARKS: 
1. this implementation is meant to make the mathematics easy to be deciphered
from the script, not so much on 'optimized' code. 
You can then optimize it to your own style. 

2. I have utilized naval rigid body terminology here whereby; 
2.1 roll -> rotation about x-axis 
2.2 pitch -> rotation about the y-axis 
2.3 yaw -> rotation about the z-axis (this is pointing 'upwards') 
"""
from math import (
    asin, pi, atan2, cos 
)

def eul_deg(R):
    if R[2,0] != 1 and R[2,0] != -1: 
        pitch_1 = -1*asin(R[2,0])
        pitch_2 = pi - pitch_1 
        roll_1 = atan2( R[2, 1] / cos(pitch_1) , R[2, 2] /cos(pitch_1) ) 
        roll_2 = atan2( R[2, 1] / cos(pitch_2) , R[2, 2] /cos(pitch_2) ) 
        yaw_1 = atan2( R[1, 0] / cos(pitch_1) , R[0, 0] / cos(pitch_1) )
        yaw_2 = atan2( R[1, 0] / cos(pitch_2) , R[0, 0] / cos(pitch_2) ) 

        # IMPORTANT NOTE here, there is more than one solution but we choose the first for this case for simplicity !
        # You can insert your own domain logic here on how to handle both solutions appropriately (see the reference publication link for more info). 
        pitch = pitch_1 
        roll = roll_1
        yaw = yaw_1 
    else: 
        yaw = 0 # anything (we default this to zero)
        if R[2,0] == -1: 
            pitch = pi/2 
            roll = yaw + atan2(R[0, 1],R[0, 2]) 
        else: 
            pitch = -pi/2 
            roll = -1*yaw + atan2(-1*R[0, 1],-1*R[0, 2]) 

    # convert from radians to degrees
    roll = roll*180/pi 
    pitch = pitch*180/pi
    yaw = yaw*180/pi 

    rxyz_deg = [roll , pitch , yaw] 
    return rxyz_deg