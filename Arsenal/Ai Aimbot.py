ModelConfidence = 0.65
MaxDetections = 5
UseHalfFloat = True

aimSpeed = 1
actRange = 150 #fov of aimbot
headshot = False
headshotSplit = 5 #e.g. 3 == 1/3 from the top of bounding box
aimPercision = 1
mouseMoveDelay = 0

AimMethod = 1  # 1. Closest To Mouse
               # 2. Biggest Bounding Box
               # 3. Highest Confidence

triggerbot_key = 'n'
aimbot_key = 'x'
closeui_key = 'p'

MONITOR_SCALE = 4
target_fps = 55
ShowGUI = True

import numpy as np
lower_pink = np.array([200, 0, 200]) # BRG
upper_pink = np.array([201, 0, 201]) # BRG 

print("\033c", end='')
print("Importing dependencies")
import dxcam
from ultralytics import YOLO
import cv2
import time
import math
import keyboard
import threading
import sys
import win32api, win32con
import ctypes
from PyQt5.QtGui import QPainter, QPen
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QSlider
from tkinter import Tk
from tkinter.filedialog import askopenfilename

MONITOR_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
MONITOR_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

print("Monitor resolution: " + str(MONITOR_WIDTH) +"x"+ str(MONITOR_HEIGHT))

Tk().withdraw()
ModelPath = askopenfilename(filetypes=[("Model File", "*.pt *.onnx *.engine")])

region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
x,y,width,height = region
screenshot_centre = [int((width-x)/2),int((height-y)/2)]
emptynumpy = np.zeros((height, width, 4), dtype=np.uint8)
emptynumpy[:,:,3] = 0
camera = dxcam.create()

model = YOLO(ModelPath)
model.conf = ModelConfidence
model.max_det = MaxDetections
model.half = UseHalfFloat

start_time = time.time()
PussyHole = 1
counter = 1
fps = 0
TryTrig = [True]

triggerbot = False
trigerbot_toggle = [True]
aim_assist = False
aim_assist_toggle = [True]
    
def triggerboot():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,screenshot_centre[0],screenshot_centre[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,screenshot_centre[0],screenshot_centre[1],0,0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,screenshot_centre[0],screenshot_centre[1],0,0)    
    TryTrig[0] = True
    
