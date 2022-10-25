import os
import shutil
from PIL import Image

# 正则化图像
def regularizeImage(img, size = (9, 8)):
    return img.resize(size).convert('L')

# 计算hash值
def getHashCode(img, size = (9, 8)):

    result = []
    for i in range(size[0] - 1):
        for j in range(size[1]):
            current_val = img.getpixel((i, j))
            next_val = img.getpixel((i + 1, j))
            if current_val > next_val:
                result.append(1)
            else:
                result.append(0)
    
    return result

# 比较hash值
def compHashCode(hc1, hc2):
    cnt = 0
    for i, j in zip(hc1, hc2):
        if i != j:
            cnt += 1
    return cnt

# 计算差异哈希算法相似度
def caldHashSimilarity(img1, img2):
    img1 = Image.open(img1)
    img2 = Image.open(img2)
    img1 = regularizeImage(img1)
    img2 = regularizeImage(img2)
    hc1 = getHashCode(img1)
    hc2 = getHashCode(img2)
    compHash = compHashCode(hc1, hc2)
    print('compHash', compHash)
    if compHash > 10:
        return False
    else:
        return True

__all__ = ['caldHashSimilarity']
# 去除相似度高的图片
def filter_similar(dir_path):
    filter_dir = os.path.join(os.path.dirname(dir_path), 'dhash_filter_similar')
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
                if caldHashSimilarity(img1_path, img2_path):
                    filter_list.append(img_files[index])
                    filter_number += 1
                    break
        for item in filter_list:
            src_path = os.path.join(root, item)
            shutil.move(src_path, filter_dir)
    return filter_number


dir = 'E:/FireDetection_data_cleaning'                 #需要处理的图片目录
num = filter_similar(dir)


