from image_features import ImageFeatureExtractor

def main():
    print("이미지 특징 추출 시작")

    extractor = ImageFeatureExtractor("../data/images")
    results = extractor.extract_all()

    print("\n 추출된 결과:")
    print(results)

if __name__ == "__main__":
    main()
