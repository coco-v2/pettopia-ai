import keras, sys, cv2, os
from keras.models import Model, load_model
import numpy as np
import pandas as pd
from math import atan2, degrees

import cat_face_preprocess as cat_face
import cat_face_landmark_preprocess as cat_lmk

img_size = 224
base_path = 'image/sample'
file_list = sorted(os.listdir(base_path))

#중요
glasses = cv2.imread('', cv2.IMREAD_UNCHANGED)

bbs_model_name = sys.argv[1]
lmks_model_name = sys.argv[2]
bbs_model = load_model(bbs_model_name)
lmks_model = load_model(lmks_model_name)

def resize_img(img):
    old_size = img.shape[:2] #(h,w)

#오버레이
def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
    bg_img = background_img.copy()

    #3채널을 4채널로
    if bg_img.shape[2] == 3:
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA)

    if overlay_size is not None:
        img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

    b, g, r, a = cv2.split(img_to_overlay_t)

    mask = cv2.medianBlur(a, 5)

    h, w, _ = img_to_overlay_t.shape
    roi = bg_img[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)]

    img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
    img2_fg = cv2.bitwise_and(img_to_overlay_t, img_to_overlay_t, mask=mask)

    bg_img[int(y-h):int(y+h/2), int(x-w/2):int(x+w/2)] = cv2.add(img1_bg, img2_fg)

    #4채널 -> 3채널
    bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2BGR)

    return bg_img

def angle_between(p1, p2):
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p2[1]

    return degrees(atan2(yDiff, xDiff ))

#test
for f in file_list:
    if '.jpg' not in f:
        continue

    img = cv2.imread(os.path.join(base_path, f))
    ori_img = img.copy()
    result_img = img.copy()

    #바운디 박스 예측

    img, ratio, top, left = cat_face.resize_img(img)

    inputs = (img.astype('float32') / 255).reshape((1, img_size, img_size, 3))
    pred_bb = bbs_model.predict(input)[0].reshape((-1,2))

    #원래 이미지의 바운딩 박스 계산
    ori_bb = ((pred_bb - np.array([left, top])) / ratio).astype(np.int)

    #랜드마크 탐지를 위한 느슨한 경계 계산
    center = np.mean(ori_bb, axis=0)
    face_size = max(np.abs(ori_bb[1] - ori_bb[0]))
    new_bb = np.array([
        center - face_size * 0.6,
        center + face_size * 0.6
    ])
    new_bb = np.clip(new_bb, 0, 99999)

    #랜드마크 예측
    face_img = ori_img[new_bb[0][1]:new_bb[1][1], new_bb[0][0]:new_bb[1][0]]


    face_img, face_ratio, face_top, face_left = cat_lmk.resize_img(face_img)

    face_inputs = (face_img.astype('float32') / 255).reshape((1, img_size, img_size, 3))

    pred_lmks = lmks_model.predict(face_inputs)[0].reshape((-1,2))

    #원래 이미지에서 랜드마크 계산
    new_lmks = ((pred_lmks - np.array([face_left, face_top])) / face_ratio).astype(np.int)
    ori_lmks = new_lmks + new_bb[0]

    #시각화
    cv2.rectangle(ori_img, pt1=tuple(ori_bb[0]), pt2=tuple(ori_bb[1]), color=(255, 255, 255), thickness=2)

    for i, l in enumerate(ori_lmks):
        cv2.putText(ori_img, str(i), tuple(l), cv2.FONT_HERSHEY_SIMPLEX, 1, (225,225,255), 2, cv2.LINE_AA)
        cv2.circle(ori_img, center=tuple(l), radius=1, color=(255, 255, 255), thickness=2)

    #안경
    glasses_center = np.mean([ori_lmks[0], ori_lmks[1]], axis=0)
    glasses_size = np.linalg.norm(ori_lmks[0] - ori_lmks[1]) * 2

    angle = -angle_between(ori_lmks[0], ori_lmks[1])
    M = cv2.getRotationMatrix2D((glasses_center.shape[1]/2, glasses.shape[0] / 2), angle, 1)
    rotated_glasses = cv2.warpAffine(glasses, M, (glasses.shape[1], glasses.shape[0]))

    try:
        result_img = overlay_transparent(result_img, rotated_glasses, glasses_center[0], glasses_center[1],
                                         overlay_size=(int(glasses_size), int(glasses.shape[0] * glasses_size / glasses.shape[1])))
    except:
        print('failed overlay image')

    cv2.imshow('img', ori_img)
    cv2.imshow('result', result_img)
    file_name, ext = os.path.splitext(f)
    cv2.imwrite('result/%s_lmks' % (file_name, ext), ori_img)
    cv2.imwrite('rsult/%s_result' % (file_name, ext), result_img)

    if cv2.waitKey(0) == ord('q'):
        break
