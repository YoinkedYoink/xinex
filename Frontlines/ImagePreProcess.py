# Import necessary libraries
import numpy as np
import cv2
import os

for picture in os.listdir('C:\\Users\\Nord\\Documents\\code\\ai-aim\\Frontlines\\test-raw\\'):
    image = cv2.imread('C:\\Users\\Nord\\Documents\\code\\ai-aim\\Frontlines\\test-raw\\'+picture)
    
    height, width, _ = image.shape
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    
    saturation = hsv[..., 1]

    saturation = cv2.add(saturation, 100)
    
    hsv[..., 1] = saturation
    
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB_FULL)
    
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# # Load image
# image = cv2.imread(r"Example-Images\uXcbt9Y321.jpg")

# # Get height and width of the image
# height, width, _ = image.shape

# # Define the pink color range
# lower_pink = np.array([100, 30, 130])
# upper_pink = np.array([255, 90, 190])
# # 153 57 121
# # 151 69 167
# # Create a mask for the pink color range
# mask = cv2.inRange(image, lower_pink, upper_pink)

# # Invert the mask to select all colors except pink
# mask_inv = cv2.bitwise_not(mask)

# # Convert the selected colors to grayscale
# gray_image = cv2.cvtColor(cv2.bitwise_and(image, image, mask=mask_inv), cv2.COLOR_BGR2GRAY)

# # Overlay the grayscale image over the mask
# overlayed_image = cv2.addWeighted(gray_image, 0.5, mask, 0.5, 0)

# # Display the modified image
# cv2.imshow('Modified Image', mask)
# cv2.waitKey(0)
# cv2.destroyAllWindows()