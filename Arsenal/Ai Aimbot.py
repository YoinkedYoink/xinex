ModelConfidence = 0.7
MaxDetections = 5
UseHalfFloat = False

aimSpeed = 1
actRange = 900
headshot = True
headshotSplit = 3 #e.g. 3 == 1/3 from the top of bounding box
aimPercision = 0.6
mouseMoveDelay = 0.01

AimMethod = 1  # 1. Closest To Mouse
               # 2. Biggest Bounding Box
               # 3. Highest Confidence

triggerbot_key = 'n'
aimbot_key = 'x'
closeui_key = 'p'

MONITOR_SCALE = 4
ShowGUI = False

import numpy as np
lower_pink = np.array([100, 0, 110])
upper_pink = np.array([255, 100, 255])

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
from matplotlib import cm
import win32api, win32con, win32gui
import ctypes
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QLabel, QVBoxLayout, QWidget
from tkinter import *
from tkinter.filedialog import askopenfilename

MONITOR_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
MONITOR_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

print("Monitor resolution: " + str(MONITOR_WIDTH) +"x"+ str(MONITOR_HEIGHT))

Tk().withdraw()
ModelPath = askopenfilename(filetypes=[("Model File", "*.pt *.onnx *.engine")])

def cooldown(cooldown_bool,wait):
    time.sleep(wait)
    cooldown_bool[0] = True


region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
x,y,width,height = region
screenshot_centre = [int((width-x)/2),int((height-y)/2)]
emptynumpy = np.zeros((height, width, 4), dtype=np.uint8)
emptynumpy[:,:,3] = 0
camera = dxcam.create()
triggerbot = False
trigerbot_toggle = [True]
aim_assist = False
aim_assist_toggle = [True]
send_next = [True]


model = YOLO(ModelPath)
model.conf = ModelConfidence
model.max_det = MaxDetections
model.half = UseHalfFloat

start_time = time.time()
PussyHole = 1
counter = 1
fps = 0
TryTrig = [True]
    
def triggerboot():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,screenshot_centre[0],screenshot_centre[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,screenshot_centre[0],screenshot_centre[1],0,0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,screenshot_centre[0],screenshot_centre[1],0,0)    
    TryTrig[0] = True
    
def GUIRun():
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Cool Overlay")
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
            self.setAttribute(QtCore.Qt.WA_NoChildEventsForParent, True)
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            self.setFixedHeight(height)
            self.setFixedWidth(width)

            # Create a label to display the image
            self.label = QLabel(self)
            self.setCentralWidget(self.label)
            self.center()

            # Create a timer to periodically update the image
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_image)
            self.timer.start(10) # Update every 10ms

        def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
        
        def update_image(self):
            if annotation is not None:
                # Convert the new numpy array to a QImage
                new_qimage = QImage(annotation.data, annotation.shape[1], annotation.shape[0], annotation.strides[0], QImage.Format.Format_ARGB8565_Premultiplied)

                # Convert the QImage to a QPixmap
                new_qpixmap = QPixmap.fromImage(new_qimage)

                # Update the QPixmap in the QLabel
                self.label.setPixmap(new_qpixmap)

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = MainWindow()
        ex.show()
        sys.exit(app.exec_())
        
camera.start(region,target_fps=60)
while True:
    close_p_dist = 100000000
    close_p = -1
    screenshot = camera.get_latest_frame()
    if type(screenshot) == np.ndarray:
        screenshot = cv2.inRange(screenshot, lower_pink, upper_pink)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2BGR)
        df = model.predict(source=screenshot, verbose=False)
        annotation = df[0].plot(img=emptynumpy)
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
            if mouseMoveDelay is not 0:
                send_next[0] = False
                thread = threading.Thread(target=cooldown, args=(send_next,mouseMoveDelay,))
                thread.start()
            

    if ShowGUI == True:
        ShowGUI = False
        threading.Thread(target=GUIRun).start()
        # screen_fps = cv2.putText(
        #     img = annotation,
        #     text = str(fps),
        #     org = (8,13),
        #     fontFace = cv2.FONT_HERSHEY_PLAIN,
        #     fontScale = 1,
        #     color = (125, 246, 55),
        #     thickness = 1
        # )

        # screen_fps_trigger = cv2.putText(
        #     img = screen_fps,
        #     text = "TBot: " + str(triggerbot),
        #     org = (8,30),
        #     fontFace= cv2.FONT_HERSHEY_PLAIN,
        #     fontScale= 1,
        #     color= (125, 246, 55),
        #     thickness= 1
        # )

        # screen_fps_trigger_aim = cv2.putText(
        #     img = screen_fps_trigger,
        #     text = "AimBot: " + str(aim_assist),
        #     org = (8,45),
        #     fontFace= cv2.FONT_HERSHEY_PLAIN,
        #     fontScale= 1,
        #     color= (125, 246, 55),
        #     thickness= 1
        # )
        # try:
        #     cv2.imshow("frame",screen_fps_trigger_aim)
        # except:
        #     pass
        
        # if(cv2.waitKey(1) == ord(closeui_key)):
        #     cv2.destroyAllWindows()
        #     break
    
    def fpscount():
        global fps
        fps = fps
        global start_time, PussyHole, counter
        counter += 1
        if(time.time() - start_time) > PussyHole:
            fpsnum = int(counter/(time.time()-start_time))
            fps = "Fps: "+ str(int(counter/(time.time()-start_time)))
            if fpsnum > 700:
                print("Likely Idle")
            else:
                print(fps)
            counter = 0
            start_time = time.time()
    fpscount()
        