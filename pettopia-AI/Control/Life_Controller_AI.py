#from ..Model.pet_filter.dog import Dog_Filter
#from ..Model.pet_filter.cat import Cat_Filter
import sys
sys.path.append('pettopia-AI')
from Model.pet_filter.dog import Dog_Filter

class Life_Controller_AI():

    def __init__(self):
        self.dog_filter = Dog_Filter.Dog_Filter()
        #self.cat_filter = Cat_Filter.Cat_Filter()

    def get_cat_filter(self, img, filter_img):
        pass

    def get_dog_filter(self, img, filter_horns, filter_nose):
        self.dog_filter.img_read(img)
        self.dog_filter.detector_face()
        self.dog_filter.detector_landmarks()
        self.dog_filter.dog_filter(filter_horns, filter_nose)

        return self.dog_filter.file_result

c = Life_Controller_AI()
c.get_dog_filter("Model/pet_filter/dog/image/dog1.jpg", "Model/pet_filter/dog/image/horns2.png", "Model/pet_filter/dog/image/nose.png")
