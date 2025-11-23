import os
import cv2

from audio_segmenter_patch import segment_audio_brightness_patch
from image_loader_repeater import load_and_repeat_images
from tile_assigner_patch import compute_scale_factors_patch
from collage_layer_builder import build_layer_collage


def main():
    print("Melody_Collage_Engine 시작")

    # 음악 분석 (0.5초 단위 brightness)
    audio_path = "../data/music/epic1.mp3"
    music_brightness = segment_audio_brightness_patch(audio_path, segment_duration=0.5)

    # brightness 길이를 240개로 맞춤
    music_brightness = music_brightness[:240]
    if len(music_brightness) < 240:
        last = music_brightness[-1]
        music_brightness += [last] * (240 - len(music_brightness))

    print(f"음악 segment 수: {len(music_brightness)}")

    # 이미지 로드 + 240장으로 확장
    images = load_and_repeat_images("../data/images", target_count=240, resize_to=256)
    print("이미지 로드 완료")

    # 음악 brightness → scale factor 변환
    scale_factors = compute_scale_factors_patch(music_brightness)
    print("스케일 계산 완료")

    # 콜라주 생성
    collage = build_layer_collage(images, scale_factors, canvas_w=1800, canvas_h=2400,
                                  base_min=180, base_max=380)

    # 저장
    os.makedirs("../results", exist_ok=True)
    output_path = "../results/layer_collage.jpg"
    cv2.imwrite(output_path, collage)

    print(f"완료!, 경로→ {output_path}")

if __name__ == "__main__":
    main()
