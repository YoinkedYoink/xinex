#mouseInputPath = "/dev/input/event2" #!!!CHANGE THIS PLEASE!!!
#https://python-evdev.readthedocs.io/en/latest/tutorial.html#listing-accessible-event-devices

ModelConfidence = 0.1
MaxDetections = 5
UseHalfFloat = False

aimSpeed = 0.6 # When not looking in bounding box
aimPercision = 1 # When looking at enemy bounding box

actRange = 900 # "FOV" but there is no circle yet
headshot = True # You don't need an explination

boxexpand = 0 # px to expand bounding box
minmove = 1 # minimum px to move mouse
mousemovedelay = 0.007 # this is in seconds!!!

AimMethod = 1  # 1. Closest To Mouse # ALL DOESN'T WORK YET
               # 2. Biggest Bounding Box
               # 3. Highest Confidence

triggerbot_key = 'n' # DOESN'T WORK YET
closeui_key = 'p' # only if ShowGUI == True
ShowGUI = False

MONITOR_WIDTH = 1920
MONITOR_HEIGHT = 1080
MONITOR_SCALE = 4



import numpy as np
lower_pink = np.array([200, 0, 200]) # BGR
upper_pink = np.array([201, 0, 201]) # BGR 

import mss
from ultralytics import YOLO
#from PIL import Image, ImageTk
import cv2
import evdev
import time
import math
import threading
from tkinter import *
from tkinter.filedialog import askopenfilename


devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
num = 0
for device in devices:
    print(num, device.name)
    num += 1
num = input("\nChoose a device: ")
mouseInputPath = devices[int(num)].path


mouse = evdev.InputDevice(mouseInputPath)
dummy = evdev.UInput.from_device(mouse)


print("\033c", end='')

print("In 3 seconds press a mouse key to bind to...")
print("!!!Do not move your mouse!!!") # I think it should reject mouse movements?
time.sleep(3)
print("Press your desired bind")

while True:
    if str(mouse.active_keys()) != "[]":
        aimbot_key = str(mouse.active_keys()).replace("[", "").replace("]", "")
        print("Found Key: " + aimbot_key)
        break
    time.sleep(0.1)


Tk().withdraw()
ModelPath = askopenfilename(filetypes=[("Model File", "*.pt")])


def cooldown(cooldown_bool,wait):
    time.sleep(wait)
    cooldown_bool[0] = True


region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
x,y,width,height = region
screenshot_centre = [int((width-x)/2),int((height-y)/2)]
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

class eventX:
    type = 2
    code = 0
    value = 0

class eventY:
    type = 2
    code = 1
    value = 0

class eventSync:
    type = 0
    code = 0
    value = 0


with mss.mss() as sct:
    while True:
        close_p_dist = 100000000
        close_p = -1
        screenshot = np.array(sct.grab({"top": math.ceil(y), "left": math.ceil(x), "width": width, "height": height}))
        if int(aimbot_key) in mouse.active_keys():
            aim_assist = True

            if type(screenshot) == np.ndarray:
                screenshot = cv2.inRange(screenshot[:,:,:-1], lower_pink, upper_pink)
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2BGR)
                df = model(source=screenshot, verbose=False)
                annotation = df[0].plot()
                boxes = df[0].boxes


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

                    if ShowGUI:
                        cv2.rectangle(screenshot,(xmin,ymin),(xmax,ymax),(0,0,255),3)
                
                except:
                    print("",end="")
        else:
            aim_assist = False

        # if keyboard.is_pressed(triggerbot_key):
        #     if trigerbot_toggle[0] == True:
        #         triggerbot = not triggerbot
        #         print(triggerbot)
        #         trigerbot_toggle[0] = False
        #         thread = threading.Thread(target=cooldown, args=(trigerbot_toggle,0.3,))
        #         thread.start()
                

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
            head_cent_list = [(xmax+xmin)/2,((ymax - ymin)/5)+ymin]
            if triggerbot == True and screenshot_centre[0] in range(int(xmin),int(xmax)) and screenshot_centre[1] in range(int(ymin),int(ymax)):
                print("lol")
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
                        eventX.value = math.floor(xdif*aimPercision)
                        eventY.value = math.floor(ydif*aimPercision)
                        dummy.write_event(eventX)
                        dummy.write_event(eventSync)
                        dummy.write_event(eventY)
                        dummy.write_event(eventSync)
                    else:
                        eventX.value = math.floor(xdif*aimSpeed)
                        eventY.value = math.floor(ydif*aimSpeed)
                        dummy.write_event(eventX)
                        dummy.write_event(eventSync)
                        dummy.write_event(eventY)
                        dummy.write_event(eventSync)


                send_next[0] = False
                thread = threading.Thread(target=cooldown, args=(send_next,mousemovedelay,))
                thread.start()

        if ShowGUI == True:
            screen_fps = cv2.putText(
                img = annotation,
                text = str(fps),
                org = (8,13),
                fontFace = cv2.FONT_HERSHEY_PLAIN,
                fontScale = 1,
                color = (125, 246, 55),
                thickness = 1
            )

            screen_fps_trigger = cv2.putText(
                img = screen_fps,
                text = "TBot: " + str(triggerbot),
                org = (8,30),
                fontFace= cv2.FONT_HERSHEY_PLAIN,
                fontScale= 1,
                color= (125, 246, 55),
                thickness= 1
            )

            screen_fps_trigger_aim = cv2.putText(
                img = screen_fps_trigger,
                text = "AimBot: " + str(aim_assist),
                org = (8,45),
                fontFace= cv2.FONT_HERSHEY_PLAIN,
                fontScale= 1,
                color= (125, 246, 55),
                thickness= 1
            )
            try:
                cv2.imshow("frame",screen_fps_trigger_aim)
            except:
                pass
            
            if(cv2.waitKey(1) == ord(closeui_key)):
                cv2.destroyAllWindows()
                break
        
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
        
