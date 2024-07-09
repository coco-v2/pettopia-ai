import cv2

# 이미지 파일 경로
s = 'mydog.jpg'

# 이미지 불러오기
img = cv2.imread(s)

# 이미지를 제대로 불러왔는지 확인
if img is not None:
    # 이미지 저장 경로와 파일 이름
    save_path = 'C:/Users/jooho/Documents/GitHub/pettopia-ai/pettopia-AI/Control/' + s

    # 이미지 저장
    cv2.imwrite(save_path, img)
    print("이미지가 성공적으로 저장되었습니다.")
else:
    print("이미지를 불러올 수 없습니다. 파일 경로를 확인하세요.")
