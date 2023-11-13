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
time.sleep(3)
while True:
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(5000),int(0),0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(-5000),int(0),0,0)
    if keyboard.is_pressed("p"):
        break
# def GUIRun():
#     class MainWindow(QMainWindow):
#         def __init__(self):
#             super().__init__()
#             self.setWindowTitle("Cool Overlay")
#             #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#             #self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
#             #self.setAttribute(QtCore.Qt.WA_NoChildEventsForParent, True)
#             #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
#             self.setFixedHeight(300)
#             self.setFixedWidth(300)

#             # Create a label to display the image
#             self.label = QLabel(self)
#             self.setCentralWidget(self.label)
#             self.center()

#         def center(self):
#             qr = self.frameGeometry()
#             cp = QDesktopWidget().availableGeometry().center()
#             qr.moveCenter(cp)
#             self.move(qr.topLeft())

#     if __name__ == '__main__':
#         app = QApplication(sys.argv)
#         ex = MainWindow()
#         ex.show()
#         sys.exit(app.exec_())
        
# GUIRun()