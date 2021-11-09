#바닥 인식
import numpy as np
import cv2

cap = cv2.VideoCapture("영상파일 후반부/확진지역_빨강_파랑2.avi")

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

    # input image, name color
    img_hsv=cv2.cvtColor(img_frame, cv2.COLOR_BGR2HSV_FULL)

    #mask 를 찾은뒤 pixel 개수 찾기
    green_sum=np.sum(cv2.inRange(img_hsv, (40, 30, 10), (100, 255, 255)))
    black_sum=np.sum(cv2.inRange(img_hsv, (0, 0, 0), (255, 255, 80)))
    
    # print(red_sum)
    if green_sum >= black_sum:
        print("안전지역")
    else:
        print("확진지역")


cv2.waitKey()
cv2.destroyAllWindows()