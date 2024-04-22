from abc import ABC, abstractmethod


class Preprocess_Data(ABC):

    @abstractmethod
    def resize_img(self):
        pass

    @abstractmethod
    def process_img(self):
        pass
