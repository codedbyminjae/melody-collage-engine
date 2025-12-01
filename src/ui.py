import cv2
from collage import rotate_image

def rotate_ui(input_path, output_path):

    original = cv2.imread(input_path)   # 원본 이미지
    preview = original.copy()           # 회전된 이미지(표시용)
    angle = 0                           # 누적 회전값

    # 미리보기 창 첫 표시
    disp = cv2.resize(preview, None, fx=0.45, fy=0.45)
    cv2.imshow("Preview", disp)
    cv2.moveWindow("Preview", 100, 100)

    # 마우스 클릭 이벤트 (교재 참고)
    def on_mouse(event, x, y, flags, param):
        nonlocal preview, angle
        if event == cv2.EVENT_LBUTTONDOWN:
            angle += 90                      # 누적 회전
            preview = rotate_image(original, angle)  # ✔ 원본 기준 회전
            disp2 = cv2.resize(preview, None, fx=0.45, fy=0.45)
            cv2.imshow("Preview", disp2)
            cv2.moveWindow("Preview", 100, 100)

    cv2.setMouseCallback("Preview", on_mouse)

    # 키 입력 루프
    while True:
        disp = cv2.resize(preview, None, fx=0.45, fy=0.45)
        cv2.imshow("Preview", disp)

        key = cv2.waitKey(10)

        if key == 13: # Enter → 저장
            print("회전된 이미지 저장")
            cv2.imwrite(output_path, preview)
            break

        if key == 27: # ESC → 종료
            print("원본 이미지만 저장")
            break

    cv2.destroyAllWindows()
