# from ..AI.pet_filter.dog import Dog_Filter
# from ..AI.pet_filter.cat import Cat_Filter
import os
import sys
import uuid
import cv2
import numpy as np

sys.path.append('pettopia-AI')
from AI.pet_filter.dog import Dog_Filter
from AI.pet_filter.cat import Cat_Filter


class Life_Controller_AI():

    def __init__(self):
        print("3.0")
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

            print(filter_img)

            self.cat_filter.img_read(img_path)
            de = self.cat_filter.detector_face()
            lm = self.cat_filter.detector_landmarks(de)
            self.cat_filter.cat_filter(filter_img, lm)

            return self.cat_filter.img_result

        except Exception as e:
            print("Error during image save:", e)

            return None



    def get_dog_filter(self, img, filter_horns, filter_nose):
        img_filename = f"uploaded_{uuid.uuid4()}.jpg"

        path = 'AI/pet_filter/dog/image/dog_img'
        img_path = os.path.join(path, img_filename)
        #image = cv2.imread(img)
        #print("3.4")

        try:
            cv2.imwrite(img_path, img)
            print("Save success")

            self.dog_filter.img_read(img_path)
            self.dog_filter.detector_face()
            self.dog_filter.detector_landmarks()
            self.dog_filter.dog_filter(filter_horns, filter_nose)

            return self.dog_filter.img_result

        except Exception as e:
            print("4-2")
            # 예외가 발생할 경우
            print("Error during image save:", e)

            return None


# c = Life_Controller_AI()
# #
# s = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/dog/image/dog_img/dog1.jpg'
# v = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/dog/image/horns_img/horns2.png'#horns2.png'
# b = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/dog/image/nose_img/nose.png'
#
# c.get_dog_filter(s, v, b)
# c.get_cat_filter(s, v)
