import sys

from keras import Model
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten

sys.path.append('pettopia-AI')
from Interface import Model as myModel
from AI.pet_disease.Preprocessing.Preprocess_Pet_Disease_Data import Preprocess_Pet_Disease_Data

import numpy as np

class Pet_Skin_Disease_Model(myModel.Model):

    def __init__(self):
        super.__init__()
        self.pet_skin = Preprocess_Pet_Disease_Data()

    def model_test(self):
        pass

    def train_model(self):
        output_size = 6
        img_size = 224

        data_paths = ['pettopia-AI/AI/pet_skin_disease/data/dataset/A1.npy',
                      'pettopia-AI/AI/pet_skin_disease/data/dataset/A2.npy',
                      'pettopia-AI/AI/pet_skin_disease/data/dataset/A3.npy',
                      'pettopia-AI/AI/pet_skin_disease/data/dataset/A4.npy',
                      'pettopia-AI/AI/pet_skin_disease/data/dataset/A5.npy',
                      'pettopia-AI/AI/pet_skin_disease/data/dataset/A6.npy']

        x_train, y_train = [], []
        for path in data_paths:
            data = np.load(path, allow_pickle=True).item()
            imgs = data.get('imgs')
            labels = data.get('labels')

            x_train.extend(imgs)
            y_train.extend(labels)

        x_train = np.array(x_train).astype('float32') / 255
        y_train = np.array(y_train).astype('float32')

        x_train = np.reshape(x_train, (-1, img_size, img_size, 3))
        y_train = np.reshape(y_train, (-1, output_size))

        # 모델 구성
        input_layer = Input(shape=(img_size, img_size, 3))
        conv1 = Conv2D(32, (3, 3), activation='relu')(input_layer)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
        conv2 = Conv2D(64, (3, 3), activation='relu')(pool1)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
        conv3 = Conv2D(128, (3, 3), activation='relu')(pool2)
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
        flatten = Flatten()(pool3)
        dense1 = Dense(256, activation='relu')(flatten)
        dense2 = Dense(output_size, activation='softmax')(dense1)

        model = Model(inputs=input_layer, outputs=dense2)

        # 모델 컴파일
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        # 모델 훈련
        model.fit(x_train, y_train, epochs=10, validation_split=0.2)

        # 모델 저장
        model.save('pettopia-AI/AI/pet_skin_disease/model/pet_skin_disease_model.h5')

    def preprocess_data(self, dir_name):
        self.pet_face.load_cat_data(dir_name)

test = Pet_Skin_Disease_Model()
# test.preprocess_data('CAT_00')
# test.preprocess_data('CAT_01')
# test.preprocess_data('CAT_02')
# test.preprocess_data('CAT_03')
# test.preprocess_data('CAT_04')
# test.preprocess_data('CAT_05')
# test.preprocess_data('CAT_06')
test.train_model()