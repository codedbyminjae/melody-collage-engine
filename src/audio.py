import librosa
import numpy as np

# 음악을 segment 단위로 나누고 각 구간의 spectral centroid(밝기)를 계산한다.
def segment_audio(audio_path, segment_duration=0.5):

    # 음악 로드 (waveform y, sampling rate sr)
    y, sr = librosa.load(audio_path, sr=None)

    # segment 길이(샘플 단위) 계산
    seg_samples = int(segment_duration * sr)
    total_segments = len(y) // seg_samples

    brightness_values = []

    for i in range(total_segments): # 전체 segment 개수만큼 반복 -> 각 segment 에서 밝기를 추출
        # segment 슬라이싱
        start = i * seg_samples
        end = (i + 1) * seg_samples
        seg = y[start:end]

        if len(seg) == 0:
            continue

        # spectral centroid 계산 → segment 밝기
        centroid = librosa.feature.spectral_centroid(y=seg, sr=sr)
        # 2D배열을 하나의 밝기 대표값으로 만들기 위해 평균값으로 변환
        brightness = float(np.mean(centroid))

        brightness_values.append(brightness)

    # segment별 brightness 리스트 반환
    return brightness_values
