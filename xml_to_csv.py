import os 
import xml.dom.minidom as xmldom
from xml.etree import ElementTree as ET


def read_xml(file_name_path,csv_path):

    csv_path=os.path.join(csv_path,"info.csv")
    with open(csv_path, "a", encoding="gbk") as f:
        f.write("label_name"+","+"file_name"+","+"\n")
    #载入数据 
    tree=ET.parse(file_name_path)
    #获取根节点
    root=tree.getroot()
    # root=root.getro#ot()
    print(root)
   #     print(len(root))
#     print(root)
#     1795
# <Element 'Annotations' at 0x0000000002A3F318>
    for i in root:
        #i.getElementsByTagName("name")[0].firstChild.data
        print(i)
        # <Element 'Annotation' at 0x0000000002E99868>
        print(i.tag)
        # Annotation

        print(i.attrib)#{}

        print(i[0].text)
        print(i[1].text)

        with open(csv_path, "a", encoding="gbk") as f:
            f.write(label_name+","+file_name+","+"\n")

        # print(i.getElementsByTagName("name")[0].firstChild.data)   

    #     print(len(root))
#     print(root)
#     1795
# <Element 'Annotations' at 0x0000000002A3F318>

#     dom = ET.fromstring(Annotation_Annotations_as_string)

# #从内存字符串中解析xml
#     print(dom)
#     print(len(dom))
#    # for i in range(len(root)):



    


    # dom = xmldom.parse(file_name_path)
    # root = dom.documentElement

    # total_anno=root.getElementsByTagName("Annotation")
    # print(len(total_anno))
    # total_name=root.getElementsByTagName("name")
    # print(len(total_name))





    # file_name = root.getElementsByTagName("name")[0].firstChild.data

    # files_name = root.getElementsByTagName("name")

    # print(files_name)
    # for files in files_name:
    #     file_name=files.getElementsByTagName()

    #     # 先判断存在几个缺陷.
    #     for i in range(len(root.getElementsByTagName("annotation"))):
    #         label_name = root.getElementsByTagName("defect_name")[i].firstChild.data


    #         with open(csv_path, "a", encoding="gbk") as f:
    #             f.write(label_name+","+file_name+","+"\n")
    # f.close()
    # return csv_path

if __name__=="__main__":
    csv_path=r"C:\\Users\\kkouba\\Desktop\\xml"
    file_path=r"C:\\Users\\kkouba\\Desktop\\xml\\anno_train.xml"
    csv=read_xml(file_name_path=file_path,csv_path=csv_path)