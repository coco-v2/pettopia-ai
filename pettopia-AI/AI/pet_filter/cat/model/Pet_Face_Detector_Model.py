from .....Interface import Model as myModel
from ..Preprocessing.Preprocess_Pet_Face_Data import Preprocess_Pet_Face_Data
import keras, datetime
import tensorflow as tf
from keras.layers import Input, Dense
from keras.models import Model
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau
from keras.applications import mobilenet_v2
from keras.losses import mean_squared_error
import numpy as np

class Pet_Face_Detector_Model(myModel.Model):

    def __init__(self):
        self.pet_face = Preprocess_Pet_Face_Data()

    def model_test(self):
        pass

    def train_model(self):
        img_size = 224

        mode = 'bbs'  # [bbs, lmks]
        if mode == 'bbs':
            output_size = 4
        elif mode == 'lmks':
            output_size = 18

        start_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        #
        # data_00 = np.load('data/archive/CAT_00.npy')
        data_01 = np.load('data/archive/CAT_01.npy')
        data_02 = np.load('data/archive/CAT_02.npy')
        data_03 = np.load('data/archive/CAT_03.npy')
        data_04 = np.load('data/archive/CAT_04.npy')
        data_05 = np.load('data/archive/CAT_05.npy')
        data_06 = np.load('data/archive/CAT_06.npy')

        x_train = np.concatenate((data_00.item().get('imgs'), data_01.item().get('imgs'), data_02.item().get('imgs'),
                                  data_03.item().get('imgs'), data_04.item().get('imgs'), data_05.item().get('imgs'),
                                  data_06.item().get('imgs')))
        y_train = np.concatenate((data_00.item().get(mode), data_01.item().get(mode), data_02.item().get(mode),
                                  data_03.item().get(mode), data_04.item().get(mode), data_05.item().get(mode),
                                  data_06.item().get(mode)))

        x_test = np.array(data_06.item().get('imgs'))
        y_test = np.array(data_06.item().get(mode))

        x_train = x_train.astype('float32') / 255
        x_test = x_test.astype('float32') / 255
        x_train = np.reshape(x_train, (-1, img_size, img_size, 3))
        x_test = np.reshape(x_test, (-1, img_size, img_size, 3))

        y_train = np.reshape(y_train, (-1, output_size))
        y_test = np.reshape(y_test, (-1, output_size))

        inputs = Input(shape=(img_size, img_size, 3))

        moblienetV2 = mobilenet_v2.MobileNetV2(input_shape=(img_size, img_size, 3), alpha=1.0, depth_multiplier=1,
                                               include_top=False,
                                               weights='imagenet', input_tensor=inputs, pooling='max')

        net = Dense(128, activation='relu')(moblienetV2.layers[-1].output)
        net = Dense(64, activation='relu')(net)
        net = Dense(output_size, activation='linear')(net)

        cat_detector_model = Model(inputs=inputs, outputs=net)

        cat_detector_model.summary()

        # 훈련
        cat_detector_model.compile(optimizer='adam', loss=mean_squared_error)

        cat_detector_model.fit(x_train, y_train, epochs=50, batch_size=32, shuffle=True,
                               validation_data=(x_test, y_test), verbose=1,
                               callbacks=[
                                   TensorBoard(log_dir='log/%s' % (start_time)),
                                   ModelCheckpoint('model/pet_face_detector/%s.h5' % (start_time), monitor='val_loss',
                                                   verbose=1, save_best_only=True, mode='auto'),
                                   ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, verbose=1, mode='auto')
                               ]
                               )

    def preprocess_data(self):
        print("D")
        self.pet_face.load_cat_data()
        print("a")

test = Pet_Face_Detector_Model()
test.preprocess_data()
#test.train_model()