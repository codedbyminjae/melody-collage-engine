# 🎧 Melody Collage Engine
A music-driven collage generator that analyzes audio emotions and matches them with image features using OpenCV.

---

## 📌 Project Overview
This project creates an artistic collage based on the emotional flow of music.  
Audio features (tempo, energy, brightness) are extracted and matched with image features (HSV colors, brightness, texture) to generate a dynamic, visually expressive collage.

---

## 🛠️ Tech Stack
- **Python 3**
- **OpenCV** — image processing
- **NumPy** — numerical operations
- **Librosa** — audio analysis
- **Scikit-Image** — texture & feature extraction

---

## 📁 Project Structure
```text
src/
    main.py              # Entry point
    audio_analysis.py    # Music emotion analysis
    image_features.py    # Image feature extraction (HSV, brightness, texture)
    collage_builder.py   # Collage layout generator

data/
    images/              # Input images for collage
    music/               # Input audio files

results/
    collages/            # Generated collage outputs

🚀 Features (Planned)

Extract HSV color features from images

Analyze music tempo, energy, and emotion

Match audio segments with best-fitting images

Generate non-grid, expressive collage visuals

Export final collage as image output

📌 Goal

Visualize the emotional flow of music using image-based collage artistry, combining audio analysis and classical image-processing techniques.