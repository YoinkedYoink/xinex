import cv2
import matplotlib.pyplot as plt
import d3dshot
import time
import numpy

d = d3dshot.create(capture_output="numpy")
img = d.screenshot()
img = img[:, :, ::-1].copy()
# img = cv2.imread(file)

B,G,R = cv2.split(img)

_, thresh = cv2.threshold(R, 180, 255, cv2.ADAPTIVE_THRESH_MEAN_C)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

R = cv2.applyColorMap(R, cv2.COLORMAP_HOT)

cv2.drawContours(R, contours, -1, (0, 255, 0), 3)


cv2.imshow("image", R)



# #import cv2
# import os
# import time

# time.sleep(0.5)

# os.system('cls')

# print("|| Input pictures directory (Default Pictures/) ||\n|>| ", end="", flush=True)
# inpath = input()

# if inpath == "":
#     print("|| Using default directory ||")
#     inpath = "Picures/"
# elif os.path.exists(inpath):
#     print("|| Found directory ||")
# else:
#     print("|| Invalid directory? ||")
#     _ = input()
#     quit()

# time.sleep(1)
# os.system('cls')

# print("|| Output pictures directory (Default ProPictures/) ||\n|>| ", end="", flush=True)
# outpath = input()

# if outpath == "":
#     print("|| Using default directory ||")
#     outpath = "ProPicures/"
# elif os.path.exists(outpath):
#     print("|| Found directory ||")
# else:
#     print("|| Invalid directory? ||")
#     _ = input()
#     quit()

# time.sleep(1)

# print("|S| Output Size |S|\n|1| Origional\n|2| 960x540\n|3| 640x360\n|4|")
