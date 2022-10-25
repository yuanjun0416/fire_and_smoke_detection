import json
import os
from pycocotools.coco import COCO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存成功") 


json_path = 'E:/fire/Fire and Smoke BBox COCO Dataset/coco128/annotations/instances_val2017.json'
img_path = 'E:/fire/Fire and Smoke BBox COCO Dataset/coco128/val2017'

# load COCO data
coco = COCO(annotation_file=json_path)

# get all image index info
ids = list(sorted(coco.imgs.keys()))
print("number of images: {}".format(len(ids)))

# get all coco class lables
coco_classes = dict([(v["id"], v["name"]) for k, v in coco.cats.items()])

square_ratio = []
object_ratio = []
image_ratio = []
#遍历前三张图片
for img_id in ids[0:]: #img_id:1
    #获取对应图像id的所有annotations idx信息
    ann_ids = coco.getAnnIds(imgIds=img_id)

    # 根据annotations idx信息获取所有标注信息
    targets = coco.loadAnns(ann_ids)

    img_h = coco.imgs[img_id]['height']
    img_w = coco.imgs[img_id]['width']
    im_ratio = img_h / img_w
    image_ratio.append(im_ratio)
    # draw box to image
    for target in targets:
        x, y, w, h = target["bbox"]
        ob_ratio = h / w
        object_ratio.append(ob_ratio)
        s_ratio = (w * h) / (img_h * img_w)
        if s_ratio>1: #如果出现目标面积/图片面积的情况，说明标注错误
            continue
        square_ratio.append(s_ratio)
text_save('image_ratio.txt', image_ratio)
text_save('object_ratio.txt', object_ratio)
text_save('square_ratio.txt', square_ratio)








