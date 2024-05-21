import cv2, os, datetime,sys
sys.path.append('pettopia-AI')
from math import atan2, degrees
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.models import load_model

class Cat_Filter():
    def __init__(self):

        detector_model_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/cat/cat_detector_model.h5'
        predictor_model_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/cat/cat_landmark_detector_model.h5'

        # 모델 로드
        self.__detector = load_model(detector_model_path)
        self.__predictor = load_model(predictor_model_path)
        self.img = None
        self.img_result = None
        self.file_result = None
        self.img_size = 224

    def img_read(self, img_path):
        print(img_path)
        img = cv2.imread(img_path)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img = cv2.resize(img, dsize=None, fx=0.2, fy=0.2)

    def img_show_result(self, img):
        cv2.imshow("image", img)
        cv2.waitKey(0)

    def resize_img(self, img):
        old_size = img.shape[:2]  # old_size is in (height, width) format
        ratio = float(self.img_size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        # new_size should be in (width, height) format
        im = cv2.resize(img, (new_size[1], new_size[0]))
        delta_w = self.img_size - new_size[1]
        delta_h = self.img_size - new_size[0]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)
        new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                    value=[0, 0, 0])
        return new_im, ratio, top, left

    def detector_face(self):

        self.img_result, ratio, top, left = self.resize_img(self.img)
        inputs = (self.img_result.astype('float32') / 255).reshape((1, self.img_size, self.img_size, 3))
        pred_bb = self.__detector.predict(inputs)[0].reshape((-1, 2))

        ori_bb = ((pred_bb - np.array([left, top])) / ratio).astype(np.int32)

        return ori_bb

    def detector_landmarks(self, ori_bb):
        center = np.mean(ori_bb, axis=0)
        face_size = max(np.abs(ori_bb[1] - ori_bb[0]))
        new_bb = np.array([
            center - face_size * 0.6,
            center + face_size * 0.6
        ])
        new_bb = np.clip(new_bb, 0, 99999)

        # 랜드마크 예측
        face_img = self.img_result[new_bb[0][1]:new_bb[1][1], new_bb[0][0]:new_bb[1][0]]

        face_img, face_ratio, face_top, face_left = self.resize_img(face_img)

        face_inputs = (face_img.astype('float32') / 255).reshape((1, self.img_size, self.img_size, 3))

        pred_lmks = self.__predictor.predict(face_inputs)[0].reshape((-1, 2))

        # 원래 이미지에서 랜드마크 계산
        new_lmks = ((pred_lmks - np.array([face_left, face_top])) / face_ratio).astype(np.int)
        ori_lmks = new_lmks + new_bb[0]

        return ori_lmks

    def cat_filter(self, filter, ori_lmks):
        glasses = cv2.imread(filter, cv2.IMREAD_UNCHANGED)

        img_result2 = self.img.copy()
        glasses_center = np.mean([ori_lmks[0], ori_lmks[1]], axis=0)
        glasses_size = np.linalg.norm(ori_lmks[0] - ori_lmks[1]) * 2

        angle = -self.angle_between(ori_lmks[0], ori_lmks[1])
        M = cv2.getRotationMatrix2D((glasses_center.shape[1] / 2, glasses.shape[0] / 2), angle, 1)
        rotated_glasses = cv2.warpAffine(glasses, M, (glasses.shape[1], glasses.shape[0]))

        try:
            result_img = self.overlay_transparent(self.img, rotated_glasses, glasses_center[0], glasses_center[1],
                                             overlay_size=(int(glasses_size),
                                                           int(glasses.shape[0] * glasses_size / glasses.shape[1])))
        except:
            print('failed overlay image')

        current_datetime = datetime.datetime.now()

        filename = current_datetime.strftime("%Y%m%d_%H%M%S")  # 예: 20220425_164230

        image_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/cat/image/res_img/' + filename + '.jpg'

        # if not cv2.imwrite(image_path, cv2.cvtColor(img_result2, cv2.COLOR_BGRA2BGR)):
        #     print("사진 저장 실패")
        # else:
        #     print(f"사진 저장 성공: {image_path}")

        self.img_result = result_img
        self.file_result = filename

    def overlay_transparent(self, background_img, img_to_overlay_t, x, y, overlay_size=None):
        bg_img = background_img.copy()

        if bg_img.shape[2] == 3:
            bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA)

        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

        b, g, r, a = cv2.split(img_to_overlay_t)

        mask = cv2.medianBlur(a, 5)

        h, w, _ = img_to_overlay_t.shape
        roi = bg_img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)]

        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(img_to_overlay_t, img_to_overlay_t, mask=mask)

        bg_img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)] = cv2.add(img1_bg, img2_fg)

        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2BGR)

        return bg_img
    def angle_between(self,p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]

        return degrees(atan2(yDiff, xDiff))

mypath = 'image/cat.jpg'
test = Cat_Filter()
test.img_read(mypath)
d = test.detector_face()
lm = test.detector_landmarks(d)
test.cat_filter('glasses.png', lm)
test.img_show_result(test.img_result)
# mypath = 'image/dog1.jpg'
# c = Dog_Filter()
# c.img_read(mypath)
# c.detector_face()
# c.detector_landmarks()
# c.dog_filter("image/horns2.png", "image/nose.png")
# c.img_show_result(c.img_result)
