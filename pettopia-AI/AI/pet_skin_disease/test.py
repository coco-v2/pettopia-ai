'''
data
    image
preprocessjing
    resize
    filers
model
'''
import numpy as np
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten


output_size = 6
img_size = 224

data_paths = ['C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A1.npy',
              'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A2.npy',
              'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A3.npy',
              'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A4.npy',
              'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A5.npy',
              'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/A6.npy']

x_train, y_train = [], []

for path in data_paths:
    # Load the data
    data = np.load(path, allow_pickle=True).item()
    imgs = data.get('imgs')
    labels = data.get('label')

    # Check if labels exist
    if labels is not None:
        x_train.extend(imgs)
        y_train.extend(labels)

# Convert lists to numpy arrays and normalize images
x_train = np.array(x_train).astype('float32') / 255

# Convert labels to integers
# label_encoder = LabelEncoder()
# y_train = label_encoder.fit_transform(y_train)

# # Ensure y_train is one-hot encoded
# y_train = to_categorical(y_train, num_classes=output_size)

# Reshape images
x_train = np.reshape(x_train, (-1, img_size, img_size, 3))

# Model definition
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

# Model compilation
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Model training
model.fit(x_train, y_train, epochs=10, validation_split=0.2)

# 모델 저장
model.save(
    'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/model/pet_skin_disease_model.h5')
