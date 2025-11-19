from typing import List
from tile import Tile

# 1. Brightness-based placement (가장 기본)
def place_tiles_by_brightness(tiles: List[Tile], grid_w: int, grid_h: int):
    tiles_sorted = sorted(tiles, key=lambda t: t.brightness)

    required = grid_w * grid_h
    selected = tiles_sorted[:required]

    return _build_layout(selected, grid_w, grid_h)

# Edge-based placement (에지 강한 순)
def place_tiles_by_edge(tiles: List[Tile], grid_w: int, grid_h: int):
    tiles_sorted = sorted(tiles, key=lambda t: t.edge_density, reverse=True)

    required = grid_w * grid_h
    selected = tiles_sorted[:required]

    return _build_layout(selected, grid_w, grid_h)

# Hue-based placement (색상 그라데이션)
def place_tiles_by_hue(tiles: List[Tile], grid_w: int, grid_h: int):
    tiles_sorted = sorted(tiles, key=lambda t: t.hue)

    required = grid_w * grid_h
    selected = tiles_sorted[:required]

    return _build_layout(selected, grid_w, grid_h)

# Audio-driven placement
def place_tiles_with_audio(tiles: List[Tile], grid_w: int, grid_h: int,
                           music_brightness: float,
                           beat_strength: float):
    """
    음악 특징값(밝기 + 비트)을 이용해 타일 선택
    - 밝은 음악: 밝은 이미지 우선
    - 강한 비트: edge 밀도가 높은 이미지 우선
    """

    # 1) brightness 기준 가중치
    tiles_sorted = sorted(
        tiles,
        key=lambda t: _audio_weight(t, music_brightness, beat_strength),
        reverse=True
    )

    required = grid_w * grid_h
    selected = tiles_sorted[:required]

    return _build_layout(selected, grid_w, grid_h)

# 내부 로직 — 오디오 기반 가중치 계산
def _audio_weight(tile: Tile, music_brightness: float, beat_strength: float):
    """
    음악 특징을 기준으로 이미지 특징과 매칭하는 가중치 계산
    """
    # 밝음 매칭
    brightness_score = (tile.brightness / 255) * music_brightness

    # 비트 ↔ edge 밀도
    edge_score = tile.edge_density * beat_strength

    # 두 요소 혼합
    return brightness_score * 0.6 + edge_score * 0.4

# 공통 레이아웃 생성 함수 (2D 형태로 타일 배치)
def _build_layout(selected_tiles: List[Tile], grid_w: int, grid_h: int):
    layout = []
    idx = 0
    for _ in range(grid_h):
        row = []
        for _ in range(grid_w):
            row.append(selected_tiles[idx])
            idx += 1
        layout.append(row)
    return layout
