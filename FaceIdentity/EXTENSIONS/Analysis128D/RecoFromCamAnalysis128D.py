import dlib          
import numpy as np   
import cv2           
import pandas as pd  

faceCSVPath = "data/features_all.csv"
facerec = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


csv_rd = pd.read_csv(faceCSVPath, header=None)


def CopyCSVDataToArray():
    features_someone_arr = []
    faceArrFromCSV = []
    for i in range(csv_rd.shape[0]):
        for j in range(0, len(csv_rd.ix[i, :])):
            features_someone_arr.append(csv_rd.ix[i, :][j])
        faceArrFromCSV.append(features_someone_arr)

    del features_someone_arr[0][0]
    print("Faces in Database：", len(faceArrFromCSV))
    return faceArrFromCSV

# 計算128D 向量(歐式距離)
# compute the e-distance between two 128D features
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist

def FaceAnalysis(faces, img_rd, path_faces_recogf, path_predictor):
    print("辨識中 ..")
    features_known_arr = CopyCSVDataToArray()
    features_cap_arr = []
    for k in range(len(faces)):
        sharePredictor = dlib.shape_predictor(path_predictor)
        shape = sharePredictor(img_rd, faces[k])
        features_cap_arr.append(facerec.compute_face_descriptor(img_rd, shape))
        print("##### camera person", k+1, "#####")
        # 让人名跟随在矩形框的下方
        # 确定人名的位置坐标
        # 先默认所有人不认识，是 unknownAA
        # set the default names of faces with "unknown"
        name_namelist = []
        name_namelist.append("unknown")

        # 对于某张人脸，遍历所有存储的人脸特征
        # for every faces detected, compare the faces in the database
        e_distance_list = []
        for i in range(len(features_known_arr)):
            # 如果 person_X 数据不为空
            if str(features_known_arr[i][0]) != '0.0':
                print("with person", str(i + 1), "the e distance: ", end='')
                e_distance_tmp = return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                print(e_distance_tmp)
                e_distance_list.append(e_distance_tmp)
            else:
                # 空数据 person_X
                e_distance_list.append(999999999)
        # Find the one with minimum e distance
        similar_person_num = e_distance_list.index(min(e_distance_list))
        print("Minimum e distance with person", int(similar_person_num)+1)

        if min(e_distance_list) < 0.4:
            # 在这里修改 person_1, person_2 ... 的名字
            # 可以在这里改称 Jack, Tom and others
            # Here you can modify the names shown on the camera
            name_namelist[k] = "Person "+str(int(similar_person_num)+1)
            print("May be person "+str(int(similar_person_num)+1))
        else:
            print("Unknown person")