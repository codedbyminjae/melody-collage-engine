import librosa
import numpy as np

# 오디오를 segment 단위로 나누고, 각 segment의 밝기(centroid)와 에너지 계산
def segment_audio(audio_path, segment_duration=0.5):

    # 음악 불러오기
    y, sr = librosa.load(audio_path, sr=None) # librosa 라이브러리 참조 부분

    # segment 길이 (sample 단위)
    seg_len = int(segment_duration * sr)
    total_segments = len(y) // seg_len

    brightness_list = [] # 밝기 저장
    energy_list = [] # 에너지 저장

    # segment 반복 처리
    for i in range(total_segments):

        start = i * seg_len
        end   = (i + 1) * seg_len

        seg = y[start:end]

        # 밝기 계산
        # centroid는 librosa에서 제공하는 특징값으로, 밝기와 연관되어 있어 참고하여 사용
        centroid = librosa.feature.spectral_centroid(y=seg, sr=sr) # 참고하여 적용한 부분
        brightness = float(np.mean(centroid))
        brightness_list.append(brightness)

        # 에너지 계산
        energy = float(np.sum(np.abs(seg))) # 에너지 변환 참조 코드
        energy_list.append(energy)

    # 두 리스트 반환
    return brightness_list, energy_list
