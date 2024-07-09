import cv2
import datetime
import numpy as np
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import load_model
from math import atan2, degrees


class Cat_Filter():
    def __init__(self):
        detector_model_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/cat/model/cat_detector_model.h5'
        predictor_model_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/cat/model/cat_landmark_model1.h5'

        # 모델 로드
        self.__detector = load_model(detector_model_path, custom_objects={'BatchNormalization': BatchNormalization},
                                     compile=False)
        self.__predictor = load_model(predictor_model_path, custom_objects={'BatchNormalization': BatchNormalization},
                                      compile=False)
        self.img = None
        self.img_result = None
        self.file_result = None
        self.img_size = 224
        self.old_size = None
        self.ratio_w = None
        self.ratio_h = None

    def img_read(self, img_path):
        self.img = cv2.imread(img_path)
        self.img = cv2.resize(self.img, self.img.shape[:2])
        self.img_result = self.img.copy()
        print("1")

        original_height, original_width = self.img.shape[:2]
        print("2")

        self.ratio_w = original_width / self.img_size
        self.ratio_h = original_height / self.img_size
        print("3")

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
        print("4")
        self.img, ratio, top, left = self.resize_img(self.img)
        print("5")
        inputs = (self.img.astype('float32') / 255).reshape((1, self.img_size, self.img_size, 3))
        pred_bb = self.__detector.predict(inputs)[0].reshape((-1, 2))

        ori_bb = ((pred_bb - np.array([left, top])) / ratio).astype(np.int32)
        return ori_bb

    def detector_landmarks(self, ori_bb):
        print("6")
        center = np.mean(ori_bb, axis=0)
        print("6.1")
        face_size = max(np.abs(ori_bb[1] - ori_bb[0]))
        print("6.2")
        new_bb = np.array([
            center - face_size * 0.6,
            center + face_size * 0.6
        ])
        print("6.3")
        new_bb = np.clip(new_bb, 0, 99999)
        print("6.4")
        face_img = self.img[int(new_bb[0][1]):int(new_bb[1][1]), int(new_bb[0][0]):int(new_bb[1][0])]
        print("6.5")
        face_img, face_ratio, face_top, face_left = self.resize_img(face_img)
        print("6.6")
        face_inputs = (face_img.astype('float32') / 255).reshape((1, self.img_size, self.img_size, 3))
        print("6.7")
        pred_lmks = self.__predictor.predict(face_inputs)[0].reshape((-1, 2))
        print("6.8")
        new_lmks = ((pred_lmks - np.array([face_left, face_top])) / face_ratio).astype(np.int32)
        print("6.9")
        ori_lmks = new_lmks + new_bb[0]

        print("7")

        return ori_lmks

    def cat_filter(self, filter, ori_lmks):
        glasses = cv2.imread(filter, cv2.IMREAD_UNCHANGED)

        print(self.ratio_w, self.ratio_h)
        glasses_center = np.mean([ori_lmks[0] , ori_lmks[1]], axis=0).astype(int) * self.ratio_h
        glasses_size = np.linalg.norm(ori_lmks[0] - ori_lmks[1]) * self.ratio_w * self.ratio_w


        angle = -self.angle_between(ori_lmks[0], ori_lmks[1])
        M = cv2.getRotationMatrix2D((glasses.shape[1] / 2, glasses.shape[0] / 2), angle, 1)
        rotated_glasses = cv2.warpAffine(glasses, M, (glasses.shape[1], glasses.shape[0]))

        try:
            result_img = self.overlay_transparent(self.img_result, rotated_glasses, glasses_center[0],
                                                  glasses_center[1],
                                                  overlay_size=(int(glasses_size), int(
                                                      glasses.shape[0] * glasses_size / glasses.shape[1])))
        except Exception as e:
            print(f'Failed to overlay image: {e}')
            result_img = self.img_result

        current_datetime = datetime.datetime.now()
        filename = current_datetime.strftime("%Y%m%d_%H%M%S")

        image_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/cat/image/res_img/' + filename + '.jpg'

        if not cv2.imwrite(image_path, cv2.cvtColor(result_img, cv2.COLOR_BGRA2BGR)):
            print("사진 저장 실패")
        else:
            print(f"사진 저장 성공: {image_path}")

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

        # Ensure x and y are valid
        x, y = int(x), int(y)
        x1, y1 = max(0, x - w // 2), max(0, y - h // 2)
        x2, y2 = min(bg_img.shape[1], x + w // 2), min(bg_img.shape[0], y + h // 2)

        # Ensure roi dimensions match
        roi = bg_img[y1:y2, x1:x2]
        if roi.shape[0] != h or roi.shape[1] != w:
            overlay_img_resized = cv2.resize(img_to_overlay_t, (roi.shape[1], roi.shape[0]))
            mask_resized = cv2.resize(mask, (roi.shape[1], roi.shape[0]))
        else:
            overlay_img_resized = img_to_overlay_t
            mask_resized = mask

        img1_bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask_resized))
        img2_fg = cv2.bitwise_and(overlay_img_resized, overlay_img_resized, mask=mask_resized)

        bg_img[y1:y2, x1:x2] = cv2.add(img1_bg, img2_fg)

        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2BGR)

        return bg_img

    def angle_between(self, p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]

        return degrees(atan2(yDiff, xDiff))


# mypath = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/cat/image/cat_img/leo.jpg'
# filter_p = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/cat/image/filter_img/glasses.png'
# test = Cat_Filter()
# test.img_read(mypath)
# d = test.detector_face()
# lm = test.detector_landmarks(d)
# test.cat_filter(filter_p, lm)
# test.img_show_result(test.img_result)
