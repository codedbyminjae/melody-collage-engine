import os
import cv2
import numpy as np

from audio import segment_audio
from image import load_images
from scaling import compute_scale
from collage import build_layer_collage
from config import (
    CANVAS_W, CANVAS_H,
    TARGET_COUNT, RESIZE_TO,
    BASE_MIN, BASE_MAX,
    MODE
)


# 리스트 길이 고정
def normalize_target(arr, target=240):
    arr = arr[:target]
    if len(arr) < target:
        arr += [arr[-1]] * (target - len(arr))
    return arr


def main():
    print("Melody Collage Engine 시작")
    print(f"MODE: {MODE}")

    # --- 음악 분석 ---
    audio_path = "../data/music/epic1.mp3"
    brightness, tempo, energy = segment_audio(audio_path, segment_duration=0.5)

    # tempo 처리
    tempo = float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo)
    print(f"tempo(raw): {tempo:.2f}")

    brightness = normalize_target(brightness, TARGET_COUNT)
    energy = normalize_target(energy, TARGET_COUNT)
    print(f"segments: {len(brightness)}")

    # 정규화
    tempo_norm = min(max((tempo - 60) / 120, 0), 1)
    energy_arr = np.array(energy)
    energy_norm = (energy_arr - np.min(energy_arr)) / (np.max(energy_arr) - np.min(energy_arr))
    energy_norm = energy_norm.tolist()

    # --- 이미지 로드 ---
    images = load_images("../data/images", target_count=TARGET_COUNT, resize_to=RESIZE_TO)
    print("이미지 로드 완료")

    # --- 스케일 계산 ---
    scales = compute_scale(brightness)
    print("스케일 계산 완료")

    # --- 콜라주 생성 ---
    collage = build_layer_collage(
        images, scales, tempo_norm, energy_norm,
        canvas_w=CANVAS_W, canvas_h=CANVAS_H,
        base_min=BASE_MIN, base_max=BASE_MAX
    )
    print("콜라주 생성 완료")

    # --- 저장 ---
    os.makedirs("../results", exist_ok=True)
    output_path = "../results/collage.jpg"
    cv2.imwrite(output_path, collage)
    print(f"저장 완료 → {output_path}")

    # --- ENTER로 종료 ---
    print("ENTER를 누르면 종료됩니다.")
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key in [13, 10, ord('\r')]:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
