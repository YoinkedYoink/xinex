ModelConfidence = 0.7
MaxDetections = 5
UseHalfFloat = True

AimbotToggle = True
aimSpeed = 1
actRange = 150 #fov of aimbot
headshot = False
headshotSplit = 5 #e.g. 3 == 1/3 from the top of bounding box
aimPercision = 1
boxexpand = 0
minmove = 1
mouseMoveDelay = 0

AimMethod = 1  # 1. Closest To Mouse
               # 2. Biggest Bounding Box
               # 3. Highest Confidence

#triggerbot_key = 'n'
aimbot_key = 'x'
closeui_key = 'p'

MONITOR_SCALE = 3
target_fps = 45
ShowStats = True
FOVShow = True

import numpy as np
lower_pink = np.array([229, 0, 229]) # BGR
upper_pink = np.array([230, 0, 230]) # BGR 

print("\033c", end='')
print("Importing dependencies")
import dxcam
from ultralytics import YOLO
import cv2
import time
import math
import keyboard
import threading
import webbrowser
import sys
import win32api, win32con
import ctypes
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QMainWindow, QLabel, QPushButton, QSlider
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
emptynumpy = np.zeros((height, width, 4), dtype=np.uint8)
#emptynumpy[:,:,3] = 0
annotation = None

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
                    except:
                        pass
                
                # if keyboard.is_pressed(triggerbot_key):
                #     if trigerbot_toggle[0] == True:
                #         triggerbot = not triggerbot
                #         #print(triggerbot)
                #         trigerbot_toggle[0] = False
                #         thread = threading.Thread(target=cooldown, args=(trigerbot_toggle,0.3,))
                #         thread.start()

                if keyboard.is_pressed(aimbot_key):
                    if AimbotToggle == True:
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
                        if headshot == True:
                            if int(head_cent_list[1]) == int(ymin):
                                hitbuff = 1
                                #print("added buffer")
                            else:
                                hitbuff = 0
                            xdif = (head_cent_list[0] - screenshot_centre[0])
                            ydif = (head_cent_list[1]+hitbuff - screenshot_centre[1])
                        else:
                            xdif = (body_cent_list[0] - screenshot_centre[0])
                            ydif = (body_cent_list[1] - screenshot_centre[1])
                        if xdif not in range(-minmove,minmove) or ydif not in range(-minmove,minmove):
                            if screenshot_centre[0] in range(int(xmin-boxexpand),int(xmax+boxexpand)) and screenshot_centre[1] in range(int(ymin-boxexpand),int(ymax+boxexpand)):
                                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(xdif * aimPercision),int(ydif * aimPercision),0,0)
                            else:
                                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(xdif * aimSpeed),int(ydif * aimSpeed),0,0)
                        xdif=0
                        ydif=0
                        if mouseMoveDelay != 0:
                            send_next[0] = False
                            thread = threading.Thread(target=cooldown, args=(send_next,mouseMoveDelay,))
                            thread.start()
                            
                    if triggerbot == True and TryTrig[0] == True and headshot == True and screenshot_centre[0] in range(int((xmax-xmin)/3),int((xmax-xmin)/3)*2) and screenshot_centre[1] in range(int(ymin),int((ymax-ymin)/headshotSplit)):
                        TryTrig[0] = False
                        threading.Thread(target=triggerboot).start()
                     elif triggerbot == True and TryTrig[0] == True and headshot == False and screenshot_centre[0] in range(int(xmin),int(xmax)) and screenshot_centre[1] in range(int(ymin),int(ymax)):
                              print("hi")
                              #head == what is on top
                              #body == 3/5 in middle -1/2 bottom and hssplit top
                              #legs same as head but to bottom
                        
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
                            #print(fps)
                            pass
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
            
            ######  Base Settings Widget ########
            
            self.settingsWidget = QFrame(self)
            self.settingsWidget.setFrameShape(QFrame.StyledPanel)
            #self.settingsWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.settingsWidget.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
            self.settingsWidget.setWindowFlags(QtCore.Qt.FramelessWindowHint 
                                | QtCore.Qt.WindowStaysOnTopHint
                                #| QtCore.Qt.WindowDoesNotAcceptFocus
                                #| QtCore.Qt.WindowTransparentForInput
                                )
            self.settingsWidget.setGeometry(int(self.width()/2-400),int((self.height()/2-225)),800,450)
            self.settingsWidget.setStyleSheet("background-color: rgb(110, 0, 106); border-style: inset; border-width: 1px; border-radius: 10px; border-color: rgb(34, 0, 33)")
            self.settingsWidget.show()
            
            KeybindText = QLabel("Insert", self.settingsWidget)
            KeybindText.setFont(QFont("Arial", 10))
            KeybindText.setStyleSheet("border-width: 0px")
            KeybindText.move(4,2)
            

            XinexText = QLabel("XineX", self.settingsWidget)
            XinexText.setFont(QFont("Arial", 17))
            XinexText.setStyleSheet("border-width: 0px")
            XinexText.move(45,85)
            
            self.GamesButton = QPushButton("Games", self.settingsWidget)
            self.GamesButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            self.GamesButton.setGeometry(10,125,130,40)
            self.GamesButton.clicked.connect(lambda: self.menuswitcher("Games"))

            
            self.AimbotButton = QPushButton("Aimbot", self.settingsWidget)
            self.AimbotButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            self.AimbotButton.setGeometry(10,175,130,40)
            self.AimbotButton.clicked.connect(lambda: self.menuswitcher("Aimbot"))

            
            self.VisualsButton = QPushButton("Visuals", self.settingsWidget)
            self.VisualsButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            self.VisualsButton.setGeometry(10,225,130,40)
            self.VisualsButton.clicked.connect(lambda: self.menuswitcher("Visuals"))

            
            self.OtherButton = QPushButton("Other", self.settingsWidget)
            self.OtherButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            self.OtherButton.setGeometry(10,275,130,40)
            self.OtherButton.clicked.connect(lambda: self.menuswitcher("Other"))

            
            self.CreditsButton = QPushButton("Credits", self.settingsWidget)
            self.CreditsButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            self.CreditsButton.setGeometry(10,325,130,40)
            self.CreditsButton.clicked.connect(lambda: self.menuswitcher("Credits"))

            
            ExitButton = QPushButton("Exit", self.settingsWidget)
            ExitButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            ExitButton.setGeometry(10,400,130,40)
            ExitButton.clicked.connect(self.exitapp)

            ##########  Games Settings  ##########
            
            self.GamesSettings = QFrame(self.settingsWidget)
            self.GamesSettings.setGeometry(150,0,650,450)
            self.GamesSettings.setStyleSheet("background-color: rgb(100, 10, 95); border-width: 3px; border-color: rgb(105, 5, 102); border-style: solid")
            self.GamesSettings.hide()
            
            self.ArsenalGame1 = QPushButton("Arsenal", self.GamesSettings)
            self.ArsenalGame1.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.ArsenalGame1.setGeometry(40,40,120,140)
            
            self.CustomGame99 = QPushButton("Custom Model", self.GamesSettings)
            self.CustomGame99.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.CustomGame99.setGeometry(545,420,100,25)
            
            ConceptGameText = QLabel("!!Concept!!", self.GamesSettings)
            ConceptGameText.setFont(QFont("Arial",70))
            ConceptGameText.setStyleSheet("border-style: none")
            ConceptGameText.move(100,200)
            
            ########  Aimbot Settings  #########
            
            self.AimbotSettings = QFrame(self.settingsWidget)
            self.AimbotSettings.setGeometry(150,0,650,450)
            self.AimbotSettings.setStyleSheet("background-color: rgb(100, 10, 95); border-width: 3px; border-color: rgb(105, 5, 102); border-style: solid")
            self.AimbotSettings.show()
            
            AimSectionLabel = QLabel("---- Aimbot ----", self.AimbotSettings)
            AimSectionLabel.setFont(QFont("Arial",15))
            AimSectionLabel.setStyleSheet("border-style: none")
            AimSectionLabel.move(15,15)
            
            AimSectionKeybind = QLabel("Bind: X", self.AimbotSettings)
            AimSectionKeybind.setFont(QFont("Arial",10))
            AimSectionKeybind.setStyleSheet("border-style: none;background-color: rgb(105, 5, 102);")
            AimSectionKeybind.move(150,20)
            
            AimSpeedSlider = QSlider(QtCore.Qt.Horizontal, self.AimbotSettings)
            AimSpeedSlider.setGeometry(15,50,120,20)
            AimSpeedSlider.setStyleSheet("border-style: none")
            AimSpeedSlider.setRange(0,100)
            AimSpeedSlider.valueChanged.connect(self.aimsliderFunc)
            
            self.AimSpeedText = QLabel(str(aimSpeed)+"x Aim Speed", self.AimbotSettings)
            self.AimSpeedText.setFont(QFont("Arial",10))
            self.AimSpeedText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            self.AimSpeedText.move(150,50)
            
            AimPercissionSlider = QSlider(QtCore.Qt.Horizontal, self.AimbotSettings)
            AimPercissionSlider.setGeometry(15,100,120,20)
            AimPercissionSlider.setStyleSheet("border-style: none")
            AimPercissionSlider.setRange(0,100)
            AimPercissionSlider.valueChanged.connect(self.PercissionaimsliderFunc)
            
            self.AimPercissionText = QLabel(str(aimPercision)+"x Percission", self.AimbotSettings)
            self.AimPercissionText.setFont(QFont("Arial",10))
            self.AimPercissionText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            self.AimPercissionText.move(150, 100)
            
            BoxExpanderSlider = QSlider(QtCore.Qt.Horizontal, self.AimbotSettings)
            BoxExpanderSlider.setGeometry(15,150,120,20)
            BoxExpanderSlider.setStyleSheet("border-style: none")
            BoxExpanderSlider.setRange(0,20)
            BoxExpanderSlider.valueChanged.connect(self.BoxExpandFunc)
            
            self.BoxExpanderText = QLabel(str(boxexpand)+"px Box Expand", self.AimbotSettings)
            self.BoxExpanderText.setFont(QFont("Arial",10))
            self.BoxExpanderText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            self.BoxExpanderText.move(150,150)
            
            MinMoveSlider = QSlider(QtCore.Qt.Horizontal, self.AimbotSettings)
            MinMoveSlider.setGeometry(15,200,120,20)
            MinMoveSlider.setStyleSheet("border-style: none")
            MinMoveSlider.setRange(0,10)
            MinMoveSlider.valueChanged.connect(self.MinMoveFunc)
            
            self.MinMoveText = QLabel(str(minmove)+"px Min Move", self.AimbotSettings)
            self.MinMoveText.setFont(QFont("Arial", 10))
            self.MinMoveText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            self.MinMoveText.move(150,200)
            
            self.HeadshotButton = QPushButton("Headshot: "+str(headshot), self.AimbotSettings)
            self.HeadshotButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.HeadshotButton.setGeometry(15,225,120,35)
            self.HeadshotButton.clicked.connect(self.HeadShotButtonFunc)
            
            self.AimbotMethodButton = QPushButton("Method: Closest", self.AimbotSettings)
            self.AimbotMethodButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.AimbotMethodButton.setGeometry(140,225,120,35)
            
            TriggerbotSectionText = QLabel("---- Triggerbot ----", self.AimbotSettings)
            TriggerbotSectionText.setFont(QFont("Arial",15))
            TriggerbotSectionText.setStyleSheet("border-style: none")
            TriggerbotSectionText.move(15,275)
            
            TriggerbotSectionKeybind = QLabel("Bind: None", self.AimbotSettings)
            TriggerbotSectionKeybind.setFont(QFont("Arial",10))
            TriggerbotSectionKeybind.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            TriggerbotSectionKeybind.move(180,280)
            
            TriggerbotConceptText = QLabel("!!Concept!!", self.AimbotSettings)
            TriggerbotConceptText.setFont(QFont("Arial", 30))
            TriggerbotConceptText.setStyleSheet("border-style: none")
            TriggerbotConceptText.move(15,325)
            
            SettingsSectionText = QLabel("---- Settings ----", self.AimbotSettings)
            SettingsSectionText.setFont(QFont("Arial", 15))
            SettingsSectionText.setStyleSheet("border-style: none")
            SettingsSectionText.move(470,15)
            
            self.AimOnOffButton = QPushButton("Aimbot "+str(AimbotToggle), self.AimbotSettings)
            self.AimOnOffButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.AimOnOffButton.setGeometry(480,45,120,35)
            self.AimOnOffButton.clicked.connect(self.AimbotButtonFunc)
            
            self.TriggerOnOffButton = QPushButton("Trigger "+str(triggerbot), self.AimbotSettings)
            self.TriggerOnOffButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.TriggerOnOffButton.setGeometry(480,95,120,35)
            self.TriggerOnOffButton.clicked.connect(self.TriggerButtonFunc)
            
            self.FOVSizeText = QLabel(str(actRange)+"px FOV", self.AimbotSettings)
            self.FOVSizeText.setFont(QFont("Arial",10))
            self.FOVSizeText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            self.FOVSizeText.move(508,140)
            
            FOVSizeSlider = QSlider(QtCore.Qt.Horizontal, self.AimbotSettings)
            FOVSizeSlider.setGeometry(480,160,120,20)
            FOVSizeSlider.setStyleSheet("border-style: none")
            FOVSizeSlider.setRange(1,1000)
            FOVSizeSlider.valueChanged.connect(self.FovChangeFunc)
            
            
            #####  Visuals Settings  ######
            
            self.VisualsSettings = QFrame(self.settingsWidget)
            self.VisualsSettings.setGeometry(150,0,650,450)
            self.VisualsSettings.setStyleSheet("background-color: rgb(100, 10, 95); border-width: 3px; border-color: rgb(105, 5, 102); border-style: solid")
            self.VisualsSettings.hide()
            
            ESPSectionLabel = QLabel("---- ESP ----", self.VisualsSettings)
            ESPSectionLabel.setFont(QFont("Arial", 15))
            ESPSectionLabel.setStyleSheet("border-style: none")
            ESPSectionLabel.move(15,15)
            
            ESPConceptLabel = QLabel("!!Concept!!", self.VisualsSettings)
            ESPConceptLabel.setFont(QFont("Arial",30))
            ESPConceptLabel.setStyleSheet("border-style: none")
            ESPConceptLabel.move(15,40)
            
            OtherSectionLabel = QLabel("---- Other ----", self.VisualsSettings)
            OtherSectionLabel.setFont(QFont("Arial",15))
            OtherSectionLabel.setStyleSheet("border-style: none")
            OtherSectionLabel.move(510,15)
            
            self.FOVOnOffButton = QPushButton("FOV "+str(FOVShow), self.VisualsSettings)
            self.FOVOnOffButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.FOVOnOffButton.setGeometry(510,50,120,35)
            self.FOVOnOffButton.clicked.connect(self.HideFOV)
            
            self.StatsOnOffButton = QPushButton("Stats "+str(ShowStats), self.VisualsSettings)
            self.StatsOnOffButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.StatsOnOffButton.setGeometry(510,100,120,35)
            self.StatsOnOffButton.clicked.connect(self.HideStats)
            
            
            #####  Other Settings  ######
            
            self.OtherSettings = QFrame(self.settingsWidget)
            self.OtherSettings.setGeometry(150,0,650,450)
            self.OtherSettings.setStyleSheet("background-color: rgb(100, 10, 95); border-width: 3px; border-color: rgb(105, 5, 102); border-style: solid")
            self.OtherSettings.hide()
            
            Welp = QLabel("don't really know what to put here", self.OtherSettings)
            Welp.setStyleSheet("border-style: none")
            Welp.setFont(QFont("Arial",30))
            Welp.move(15,15)
            
            self.ConfigSaveButton = QPushButton("Save Config (Placeholder)", self.OtherSettings)
            self.ConfigSaveButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.ConfigSaveButton.setGeometry(15,100,120,35)
            
            self.ConfigLoadButton = QPushButton("Load Config (Placeholder)", self.OtherSettings)
            self.ConfigLoadButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.ConfigLoadButton.setGeometry(15,150,120,35)
            
            #####  Credits Page  #####
            
            self.CreditsPage = QFrame(self.settingsWidget)
            self.CreditsPage.setGeometry(150,0,650,450)
            self.CreditsPage.setStyleSheet("background-color: rgb(100, 10, 95); border-width: 3px; border-color: rgb(105, 5, 102); border-style: solid")
            self.CreditsPage.hide()
            
            self.GithubButton = QPushButton("Github", self.CreditsPage)
            self.GithubButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.GithubButton.setGeometry(40,30,120,35)
            self.GithubButton.clicked.connect(lambda: self.weblinks("github"))
            
            self.DiscordButton = QPushButton("Discord Server", self.CreditsPage)
            self.DiscordButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.DiscordButton.setGeometry(270,30,120,35)
            self.DiscordButton.clicked.connect(lambda: self.weblinks("discord"))
            
            self.YoutubeButton = QPushButton("Youtube", self.CreditsPage)
            self.YoutubeButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            self.YoutubeButton.setGeometry(490,30,120,35)
            self.YoutubeButton.clicked.connect(lambda: self.weblinks("youtube"))
            
            ThankYouText = QLabel("          Thank You for using this script!\n     If you find issues or have suggestions\nPlease add me on discord or submit a github issue", self.CreditsPage)
            ThankYouText.setStyleSheet("border-style: none")
            ThankYouText.setFont(QFont("Arial",15))
            ThankYouText.move(130,200)
            
            #########################################################################
            #########################################################################
            #########################################################################
                        
            
            
            self.stats = QLabel(self)
            #label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            self.stats.setText("oop")
            self.stats.move(int(self.width()/15),int(self.height()/15))
            self.stats.resize(70,50)
            self.stats.setStyleSheet('background-color: rgba(255,255,255,60);border: 1px solid rgba(255,0,0,90)')
            self.stats.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_stats)
            self.timer.start(10)
            
            keyboard.add_hotkey('insert', lambda: self.menuswitcher("hotkey"))
                        
        def update_stats(self):
            if ShowStats:
                self.stats.setVisible(True)
                self.stats.setText("fps: "+ str(fps) + "\naim: "+ str(aim_assist) +"\nhit: " + str(triggerbot))
            else:
                self.stats.setVisible(False)
            
        def menuswitcher(self, menu):
            if menu == "hotkey":
                if self.settingsWidget.isVisible():
                    self.settingsWidget.hide()
                else:
                    self.settingsWidget.show()
            else:
                self.GamesSettings.hide()
                self.GamesButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
                self.AimbotSettings.hide()
                self.AimbotButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
                self.VisualsSettings.hide()
                self.VisualsButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
                self.OtherSettings.hide()
                self.OtherButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
                self.CreditsPage.hide()
                self.CreditsButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
                if menu == "Games":
                    self.GamesSettings.show()
                    self.GamesButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(60, 200, 30)")
                if menu == "Aimbot":
                    self.AimbotSettings.show()
                    self.AimbotButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(60, 200, 30)")
                if menu == "Visuals":
                    self.VisualsSettings.show()
                    self.VisualsButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(60, 200, 30)")
                if menu == "Other":
                    self.OtherSettings.show()
                    self.OtherButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(60, 200, 30)")
                if menu == "Credits":
                    self.CreditsPage.show()
                    self.CreditsButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(60, 200, 30)")
                
            
        def TriggerButtonFunc(self):
            global triggerbot
            triggerbot = not triggerbot
            self.TriggerOnOffButton.setText("Trigger "+str(triggerbot))
            
        def AimbotButtonFunc(self):
            global AimbotToggle
            AimbotToggle = not AimbotToggle
            self.AimOnOffButton.setText("Aimbot "+str(AimbotToggle))
            
        def HeadShotButtonFunc(self):
            global headshot
            headshot = not headshot
            self.HeadshotButton.setText("Headshot: "+str(headshot))
            
        def aimsliderFunc(self, val):
            global aimSpeed
            aimSpeed = val/100
            self.AimSpeedText.setText(str(aimSpeed)+" Aim Speed")
            
        def PercissionaimsliderFunc(self, val):
            global aimPercision
            aimPercision = val/100
            self.AimPercissionText.setText(str(aimPercision)+"x Percission")
            
        def BoxExpandFunc(self,val):
            global boxexpand
            boxexpand = val
            self.BoxExpanderText.setText(str(boxexpand)+"px Box Expand")
            
        def MinMoveFunc(self, val):
            global minmove
            minmove = val
            self.MinMoveText.setText(str(minmove)+"px Min Move")
            
        def FovChangeFunc(self, val):
            global actRange
            actRange = val
            self.FOVSizeText.setText(str(actRange)+"px FOV")
            self.update()
            
        def HideFOV(self):
            global FOVShow
            FOVShow = not FOVShow
            self.FOVOnOffButton.setText("FOV "+str(FOVShow))
            self.update()
            
        def HideStats(self):
            global ShowStats
            ShowStats = not ShowStats
            self.StatsOnOffButton.setText("Stats "+str(ShowStats))
            
        def weblinks(self,link):
            if link == "github":
                webbrowser.open_new_tab("https://github.com/YoinkedYoink")
            if link == "discord":
                webbrowser.open_new_tab("https://discord.gg/jMyVTHzNn2")
            if link == "youtube":
                webbrowser.open_new_tab("https://www.youtube.com/channel/UC_nLZkt28dGri1h5LGGMsQw")
        
        def paintEvent(self, event):
            if FOVShow:
                painter = QPainter(self)
                painter.setPen(QPen(QtCore.Qt.black,1,QtCore.Qt.DashLine))
                painter.drawEllipse(int((MONITOR_WIDTH/2)-actRange),int((MONITOR_HEIGHT/2)-actRange),actRange*2,actRange*2)
            self.settingsWidget.raise_()
           
        
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = MainWindow()
        t = threading.Thread(target=MainWindow.actualclusterfuck, daemon=True)
        t.start()
        ex.show()
        sys.exit(app.exec_())
        
GUIRun()
