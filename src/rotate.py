import cv2
from config import PREVIEW_FX, PREVIEW_FY

# 회전 상태 변수
angle = 0
orig = None
rot = None
center = None

# 좌클릭 → 90도 회전
def onMouse(event, x, y, flags, param):
    global angle, rot, orig, center

    if event == cv2.EVENT_LBUTTONDOWN:
        angle = (angle + 90) % 360

        # 회전 행렬
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        # 이미지 회전
        rot = cv2.warpAffine(orig, M, (orig.shape[1], orig.shape[0]))

        # 프리뷰 표시 (config 기반 스케일)
        preview = cv2.resize(rot, None, fx=PREVIEW_FX, fy=PREVIEW_FY)
        cv2.imshow("Preview", preview)

# 회전 UI → ENTER 저장 / ESC 취소
def rotate_with_click_and_save(input_path, output_path):
    global orig, rot, center, angle

    # 원본 이미지 로드 (컬러 유지)
    orig = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if orig is None:
        raise Exception(f"이미지 로드 실패: {input_path}")

    rot = orig.copy()
    h, w = orig.shape[:2]
    center = (w // 2, h // 2)
    angle = 0

    # 초기 프리뷰 표시
    preview = cv2.resize(rot, None, fx=PREVIEW_FX, fy=PREVIEW_FY)
    cv2.imshow("Preview", preview)
    cv2.setMouseCallback("Preview", onMouse)

    # 입력 대기
    while True:
        key = cv2.waitKey(0)

        # ENTER → 저장
        if key == 13:
            cv2.imwrite(output_path, rot)
            print(f"[INFO] 저장 완료: {output_path}")
            break

        # ESC → 취소
        elif key == 27:
            print("[INFO] 회전 취소")
            break

    cv2.destroyAllWindows()
