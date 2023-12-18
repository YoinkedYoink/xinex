import time
import math
import keyboard
import random
import threading
import sys
import win32api, win32con, win32gui
import ctypes
from PyQt5.QtGui import QImage, QPixmap, QColor, QFont
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QEvent
from PyQt5.QtWidgets import QApplication, QGraphicsRectItem, QSlider, QFrame, QDesktopWidget, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
def GUIRun():
    class MainWindow(QMainWindow):
        def exitapp(self):
            print("bye bye")
            sys.exit()
        
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Cool Overlay")
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            #self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
            self.setAttribute(QtCore.Qt.WA_NoChildEventsForParent, True)
            self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint 
                                | QtCore.Qt.WindowStaysOnTopHint
                                | QtCore.Qt.WindowDoesNotAcceptFocus
                                #| QtCore.Qt.WindowTransparentForInput
                                )
            self.setFixedHeight(1080)
            self.setFixedWidth(1920)
            
            ######  Base Settings Widget ########
            
            self.settingsWidget = QFrame(self)
            self.settingsWidget.setFrameShape(QFrame.StyledPanel)
            #self.settingsWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.settingsWidget.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
            self.settingsWidget.setWindowFlags(QtCore.Qt.FramelessWindowHint 
                                | QtCore.Qt.WindowStaysOnTopHint
                                | QtCore.Qt.WindowDoesNotAcceptFocus
                                #| QtCore.Qt.WindowTransparentForInput
                                )
            self.settingsWidget.setGeometry(int(self.width()/2-400),int((self.height()/2-225)),800,450)
            self.settingsWidget.setStyleSheet("background-color: rgb(110, 0, 106); border-style: inset; border-width: 1px; border-radius: 10px; border-color: rgb(34, 0, 33)")
            
            KeybindText = QLabel("Alt + M", self.settingsWidget)
            KeybindText.setFont(QFont("Arial", 10))
            KeybindText.setStyleSheet("border-width: 0px")
            KeybindText.move(4,2)
            

            XinexText = QLabel("XineX", self.settingsWidget)
            XinexText.setFont(QFont("Arial", 17))
            XinexText.setStyleSheet("border-width: 0px")
            XinexText.move(45,85)
            
            GamesButton = QPushButton("Games", self.settingsWidget)
            GamesButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            GamesButton.setGeometry(10,125,130,40)

            
            AimbotButton = QPushButton("Aimbot", self.settingsWidget)
            AimbotButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            AimbotButton.setGeometry(10,175,130,40)

            
            VisualsButton = QPushButton("Visuals", self.settingsWidget)
            VisualsButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            VisualsButton.setGeometry(10,225,130,40)

            
            OtherButton = QPushButton("Other", self.settingsWidget)
            OtherButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            OtherButton.setGeometry(10,275,130,40)

            
            CreditsButton = QPushButton("Credits", self.settingsWidget)
            CreditsButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            CreditsButton.setGeometry(10,325,130,40)

            
            ExitButton = QPushButton("Exit", self.settingsWidget)
            ExitButton.setStyleSheet("background-color: rgb(116, 0, 113); border-style: inset; border-width: 2px; border-radius: 5px; border-color: rgb(93, 0, 90)")
            ExitButton.setGeometry(10,400,130,40)

            ##########  Games Settings  ##########
            
            self.GamesSettings = QFrame(self.settingsWidget)
            self.GamesSettings.setGeometry(150,0,650,450)
            self.GamesSettings.setStyleSheet("background-color: rgb(100, 10, 95); border-width: 3px; border-color: rgb(105, 5, 102); border-style: solid")
            self.GamesSettings.hide()
            
            ArsenalGame1 = QPushButton("Arsenal", self.GamesSettings)
            ArsenalGame1.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            ArsenalGame1.setGeometry(40,40,120,140)
            
            CustomGame99 = QPushButton("Custom Model", self.GamesSettings)
            CustomGame99.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            CustomGame99.setGeometry(545,420,100,25)
            
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
            
            AimSpeedText = QLabel("0.5x Aim Speed", self.AimbotSettings)
            AimSpeedText.setFont(QFont("Arial",10))
            AimSpeedText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            AimSpeedText.move(150,50)
            
            AimPercissionSlider = QSlider(QtCore.Qt.Horizontal, self.AimbotSettings)
            AimPercissionSlider.setGeometry(15,100,120,20)
            AimPercissionSlider.setStyleSheet("border-style: none")
            AimPercissionSlider.setRange(0,100)
            
            AimPercissionText = QLabel("0.5x Percission", self.AimbotSettings)
            AimPercissionText.setFont(QFont("Arial",10))
            AimPercissionText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            AimPercissionText.move(150, 100)
            
            BoxExpanderSlider = QSlider(QtCore.Qt.Horizontal, self.AimbotSettings)
            BoxExpanderSlider.setGeometry(15,150,120,20)
            BoxExpanderSlider.setStyleSheet("border-style: none")
            BoxExpanderSlider.setRange(0,20)
            
            BoxExpanderText = QLabel("5px Box Expand", self.AimbotSettings)
            BoxExpanderText.setFont(QFont("Arial",10))
            BoxExpanderText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            BoxExpanderText.move(150,150)
            
            MinMoveSlider = QSlider(QtCore.Qt.Horizontal, self.AimbotSettings)
            MinMoveSlider.setGeometry(15,200,120,20)
            MinMoveSlider.setStyleSheet("border-style: none")
            MinMoveSlider.setRange(0,10)
            
            MinMoveText = QLabel("0px Min Move", self.AimbotSettings)
            MinMoveText.setFont(QFont("Arial", 10))
            MinMoveText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            MinMoveText.move(150,200)
            
            HeadshotButton = QPushButton("Headshot: True", self.AimbotSettings)
            HeadshotButton.setText("Headshot: False")
            HeadshotButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            HeadshotButton.setGeometry(15,225,120,35)
            
            AimbotMethodButton = QPushButton("Method: Closest", self.AimbotSettings)
            AimbotMethodButton.setText("Method: Confidence")
            AimbotMethodButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            AimbotMethodButton.setGeometry(140,225,120,35)
            
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
            
            AimOnOffButton = QPushButton("Aimbot ON", self.AimbotSettings)
            AimOnOffButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            AimOnOffButton.setGeometry(480,45,120,35)
            
            TriggerOnOffButton = QPushButton("Trigger ON", self.AimbotSettings)
            TriggerOnOffButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            TriggerOnOffButton.setGeometry(480,95,120,35)
            
            FOVSizeText = QLabel("243px FOV", self.AimbotSettings)
            FOVSizeText.setFont(QFont("Arial",10))
            FOVSizeText.setStyleSheet("background-color: rgb(105, 5, 102); border-style: none")
            FOVSizeText.move(508,140)
            
            FOVSizeSlider = QSlider(QtCore.Qt.Horizontal, self.AimbotSettings)
            FOVSizeSlider.setGeometry(480,160,120,20)
            FOVSizeSlider.setStyleSheet("border-style: none")
            FOVSizeSlider.setRange(1,1000)
            
            
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
            
            FOVOnOffButton = QPushButton("FOV Hidden", self.VisualsSettings)
            FOVOnOffButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            FOVOnOffButton.setGeometry(510,50,120,35)
            
            StatsOnOffButton = QPushButton("Stats Hidden", self.VisualsSettings)
            StatsOnOffButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            StatsOnOffButton.setGeometry(510,100,120,35)
            
            
            #####  Other Settings  ######
            
            self.OtherSettings = QFrame(self.settingsWidget)
            self.OtherSettings.setGeometry(150,0,650,450)
            self.OtherSettings.setStyleSheet("background-color: rgb(100, 10, 95); border-width: 3px; border-color: rgb(105, 5, 102); border-style: solid")
            self.OtherSettings.hide()
            
            Welp = QLabel("don't really know what to put here", self.OtherSettings)
            Welp.setStyleSheet("border-style: none")
            Welp.setFont(QFont("Arial",30))
            Welp.move(15,15)
            
            ConfigSaveButton = QPushButton("Save Config (Placeholder)", self.OtherSettings)
            ConfigSaveButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            ConfigSaveButton.setGeometry(15,100,120,35)
            
            ConfigLoadButton = QPushButton("Load Config (Placeholder)", self.OtherSettings)
            ConfigLoadButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            ConfigLoadButton.setGeometry(15,150,120,35)
            
            #####  Credits Page  #####
            
            self.CreditsPage = QFrame(self.settingsWidget)
            self.CreditsPage.setGeometry(150,0,650,450)
            self.CreditsPage.setStyleSheet("background-color: rgb(100, 10, 95); border-width: 3px; border-color: rgb(105, 5, 102); border-style: solid")
            self.CreditsPage.hide()
            
            GithubButton = QPushButton("Github", self.CreditsPage)
            GithubButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            GithubButton.setGeometry(40,30,120,35)
            
            DiscordButton = QPushButton("Discord Server", self.CreditsPage)
            DiscordButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            DiscordButton.setGeometry(270,30,120,35)
            
            YoutubeButton = QPushButton("Youtube", self.CreditsPage)
            YoutubeButton.setStyleSheet("background-color: rgb(120,30,115);border-style: outset; border-width: 3px; border-radius: 10px; border-color: rgb(39, 0, 54)")
            YoutubeButton.setGeometry(490,30,120,35)
            
            ThankYouText = QLabel("          Thank You for using this script!\n     If you find issues or have suggestions\nPlease add me on discord or submit a github issue", self.CreditsPage)
            ThankYouText.setStyleSheet("border-style: none")
            ThankYouText.setFont(QFont("Arial",15))
            ThankYouText.move(130,200)


            
            
            
            
            
            exit = QPushButton('Exit', self)
            exit.move(int(self.width()*0.9),int(self.height()*0.9))
            exit.clicked.connect(self.exitapp)
            
            self.placehold = QPushButton("CLICK", self)
            self.placehold.move(int(self.width()*0.5),int(self.height()*0.5))
            self.placehold.clicked.connect(self.placeclick)
            self.placehold.hide()
            
            self.settbutt = QPushButton('Settings', self)
            self.settbutt.move(int(self.width()*0.8),int(self.height()*0.9))
            self.settbutt.clicked.connect(self.opensett)
            
            self.stats = QLabel(self)
            #label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            self.stats.setText("oop")
            self.stats.move(int(self.width()/10),int(self.height()/10))
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_ui)
            self.timer.start(10)
            
        def update_ui(self):
            self.stats.setText("fps: 59.028434237\ndets: 3\nconf: 32.6")
            
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
        
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = MainWindow()
        ex.show()
        sys.exit(app.exec_())

GUIRun()