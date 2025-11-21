import cv2
import numpy as np
import os

#  images 폴더 안의 이미지를 읽고, 평균 밝기 계산
def load_tiles_from_folder(folder_path):
    tiles = []

    for filename in os.listdir(folder_path):
        # 타겟 이미지는 제외하기 위해 파일명에 target 있는지 체크
        if 'target' in filename.lower():
            continue

        path = os.path.join(folder_path, filename)
        img = cv2.imread(path)

        if img is None:
            print(f"[WARN] 이미지를 읽을 수 없습니다: {filename}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray))

        tiles.append({
            "file": filename,
            "path": path,
            "brightness": brightness
        })

    if len(tiles) != 25:
        print(f"[WARN] 현재 타일 개수: {len(tiles)}개 (25개 필요)")

    return tiles
