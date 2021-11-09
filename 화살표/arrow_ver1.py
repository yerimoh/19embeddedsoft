#화살표
import numpy as np
import cv2

cap = cv2.VideoCapture("/Users/han/Documents/study/python_OpenCV/영상녹화본/화살표 오른쪽 video.mp4")

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
    img_copy = img_frame.copy()
    src=cv2.cvtColor(img_copy, cv2.COLOR_RGB2GRAY)
    src=cv2.threshold(src, 70, 255, cv2.THRESH_BINARY_INV)[1]

    sobel_x = cv2.Sobel(src,cv2.CV_64F,1,0,ksize=3)
    sobel_y = cv2.Sobel(src,cv2.CV_64F,0,1,ksize=3)
    sobel  = cv2.addWeighted (sobel_x , 1, sobel_y, 1, 0)

    x_point= np.nonzero(sobel)[0]
    y_point = np.nonzero(sobel)[1]
    listy_non = y_point.tolist()
    listx_non = x_point.tolist()

    # 길이
    length = x_point.size

    left = 0
    right = 0
    for i in range(length-1):
        if listx_non[i] > 320:
            right +=1
        elif listx_non[i] < 320:
            left+=1
    print(left)
    print(right)
    if right > left:
        print("right")
    else:
        print("left")

    cv2.imshow('',sobel)

cv2.waitKey()
cv2.destroyAllWindows()