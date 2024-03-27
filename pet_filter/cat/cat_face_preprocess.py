import random
import dlib, cv2, os
import numpy as np
import  pandas as pd

img_size = 224
dir_name = 'CAT_00'
base_path = 'data/archive/cats/%s' % dir_name
file_list = sorted(os.listdir(base_path))
random.shuffle(file_list)

dataset = {
    'imgs' : [],
    'lmks' : [],
    'bbs' : []
}

def resize_img(img):
    old_size = img.shape[:2] #높이, 너비
    ratio = float(img_size) / max(old_size) #가장 큰 이미지 기준으로 비율 구하기
    new_size = tuple([int(x*ratio) for x in old_size])
    img = cv2.resize(img, (new_size[1], new_size[0])) #새 사이즈로 포맷 맞추기

    delta_w = img_size - new_size[1] #원본 임지ㅣ와 새이미지 크기 간의 차이 계산
    delta_h = img_size - new_size[0]

    top, bottom = delta_h // 2, delta_h - (delta_h // 2) #패딩 계산
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    #패딩 추가. 상하좌우에 동일한 색상의 패팅을 추가하고 색은 [0,0,0]으로

    return new_img, ratio, top, left

def load_cat_data():
    for f in file_list:
        if '.cat' not in f:
            continue

        #랜드마크 읽기
        pd_frame = pd.read_csv(os.path.join(base_path, f), sep=' ', header=None)
        landmarks = (pd_frame.as_matrix()[0][1:-1]).reshape((-1,2)) #pd를 numpy로 변환. 1차원 배열을 2차원(자동, 2열)으로 재구성

        #사진 가져오기
        img_filename, ext = os.path.splitext(f) #이름과 확장자 분리(확장자 포함 and 확장자 미포함)
        img = cv2.imread(os.path.join(base_path, img_filename))

        #
        img, ratio, top, left = resize_img(img)
        landmarks = ((landmarks * ratio) + np.array([left, top])).astype(np.int)
        bb = np.array([np.min(landmarks, axis=0), np.max(landmarks, axis=0)])

        dataset['imgs'].append(img)
        dataset['lmks'].append(landmarks.flatten())
        dataset['bbs'].append(bb.flatten())

        # for i in landmarks:
        #     cv2.circle(img, center=tuple(1), radius=1, color=(225,225,225), thickness=2)
        #
        # cv2.imshow('img', img)
        # if cv2.waitKey(0) == ord('q'):
        #     break

    np.save('dataset/%s.npy' %dir_name, np.array((dataset)))



