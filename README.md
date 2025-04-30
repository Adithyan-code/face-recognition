# Face Recognition Attendance System

This project implements a face recognition-based attendance system using Raspberry Pi, PiCamera, and an I2C LCD display. It captures images, trains a face recognition model, and performs live recognition, updating attendance records to ThingSpeak.

## Features

- Capture images using PiCamera
- Train a face recognition model
- Live face recognition with real-time attendance logging
- Display recognized names on an I2C LCD
- Send attendance data to ThingSpeak

## Setup Instructions

1. *Install Dependencies:*
2. *Capture Images:*

Run capture_images.py and press SPACE to capture images. Press ESC to exit.

3. *Train Model:*

Run train_model.py to process and encode the captured images.

4. *Live Recognition:*

Run live_recognition.py to start the live face recognition system.

## Notes

- Ensure your Raspberry Pi has the necessary hardware connected (PiCamera and I2C LCD).
- Replace WRITEKEY in live_recognition.py with your ThingSpeak API key.
- Create a folder named dataset in the project directory before capturing images.

## License
