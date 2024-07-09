import sys

sys.path.append('pettopia-AI')
from Interface import Model as myModel
from AI.pet_filter.cat.Preprocessing.Preprocess_Pet_Face_Data import Preprocess_Pet_Face_Data

from keras.layers import Input, Dense
from keras.applications import mobilenet_v2
import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, BatchNormalization, Dropout

class Pet_Landmark_Detector_Model(myModel.Model):
    def __init__(self):
        self.pet_face = Preprocess_Pet_Face_Data()

    def model_test(self):
        pass

    def train_model(self):

        img_size = 224

        mode = 'lmks' #[bbs, lmks]
        if mode == 'bbs':
            output_size = 4
        elif mode == 'lmks':
            output_size = 18

            # 데이터 로드 및 전처리
        data_paths = ['CAT_00.npy', 'CAT_01.npy', 'CAT_02.npy', 'CAT_03.npy', 'CAT_04.npy', 'CAT_05.npy', 'CAT_06.npy']

        x_train, y_train, x_test, y_test = [], [], [], []
        for i, path in enumerate(data_paths):
            data = np.load(path, allow_pickle=True)
            imgs = data.item().get('imgs')
            labels = data.item().get(mode)

            x_train.append(imgs)
            y_train.append(labels)

        x_train = np.concatenate(x_train).astype('float32') / 255
        y_train = np.concatenate(y_train).astype('float32')

        x_train = np.reshape(x_train, (-1, img_size, img_size, 3))
        y_train = np.reshape(y_train, (-1, output_size))

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
        model.add(Dense(units=18, activation="linear"))


        model.summary()
        model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

        x = np.reshape(x_train, (-1, 224, 224, 3))

        model.fit(x_train, y_train, batch_size=64, epochs=12, verbose=1, validation_split=0.2, shuffle=True)

        model.save('cat_landmark_detector_model.h5')

test = Pet_Landmark_Detector_Model()
test.train_model()