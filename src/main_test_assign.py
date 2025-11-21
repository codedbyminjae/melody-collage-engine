from target_processor import load_target_image, split_into_grid, get_filling_order
from tile_maker import load_tiles_from_folder
from audio_segmenter import segment_audio_brightness
from tile_assigner import assign_tiles_to_target

# ----- 1) 타겟 이미지 brightness map -----
_, gray = load_target_image("../data/images/target_strarry_night.jpg")
brightness_map = split_into_grid(gray)
target_order = get_filling_order(brightness_map)

# ----- 2) 타일 25개 brightness -----
tiles = load_tiles_from_folder("../data/images")

# ----- 3) 음악 segment brightness -----
segments = segment_audio_brightness("../data/music/epic1.mp3")

# ----- 4) 매핑 실행 -----
assigned = assign_tiles_to_target(target_order, tiles, segments)

# ----- 5) 5×5 형태로 출력 -----
grid = [[None for _ in range(5)] for _ in range(5)]

for cell in assigned:
    r = cell["row"]
    c = cell["col"]
    grid[r][c] = cell["tile"]["file"]

print("\n=== Tile Layout (5×5) ===")
for row in grid:
    print(row)
