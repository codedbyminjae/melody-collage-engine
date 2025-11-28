import os
import cv2
import numpy as np

from audio import segment_audio
from image import load_images
from scaling import compute_scale
from collage import build_layer_collage
from config import CANVAS_W, CANVAS_H, TARGET_COUNT, RESIZE_TO, BASE_MIN, BASE_MAX


def normalize_target(arr, target):
    arr = arr[:target]
    if len(arr) < target:
        arr += [arr[-1]] * (target - len(arr))
    return arr


def main():
    print("Melody Collage Engine 시작")

    # 1) 음악 분석
    brightness, tempo, energy = segment_audio("../data/music/epic1.mp3", segment_duration=0.5)
    tempo = float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo)
    print(f"tempo(raw): {tempo:.2f}")

    brightness = normalize_target(brightness, TARGET_COUNT)
    energy = normalize_target(energy, TARGET_COUNT)
    print(f"segment 개수: {len(brightness)}")

    tempo_norm = min(max((tempo - 60) / 120, 0), 1)
    energy_norm = (np.array(energy) - min(energy)) / (max(energy) - min(energy))
    energy_norm = energy_norm.tolist()

    # 2) 이미지 로드
    images = load_images("../data/images", TARGET_COUNT, RESIZE_TO)
    print("이미지 로드 완료")

    # 3) 스케일 계산
    scales = compute_scale(brightness)
    print("스케일 계산 완료")

    # 4) 콜라주 생성
    collage = build_layer_collage(
        images, scales, tempo_norm, energy_norm,
        canvas_w=CANVAS_W, canvas_h=CANVAS_H,
        base_min=BASE_MIN, base_max=BASE_MAX
    )
    print("콜라주 생성 완료")

    # 5) 저장
    os.makedirs("../results", exist_ok=True)
    output = "../results/collage.jpg"
    cv2.imwrite(output, collage)
    print(f"저장 완료 → {output}")

    # ENTER로 종료
    print("프리뷰 창에서 ENTER를 누르면 종료됩니다.")

    while True:
        if cv2.waitKey(0) & 0xFF in [13, 10, ord('\r')]:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
