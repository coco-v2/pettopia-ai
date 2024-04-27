#from ..AI.pet_filter.dog import Dog_Filter
#from ..AI.pet_filter.cat import Cat_Filter
import sys
sys.path.append('pettopia-AI')
from AI.pet_filter.dog import Dog_Filter

class Life_Controller_AI():

    def __init__(self):
        self.dog_filter = Dog_Filter.Dog_Filter()
        #self.cat_filter = Cat_Filter.Cat_Filter()

    def get_cat_filter(self, img, filter_img):
        pass

    def get_dog_filter(self, img, filter_horns, filter_nose):
        path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_filter/dog/image/'

        self.dog_filter.img_read(path+'dog_img/'+img)
        self.dog_filter.detector_face()
        self.dog_filter.detector_landmarks()
        self.dog_filter.dog_filter(path+'horns_img/'+filter_horns, path+'nose_img/'+filter_nose)

        return self.dog_filter.img_result

c = Life_Controller_AI()
s = 'dog1.jpg'
v = 'horns2.png'
b = 'nose.png'

c.get_dog_filter(s, v, b)

