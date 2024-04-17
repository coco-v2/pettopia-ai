import random, sys
import dlib, cv2, os
import pandas as pd
import numpy as np

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
    old_size = img.shape[:2]
    ratio = float(img_size) / max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    img = cv2.resize(img, (new_size[1], new_size[0]))
    delta_w = img_size - new_size[1]
    delta_h = img_size - new_size[0]

    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return new_img, ratio, top, left

def load_cat_data():
    for f in file_list:
        if '.cat' not in f:
            continue

        #랜드마크 가져오기
        pd_frame = pd.read_csv(os.path.join(base_path, f), sep=' ', header=None)
        landmarks = (pd_frame.as_matrix()[0][1, -1]).reshape((-1,2))
        bb = np.array([np.min(landmarks, axis=0), np.max(landmarks, axis=0)]).astype(np.int)

        center = np.mean(bb, axis=0)
        face_size = max(np.abs(np.max(landmarks, axis=0) - np.min(landmarks, axis=0)))

        new_bb = np.array([
            center - face_size * 0.6,
            center + face_size * 0.6
        ]).astype(np.int)
        new_bb = np.clip(new_bb, 0, 99999)
        new_landmarks = landmarks - new_bb[0]

        #load image
        img_filename, ext = os.path.splitext(f)

        img = cv2.imread(os.path.join(base_path, img_filename))
        new_img = img[new_bb[0][1]:new_bb[1][1], new_bb[0][0]:new_bb[1][0]]

        #resize image and relocate landmarks
        dataset['imgs'].append(img)
        dataset['lmks'].append(landmarks.flatten())
        dataset['bbs'].append(bb.flatten())

        # for i in landmarks:
        #     cv2.circle(img, center=tuple(1), radius=1, color=(225,225,225), thickness=2)
        #
        # cv2.imshow('img', img)
        # if cv2.waitKey(0) == ord('q'):
        #     break

    np.save('dataset/%s.npy' % dir_name, np.array((dataset)))