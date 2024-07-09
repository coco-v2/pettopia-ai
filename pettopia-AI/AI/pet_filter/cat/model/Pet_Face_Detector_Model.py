import sys

sys.path.append('pettopia-AI')
from Interface import Model as myModel
from AI.pet_filter.cat.Preprocessing.Preprocess_Pet_Face_Data import Preprocess_Pet_Face_Data
import datetime
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, BatchNormalization, Dropout

import numpy as np

class Pet_Face_Detector_Model(myModel.Model):

    def __init__(self):
        super.__init__()
        self.pet_face = Preprocess_Pet_Face_Data()

    def model_test(self):
        pass

    def train_model(self):
        x_train, y_train = self.pet_face.process_img()

        # 모델 구성
        model = Sequential()
        model.add(Conv2D(input_shape=(224, 224, 3), filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Conv2D(filters=128, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(Conv2D(filters=128, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Conv2D(filters=256, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(Conv2D(filters=256, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(Conv2D(filters=256, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Flatten())
        model.add(BatchNormalization())
        model.add(Dense(units=4096, activation="relu"))
        model.add(Dropout(0.5))
        model.add(BatchNormalization())
        model.add(Dense(units=4096, activation="relu"))
        model.add(Dropout(0.5))
        model.add(BatchNormalization())
        model.add(Dense(units=1000, activation="relu"))
        model.add(Dropout(0.5))
        model.add(BatchNormalization())
        model.add(Dense(units=4, activation="linear"))

        print("train")
        # 모델 컴파일 및 훈련
        model.summary()
        model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

        x = np.reshape(x_train, (-1, 224, 224, 3))
        # 데이터를 x와 y로 수정 후 모델 학습
        model.fit(x_train, y_train, batch_size=64, epochs=12, verbose=1, validation_split=0.2, shuffle=True)

        model.save('cat_detector_model.h5')

    def preprocess_data(self, dir_name):
        self.pet_face.load_cat_data(dir_name)

#test = Pet_Face_Detector_Model()
# test.preprocess_data('CAT_00')
# test.preprocess_data('CAT_01')
# test.preprocess_data('CAT_02')
# test.preprocess_data('CAT_03')
# test.preprocess_data('CAT_04')
# test.preprocess_data('CAT_05')
# test.preprocess_data('CAT_06')
#test.train_model()