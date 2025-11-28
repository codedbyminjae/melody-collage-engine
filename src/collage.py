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
    PREVIEW_FX,
    PREVIEW_FY
)

# -------------------------------------------------
# 회전
# -------------------------------------------------
def random_rotate(img, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(
        img, M, (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )

# -------------------------------------------------
# 채도 조절
# -------------------------------------------------
def adjust_saturation(img, factor):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

# -------------------------------------------------
# 알파 블렌딩
# -------------------------------------------------
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

# -------------------------------------------------
# Flow Mode 이미지 변환 (scale·채도·회전)
# -------------------------------------------------
def process_image(img, scale, tempo_norm, energy_norm, idx, base_min, base_max):
    base = random.randint(base_min, base_max)
    size = int(base * scale)
    size = max(80, min(600, size))

    # 크기 조절
    img = cv2.resize(img, (size, size))

    # 채도 조절
    sat = (0.3 + scale * 1.4) * (0.4 + tempo_norm)
    img = adjust_saturation(img, sat)

    # 회전 조절
    rot_range = 15 + energy_norm[idx] * 30
    angle = random.uniform(-rot_range, rot_range)
    img = random_rotate(img, angle)

    return img, size

# -------------------------------------------------
# 콜라주 생성 (Flow + Random 위치 모드)
# -------------------------------------------------
def build_layer_collage(
    images, scale_factors, tempo_norm, energy_norm,
    canvas_w, canvas_h, base_min, base_max
):
    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    INTRO_MAX = 10
    OUTRO_MAX = 10
    intro_count = 0
    outro_count = 0

    for idx, img in enumerate(images):

        # -------------------------------------------------
        # Flow 기반 시각 변환 (MODE와 관계없이 동일)
        # -------------------------------------------------
        scale = scale_factors[idx]
        processed, size = process_image(
            img, scale, tempo_norm, energy_norm, idx, base_min, base_max
        )

        # -------------------------------------------------
        # Random Mode: 위치만 랜덤
        # -------------------------------------------------
        if MODE == "random":
            x = random.randint(0, canvas_w - size)
            y = random.randint(0, canvas_h - size)

        # -------------------------------------------------
        # Flow Mode: 음악 기반 위치 배치
        # -------------------------------------------------
        else:
            # 인트로: 상단 왼쪽
            if intro_count < INTRO_MAX and idx < INTRO_CUTOFF:
                intro_count += 1
                y = random.randint(0, 150)
                x = random.randint(0, int(canvas_w * 0.33))

            # 아웃트로: 하단 오른쪽
            elif outro_count < OUTRO_MAX and idx > OUTRO_CUTOFF:
                outro_count += 1

                y_min = max(canvas_h - 200, 0)
                y_max = canvas_h - size
                if y_min > y_max:
                    y_min = y_max
                y = random.randint(y_min, y_max)

                x_min = int(canvas_w * 0.66)
                x_max = canvas_w - size
                if x_min > x_max:
                    x_min = x_max
                x = random.randint(x_min, x_max)

            # 중간 구간: 랜덤 + 음악 흐름 혼합
            else:
                # 음악 시간 흐름 기반 y
                t_y = int((idx / TARGET_COUNT) * canvas_h)
                y_rand = random.randint(0, canvas_h - size)
                y = int(0.8 * y_rand + 0.2 * t_y)
                y = min(max(y, 0), canvas_h - size)

                # x는 전체 랜덤
                x = random.randint(0, canvas_w - size)

        # -------------------------------------------------
        # 투명도 (Flow 기반)
        # -------------------------------------------------
        alpha = min(max(0.65 + scale * 0.25, 0.4), 1.0)

        # 합성
        canvas = alpha_blend(canvas, processed, x, y, alpha)

        # -------------------------------------------------
        # 실시간 미리보기
        # -------------------------------------------------
        if PREVIEW:
            preview = cv2.resize(canvas, None, fx=PREVIEW_FX, fy=PREVIEW_FY)
            cv2.imshow("Preview", preview)
            cv2.waitKey(PREVIEW_DELAY)

    return canvas
