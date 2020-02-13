import os
# 将所有图片的路径转化为一个列表
from imutils import paths
# 读取xml文件
import xml.dom.minidom as xmldom
# 解析器
import argparse
# 复制文件
import shutil
import pandas as pd

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


#定义解析器

def args_parse():
    arg=argparse.ArgumentParser()
    arg.add_argument("-Opath","--origin_path",required=True,help="origin file path")
    arg.add_argument("-Npath","--new_path",required=True,help="new file path")
    ap=vars(arg.parse_args())
    return ap

def copy_file(origin_path, new_path):
    name_labels = list(os.listdir(origin_path))

    # 提取label下的xml文件，并复制一份
    os.makedirs(new_path)

    normal_num = []
    normal_label = []
    # 遍历文件夹
    for name_label in name_labels:
        # 所有文件路径
        name_label_files = list(os.listdir(os.path.join(origin_path, name_label)))

        os.makedirs(os.path.join(new_path, name_label))
        new_annotation_path = os.path.join(new_path, name_label)
        
        # 如果文件夹下文件全部是图片

        if len(list(os.listdir(os.path.join(origin_path,name_label)))) == len(list(paths.list_images(os.path.join(origin_path,name_label)))):
            normal_label.append(name_label)
            normal_num.append(len(list(paths.list_images(os.path.join(origin_path,name_label)))))
            for file_name in name_label_files:
                origin_xml_path = os.path.join(origin_path, name_label, file_name)
                new_xml_path = os.path.join(new_path, name_label, file_name)
                shutil.copy(origin_xml_path, new_xml_path)       
            continue       

        for file_name in name_label_files:

            if file_name.split(".")[-1] == "xml":
                origin_xml_path = os.path.join(origin_path, name_label, file_name)
                new_xml_path = os.path.join(new_path, name_label, file_name)
                shutil.copy(origin_xml_path, new_xml_path)
    return normal_num, normal_label


# 读取XML文件并保存在csv中

def read_xml(new_path,normal_labels):
    name_labels=os.listdir(new_path)
    csv_path=os.path.join(new_path,"info.csv")
    with open(csv_path, "a", encoding="gbk") as f:
        f.write("label_name"+","+"file_name"+","+"width"+","+"height"+","
            + "depth"+","+"xmin"+","+"ymin"+","+"xmax"+","+"ymax"+","+"percent"+"\n")
    
    for label_name in name_labels:
        if label_name in normal_labels:
            continue
        label_name_path = os.path.join(new_path, label_name)
        files_name = list(os.listdir(label_name_path))
        for file_name in files_name:
            file_name_path = os.path.join(label_name_path, file_name)
            dom = xmldom.parse(file_name_path)
            root = dom.documentElement

            file_name = root.getElementsByTagName("filename")[0].firstChild.data
            width = root.getElementsByTagName("width")[0].firstChild.data
            height = root.getElementsByTagName("height")[0].firstChild.data
            depth = root.getElementsByTagName("depth")[0].firstChild.data

            # 先判断存在几个缺陷.
            for i in range(len(root.getElementsByTagName("object"))):
                label_name = root.getElementsByTagName("name")[i].firstChild.data
                xmin = root.getElementsByTagName("xmin")[i].firstChild.data
                ymin = root.getElementsByTagName("ymin")[i].firstChild.data
                xmax = root.getElementsByTagName("xmax")[i].firstChild.data
                ymax = root.getElementsByTagName("ymax")[i].firstChild.data
                area_1 = abs(int(xmax)-int(xmin))*abs(int(ymax)-int(ymin))*100
                area_2 = int(width)*int(height) 
                percent = round(area_1/area_2, 2)

                with open(csv_path, "a", encoding="gbk") as f:
                    f.write(label_name+","+file_name+","+width+","+height+","+depth+","
                            + xmin+","+ymin+","+xmax+","+ymax+","+str(percent)+"\n")
    f.close()
    return csv_path

