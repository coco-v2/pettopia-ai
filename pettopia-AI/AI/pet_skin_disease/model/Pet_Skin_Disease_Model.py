import sys

from keras import Model
from keras.models import Model
from keras.layers import Dense
from tensorflow.keras.models import load_model
import cv2
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils import class_weight


sys.path.append('pettopia-AI')
from AI.pet_disease.Preprocessing.Preprocess_Pet_Skin_Data import Preprocess_Pet_Skin_Data

import numpy as np

class Pet_Skin_Disease_Model():

     def __init__(self):
        self.pet_skin = Preprocess_Pet_Skin_Data.Preprocess_Pet_Skin_Data()

     def preprocess_image(self, img_path, img_size=224):
        image = cv2.imread(img_path)
        if image is None:
            raise ValueError(f"Could not open or find the image {img_path}")
        image = cv2.resize(image, (img_size, img_size))
        image = image.astype('float32') / 255
        image = np.expand_dims(image, axis=0)

        return image

     def model_test(self, img):
        image_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/image/' + img
        model_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/model/best_inception_v3_model.h5'

        # 이미지 전처리
        image = self.preprocess_image(image_path)

        # 모델 로드
        model = load_model(model_path, compile=False)

        # 예측 수행
        predictions = model.predict(image)

        # 예측 결과 처리
        result_index = np.argmax(predictions)
        result = int(result_index) + 1
        print(f"Predictions: {predictions}")

        # 결과 해석
        if result == 1:
            result_label = "구진"
        elif result == 2:
            result_label = "비듬/각질/상피성잔고리"
        elif result == 3:
            result_label = "태선화/과다색소침착"
        elif result == 4:
            result_label = "농포/여드름"

        print(f"Result: {result_label}")

        return result_label

     def train_model(self):
        output_size = 4
        img_size = 224

        data_paths = ['C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A1.npy',
                      'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A2.npy',
                      'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A3.npy',
                      'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A4.npy']

        x_data, y_data = [], []

        for path in data_paths:
            try:
                data = np.load(path, allow_pickle=True).item()
                imgs = data.get('imgs')
                labels = data.get('label')

                if labels is not None:
                    for img in imgs:
                        resized_img = cv2.resize(img, (img_size, img_size))
                        x_data.append(resized_img)
                    y_data.extend(labels)
            except Exception as e:
                print(f"Error loading data from {path}: {e}")

        x_data = np.array(x_data).astype('float32') / 255

        label_encoder = LabelEncoder()
        y_data_int = label_encoder.fit_transform(y_data)

        y_data = to_categorical(y_data_int, num_classes=output_size)

        x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2, random_state=42)

        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )

        train_generator = datagen.flow(x_train, y_train, batch_size=32)
        val_generator = datagen.flow(x_val, y_val, batch_size=32)

        base_model = tf.keras.applications.InceptionV3(weights='imagenet', include_top=False, input_shape=input_shape)
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)  # Dropout 추가
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)  # Dropout 추
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(64, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        output_layer = Dense(output_size, activation='softmax')(x)
        model = Model(inputs=base_model.input, outputs=output_layer)

        class_weights = dict(
            enumerate(class_weight.compute_class_weight('balanced', classes=np.unique(y_data_int), y=y_data_int)))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=10, validation_split=0.2)

        model.fit(train_generator,
                               epochs=25,
                               validation_data=val_generator,
                               class_weight=class_weights)

        model.save('C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/model/final_inception_v3_model.h5')

     def preprocess_data(self, dir_name):
        self.pet_face.load_cat_data(dir_name)

# test = Pet_Skin_Disease_Model()
# # # # test.preprocess_data('CAT_00')
# # # # test.preprocess_data('CAT_01')
# # # # test.preprocess_data('CAT_02')
# # # # test.preprocess_data('CAT_03')
# # # # test.preprocess_data('CAT_04')
# # # # test.preprocess_data('CAT_05')
# # # # test.preprocess_data('CAT_06')
# # # #test.train_model()
# test.model_test('3.jpg')
