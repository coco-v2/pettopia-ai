import dlib
import cv2
import matplotlib.pyplot as plt
#conda install -c conda-forge dlib
#conda install -c conda-forge/label/cf201901 dlib
#conda install -c conda-forge/label/cf202003 dlib

detector = dlib.cnn_face_detection_model_v1('model/dogHeadDetector.dat')
predictor = dlib.shape_predictor('model/landmarkDetector.dat')

img = cv2.imread("image/dog1.jpg")

cv2.imshow("img", img)

#얼굴을 검출
faces = detector(img)

# 검출된 얼굴에 대해 랜드마크를 검출하고 표시
for face in faces:
    landmarks = predictor(img, face)

    for i in range(68):
        x, y = landmarks.part(i).x, landmarks.part(i).y
        cv2.circle(img, (x, y), 2, (0, 255, 0), -1)

# 결과 이미지를 출력
cv2.imshow("img", img)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
cv2.waitKey(0)