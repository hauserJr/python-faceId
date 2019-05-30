import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np

# Init
path_images_from_camera = "data//data_faces_from_camera//"

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("data/data_dlib/shape_predictor_5_face_landmarks.dat")

face_rec = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


# 取得單一圖片的特徵值
def return_128d_features(path_img):
    img_rd = io.imread(path_img)
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    faces = detector(img_gray, 1)

    print("%-40s %-20s" % ("偵測到人臉 / image with faces detected:", path_img), '\n')

    # 檢測是否為人臉
    # 是人臉才進行計算
    if len(faces) != 0:
        shape = predictor(img_gray, faces[0])
        face_descriptor = face_rec.compute_face_descriptor(img_gray, shape)
    else:
        face_descriptor = 0
        print("no face")

    return face_descriptor


# 從資料夾取得
def return_features_mean_personX(ImagePath):
    features_list_personX = []
    photos_list = os.listdir(ImagePath)
    if photos_list:
        for i in range(len(photos_list)):
            # 使用return_128d_features()得到128d特徵點
            print("%-40s %-20s" % ("取得的人臉圖像 / image to read:", ImagePath + "/" + photos_list[i]))
            features_128d = return_128d_features(ImagePath + "/" + photos_list[i])
            #  print(features_128d)
            # 如果偵測到無法辨識的圖片
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)
    else:
        print("無任何圖檔 / Warning: No images in " + ImagePath + '/', '\n')

    # 計算特徵值
    # N x 128D -> 1 x 128D
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX).mean(axis=0)
    else:
        features_mean_personX = '0'

    return features_mean_personX



def Cal128DFunc (ImagePath):
    # 讀取尚未建議的圖像數據
    people = os.listdir(ImagePath)
    people.sort()

    with open("data/features_all.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for person in people:
            print("##### " + person + " #####")
            # Get the mean/average features of face/personX, it will be a list with a length of 128D
            features_mean_personX = return_features_mean_personX(ImagePath)

            test = list(features_mean_personX)
            test.insert(0, 'Unknow')
            writer.writerow(test)

            print("特徵值平均 / The mean of features:", list(features_mean_personX))
            print('\n')

            
            os.remove(ImagePath + "//" +person)
        print("已經人臉數據存入 / Save all the features of faces registered into: data/features_all.csv")
        print("建模原檔已刪除")