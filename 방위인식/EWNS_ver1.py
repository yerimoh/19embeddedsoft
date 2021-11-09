## EWNS
import numpy as np
import pytesseract
import cv2
cap = cv2.VideoCapture("nv.avi")

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
    # Grayscale, Gaussian blur, Otsu's threshold
    gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)

  
    thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)[1]




    # Perform text extraction
    data = pytesseract.image_to_string(thresh , lang='eng', config='—psm 10')
    if data == 'W' or data == 'w' or data == 'Ww' or data == 'VV':
       print('W')
    elif data == 'S' or data == 'S,' or data == 'S;' or data == 's' or data == 's,' or data == 's;' or data ==  '»':
       print('S')
    elif data == 'N' or data == 'Ni':
       print('N')
    elif data == 'E' or data == 'a':    #  사용자 지정 예외처리
       print('N')   
    #print(data)

    cv2.imshow('thresh', thresh)
cv2.waitKey()
cv2.destroyAllWindows()