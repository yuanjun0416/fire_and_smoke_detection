import os
from PIL import Image,ImageFile
#ImageFile.LOAD_TRUNCATED_IMAGES = True    #如果图片太大报错可以使用这个
 
b = 0
dir = 'E:/FireDetection/WildFires/Smoke5'                 #需要处理的图片目录
files = os.listdir(dir)     #得到需要处理的所有图片
files.sort()                #对图片进行排序
 
for each_bmp in files:  # 遍历图片，进行筛选
    
    if not each_bmp.endswith(('jpg', 'png', 'jpeg', 'bmp')):  #如果不是图片格式，就丢弃该文件，直接执行下一文件
        print(each_bmp)
        continue

    
    each_bmp_root = os.path.join(dir, each_bmp) #得到每个图片路径
    try:                                        #如果图片损坏，则丢弃该文件，直接执行下一文件
        Image.open(each_bmp_root).load()
    except OSError:
        continue
    image = Image.open(each_bmp_root)    #打开每个图片
    img = image.convert('RGB')     #转化成RGB，其实图片大多都是RGB，即使灰度图也不一定转RGB，看需求
    width = img.size[0]           #获取图像的宽和长
    height = img.size[1]

    if (1920>=width>=544) and (1920>=height>=640):  #将1920>=width>=544, 1920>=height>=640的文件保存在指定文件夹中
        img.save('E:/FireDetection_data_cleaning/'+each_bmp)     
