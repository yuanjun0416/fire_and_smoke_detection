import os
import yaml
from PIL import Image
import numpy as np

def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存成功") 


# yaml_path = 'E:/fire/FDD.v3i.yolov5pytorch/data.yaml'
# with open(yaml_path) as f:
#     data = yaml.load(f, Loader=yaml.FullLoader)
# print(data['names'])

# #yolov5类别种类
# categorys = data['names']
# #类别数
# number_classes = len(categorys)


square_ratio = []
img_ratio = []
object_ratio = []

label_path = 'E:/fire/my datasets.v1i.yolov5pytorch/train/labels' #yolov5 labels所在的位置
label_list = os.listdir(label_path)
images_path = label_path.replace('labels', 'images') #yolov5 images所在的位置
for list in label_list: #遍历labels中的所有文件
    list_img = list.replace('txt', 'jpg')        
    image_p = os.path.join(images_path, list_img) #yolov5 中的images中的每一张图片
    try:
        Image.open(image_p).load()
    except OSError:
        print(image_p)
        continue
    image = np.array(Image.open(image_p))
    img_h = image.shape[1]
    img_w = image.shape[0]
    i_ratio = float(img_h) / float(img_w)   
    img_ratio.append(i_ratio)
    label_p = os.path.join(label_path, list)
    with open(label_p, 'r') as f:
        for l in f.readlines():#遍历labels中的每一个文件中的每一行，也就是每一个目标
            line = l.strip().split(" ")
            ob_w = line[3] #yolov5 数据的格式 x_center, y_center, width, height 全部都是相对值， 相对于整幅图片的尺寸
            ob_h = line[4]
            if float(ob_w) == 0 or float(ob_h) == 0:
                print(label_p)
                continue
            o_ratio = (float(ob_h)*float(img_h)) / (float(ob_w) * float(img_w))
            object_ratio.append(o_ratio)
            s_ratio = (float(ob_h) * float(ob_w))
            if s_ratio>1:  #如果出现目标面积/图片面积的情况，说明标注错误
                continue
            square_ratio.append(s_ratio)

text_save('./square_ratio.txt', square_ratio)
text_save('./image_ratio.txt', img_ratio)
text_save('./object_ratio.txt', object_ratio)