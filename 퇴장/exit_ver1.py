# exit
import numpy as np
import cv2

cap = cv2.VideoCapture("/Users/han/Documents/study/python_OpenCV/11:5 영상자료/선보고걸어가기(25도).avi")

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
    img_frame = cv2.GaussianBlur(img_frame, (5,5) ,0)
    img_hsv=cv2.cvtColor(img_frame, cv2.COLOR_BGR2HSV_FULL)


    ## 물체 mask
    img_mask_road = cv2.inRange(img_hsv, (10, 100, 100), (40, 255, 180)) #중간값이 hsv lower, 오른쪽값이 hsv upper

    ## x=0 pixel에서 y값의 개수찾기
    if np.count_nonzero(img_mask_road[:,0]) > 88: #88 = reference value
        print("출구 길 확인")
        
    cv2.imshow("contour",img_mask_road)

cv2.waitKey()
cv2.destroyAllWindows()