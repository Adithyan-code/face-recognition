from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import urllib.request
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import smbus2  # For I2C communication
import I2C_LCD_driver  # Library for I2C LCD

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, False)

# Initialize I2C LCD
lcd = I2C_LCD_driver.lcd()
GPIO.output(16, True)
lcd.lcd_display_string("Face Recognize", 1)
lcd.lcd_display_string("Attendance", 2)
sleep(1)
GPIO.output(16, False)

currentname = "unknown"
WRITEKEY = "Z0D9CUKLU154PQSP"
encodingsP = "encodings.pickle"

print("[INFO] loading encodings + face detector...")
with open(encodingsP, "rb") as file:
    data = pickle.load(file)

vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
fps = FPS().start()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    boxes = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

        if currentname != name:
            currentname = name
            print(f"Recognized: {currentname}")

            # Display name on LCD
            GPIO.output(16, True)
            lcd.lcd_clear()
            lcd.lcd_display_string("Recognized:", 1)
            lcd.lcd_display_string(currentname, 2)
            sleep(6)
            lcd.lcd_clear()
            lcd.lcd_display_string("Face Recognize", 1)
            lcd.lcd_display_string("Attendance", 2)
            GPIO.output(16, False)

            try:
                WriteURL = f'https://api.thingspeak.com/update?api_key={WRITEKEY}&field1={name}'
                urllib.request.urlopen(WriteURL)
            except Exception as e:
                print(f"Error sending data to ThingSpeak: {e}")

        names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    fps.update()

fps.stop()
print(f"[INFO] Elapsed time: {fps.elapsed():.2f}")
print(f"[INFO] Approx. FPS: {fps.fps():.2f}")
cv2.destroyAllWindows()
vs.stop()
