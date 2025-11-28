import cv2
import numpy as np
import random

from config import (
    TARGET_COUNT,
    INTRO_CUTOFF,
    OUTRO_CUTOFF,
    PREVIEW,
    PREVIEW_DELAY,
    MODE,
)

# 회전
def random_rotate(img, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h),
                          flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REFLECT)

# 채도 조절
def adjust_saturation(img, factor):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

# α-블렌딩
def alpha_blend(canvas, img, x, y, alpha):
    h, w = img.shape[:2]
    H, W = canvas.shape[:2]

    if x + w > W or y + h > H:
        w = max(0, W - x)
        h = max(0, H - y)
        img = img[:h, :w]

    if w <= 0 or h <= 0:
        return canvas

    roi = canvas[y:y+h, x:x+w]
    blended = (roi * (1 - alpha) + img * alpha).astype(np.uint8)
    canvas[y:y+h, x:x+w] = blended
    return canvas

# 이미지 처리(크기·채도·회전)
def process_image(img, scale, tempo_norm, energy_norm, idx, base_min, base_max):
    base = random.randint(base_min, base_max)
    size = int(base * scale)
    size = max(80, min(600, size))

    img = cv2.resize(img, (size, size))

    sat = (0.3 + scale * 1.4) * (0.4 + tempo_norm)
    img = adjust_saturation(img, sat)

    rot_range = 15 + energy_norm[idx] * 30
    angle = random.uniform(-rot_range, rot_range)
    img = random_rotate(img, angle)

    return img, size

# 콜라주 생성
def build_layer_collage(images, scale_factors, tempo_norm, energy_norm,
                        canvas_w, canvas_h, base_min, base_max):

    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    for idx, img in enumerate(images):

        # 스케일 보정(인트로/아웃트로)
        scale = scale_factors[idx]
        if idx < INTRO_CUTOFF:
            scale *= 0.85
        elif idx > OUTRO_CUTOFF:
            scale *= 1.15

        # 이미지 처리
        processed, size = process_image(img, scale, tempo_norm, energy_norm, idx,
                                        base_min, base_max)

        # -----------------------
        # 위치 결정: MODE 적용
        # -----------------------

        # 랜덤 콜라주
        if MODE == "random":
            y = random.randint(0, canvas_h - size)
            x = random.randint(0, canvas_w - size)

        # 음악 흐름 모드
        else:
            # 인트로: 상단 좌측
            if idx < INTRO_CUTOFF:
                y = random.randint(0, 150)
                x = random.randint(0, canvas_w // 3)

            # 아웃트로: 하단 우측
            elif idx > OUTRO_CUTOFF:
                margin = int(canvas_h * 0.15)
                y_min = max(canvas_h - margin, 0)
                y_max = canvas_h - size
                if y_min > y_max:
                    y_min = y_max
                y = random.randint(y_min, y_max)

                x_min = canvas_w - (canvas_w // 3)
                x_max = canvas_w - size
                x = random.randint(x_min, max(x_min, x_max))

            # 중간(랜덤 80% + 흐름 20%)
            else:
                t_y = int((idx / TARGET_COUNT) * canvas_h)
                y_rand = random.randint(0, canvas_h - size)
                y = int(0.8 * y_rand + 0.2 * t_y)
                y = min(max(y, 0), canvas_h - size)

                x = random.randint(0, canvas_w - size)

        # 투명도
        alpha = min(max(0.65 + scale * 0.25, 0.4), 1.0)

        # 합성
        canvas = alpha_blend(canvas, processed, x, y, alpha)

        # 실시간 미리보기
        if PREVIEW:
            preview = cv2.resize(canvas, None, fx=0.4, fy=0.3)
            cv2.imshow("Preview", preview)
            cv2.waitKey(PREVIEW_DELAY)

    return canvas
