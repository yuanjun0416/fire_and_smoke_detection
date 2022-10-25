import numpy as np
a = np.array([1.1,2.1,3.1])
b = np.array([4,5,6])
np.savetxt('1.txt',(a,b))
# 此时文件夹中多了一个1.txt

c = np.loadtxt('1.txt')
print(c.shape)  # (2,3)   两行三列
c[0] = np.array([1,2,3]) 


def text_save(filename, data):#filename为写入txt文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存成功") 

text_save('1.txt', (a,b))
c = np.loadtxt('1.txt')
print(c.shape)  # (2,3)   两行三列