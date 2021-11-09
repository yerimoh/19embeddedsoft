#ABCD
import numpy as np
import pytesseract
import cv2
cap = cv2.VideoCapture("영상녹화본/B video.avi")

if cap.isOpened() == False:
    print("카메라를 열 수 없습니다.")
    exit(1)

while(True):
    ret,img_frame = cap.read()
    if ret==False:
        print("캡쳐 실패")
        break
    key=cv2.waitKey(1)
    if key==27:
        break
    img_copy = img_frame.copy()
    img_hsv=cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV_FULL)

    # 범위내 픽셀을 찾기
    img_mask_blue = cv2.inRange(img_hsv, (140, 30, 30), (160, 220, 80))
    img_mask_red = cv2.inRange(img_hsv, (160, 30, 30), (360, 255, 255))
    # 각 색상 픽셀 개수 구해서 비교
    if np.sum(img_mask_red) >= np.sum(img_mask_blue):
        print("red text")
    else:
        print("blue text")

    # text 인식
    # Grayscale, Gaussian blur, Otsu's threshold
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    
    # Perform text extraction
    data = pytesseract.image_to_string(invert, lang='eng', config=(" --psm 10"))
    print("--> ", data)

cv2.waitKey()
cv2.destroyAllWindows()