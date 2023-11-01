import numpy as np
from tkinter import Tk
from tkinter.filedialog import askdirectory
#CHANGE THESE IF YOU HAVE TO

video_folder = askdirectory(title='Input Video Folder')
image_export_folder = askdirectory(title='Output Image Folder')

MONITOR_WIDTH = 1920
MONITOR_HEIGHT = 1080

MONITOR_SCALE = 1 #how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions

percentFrames = 20

#no need to change anything under here
import cv2
import os

if __name__ == "__main__":

    os.chdir(image_export_folder)# changes directory to exports

    region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
    x,y,width,height = region
    print(region)
    images = 0
    for video_name in os.listdir(video_folder):
        vidcap = cv2.VideoCapture(video_folder+"\\"+video_name)#assigning current video
        success, image = vidcap.read()# reads in a frame
        count = 0
        frame = 0   
        while success:
            frame += 1
            success, image = vidcap.read()
            if (frame % percentFrames == 0):# only activates every 20 frames
                image = image[y:height,x:width]#crops image to scale cordinates
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    
                saturation = hsv[..., 1]

                saturation = cv2.add(saturation, 100)
                
                hsv[..., 1] = saturation
                
                image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB_FULL)
                
                cv2.imwrite(video_name+"frame%d.jpg" % count, image)     # save frame as JPG file
                success, image = vidcap.read()
                print('Read a new frame: ', success, " | ", count)
                count += 1
                images += 1

    print("Total images created: ", images)