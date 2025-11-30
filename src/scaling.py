def compute_scale(brightness_list, min_scale=0.7, max_scale=1.8):

    # brightness 최소/최대 계산
    b_min = min(brightness_list)
    b_max = max(brightness_list)

    scale_list = []

    for b in brightness_list:
        # brightness 0~1사이의 값으로 정규화
        if b_max == b_min: # 값이 같을때의 예외처리 (분모가 0인 경우)
            norm = 0.5
        else:
            norm = (b - b_min) / (b_max - b_min)

        # 정규화값을 scale 범위로 매핑 (0.7 ~ 1.8 사이)
        scale = min_scale + norm * (max_scale - min_scale)
        scale_list.append(scale)

    # segment별 scale 리스트 반환
    return scale_list
