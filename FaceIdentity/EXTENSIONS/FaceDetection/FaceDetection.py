import dlib         # 人臉識別
import numpy as np  # 數據處理
import cv2          # 影像處理
import os           # 讀寫文件
import shutil       # 讀寫文件
import EXTENSIONS.FaceDCal.Faces128DCal as Cal128D
import threading
from tkinter import *
import pandas as pd  # 數據處理
import time
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

##################
#判別是圖片或人臉#
##############################################################################################
def RealFace(img_rd,  faceScore, faces):
    positionLeft = 0
    positionTop = 0
    for i, v in enumerate(faces):
        positionLeft = v.left()
        positionTop = v.top()
    font = cv2.FONT_HERSHEY_COMPLEX
    minfacesScoreBase = 0.71
    maxfacesScoreBase = 1.5
    if float(faceScore) >= maxfacesScoreBase or float(faceScore) <= minfacesScoreBase:
        return "Warning"
    else:
        #當辨別為真的人臉後,進入人臉辨識階段
        FaceIdentification(faces, img_rd)
        return 'Get It'
##############################################################################################

##############################################################################################
# 計算歐式距離
# compute the e-distance between two 128D features
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist

def FaceIdentification(faces, img_rd):
    features_cap_arr = []
    # traversal all the faces in the database
    for k in range(len(faces)):
        print("##### 偵測到的人數：", k+1, " #####")
        faceShape = sharePredictor(img_rd, faces[k])
        faceRecognition = dlib.face_recognition_model_v1(path_faces_recogf)
        features_cap_arr.append(faceRecognition.compute_face_descriptor(img_rd, faceShape))
        # 將人臉特徵儲存
        # for every faces detected, compare the faces in the database
        e_distance_list = []

        features_known_arr = FacesKnown()
        userName = 'Unknow'

        for i in range(len(features_known_arr)):
            # 如果數據存在
            
            if str(features_known_arr[i][0]) != '0.0':
                # 數據分析進行前刪除姓名
                userName = features_known_arr[i][0]
                del features_known_arr[i][0]
                print("with person", str(i + 1), "the e distance: ", end='')
                e_distance_tmp = return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                print(e_distance_tmp)
                e_distance_list.append(e_distance_tmp)

                # 分數低於0.4則離開(越低代表為本人的機率越高)
                if (e_distance_tmp < 0.4) :
                    break
            else:
                # 數據不存在
                e_distance_list.append(999999999)

        # 尋找符合特徵的人臉數量
        similar_person_num = e_distance_list.index(min(e_distance_list))
        print("Minimum e distance with person", int(similar_person_num)+1)

        positionLeft = 0
        positionTop = 0
        for i, v in enumerate(faces):
            positionLeft = v.left() - 60
            positionBottom = v.bottom() - 30
        font = cv2.FONT_HERSHEY_COMPLEX
        if min(e_distance_list) < 0.4:
            print("符合人臉條件數量： "+ str(int(similar_person_num)+1))
            cv2.putText(img_rd, userName + " Pass", (positionLeft, positionBottom), font, 0.8, (0, 255, 21), 1, cv2.LINE_AA)
            break
        else:
            print("偵測到訪客")
            cv2.putText(img_rd, "Reject", (positionLeft, positionBottom), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            break
        

def FacesKnown ():
    # 取得存放人臉特徵值的CSV
    path_features_known_csv = "data/features_all.csv"
    csv_rd = pd.read_csv(path_features_known_csv, header=None)

    # 將CSV數據存入Array用於判斷
    features_known_arr = []

    # 讀取CSV內的特徵值
    # print known faces
    for i in range(csv_rd.shape[0]):
        features_someone_arr = []
        for j in range(0, len(csv_rd.ix[i, :])):
            features_someone_arr.append(csv_rd.ix[i, :][j])
        features_known_arr.append(features_someone_arr)

    # 取得辨識資料姓名
    print("目前有多少人臉數據：", len(features_known_arr))
    return features_known_arr
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


def FaceIds (img_rd, faceScore, faces):
    faceText = RealFace(img_rd, faceScore, faces)
    font = cv2.FONT_HERSHEY_COMPLEX
    for i, v in enumerate(faces):
        cv2.putText(img_rd, faceText, (v.left() - 60, v.top() - 90), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)



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

                    #建立執行緒
                    threadBuild = threading.Thread(target = FaceIds, args = (img_rd, faceScore[i], faces,))

                    # scoreText = 是否為人臉分數,越高代表越有可能是真實人臉
                    scoreText = " %2.2f ( %d )" % (faceScore[i], idx[i])
                    cv2.putText(img_rd, scoreText, (v.right() - 60, v.bottom() + 30), cv2. FONT_HERSHEY_DUPLEX,0.7, (255, 255, 21), 1, cv2. LINE_AA)
                    
                    # 執行該子執行緒
                    threadBuild.start()

                    #faceText = RealFace(img_rd, faceScore[i], faces)
                    #cv2.putText(img_rd, faceText, (v.left() - 60, v.bottom() - 70), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

                    # 等待執行結束
                    threadBuild.join()
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

    