# 统计csv画直方图
def read_csv(new_path,csv_path,normal_num, normal_label):
    print("normal_num",normal_num)
    print("normal_label",normal_label)
    df = pd.read_csv(csv_path, encoding="gbk")
    # 统计各个label下xml文件的个数
    label_numfile_Se = df.loc[:, "label_name"].value_counts()
    big_num_Se = label_numfile_Se[label_numfile_Se.values >= 10]

    big_labels_list = list(big_num_Se.index)
    big_num_list = list(big_num_Se.values)

    other_num_list=[]
    other_num_list.append(int(label_numfile_Se[label_numfile_Se.values < 10].sum()))
    other_label_list = ["其他"]

    # 准备数据
    x = normal_label+big_labels_list+other_label_list
    height = normal_num+big_num_list+other_num_list
    
    # 图的尺寸
    plt.figure(figsize=(40, 30), dpi=96)
    
    # 图的名称
    plt.title("bar_figure",fontsize=80,y=1.02)

    # 画直方图
    plt.bar(x, height, color=["r", "g", "b", "k", "m", "c", "y"],ec="k")

    # 添加刻度
    plt.xticks(range(len(x)), x)#plt.xticks(range(len(x)), x)
    plt.yticks(range(0, max(height)+50, 100))
    plt.tick_params(labelsize=50)

    # 添加标签
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 80,
             }
    plt.xlabel("label", fontdict=font2)#fontsize=80
    plt.ylabel("number",fontdict=font2)

    #添加网格
    plt.grid(axis="y",alpha=0.75)#alpha透明度,linewidth=1.0

    #添加数据标签
    for x_1,height_1 in zip(x,height):
        plt.text(x_1,height_1+5,"%.0f"%height_1,ha="center",fontsize=45,va="bottom")

    #边框设计
    ax=plt.gca()
    ax.spines["bottom"].set_linewidth(2.5)
    ax.spines["top"].set_linewidth(2.5)
    ax.spines["left"].set_linewidth(2.5)
    ax.spines["right"].set_linewidth(2.5)
    #ax.spines["bottom"].set_color()#设置 底部颜色

    #显示图例
    # plt.legend()

    #保存图片 
    bar_path=os.path.join(new_path,"bar.png")  
    plt.savefig(bar_path)

    #画饼状图
    plt.figure(figsize=(8,8),dpi=96)#正方形

    # fig=plt.figure(figsize=(8,8))
    # fig.subplot(2,2,1)  #分四块，放在第一块

    #给画板来个名字
    plt.title("defect cover",fontsize=100)

    #数据
    small_1=len(df[df["percent"]<1])
    mid_1=len(df[(df["percent"]<10)&(df["percent"]>1)])
    big_1=len(df[df["percent"]>10])

    values_2=[big_1,mid_1,small_1]
    labels=["大于10%","不超过10%","不超过1%"]
    explode=[0.03,0.02,0.01]#离中心的距离
    
    #画图
    #值，距中心距离，标签，保留百分数,圆的直径，旋转方向，边框属性，文本属性，圆中心，阴影
    plt.pie(values_2,explode=explode,labels=labels,autopct="%.2f%%",
            wedgeprops={"linewidth":0.6,"edgecolor":"red"},
            textprops={"fontsize":20,"color":"k"},
            center=(0,0),
            radius=0.9,
            pctdistance=0.7,labeldistance=1.2,
            counterclock=False,
            shadow=True)
    #显示图例
    plt.legend()
    pie_path=os.path.join(new_path,"pie.png")
    plt.savefig(pie_path)

    #画方形图
   
    #差值
    df["x_difference"]=df["xmax"]-df["xmin"]
    df["y_difference"]=df["ymax"]-df["ymin"]

    x_difference=np.array(abs(df["x_difference"]))
    #组距

    distance=100
    #组数
    x_max=max(x_difference)
    x_min=min(x_difference)
    group_num=math.ceil((x_max-x_min)/distance)

    #确定刻度值
    #起始刻度
    first_ticks=math.floor(x_min/distance)
    #算上起始和终止
    group_num=group_num+first_ticks+1
    x_list=[]
    for i in range(group_num):
        x_list.append(i*100)

    #画板大小
    plt.figure(figsize=(40,30),dpi=96)
    #标题
    plt.title("x轴缺陷尺度变化图",fontsize=60,y=1.02)

    #画图
    plt.hist(x_difference,x_list,color="r",edgecolor="k")#rwidth=0.75,

    #调整刻度
    ticks_distance=500
    ticks_num=math.floor((max(x_list)-min(x_list))/ticks_distance)

    ticks_list=[]
    for i in range(ticks_num):
        ticks_list.append(min(x_list)+(i*500))
    ticks_list.append(max(x_list))
    plt.xticks(ticks_list)

    plt.tick_params(labelsize=50)

    #plt.ylim()

    #标签

    plt.xlabel("difference_value",fontsize=60)#fontdict
    plt.ylabel("counts",fontsize=60)

    #网格
    plt.grid(axis="y",alpha=0.75,linewidth=1.0)

    #添加数据标签
    # for a,b in zip(x_difference,x_list):
    #     plt.text(a,b,"%.0f"%b,ha="center",va="bottom",fontsize=20)

    #边框设计
    ax=plt.gca()
    ax.spines["bottom"].set_linewidth(2.5)
    ax.spines["top"].set_linewidth(2.5)
    ax.spines["left"].set_linewidth(2.5)
    ax.spines["right"].set_linewidth(2.5)
    #显示图例
    #plt.legend()

    #保存图片
    hist_1_path=os.path.join(new_path,"pist_1.png")
    plt.savefig(hist_1_path)


    y_difference=np.array(abs(df["y_difference"]))
    #组距

    distance=100
    # print(x_max)
    # print(x_min)
    #组数
    y_max=max(y_difference)
    y_min=min(y_difference)
    group_num=math.ceil((y_max-y_min)/distance)
    print(y_max)
    print(y_min)

    #确定刻度值
    #起始刻度
    first_ticks=math.floor(y_min/distance)
    #算上起始和终止
    group_num=group_num+first_ticks+1
    y_list=[]
    for i in range(group_num):
        y_list.append(i*100)

    #画板大小
    plt.figure(figsize=(40,30),dpi=96)
    #标题
    plt.title("y轴缺陷尺度变化图",fontsize=60,y=1.02)

    #画图
    n_y,bins_limit_y,patches_y=plt.hist(y_difference,y_list,color="r",edgecolor="k")#rwidth=0.75,

    #调整刻度
    ticks_distance=500
    ticks_num=math.ceil((max(y_list)-min(y_list))/ticks_distance)

    ticks_list=[]
    for i in range(ticks_num):
        ticks_list.append(min(y_list)+(i*500))
    ticks_list.append(max(y_list))
    plt.xticks(ticks_list)

    print(ticks_list)
    #plt.xticks(y_list)
    plt.tick_params(labelsize=50)
    #plt.ylim()

    #标签

    plt.xlabel("difference_value",fontsize=60)#fontdict
    plt.ylabel("counts",fontsize=60)

    #网格
    plt.grid(axis="y",alpha=0.75,linewidth=1.0)

    #添加数据标签
    for a,b in zip(bins_limit_y,n_y):
        plt.text(a+45,b+1,"%.0f"%b,ha="center",va="bottom",fontsize=60)

    #边框设计
    ax=plt.gca()
    ax.spines["bottom"].set_linewidth(2.5)
    ax.spines["top"].set_linewidth(2.5)
    ax.spines["left"].set_linewidth(2.5)
    ax.spines["right"].set_linewidth(2.5)
    #显示图例
    #plt.legend()
    #显示图片
    hist_2_path=os.path.join(new_path,"hist_2.png")
    plt.savefig(hist_2_path)


if __name__=="__main__":
    ap=args_parse()
    origin_path=ap["origin_path"]
    new_path=ap["new_path"]
    normal_num, normal_labels=copy_file(origin_path, new_path)
    csv_path=read_xml(new_path,normal_labels)
    read_csv(new_path,csv_path, normal_num, normal_labels)




