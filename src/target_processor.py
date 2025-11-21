import cv2
import numpy as np

# 타겟 이미지를 읽고 RGB→GRAY로 변환
def load_target_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"타겟 이미지가 존재하지 않습니다: {path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img, gray

# 타깃 이미지를 5x5로 나누고, 각 칸의 평균 밝기 계산
def split_into_grid(gray_img, grid_w=5, grid_h=5):
    h, w = gray_img.shape
    cell_h = h // grid_h
    cell_w = w // grid_w

    brightness_map = []

    for r in range(grid_h):
        for c in range(grid_w):
            cell = gray_img[
                r * cell_h : (r + 1) * cell_h,
                c * cell_w : (c + 1) * cell_w
            ]

            mean_brightness = float(np.mean(cell))
            brightness_map.append({
                "row": r,
                "col": c,
                "brightness": mean_brightness
            })

    return brightness_map

# 밝기가 낮은 칸 부터 하기 위해 오름차순 정렬
def get_filling_order(brightness_map):
    return sorted(brightness_map, key=lambda x: x["brightness"])
