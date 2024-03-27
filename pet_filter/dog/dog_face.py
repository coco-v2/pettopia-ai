import dlib, cv2, os
import imutils2
import numpy as np
import matplotlib.pyplot as plt

class dog_face_detector():

    def __init__(self):
        detector = dlib.cnn_face_detection_model_v1('model/dogHeadDetector.dat')
        predictor = dlib.shape_predictor('../../landmarkDetector.dat')
        img = '../../dog1.jpg'

    def img_read(self, img_path):
        img_path = 'image/dog1.jpg'
        img = cv2.imread(img_path)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img = cv2.resize(img, dsize=None, fx=0.2, fy=0.2)

    def img_show(self):
        cv2.imshow("image", self.img)
        cv2.waitKey(0)

    def detector_face(self):
        dets = self.detector(self.img, upsample_num_times=1) #객체 탐지기 사용

