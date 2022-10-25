import os
import numpy as np
import cv2
import shutil


# 计算两张图片的相似度
def calc_similarity(img1_path, img2_path):
    img1 = cv2.imdecode(np.fromfile(img1_path, dtype=np.uint8), -1)
    H1 = cv2.calcHist([img1], [1], None, [256], [0, 256])  # 计算图直方图
    H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)  # 对图片进行归一化处理
    img2 = cv2.imdecode(np.fromfile(img2_path, dtype=np.uint8), -1)
    H2 = cv2.calcHist([img2], [1], None, [256], [0, 256])  # 计算图直方图
    H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)  # 对图片进行归一化处理
    similarity1 = cv2.compareHist(H1, H2, 0)  # 相似度比较
    print('similarity:', similarity1)
    if similarity1 > 0.85:  # 0.98是阈值，可根据需求调整
        return True
    else:
        return False

# 去除相似度高的图片
def filter_similar(dir_path):
    filter_dir = os.path.join(os.path.dirname(dir_path), 'filter_similar')
    if not os.path.exists(filter_dir):
        os.mkdir(filter_dir)
    filter_number = 0
    for root, dirs, files in os.walk(dir_path):
        img_files = [file_name for file_name in files ]
        filter_list = []
        for index in range(len(img_files))[:-4]:
            if img_files[index] in filter_list:
                continue
            for idx in range(len(img_files))[(index+1):(index+5)]:
                img1_path = os.path.join(root, img_files[index])
                img2_path = os.path.join(root, img_files[idx])
                if calc_similarity(img1_path, img2_path):
                    filter_list.append(img_files[index])
                    filter_number += 1
                    break
        for item in filter_list:
            src_path = os.path.join(root, item)
            shutil.move(src_path, filter_dir)
    return filter_number


dir = 'E:/FireDetection_data_cleaning'                 #需要处理的图片目录
num = filter_similar(dir)
