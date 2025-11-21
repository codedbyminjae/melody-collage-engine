import librosa
import numpy as np

# 음악을 25등분 하고 각 segmnet의 밝기 계산
def segment_audio_brightness(audio_path, segments=25):
    y, sr = librosa.load(audio_path, sr=None)

    total_len = len(y)
    seg_len = total_len // segments

    segment_vals = []

    for i in range(segments):
        start = i * seg_len
        end = (i + 1) * seg_len

        seg = y[start:end]

        # segment brightness = 절대값 평균 (기본 에너지)
        brightness = float(np.mean(np.abs(seg)))
        segment_vals.append(brightness)

    return segment_vals
