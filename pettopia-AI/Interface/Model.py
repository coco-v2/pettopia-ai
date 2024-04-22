from abc import ABC, abstractmethod

class Model(ABC):

    @abstractmethod
    def model_test(self):
        pass

    @abstractmethod
    def train_model(self):
        pass

    def preprocess_data(self):
        pass
