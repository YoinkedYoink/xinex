ModelConfidence = 0.85
MaxDetections = 5
UseHalfFloat = True

aimSpeed = 0.99
actRange = 200 #fov of aimbot
headshot = True
headshotSplit = 4 #e.g. 3 == 1/3 from the top of bounding box
aimPercision = 0.95
mouseMoveDelay = 0.00001

AimMethod = 1  # 1. Closest To Mouse
               # 2. Biggest Bounding Box
               # 3. Highest Confidence

triggerbot_key = 'n'
aimbot_key = 'x'
closeui_key = 'p'

MONITOR_SCALE = 3
target_fps = 50
ShowGUI = True

import numpy as np
lower_pink = np.array([130, 0, 120]) # BRG
upper_pink = np.array([255, 100, 230]) # BRG 

print("\033c", end='')
print("Importing dependencies")
import dxcam
from ultralytics import YOLO
#from PIL import Image, ImageTk
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
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from tkinter import *
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

                        cv2.rectangle(screenshot,(xmin,ymin),(xmax,ymax),(0,0,255),3)
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
                    if triggerbot == True and TryTrig[0] == True and screenshot_centre[0] in range(int(xmin),int(xmax)) and screenshot_centre[1] in range(int(ymin),int(ymax)):
                        TryTrig[0] = False
                        threading.Thread(target=triggerboot).start()
                    if aim_assist == True and close_p_dist < actRange and send_next[0] == True:
                        if screenshot_centre[0] in range(int(xmin),int(xmax)) and screenshot_centre[1] in range(int(ymin),int(ymax)):
                            if headshot == True:
                                xdif = (head_cent_list[0] - screenshot_centre[0]) * aimPercision
                                ydif = (head_cent_list[1] - screenshot_centre[1]) * aimPercision
                            else:
                                xdif = (body_cent_list[0] - screenshot_centre[0]) * aimPercision
                                ydif = (body_cent_list[1] - screenshot_centre[1]) * aimPercision
                        else:
                            if headshot == True:
                                xdif = (head_cent_list[0] - screenshot_centre[0]) * aimSpeed
                                ydif = (head_cent_list[1] - screenshot_centre[1]) * aimSpeed
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
            self.setFixedHeight(1080)
            self.setFixedWidth(1920)
            
            exit = QPushButton('Exit', self)
            exit.move(int(self.width()*0.93),int(self.height()*0.95))
            exit.clicked.connect(self.exitapp)
            
            self.placehold = QPushButton("CLICK", self)
            self.placehold.move(int(self.width()*0.5),int(self.height()*0.5))
            self.placehold.clicked.connect(self.placeclick)
            self.placehold.hide()
            
            self.settbutt = QPushButton('Settings', self)
            self.settbutt.move(int(self.width()*0.88),int(self.height()*0.95))
            self.settbutt.clicked.connect(self.opensett)
            
            self.stats = QLabel(self)
            #label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            self.stats.setText("oop")
            self.stats.move(int(self.width()/15),int(self.height()/15))
            self.stats.resize(70,50)
            self.stats.setStyleSheet('background-color: yellow;border: 1px solid red')
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_ui)
            self.timer.start(10)
            
        def update_ui(self):
            self.stats.setText("fps: "+ str(fps) + "\naim: "+ str(aim_assist) +"\nhit: " + str(triggerbot))
            
        def opensett(self):
            print("Opening settings")
            self.placehold.show()
            
        def placeclick(self):
            print("clickclack")
            self.placehold.hide()
        
        # def center(self):
        #     qr = self.frameGeometry()
        #     cp = QDesktopWidget().availableGeometry().center()
        #     qr.moveCenter(cp)
        #     self.move(qr.topLeft())   
        
        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setPen(QPen())
            painter.drawEllipse(int((MONITOR_WIDTH/2)-actRange),int((MONITOR_HEIGHT/2)-actRange),actRange*2,actRange*2)
            
        
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = MainWindow()
        t = threading.Thread(target=MainWindow.actualclusterfuck, daemon=True)
        t.start()
        ex.show()
        sys.exit(app.exec_())
        
GUIRun()