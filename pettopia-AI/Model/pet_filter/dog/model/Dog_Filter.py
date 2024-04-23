import dlib, cv2, os
from imutils import face_utils
from math import atan2, degrees
pwd = os.path.dirname(__file__)
import matplotlib.pyplot as plt
import numpy as np

# conda install -c conda-forge dlib
# conda install -c conda-forge/label/cf201901 dlib
# conda install -c conda-forge/label/cf202003 dlib

class Dog_Filter_AI():

    def __init__(self):
        self.detector = dlib.cnn_face_detection_model_v1(pwd+'/dogHeadDetector.dat')
        self.predictor = dlib.shape_predictor(pwd+'/landmarkDetector.dat')
        self.img = None
        self.img_result = None
        self.dets = None
        self.faces = None
        self.shapes = []
        self.shape = None

    def img_read(self, img_path):
        img = cv2.imread(img_path)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img = cv2.resize(img, dsize=None, fx=0.2, fy=0.2)

    def img_show_result(self, img):
        cv2.imshow("image", img)
        cv2.waitKey(0)

    def detector_face(self):
        #객체 탐지기 사용
        self.dets = self.detector(self.img, upsample_num_times=1)

        img_result = self.img.copy()

        for i, d in enumerate(self.dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(i, d.rect.left(),
                                                                                              d.rect.top(),
                                                                                              d.rect.right(),
                                                                                              d.rect.bottom(),
                                                                                              d.confidence))

            x1, y1 = d.rect.left(), d.rect.top()
            x2, y2 = d.rect.right(), d.rect.bottom()

            #cv2.rectangle(img_result, pt1=(x1, y1), pt2=(x2, y2), thickness=2, color=(255, 0, 0), lineType=cv2.LINE_AA)

        self.img_result = img_result

    def detector_landmarks(self):

        for i, d in enumerate(self.dets):
            self.shape = self.predictor(self.img, d.rect)
            self.shape = face_utils.shape_to_np(self.shape)

            for i, p in enumerate(self.shape):
                self.shapes.append(self.shape)
                cv2.circle(self.img_result, center=tuple(p), radius=3, color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_AA)
                cv2.putText(self.img_result, str(i), tuple(p), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
                            cv2.LINE_AA)

    def dog_filter(self, filter_head, filter_nose):

        img_result2 = self.img.copy()

        horns = cv2.imread(filter_head, cv2.IMREAD_UNCHANGED)
        horns_h, horns_w = horns.shape[:2]

        nose = cv2.imread(filter_nose, cv2.IMREAD_UNCHANGED)

        for shape in self.shapes:
            horns_center = np.mean([shape[4], shape[1]], axis=0) // [1, 1.05]
            horns_size = np.linalg.norm(shape[4] - shape[1]) * 2

            nose_center = shape[3]
            nose_size = horns_size // 4

            angle = -self.angle_between(shape[4], shape[1])
            M = cv2.getRotationMatrix2D((horns_w, horns_h), angle, 1)
            rotated_horns = cv2.warpAffine(horns, M, (horns_w, horns_h))

            img_result2 = self.overlay_transparent(img_result2, nose, nose_center[0], nose_center[1],
                                              overlay_size=(int(nose_size), int(nose_size)))
            try:
                img_result2 = self.overlay_transparent(img_result2, rotated_horns, horns_center[0], horns_center[1],
                                                  overlay_size=(int(horns_size), int(horns_h * horns_size / horns_w)))
            except:
                print('failed overlay image')

        filename = "petopia-AI/img"
        ext = "myPet"

        #img_out2 = cv2.cvtColor(img_result2, cv2.COLOR_RGB2BGR)
        #cv2.imwrite('img/%s_out2%s' % (filename, ext), img_result2)

        self.img_result = img_result2

    def overlay_transparent(self, background_img, img_to_overlay_t, x, y, overlay_size=None):
        img_to_overlay_t = cv2.cvtColor(img_to_overlay_t, cv2.COLOR_BGRA2RGBA)
        bg_img = background_img
        # convert 3 channels to 4 channels
        if bg_img.shape[2] == 3:
            bg_img = cv2.cvtColor(bg_img, cv2.COLOR_RGB2RGBA)

        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

        b, g, r, a = cv2.split(img_to_overlay_t)

        mask = cv2.medianBlur(a, 5)

        h, w, _ = img_to_overlay_t.shape
        roi = bg_img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)]

        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(img_to_overlay_t, img_to_overlay_t, mask=mask)

        bg_img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)] = cv2.add(img1_bg, img2_fg)

        # convert 4 channels to 4 channels
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_RGBA2RGB)

        return bg_img

    def angle_between(self,p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]

        return degrees(atan2(yDiff, xDiff))

# mypath = '../image/dog1.jpg'
# c = Dog_Filter_AI()
# c.img_read(mypath)
# c.detector_face()
# c.detector_landmarks()
# c.dog_filter("d")
# c.img_show_result(c.img_result)


