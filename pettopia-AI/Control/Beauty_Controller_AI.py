# from ..AI.pet_filter.dog import Dog_Filter
# from ..AI.pet_filter.cat import Cat_Filter
import os
import sys
import uuid
import cv2

sys.path.append('pettopia-AI')
from AI.pet_color.Model.Pet_Color_Model import Pet_Color_Model

class Beauty_Controller_AI():

    def __init__(self):
        self.pet_color = Pet_Color_Model()

    def get_pet_color(self, img):
        img_filename = f"uploaded_{uuid.uuid4()}.jpg"

        path = 'AI/pet_color/data'
        img_path = os.path.join(path, img_filename)
        try:
            cv2.imwrite(img_path, img)
            print("Save success")
        except Exception as e:
            # 예외가 발생할 경우
            print("Error during image save:", e)

        result = self.pet_color.process_data(img_path)

        return result