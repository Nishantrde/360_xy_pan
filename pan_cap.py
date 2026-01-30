
import numpy as np
import cv2

# Capture images from the camera
images = []
num_images = 5  # Number of images to capture for stitching
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

print(f"Capturing {num_images} images. Press SPACE to capture each image.")
for i in range(num_images):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        cv2.imshow('Camera', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # SPACE key
            images.append(frame.copy())
            print(f"Captured image {i+1}")
            break
        elif key == 27:  # ESC to exit
            print("Exiting capture early.")
            cap.release()
            cv2.destroyAllWindows()
            exit()
cv2.destroyAllWindows()
cap.release()

imageStitcher = cv2.Stitcher_create()

error, stitched_img = imageStitcher.stitch(images)

if not error:
    cv2.imwrite("stitched_img.png", stitched_img)
    cv2.imshow("stitched op", stitched_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error during stitching:", error)