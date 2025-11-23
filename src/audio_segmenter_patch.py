import librosa
import numpy as np

def segment_audio_brightness_patch(audio_path, segment_duration=0.5):
    """
    음악 → librosa.load
    0.5초 길이만큼 slicing
    각 구간에서 spectral centroid(밝기) 계산
    결과를 brightness 리스트로 누적
    """

    # 음악 파일 로드 (mp3 _> waveform 형태로 변환)
    y, sr = librosa.load(audio_path, sr=None)

    # segment당 샘플 수
    seg_samples = int(segment_duration * sr)
    # 전체 segment 개수
    total_segments = len(y) // seg_samples

    brightness_values = []

    for i in range(total_segments):
        # i번째 segment 추출
        seg = y[i * seg_samples : (i + 1) * seg_samples]

        if len(seg) == 0:
            continue

        # Spectral Centroid  = 해당 구간의 음악 밝기
        centroid = librosa.feature.spectral_centroid(y=seg, sr=sr)
        brightness = float(np.mean(centroid))

        brightness_values.append(brightness)

    # print(f"음악 segment 추출 완료") 디버깅용 확인 코드
    return brightness_values
