from image_features import ImageFeatureExtractor
from audio_analysis import AudioAnalysis

def main():
    print("이미지 특징 추출 시작")

    extractor = ImageFeatureExtractor("../data/images")
    results = extractor.extract_all()

    print("\n 이미지 분석 결과:")
    print(results)

    print("\n 음악 분석 시작")

    audio_analysis = AudioAnalysis("../data/music/epic1.mp3")
    audio_results = audio_analysis.analyze()

    print("\n 음악 분석 결과")
    print(audio_results)

if __name__ == "__main__":
    main()
