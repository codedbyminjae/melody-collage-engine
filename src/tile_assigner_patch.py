def compute_scale_factors_patch(brightness_values, min_scale=0.7, max_scale=1.8):
    """
    brightness -> scale factor로 변환
    음악 brightness 값을 0에서 1사이의 값으로 정규화 한 후,
    이미지 크기, 채도, 투명도 조절에 사용할 scale factor로 변환한다.
    """

    # brightness 최소·최대 (정규화 구간 계산에 필요)
    b_min = min(brightness_values)
    b_max = max(brightness_values)

    scale_factors = []

    # 각 segment의 brightness를 0~1로 정규화 후 scale로 변환
    for b in brightness_values:

        # 정규화 (min = 0, max = 1)
        if b_max == b_min:
            norm = 0.5 # bright가 모두 같은 경우
        else:
            norm = (b - b_min) / (b_max - b_min)

        # norm(0~1)을 scale 범위 (0.7~1.8)로 변환
        scale = min_scale + norm * (max_scale - min_scale)

        scale_factors.append(scale)

    return scale_factors
