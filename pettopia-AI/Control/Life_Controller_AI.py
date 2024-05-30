# from ..AI.pet_filter.dog import Dog_Filter
# from ..AI.pet_filter.cat import Cat_Filter
import os
import sys
import uuid
import cv2

sys.path.append('pettopia-AI')
from AI.pet_filter.dog import Dog_Filter
from AI.pet_filter.cat import Cat_Filter


class Life_Controller_AI():

    def __init__(self):
        self.dog_filter = Dog_Filter.Dog_Filter()
        self.cat_filter = Cat_Filter.Cat_Filter()

    def get_cat_filter(self, img, filter_img):
        img_filename = f"uploaded_{uuid.uuid4()}.jpg"

        path = 'AI/pet_filter/cat/image/cat_img'
        img_path = os.path.join(path, img_filename)
        try:
            # 이미지 저장
            cv2.imwrite(img_path, img)
            print("Save success")
        except Exception as e:
            print("Error during image save:", e)

        self.cat_filter.img_read(img_path)
        de = self.cat_filter.detector_face()
        lm = self.cat_filter.detector_landmarks(de)
        self.cat_filter.dog_filter(filter_img, lm)

        return self.cat_filter.img_result

    def get_dog_filter(self, img, filter_horns, filter_nose):
        img_filename = f"uploaded_{uuid.uuid4()}.jpg"

        path = 'AI/pet_filter/dog/image/dog_img'
        img_path = os.path.join(path, img_filename)
        try:
            cv2.imwrite(img_path, img)
            print("Save success")
        except Exception as e:
            # 예외가 발생할 경우
            print("Error during image save:", e)

        self.dog_filter.img_read(img_path)
        self.dog_filter.detector_face()
        self.dog_filter.detector_landmarks()
        self.dog_filter.dog_filter(filter_horns, filter_nose)

        return self.dog_filter.img_result

# c = Life_Controller_AI()
# s = 'dog1.jpg'
# v = 'horns2.png'
# b = 'nose.png'

# c.get_dog_filter(s, v, b)
