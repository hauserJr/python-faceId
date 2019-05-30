import dlib         # 人臉識別
import numpy as np  # 數據處理
import cv2          # 影像處理
import os           # 讀寫文件
import shutil       # 讀寫文件
import EXTENSIONS.FaceDCal.Faces128DCal as Cal128D
from tkinter import *
import pandas as pd  # 數據處理
path_faces_person = "data//data_faces_from_camera//"
path_faces_recogf = "data/data_dlib/dlib_face_recognition_resnet_model_v1.dat"
path_predictor = "data/data_dlib/shape_predictor_68_face_landmarks.dat"

######
#Init#
##############################################################################################
# 人臉偵測器
faceDetector = dlib.get_frontal_face_detector()

# 人臉68點偵測
sharePredictor = dlib.shape_predictor(path_predictor)

# 設定攝影機
videoCapture = cv2.VideoCapture(0)

# 設定畫質 預設640x480
# 這裡修正為1080P
# 设置视频参数 set camera
videoCapture.set(0, 480)
videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 680)
##############################################################################################

def SetupCamera():
    runStatus = False
    while videoCapture.isOpened():
        kk = cv2.waitKey(1)
        flag, img_rd = videoCapture.read()

        #keyIn = cv2.waitKey(1)

        # 圖片色階 (灰階為正常設定,但影像好像沒反應)
        img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)
    
        # 人臉計算
        faces = faceDetector(img_gray, 0)

        # 人臉分數計算
        #偵測人臉
        face_rects, scores, idx = faceDetector.run(img_rd, 0)

        # NORMAL = 自行調整視窗大小
        cv2.namedWindow("camera", cv2.WINDOW_AUTOSIZE)

        if (runStatus == False):
            runStatus = True
            GetCameraFaces(faces, img_rd, idx, scores)
            
        
        # 自訂視窗大小,設定大小完無法自行調整視窗大小
        #cv2.resizeWindow("camera", 960, 540)
        cv2.imshow("camera", img_rd)

        # 定義Keyboard Input
        # ESC 離開While
        if cv2.waitKey(1) == 27:
            break

        runStatus = False




def GetCameraFaces(faces, img_rd, idx, faceScore):
    font = cv2.FONT_HERSHEY_COMPLEX

    if len(faces) != 0 :
        print("【DATA】人臉數：" + str(len(faces)))
        #print(faces)

        # 人臉識別的top bottom right leftZ
        for i, v in enumerate(faces):

            # 辨識距離設定
            distanceCal = v.bottom() - v.top()
            if distanceCal <= 130:
                break;

            colorRectangle = (255, 255, 255)

            # print("上" + str(d.top()))
            # print("下" + str(d.bottom()))
            # print("左" + str(d.left()))
            # print("右" + str(d.right()))
            # print("高" + str(d.bottom() - d.top()))
            # print("寬" + str(d.right() - d.left()))
            # height = d.bottom() - d.top()
            # width = d.right() - d.left()
            # 人臉邊界設定
            topOverRange = (480 - v.top()) / 3.5

            leftOverRange = 480 * 0.7

            rightOverRange = 640 * 0.47

            bottomOverRange = 480

            #if ((d.top() <= topOverRange) or (d.bottom() >= bottomOverRange) or (d.left() >= leftOverRange) or (d.right() <= rightOverRange)):
            if (FALSE) :
                # 人臉不在框內
                colorRectangle = (0, 0, 255)
                cv2.putText(img_rd, "Over Range", (40, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            else:
                # 人臉在框內
                colorRectangle = (255, 255, 255)

                if (len(faceScore)) and len(faceScore)-1 >= i:

                    # scoreText = 是否為人臉分數,越高代表越有可能是真實人臉
                    scoreText = " %2.2f ( %d )" % (faceScore[i], idx[i])
                    cv2.putText(img_rd, scoreText, (v.right() - 60, v.bottom() + 30), cv2. FONT_HERSHEY_DUPLEX,0.7, (255, 255, 21), 1, cv2. LINE_AA)
                else:
                    scoreText = 0

            # 畫製人臉框
            cv2.rectangle(img_rd,
                tuple([v.left() - 80, v.top() - 70]),
                tuple([v.right() + 80, v.bottom()]),
                colorRectangle, 2)

            if cv2.waitKey(1) == 115 or cv2.waitKey(1) == 83:
                TakePicture(faces,img_rd)
    else :
        print("【INFO】畫面中尚無人臉")

def TakePicture(faces,img_rd):
    for i, v in enumerate(faces):
        height = (v.bottom() - v.top())
        width = (v.right() - v.left())
        im_blank = np.zeros((int(height), width, 3), np.uint8)

        for ii in range(height):
            for jj in range(width):
                im_blank[ii][jj] = img_rd[v.top() + ii][v.left() + jj]

    #判斷圖片區有多少張照片,用於避免重複命名
    photos_list = os.listdir(path_faces_person)
    ImgIndex = len(photos_list)

    #將圖檔存檔
    cv2.imwrite(path_faces_person + "/img_face_" + str(ImgIndex+1)+ ".jpg", im_blank)

    #圖檔存檔後進入訓練
    print('人臉訓練中 ..')
    Cal128D.Cal128DFunc(path_faces_person)



if not videoCapture.isOpened():
    print("【ERROR】未偵測可使用的攝影機")
else:
    print("【INFO】攝影機啟動成功")
    SetupCamera()


# 釋放Camera資源
videoCapture.release()

cv2.destroyAllWindows()

    