import numpy as np
import cv2 
import glob
import imutils

image_path = glob.glob("imgs/*.jpeg")
images = []

for image in image_path:
    img = cv2.imread(image)
    images.append(img)
    # cv2.imshow("Image", img)
    cv2.waitKey(0)

imageStitcher = cv2.Stitcher_create()

error, stitched_img = imageStitcher.stitch(images)

if not error:

    cv2.imwrite("stiched_img.png", stitched_img)
    cv2.imshow("stitched op", stitched_img)
    cv2.waitKey(0)








