# from ..AI.pet_filter.dog import Dog_Filter
# from ..AI.pet_filter.cat import Cat_Filter
import os
import sys
import uuid
import cv2

sys.path.append('pettopia-AI')
from AI.pet_filter.dog import Dog_Filter


class Life_Controller_AI():

    def __init__(self):
        self.dog_filter = Dog_Filter.Dog_Filter()
        # self.cat_filter = Cat_Filter.Cat_Filter()

    def get_cat_filter(self, img, filter_img):
        pass

    def get_dog_filter(self, img, filter_horns, filter_nose):
        img_filename = f"uploaded_{uuid.uuid4()}.jpg"
        print(img_filename)
        path = 'C:/pettopia_AI/petFilter_AI/pettopia-ai/pettopia-AI/AI/pet_filter/dog/image/'
        img_path = os.path.join(path, img_filename)
        try:
            # 이미지 저장
            cv2.imwrite(img_path, img)  # OpenCV를 사용하여 저장
            print("Save success")
        except Exception as e:
            # 예외가 발생할 경우
            print("Error during image save:", e)  # 에러 메시지 출력

        self.dog_filter.img_read(img_path)
        print("1")
        self.dog_filter.detector_face()
        print("2")
        self.dog_filter.detector_landmarks()
        print("3")
        self.dog_filter.dog_filter(path + 'horns_img/' + filter_horns, path + 'nose_img/' + filter_nose)

        print(4)

        return self.dog_filter.img_result

# c = Life_Controller_AI()
# s = 'dog1.jpg'
# v = 'horns2.png'
# b = 'nose.png'

# c.get_dog_filter(s, v, b)
