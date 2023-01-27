import warnings
warnings.filterwarnings('ignore')

import filecmp

import cv2
import math
import os 
import numpy as np 
from datetime import datetime

import imutils
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QImage 
from PyQt5.QtWidgets import  QApplication, QWidget, QVBoxLayout, QPushButton,QFileDialog, QLabel, QTextEdit
from skimage.metrics import structural_similarity
from imutils import contours, perspective
from scipy.spatial import distance as dist

from natsort import natsort

from ui_MainWindow import *

class Main_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(Main_Window, self).__init__(parent=parent)

        if True: 
            self.anapencere = Ui_MainWindow()
            self.anapencere.setupUi(self)

            self.anapencere.pushButtonSelectFile.clicked.connect(self.process_image_start)
            self.anapencere.pushButtonSelectFile.clicked.connect(self.choose_image)
            self.anapencere.pushButtonRead.clicked.connect(self.image_process)
            self.anapencere.pushButtonStart.clicked.connect(self.choose_image)
            self.anapencere.pushButtonSave.clicked.connect(self.save_date)
 
    def process_image_start(self):
        print("Process i start...")

        self.fname = QFileDialog.getOpenFileName(self, "Open file", "C:/Users/*.jpg")

        self.imagePath = self.fname[0]
        pixmap = QPixmap(self.imagePath)
        self.anapencere.label_Img_Photo_1.setPixmap(QPixmap(pixmap))

    def  choose_image(self):
        print( "Choose Process..")

        self.image = self.imagePath
        self.image_new = cv2.imread(self.image)
        self.image_new = cv2.resize(self.image_new,(683,512))

        height,width,channel = self.image_new.shape
        step = channel*width

        self.qImg = QImage(self.image_new.data, width, height, step, QImage.Format_RGB888)
        self.anapencere.label_Img_Photo_1.setPixmap(QtGui.QPixmap.fromImage(self.qImg))
       

    def image_process(self):
        print("Image process")

        # gray, blur, adptive threshold.
        gray = cv2.cvtColor(self.image_new, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11,5), 0)
        thresh = cv2.threshold(blur, 0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,kernel)


        cnts = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        detector = cv2.SimpleBlobDetector_create ()
        keypoints = detector.detect(thresh)

        total_count = 0
        for i in keypoints:
            total_count = total_count + 1

        self.anapencere.label_Toplam_Bubble_Num.setText("Toplam Bubble Sayısı : {}".format(f'{total_count}')) 

        for c in cnts:

            # find primeter of countour
            primeter = cv2.arcLength(c,True)

            #perform contour approximation
            approx = cv2.approxPolyDP(c, 0.04 * primeter, True)
            if len (approx) > 6:
                x,y,w,h = cv2.boundingRect(c)
                diameter = w
                radius = w/2

                # find centroid
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m10"] / M["m00"])

                # Draw the contour and center of the shape on image 
                cv2.rectangle(self.image_new, (x,y), (x+w, y+h), (0,255,0), 4)
                cv2.drawContours(self.image_new, [c], 0, (36,255,12), 4)
                cv2.circle(self.image_new, (cX,cY), 15, (32,159,22), -1)

                # draw line and diameter  information 
                cv2.line(self.image_new,  (x,y + int(h/2)), (x + w,y + int(h/2)), (156,188,24),3)
                cv2.putText(self.image_new, "Diameter: {}".format(diameter),(cX-50, cY-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(160,255,255),1)

                self.anapencere.label_Toplam_Bubble_Alan.setText("Toplam Bubble Alanı: {}".format(f'{diameter}'))

                height, width, channel = self.image_new.shape
                step = channel * width
                self.qImg = QImage(self.image_new.data, width, height, step, QImage.Format_RGB888)
                self.anapencere.label_Image_photo_2.setPixmap(QtGui.QPixmap.fromImage(self.qImg))

                # Image name 
                image_name = "Image_name :{}".format(f'{self.image}')
                print(image_name)

                # count the number of circles
                label_count = "total_count_buble :{}".format(f'{total_count}')
                print(label_count)

                # buble total area ccalculation 
                label_diameter = "diameter_bubble:{}".format(f'{diameter}')
                print(label_diameter)

                # ımage, date and time information
                location = "Buble_Date:{}".format(f'{datetime.now(): %Y-%m-%d}')
                print(location)

    def save_date(self):
        pass

if __name__  == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    pencere = Main_Window()
    pencere.show()
    sys.exit(app.exec_())