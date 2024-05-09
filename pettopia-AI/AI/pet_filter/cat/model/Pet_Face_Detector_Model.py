import sys

sys.path.append('pettopia-AI')
from Interface import Model as myModel
from AI.pet_filter.cat.Preprocessing.Preprocess_Pet_Face_Data import Preprocess_Pet_Face_Data
import datetime
from tensorflow.python.keras.layers import Input, Dense
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau
from tensorflow import keras
from tensorflow.python.keras.losses import mean_squared_error
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
        data_00 = np.load('AI/pet_filter/cat/data/dataset/CAT_00.npy', allow_pickle=True)
        data_01 = np.load('AI/pet_filter/cat/data/dataset/CAT_01.npy', allow_pickle=True)
        data_02 = np.load('AI/pet_filter/cat/data/dataset/CAT_02.npy', allow_pickle=True)
        data_03 = np.load('AI/pet_filter/cat/data/dataset/CAT_03.npy', allow_pickle=True)
        data_04 = np.load('AI/pet_filter/cat/data/dataset/CAT_04.npy', allow_pickle=True)
        data_05 = np.load('AI/pet_filter/cat/data/dataset/CAT_05.npy', allow_pickle=True)
        data_06 = np.load('AI/pet_filter/cat/data/dataset/CAT_06.npy', allow_pickle=True)

        x_train = np.concatenate((data_00.item().get('imgs'), data_01.item().get('imgs'), data_02.item().get('imgs'),
                                  data_03.item().get('imgs'), data_04.item().get('imgs'), data_05.item().get('imgs')))
        y_train = np.concatenate((data_00.item().get(mode), data_01.item().get(mode), data_02.item().get(mode),
                                  data_03.item().get(mode), data_04.item().get(mode), data_05.item().get(mode)))

        x_test = np.array(data_06.item().get('imgs'))
        y_test = np.array(data_06.item().get(mode))

        x_train = x_train.astype('float32') / 255
        x_test = x_test.astype('float32') / 255
        x_train = np.reshape(x_train, (-1, img_size, img_size, 3))
        x_test = np.reshape(x_test, (-1, img_size, img_size, 3))

        y_train = np.reshape(y_train, (-1, output_size))
        y_test = np.reshape(y_test, (-1, output_size))

        inputs = Input(shape=(img_size, img_size, 3))

        moblienetV2 = keras.applications.MobileNetV2(input_shape=(img_size, img_size, 3), alpha=1.0, depth_multiplier=1,
                                               include_top=False,
                                               weights='imagenet', input_tensor=inputs, pooling='max')

        net = Dense(128, activation='relu')(moblienetV2.layers[-1].output)
        net = Dense(64, activation='relu')(net)
        net = Dense(32, activation='relu')(net)
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

    def preprocess_data(self, dir_name):
        self.pet_face.load_cat_data(dir_name)

test = Pet_Face_Detector_Model()
# test.preprocess_data('CAT_00')
# test.preprocess_data('CAT_01')
# test.preprocess_data('CAT_02')
# test.preprocess_data('CAT_03')
# test.preprocess_data('CAT_04')
# test.preprocess_data('CAT_05')
# test.preprocess_data('CAT_06')
test.train_model()