import os
import cv2

from audio import segment_audio
from image import load_images
from scaling import compute_scale
from collage import build_layer_collage


# brightness를 240개로 맞추는 함수
def normalize_brightness(brightness, target=240):
    brightness = brightness[:target]
    if len(brightness) < target:
        last = brightness[-1]
        brightness += [last] * (target - len(brightness))
    return brightness


def main():
    print("Melody Collage Engine 시작")

    # 1) 음악 brightness 추출
    audio_path = "../data/music/epic1.mp3"
    brightness = segment_audio(audio_path, segment_duration=0.5)
    brightness = normalize_brightness(brightness)
    print(f"음악 segment 수: {len(brightness)}")

    # 2) 이미지 로드 & 240장 확장
    images = load_images("../data/images", target_count=240, resize_to=256)
    print("이미지 로드 완료")

    # 3) brightness → scale 변환
    scales = compute_scale(brightness)
    print("스케일 계산 완료")

    # 4) 콜라주 생성
    collage = build_layer_collage(
        images, scales,
        canvas_w=1800, canvas_h=2400,
        base_min=180, base_max=380
    )

    # 5) 저장
    os.makedirs("../results", exist_ok=True)
    output_path = "../results/layer_collage.jpg"
    cv2.imwrite(output_path, collage)

    print(f"완료! 저장 경로: {output_path}")


if __name__ == "__main__":
    main()
