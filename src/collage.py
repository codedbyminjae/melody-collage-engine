import cv2
import numpy as np
import random

# 회전 함수 (energy 기반 회전폭)
def rotate_image(img, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

# 알파 블렌딩
def alpha_blend(canvas, img, x, y, alpha):
    h, w = img.shape[:2]
    H, W = canvas.shape[:2]

    roi = canvas[y:y+h, x:x+w]
    blended = (roi * (1 - alpha) + img * alpha).astype(np.uint8)  # 배경과 로고 부분 코드 참조
    canvas[y:y+h, x:x+w] = blended
    return canvas

def build_collage(images, scale_list, rotation_list, canvas_w, canvas_h):

    # 빈 캔버스 생성
    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    for idx, img in enumerate(images):

        # 1. 크기 변화 (brightness → scale)
        scale = scale_list[idx]
        base_size = 180                     # 기본 이미지 크기
        size = int(base_size * scale)
        size = max(80, min(500, size))      # 과도한 크기 제한

        img = cv2.resize(img, (size, size))

        # 2. 회전 (energy → 회전폭 반영)
        real_rot = rotation_list[idx] # 현재 인덱스의 회전값 (정규화 된 값)
        direction = random.choice([-1, 1])
        angle = direction * real_rot # 최종 회전 각도
        img = rotate_image(img, angle)

        # 3) 위치는 완전 랜덤 (단순화)
        x = random.randint(0, canvas_w - size)
        y = random.randint(0, canvas_h - size)

        # 4) 알파 값
        alpha = 0.55 + scale * 0.20
        alpha = max(0.4, min(alpha, 0.9)) # 클램핑 과정

        # 5) 합성
        canvas = alpha_blend(canvas, img, x, y, alpha)

        # 6) 실시간 미리보기 생성
        preview = cv2.resize(canvas, None, fx = 0.45, fy = 0.45)

        cv2.imshow("Making Collage", preview)
        cv2.moveWindow("Making Collage", 100, 100)
        cv2.waitKey(10)

    return canvas
