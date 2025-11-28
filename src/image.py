import os
import cv2

def load_images(folder, target_count=240, resize_to=256):
    # 이미지 리스트 생성
    images = []

    # 폴더 내 이미지 파일 탐색
    for file in os.listdir(folder):
        if not (file.lower().endswith(".jpg") or file.lower().endswith(".png")):
            continue

        img_path = os.path.join(folder, file)
        img = cv2.imread(img_path)

        # 로드 실패 시 무시
        if img is None:
            print("이미지 로드 실패:", file)
            continue

        # 리사이즈 후 저장
        img_resized = cv2.resize(img, (resize_to, resize_to))
        images.append(img_resized)

    # 이미지가 없으면 에러
    if len(images) == 0:
        raise ValueError("이미지 없음")

    # target_count만큼 반복하여 확장
    repeated = []
    index = 0
    for i in range(target_count):
        repeated.append(images[index])
        index = (index + 1) % len(images)  # 순환 구조

    return repeated
