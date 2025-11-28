import os
import cv2
import numpy as np

from audio import segment_audio
from image import load_images
from scaling import compute_scale
from collage import build_layer_collage
from rotate import rotate_with_click_and_save

from config import (
    CANVAS_W, CANVAS_H,
    TARGET_COUNT, RESIZE_TO,
    BASE_MIN, BASE_MAX,
    MODE,
)

# 고정 길이 보정
def normalize_target(arr, target=240):
    arr = arr[:target]
    if len(arr) < target:
        arr += [arr[-1]] * (target - len(arr))
    return arr


def main():
    print("Melody Collage Engine 시작")
    print(f"MODE: {MODE}")

    # 1) 오디오 분석
    audio_path = "../data/music/epic1.mp3"
    brightness, tempo, energy = segment_audio(audio_path, segment_duration=0.5)

    tempo = float(tempo)
    print(f"Tempo: {tempo:.2f}")

    # 데이터 길이 보정
    brightness = normalize_target(brightness, TARGET_COUNT)
    energy = normalize_target(energy, TARGET_COUNT)

    print(f"Segments: {len(brightness)}")

    # 정규화
    tempo_norm = min(max((tempo - 60) / 120, 0), 1)

    energy_arr = np.array(energy)
    energy_norm = (energy_arr - np.min(energy_arr)) / (np.max(energy_arr) - np.min(energy_arr))
    energy_norm = energy_norm.tolist()

    # 2) 이미지 로드
    images = load_images("../data/images", target_count=TARGET_COUNT, resize_to=RESIZE_TO)
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

    # 5) 저장 및 회전 UI 실행
    os.makedirs("../results", exist_ok=True)

    preview_path = "../results/collage_preview.jpg"
    final_path = "../results/collage_final.jpg"

    cv2.imwrite(preview_path, collage)
    print(f"프리뷰 저장: {preview_path}")

    print("\n=== 회전 모드 실행 ===")
    print("좌클릭: 90° 회전 | ENTER: 저장 | ESC: 취소\n")

    rotate_with_click_and_save(preview_path, final_path)

    print(f"최종 저장 완료: {final_path}")
    print("프로그램 종료!")

if __name__ == "__main__":
    main()
