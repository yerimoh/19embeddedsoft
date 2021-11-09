# 미션 
import numpy as np
import cv2

cap = cv2.VideoCapture("/Users/han/Documents/study/python_OpenCV/11:5 영상자료/안전지역3.avi")

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
    object_color = 1; # 1 : red, 2 : blue
    ground_color = 1; # 1 : green, 2: black
    img_hsv=cv2.cvtColor(img_frame, cv2.COLOR_BGR2HSV_FULL)
    
    #target object detect
    ## hsv 색공간 빨간색, 파란색 영역 설정
    if object_color == 1: # red
        object_lower=(210, 30, 60)
        object_upper=(255, 255, 255)
    else:               # blue
        object_lower=(140, 10, 10)
        object_upper=(160, 255, 180)
    ## hsv 색공간 초록색, 검은색 영역 설정
    if ground_color == 1: # green
        ground_lower=(60, 10, 10)
        ground_upper=(140, 255, 255)
    else:               # black
        ground_lower=(0, 0, 0)
        ground_upper=(255, 255, 80)


    ## 물체 mask
    img_mask_object = cv2.inRange(img_hsv, object_lower, object_upper)
    img_mask_ground = cv2.inRange(img_hsv, ground_lower, ground_upper)

    # 이진화 영상을 모폴로지 커널을 이용해 전처리
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    img_mask_ground = cv2.morphologyEx(img_mask_ground, cv2.MORPH_OPEN, k) 
    img_mask_object = cv2.morphologyEx(img_mask_object, cv2.MORPH_OPEN, k) 

    # mask별 center fo gravity point, 영상 중심점 찾기
    object_mask_CG_x_point = np.mean(np.nonzero(img_mask_object)[0])
    object_mask_CG_y_point = np.mean(np.nonzero(img_mask_object)[1])

    video_center_x_point = 320
    video_center_y_point = 240

        ##영상 중심점과 object CG point x축 차이 결과값 (return)
    distance_object_video=video_center_x_point - object_mask_CG_x_point #값이 음수이면 영상 중심 기준 왼쪽



    # mask img 를 이용한 윤곽선 검출
    ground_contours= cv2.findContours(img_mask_ground, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    object_contours= cv2.findContours(img_mask_object, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]

    if len(ground_contours) != 0:
        ground_max_size = 0
        for i in range(len(ground_contours)):
            if ground_max_size < len(ground_contours[i]):
                ground_max_size=len(ground_contours[i])
                ground_max_size_index = i
        cv2.drawContours(img_frame, [ground_contours[ground_max_size_index]], -1, (0, 0, 255), 2)


        if len(object_contours) != 0:
            object_max_size = 0
            for i in range(len(object_contours)):
                if object_max_size < len(object_contours[i]):
                    object_max_size=len(object_contours[i])
                    object_max_size_index = i
            cv2.drawContours(img_frame, [object_contours[object_max_size_index]], -1, (0, 255, 0), 2)



            #object contour의 min_y, min_x, max_x 찾기
            object_temp_x = []
            object_temp_y = []
            for i in range(len([object_contours[object_max_size_index]][0])):
                object_temp_x.append([object_contours[object_max_size_index]][0][i][0][0])
                object_temp_y.append([object_contours[object_max_size_index]][0][i][0][1])
            #print(temp) x
            object_x_max=max(object_temp_x)
            object_x_min=min(object_temp_x)
            object_y_max=max(object_temp_y)



            #ground contour중 object contour의 min_y에서의 x값 찾기
            ground_temp_x = []
            ground_temp_y_max = 480 #y maximum값에서 시작
            for i in range(0,len([ground_contours[ground_max_size_index]][0])):
                ii= [ground_contours[ground_max_size_index]][0][i][0][1]
                if ii == object_y_max:
                    ground_temp_x.append([ground_contours[ground_max_size_index]][0][i][0][0])
                if ground_temp_y_max > ii:
                    ground_temp_y_max = ii

            if len(ground_temp_x) !=0:
                ground_x_max=max(ground_temp_x)
                ground_x_min=min(ground_temp_x)



                #ground x와 ovject x를 이용한 객체 위치 추정 (return)
                if (ground_x_max>=object_x_max) and (ground_x_min <= object_x_min):
                    print("객체가 구역 내부에 있음")
                elif (ground_x_max<object_x_min):
                    print("객체가 구역 오른쪽 외부에 있음")
                elif (ground_x_min > object_x_max):
                    print("객체가 구역 왼쪽 외부에 있음")
                else :
                    print("객체가 식별되지 않음")


    cv2.imshow("object",img_mask_object)
    cv2.imshow("ground",img_mask_ground)
    cv2.imshow("contour",img_frame)

cv2.waitKey()
cv2.destroyAllWindows()