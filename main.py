# -*- coding:utf-8 -*-
import sys,openpyxl,xlwt
from openpyxl import Workbook
import matplotlib
import sys

from PyQt5.QtCore import *
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from influxdb import InfluxDBClient
import csv

from multiprocessing import Queue

q=Queue(maxsize=5)

global count
global filename
global ppp #函数间隔
global mubiao   #目标文件夹全局变量


class Example(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1000, 500)
        self.setWindowTitle('春风不度玉门关')

        exitAction = QAction(QIcon('exit.png'), '&退出', self)       
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('退出软件')
        exitAction.triggered.connect(self.close)

        bxitAction = QAction(QIcon('exit.png'), '&帮助', self)       
        bxitAction.setShortcut('Ctrl+H')
        bxitAction.setStatusTip('帮助文档')  #状态栏提示
        #bxitAction.triggered.connect(self.show_child)

        self.statusBar().showMessage('状态栏',0)
        self.statusBar().setStyleSheet("background-color:green")
 
        #self.statusBar()
        #self.statusBar.setStyleSheet("background-color:gray")
        menubar = self.menuBar()
        aMenu = menubar.addMenu('&菜单')
        aMenu.addAction(exitAction)
        aMenu.addAction(bxitAction)

        bMenu = menubar.addMenu('&教程')
        bMenu.addAction(bxitAction)


        #选择文件按钮
        self.start = QPushButton(self)
        self.start.setText("选择文件")         #按钮文本
        self.start.move(20,50)                   #按钮位s置
        self.start.clicked.connect(self.open_file)


        #文件路径
        self.readlen=QLabel(self)
        self.readlen.setGeometry(150,55,200,20)
        self.readlen.setText("文件路径：")
        #文件路径输入框
        self.time0=QLineEdit(self)
        self.time0.setGeometry(220,55,250,20)
        self.time0.setText("选择文件或者手动输入路径")

        #文件行数
        self.readlen1=QLabel(self)
        self.readlen1.setGeometry(490,55,200,20)
        self.readlen1.setText("行数：")
        self.time1=QLineEdit(self)
        self.time1.setGeometry(540,55,250,20)
        self.time1.setText("选择文件或者手动输入路径")

        #设定间隔
        self.readlen1=QLabel(self)
        self.readlen1.setGeometry(20,100,200,20)
        self.readlen1.setText("设定采样间隔：")
        self.time2=QLineEdit(self)
        self.time2.setGeometry(150,100,100,20)
        

        #计算行数
        self.start9 = QPushButton(self)
        self.start9.setText("预估行数：")         #按钮文本
        self.start9.move(300,100)                   #按钮位s置
        self.start9.clicked.connect(self.jsfile)
        self.time3=QLineEdit(self)
        self.time3.setGeometry(450,100,100,20)

        #选择目标文件夹按钮
        self.start90 = QPushButton(self)
        self.start90.setText("选择目标文件夹")         #按钮文本
        self.start90.move(20,300)                   #按钮位s置
        self.start90.clicked.connect(self.xz)

        #显示目标路径
        self.readlen2=QLabel(self)
        self.readlen2.setGeometry(200,290,200,50)  #位置，大小
        self.readlen2.setText("目标路径：")
        self.t=QLineEdit(self)
        self.t.setGeometry(150,300,200,30)
        self.t.setText("选择文件或者手动输入路径")

        #请输入文件名.csv
        self.t11=QLineEdit(self)
        self.t11.setGeometry(360,300,200,30)
        self.t11.setText("请输入文件名.csv")




        #提取
        self.start9 = QPushButton(self)
        self.start9.setText("提取")         #按钮文本
        self.start9.move(50,400)                   #按钮位s置
        self.start9.clicked.connect(self.tq)
        

        self.show()
    

    def open_file(self):
        global filename
        filename,_ = QFileDialog.getOpenFileName(self);
        #text=open(filename,'r').read()
        global count
        count=0
        if filename:
            print(filename)
            self.time0.setText(filename)

            with open(filename)as f:
                for row in f:
                    count += 1
        
        print(count)
        self.time1.setText(str(count))
    
    #计算文件行数
    def jsfile(self):
        pp=self.time2.text()
        global ppp
        ppp=int(pp)
        global count
        pppp=ppp+1
        self.time3.setText(str(int(count/pppp)))
    
    #选择目标文件夹
    def xz(self):
        s=QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
        try:
            global mubiao
            mubiao=s
            self.t.setText(s)
        except:
            pass

    #提取按钮，重新写入新文件
    def tq(self):
        rows=[]
        p=0
        global filename,ppp,count,mubiao
        h=int(self.time2.text())  #获取设定的文件行数
        mz=self.t11.text()
        mzz=mubiao+"/"+mz
        with open(filename,'r') as f:
            for i in f:
                p=p+1

                xpo=[]
                for xp in i.split(','):
                    xpo.append(xp.replace("\n",""))
                    

                rows.append(xpo)
                
                #rows.append(i.split(','))
                if p>10000:
                    print(sys.getsizeof(rows))
                    with open(mzz,"a+",newline='') as csvfile:
                        writer = csv.writer(csvfile)
                   #写入多行用writerows
                        for i in range(len(rows)):
                            if i%(h+1)==0:
                               writer.writerows([rows[i]])
                        rows.clear()
                        p=0
                    xpo.clear()
        with open(mzz,"a+",newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(len(rows)):
                if i%(h+1)==0:
                   writer.writerows([rows[i]])
                



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    

    
    sys.exit(app.exec_())
