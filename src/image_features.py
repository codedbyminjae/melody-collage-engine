import cv2
import numpy as np
import os

class ImageFeatureExtractor:
    def __init__(self, folder_path):  # 이미지가 들어있는 경로 저장 함수
        self.folder_path = folder_path

    def extract_all(self):  # 폴더 안의 이미지를 모두 읽고 특징 추출 함수
        results = []  # 결과 저장 리스트

        for file in os.listdir(self.folder_path): # os.listdir 함수 사용 <- 파일 이름 목록을 리스트로 가져오는 함수
            # 전체 이미지 파일 중 우선은 jpg와 png 확장자의 이미지만 처리
            if not (file.lower().endswith(".jpg") or file.lower().endswith(".png")):
                continue

            img_path = os.path.join(self.folder_path, file)
            img = cv2.imread(img_path)

            if img is None:  # 이미지 리딩 실패시
                print("이미지 읽기 실패")
                continue

            features = self.extract_features(img)  # 이미지 특징 추출

            results.append({  # 파일명과 특징 저장
                "file": file,
                "features": features
            })

        # 폴더 내 이미지 없을 경우의 메시지
        if len(results) == 0:
            print("No image")

        return results

    def extract_features(self, img):
        # HSV 평균, 색상, 채도, 밝기
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 전체 픽셀을 (N, 3) 형태로 펼쳐서 HSV 각 평균
        h_mean, s_mean, v_mean = np.mean(hsv.reshape(-1, 3), axis=0)

        # 밝기
        # 흑백으로 변환 후 전체 평균 값 = 이미지 밝기 정도
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)

        # Edge Density (경계선 비율)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / (img.shape[0] * img.shape[1])

        return {
            # float으로 변환 이유 = 추후 numpy숫자 오류 방지
            "hue": float(h_mean),
            "saturation": float(s_mean),
            "value": float(v_mean),
            "brightness": float(brightness),
            "edge_density": float(edge_density)
        }
