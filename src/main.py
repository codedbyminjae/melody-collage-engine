import os
import cv2

from audio import segment_audio
from image import load_images
from scaling import compute_brightness, compute_energy
from collage import build_collage

print("Melody Collage Engine")

# 1. 오디오 분석
audio_path = "../data/music/epic1.mp3"
print(f"음악 분석 시작 : {audio_path}")

brightness_list, energy_list = segment_audio(audio_path, segment_duration=0.5)
print(f" - brightness 추출 완료 ({len(brightness_list)}개)")
print(f" - energy 추출 완료 ({len(energy_list)}개)")

# 2. 이미지 로드
print("\n이미지 로드 시작")
images = load_images("../data/images", target=301, resize=256)
print(f" - 이미지 {len(images)}개 사용")

# 3. 밝기 → 크기(scale), 에너지 → 회전(rotation)
scale_list = compute_brightness(brightness_list)
rotation_list = compute_energy(energy_list)
print("scale_list 계산 완료")
print("rotation_list 계산 완료")

# 4. 콜라주 생성
print("\n콜라주 생성 시작")
canvas = build_collage(images, scale_list, rotation_list, canvas_w=1920, canvas_h=1080)
print("콜라주 생성 완료")

# 5. 저장
print("\n결과 저장")

os.makedirs("../results", exist_ok=True)
result_path = "../results/collage_result.jpg"
cv2.imwrite(result_path, canvas)

print(f" - 저장 완료: {result_path}")
print("\n프로그램 종료")
