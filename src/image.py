import os
import cv2

def load_images(folder, target, resize):
    
    images = [] # 이미지 리스트 생성

    for file in os.listdir(folder): # # 폴더 내 모든 이미지를 자동으로 불러오기 위해 listdir 사용 (참조부분)
        if not (file.lower().endswith(".jpg") or file.lower().endswith(".png")): # 확장자로 예외처리 (이미지만)
            continue

        img_path = os.path.join(folder, file)
        img = cv2.imread(img_path)

        if img is None: # 로드 실패 시 무시
            # print("이미지 로드 실패:", file)
            continue

        img_resized = cv2.resize(img, (resize, resize)) # 리사이즈 후 저장
        images.append(img_resized)

    repeated = []
    index = 0
    for i in range(target): # target 개수 만큼 반복하여 확장
        repeated.append(images[index])
        index += 1
        if index == len(images):
            index = 0

    return repeated
