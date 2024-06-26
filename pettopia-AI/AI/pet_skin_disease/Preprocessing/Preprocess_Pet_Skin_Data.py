import json, re
import sys
sys.path.append('pettopia-AI')

#from Interface import Process_Data

import random
import cv2, os
import numpy as np
import pandas as pd

class Preprocess_Pet_Disease_Data():

    def __init__(self):
        super().__init__()
        self.img_size = 224
        self.dir_name = 'A1'
        self.base_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/archive/%s' % self.dir_name
        self.file_list = sorted(os.listdir(self.base_path))
        random.shuffle(self.file_list)
        self.dataset = {
            'imgs':[],
            'label':[],
        }

    def resize_img(self, img):
        old_size = img.shape[:2]  # 높이, 너비
        ratio = float(self.img_size) / max(old_size)  # 가장 큰 이미지 기준으로 비율 구하기
        new_size = tuple([int(x * ratio) for x in old_size])
        img = cv2.resize(img, (new_size[1], new_size[0]))  # 새 사이즈로 포맷 맞추기

        delta_w = self.img_size - new_size[1]  # 원본 이미지와 새이미지 크기 간의 차이 계산
        delta_h = self.img_size - new_size[0]

        top, bottom = delta_h // 2, delta_h - (delta_h // 2)  # 패딩 계산
        left, right = delta_w // 2, delta_w - (delta_w // 2)
        new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        # 패딩 추가. 상하좌우에 동일한 색상의 패팅을 추가하고 색은 [0,0,0]으로

        return new_img, ratio, top, left

    def process_img(self):
        img_size = 224
        mode = 'bbs'  # [bbs, lmks]
        output_size = 4 if mode == 'bbs' else 18

        # 데이터 로드 및 전처리
        data_paths = []

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

        return x_train, y_train

    def process_filter(self, img):
        sharpening_kernel = np.array([[-1, -1, -1],
                                      [-1, 9, -1],
                                      [-1, -1, -1]])

        # 샤프닝 필터 적용
        sharpened_image = cv2.filter2D(img, -1, sharpening_kernel)

        return sharpened_image

    def load_data(self, dir_name):
        cnt = 0

        base_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/archive/%s' % dir_name
        file_list = sorted(os.listdir(base_path))
        random.shuffle(file_list)

        for f in file_list:
            if '.json' not in f:
                continue

            json_file_path = os.path.join(base_path, f)
            with open(json_file_path, 'r', encoding='UTF8') as file:
                data = json.load(file)

                for item in data['labelingInfo']:
                    if 'box' in item:
                        box = item['box']

                        label = box['label']
                        label_num = re.findall(r'\d+', dir_name)


                        location = box['location']
                        x = int(location[0]['x'])
                        y = int(location[0]['y'])
                        width = int(location[0]['width'])
                        height = int(location[0]['height'])

                        img_filename, _ = os.path.splitext(f)
                        img_path = os.path.join(base_path, img_filename + '.jpg')
                        img = cv2.imread(img_path)
                        cropped_img = img[y:y+height, x:x+width]

                        res_img = self.process_filter(cropped_img)
                        # cv2.imshow("d", res_img)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()

                        if img is not None:
                            self.dataset['label'].append(int(label_num[0]))
                            self.dataset['imgs'].append(res_img)

                    print(cnt)
                    cnt += 1

                if cnt > 5001:
                    break


        np.save('C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/AI/pet_skin_disease/data/dataset/%s.npy' % dir_name, np.array((self.dataset)))

test = Preprocess_Pet_Disease_Data()
print("a1")
test.load_data('A1')
#print("a2")
#test.load_data('A2')
#print("a3")
#test.load_data('A3')
#print("a4")
#test.load_data('A4')
#print("a5")
#test.load_data('A5')
# print("a6")
# test.load_data('A6')

# def delete_image_and_json_pairs_except_n(dir_name, n):
#     base_path = 'AI/pet_skin_disease/data/archive/%s' % dir_name
#     file_list = sorted(os.listdir(base_path))
#
#     jpg_files = [f for f in file_list if f.endswith('.jpg')]
#     total_pairs = len(jpg_files)
#
#     delete_count = total_pairs - n
#
#     random.shuffle(jpg_files)
#
#     cnt = 0
#
#     for jpg_file in jpg_files:
#         json_file_path = os.path.join(base_path, jpg_file[:-4] + '.json')
#
#         os.remove(os.path.join(base_path, jpg_file))
#         #print("Image file %s deleted." % jpg_file)
#         cnt += 1
#
#         if os.path.exists(json_file_path):
#             os.remove(json_file_path)
#             #print("JSON file %s deleted." % json_file_path)
#             cnt += 1
#
#         if cnt == delete_count * 2:
#             break
#
#     print("%d image and json pairs deleted." % (cnt // 2))
#
# delete_image_and_json_pairs_except_n('A1', 5000)