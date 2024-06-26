from .....Interface import Process_Data

import random, sys
import dlib, cv2, os
import pandas as pd
import numpy as np

class Preproces_Pet_Landmark_Data(Process_Data.Preprocess_Data):

    def __init__(self):
        self.img_size = 224
        self.dir_name = 'CAT_00'
        self.base_path = 'data/archive/cats/%s' % self.dir_name
        self.file_list = sorted(os.listdir(self.base_path))
        random.shuffle(self.file_list)

        self.dataset = {
            'imgs': [],
            'lmks': [],
            'bbs': []
        }

    def resize_img(self, img):
        old_size = img.shape[:2]  # 높이, 너비
        ratio = float(self.img_size) / max(old_size)  # 가장 큰 이미지 기준으로 비율 구하기
        new_size = tuple([int(x * ratio) for x in old_size])
        img = cv2.resize(img, (new_size[1], new_size[0]))  # 새 사이즈로 포맷 맞추기

        delta_w = self.img_size - new_size[1]  # 원본 임지ㅣ와 새이미지 크기 간의 차이 계산
        delta_h = self.img_size - new_size[0]

        top, bottom = delta_h // 2, delta_h - (delta_h // 2)  # 패딩 계산
        left, right = delta_w // 2, delta_w - (delta_w // 2)
        new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        # 패딩 추가. 상하좌우에 동일한 색상의 패팅을 추가하고 색은 [0,0,0]으로

        return new_img, ratio, top, left

    def process_img(self):
        pass

    def load_cat_data(self):
        for f in self.file_list:
            if '.cat' not in f:
                continue

            # 랜드마크 가져오기
            pd_frame = pd.read_csv(os.path.join(self.base_path, f), sep=' ', header=None)
            landmarks = (pd_frame.as_matrix()[0][1, -1]).reshape((-1, 2))
            bb = np.array([np.min(landmarks, axis=0), np.max(landmarks, axis=0)]).astype(np.int)

            center = np.mean(bb, axis=0)
            face_size = max(np.abs(np.max(landmarks, axis=0) - np.min(landmarks, axis=0)))

            new_bb = np.array([
                center - face_size * 0.6,
                center + face_size * 0.6
            ]).astype(np.int)
            new_bb = np.clip(new_bb, 0, 99999)
            new_landmarks = landmarks - new_bb[0]

            # load image
            img_filename, ext = os.path.splitext(f)

            img = cv2.imread(os.path.join(self.base_path, img_filename))
            new_img = img[new_bb[0][1]:new_bb[1][1], new_bb[0][0]:new_bb[1][0]]

            # resize image and relocate landmarks
            self.dataset['imgs'].append(img)
            self.dataset['lmks'].append(landmarks.flatten())
            self.dataset['bbs'].append(bb.flatten())

            # for i in landmarks:
            #     cv2.circle(img, center=tuple(1), radius=1, color=(225,225,225), thickness=2)
            #
            # cv2.imshow('img', img)
            # if cv2.waitKey(0) == ord('q'):
            #     break

        np.save('dataset/%s.npy' % self.dir_name, np.array((self.dataset)))