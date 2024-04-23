from ....Interface import Model
from Preprocessing.Preprocess_Pet_Face_Data import Preprocess_Pet_Face_Data

class Pet_Face_Detector_Model(Model.Model):

    def __init__(self):
        self.pet_face = Preprocess_Pet_Face_Data()

    def model_test(self):
        pass

    def train_model(self):
        pass

    def preprocess_data(self):
        pass