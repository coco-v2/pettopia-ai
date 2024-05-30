import cv2
import numpy as np
from sklearn.cluster import KMeans
import os,sys

sys.path.append('pettopia-AI')
from AI.pet_color.Preprocess.Preprocess_Pet_Image_Data import Preprocess_Pet_Image_Data

class Pet_Color_Model():

  def __init__(self):
    self.preprocess_data = Preprocess_Pet_Image_Data()

  # 주요 색상 추출
  def extract_colors(self, image_path, num_colors=3):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image.reshape(-1, 3)

    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_

    return colors


  # 조화로운 색상 찾기
  def find_harmonious_colors(self, colors):
    n5_hsv = (0, 0, 128)  # 중성 회색 (N5)의 HSV 값
    harmonious_colors = []

    for color in colors:
      hsv_color = self.preprocess_data.rgb_to_hsv_255(*color)
      harmonious_color_hsv = (hsv_color[0], hsv_color[1], n5_hsv[2])
      harmonious_color_rgb = self.preprocess_data.hsv_to_rgb_255(*harmonious_color_hsv)
      harmonious_colors.append(harmonious_color_rgb)

    return harmonious_colors

  # 이미지 처리 및 저장
  def process_data(self, image_path):
    colors = self.extract_colors(image_path)
    harmonious_colors = self.find_harmonious_colors(colors)

    harmonious_colors = [tuple(map(int, color)) for color in harmonious_colors]

    self.save_colors(harmonious_colors)

  def save_colors(self, colors):
    result = []

    for idx, color in enumerate(colors):
      color_img = np.zeros((100, 100, 3), dtype=np.uint8)
      color_img[:] = color

      #hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
      result.append(color)

    return result


# 이미지 경로
# image_path = 'AI/pet_color/data/cat.jpg'
#
# test = Pet_Color_Model()
# test.process_data(image_path)
