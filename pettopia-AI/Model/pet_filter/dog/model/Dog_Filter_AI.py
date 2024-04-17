import dlib, cv2
from imutils import face_utils
import matplotlib.pyplot as plt

# conda install -c conda-forge dlib
# conda install -c conda-forge/label/cf201901 dlib
# conda install -c conda-forge/label/cf202003 dlib

class Dog_Filter_AI():

    def __init__(self):
        self.detector = dlib.cnn_face_detection_model_v1('dogHeadDetector.dat')
        self.predictor = dlib.shape_predictor('landmarkDetector.dat')
        self.img_result = None
        self.dets = None
        self.faces = None

    def img_read(self, img_path):
        img = cv2.imread(img_path)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img = cv2.resize(img, dsize=None, fx=0.2, fy=0.2)

    def img_show_result(self):
        cv2.imshow("image", self.img)
        cv2.waitKey(0)

    def detector_face(self):
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

            cv2.rectangle(img_result, pt1=(x1, y1), pt2=(x2, y2), thickness=2, color=(255, 0, 0), lineType=cv2.LINE_AA)

        self.img_result = img_result

    def detector_landmarks(self):
        shapes = []

        for i, d in enumerate(self.dets):
            shape = self.predictor(self.img, d.rect)
            shape = face_utils.shape_to_np(shape)

            for i, p in enumerate(shape):
                shapes.append(shape)
                cv2.circle(self.img_result, center=tuple(p), radius=3, color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_AA)
                cv2.putText(self.img_result, str(i), tuple(p), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
                            cv2.LINE_AA)

        cv2.imshow("img",self.img_result)

    #Todo
    def dog_filter(self):
        return 0

# mypath = '../image/dog1.jpg'
# c = Dog_Filter_AI()
# c.img_read(mypath)
# c.img_show_result()
# c.detector_face()
# c.detector_landmarks()
# #c.img_show()


