## 文件内容

统计的是图片的高宽比(h/w), 标注的真实框的高宽比(h/w), 标注的真实框的面积比图片的面积(anchor_square/image_square)


### 文件结构
```
├── coco_dataset_statis.py  统计coco数据集格式的文件的一些参数
├── voc_dataset_statis.py 统计voc数据集格式的文件的一些参数 
├── yolov5_statis.py 统计yolov5数据集格式的文件的一些参数
├── save_txt.py 将列表保存到txt文件中
├── draw_bar.py 读取保存在txt文件中的值，并画柱状图
└── data.py 无任何意义的代码，只是当时遇到一些问题，需要尝试的
```
