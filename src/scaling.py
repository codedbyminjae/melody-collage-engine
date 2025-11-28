def compute_scale(brightness_values, min_scale=0.7, max_scale=1.8):
    # brightness 최소/최대 계산
    b_min = min(brightness_values)
    b_max = max(brightness_values)

    scale_factors = []

    for b in brightness_values:
        # brightness -> 0~1 정규화
        if b_max == b_min:
            norm = 0.5      # 값이 모두 같을 때
        else:
            norm = (b - b_min) / (b_max - b_min)

        # 정규화값을 scale 범위로 매핑
        scale = min_scale + norm * (max_scale - min_scale)
        scale_factors.append(scale)

    # segment별 scale factor 리스트 반환
    return scale_factors
