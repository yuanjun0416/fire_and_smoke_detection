
import numpy as np
from pyecharts.charts import Bar
from pyecharts import options as opts
from scipy.ndimage import measurements
def text_read(filename):#filename为读取文件的路径，data为要写入数据列表.
    file = open(filename,'r')
    data_list = []
    for line in file.readlines():
        curline = line.strip().split(" ")
        floatline = list(map(float, curline))
        data_list.append(floatline)
    file.close()
    print("读取成功")
    data_list = list(np.array(data_list).ravel())
    return data_list

def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存成功")  

square_list = text_read('./square_ratio.txt')
image_list = text_read('./image_ratio.txt')
object_list = text_read('./object_ratio.txt')

square_list = [num for num in square_list if num <=1]

# =============================================================================
# 画出直方图
# =============================================================================
num = 1 #最大面积
square_min = min(square_list)
square_max = max(square_list)
print("square_min:{}, square_max:{}".format(square_min, square_max))
histogram1 = measurements.histogram(square_list,0,num,10) #直方图
sum_square = sum(histogram1)
histogram1 = histogram1/sum(histogram1) * 100
histogram1 = np.round(histogram1, 4)
histogram1 = list(map(float, histogram1)) #转换成 int 格式
# histogram1 = list(map(int, histogram1)) #转换成 int 格式
print("histogram is ", histogram1)
 
bar = Bar()
bar.add_xaxis(["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])
bar.add_yaxis('数目{}'.format(sum_square), histogram1)
bar.set_global_opts(title_opts=opts.TitleOpts(title="anchor与image的面积比"))
bar.render('./anchor_image.html')#generate HTML file
# =============================================================================
# 画出直方图
# =============================================================================
num = 5 #image_ratio最大值
image_min = min(image_list)
image_max = max(image_list)
print("image_min:{}, image_max:{}".format(image_min, image_max))
histogram2_2 = measurements.histogram(image_list,1.0000000001,num,5) #直方图
histogram2 = measurements.histogram(image_list,0.4,1,6) #直方图
histogram2 = np.hstack((histogram2, histogram2_2))
sum_image = sum(histogram2)
histogram2 = histogram2/sum(histogram2) * 100
histogram2 = np.round(histogram2, 4)
# histogram2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] 
histogram2 = list(map(float, histogram2)) #转换成 int 格式
print("histogram is ", histogram2)
bar = Bar()
bar.add_xaxis(["0.4-0.5", "0.5-0.6", "0.6-0.7", "0.7-0.8", "0.8-0.9", "0.9-1", "1-2", "2-3", "3-4", "4-5"])
bar.add_yaxis('数目{}'.format(sum_image), histogram2)
bar.set_global_opts(title_opts=opts.TitleOpts(title="image的h/w"))
bar.render('./image_ratio.html')#generate HTML file
# 画出直方图
# =============================================================================
num = 9 #object_ratio最大值
object_min = min(object_list)
object_max = max(object_list)
histogram3_3 = measurements.histogram(object_list,1.0000000001,num,4) #直方图
histogram3 = measurements.histogram(object_list,0,1,10) #直方图
histogram3 = np.hstack((histogram3, histogram3_3))
sum_object = sum(histogram3)
print("object_min:{}, object_max:{}".format(object_min, object_max))
histogram3 = histogram3/sum(histogram3) * 100
histogram3 = np.round(histogram3, 4)
histogram3 = list(map(float, histogram3)) #转换成 int 格式
print("histogram is ", histogram3)
bar = Bar()
bar.add_xaxis(["0-0.1", "0.1-0.2", "0.2-0.3", "0.3-0.4", "0.4-0.5", "0.5-0.6", "0.6-0.7", "0.7-0.8", "0.8-0.9", "0.9-1.0", "1-3", "3-5", "5-7", "7-9"])
bar.add_yaxis('数目{}'.format(sum_object), histogram3)
bar.set_global_opts(title_opts=opts.TitleOpts(title="anchor的h/w"))
bar.render('./anchor_ratio.html')#generate HTML file
print("图像搞定")