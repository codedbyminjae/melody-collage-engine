import cv2
import numpy as np
import random


# 회전
def random_rotate(img, angle):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h),
                          flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REFLECT)


# 채도 조절
def adjust_saturation(img, factor):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


# 알파 블렌딩
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


# 단일 이미지 처리
def process_image(img, scale, tempo_norm, energy_norm, idx, base_min, base_max):
    # 크기 결정
    base = random.randint(base_min, base_max)
    size = int(base * scale)
    size = max(80, min(600, size))

    img = cv2.resize(img, (size, size))

    # tempo 기반 채도 조절
    sat_factor = (0.3 + scale * 1.4) * (0.4 + tempo_norm)
    img = adjust_saturation(img, sat_factor)

    # 에너지 기반 회전: 조용한 구간=작은 회전 / 에너지 높은 구간=강한 회전
    rotation_range = 10 + energy_norm[idx] * 40
    angle = random.uniform(-rotation_range, rotation_range)
    img = random_rotate(img, angle)

    return img, size


# 콜라주 생성
def build_layer_collage(images, scale_factors, tempo_norm, energy_norm,
                        canvas_w=1800, canvas_h=2400,
                        base_min=180, base_max=380):

    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    for idx, img in enumerate(images):
        scale = scale_factors[idx]

        # 인트로/아웃트로 강조
        if idx < 40:
            scale *= 0.85
        elif idx > 200:
            scale *= 1.15

        # 에너지 + 템포 + 밝기 모두 반영해 이미지 처리
        processed, size = process_image(
            img, scale, tempo_norm, energy_norm, idx, base_min, base_max
        )

        # 랜덤 위치
        x = random.randint(0, canvas_w - size)
        y = random.randint(0, canvas_h - size)

        # 투명도(밝기 기반)
        alpha = min(max(0.65 + scale * 0.25, 0.4), 1.0)

        canvas = alpha_blend(canvas, processed, x, y, alpha)

    return canvas
