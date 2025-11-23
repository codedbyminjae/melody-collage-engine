import cv2
import os

def load_and_repeat_images(folder, target_count=240, resize_to=256):
    """
    1. 폴더에서 이미지를 모두 읽는다.
    2. 크기를 동일하게 맞춘다
    3. 이미지 개수는 한정적이기에 반복해서 target_count 개로 맞춘다.
    4. 이를 리스트로 반환한다.
    """

    # 이미지 저장 배열
    images = []

    # 폴더 내부 전체 이미지 파일 탐색
    for file in os.listdir(folder):

        # 확장자 jpg/png인지 확인 (대소문자 혼합 파일 대비)
        if not (file.lower().endswith(".jpg") or file.lower().endswith(".png")):
            continue

        img_path = os.path.join(folder, file)
        img = cv2.imread(img_path)

        # 정상적으로 로드되지 않은 이미지 제외
        if img is None:
            print("이미지 로드 실패:", file)
            continue

        # 모든 이미지를 동일 크기로 세팅
        img_resized = cv2.resize(img, (resize_to, resize_to))
        images.append(img_resized)

    # 로드된 이미지가 없을 경우 예외 처리
    if len(images) == 0:
        raise ValueError("이미지 없음")

    # 음악 segment 개수 만큼 이미지를 반복하여 확장
    repeated = []
    index = 0
    for i in range(target_count):
        repeated.append(images[index])

        # index를 0 -> 1 -> ... -> 마지막 -> 다시 0 순환 구조
        index = (index + 1) % len(images)

    return repeated
