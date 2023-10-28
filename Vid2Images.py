import numpy as np
#CHANGE THESE IF YOU HAVE TO

video_folder = r"C:\Users\Nord\Documents\ShareX\Screenshots\2023-10"
image_export_folder = r"C:\Users\Nord\Documents\code\ai-aim\images"

MONITOR_WIDTH = 1920
MONITOR_HEIGHT = 1080

MONITOR_SCALE = 1 #how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions

lower_pink = np.array([100, 0, 110]) #player outline colour lower and upper bounds
upper_pink = np.array([255, 100, 255])

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
                mask = cv2.inRange(image, lower_pink, upper_pink)
                
                cv2.imwrite(video_name+"frame%d.jpg" % count, mask)     # save frame as JPG file
                success, image = vidcap.read()
                print('Read a new frame: ', success, " | ", count)
                count += 1
                images += 1

    print("Total images created: ", images)