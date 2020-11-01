import os
import cv2
import sys
import dlib
import numpy as np
from datetime import datetime

# helper modules
from utils.drawFace import draw
import utils.reference_world as world

class LandmarkDetection:

    def __init__(self):
        
        self.PREDICTOR_PATH = "AnomalyServer\weights\shape_predictor_68_face_landmarks.dat"
        self.left = False
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.PREDICTOR_PATH)
        self.GAZE = 'Face Not Found'
        self.integrity = {
            "face-toggle": []
        }
        return
    
    def run(self, img, result):

        faces = self.detector(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
        face3Dmodel = world.ref3DModel()

        for face in faces:
            shape = self.predictor(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), face)
            draw(img, shape)
            refImgPts = world.ref2dImagePoints(shape)
            height, width, channels = img.shape
            focalLength = 5 * width
            cameraMatrix = world.cameraMatrix(focalLength, (height / 2, width / 2))
            mdists = np.zeros((4, 1), dtype=np.float64)

            # calculate rotation and translation vector using solvePnP
            success, rotationVector, translationVector = cv2.solvePnP(
                face3Dmodel, refImgPts, cameraMatrix, mdists)

            noseEndPoints3D = np.array([[0, 0, 1000.0]], dtype=np.float64)
            noseEndPoint2D, jacobian = cv2.projectPoints(
                noseEndPoints3D, rotationVector, translationVector, cameraMatrix, mdists)

            #  draw nose line
            p1 = (int(refImgPts[0, 0]), int(refImgPts[0, 1]))
            p2 = (int(noseEndPoint2D[0, 0, 0]), int(noseEndPoint2D[0, 0, 1]))
            cv2.line(img, p1, p2, (110, 220, 0),
                     thickness=2, lineType=cv2.LINE_AA)

            # calculating euler angles
            rmat, jac = cv2.Rodrigues(rotationVector)
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
            # print(f"Qx:{Qx}\tQy:{Qy}\tQz:{Qz}\t")
            x = np.arctan2(Qx[2][1], Qx[2][2])
            y = np.arctan2(-Qy[2][0], np.sqrt((Qy[2][1] * Qy[2][1] ) + (Qy[2][2] * Qy[2][2])))
            z = np.arctan2(Qz[0][0], Qz[1][0])
            # print("ThetaX: ", x)
            if angles[1] < -15:
                if(self.left == False):
                    self.integrity['face-toggle'].append(datetime.now())
                    self.left = True
                self.GAZE = "Looking: Left"
            elif angles[1] > 15:
                if(self.left == True):
                    self.integrity['face-toggle'].append(datetime.now())
                    self.left = False
                self.GAZE = "Looking: Right"
            else:
                self.GAZE = "Forward"

        cv2.putText(img, self.GAZE, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 80), 2)
        result.write(img)
        return
    
    def get_integrity(self):
        return self.integrity