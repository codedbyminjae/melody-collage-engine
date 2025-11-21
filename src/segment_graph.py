import matplotlib.pyplot as plt
from audio_segmenter import segment_audio_brightness

def main():
    # 음악 segment brightness 계산
    segments = segment_audio_brightness("../data/music/epic1.mp3")

    # 그래프 생성
    plt.figure(figsize=(12, 4))
    plt.plot(segments, marker="o", linewidth=2)
    plt.title("Music Segment Brightness (25 Segments)", fontsize=16)
    plt.xlabel("Segment Index (0 ~ 24)", fontsize=12)
    plt.ylabel("Brightness (Energy)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)

    # 저장
    plt.savefig("../results/segment_graph.png", dpi=200)
    print("그래프 저장 완료 ➜ ../results/segment_graph.png")

if __name__ == "__main__":
    main()
