import cv2
import numpy as np
from tile import Tile

"""
layout: 2D 배열
title_size: 각 타일 이미지 크기
return 최종 합성된 numpy 이미지
"""
def build_collage(layout, tile_size=128):
    grid_h = len(layout)
    grid_w = len(layout[0])

    # 최종 결과 이미지 캔버스 생성
    collage_h = grid_h * tile_size
    collage_w = grid_w * tile_size
    collage = np.zeros((collage_h, collage_w, 3), dtype=np.uint8)

    # 각 타일을 순서대로 채워넣기
    for row_idx, row in enumerate(layout):
        for col_idx, tile in enumerate(row):

            # 타일 이미지 로드
            img = cv2.imread(tile.img_path)
            if img is None:
                continue

            # 타일 크기 맞춰 리사이즈
            img_resized = cv2.resize(img, (tile_size, tile_size))

            # collage에 붙여넣기
            y1 = row_idx * tile_size
            y2 = y1 + tile_size
            x1 = col_idx * tile_size
            x2 = x1 + tile_size

            collage[y1:y2, x1:x2] = img_resized

    return collage