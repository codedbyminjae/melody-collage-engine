## 🎧 Melody Collage Engine
---

A music-driven layer-based collage generator powered by audio brightness and OpenCV.

음악의 흐름(밝기·강약)에 따라  
이미지의 크기, 채도, 회전, 투명도가 변화하며  
랜덤 레이어 방식으로 예술적인 콜라주 이미지가 생성됩니다.

---

## 📌 Overview
---

이 프로젝트는 음악을 일정 구간(0.5초 단위)으로 나눈 뒤 spectral brightness를 기반으로  
이미지의 시각적 속성을 동적으로 조정하여, 음악의 감정 흐름을 시각화한 콜라주 작품을 생성합니다.

---

## 🛠️ Tech Stack
---

- Python 3  
- OpenCV — 이미지 변환 · 회전 · 블렌딩  
- NumPy — 수치 연산  
- Librosa — 오디오 밝기 분석  
- Random — 레이어 위치, 크기, 회전 값 생성  

---

## 📁 Project Structure
---

src/  
    main_layer_collage.py       # 엔진 실행 파일  
    audio_segmenter_patch.py    # 음악 brightness 분석  
    image_loader_repeater.py    # 이미지 리사이즈 + 반복 로딩  
    tile_assigner_patch.py      # brightness → scale factor 변환  
    collage_layer_builder.py    # 레이어 기반 콜라주 생성  

data/  
    images/                     # 입력 이미지  
    music/                      # 입력 음악 파일  

results/  
    layer_collage.jpg           # 최종 콜라주 결과물  

---

## 🚀 How It Works
---

### 1) Audio → Brightness Extraction
- 음악을 0.5초 단위로 분리  
- 각 구간의 spectral brightness 계산  
- 총 240개 segment로 맞춤  

---

### 2) Image Loading & Repeating
- 모든 이미지를 256×256으로 통일  
- 이미지 수가 부족하면 순차 반복하여 240장으로 확장  

---

### 3) Brightness → Scale Mapping
- brightness 값을 0~1로 정규화  
- 스케일 값 0.7 ~ 1.8  
- 이미지의 크기, 채도, 투명도에 반영됨  

---

### 4) Layer-Based Artistic Collage
각 이미지에 대해 다음 시각 효과 적용:

- 크기 조정 (base × scale)  
- 채도(Saturation) 강화  
- 랜덤 미세 회전  
- 랜덤 위치 배치  
- α-블렌딩으로 자연스럽게 겹침  

음악의 감정을 시각적 레이어로 표현하는 방식입니다.

---

## 🖼️ Output
---

results/  
    layer_collage.jpg  

---

## ▶️ Run the Engine
---

python main_layer_collage.py

---

## 🎨 Project Goal
---

음악의 감정선을 색감 · 크기 · 투명도로 표현한  
음악 기반 콜라주 아트워크를 생성하는 것이 목적입니다.

---

## 📌 Future Improvements
---

- 다양한 오디오 특징 추가 (energy, tempo 등)  
- 이미지 간 중첩 규칙 개선  
- 배경 스타일 옵션 추가  
- GUI 기반 실시간 콜라주 앱  

---

## 📄 License
---

This project is developed for the 영상처리 프로그래밍 course.
