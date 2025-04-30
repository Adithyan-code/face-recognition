import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import os

name = 'abhishek'  # Replace with your name
dataset_path = f'dataset/{name}'
os.makedirs(dataset_path, exist_ok=True)

cam = PiCamera()
cam.resolution = (512, 304)
cam.framerate = 10
rawCapture = PiRGBArray(cam, size=(512, 304))

img_counter = 0

print("Press SPACE to capture images. Press ESC to exit.")

for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv2.imshow("Press SPACE to take a photo", image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    if key == 27:  # ESC pressed
        print("Escape hit, closing...")
        break
    elif key == 32:  # SPACE pressed
        img_name = f"{dataset_path}/image_{img_counter}.jpg"
        cv2.imwrite(img_name, image)
        print(f"{img_name} written!")
        img_counter += 1

cv2.destroyAllWindows()
