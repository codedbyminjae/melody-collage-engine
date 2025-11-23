import cv2
import numpy as np
import random


# 이미지를 특정 각도만큼 회전시키는 함수
def random_rotate(img, angle):
    # 이미지 높이·너비
    h, w = img.shape[:2]

    # 회전 중심 (이미지 정중앙)
    center = (w // 2, h // 2)

    # 회전에 필요한 2D 변환 행렬 생성
    # 중심(center)을 기준으로 angle 만큼 회전하는 변환 행렬 생성
    # scale=1.0은 크기 변화 없이 회전만 적용
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)

    # 회전 적용
    # warpAffine: 변환 행렬(rot_mat)을 이용해 이미지 재배치
    # 출력 크기는 원본 크기(w, h) 그대로 유지
    # 회전으로 생기는 이미지 내부의 빈 영역은 BORDER_REFLECT로 자연스럽게 채움
    rotated = cv2.warpAffine(
        img, rot_mat, (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )

    return rotated

# 이미지의 채도를 조절하는 함수
def adjust_saturation(img, factor):
    # BGR -> HSV 변환 (Saturation만 조정하기 위해)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    # 채도에 factor 적용
    img_hsv[:, :, 1] *= factor
    # 채도 범위를 255 까지로 제한
    img_hsv[:, :, 1] = np.clip(img_hsv[:, :, 1], 0, 255)
    # 다시 HSV -> BGR로 변환
    return cv2.cvtColor(img_hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

def alpha_blend(canvas, img, x, y, alpha):
    # 새로운 이미지 크기
    h, w = img.shape[:2]

    # 캔버스 크기 
    H, W = canvas.shape[:2]
    # 이미지가 캔버스를 넘어가는 경우 잘라내기
    if x + w > W or y + h > H:
        w = min(w, W - x)
        h = min(h, H - y)
        img = img[:h, :w]
        
    # 완전히 영역 밖이면 작업하지 않음
    if w <= 0 or h <= 0:
        return canvas

    # 캔버스에서 img가 들어갈 부분
    roi = canvas[y:y+h, x:x+w]

    # ROI와 img를 투명도(alpha) 비율로 섞기
    # - roi * (1 - alpha): 기존 캔버스가 차지하는 비율
    # - img * alpha      : 새 이미지가 차지하는 비율
    # alpha=1.0 이면 img가 완전히 덮고,
    # alpha<1.0 이면 두 이미지가 자연스럽게 섞임
    # α-블렌딩 공식: output = A*(1-α) + B*α
    blended = (roi * (1 - alpha) + img * alpha).astype(np.uint8)

    # 블렌딩 결과 캔버스에 반영
    canvas[y:y+h, x:x+w] = blended
    return canvas

def build_layer_collage(images, scale_factors,
                        canvas_w=1800, canvas_h=2400,
                        base_min=180, base_max=380):
    """
    음악 기반 콜라주 생성 함수.
    - 이미지마다: 크기 조정 → 채도 강화 → 회전 → 위치 지정 → 투명도 블렌딩
    - scale_factors는 음악 brightness로부터 계산된 스케일 값
    """

    # 비어 있는 캔버스 생성 (검정 배경)
    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    for idx, img in enumerate(images):
        scale = scale_factors[idx]

        # 1) 이미지 크기 결정 (음악 scale + 랜덤성)
        base = random.randint(base_min, base_max)
        final_size = int(base * scale)
        final_size = max(80, min(600, final_size))  # 너무 크거나 작지 않도록 제한

        resized = cv2.resize(img, (final_size, final_size))

        # 2) 음악 기반 색조 보정 (채도 강화)
        # 변화가 눈에 보이도록 강화된 공식 사용
        sat_factor = 0.3 + scale * 1.4
        resized = adjust_saturation(resized, sat_factor)

        # 3) 랜덤 회전 (미세하게 기울여 콜라주 느낌)
        angle = random.uniform(-5, 5)
        rotated = random_rotate(resized, angle)

        # 4) 캔버스 내 랜덤 배치
        x = random.randint(0, canvas_w - final_size)
        y = random.randint(0, canvas_h - final_size)

        # 5) 음악 기반 투명도
        alpha = 0.65 + scale * 0.25
        alpha = min(max(alpha, 0.4), 1.0)

        # 6) 캔버스에 블렌딩
        canvas = alpha_blend(canvas, rotated, x, y, alpha)

    return canvas
