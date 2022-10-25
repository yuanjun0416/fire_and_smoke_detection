#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 06:42:30 2018
@author: pc
"""
 
import os
from pyecharts.charts import Bar
from pyecharts import options as opts
import os.path
import xml.dom.minidom
import xml.etree.cElementTree as et
from scipy.ndimage import measurements
import numpy as np

 
def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存成功")  


path="E:/fire/fire smoke dataset/fire&smoke/Annotations"
files=os.listdir(path)
s=[]

square_list = []
side_list = []
object_list = []
# =============================================================================
# extensional filename
# =============================================================================
def file_extension(path): 
    return os.path.splitext(path)[1] 
 
for xmlFile in files: 
    if not os.path.isdir(xmlFile): 
        if file_extension(xmlFile) == '.xml':
            # print(os.path.join(path,xmlFile))
            tree=et.parse(os.path.join(path,xmlFile))
            root=tree.getroot()
            filename=root.find('filename').text
#            print("filename is", path + '/' + xmlFile)
            for Object in root.findall('size'):
                side1=Object.find('width').text
                side2=Object.find('height').text
                side = int(side2) / int(side1)
                side_list.append(side)
                # side_list.append(int(side1))
                # side_list.append(int(side2))
#                print(xmin,ymin,xmax,ymax)
                # print(square)
            for Object in root.findall('object'):
#                name=Object.find('name').text
#                print("Object name is ", name)
                bndbox=Object.find('bndbox')
                xmin=bndbox.find('xmin').text
                ymin=bndbox.find('ymin').text
                xmax=bndbox.find('xmax').text
                ymax=bndbox.find('ymax').text
                square = (int(ymax)-int(ymin)) * (int(xmax)-int(xmin)) / (int(side1) * int(side2))
                if square>1:    #如果出现目标面积/图片面积的情况，说明标注错误
                    continue
                object = (int(ymax)-int(ymin)) / (int(xmax)-int(xmin))
                square_list.append(square)
                object_list.append(object)
#                print(xmin,ymin,xmax,ymax)
                # print(square)
                

text_save('image_ratio.txt', side_list)
text_save('object_ratio.txt', object_list)
text_save('square_ratio.txt', square_list)
#print("square is ", square_list)
 
# =============================================================================
# 画出直方图
# =============================================================================
num = 1 #最大面积
histogram1 = measurements.histogram(square_list,0,num,10) #直方图
histogram1 = histogram1/sum(histogram1) * 100
histogram1 = np.round(histogram1, 4)
histogram1 = list(map(float, histogram1)) #转换成 int 格式
# histogram1 = list(map(int, histogram1)) #转换成 int 格式
print("histogram is ", histogram1)
 
bar = Bar()
bar.add_xaxis(["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])
bar.add_yaxis('数目', histogram1)
bar.set_global_opts(title_opts=opts.TitleOpts(title="anchor与image的面积比"))
bar.render('./anchor_image.html')#generate HTML file
# =============================================================================
# 画出直方图
# =============================================================================
num = 2 #image_ratio最大值
histogram2 = measurements.histogram(side_list,0,num,10) #直方图
histogram2 = histogram2/sum(histogram2) * 100
histogram2 = np.round(histogram2, 4)
histogram2 = list(map(float, histogram2)) #转换成 int 格式
print("histogram is ", histogram2)
 
bar = Bar()
bar.add_xaxis(["0.2", "0.4", "0.6", "0.8", "1.0", "1.2", "1.4", "1.6", "1.8", "2.0"])
bar.add_yaxis('数目', histogram2)
bar.set_global_opts(title_opts=opts.TitleOpts(title="image的h/w"))
bar.render('./image_ratio.html')#generate HTML file
# 画出直方图
# =============================================================================
num = 10 #object_ratio最大值
histogram3 = measurements.histogram(object_list,0,num,10) #直方图
histogram3 = histogram3/sum(histogram3) * 100
histogram3 = np.round(histogram3, 4)
histogram3 = list(map(float, histogram3)) #转换成 int 格式
print("histogram is ", histogram3)
bar = Bar()
bar.add_xaxis(["1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0"])
bar.add_yaxis('数目', histogram3)
bar.set_global_opts(title_opts=opts.TitleOpts(title="anchor的h/w"))
bar.render('./anchor_ratio.html')#generate HTML file
print("图像搞定")