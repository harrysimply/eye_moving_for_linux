#coding = utf-8
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



#获取txt文件
path=os.getcwd()+'/data/'


for root, dirs, files in os.walk(path):
    print(root)#打印当前目录
    print(dirs)#打印当前目录下的文件夹
    #print(files)#打印当前目录下的所有文件，并以列表形式存储['2018-06-29 16:31:45-16:33:25.txt', '2018-06-29 16:33:36-16:38:30.txt', '2018-06-27 19:38:07-19:38:51.txt']

#选择需要操作的文件

files.sort()
print(files)
file=files[-4]
newfile=root+file
print(newfile)

for i in files:
    if i.split('.')[-1]=='txt':
        print("{}是文本文档".format(i.split('.')[0]))
        file=root+i.split('.')[0]+'txt'
        with open(file, 'r') as f:
            print("read the " + file)
            l = []
            while 1:
                line = f.readline().split('\n')[0]  # 去掉txt中的‘\n’
                # print(line)
                # line=map(int,line)
                l.append(line)
                if not line:
                    break
        l = l[1:-2]
        print(l)
        x = [float(nums.split(',')[0].split('[')[1]) for nums in l]




with open(newfile,'r') as f:
    print("read the "+newfile)
    l=[]
    while 1:
        line=f.readline().split('\n')[0]#去掉txt中的‘\n’
        #print(line)
        #line=map(int,line)
        l.append(line)
        if not line:
            break
l=l[1:-2]
print(l)
# for nums in l:
#     #print(float(nums))
#     nums=nums.split(',')
#     print(float(nums[0].split('(')[1]))
#     #print(float(nums[1].split(')')[0]))
#将坐标字符串通过split函数切片成x和y的数列
x=[float(nums.split(',')[0].split('[')[1]) for nums in l]
y=[float(nums.split(',')[1].split(']')[0]) for nums in l]
print(x)
print(len(x))
print(y)
print(len(y))

#先用图像表示下已知的记录
plt.figure(figsize=(6,12),dpi=100)
#plt.figure(0)
font1 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 10,
}


plt.subplot(8,1,1)
#plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
#plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
stand=range(len(x))

#plt.xticks(range(len(x)),size=12,rotation=50) #设置字体大小和字体倾斜度
plt.xlabel('time',font1) # x轴标签
plt.ylabel('move',font1)
plt.title('X directions of Eye',font1)  # 图的名称
plt.plot(stand,x, color ='green', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)

plt.subplot(8,1,2)
plt.xlabel('time',font1) # x轴标签
plt.ylabel('move',font1)
plt.title('Y directions of Eye',font1)  # 图的名称
plt.plot(stand,y, color ='green', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)
#plt.tight_layout()


plt.subplot(4,2,3)
plt.xlabel('X',font1) # x轴标签
plt.ylabel('Y',font1)
plt.title('Normal Moves of Eye',font1)  # 图的名称
plt.plot(x,y, color ='blue', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)





#接下来只针对x轴坐标的变化做出相空间重构

oldx=x[:-100]
len(oldx)
newx=x[100:]
plt.subplot(4,2,4)
plt.xlabel('X',font1) # x轴标签
plt.ylabel('delay X',font1)
plt.title('space reconstrut of 100 delay',font1)  # 图的名称
plt.plot(newx,oldx, color ='blue', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)

olddx=x[:-50]
len(oldx)
newwx=x[50:]
plt.subplot(4,2,5)
plt.xlabel('X',font1) # x轴标签
plt.ylabel('delay X',font1)
plt.title('space reconstrut of 50 delay',font1)  # 图的名称
plt.plot(newwx,olddx, color ='blue', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)

olddx=x[:-10]
len(oldx)
newwx=x[10:]
plt.subplot(4,2,6)
plt.xlabel('X',font1) # x轴标签
plt.ylabel('delay X',font1)
plt.title('space reconstrut of 10 delay',font1)  # 图的名称
plt.plot(newwx,olddx, color ='blue', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)