def GUIRun():
    class MainWindow(QMainWindow):
        def actualclusterfuck():
            global triggerbot
            global aim_assist
            send_next = [True]
            def cooldown(cooldown_bool,wait):
                time.sleep(wait)
                cooldown_bool[0] = True
                
            camera.start(region,target_fps)
            while True:
                close_p_dist = 100000000
                close_p = -1
                screenshot = camera.get_latest_frame()
                if type(screenshot) == np.ndarray:
                    screenshot = cv2.inRange(screenshot, lower_pink, upper_pink)
                    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2BGR)
                    df = model.predict(source=screenshot, verbose=False)
                    boxes = df[0].boxes
                    df = 0

                for i in range (0,MaxDetections):
                    try:
                        df = boxes[i].xyxy[0]
                        xmin = int(df[0])
                        ymin = int(df[1])
                        xmax = int(df[2])
                        ymax = int(df[3])

                        centerX = (xmax-xmin)/2+xmin
                        centerY = (ymax-ymin)/2+ymin

                        distance = math.dist([centerX,centerY],screenshot_centre)

                        if int(distance) < close_p_dist:
                            close_p_dist = distance
                            close_p = i

                        #cv2.rectangle(screenshot,(xmin,ymin),(xmax,ymax),(0,0,255),3)
                    except:
                        pass

                if keyboard.is_pressed(triggerbot_key):
                    if trigerbot_toggle[0] == True:
                        triggerbot = not triggerbot
                        print(triggerbot)
                        trigerbot_toggle[0] = False
                        thread = threading.Thread(target=cooldown, args=(trigerbot_toggle,0.3,))
                        thread.start()

                if keyboard.is_pressed(aimbot_key):
                    aim_assist = True
                else:
                    aim_assist = False
                    # if aim_assist_toggle[0] == True:
                    #     aim_assist = not aim_assist
                    #     print(aim_assist)
                    #     aim_assist_toggle[0] = False
                    #     thread = threading.Thread(target=cooldown, args=(aim_assist_toggle,5,))
                    #     thread.start()
                        

                if close_p != -1:
                    df = boxes[close_p].xyxy[0]
                    xmin = df[0]
                    ymin = df[1]
                    xmax = df[2]
                    ymax = df[3]

                    body_cent_list = [(xmax+xmin)/2,(ymax+ymin)/2]
                    head_cent_list = [(xmax+xmin)/2,((ymax - ymin)/headshotSplit)+ymin]
                    if aim_assist == True and close_p_dist < actRange and send_next[0] == True:
                        if screenshot_centre[0] in range(int(xmin),int(xmax)) and screenshot_centre[1] in range(int(ymin),int(ymax)):
                            if headshot == True:
                                if int(head_cent_list[1]) == int(ymin):
                                    hitbuff = 1
                                    print("added buffer")
                                else:
                                    hitbuff = 0
                                xdif = (head_cent_list[0] - screenshot_centre[0]) * aimPercision
                                ydif = (head_cent_list[1]+hitbuff - screenshot_centre[1]) * aimPercision
                            else:
                                xdif = (body_cent_list[0] - screenshot_centre[0]) * aimPercision
                                ydif = (body_cent_list[1] - screenshot_centre[1]) * aimPercision
                        else:
                            if headshot == True:
                                if int(head_cent_list[1]) == int(ymin):
                                    hitbuff = 1
                                    print("added buffer")
                                else:
                                    hitbuff = 0
                                xdif = (head_cent_list[0] - screenshot_centre[0]) * aimSpeed
                                ydif = (head_cent_list[1]+hitbuff - screenshot_centre[1]) * aimSpeed
                            else:
                                xdif = (body_cent_list[0] - screenshot_centre[0]) * aimSpeed
                                ydif = (body_cent_list[1] - screenshot_centre[1]) * aimSpeed
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(xdif),int(ydif),0,0)
                        xdif=0
                        ydif=0
                        if mouseMoveDelay != 0:
                            send_next[0] = False
                            thread = threading.Thread(target=cooldown, args=(send_next,mouseMoveDelay,))
                            thread.start()
                            
                    if triggerbot == True and TryTrig[0] == True and screenshot_centre[0] in range(int(xmin),int(xmax)) and screenshot_centre[1] in range(int(ymin),int(ymax)):
                        TryTrig[0] = False
                        threading.Thread(target=triggerboot).start()
                        
                def fpscount():
                    global fps
                    fps = fps
                    global start_time, PussyHole, counter
                    counter += 1
                    if(time.time() - start_time) > PussyHole:
                        fps = str(int(counter/(time.time()-start_time)))
                        if int(fps) > 700 or int(fps) <= 5:
                            fps = "Likely Idle"
                        else:
                            print(fps)
                        counter = 0
                        start_time = time.time()
                fpscount()
        
        def exitapp(self):
            print("bye bye")
            sys.exit(app.exec_())
        
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Cool Overlay")
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            #self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
            #self.setAttribute(QtCore.Qt.WA_NoChildEventsForParent, True)
            self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint 
                                | QtCore.Qt.WindowStaysOnTopHint
                                | QtCore.Qt.WindowDoesNotAcceptFocus
                                #| QtCore.Qt.WindowTransparentForInput
                                )
            self.setFixedHeight(int(MONITOR_HEIGHT))
            self.setFixedWidth(int(MONITOR_WIDTH))
            
            exit = QPushButton('Exit', self)
            exit.move(int(self.width()*0.93),int(self.height()*0.95))
            exit.clicked.connect(self.exitapp)
            
            self.TriggerButton = QPushButton("Triggerbot: "+str(triggerbot), self)
            self.TriggerButton.move(int(self.width()*0.45),int(self.height()*0.45))
            self.TriggerButton.clicked.connect(self.TriggerButtonFunc)
            self.TriggerButton.hide()
            
            self.HeadshotButton = QPushButton("Headshot: "+str(headshot), self)
            self.HeadshotButton.move(int(self.width()*0.5),int(self.height()*0.45))
            self.HeadshotButton.clicked.connect(self.HeadShotButtonFunc)
            self.HeadshotButton.hide()
            
            self.aimslider = QSlider(QtCore.Qt.Horizontal, self)
            self.aimslider.setGeometry(QtCore.QRect(int(self.width()*0.45),int(self.height()*0.5),80,10))
            self.aimslider.setRange(0,100)
            self.aimslider.valueChanged.connect(self.aimsliderFunc)
            self.aimslider.hide()
            
            self.aimsilderlabel = QLabel(self)
            self.aimsilderlabel.setText(str(aimSpeed)+"x Aim Speed")
            self.aimsilderlabel.move(int(self.width()*0.5),int(self.height()*0.5))
            self.aimsilderlabel.setStyleSheet('background-color: white;border: 1px solid black')
            self.aimsilderlabel.hide()
            
            self.Percissionaimslider = QSlider(QtCore.Qt.Horizontal, self)
            self.Percissionaimslider.setGeometry(QtCore.QRect(int(self.width()*0.45),int(self.height()*0.55),80,10))
            self.Percissionaimslider.setRange(0,100)
            self.Percissionaimslider.valueChanged.connect(self.PercissionaimsliderFunc)
            self.Percissionaimslider.hide()
            
            self.Percissionaimsilderlabel = QLabel(self)
            self.Percissionaimsilderlabel.setText(str(aimSpeed)+"x Percission Aim")
            self.Percissionaimsilderlabel.move(int(self.width()*0.5),int(self.height()*0.55))
            self.Percissionaimsilderlabel.setStyleSheet('background-color: white;border: 1px solid black')
            self.Percissionaimsilderlabel.hide()
            
            self.settbutt = QPushButton('Open Sett', self)
            self.settbutt.move(int(self.width()*0.88),int(self.height()*0.95))
            self.settbutt.clicked.connect(self.opensett)
            
            self.stats = QLabel(self)
            #label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            self.stats.setText("oop")
            self.stats.move(int(self.width()/15),int(self.height()/15))
            self.stats.resize(70,50)
            self.stats.setStyleSheet('background-color: yellow;border: 1px solid red')
            self.stats.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_ui)
            self.timer.start(10)
            
        def update_ui(self):
            self.stats.setText("fps: "+ str(fps) + "\naim: "+ str(aim_assist) +"\nhit: " + str(triggerbot))
            
        def opensett(self):
            print("Opening settings")
            if self.TriggerButton.isVisible() == False:
                self.settbutt.setText("Close Sett")
                self.TriggerButton.show()
                self.HeadshotButton.show()
                self.aimslider.show()
                self.aimsilderlabel.show()
                self.Percissionaimslider.show()
                self.Percissionaimsilderlabel.show()
            else:
                self.settbutt.setText("Open Sett")
                self.TriggerButton.hide()
                self.HeadshotButton.hide()
                self.aimslider.hide()
                self.aimsilderlabel.hide()
                self.Percissionaimslider.hide()
                self.Percissionaimsilderlabel.hide()
            
        def TriggerButtonFunc(self):
            global triggerbot
            triggerbot = not triggerbot
            print("Triggerbot: "+str(triggerbot))
            self.TriggerButton.setText("Triggerbot: "+str(triggerbot))
            
        def HeadShotButtonFunc(self):
            global headshot
            headshot = not headshot
            print("Headshot: "+str(headshot))
            self.HeadshotButton.setText("Headshot: "+str(headshot))
            
        def aimsliderFunc(self, val):
            global aimSpeed
            aimSpeed = val/100
            self.aimsilderlabel.setText(str(aimSpeed)+"x Aim Speed")
            
        def PercissionaimsliderFunc(self, val):
            global aimPercision
            aimPercision = val/100
            self.Percissionaimsilderlabel.setText(str(aimPercision)+"x Percission Aim")
        
        # def center(self):
        #     qr = self.frameGeometry()
        #     cp = QDesktopWidget().availableGeometry().center()
        #     qr.moveCenter(cp)
        #     self.move(qr.topLeft())   
        
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setPen(QPen())
            self.eclipse = painter.drawEllipse(int((MONITOR_WIDTH/2)-actRange),int((MONITOR_HEIGHT/2)-actRange),actRange*2,actRange*2)
            
        
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = MainWindow()
        t = threading.Thread(target=MainWindow.actualclusterfuck, daemon=True)
        t.start()
        ex.show()
        sys.exit(app.exec_())
        
GUIRun()