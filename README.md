<p align="center">
  <img src="results/collage_preview.jpg" width="200">
</p>

## 🎧 Melody Collage Engine
---
음악의 흐름(밝기 · 강약 · 에너지)에 따라  
이미지의 **크기 · 채도 · 회전 · 투명도**가 동적으로 변화하며  
OpenCV 기반 레이어 방식으로 음악 기반 콜라주 아트워크를 생성하는 엔진입니다.

---

## 📌 Overview
---
이 프로젝트는 음악을 0.5초 단위로 분할한 뒤  
각 구간의 **spectral brightness / energy / tempo**를 분석하여  
이미지의 시각적 속성을 변화시키는 방식으로  
음악의 감정선과 흐름을 시각적으로 표현한 콜라주를 생성합니다.

---

## 🛠️ Tech Stack
---
- Python 3  
- OpenCV — 이미지 변환 · 회전 · 블렌딩  
- NumPy — 수치 연산  
- Librosa — 오디오 밝기 & 에너지 분석  
- Random — 위치, 크기, 회전 값 생성  

---

## 📁 Project Structure
---
src/  
    main.py                  # 엔진 실행 파일  
    audio.py                 # 오디오 분석(밝기/에너지)  
    image.py                 # 이미지 로더 + 반복 로딩  
    scaling.py               # brightness → scale 변환  
    collage.py               # 레이어 기반 콜라주 생성  
    rotate.py                # 결과 이미지 회전 UI  

data/  
    images/                  # 입력 이미지  
    music/                   # 입력 음악  

results/  
    collage_preview.jpg      # 프리뷰  
    collage_final.jpg        # 최종 결과물  

---

## 🚀 How It Works
---
### 1) Audio → Brightness Extraction  
- 음악을 0.5초 단위로 분할  
- spectral centroid 기반 brightness 계산  
- energy & tempo 분석  
- 240개 segment로 정규화  

### 2) Image Loading  
- 모든 이미지를 지정 크기로 리사이즈  
- 부족하면 순차 반복하여 총 240장 확보  

### 3) Brightness → Scale Mapping  
- brightness를 0~1로 정규화  
- 스케일 0.7 ~ 1.8 매핑  
- 이미지 크기 · 채도 · 투명도 반영  

### 4) Layer-Based Artistic Collage  
각 이미지에 대해 다음 효과 적용:  
- 크기 조정  
- 채도 조절  
- 랜덤 회전  
- 랜덤 위치 배치  
- α-블렌딩  

음악의 감정 흐름을 레이어 구조로 시각적으로 표현합니다.

---

## 🖼️ Output
---
results/  
    collage_final.jpg  

---

## ▶️ Run the Engine
---
```bash
python src/main.py
```

---

## 🎨 Project Goal
---
음악의 밝기, 에너지, 리듬에 기반하여  
**동적으로 변화하는 시각적 콜라주 아트워크**를 생성하는 것이 목표입니다.

---

## 📌 Future Improvements
---
- 다양한 오디오 특징 추가 (MFCC, beat tracking 등)  
- 이미지 중첩 규칙 개선  
- 렌더링 속도 최적화  
- GUI 기반 실시간 아트워크 생성  

---

## 📄 License
---
This project was developed for the **영상처리 프로그래밍** course.