olddx=x[:-5]
len(oldx)
newwx=x[5:]
plt.subplot(4,2,7)
plt.xlabel('X',font1) # x轴标签
plt.ylabel('delay X',font1)
plt.title('space reconstrut of 5 delay',font1)  # 图的名称
plt.plot(newwx,olddx, color ='blue', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)


olddx=x
len(oldx)
newwx=x
plt.subplot(4,2,8)
plt.xlabel('X',font1) # x轴标签
plt.ylabel('X',font1)
plt.title('space reconstrut of No delay',font1)  # 图的名称
plt.plot(newwx,olddx, color ='blue', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('sample_img/{}_2d.png'.format(file.split('.')[0]), format='png')
#plt.savefig('sample_img/2d.png', format='png')
#做出相空间重构的3D视图


#plt.figure(1)
fig=plt.figure(figsize=(6,12),dpi=100)

plt.subplot(8,1,1)
#plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
#plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
stand=range(len(x))

#plt.xticks(range(len(x)),size=12,rotation=50) #设置字体大小和字体倾斜度
plt.xlabel('time',font1) # x轴标签
plt.ylabel('move',font1)
plt.title('X directions of Eye',font1)  # 图的名称
plt.plot(stand,x, color ='green', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)

plt.subplot(8,1,2)
plt.xlabel('time',font1) # x轴标签
plt.ylabel('move',font1)
plt.title('Y directions of Eye',font1)  # 图的名称
plt.plot(stand,y, color ='green', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)


plt.subplot(4,2,3)
plt.xlabel('X',font1) # x轴标签
plt.ylabel('Y',font1)
plt.title('Normal Moves of Eye',font1)  # 图的名称
plt.plot(x,y, color ='blue', linewidth=1, linestyle="-")
plt.legend()
plt.grid(True)

ax=plt.subplot(424,projection='3d')
x1=x[:-200]
print(len(x1))
x2=x[100:-100]
print(len(x2))
x3=x[200:]
print(len(x3))

ax.plot(x1,x2,x3,lw=0.5)

ax.set_xlabel("X delay 200",font1)
ax.set_ylabel("X delay 100",font1)
ax.set_zlabel("X",font1)

ax.set_title("3D space reconstruct of 100 delay",font1)

#https://blog.csdn.net/claroja/article/details/70841382
#https://blog.csdn.net/eddy_zheng/article/details/48713449

ax=plt.subplot(425,projection='3d')
x1=x[:-100]
print(len(x1))
x2=x[50:-50]
print(len(x2))
x3=x[100:]
print(len(x3))

ax.plot(x1,x2,x3,lw=0.5)

ax.set_xlabel("X delay 100",font1)
ax.set_ylabel("X delay 50",font1)
ax.set_zlabel("X",font1)

ax.set_title("3D space reconstruct of 50 delay",font1)

ax=plt.subplot(426,projection='3d')
x1=x[:-20]
print(len(x1))
x2=x[10:-10]
print(len(x2))
x3=x[20:]
print(len(x3))

ax.plot(x1,x2,x3,lw=0.5)

ax.set_xlabel("X delay 100",font1)
ax.set_ylabel("X delay 50",font1)
ax.set_zlabel("X",font1)

ax.set_title("3D space reconstruct of 10 delay",font1)

ax=plt.subplot(427,projection='3d')
x1=x[:-10]
print(len(x1))
x2=x[5:-5]
print(len(x2))
x3=x[10:]
print(len(x3))

ax.plot(x1,x2,x3,lw=0.5)

ax.set_xlabel("X delay 10",font1)
ax.set_ylabel("X delay 5",font1)
ax.set_zlabel("X",font1)

ax.set_title("3D space reconstruct of 5 delay",font1)

ax=plt.subplot(428,projection='3d')
x1=x
print(len(x1))
x2=x
print(len(x2))
x3=x
print(len(x3))

ax.plot(x1,x2,x3,lw=0.5)

ax.set_xlabel("X",font1)
ax.set_ylabel("X",font1)
ax.set_zlabel("X",font1)


ax.set_title("3D space reconstruct of NO delay",font1)
plt.tight_layout()
plt.savefig('sample_img/{}_3d.png'.format(file.split('.')[0]), format='png')
plt.show()