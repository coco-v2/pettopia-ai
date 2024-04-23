from abc import ABC, abstractmethod

class Model(ABC):

    @abstractmethod
    def model_test(self):
        pass

    @abstractmethod
    def train_model(self):
        pass

    @abstractmethod
    def preprocess_data(self):
        pass
