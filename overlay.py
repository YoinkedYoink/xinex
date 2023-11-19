import time
import math
import keyboard
import random
import threading
import sys
import win32api, win32con, win32gui
import ctypes
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QEvent
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
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