'''

def preprocessing_img
def train_pet_color_model
def test
'''
import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Input, Dense
import numpy as np

# 가정: 색상을 RGB 형태로 입력 받음. 출력은 먼셀 색조화론에 따른 분류 값임.
# 입력 색상 예시 (RGB)
colors = np.array([
  [255, 0, 0],  # 빨간색
  [0, 255, 0],  # 초록색
  [0, 0, 255]   # 파란색
])

# 해당 색상의 먼셀 색조화론에 따른 분류 (예시 값)
labels = np.array([
  [1],  # 빨간색
  [2],  # 초록색
  [3]   # 파란색
])

model = Sequential([
  Dense(64, activation='relu', input_shape=(3,)),  # 3개의 입력(색상 RGB)
  Dense(64, activation='relu'),
  Dense(1, activation='sigmoid')  # 출력: 먼셀 색조 분류값
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(colors, labels, epochs=500)

# 새로운 색상으로 테스트
new_colors = np.array([
  [128, 0, 0]  # 어두운 빨간색
])

print(model.predict(new_colors))