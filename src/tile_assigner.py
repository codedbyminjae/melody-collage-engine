def assign_tiles_to_target(target_order, tile_list, segment_brightness):
    """
    target_order: 타겟 이미지 밝기순 정렬 리스트 (len=25)
    tile_list: 타일 이미지 brightness 리스트 (len=25)
    segment_brightness: 음악 segment brightness 리스트 (len=25)
    return: 5x5 위치에 어떤 tile이 들어갈지 매핑된 리스트
    """

    # 음악 segment brightness 오름차순 정렬
    seg_sorted = sorted(
        list(enumerate(segment_brightness)),
        key=lambda x: x[1]
    )
    # seg_sorted = [(segment_index, brightness), ...]

    # 타일 밝기 기준 정렬
    tiles_sorted = sorted(
        tile_list,
        key=lambda x: x["brightness"]
    )
    # tiles_sorted[i] → i번째로 어두운 타일

    # segment brightness 순서대로 타일 매칭
    # segment 0 → 가장 어두운 tile
    segment_to_tile = {}
    for i in range(25):
        seg_idx = seg_sorted[i][0]
        segment_to_tile[seg_idx] = tiles_sorted[i]

    # target brightness 순서에 segment 결과를 배치
    # 타겟 이미지 밝기 map도 25개니까 index 0~24
    assigned = []
    for i, target_cell in enumerate(target_order):
        tile = segment_to_tile[i]   # i번째 segment tile 배치
        assigned.append({
            "row": target_cell["row"],
            "col": target_cell["col"],
            "tile": tile,
        })

    return assigned
