import librosa as lr
import numpy as np

class AudioAnalysis:
    def __init__(self, music_path): # 분석 대상 음악 파일 경로 저장
        self.music_path = music_path

    def analyze(self): # 음악의 주요 특징값 추출
        # 음악 파일 업로드
        y, sr = lr.load(self.music_path)

        # Tempo (bpm)
        tempo, _ = lr.beat.beat_track(y = y, sr = sr)

        # Energy
        energy = float(np.mean(y**2))

        # Spectral Centroid
        spectral_centroid = lr.feature.spectral_centroid(y = y, sr = sr)
        brightness = float(np.mean(spectral_centroid))

        # 결과
        return {
            "tempo": float(tempo),
            "energy": float(energy),
            "brightness": (brightness),
        }